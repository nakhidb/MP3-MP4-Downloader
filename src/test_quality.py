import yt_dlp

url = "https://youtu.be/fmNXLXofqm4"
quality = "1080"
fmt = f'bestvideo[height<={quality}]+bestaudio[ext=m4a]/bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'

tests = [
    ['tv_embedded'],
    ['tv_embedded', 'android_vr', 'web']
]

for clients in tests:
    print(f"\n--- Testing clients: {clients} ---")
    opts = {
        'quiet': True,
        'extractor_args': {
            'youtube': {
                'player_client': clients,
                'skip': ['webpage']
            }
        },
        'format': fmt,
        'simulate': True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            req = info.get('requested_formats') or [info]
            total = 0
            for f in req:
                sz = f.get('filesize_approx') or f.get('filesize') or 0
                total += sz
                print(f"  id={f.get('format_id')} h={f.get('height')} sz={sz//1024//1024}MB vcodec={str(f.get('vcodec','?'))[:15]}")
            print(f"  TOTAL: {total//1024//1024} MB")
    except Exception as e:
        print(f"  ERROR: {e}")
