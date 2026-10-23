# TrackDrop 🎵

> A sleek, high-speed, and modern desktop audio & video downloader for Windows.

TrackDrop makes it effortless to download single tracks, albums, and playlists from YouTube and Spotify in ultra-high quality.

---

## ✨ Features

- ⚡ **High-Speed Downloads:** Ultra-fast audio & video extraction.
- 🎧 **Studio Quality Audio:** Crystal-clear MP3 conversion up to 320 kbps.
- 🎬 **Crisp Video Formats:** Full HD, 2K, and 4K MP4 video downloads.
- 🟢 **Spotify Integration:** Download single tracks or full playlists automatically.
- 📦 **Batch Downloader:** Queue multiple tracks with live per-track progress bars.
- 🎨 **Modern Minimalist UI:** Native desktop experience with dark mode and smooth animations.
- 🛠️ **Built-in FFmpeg Manager:** Automatically detects or installs required conversion tools with one click.

---

## 🚀 How to Run

### Option 1: Direct Download (Easiest)
1. Go to the **[Releases](../../releases)** tab on GitHub.
2. Download the latest **`TrackDrop.exe`**.
3. Double-click to run!

> **Security Note:** If Windows SmartScreen shows a warning on first launch, click **"More info"** and then **"Run anyway"**. TrackDrop is fully open-source and safe.

---

### Option 2: Run from Source

#### Prerequisites
- Windows 10/11
- Python 3.10+

```bash
# Clone the repository
git clone https://github.com/nakhidb/MP3-MP4-Downloader.git
cd MP3-MP4-Downloader

# Set up virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python src/main.py
```

### Build Single-File Executable
To package the app into a standalone `TrackDrop.exe`:
```bash
python src/build_exe.py
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
