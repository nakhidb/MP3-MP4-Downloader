import os
import sys
import json
import re
import time
import glob
import logging
import webbrowser
import base64
import shutil
import threading
import hmac
import hashlib
import struct
import requests
import tempfile
import concurrent.futures
from urllib.parse import urlparse
import yt_dlp
# pyrefly: ignore [missing-import]
import webview

try:
    import telemetry
except ImportError:
    try:
        from src import telemetry
    except ImportError:
        telemetry = None

CURRENT_VERSION = "v1.9"
GITHUB_REPO = "nakhidb/MP3-MP4-Downloader"

_WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

def parse_version(value):
    """Return a comparable tuple for tags such as v1.8 or v1.10.2."""
    parts = [int(p) for p in re.findall(r"\d+", str(value or ""))]
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts) or (0,)

def url_host(url):
    try:
        return (urlparse(url).hostname or "").lower()
    except Exception:
        return ""

def is_spotify_url(url):
    host = url_host(url)
    return host == "spotify.com" or host.endswith(".spotify.com")

def is_youtube_url(url):
    host = url_host(url)
    return host in {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com", "youtu.be"} or host.endswith(".youtube.com")

def extract_spotify_id(url, kind):
    """Extract a 22-character Spotify playlist/track/album id from a URL."""
    match = re.search(rf"/{re.escape(kind)}/([A-Za-z0-9]{{22}})", url or "")
    return match.group(1) if match else ""

def sanitize_filename(name, max_length=180):
    """Make a title safe for Windows paths without destroying Unicode."""
    value = str(name or "")
    value = re.sub(r'[\\/*?:"<>|\x00-\x1f]', "", value)
    value = re.sub(r"\s+", " ", value).strip(" .")
    if not value:
        value = "track"
    if value.split(".")[0].strip().upper() in _WINDOWS_RESERVED_NAMES:
        value = f"_{value}"
    if len(value) > max_length:
        value = value[:max_length].rstrip(" .")
    return value or "track"

def video_quality_height(quality):
    if "4K" in quality or "2160" in quality:
        return "2160"
    if "2K" in quality or "1440" in quality:
        return "1440"
    match = re.search(r"(\d+)", quality or "")
    return match.group(1) if match else "1080"

def audio_bitrate(quality):
    match = re.search(r"(\d+)", quality or "")
    return match.group(1) if match else "320"

def find_output_file(save_dir, base_name, ext):
    """Find the real output file. Post-processors can change the final extension."""
    expected = os.path.join(save_dir, f"{base_name}.{str(ext).lower()}")
    if os.path.exists(expected):
        return expected
    candidates = [
        p for p in glob.glob(os.path.join(glob.escape(save_dir), glob.escape(base_name) + ".*"))
        if not p.endswith(".part") and not p.endswith(".ytdl")
    ]
    if not candidates:
        return None
    candidates.sort(key=os.path.getmtime, reverse=True)
    preferred = [p for p in candidates if p.lower().endswith("." + str(ext).lower())]
    return (preferred or candidates)[0]

def cleanup_partial(save_dir, base_name, target_filepath=None, temp_dir=None):
    """Remove a cancelled/crashed download and its .part companions."""
    if not base_name:
        return
    paths = []
    if target_filepath:
        paths.append(target_filepath)
    for folder in (save_dir, temp_dir or tempfile.gettempdir()):
        if not folder:
            continue
        paths.extend(glob.glob(os.path.join(glob.escape(folder), glob.escape(base_name) + ".part")))
        paths.extend(glob.glob(os.path.join(glob.escape(folder), glob.escape(base_name) + ".*.part")))
    for path in set(paths):
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception as exc:
            logging.debug("Could not remove partial file %s: %s", path, exc)

# Get config directory and config file path
def get_config_dir():
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data and os.path.exists(local_app_data):
        config_dir = os.path.join(local_app_data, "TrackDrop")
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".trackdrop")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

def get_cache_dir():
    cache_dir = os.path.join(get_config_dir(), "cache")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def get_config_path():
    return os.path.join(get_config_dir(), "spotify_config.json")

def get_default_download_dir():
    # Prefer standard OS Downloads folder, fallback to user home directory
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    if os.path.exists(downloads_dir):
        return downloads_dir
    return os.path.expanduser("~")

