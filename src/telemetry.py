import os
import sys
import uuid
import platform
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# ==============================================================================
# Sentry DSN Configuration
# ==============================================================================
# Sentry.io DSN açarınızı bura yapışdıra bilərsiniz və ya Windows Environment
# dəyişəni kimi 'SENTRY_DSN' təyin edə bilərsiniz.
# DSN açıq mənbədə (open-source) gizli açar deyil, client-side qorunmalıdır.
DEFAULT_SENTRY_DSN = "https://57392982513484cd21e7f0badfd55acb@o4512307230474240.ingest.us.sentry.io/4512307274317824"
SENTRY_DSN = os.environ.get("SENTRY_DSN", DEFAULT_SENTRY_DSN)


_telemetry_initialized = False
_device_info: Dict[str, str] = {}


def get_config_dir() -> Path:
    """Returns local app configuration directory."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data and os.path.exists(local_app_data):
        config_dir = Path(local_app_data) / "TrackDrop"
    else:
        config_dir = Path.home() / ".trackdrop"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_mac_address() -> str:
    """Returns the primary network interface MAC address."""
    try:
        mac_num = uuid.getnode()
        mac_hex = f"{mac_num:012x}"
        mac_str = ":".join(mac_hex[i : i + 2] for i in range(0, 12, 2)).upper()
        return mac_str
    except Exception:
        return "UNKNOWN_MAC"


def get_or_create_device_id() -> str:
    """
    Returns a persistent anonymous device identifier.
    Combines MAC address with a locally generated persistent UUID.
    """
    global _device_info
    if _device_info.get("device_id"):
        return _device_info["device_id"]

    config_dir = get_config_dir()
    id_file = config_dir / "device_id.txt"

    device_uuid = ""
    if id_file.exists():
        try:
            device_uuid = id_file.read_text(encoding="utf-8").strip()
        except Exception:
            device_uuid = ""

    if not device_uuid:
        device_uuid = str(uuid.uuid4())
        try:
            id_file.write_text(device_uuid, encoding="utf-8")
        except Exception:
            pass

    mac = get_mac_address()
    device_id = f"MAC_{mac.replace(':', '')}_{device_uuid[:8]}"

    _device_info = {
        "device_id": device_id,
        "mac_address": mac,
        "device_uuid": device_uuid,
        "os": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine(),
    }
    return device_id


def init_telemetry(app_version: str = "v1.8") -> bool:
    """
    Initializes Sentry telemetry and error tracking.
    If DSN is not set or placeholder, runs safely in local mode.
    """
    global _telemetry_initialized
    if _telemetry_initialized:
        return True

    device_id = get_or_create_device_id()
    mac = _device_info.get("mac_address", "UNKNOWN")

    # Local logger setup
    log_file = get_config_dir() / "trackdrop.log"
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8",
    )
    logging.info(f"App started: Version={app_version}, DeviceID={device_id}, MAC={mac}")

    # Check if Sentry DSN is configured
    is_placeholder = "examplePublicKey" in SENTRY_DSN or not SENTRY_DSN.strip()
    if is_placeholder:
        logging.info("Sentry DSN is not configured yet. Running in offline telemetry mode.")
        _telemetry_initialized = True
        return False

    try:
        import sentry_sdk
        from sentry_sdk.integrations.logging import LoggingIntegration

        sentry_logging = LoggingIntegration(
            level=logging.INFO,        # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        )

        mac_short = mac.replace(":", "")[-6:]
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            release=f"trackdrop@{app_version}",
            environment="production",
            traces_sample_rate=0.05,
            send_default_pii=False,
            integrations=[sentry_logging],
        )

        sentry_sdk.set_user({
            "id": device_id,
            "mac_address": mac,
            "username": f"Device-{mac_short}",
        })

        sentry_sdk.set_tag("mac_address", mac)
        sentry_sdk.set_tag("app_version", app_version)
        sentry_sdk.set_tag("os_platform", platform.platform())

        # Unhandled exception hook
        def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logging.critical("Unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback))
            sentry_sdk.capture_exception((exc_type, exc_value, exc_traceback))
            sys.__excepthook__(exc_type, exc_value, exc_traceback)

        sys.excepthook = handle_unhandled_exception
        _telemetry_initialized = True
        logging.info("Sentry telemetry initialized successfully.")
        return True
    except Exception as e:
        logging.warning(f"Failed to initialize Sentry: {e}")
        _telemetry_initialized = True
        return False


def record_breadcrumb(category: str, message: str, data: Optional[Dict[str, Any]] = None, level: str = "info") -> None:
    """
    Records an operational step (breadcrumb) without personal data.
    E.g.: category='download', message='yt-dlp extract started', data={'format': 'mp3'}
    """
    try:
        import sentry_sdk
        sentry_sdk.add_breadcrumb(
            category=category,
            message=message,
            data=data or {},
            level=level,
        )
    except Exception:
        pass
    logging.info(f"[{category}] {message}")


def capture_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """
    Sends caught error and context to Sentry and writes to local log.
    """
    try:
        import sentry_sdk
        with sentry_sdk.push_scope() as scope:
            if context:
                for k, v in context.items():
                    scope.set_extra(k, v)
            sentry_sdk.capture_exception(error)
    except Exception:
        pass
    logging.error(f"Error captured: {error}", exc_info=True)
