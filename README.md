# TrackDrop 🎵

Müasir, sürətli və minimalist masaüstü audio/video yükləyici (YouTube & Spotify dəstəyi ilə).

## 🚀 Xüsusiyyətlər
- **Audio & Video Yükləmə:** YouTube linklərindən yüksək keyfiyyətli MP3 (320kbps) və MP4 (1080p, 2K, 4K).
- **Spotify Dəstəyi:** Tək mahnı və ya pleylist linkləri ilə avtomatik sinxronizasiya.
- **Toplu Yükləmə (Batch Download):** Bütün pleylisti bir kliklə yükləmə imkanı.
- **Daxili Telemetriya:** Sentry dəstəyi ilə səhvlərin və cihazların anonim izlənməsi.

---

## 💻 Quraşdırma və İşə Salma

### 1. Tələblər
- Python 3.10 və ya daha yuxarı versiya
- Windows 10/11

### 2. Kitabxanaların yüklənməsi
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Tətbiqi işə salmaq
```bash
python src/main.py
```

### 4. Yeni EXE faylı yığmaq (Build)
```bash
python src/build_exe.py
```
Yığılmış `TrackDrop.exe` faylı avtomatik layihənin əsas qovluğuna yerləşdiriləcək.

---

## 📊 Telemetriya və Xəta İzləmə (Sentry)
Tətbiqdə yaranan xətaları, hansı sətirdə baş verdiyini və hansı cihazda yarandığını görmək üçün:
1. [sentry.io](https://sentry.io) saytında pulsuz hesab açın.
2. Yeni **Python** layihəsi yaradıb `DSN` linkini kopyalayın.
3. `src/telemetry.py` faylında `DEFAULT_SENTRY_DSN` dəyişəninə öz DSN açarınızı yapışdırın (və ya `SENTRY_DSN` sistem dəyişəni təyin edin).