class Bridge:
    def __init__(self):
        self._window = None
        self.download_cancelled = False
        self.active_downloads = {} # to track active download threads
        self._download_lock = threading.Lock()
        self._config_lock = threading.RLock()
        self._spotify_token_cache = {}
        self._anon_token_cache = {}
        self._yt_playlist_cache = {}
        self.ffmpeg_downloading = False
        self.ffmpeg_progress = {
            "status": "idle",
            "pct": 0,
            "downloaded_mb": 0,
            "total_mb": 0,
            "remaining_mb": 0,
            "speed_str": "0.0 MB/s",
            "eta_sec": 0,
            "message": ""
        }
        self.cached_spotify_playlists = {}
        self.cached_playlist_parts = {}
        self._http_session = requests.Session()
        self.update_downloading = False
        self.update_progress = {"status": "idle", "pct": 0, "message": ""}

    def _get_disk_cache(self, filename):
        try:
            cache_file = os.path.join(get_cache_dir(), filename)
            if os.path.exists(cache_file):
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    def _save_disk_cache(self, filename, data):
        try:
            cache_dir = get_cache_dir()
            cache_file = os.path.join(cache_dir, filename)
            temp_file = cache_file + ".tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            os.replace(temp_file, cache_file)
        except Exception as exc:
            logging.debug("Could not save cache %s: %s", filename, exc)

    def _js(self, func, *args):
        """Call a JS function with JSON-encoded arguments (safe for quotes)."""
        payload = ", ".join(json.dumps(arg, ensure_ascii=False) for arg in args)
        self.eval_js(f"window.{func}({payload})")

    def get_ffmpeg_path(self):
        if hasattr(sys, '_MEIPASS'):
            ffmpeg_exe = os.path.join(sys._MEIPASS, "ffmpeg.exe")
            if os.path.exists(ffmpeg_exe):
                return sys._MEIPASS
        # Check ~/.trackdrop/ffmpeg
        config_dir = get_config_dir()
        ffmpeg_dir = os.path.join(config_dir, "ffmpeg")
        ffmpeg_exe = os.path.join(ffmpeg_dir, "ffmpeg.exe")
        if os.path.exists(ffmpeg_exe):
            return ffmpeg_dir
        # Check system path
        ffmpeg_in_path = shutil.which("ffmpeg")
        if ffmpeg_in_path:
            return os.path.dirname(ffmpeg_in_path)
        return None

    def check_ffmpeg(self):
        return self.get_ffmpeg_path() is not None

    def get_ffmpeg_progress(self):
        return self.ffmpeg_progress

    def download_ffmpeg(self):
        if self.ffmpeg_downloading:
            # Already downloading, simply instruct UI to open the modal with current state
            self._js("showFfmpegModal", self.ffmpeg_progress)
            return

        self.ffmpeg_downloading = True
        self._js("showFfmpegModal")

        def worker():
            import time
            import zipfile
            import io

            try:
                if telemetry:
                    telemetry.record_breadcrumb("ffmpeg", "FFmpeg prebuilt download started")
                url = "https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v4.4.1/ffmpeg-4.4.1-win-64.zip"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

                session = requests.Session()
                r = session.get(url, headers=headers, stream=True, timeout=30)
                r.raise_for_status()

                total_length = r.headers.get('content-length')
                config_dir = get_config_dir()
                ffmpeg_dir = os.path.join(config_dir, "ffmpeg")
                os.makedirs(ffmpeg_dir, exist_ok=True)

                zip_data = io.BytesIO()
                start_time = time.time()
                last_update_time = 0

                if total_length is None:
                    zip_data.write(r.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    tot_mb = round(total_length / (1024 * 1024), 1)

                    for chunk in r.iter_content(chunk_size=131072):
                        dl += len(chunk)
                        zip_data.write(chunk)

                        now = time.time()
                        # Update UI stats every 100ms or on completion
                        if now - last_update_time >= 0.1 or dl >= total_length:
                            last_update_time = now
                            elapsed = max(0.001, now - start_time)
                            speed_bps = dl / elapsed
                            speed_mbps = speed_bps / (1024 * 1024)
                            spd_str = f"{speed_mbps:.1f} MB/s" if speed_mbps >= 1.0 else f"{(speed_bps / 1024):.0f} KB/s"

                            remaining_bytes = max(0, total_length - dl)
                            eta_sec = int(remaining_bytes / speed_bps) if speed_bps > 0 else 0

                            pct = int((dl / total_length) * 100)
                            dl_mb = round(dl / (1024 * 1024), 1)
                            rem_mb = round(remaining_bytes / (1024 * 1024), 1)

                            self.ffmpeg_progress = {
                                "status": "downloading",
                                "pct": pct,
                                "downloaded_mb": dl_mb,
                                "total_mb": tot_mb,
                                "remaining_mb": rem_mb,
                                "speed_str": spd_str,
                                "eta_sec": eta_sec,
                                "message": ""
                            }
                            self._js("updateFfmpegModalProgress", self.ffmpeg_progress)

                self.ffmpeg_progress["status"] = "installing"
                self.ffmpeg_progress["pct"] = 100
                self._js("updateFfmpegModalProgress", self.ffmpeg_progress)

                with zipfile.ZipFile(zip_data) as z:
                    base_dir = os.path.abspath(ffmpeg_dir)
                    for member in z.infolist():
                        member_path = os.path.abspath(os.path.join(base_dir, member.filename))
                        if member_path != base_dir and not member_path.startswith(base_dir + os.sep):
                            raise Exception("FFmpeg arxivində təhlükəli fayl yolu aşkarlandı.")
                    z.extractall(base_dir)

                # Some ffbinaries archives contain a nested folder. Normalize the
                # binaries to the expected root so get_ffmpeg_path() can find them.
                expected_ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                if not os.path.exists(expected_ffmpeg):
                    for root, _dirs, files in os.walk(ffmpeg_dir):
                        if "ffmpeg.exe" in files:
                            for binary in ("ffmpeg.exe", "ffprobe.exe"):
                                src = os.path.join(root, binary)
                                dst = os.path.join(ffmpeg_dir, binary)
                                if os.path.exists(src) and os.path.abspath(src) != os.path.abspath(dst):
                                    shutil.copy2(src, dst)
                            break
                if not os.path.exists(expected_ffmpeg):
                    raise Exception("FFmpeg arxivində ffmpeg.exe tapılmadı.")

                self.ffmpeg_progress["status"] = "success"
                self.ffmpeg_downloading = False
                self._js("onFfmpegSuccess")
            except Exception as e:
                if telemetry:
                    telemetry.capture_error(e, {"step": "download_ffmpeg"})
                self.ffmpeg_downloading = False
                self.ffmpeg_progress["status"] = "error"
                self.ffmpeg_progress["message"] = str(e)
                self._js("onFfmpegError", str(e))

        threading.Thread(target=worker, daemon=True).start()

    def check_updates(self):
        def worker():
            try:
                url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
                headers = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    latest_tag = data.get("tag_name", "")
                    if latest_tag:
                        current_parsed = parse_version(CURRENT_VERSION)
                        latest_parsed = parse_version(latest_tag)
                        if latest_parsed > current_parsed:
                            html_url = data.get("html_url", f"https://github.com/{GITHUB_REPO}/releases")
                            # Find .exe asset if available
                            exe_download_url = ""
                            for asset in data.get("assets", []):
                                aname = asset.get("name", "").lower()
                                if aname.endswith(".exe"):
                                    exe_download_url = asset.get("browser_download_url", "")
                                    break

                            self._js("showUpdateNotification", latest_tag, html_url, exe_download_url)
            except Exception as e:
                logging.warning("Error checking updates: %s", e)

        threading.Thread(target=worker, daemon=True).start()

    def download_and_install_update(self, exe_url=""):
        if self.update_downloading:
            return {"status": "already_downloading"}

        self.update_downloading = True

        def worker():
            import subprocess
            try:
                # 1. Fetch release details to ensure we have the direct exe URL
                # and (when GitHub provides it) a SHA-256 digest for verification.
                target_url = exe_url
                expected_digest = ""
                rel_api = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
                headers = {"User-Agent": "Mozilla/5.0"}
                try:
                    r_rel = requests.get(rel_api, headers=headers, timeout=10)
                    if r_rel.status_code == 200:
                        rel_data = r_rel.json()
                        for asset in rel_data.get("assets", []):
                            if not asset.get("name", "").lower().endswith(".exe"):
                                continue
                            asset_url = asset.get("browser_download_url", "")
                            if not target_url or asset_url == target_url:
                                target_url = target_url or asset_url
                                expected_digest = asset.get("digest", "") or ""
                                if target_url == asset_url:
                                    break
                except Exception as exc:
                    logging.warning("Could not fetch release metadata: %s", exc)

                if not target_url:
                    raise Exception("Release-də .exe faylı tapılmadı!")

                self._js("updateUpdaterProgress", 5, "Yenilənmə faylı yüklənir...")

                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                r = requests.get(target_url, headers=headers, stream=True, timeout=30)
                r.raise_for_status()

                total_len = r.headers.get("content-length")
                total_bytes = int(total_len) if total_len else 0

                temp_dir = tempfile.gettempdir()
                new_exe_path = os.path.join(temp_dir, "TrackDrop_Update.exe")

                downloaded = 0
                last_time = time.time()
                hasher = hashlib.sha256()
                with open(new_exe_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        if not chunk:
                            continue
                        f.write(chunk)
                        hasher.update(chunk)
                        downloaded += len(chunk)
                        now = time.time()
                        if now - last_time >= 0.15:
                            last_time = now
                            if total_bytes > 0:
                                pct = min(95, int((downloaded / total_bytes) * 90) + 5)
                                self._js("updateUpdaterProgress", pct, f"{pct}% yükləndi...")

                if downloaded == 0:
                    raise Exception("Yenilənmə faylı boşdur.")
                if expected_digest.lower().startswith("sha256:"):
                    actual_digest = hasher.hexdigest().lower()
                    if not hmac.compare_digest(actual_digest, expected_digest.split(":", 1)[1].lower()):
                        try:
                            os.remove(new_exe_path)
                        except OSError:
                            pass
                        raise Exception("Yenilənmə faylının SHA-256 yoxlaması uğursuz oldu.")

                self._js("updateUpdaterProgress", 98, "Quraşdırılır və yenidən başladılır...")
                time.sleep(0.5)

                # Determine the current running exe path
                current_exe = sys.executable
                if not getattr(sys, 'frozen', False):
                    # In development, target TrackDrop.exe in the project root.
                    # Never replace the Python interpreter that runs the source
                    # build if that exe is missing.
                    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    possible_exe = os.path.join(root_dir, "TrackDrop.exe")
                    if os.path.exists(possible_exe):
                        current_exe = possible_exe
                    else:
                        raise Exception(
                            "Avtomatik yeniləmə yalnız quraşdırılmış TrackDrop.exe üçün mövcuddur."
                        )

                updater_bat = os.path.join(temp_dir, "trackdrop_updater.bat")
                clean_env = os.environ.copy()
                clean_env.pop("_MEIPASS2", None)
                clean_env.pop("_MEIPASS", None)
                exe_dir = os.path.dirname(os.path.abspath(current_exe))
                current_pid = os.getpid()

                bat_content = f"""@echo off
set _MEIPASS2=
set _MEIPASS=
timeout /t 1 /nobreak >nul
taskkill /f /pid {current_pid} >nul 2>&1
timeout /t 1 /nobreak >nul
:wait_loop
if exist "{current_exe}" (
    move /y "{current_exe}" "{current_exe}.bak" >nul 2>&1
)
if exist "{current_exe}" (
    timeout /t 1 /nobreak >nul
    goto wait_loop
)
move /y "{new_exe_path}" "{current_exe}" >nul 2>&1
if not exist "{current_exe}" (
    if exist "{current_exe}.bak" move /y "{current_exe}.bak" "{current_exe}" >nul 2>&1
    if exist "{current_exe}" start "" "{current_exe}"
    del "%~f0" >nul 2>&1
    exit
)
timeout /t 1 /nobreak >nul
cd /d "{exe_dir}"
start "" "{current_exe}"
del "{current_exe}.bak" >nul 2>&1
del "%~f0" >nul 2>&1
exit
"""
                with open(updater_bat, "w", encoding="utf-8") as bf:
                    bf.write(bat_content)

                # Launch updater batch detached with clean environment
                subprocess.Popen(
                    ["cmd.exe", "/c", updater_bat],
                    env=clean_env,
                    cwd=exe_dir,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
                )

                self._js("updateUpdaterProgress", 100, "Uğurlu! Yenidən başladılır...")
                time.sleep(0.8)
                if self._window:
                    try:
                        self._window.destroy()
                    except Exception as exc:
                        logging.warning("Could not destroy window during update: %s", exc)

            except Exception as e:
                logging.error("Update install error: %s", e)
                self.update_downloading = False
                self._js("onUpdaterError", str(e))

        threading.Thread(target=worker, daemon=True).start()
        return {"status": "started"}

    def open_external_url(self, url):
        if urlparse(url or "").scheme not in ("http", "https"):
            return {"success": False, "error": "invalid_url"}
        webbrowser.open(url)
        return {"success": True}

    # login_with_spotify removed as requested (Spotify blocks direct auth token endpoint)

    def _read_config(self):
        path = get_config_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except Exception as exc:
                logging.warning("Could not read config: %s", exc)
        return {}

    def _write_config(self, data):
        path = get_config_path()
        temp_path = path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, path)

    def get_spotify_config(self):
        with self._config_lock:
            data = self._read_config()
        return {
            "client_id": str(data.get("client_id", "") or ""),
            "client_secret": str(data.get("client_secret", "") or ""),
            "api_key": str(data.get("api_key", "") or ""),
            "download_dir": str(data.get("download_dir", "") or ""),
        }

    def get_download_dir(self):
        config = self.get_spotify_config()
        configured_dir = config.get("download_dir", "").strip()
        if configured_dir and os.path.isdir(configured_dir):
            return configured_dir
        return get_default_download_dir()

    def set_download_dir(self, new_dir):
        new_dir = (new_dir or "").strip()
        if not new_dir or not os.path.isdir(new_dir):
            return {"success": False, "error": "Folder does not exist"}
        try:
            with self._config_lock:
                data = self._read_config()
                data["download_dir"] = new_dir
                self._write_config(data)
            return {"success": True, "download_dir": new_dir}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def choose_download_dir(self):
        if not self._window:
            return None
        current_dir = self.get_download_dir()
        dialog_type = (
            webview.FileDialog.FOLDER
            if hasattr(webview, "FileDialog")
            else webview.FOLDER_DIALOG
        )
        dialog_res = self._window.create_file_dialog(
            dialog_type=dialog_type,
            directory=current_dir if os.path.exists(current_dir) else ""
        )
        if dialog_res and len(dialog_res) > 0:
            chosen = dialog_res[0]
            if chosen and os.path.isdir(chosen):
                self.set_download_dir(chosen)
                return chosen
        return None

    def save_spotify_config(self, api_key_or_id, client_secret=""):
        api_key_or_id = (api_key_or_id or "").strip()
        client_secret = (client_secret or "").strip()

        if not api_key_or_id and not client_secret:
            return {"success": False, "error": "empty"}

        # A 32-char hex value is a Client ID, not a Bearer token.
        if not client_secret and re.fullmatch(r"[0-9a-fA-F]{32}", api_key_or_id):
            return {"success": False, "error": "client_secret_required"}

        try:
            with self._config_lock:
                data = self._read_config()
                if client_secret:
                    data.update({
                        "client_id": api_key_or_id,
                        "client_secret": client_secret,
                        "api_key": "",
                    })
                else:
                    data.update({
                        "client_id": "",
                        "client_secret": "",
                        "api_key": api_key_or_id,
                    })
                self._write_config(data)
            self._spotify_token_cache = {}
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_spotify_auth(self, client_id="", client_secret="", api_key=""):
        try:
            api_key = (api_key or "").strip()
            client_id = (client_id or "").strip()
            client_secret = (client_secret or "").strip()

            # 1. Direct Bearer/API token
            if api_key:
                headers = {"Authorization": f"Bearer {api_key}"}
                r = requests.get(
                    "https://api.spotify.com/v1/playlists/37i9dQZF1DXcBWIGoYBM5M/tracks?limit=1",
                    headers=headers,
                    timeout=8
                )
                if r.status_code == 200:
                    return {"authenticated": True, "token": api_key}
                # A stale saved token should not hide valid client credentials.
                if not (client_id and client_secret):
                    return {"authenticated": False, "error": "invalid_token"}

            # 2. Client ID + Secret, with a small in-memory token cache
            if client_id and client_secret:
                now = time.time()
                cached = self._spotify_token_cache
                if (
                    cached.get("token")
                    and cached.get("client_id") == client_id
                    and cached.get("client_secret") == client_secret
                    and cached.get("expires", 0) > now + 15
                ):
                    return {"authenticated": True, "token": cached["token"]}

                auth_url = "https://accounts.spotify.com/api/token"
                auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
                headers = {
                    "Authorization": f"Basic {auth_header}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                r = requests.post(auth_url, headers=headers, data={"grant_type": "client_credentials"}, timeout=10)
                if r.status_code == 200:
                    payload = r.json()
                    token = payload.get("access_token")
                    if token:
                        expires_in = int(payload.get("expires_in", 3600) or 3600)
                        self._spotify_token_cache = {
                            "token": token,
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "expires": now + expires_in,
                        }
                        return {"authenticated": True, "token": token}
                return {"authenticated": False, "error": "invalid_credentials"}
        except Exception as e:
            logging.warning("Spotify auth error: %s", e)
        return {"authenticated": False}

    def _get_spotify_anonymous_token(self):
        now = time.time()
        cached = self._anon_token_cache
        if cached.get("token") and cached.get("expires", 0) > now + 30:
            return cached["token"]

        fallback_secret = (
            61,
            bytearray([44,55,47,42,70,40,34,114,76,74,50,111,120,97,75,76,94,102,43,69,49,120,118,80,64,78])
        )
        try:
            try:
                res = requests.get(
                    "https://code.thetadev.de/ThetaDev/spotify-secrets/raw/branch/main/secrets/secretDict.json",
                    timeout=3
                )
                if res.ok:
                    secrets = res.json()
                    version = max(secrets, key=int)
                    secret_bytes = bytearray(secrets[version])
                else:
                    version, secret_bytes = fallback_secret
            except Exception:
                version, secret_bytes = fallback_secret

            transformed = [e ^ ((t % 33) + 9) for t, e in enumerate(secret_bytes)]
            joined = "".join(str(num) for num in transformed)
            hex_str = joined.encode().hex()
            secret = base64.b32encode(bytes.fromhex(hex_str)).decode().rstrip("=")

            key = base64.b32decode(secret + "=" * ((8 - len(secret) % 8) % 8))
            intervals_no = int(time.time()) // 30
            msg = struct.pack(">Q", intervals_no)
            h = hmac.new(key, msg, hashlib.sha1).digest()
            o = h[19] & 15
            h_int = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
            totp = f"{h_int:06d}"

            params = {
                "reason": "init",
                "productType": "web-player",
                "totp": totp,
                "totpVer": str(version),
                "totpServer": totp,
            }
            r = requests.get(
                "https://open.spotify.com/api/token",
                params=params,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=5,
            )
            if r.status_code == 200:
                token = r.json().get("accessToken")
                if token:
                    self._anon_token_cache = {
                        "token": token,
                        "expires": now + 1800,
                    }
                    return token
        except Exception as e:
            logging.warning("Error getting anonymous Spotify token: %s", e)
        return None

    def get_spotify_playlist_track_ids(self, playlist_id):
        """Fetch all track IDs for a Spotify playlist using anonymous session."""
        try:
            token = self._get_spotify_anonymous_token()
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                r = requests.get(
                    f"https://spclient.wg.spotify.com/playlist/v2/playlist/{playlist_id}",
                    headers=headers,
                    timeout=8
                )
                if r.status_code == 200:
                    raw_ids = re.findall(b"spotify:track:([a-zA-Z0-9]{22})", r.content)
                    if raw_ids:
                        return [tid.decode("ascii") for tid in raw_ids]
        except Exception as e:
            print(f"Error fetching track IDs from spclient: {e}")
        return []

    def get_spotify_playlist_total(self, playlist_id):
        """Fetch total song count from Spotify public playlist page."""
        try:
            url = f"https://open.spotify.com/playlist/{playlist_id}"
            headers = {
                "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
                "Accept-Language": "en-US,en;q=0.9"
            }
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code == 200:
                # 1. music:song_count meta tag
                m1 = re.search(r'name=["\']music:song_count["\']\s+content=["\'](\d+)["\']', r.text)
                if not m1:
                    m1 = re.search(r'content=["\'](\d+)["\']\s+name=["\']music:song_count["\']', r.text)
                if not m1:
                    m1 = re.search(r'music:song_count["\']?\s+content=["\']?(\d+)', r.text)
                if m1:
                    return int(m1.group(1))

                # 2. og:description or description meta tag containing items count
                m2 = re.search(r'(?:items|tracks|songs)\s*·\s*(\d+)', r.text, re.IGNORECASE)
                if not m2:
                    m2 = re.search(r'(\d+)\s+(?:items|tracks|songs|mahnı)', r.text, re.IGNORECASE)
                if m2:
                    return int(m2.group(1))

                # 3. JSON in script tags (initial-state / session)
                m3 = re.search(r'"total(?:Tracks|Length)?":\s*(\d+)', r.text)
                if m3:
                    return int(m3.group(1))
        except Exception as e:
            print(f"Error getting spotify playlist total: {e}")
        return None

    def _fetch_single_track_embed(self, track_id):
        """Fetch title, artist, duration and thumbnail for a single Spotify track."""
        try:
            url = f"https://open.spotify.com/embed/track/{track_id}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }
            r = self._http_session.get(url, headers=headers, timeout=4)
            if r.status_code == 200:
                pattern = r'<script\s+id="__NEXT_DATA__"\s+type="application/json">([^<]+)</script>'
                m = re.search(pattern, r.text)
                if m:
                    import html as html_mod
                    js_data = json.loads(html_mod.unescape(m.group(1)))
                    entity = js_data.get("props", {}).get("pageProps", {}).get("state", {}).get("data", {}).get("entity", {})
                    title = entity.get("name", "")
                    artists = ", ".join([a.get("name", "") for a in entity.get("artists", []) if a.get("name")])
                    duration = entity.get("duration", 0) // 1000
                    images = entity.get("visualIdentity", {}).get("image", [])
                    thumb = images[0].get("url", "") if images else ""
                    return {
                        "title": title,
                        "artist": artists,
                        "duration": duration,
                        "thumbnail": thumb,
                        "url": f"ytsearch1:{artists} - {title}" if artists else f"ytsearch1:{title}"
                    }
        except Exception as exc:
            logging.debug("Spotify embed parse failed: %s", exc)

        # Fallback to oembed
        try:
            r = self._http_session.get(f"https://open.spotify.com/oembed?url=https://open.spotify.com/track/{track_id}", timeout=3.5)
            if r.status_code == 200:
                odata = r.json()
                title = odata.get("title", "")
                thumb = odata.get("thumbnail_url", "")
                return {
                    "title": title,
                    "artist": "",
                    "duration": 0,
                    "thumbnail": thumb,
                    "url": f"ytsearch1:{title}"
                }
        except Exception as exc:
            logging.debug("Spotify oembed fallback failed: %s", exc)
        return None

    def _fetch_single_track_thumbnail(self, track_id):
        """Fast fetch thumbnail URL for a track using oembed."""
        if not track_id:
            return ""
        try:
            r = self._http_session.get(f"https://open.spotify.com/oembed?url=https://open.spotify.com/track/{track_id}", timeout=3.5)
            if r.status_code == 200:
                return r.json().get("thumbnail_url", "")
        except Exception as exc:
            logging.debug("Spotify thumbnail fetch failed: %s", exc)
        return ""

    def get_spotify_playlist_no_api(self, playlist_id, offset=0, limit=100):
        """Fetch Spotify playlist tracks with real pagination support, disk caching and throttled workers."""
        cache_key = (playlist_id, offset, limit)
        if cache_key in self.cached_playlist_parts:
            return self.cached_playlist_parts[cache_key]

        disk_part_file = f"pl_{playlist_id}_part_{offset}_{limit}.json"
        disk_cached_part = self._get_disk_cache(disk_part_file)
        if disk_cached_part and disk_cached_part.get("tracks"):
            self.cached_playlist_parts[cache_key] = disk_cached_part
            return disk_cached_part

        try:
            import html as html_mod
            cached_data = self.cached_spotify_playlists.get(playlist_id, {})
            playlist_name = cached_data.get("name")
            all_track_ids = cached_data.get("track_ids")

            disk_meta_file = f"pl_{playlist_id}_meta.json"
            if not all_track_ids or not playlist_name:
                disk_meta = self._get_disk_cache(disk_meta_file)
                if disk_meta:
                    playlist_name = playlist_name or disk_meta.get("name")
                    all_track_ids = all_track_ids or disk_meta.get("track_ids")

            if not all_track_ids:
                all_track_ids = self.get_spotify_playlist_track_ids(playlist_id)
            total = self.get_spotify_playlist_total(playlist_id)
            if not total:
                total = len(all_track_ids) if all_track_ids else None

            # If requesting Part 1 (offset == 0), get rich track data instantly from embed page
            if offset == 0:
                embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                }
                r = self._http_session.get(embed_url, headers=headers, timeout=12)
                if r.status_code == 200:
                    pattern = r'<script\s+id="__NEXT_DATA__"\s+type="application/json">([^<]+)</script>'
                    m = re.search(pattern, r.text)
                    if m:
                        js_data = json.loads(html_mod.unescape(m.group(1)))
                        entity = js_data.get("props", {}).get("pageProps", {}).get("state", {}).get("data", {}).get("entity", {})
                        playlist_name = entity.get("title") or entity.get("name") or playlist_name or "Spotify Playlist"
                        track_list = entity.get("trackList", [])

                        track_ids_for_thumbs = []
                        for item in track_list:
                            uri = item.get("uri", "")
                            tid = uri.split(":")[-1] if uri else ""
                            track_ids_for_thumbs.append(tid)

                        # Parallel fetch for thumbnails with CPU-safe worker count (8)
                        thumbnails = []
                        if track_ids_for_thumbs:
                            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                                thumbnails = list(executor.map(self._fetch_single_track_thumbnail, track_ids_for_thumbs))

                        tracks = []
                        for idx, item in enumerate(track_list):
                            title = item.get("title", "")
                            artist = item.get("subtitle", "")
                            duration_ms = item.get("duration", 0)
                            duration_sec = duration_ms // 1000
                            thumb = thumbnails[idx] if idx < len(thumbnails) else ""
                            tracks.append({
                                "title": title,
                                "artist": artist,
                                "duration": duration_sec,
                                "thumbnail": thumb,
                                "url": f"ytsearch1:{artist} - {title}"
                            })

                        if total is None or total < len(tracks):
                            total = len(all_track_ids) if all_track_ids else len(tracks)

                        self.cached_spotify_playlists[playlist_id] = {
                            "name": playlist_name,
                            "track_ids": all_track_ids,
                            "total": total
                        }
                        self._save_disk_cache(disk_meta_file, {
                            "name": playlist_name,
                            "track_ids": all_track_ids,
                            "total": total
                        })

                        res = {
                            "playlist_name": playlist_name,
                            "tracks": tracks,
                            "total_tracks": total,
                            "is_partial": (total > len(tracks)),
                            "has_api": False
                        }
                        self.cached_playlist_parts[cache_key] = res
                        self._save_disk_cache(disk_part_file, res)
                        return res

            # If offset > 0 (Part 2, Part 3, etc.), fetch tracks from discovered track IDs
            if all_track_ids:
                sub_ids = all_track_ids[offset:offset+limit]
                tracks = []
                # Throttled to 8 workers to prevent 100% CPU lockup
                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                    results = list(executor.map(self._fetch_single_track_embed, sub_ids))
                tracks = [t for t in results if t]

                if not total:
                    total = len(all_track_ids)

                playlist_name = playlist_name or "Spotify Playlist"
                res = {
                    "playlist_name": playlist_name,
                    "tracks": tracks,
                    "total_tracks": total,
                    "is_partial": (total > (offset + len(tracks))),
                    "has_api": False
                }
                self.cached_playlist_parts[cache_key] = res
                self._save_disk_cache(disk_part_file, res)
                return res

            return None
        except Exception as e:
            print(f"Error scraping Spotify playlist: {e}")
            return None

    def fetch_playlist(self, url, offset=0, limit=100):
        url = (url or "").strip()
        if not url:
            return {"error": "empty_url"}

        try:
            offset = max(0, int(offset))
        except (TypeError, ValueError):
            offset = 0
        try:
            limit = max(1, min(100, int(limit)))
        except (TypeError, ValueError):
            limit = 100

        is_spotify = is_spotify_url(url)
        is_youtube = is_youtube_url(url)

        # Prevent single-track links in the playlist tab.
        if is_spotify and "/track/" in url:
            return {"error": "single_track_in_playlist"}
        if is_youtube and ("list=" not in url and "/playlist" not in url):
            return {"error": "single_track_in_playlist"}

        # 1. Spotify playlist
        if is_spotify and "/playlist/" in url:
            playlist_id = extract_spotify_id(url, "playlist")
            if not playlist_id:
                return {"error": "invalid_spotify_url"}

            config = self.get_spotify_config()
            client_id = config.get("client_id", "")
            client_secret = config.get("client_secret", "")
            api_key = config.get("api_key", "")

            auth_res = self.check_spotify_auth(client_id, client_secret, api_key)
            auth_error = False
            if auth_res.get("authenticated"):
                token = auth_res.get("token")
                tracks = []
                headers = {"Authorization": f"Bearer {token}"}

                try:
                    r_playlist = requests.get(
                        f"https://api.spotify.com/v1/playlists/{playlist_id}",
                        headers=headers,
                        timeout=10,
                    )
                    playlist_name = "Spotify Playlist"
                    total_tracks = 0
                    if r_playlist.status_code == 200:
                        pdata = r_playlist.json()
                        playlist_name = pdata.get("name", "Spotify Playlist")
                        total_tracks = pdata.get("tracks", {}).get("total", 0)

                    fetch_url = (
                        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
                        f"?offset={offset}&limit={limit}"
                    )
                    r_tracks = requests.get(fetch_url, headers=headers, timeout=15)
                    status = r_tracks.status_code
                    if status == 200:
                        data = r_tracks.json()
                        if not total_tracks:
                            total_tracks = data.get("total", 0)
                        for item in data.get("items", []):
                            track = item.get("track")
                            if not track:
                                continue
                            name = track.get("name", "")
                            artists = [a.get("name", "") for a in track.get("artists", [])]
                            artist_str = ", ".join(artists)
                            duration_ms = track.get("duration_ms", 0)
                            duration_sec = duration_ms // 1000
                            album = track.get("album", {})
                            images = album.get("images", [])
                            thumb = images[0].get("url", "") if images else ""
                            tracks.append({
                                "title": name,
                                "artist": artist_str,
                                "duration": duration_sec,
                                "thumbnail": thumb,
                                "url": f"ytsearch1:{artist_str} - {name}"
                            })
                        res_api = {
                            "playlist_name": playlist_name,
                            "tracks": tracks,
                            "total_tracks": total_tracks or len(tracks),
                            "offset": offset,
                            "limit": limit,
                            "has_api": True,
                            "source": "spotify",
                        }
                        self._save_disk_cache(
                            f"pl_{playlist_id}_part_{offset}_{limit}.json", res_api
                        )
                        return res_api
                    if status in (401, 403):
                        # Never wipe the user's credentials because a token expired.
                        auth_error = True
                        self._spotify_token_cache = {}
                        logging.warning("Spotify token rejected (%s); falling back to public page", status)
                except Exception as e:
                    logging.warning("Spotify API fetch error: %s", e)

            # Fallback to embed scraper & anonymous pagination
            embed_res = self.get_spotify_playlist_no_api(playlist_id, offset=offset, limit=limit)
            if embed_res and embed_res.get("tracks"):
                embed_res["offset"] = offset
                embed_res["limit"] = limit
                embed_res["source"] = "spotify"
                return embed_res

            if auth_error:
                return {"error": "spotify_token_invalid"}
            return {"error": "spotify_fetch_failed"}

        # 2. YouTube playlist / extract_flat
        if is_youtube:
            try:
                now = time.time()
                cached = self._yt_playlist_cache.get(url)
                if cached and cached.get("expires", 0) > now:
                    playlist_name, all_entries = cached["name"], cached["entries"]
                else:
                    ydl_opts = {
                        'extract_flat': True,
                        'quiet': True,
                        'skip_download': True,
                        'no_warnings': True,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                    playlist_name = info.get('title', 'YouTube Playlist')
                    all_entries = [entry for entry in (info.get('entries') or []) if entry]
                    self._yt_playlist_cache = {
                        url: {
                            "name": playlist_name,
                            "entries": all_entries,
                            "expires": now + 1800,
                        }
                    }

                total_tracks = len(all_entries)
                selected_entries = all_entries[offset:offset + limit]
                tracks = []
                for entry in selected_entries:
                    thumbs = entry.get('thumbnails') or []
                    thumb = entry.get('thumbnail') or (thumbs[-1].get('url', '') if thumbs else '')
                    vid_id = entry.get('id')
                    track_url = entry.get('url') or entry.get('webpage_url')
                    if vid_id and (not track_url or not str(track_url).startswith("http")):
                        track_url = f"https://www.youtube.com/watch?v={vid_id}"
                    tracks.append({
                        "title": entry.get('title', 'YouTube Video'),
                        "artist": entry.get('uploader') or entry.get('channel') or 'Unknown Artist',
                        "duration": entry.get('duration', 0) or 0,
                        "thumbnail": thumb,
                        "url": track_url,
                    })
                return {
                    "playlist_name": playlist_name,
                    "tracks": tracks,
                    "total_tracks": total_tracks,
                    "offset": offset,
                    "limit": limit,
                    "has_api": False,
                    "source": "youtube",
                }
            except Exception as e:
                logging.warning("YouTube playlist fetch error: %s", e)
                return {"error": str(e)}

        return {"error": "unsupported_playlist_url"}

    def cancel_download(self):
        self.download_cancelled = True

    def get_spotify_track_info_no_api(self, url):
        try:
            import html
            track_id = extract_spotify_id(url, "track")
            if not track_id:
                return None
            embed_url = f"https://open.spotify.com/embed/track/{track_id}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            r = requests.get(embed_url, headers=headers, timeout=10)
            if r.status_code == 200:
                content = r.text
                next_data_match = re.search(r'<script\s+id="__NEXT_DATA__"\s+type="application/json">([^<]+)</script>', content)
                if next_data_match:
                    js_str = html.unescape(next_data_match.group(1))
                    js_data = json.loads(js_str)
                    entity = js_data.get("props", {}).get("pageProps", {}).get("state", {}).get("data", {}).get("entity", {})
                    if entity:
                        title = entity.get("title") or entity.get("name")
                        if not title:
                            return None
                        artists = [a.get("name") for a in entity.get("artists", [])]
                        artist_str = ", ".join(name for name in artists if name)
                        return f"{artist_str} - {title}" if artist_str else title
        except Exception as e:
            print(f"Error scraping Spotify track: {e}")
        return None

    def get_base_ydl_opts(self):
        opts = {
            'extractor_args': {
                'youtube': {
                    # tv_embedded + skip webpage triggers visionos fallback which bypasses SABR restrictions
                    # Do NOT add android_vr or web as fallbacks, as they trigger SABR/PO Token errors!
                    'player_client': ['tv_embedded'],
                    'skip': ['webpage'],
                }
            },
            'geo_bypass': True,
            'concurrent_fragment_downloads': 8,
            'buffersize': 2097152,
            'http_chunk_size': 10485760,
            'retries': 15,
            'fragment_retries': 15,
            'file_access_retries': 5,
        }
        return opts

    def _unique_base_name(self, save_dir, title, ext):
        clean_title = sanitize_filename(title)
        base_name = clean_title
        counter = 1
        while counter < 1000:
            # Check every companion file, not just the target extension. A
            # crashed previous attempt may have left a different container
            # extension or an unfinished partial behind.
            existing = glob.glob(
                os.path.join(glob.escape(save_dir), glob.escape(base_name) + ".*")
            )
            if not existing:
                return base_name
            base_name = f"{clean_title} ({counter})"
            counter += 1
        return f"{clean_title} ({int(time.time())})"

    def _build_ydl_opts(self, save_dir, base_name, quality, ext, is_audio, progress_hooks=None):
        opts = self.get_base_ydl_opts()
        opts.update({
            # yt-dlp treats % as a template marker; escape any literal percent
            # signs that came from the video title.
            'outtmpl': base_name.replace('%', '%%') + '.%(ext)s',
            'paths': {
                'home': save_dir,
                'temp': tempfile.gettempdir(),
            },
            'progress_hooks': progress_hooks or [],
            'quiet': True,
            'overwrites': False,
            'noplaylist': True,
        })

        if is_audio:
            opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': str(ext).lower(),
                    'preferredquality': audio_bitrate(quality),
                }],
            })
        else:
            height = video_quality_height(quality)
            if str(ext).lower() == "mp4":
                # Prefer MP4-compatible codecs so the final remux never fails
                # with VP9/Opus streams inside an MP4 container.
                fmt = (
                    f"bestvideo[ext=mp4][vcodec^=avc1][height<={height}]+bestaudio[ext=m4a]/"
                    f"best[ext=mp4][height<={height}]"
                )
                opts['postprocessor_args'] = ['-c:v', 'copy', '-c:a', 'aac']
            else:
                fmt = (
                    f"bestvideo[height<={height}]+bestaudio/"
                    f"best[height<={height}]"
                )
                opts['postprocessor_args'] = ['-c', 'copy']
            opts.update({
                'format': fmt,
                'merge_output_format': str(ext).lower(),
            })

        ffmpeg_location = self.get_ffmpeg_path()
        if ffmpeg_location:
            opts['ffmpeg_location'] = ffmpeg_location
        return opts

    def download_single(self, url, media_type, quality, ext):
        url = (url or "").strip()
        if not self._download_lock.locked():
            self.download_cancelled = False

        def worker():
            if not self._download_lock.acquire(blocking=False):
                self._js("onDownloadBusy")
                return

            save_dir = None
            base_name = None
            target_filepath = None
            try:
                if not self.check_ffmpeg():
                    self._js("updateDownloadProgress", 0, "cancelled", "FFmpeg tələb olunur.")
                    self._js("showFfmpegModal")
                    return

                if telemetry:
                    telemetry.record_breadcrumb("download_single", "Single download initiated", {
                        "media_type": media_type,
                        "quality": quality,
                        "ext": ext,
                        "is_spotify": is_spotify_url(url),
                    })

                if not url:
                    raise Exception("ERROR_EMPTY_URL")
                if is_spotify_url(url) and "/playlist/" in url:
                    raise Exception("ERROR_PLAYLIST_IN_SINGLE")
                if is_youtube_url(url) and (
                    "/playlist" in url or ("list=" in url and "v=" not in url)
                ):
                    raise Exception("ERROR_PLAYLIST_IN_SINGLE")

                parsed = urlparse(url)
                if not url.startswith("ytsearch") and parsed.scheme not in ("http", "https"):
                    raise Exception("ERROR_UNSUPPORTED_URL")

                self._js("updateDownloadProgress", 0, "extracting", "Video məlumatları alınır...")

                resolved_url = url
                spotify_title = None
                if is_spotify_url(url) and "/track/" in url:
                    spotify_title = self.get_spotify_track_info_no_api(url)
                    if spotify_title:
                        resolved_url = f"ytsearch1:{spotify_title}"
                    else:
                        config = self.get_spotify_config()
                        auth_res = self.check_spotify_auth(
                            config.get("client_id", ""),
                            config.get("client_secret", ""),
                            config.get("api_key", ""),
                        )
                        if not auth_res.get("authenticated"):
                            self._js("updateDownloadProgress", 0, "cancelled", "Spotify məlumatı üçün giriş tələb olunur.")
                            self._js("showSpotifyAuthModal")
                            return
                        track_id = extract_spotify_id(url, "track")
                        if not track_id:
                            raise Exception("Spotify trek ID-si tapılmadı.")
                        r_track = requests.get(
                            f"https://api.spotify.com/v1/tracks/{track_id}",
                            headers={"Authorization": f"Bearer {auth_res.get('token')}"},
                            timeout=10,
                        )
                        if r_track.status_code != 200:
                            raise Exception("Spotify trek məlumatı alınmadı.")
                        track_info = r_track.json()
                        name = track_info.get("name", "")
                        artists = ", ".join(
                            a.get("name", "") for a in track_info.get("artists", [])
                        )
                        spotify_title = f"{artists} - {name}"
                        resolved_url = f"ytsearch1:{spotify_title}"

                base_opts = self.get_base_ydl_opts()
                base_opts.update({'quiet': True, 'extract_flat': True, 'skip_download': True})
                with yt_dlp.YoutubeDL(base_opts) as ydl:
                    info = ydl.extract_info(resolved_url, download=False)
                if not info:
                    raise Exception("Video məlumatı tapılmadı.")
                entries = info.get('entries') if isinstance(info, dict) else None
                if entries:
                    video_title = entries[0].get('title', 'video') if entries[0] else 'video'
                else:
                    video_title = info.get('title', 'video')
                if spotify_title:
                    video_title = spotify_title

                save_dir = self.get_download_dir()
                os.makedirs(save_dir, exist_ok=True)
                base_name = self._unique_base_name(save_dir, video_title, ext)
                target_filepath = os.path.join(save_dir, f"{base_name}.{str(ext).lower()}")
                self._js("updateDownloadProgress", 0, "downloading", "Yüklənir...")

                last_emit = [0.0]

                def ytdl_hook(d):
                    if self.download_cancelled:
                        raise Exception("DOWNLOAD_CANCELLED")
                    status = d.get('status')
                    if status == 'downloading':
                        now = time.monotonic()
                        if now - last_emit[0] < 0.15:
                            return
                        last_emit[0] = now
                        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                        downloaded = d.get('downloaded_bytes', 0) or 0
                        if total > 0:
                            pct = max(0, min(99, int(downloaded / total * 100)))
                            dl_mb = downloaded / (1024 * 1024)
                            tot_mb = total / (1024 * 1024)
                            speed = d.get('speed') or 0
                            spd_str = f"{speed / (1024 * 1024):.1f} MB/s" if speed else "0.0 MB/s"
                            detail = f"{dl_mb:.1f} MB / {tot_mb:.1f} MB  |  Sürət: {spd_str}"
                            self._js("updateDownloadProgress", pct, "downloading", detail)
                    elif status == 'finished':
                        self._js("updateDownloadProgress", 100, "downloading", "Yüklənir...")

                is_audio = str(media_type).lower() in ["audio", "audio_lbl", "səs", "səsləndi"]
                opts = self._build_ydl_opts(
                    save_dir, base_name, quality, ext, is_audio, [ytdl_hook]
                )
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([resolved_url])

                if self.download_cancelled:
                    raise Exception("DOWNLOAD_CANCELLED")

                actual_path = find_output_file(save_dir, base_name, ext)
                if not actual_path:
                    raise Exception("Yükləmə tamamlandı, amma fayl tapılmadı.")
                filename = os.path.basename(actual_path)
                self._js("updateDownloadProgress", 100, "success", filename)
                self._js("addHistoryItem", filename)
                self._js("showInAppToast", f"✓ {filename}", "success")

            except Exception as e:
                err = str(e)
                if "DOWNLOAD_CANCELLED" in err:
                    cleanup_partial(save_dir, base_name, target_filepath)
                    self._js("updateDownloadProgress", 0, "cancelled", "Yükləmə ləğv edildi.")
                elif "ERROR_PLAYLIST_IN_SINGLE" in err:
                    self._js("updateDownloadProgress", 0, "error", "ERROR_PLAYLIST_IN_SINGLE")
                elif "ERROR_EMPTY_URL" in err:
                    self._js("updateDownloadProgress", 0, "error", "Link boşdur.")
                elif "ERROR_UNSUPPORTED_URL" in err:
                    self._js("updateDownloadProgress", 0, "error", "Yalnız http(s) linkləri dəstəklənir.")
                else:
                    logging.error("Single download failed: %s", e)
                    if telemetry:
                        telemetry.capture_error(e, {
                            "step": "download_single",
                            "media_type": media_type,
                            "quality": quality,
                            "ext": ext,
                        })
                    self._js("updateDownloadProgress", 0, "error", f"Xəta: {err}")
            finally:
                self._js("resetDownloadButton")
                self._download_lock.release()

        threading.Thread(target=worker, daemon=True).start()
        return {"status": "started"}

    def download_selected_tracks(self, tracks, is_audio, media_type, quality, ext):
        if not isinstance(tracks, list) or not tracks:
            self._js("resetPlaylistDownloadState")
            return {"status": "empty"}

        is_audio = bool(is_audio) or str(media_type).lower() in ["audio", "audio_lbl", "səs", "səsləndi"]
        if not self._download_lock.locked():
            self.download_cancelled = False

        def worker():
            if not self._download_lock.acquire(blocking=False):
                self._js("onDownloadBusy")
                return

            try:
                if not self.check_ffmpeg():
                    self._js("showInAppToast", "FFmpeg tələb olunur.", "error")
                    self._js("showFfmpegModal")
                    return

                save_dir = self.get_download_dir()
                os.makedirs(save_dir, exist_ok=True)
                total_tracks = len(tracks)
                success_count = 0
                failed_count = 0
                if telemetry:
                    telemetry.record_breadcrumb("playlist", f"Batch download started: {total_tracks} tracks", {
                        "is_audio": is_audio,
                        "ext": ext,
                    })

                def make_hook(current_idx, track_title):
                    last_emit = [0.0]

                    def ytdl_hook(d):
                        if self.download_cancelled:
                            raise Exception("DOWNLOAD_CANCELLED")
                        status = d.get('status')
                        if status == 'downloading':
                            now = time.monotonic()
                            if now - last_emit[0] < 0.15:
                                return
                            last_emit[0] = now
                            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                            downloaded = d.get('downloaded_bytes', 0) or 0
                            track_pct = int(downloaded / total * 100) if total > 0 else 0
                            dl_mb = round(downloaded / (1024 * 1024), 1)
                            tot_mb = round(total / (1024 * 1024), 1)
                            speed = d.get('speed') or 0
                            spd_str = f"{speed / (1024 * 1024):.1f} MB/s" if speed else "0.0 MB/s"
                            overall_pct = int(
                                ((current_idx + (track_pct / 100.0)) / total_tracks) * 100
                            )
                            self._js(
                                "updatePlaylistDownloadProgress",
                                overall_pct, current_idx, total_tracks, track_title,
                                track_pct, dl_mb, tot_mb, spd_str,
                            )
                        elif status == 'finished':
                            overall_pct = int(((current_idx + 1) / total_tracks) * 100)
                            self._js(
                                "updatePlaylistDownloadProgress",
                                overall_pct, current_idx, total_tracks, track_title,
                                100, 0, 0, "",
                            )

                    return ytdl_hook

                for idx, track in enumerate(tracks):
                    if self.download_cancelled:
                        break
                    title = str(track.get("title") or f"Track {idx + 1}")
                    track_url = str(track.get("url") or "").strip()
                    client_key = str(track.get("client_key") or idx)
                    self._js("onPlaylistTrackStart", client_key, idx)

                    if not track_url:
                        failed_count += 1
                        self._js("onPlaylistTrackFinished", client_key, "error", title)
                        continue

                    # Spotify search results can contain open.spotify.com links.
                    # Resolve them to a YouTube search query before handing them
                    # to yt-dlp (which does not download Spotify streams).
                    if is_spotify_url(track_url) and "/track/" in track_url:
                        spotify_title = self.get_spotify_track_info_no_api(track_url) or title
                        track_url = f"ytsearch1:{spotify_title}"

                    base_name = self._unique_base_name(save_dir, title, ext)
                    target_filepath = os.path.join(save_dir, f"{base_name}.{str(ext).lower()}")
                    hook = make_hook(idx, title)

                    try:
                        opts = self._build_ydl_opts(
                            save_dir, base_name, quality, ext, is_audio, [hook]
                        )
                        with yt_dlp.YoutubeDL(opts) as ydl:
                            ydl.download([track_url])

                        if self.download_cancelled:
                            raise Exception("DOWNLOAD_CANCELLED")

                        actual_path = find_output_file(save_dir, base_name, ext)
                        if not actual_path:
                            raise Exception("Yükləmə tamamlandı, amma fayl tapılmadı.")
                        filename = os.path.basename(actual_path)
                        success_count += 1
                        self._js("onPlaylistTrackFinished", client_key, "success", title)
                        self._js("addHistoryItem", filename)

                    except Exception as e:
                        err = str(e)
                        if "DOWNLOAD_CANCELLED" in err:
                            cleanup_partial(save_dir, base_name, target_filepath)
                            self._js("onPlaylistTrackFinished", client_key, "cancelled", title)
                            break
                        logging.error("Error downloading track %s: %s", title, err)
                        if telemetry:
                            telemetry.capture_error(e, {
                                "step": "playlist_track",
                                "track_index": idx,
                                "is_audio": is_audio,
                                "ext": ext,
                            })
                        cleanup_partial(save_dir, base_name, target_filepath)
                        failed_count += 1
                        self._js("onPlaylistTrackFinished", client_key, "error", title)

                status = "cancelled" if self.download_cancelled else "completed"
                self._js(
                    "onPlaylistBatchDone", status, total_tracks,
                    success_count, failed_count,
                )

            except Exception as e:
                logging.error("Playlist batch failed: %s", e)
                if telemetry and "DOWNLOAD_CANCELLED" not in str(e):
                    telemetry.capture_error(e, {"step": "playlist_batch_overall"})
                self._js("onPlaylistBatchError", str(e))
            finally:
                self._js("resetPlaylistDownloadState")
                self._download_lock.release()

        threading.Thread(target=worker, daemon=True).start()
        return {"status": "started"}

    def search_tracks(self, query, source="spotify", limit=25):
        query = (query or "").strip()
        if not query:
            return []

        try:
            limit = max(1, min(50, int(limit)))
        except (TypeError, ValueError):
            limit = 25

        results = []
        source_lower = (source or "spotify").lower()

        if source_lower == "youtube":
            try:
                base_opts = self.get_base_ydl_opts()
                base_opts.update({
                    'quiet': True,
                    'extract_flat': True,
                    'skip_download': True
                })
                with yt_dlp.YoutubeDL(base_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
                    for entry in info.get("entries", []):
                        if not entry:
                            continue
                        dur = entry.get("duration", 0) or 0
                        dur_str = f"{int(dur)//60}:{int(dur)%60:02d}" if dur else ""
                        vid_id = entry.get("id")
                        title = entry.get("title", "")
                        channel = entry.get("uploader", "") or entry.get("channel", "")
                        thumb = entry.get("thumbnail") or (entry.get("thumbnails", [{}])[0].get("url") if entry.get("thumbnails") else "")
                        url = entry.get("url") or f"https://www.youtube.com/watch?v={vid_id}"
                        if vid_id and not url.startswith("http"):
                            url = f"https://www.youtube.com/watch?v={vid_id}"
                        results.append({
                            "id": vid_id,
                            "title": title,
                            "artist": channel,
                            "duration": dur,
                            "duration_str": dur_str,
                            "thumbnail": thumb,
                            "url": url,
                            "source": "youtube"
                        })
            except Exception as e:
                print(f"YouTube search error: {e}")
        else:
            # 1. If user configured Spotify credentials, try official Spotify API first
            config = self.get_spotify_config()
            client_id = config.get("client_id")
            client_secret = config.get("client_secret")
            api_key = config.get("api_key")
            auth_res = self.check_spotify_auth(client_id, client_secret, api_key)
            if auth_res.get("authenticated"):
                try:
                    token = auth_res.get("token")
                    headers = {"Authorization": f"Bearer {token}"}
                    r = requests.get(
                        f"https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=track&limit={limit}",
                        headers=headers,
                        timeout=6
                    )
                    if r.status_code == 200:
                        for it in r.json().get("tracks", {}).get("items", []):
                            name = it.get("name", "")
                            artists = ", ".join([a.get("name", "") for a in it.get("artists", []) if a.get("name")])
                            dur_ms = it.get("duration_ms", 0) or 0
                            dur_sec = dur_ms // 1000
                            dur_str = f"{dur_sec//60}:{dur_sec%60:02d}"
                            images = it.get("album", {}).get("images", [])
                            thumb = images[0].get("url", "") if images else ""
                            spotify_url = it.get("external_urls", {}).get("spotify", "")
                            results.append({
                                "id": it.get("id"),
                                "title": name,
                                "artist": artists,
                                "duration": dur_sec,
                                "duration_str": dur_str,
                                "thumbnail": thumb,
                                "url": spotify_url or f"https://open.spotify.com/track/{it.get('id')}",
                                "source": "spotify"
                            })
                        if results:
                            return results[:limit]
                except Exception as e:
                    logging.warning("Official Spotify search error: %s", e)

            # 2. Live global music catalog (always real-time, no quota blocks, smart artist catalogue matching)
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                seen_ids = set()

                # A. Check artist autocomplete or artist search for full artist track discovery
                try:
                    r_art = requests.get(
                        "https://api.deezer.com/search/artist",
                        params={"q": query, "limit": 1},
                        headers=headers,
                        timeout=4
                    )
                    if r_art.status_code == 200:
                        arts = r_art.json().get("data", [])
                        if arts:
                            art_id = arts[0].get("id")
                            r_top = requests.get(
                                f"https://api.deezer.com/artist/{art_id}/top",
                                params={"limit": 30},
                                headers=headers,
                                timeout=4
                            )
                            if r_top.status_code == 200:
                                for it in r_top.json().get("data", []):
                                    tid = str(it.get("id"))
                                    if tid not in seen_ids:
                                        seen_ids.add(tid)
                                        dur = it.get("duration", 0) or 0
                                        dur_str = f"{dur//60}:{dur%60:02d}"
                                        title = it.get("title", "")
                                        artist = it.get("artist", {}).get("name", "")
                                        album = it.get("album", {})
                                        cover = album.get("cover_medium") or album.get("cover") or it.get("artist", {}).get("picture_medium", "")
                                        results.append({
                                            "id": tid,
                                            "title": title,
                                            "artist": artist,
                                            "duration": dur,
                                            "duration_str": dur_str,
                                            "thumbnail": cover,
                                            "url": f"ytsearch1:{artist} - {title}",
                                            "display_name": f"{artist} - {title}",
                                            "source": "spotify"
                                        })
                except Exception as e_art:
                    logging.debug("Deezer artist search failed: %s", e_art)

                # B. General track search
                r = requests.get(
                    "https://api.deezer.com/search",
                    params={"q": query, "limit": limit},
                    headers=headers,
                    timeout=5
                )
                if r.status_code == 200:
                    for it in r.json().get("data", []):
                        tid = str(it.get("id"))
                        if tid not in seen_ids:
                            seen_ids.add(tid)
                            dur = it.get("duration", 0) or 0
                            dur_str = f"{dur//60}:{dur%60:02d}"
                            title = it.get("title", "")
                            artist = it.get("artist", {}).get("name", "")
                            album = it.get("album", {})
                            cover = album.get("cover_medium") or album.get("cover") or it.get("artist", {}).get("picture_medium", "")
                            results.append({
                                "id": tid,
                                "title": title,
                                "artist": artist,
                                "duration": dur,
                                "duration_str": dur_str,
                                "thumbnail": cover,
                                "url": f"ytsearch1:{artist} - {title}",
                                "display_name": f"{artist} - {title}",
                                "source": "spotify"
                            })
            except Exception as e:
                logging.warning("Music catalog search error: %s", e)

        return results[:limit]

    def get_clipboard_text(self):
        """Read Unicode text from the Windows clipboard without creating Tk in a worker thread."""
        if os.name == "nt":
            try:
                import ctypes
                from ctypes import wintypes

                user32 = ctypes.windll.user32
                kernel32 = ctypes.windll.kernel32
                CF_UNICODETEXT = 13

                user32.OpenClipboard.argtypes = [wintypes.HWND]
                user32.OpenClipboard.restype = wintypes.BOOL
                user32.GetClipboardData.argtypes = [wintypes.UINT]
                user32.GetClipboardData.restype = wintypes.HANDLE
                user32.CloseClipboard.restype = wintypes.BOOL
                kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
                kernel32.GlobalLock.restype = wintypes.LPVOID
                kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
                kernel32.GlobalUnlock.restype = wintypes.BOOL

                if not user32.OpenClipboard(None):
                    return ""
                try:
                    handle = user32.GetClipboardData(CF_UNICODETEXT)
                    if not handle:
                        return ""
                    pointer = kernel32.GlobalLock(handle)
                    if not pointer:
                        return ""
                    try:
                        return ctypes.wstring_at(pointer)
                    finally:
                        kernel32.GlobalUnlock(handle)
                finally:
                    user32.CloseClipboard()
            except Exception as exc:
                logging.debug("Windows clipboard read failed: %s", exc)

        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            try:
                return root.clipboard_get()
            finally:
                root.destroy()
        except Exception:
            return ""

    def eval_js(self, script):
        if self._window:
            try:
                self._window.evaluate_js(script)
            except Exception as exc:
                logging.debug("evaluate_js failed: %s", exc)

    def report_client_error(self, message, source="", lineno=0, colno=0):
        """Allows JavaScript UI to report unhandled exceptions to telemetry."""
        if telemetry:
            telemetry.record_breadcrumb("client_js", f"UI error: {message}", {
                "source": source,
                "lineno": lineno,
                "colno": colno
            }, level="error")
            telemetry.capture_error(Exception(f"UI Error: {message} ({source}:{lineno}:{colno})"))

    def get_telemetry_info(self):
        """Return non-sensitive diagnostic identifiers for the UI."""
        if telemetry:
            return {
                "device_id": telemetry.get_or_create_device_id(),
                "version": CURRENT_VERSION,
            }
        return {"device_id": "unknown", "version": CURRENT_VERSION}



