import os
import sys
import json
import re
import base64
import shutil
import threading
import requests
import yt_dlp
# pyrefly: ignore [missing-import]
import webview

CURRENT_VERSION = "v1.0.4"
GITHUB_REPO = "nakhidb/MP3-MP4-Downloader"

# Get config directory and config file path
def get_config_dir():
    config_dir = os.path.join(os.path.expanduser("~"), ".trackdrop")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

def get_config_path():
    return os.path.join(get_config_dir(), "spotify_config.json")

class Bridge:
    def __init__(self):
        self._window = None
        self.download_cancelled = False
        self.active_downloads = {} # to track active download threads
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
            self.eval_js(f"window.showFfmpegModal({json.dumps(self.ffmpeg_progress)})")
            return

        self.ffmpeg_downloading = True
        self.eval_js("window.showFfmpegModal()")

        def worker():
            import time
            import zipfile
            import io

            try:
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
                            self.eval_js(f"window.updateFfmpegModalProgress({json.dumps(self.ffmpeg_progress)})")
                
                self.ffmpeg_progress["status"] = "installing"
                self.ffmpeg_progress["pct"] = 100
                self.eval_js(f"window.updateFfmpegModalProgress({json.dumps(self.ffmpeg_progress)})")
                
                with zipfile.ZipFile(zip_data) as z:
                    z.extractall(ffmpeg_dir)
                
                self.ffmpeg_progress["status"] = "success"
                self.ffmpeg_downloading = False
                self.eval_js(f"window.onFfmpegSuccess()")
            except Exception as e:
                self.ffmpeg_downloading = False
                self.ffmpeg_progress["status"] = "error"
                self.ffmpeg_progress["message"] = str(e)
                self.eval_js(f"window.onFfmpegError({json.dumps(str(e))})")
        
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
                        def parse_version(v_str):
                            nums = re.findall(r'\d+', v_str)
                            return [int(n) for n in nums]
                        
                        current_parsed = parse_version(CURRENT_VERSION)
                        latest_parsed = parse_version(latest_tag)
                        if latest_parsed > current_parsed:
                            html_url = data.get("html_url", f"https://github.com/{GITHUB_REPO}/releases")
                            self.eval_js(f"window.showUpdateNotification('{latest_tag}', '{html_url}')")
            except Exception as e:
                print(f"Error checking updates: {e}")
                
        threading.Thread(target=worker, daemon=True).start()

    def open_external_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def get_spotify_config(self):
        path = get_config_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"client_id": "", "client_secret": ""}

    def save_spotify_config(self, client_id, client_secret):
        path = get_config_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"client_id": client_id, "client_secret": client_secret}, f, indent=2)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_spotify_auth(self, client_id, client_secret):
        try:
            auth_url = "https://accounts.spotify.com/api/token"
            auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {"grant_type": "client_credentials"}
            r = requests.post(auth_url, headers=headers, data=data, timeout=10)
            if r.status_code == 200 and "access_token" in r.json():
                return {"authenticated": True}
        except:
            pass
        return {"authenticated": False}

    def get_spotify_playlist_no_api(self, playlist_id):
        """Fetch Spotify playlist tracks via embed page without API keys."""
        try:
            import html as html_mod
            embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            r = requests.get(embed_url, headers=headers, timeout=15)
            if r.status_code != 200:
                return None
            pattern = r'<script\s+id="__NEXT_DATA__"\s+type="application/json">([^<]+)</script>'
            m = re.search(pattern, r.text)
            if not m:
                return None
            js_data = json.loads(html_mod.unescape(m.group(1)))
            entity = js_data.get("props", {}).get("pageProps", {}).get("state", {}).get("data", {}).get("entity", {})
            playlist_name = entity.get("title") or entity.get("name") or "Spotify Playlist"
            track_list = entity.get("trackList", [])
            tracks = []
            for item in track_list:
                title = item.get("title", "")
                artist = item.get("subtitle", "")
                duration_ms = item.get("duration", 0)
                duration_sec = duration_ms // 1000
                tracks.append({
                    "title": title,
                    "artist": artist,
                    "duration": duration_sec,
                    "thumbnail": "",
                    "url": f"ytsearch1:{artist} - {title}"
                })
            return {"playlist_name": playlist_name, "tracks": tracks}
        except Exception as e:
            print(f"Error scraping Spotify playlist: {e}")
            return None

    def fetch_playlist(self, url):
        # 1. Spotify playlist
        if "spotify.com" in url and "playlist/" in url:
            playlist_id = url.split("playlist/")[1].split("?")[0].split("/")[0]

            # Try no-API embed scraping first
            result = self.get_spotify_playlist_no_api(playlist_id)
            if result:
                return result

            # Fallback: require API credentials
            config = self.get_spotify_config()
            client_id = config.get("client_id")
            client_secret = config.get("client_secret")
            
            auth_res = self.check_spotify_auth(client_id, client_secret)
            if not auth_res.get("authenticated"):
                return {"error": "spotify_auth_required"}
                
            auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
            r_token = requests.post("https://accounts.spotify.com/api/token", 
                                    headers={"Authorization": f"Basic {auth_header}", "Content-Type": "application/x-www-form-urlencoded"},
                                    data={"grant_type": "client_credentials"}, timeout=10)
            token = r_token.json().get("access_token")
            
            tracks = []
            next_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100"
            headers = {"Authorization": f"Bearer {token}"}
            
            try:
                r_playlist = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers, timeout=10)
                playlist_name = "Spotify Playlist"
                if r_playlist.status_code == 200:
                    playlist_name = r_playlist.json().get("name", "Spotify Playlist")
                
                while next_url:
                    r_tracks = requests.get(next_url, headers=headers, timeout=10)
                    if r_tracks.status_code == 200:
                        data = r_tracks.json()
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
                            thumb = images[-1].get("url", "") if images else ""
                            tracks.append({
                                "title": name,
                                "artist": artist_str,
                                "duration": duration_sec,
                                "thumbnail": thumb,
                                "url": f"ytsearch1:{artist_str} - {name}"
                            })
                        next_url = data.get("next")
                    else:
                        break
                        
                return {"playlist_name": playlist_name, "tracks": tracks}
            except Exception as e:
                return {"error": str(e)}

        # 2. YouTube playlist / extract_flat
        else:
            try:
                ydl_opts = {
                    'extract_flat': True,
                    'quiet': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    playlist_name = info.get('title', 'YouTube Playlist')
                    tracks = []
                    if 'entries' in info:
                        for entry in info['entries']:
                            if not entry:
                                continue
                            tracks.append({
                                "title": entry.get('title', 'YouTube Video'),
                                "artist": entry.get('uploader', 'Unknown Artist'),
                                "duration": entry.get('duration', 0),
                                "thumbnail": entry.get('thumbnails', [{}])[0].get('url', '') if entry.get('thumbnails') else '',
                                "url": f"https://www.youtube.com/watch?v={entry.get('id')}"
                            })
                    return {"playlist_name": playlist_name, "tracks": tracks}
            except Exception as e:
                return {"error": str(e)}

    def cancel_download(self):
        self.download_cancelled = True

    def get_spotify_track_info_no_api(self, url):
        try:
            import html
            track_id = url.split("track/")[1].split("?")[0].split("/")[0]
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
                        artists = [a.get("name") for a in entity.get("artists", [])]
                        artist_str = ", ".join(artists)
                        return f"{artist_str} - {title}"
        except Exception as e:
            print(f"Error scraping Spotify track: {e}")
        return None

    def get_base_ydl_opts(self):
        opts = {
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web', 'mweb'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            'nocheckcertificate': True,
            'geo_bypass': True,
            'concurrent_fragment_downloads': 16,
            'buffersize': 2097152,
            'http_chunk_size': 10485760,
            'retries': 15,
            'fragment_retries': 15,
            'file_access_retries': 5,
        }
        if shutil.which("node"):
            opts['js_runtimes'] = {'node': {}}
        return opts

    def download_single(self, url, media_type, quality, ext):
        self.download_cancelled = False
        
        def worker():
            try:
                # Check if it is a playlist link
                is_spotify_playlist = "spotify.com" in url and "playlist/" in url
                is_youtube_playlist = "youtube.com" in url and ("playlist" in url or "list=" in url)
                if is_spotify_playlist or is_youtube_playlist:
                    raise Exception("ERROR_PLAYLIST_IN_SINGLE")

                # 1. Fetch info to get default title
                self.eval_js("window.updateDownloadProgress(0, 'extracting', 'Video məlumatları alınır...')")
                
                # Check and resolve Spotify single track URLs
                original_url = url
                spotify_title = None
                
                if "spotify.com" in url and "track/" in url:
                    # Try to scrape the track info without API key first
                    spotify_title = self.get_spotify_track_info_no_api(url)
                    
                    if spotify_title:
                        resolved_url = f"ytsearch1:{spotify_title}"
                    else:
                        # Fallback to Spotify API credentials
                        config = self.get_spotify_config()
                        client_id = config.get("client_id")
                        client_secret = config.get("client_secret")
                        auth_res = self.check_spotify_auth(client_id, client_secret)
                        if not auth_res.get("authenticated"):
                            self.eval_js("window.showSpotifyAuthModal()")
                            return
                        
                        track_id = url.split("track/")[1].split("?")[0].split("/")[0]
                        # Get Token
                        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
                        r_token = requests.post("https://accounts.spotify.com/api/token", 
                                                headers={"Authorization": f"Basic {auth_header}", "Content-Type": "application/x-www-form-urlencoded"},
                                                data={"grant_type": "client_credentials"}, timeout=10)
                        token = r_token.json().get("access_token")
                        
                        # Fetch Track info
                        r_track = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers={"Authorization": f"Bearer {token}"}, timeout=10)
                        if r_track.status_code == 200:
                            track_info = r_track.json()
                            name = track_info.get("name")
                            artists = [a.get("name") for a in track_info.get("artists", [])]
                            artist_str = ", ".join(artists)
                            spotify_title = f"{artist_str} - {name}"
                            resolved_url = f"ytsearch1:{spotify_title}"
                        else:
                            raise Exception("Failed to fetch Spotify track metadata.")
                else:
                    resolved_url = url

                base_opts = self.get_base_ydl_opts()
                base_opts.update({'quiet': True, 'extract_flat': True, 'skip_download': True})
                with yt_dlp.YoutubeDL(base_opts) as ydl:
                    info = ydl.extract_info(resolved_url, download=False)
                    if 'entries' in info and len(info['entries']) > 0:
                        video_title = info['entries'][0].get('title', 'video')
                    else:
                        video_title = info.get('title', 'video')
                        
                if spotify_title:
                    video_title = spotify_title
                    
                clean_title = re.sub(r'[\\/*?:"<>|]', "", video_title)
                
                # 2. Open Save File Dialog
                dialog_res = self._window.create_file_dialog(
                    dialog_type=webview.SAVE_DIALOG,
                    save_filename=f"{clean_title}.{ext.lower()}"
                )
                if not dialog_res:
                    self.eval_js("window.resetDownloadButton()")
                    return
                target_filepath = dialog_res[0]
                
                # Strip the extension suffix if it matches ext.lower() to prevent duplicate extension (.mp3.mp3)
                base_path = target_filepath
                ext_suffix = f".{ext.lower()}"
                if base_path.lower().endswith(ext_suffix):
                    base_path = base_path[:-len(ext_suffix)]
                outtmpl_path = base_path + '.%(ext)s'
                
                # 3. Perform download
                self.eval_js("window.updateDownloadProgress(0, 'downloading', 'Yüklənir...')")
                ffmpeg_location = self.get_ffmpeg_path()
                
                def ytdl_hook(d):
                    if self.download_cancelled:
                        raise Exception("DOWNLOAD_CANCELLED")
                    if d['status'] == 'downloading':
                        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                        downloaded = d.get('downloaded_bytes', 0)
                        if total > 0:
                            pct = int(downloaded / total * 100)
                            dl_mb = downloaded / (1024 * 1024)
                            tot_mb = total / (1024 * 1024)
                            speed = d.get('speed', 0)
                            spd_str = f"{speed / (1024*1024):.1f} MB/s" if speed else "0.0 MB/s"
                            detail = f"{dl_mb:.1f} MB / {tot_mb:.1f} MB  |  Sürət: {spd_str}"
                            self.eval_js(f"window.updateDownloadProgress({pct}, 'downloading', '{detail}')")
                    elif d['status'] == 'finished':
                        self.eval_js("window.updateDownloadProgress(100, 'converting', 'Konvertasiya olunur...')")

                ydl_opts_dl = self.get_base_ydl_opts()
                ydl_opts_dl.update({
                    'outtmpl': outtmpl_path,
                    'progress_hooks': [ytdl_hook],
                    'quiet': True,
                })

                is_audio = media_type.lower() in ["audio", "audio_lbl", "səs", "səsləndi"]
                if is_audio:
                    bitrate = quality.split()[0]
                    ydl_opts_dl.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': ext.lower(),
                            'preferredquality': bitrate,
                        }],
                    })
                else:
                    if "4K" in quality:
                        p_quality = "2160"
                    elif "2K" in quality:
                        p_quality = "1440"
                    else:
                        p_quality = quality.split('p')[0]
                    ydl_opts_dl.update({
                        'format': f'bestvideo[height<={p_quality}]+bestaudio/best/[height<={p_quality}]/best',
                        'merge_output_format': ext.lower(),
                        'postprocessor_args': {
                            'merger': ['-c:v', 'copy', '-c:a', 'aac'],
                        },
                    })
                    
                if ffmpeg_location:
                    ydl_opts_dl['ffmpeg_location'] = ffmpeg_location
                    
                with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
                    ydl.download([resolved_url])
                    
                if self.download_cancelled:
                    raise Exception("DOWNLOAD_CANCELLED")
                    
                filename = os.path.basename(target_filepath)
                self.eval_js(f"window.updateDownloadProgress(100, 'success', '{filename}')")
                # Append to history
                self.eval_js(f"window.addHistoryItem('{filename}')")
                
            except Exception as e:
                if "DOWNLOAD_CANCELLED" in str(e):
                    # Clean partial file if exists
                    try:
                        if os.path.exists(target_filepath):
                            os.remove(target_filepath)
                    except:
                        pass
                    self.eval_js("window.updateDownloadProgress(0, 'cancelled', 'Yükləmə ləğv edildi.')")
                elif "ERROR_PLAYLIST_IN_SINGLE" in str(e):
                    self.eval_js("window.updateDownloadProgress(0, 'error', 'ERROR_PLAYLIST_IN_SINGLE')")
                else:
                    err_msg = json.dumps(f"Xəta: {str(e)}")
                    self.eval_js(f"window.updateDownloadProgress(0, 'error', {err_msg})")
            finally:
                self.eval_js("window.resetDownloadButton()")
                
        threading.Thread(target=worker, daemon=True).start()

    def download_selected_tracks(self, tracks, is_audio, media_type, quality, ext):
        self.download_cancelled = False
        
        def worker():
            try:
                # 1. Ask save folder
                dialog_res = self._window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG)
                if not dialog_res:
                    self.eval_js("window.resetPlaylistDownloadState()")
                    return
                save_dir = dialog_res[0]
                
                ffmpeg_location = self.get_ffmpeg_path()
                total_tracks = len(tracks)
                
                # Define hook factory with detailed real-time track and playlist progress
                def make_hook(bridge_ref, current_idx, track_title):
                    def ytdl_hook(d):
                        if bridge_ref.download_cancelled:
                            raise Exception("DOWNLOAD_CANCELLED")
                        if d['status'] == 'downloading':
                            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                            downloaded = d.get('downloaded_bytes', 0)
                            track_pct = int(downloaded / total * 100) if total > 0 else 0
                            dl_mb = round(downloaded / (1024 * 1024), 1)
                            tot_mb = round(total / (1024 * 1024), 1)
                            speed = d.get('speed', 0)
                            spd_str = f"{speed / (1024*1024):.1f} MB/s" if speed else "0.0 MB/s"
                            
                            overall_pct = int(((current_idx + (track_pct / 100.0)) / total_tracks) * 100)
                            safe_title = json.dumps(track_title)
                            bridge_ref.eval_js(
                                f"window.updatePlaylistDownloadProgress({overall_pct}, {current_idx}, {total_tracks}, {safe_title}, {track_pct}, {dl_mb}, {tot_mb}, '{spd_str}')"
                            )
                        elif d['status'] == 'finished':
                            overall_pct = int(((current_idx + 1) / total_tracks) * 100)
                            safe_title = json.dumps(track_title)
                            bridge_ref.eval_js(
                                f"window.updatePlaylistDownloadProgress({overall_pct}, {current_idx}, {total_tracks}, {safe_title}, 100, 0, 0, 'Konvertasiya...')"
                            )
                    return ytdl_hook
                
                for idx, track in enumerate(tracks):
                    if self.download_cancelled:
                        break
                        
                    title = track.get("title", f"Track {idx+1}")
                    url = track.get("url")
                    
                    self.eval_js(f"window.onPlaylistTrackStart({idx})")
                    
                    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
                    base_filepath = os.path.join(save_dir, clean_title)
                    outtmpl_path = base_filepath + '.%(ext)s'
                    
                    hook = make_hook(self, idx, title)
                    
                    try:
                        ydl_opts = self.get_base_ydl_opts()
                        ydl_opts.update({
                            'outtmpl': outtmpl_path,
                            'progress_hooks': [hook],
                            'quiet': True,
                        })

                        if is_audio:
                            bitrate = quality.split()[0]
                            ydl_opts.update({
                                'format': 'bestaudio/best',
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': ext.lower(),
                                    'preferredquality': bitrate,
                                }],
                            })
                        else:
                            if "4K" in quality:
                                p_quality = "2160"
                            elif "2K" in quality:
                                p_quality = "1440"
                            else:
                                p_quality = quality.split('p')[0]
                            ydl_opts.update({
                                'format': f'bestvideo[height<={p_quality}]+bestaudio/best/[height<={p_quality}]/best',
                                'merge_output_format': ext.lower(),
                                'postprocessor_args': {
                                    'merger': ['-c:v', 'copy', '-c:a', 'aac'],
                                },
                            })
                            
                        if ffmpeg_location:
                            ydl_opts['ffmpeg_location'] = ffmpeg_location
                            
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])
                        
                        self.eval_js(f"window.onPlaylistTrackFinished({idx}, 'success', {json.dumps(title)})")
                        self.eval_js(f"window.addHistoryItem({json.dumps(clean_title + '.' + ext.lower())})")
                            
                    except Exception as e:
                        err = str(e)
                        if "DOWNLOAD_CANCELLED" in err:
                            self.download_cancelled = True
                            self.eval_js(f"window.onPlaylistTrackFinished({idx}, 'cancelled', {json.dumps(title)})")
                            break
                        print(f"Error downloading track {title}: {err}")
                        self.eval_js(f"window.onPlaylistTrackFinished({idx}, 'error', {json.dumps(title)})")
                        # Keep going for other tracks
                        
                if self.download_cancelled:
                    self.eval_js("window.updatePlaylistStatus('Yükləmə ləğv edildi.')")
                else:
                    self.eval_js(f"window.updatePlaylistStatus('Hamısı tamamlandı! ({total_tracks}/{total_tracks})')")
                    
            except Exception as e:
                self.eval_js(f"window.updatePlaylistStatus('Xəta baş verdi: {str(e)}')")
            finally:
                self.eval_js("window.resetPlaylistDownloadState()")
                
        threading.Thread(target=worker, daemon=True).start()


    def get_clipboard_text(self):
        # We can implement a clean clipboard getter using pywebview window or tkinter fallback
        try:
            import tkinter as tk
            r = tk.Tk()
            r.withdraw()
            text = r.clipboard_get()
            r.destroy()
            return text
        except:
            return ""

    def eval_js(self, script):
        if self._window:
            try:
                self._window.evaluate_js(script)
            except:
                pass

