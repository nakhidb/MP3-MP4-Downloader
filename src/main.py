import os
import sys
import webview
def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Prepend local src directory so changes in bridge.py are live immediately without rebuild
_app_dir = get_app_dir()
_src_dir = os.path.join(_app_dir, "src")
_bridge_file = os.path.join(_src_dir, "bridge.py")

if os.path.exists(_src_dir) and _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

try:
    import telemetry
    telemetry.init_telemetry("v1.9")
except Exception as _te:
    print(f"Telemetry notice: {_te}")


Bridge = None
if os.path.exists(_bridge_file):
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("bridge", _bridge_file)
        if spec and spec.loader:
            bridge_mod = importlib.util.module_from_spec(spec)
            sys.modules["bridge"] = bridge_mod
            spec.loader.exec_module(bridge_mod)
            Bridge = getattr(bridge_mod, "Bridge", None)
    except Exception as _e:
        print(f"Failed to load external bridge: {_e}")

if Bridge is None:
    try:
        if os.path.exists(_src_dir) and _src_dir not in sys.path:
            sys.path.insert(0, _src_dir)
        from bridge import Bridge
    except ImportError:
        import bridge
        Bridge = bridge.Bridge


def get_html_path():
    # 1. First priority: live local web directory next to the exe or project root
    app_dir = get_app_dir()
    local_html = os.path.join(app_dir, 'web', 'index.html')
    if os.path.exists(local_html):
        return os.path.abspath(local_html)

    # 2. Fallback: bundled _MEIPASS if running standalone without local web folder
    if hasattr(sys, '_MEIPASS'):
        bundle_html = os.path.join(sys._MEIPASS, 'web', 'index.html')
        if os.path.exists(bundle_html):
            return bundle_html

    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(base_dir, '..', 'web', 'index.html'))


def main():
    bridge = Bridge()
    
    # We can center the window directly by setting hidden=True, calculating screen sizes on start, and then showing it exactly at the center in the start event callback without delay to avoid the double-jump flash.
    window = webview.create_window(
        title="TrackDrop",
        url=get_html_path(),
        js_api=bridge,
        width=1045,
        height=745,
        min_size=(880, 500),
        background_color='#121212',
        hidden=True  # Keep hidden until centered
    )
    
    bridge._window = window

    def initialize_app(w):
        # Center the window immediately on startup using native Windows API
        try:
            import ctypes
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
        except Exception:
            try:
                screen_width = w.screen.width
                screen_height = w.screen.height
            except Exception:
                screen_width, screen_height = 1920, 1080
        
        cx = (screen_width - 1045) // 2
        cy = (screen_height - 745) // 2
        
        # Ensure it doesn't render off-screen or too low
        if cx < 0: cx = 0
        if cy < 0: cy = 0
        
        try:
            w.move(cx, cy)
        except Exception:
            pass
        w.show()

    webview.start(initialize_app, window)

if __name__ == '__main__':
    main()
