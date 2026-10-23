## Release Notes & Improvements (v1.0.7)

### 🇬🇧 English
- **Large Playlist Performance & RAM/CPU Optimization:** Introduced chunked memory management and caching in `%LOCALAPPDATA%/TrackDrop/cache` to prevent system freezing and 100% CPU spikes when loading huge playlists (e.g. 2,600+ tracks / 27+ parts).
- **Concurrency & Part Locking:** Added state protection (`isPlaylistLoading`) preventing overlapping part selections; clicking multiple parts now queues gracefully and alerts the user without crashing the interface.
- **Direct In-App Auto-Update:** Upgraded the updater flow to download latest releases directly within the app and auto-replace the executable smoothly without throwing the user out to a browser.
- **UI & Layout Refinements:** Redesigned playlist part navigation tags with generous spacing, better typography, and polished border states.
- **Multilingual UI Support:** Completed full English, Azerbaijani, and Russian translations for all batch actions, download filters, status toasts, and playlist part indicators. Smooth animated transitions between selected languages in the header.

---

### 🇦🇿 Azərbaycan dili
- **Böyük Pleylistlər üçün Performans və Yaddaş (RAM/CPU) Optimizasiyası:** 2600+ mahnı və 27+ part olan nəhəng pleylistlərdə kompüterin donması və prosessorun 100% yüklənməsi aradan qaldırıldı. Mahnı məlumatları `%LOCALAPPDATA%/TrackDrop/cache` daxilində kəşlənərək təkrar keçidlərdə anında açılır.
- **Hissələr (Part) Arası Bloklama və Təhlükəsizlik:** Eyni anda bir neçə parta tıklandıqda donmanın qarşısını almaq üçün `isPlaylistLoading` kilidi əlavə edildi; istifadəçiyə paket yüklənənədək xəbərdarlıq bildirişi göstərilir.
- **Avtomatik Daxili Yenilənmə (Direct In-App Updater):** Proqram daxilindən GitHub Release vasitəsilə ən son versiyanı birbaşa endirib quraşdırma təmin edildi; istifadəçinin brauzerə yönləndirilməsinə ehtiyac qalmadı.
- **İnterfeys və Part Görünüşünün Təkmilləşdirilməsi:** Part düymələri arasındakı sıxlıq aradan qaldırıldı, oxunaqlı və səliqəli məsafələr təyin olundu.
- **Tam Çoxdilli (AZ / EN / РУС) Dəstək:** Bütün filtrlər, status bildirişləri, pleylist hissələri və düymələr üçün dil tərcümələri tamamlandı. Başlıqdakı dillər arası seçim hamar animasiya ilə təchiz edildi.
