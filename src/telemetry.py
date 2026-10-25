import os
import sys
import uuid
import platform
import logging
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Dict, Any

# ==============================================================================
# Sentry DSN Configuration
# ==============================================================================
# Sentry.io DSN-inizi bura yerləşdirə və ya 'SENTRY_DSN' mühit dəyişəni ilə
# təyin edə bilərsiniz. DSN açıq mənbədə gizli açar sayılmır.
DEFAULT_SENTRY_DSN = "https://57392982513484cd21e7f0badfd55acb@o4512307230474240.ingest.us.sentry.io/4512307274317824"
SENTRY_DSN = os.environ.get("SENTRY_DSN", DEFAULT_SENTRY_DSN)

# Telemetry is opt-out. Set TRACKDROP_TELEMETRY=0 (or create the file
# <config_dir>/telemetry_opt_out) to disable remote error reporting completely.
_TELEMETRY_DISABLED_VALUES = {"0", "false", "off", "no", "disabled"}

_telemetry_initialized = False
_telemetry_enabled = True
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


def is_telemetry_enabled() -> bool:
    """Remote telemetry can be disabled by env var or a local opt-out file."""
    global _telemetry_enabled
    if os.environ.get("TRACKDROP_TELEMETRY", "").strip().lower() in _TELEMETRY_DISABLED_VALUES:
        _telemetry_enabled = False
        return False
    if os.environ.get("TRACKDROP_TELEMETRY_OPT_OUT", "").strip().lower() in _TELEMETRY_DISABLED_VALUES:
        _telemetry_enabled = False
        return False
    try:
        if (get_config_dir() / "telemetry_opt_out").exists():
            _telemetry_enabled = False
            return False
    except Exception:
        pass
    _telemetry_enabled = True
    return True


def get_or_create_device_id() -> str:
    """Return an anonymous, locally generated persistent UUID."""
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

    _device_info = {
        "device_id": device_uuid,
        "device_uuid": device_uuid,
        "os": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine(),
    }
    return device_uuid


def _configure_local_logging() -> None:
    """Attach a bounded, rotating log handler once."""
    try:
        log_file = get_config_dir() / "trackdrop.log"
        root = logging.getLogger()
        already_configured = any(
            isinstance(handler, RotatingFileHandler)
            and getattr(handler, "baseFilename", "") == str(log_file)
            for handler in root.handlers
        )
        if already_configured:
            return
        handler = RotatingFileHandler(
            str(log_file),
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        root.addHandler(handler)
        if root.level == logging.NOTSET:
            root.setLevel(logging.INFO)
    except Exception:
        # A broken log file must never prevent the application from starting.
        pass


def init_telemetry(app_version: str = "v1.8") -> bool:
    """
    Initializes Sentry telemetry and error tracking.
    Returns False when the DSN is missing or the user opted out.
    """
    global _telemetry_initialized, _telemetry_enabled
    if _telemetry_initialized:
        return _telemetry_enabled

    _telemetry_initialized = True
    _configure_local_logging()
    device_id = get_or_create_device_id()

    logging.info("App started: Version=%s, DeviceID=%s", app_version, device_id)

    if not is_telemetry_enabled():
        logging.info("Telemetry disabled by user preference. Running in local-only mode.")
        return False

    dsn = (SENTRY_DSN or "").strip()
    if not dsn or "examplePublicKey" in dsn:
        logging.info("Sentry DSN is not configured. Running in offline telemetry mode.")
        _telemetry_enabled = False
        return False

    try:
        import sentry_sdk
        from sentry_sdk.integrations.logging import LoggingIntegration

        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR,
        )

        sentry_sdk.init(
            dsn=dsn,
            release=f"trackdrop@{app_version}",
            environment="production",
            traces_sample_rate=0.05,
            send_default_pii=False,
            integrations=[sentry_logging],
        )

        # Only a random local UUID is sent. No MAC address, hostname, username,
        # IP-derived identity or file paths are attached intentionally.
        sentry_sdk.set_user({"id": device_id})
        sentry_sdk.set_tag("app_version", app_version)
        sentry_sdk.set_tag("os_platform", platform.system())
        sentry_sdk.set_tag("os_release", platform.release())

        default_excepthook = sys.excepthook
        default_thread_excepthook = threading.excepthook

        def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                default_excepthook(exc_type, exc_value, exc_traceback)
                return
            logging.critical(
                "Unhandled exception:",
                exc_info=(exc_type, exc_value, exc_traceback),
            )
            try:
                sentry_sdk.capture_exception(exc_value)
            except Exception:
                pass
            default_excepthook(exc_type, exc_value, exc_traceback)

        def handle_thread_exception(args):
            if issubclass(args.exc_type, KeyboardInterrupt):
                default_thread_excepthook(args)
                return
            logging.critical(
                "Unhandled exception in thread %s:",
                getattr(args.thread, "name", "unknown"),
                exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
            )
            try:
                sentry_sdk.capture_exception(args.exc_value)
            except Exception:
                pass
            default_thread_excepthook(args)

        sys.excepthook = handle_unhandled_exception
        threading.excepthook = handle_thread_exception
        _telemetry_enabled = True
        logging.info("Sentry telemetry initialized successfully.")
        return True
    except Exception as exc:
        logging.warning("Failed to initialize Sentry: %s", exc)
        _telemetry_enabled = False
        return False


def record_breadcrumb(category: str, message: str, data: Optional[Dict[str, Any]] = None, level: str = "info") -> None:
    """Record an operational step without personal data."""
    if not _telemetry_enabled:
        return
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
    logging.info("[%s] %s", category, message)


def capture_error(error: BaseException, context: Optional[Dict[str, Any]] = None) -> None:
    """Send a caught error and non-sensitive context to Sentry and the local log."""
    if _telemetry_enabled:
        try:
            import sentry_sdk
            with sentry_sdk.push_scope() as scope:
                scope.set_tag("handled", "true")
                if context:
                    for key, value in context.items():
                        scope.set_extra(key, value)
                sentry_sdk.capture_exception(error)
        except Exception:
            pass

    if error.__traceback__ is not None:
        logging.error(
            "Error captured: %s",
            error,
            exc_info=(type(error), error, error.__traceback__),
        )
    else:
        logging.error("Error captured: %s", error)
