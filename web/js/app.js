function escapeHtml(unsafe) {
  return (unsafe || "").toString()
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

window.onerror = function(message, source, lineno, colno, error) {
  try {
    if (window.pywebview && window.pywebview.api && window.pywebview.api.report_client_error) {
      window.pywebview.api.report_client_error(String(message), String(source || ""), lineno || 0, colno || 0);
    }
  } catch (e) {}
  return false;
};


// Translations Dictionary
const translations = {
  "AZ": {
    "subtitle": "Müasir səs və video yükləyici",
    "lbl_url": "Linki aşağıya yapışdırın:",
    "btn_paste": "Yapışdır",
    "btn_playlist_paste": "Yapışdır",
    "lbl_media": "Media Tipi:",
    "lbl_format": "Format:",
    "lbl_quality": "Keyfiyyət:",
    "lbl_download_btn": "Yüklə",
    "btn_cancel": "Ləğv et",
    "btn_cancel_playlist": "Ləğv Et",
    "lbl_fetch_btn": "Pleylisti Yüklə",
    "lbl_select_all": "Hamısını Seç",
    "lbl_download_selected": "Seçilənləri Yüklə",
    "history_title": "Yükləmə Tarixçəsi",
    "history_empty": "Hələ heç bir yükləmə yoxdur",
    "lbl_audio_segment": "Səs (MP3)",
    "lbl_video_segment": "Video (MP4)",
    "nav_single": "URL Yükləyici",
    "nav_playlist": "Pleylist Yükləyici",
    "status_extracting": "Məlumatlar alınır...",
    "status_downloading": "Yüklənir...",
    "status_converting": "Yüklənir...",
    "status_success": "✓ Uğurla yükləndi!",
    "status_error": "✕ Xəta baş verdi!",
    "status_cancelled": "⊘ Ləğv edildi!",
    "filter_all": "Hamısı",
    "filter_downloaded": "Yüklənənlər",
    "filter_pending": "Yüklənməyənlər",
    "search_placeholder": "Mahnı və ya sənətçi axtar...",
    "spotify_modal_title": "Spotify API Açarı Tənzimləmələri",
    "spotify_modal_desc": "Spotify pleylistlərində 100-dən çox mahnı olduqda hamısını tam əldə etmək üçün API açarı lazımdır. Tamamilə pulsuzdur.",
    "spotify_inst_title": "Açarı necə almaq olar?",
    "spotify_inst_step1": "1. Yaşıl düyməyə basıb developer.spotify.com saytına daxil olun.",
    "spotify_inst_step2": "2. Create an App düyməsinə basıb yaranan açarı kopyalayın.",
    "spotify_inst_step3": "3. Açarı yuxarıdakı xanaya yapışdırıb yadda saxlayın.",
    "btn_spotify_site": "Spotify-a Keç",
    "btn_spotify_cancel": "Ləğv Et",
    "btn_spotify_save": "Yadda Saxla",
    "btn_manage_api_key": "API Key",
    "spotify_key_invalid_toast": "Daxil edilmiş Spotify API açarı xətalıdır və ya vaxtı bitib! Zəhmət olmasa yeniləyin.",
    "gopro_title": "TrackDrop Premium ⚡",
    "gopro_desc": "Sənin üçün tamamilə pulsuzdur!",
    "gopro_feat_1": "Sevimli musiqilərini saniyələr içində yaddaşda saxla",
    "gopro_feat_2": "Reklamsız və gözləmə saniyələri olmadan yükləmə",
    "gopro_feat_3": "Heç bir limit, heç bir gizli ödəniş yoxdur",
    "gopro_feat_4": "Abunəlik dərdi olmadan ömürlük istifadə et",
    "btn_gopro_purchase": "Aktiv Et!",
    "btn_gopro_sidebar": "Premium Al",
    "status_premium_active": "Premium Aktivdir",
    "status_premium_btn_done": "Aktiv Edildi",
    "placeholder_url": "Spotify və ya YouTube linkini bura yapışdırın...",
    "placeholder_playlist_url": "Spotify və ya YouTube pleylist linkini bura yapışdırın...",
    "error_playlist_in_single": "Bu link pleylist yüklənilməsi üçündür. Zəhmət olmasa 'Pleylist Yükləyici' bölməsinə keçin.",
    "error_title": "Xəta",
    "ffmpeg_badge_ok": "FFmpeg Aktivdir",
    "ffmpeg_badge_missing": "FFmpeg Yoxdur (Yüklə)",
    "ffmpeg_modal_title": "FFmpeg Quraşdırılır",
    "ffmpeg_modal_status_starting": "Yükləmə başladılır...",
    "ffmpeg_modal_status_downloading": "FFmpeg serverdən yüklənir...",
    "ffmpeg_modal_status_installing": "Arxiv açılır və quraşdırılır...",
    "ffmpeg_modal_status_success": "FFmpeg uğurla quraşdırıldı! ✓",
    "ffmpeg_modal_status_error": "FFmpeg yüklənməsi xətası",
    "ffmpeg_stat_size": "Həcm",
    "ffmpeg_stat_speed": "Sürət",
    "ffmpeg_stat_eta": "Qalan Vaxt",
    "ffmpeg_modal_note": "Pəncərəni bağlasanız da yüklənmə arxa fonda davam edəcək.",
    "update_title": "Yeni yenilənmə var! 🚀",
    "update_desc": "Yeni versiya ({version}) artıq hazırdır. Yenilikləri və təkmilləşdirmələri əldə etmək üçün yükləyin.",
    "btn_update_download": "İndi Yüklə",
    "btn_update_close": "Bağla",
    "spotify_limit_title": "Spotify Pleylist Hissələri (100 Mahnı Limiti)",
    "spotify_limit_desc": "Spotify tətbiqlərə bir dəfədə maksimum 100 mahnı çəkməyə icazə verir. Bir neçə parta bölünmüş hissələrdən yükləyə bilərsiniz.",
    "search_results_title": "Axtarış Nəticələri",
    "selected_basket_title": "Seçilən Mahnılar",
    "btn_clear_basket": "Təmizlə",
    "btn_download_all": "Hamısını Yüklə",
    "basket_empty_desc": "Hələ heç bir mahnı seçilməyib. Nəticələrdən [+] ilə əlavə edin.",
    "songs_unit": "mahnı",
    "badge_downloaded": "Yüklənib",
    "pager_prev": "Əvvəlki",
    "pager_next": "Növbəti",
    "pager_info": "Səhifə {page} / {totalPages} · {start}–{end} / {total} mahnı",
    "all_completed": "Hamısı tamamlandı! ({count})",
    "wait_loading_part": "Zəhmət olmasa gözləyin, hazırda {part} yüklənir...",
    "wait_preparing_playlist": "Zəhmət olmasa gözləyin, pleylist məlumatları alınır və hissələrə bölünür...",
    "loading_part_notice": "Part {part} yüklənir, zəhmət olmasa gözləyin...",
    "btn_download_folder_title": "Yükləmə qovluğunu dəyiş",
    "folder_changed_toast": "Yükləmə qovluğu yeniləndi: ",
    "folder_default_lbl": "Yükləmə qovluğu"
  },
  "EN": {
    "subtitle": "Modern Audio and Video Downloader",
    "lbl_url": "Paste the link below:",
    "btn_paste": "Paste",
    "btn_playlist_paste": "Paste",
    "lbl_media": "Media Type:",
    "lbl_format": "Format:",
    "lbl_quality": "Quality:",
    "lbl_download_btn": "Download",
    "btn_cancel": "Cancel",
    "btn_cancel_playlist": "Cancel",
    "lbl_fetch_btn": "Fetch Playlist",
    "lbl_select_all": "Select All",
    "lbl_download_selected": "Download Selected",
    "history_title": "Download History",
    "history_empty": "No downloads yet",
    "lbl_audio_segment": "Audio (MP3)",
    "lbl_video_segment": "Video (MP4)",
    "nav_single": "URL Downloader",
    "nav_playlist": "Playlist Downloader",
    "status_extracting": "Fetching video info...",
    "status_downloading": "Downloading...",
    "status_converting": "Downloading...",
    "status_success": "✓ Successfully downloaded!",
    "status_error": "✕ An error occurred!",
    "status_cancelled": "⊘ Cancelled!",
    "filter_all": "All",
    "filter_downloaded": "Downloaded",
    "filter_pending": "Not Downloaded",
    "search_placeholder": "Search track or artist...",
    "spotify_modal_title": "Spotify API Key Settings",
    "spotify_modal_desc": "Spotify playlists require an API key to fetch more than 100 tracks without limits. It is completely free.",
    "spotify_inst_title": "How to get an API key?",
    "spotify_inst_step1": "1. Click the green button to open developer.spotify.com.",
    "spotify_inst_step2": "2. Click Create an App and copy the generated key/token.",
    "spotify_inst_step3": "3. Paste the key in the field above and click Save.",
    "btn_spotify_site": "Go to Spotify",
    "btn_spotify_cancel": "Cancel",
    "btn_spotify_save": "Save Key",
    "btn_manage_api_key": "API Key",
    "spotify_key_invalid_toast": "The Spotify API key entered is invalid or expired! Please update it.",
    "gopro_title": "TrackDrop Premium ⚡",
    "gopro_desc": "Completely free for you!",
    "gopro_feat_1": "Save your favorite music in seconds",
    "gopro_feat_2": "Ad-free download without waiting seconds",
    "gopro_feat_3": "No limits, no hidden fees",
    "gopro_feat_4": "Lifetime use without subscription hassle",
    "btn_gopro_purchase": "Activate Now!",
    "btn_gopro_sidebar": "Buy Premium",
    "status_premium_active": "Premium Active",
    "status_premium_btn_done": "Activated",
    "placeholder_url": "Paste Spotify or YouTube link here...",
    "placeholder_playlist_url": "Paste Spotify or YouTube playlist link here...",
    "error_playlist_in_single": "This link is for downloading playlists. Please switch to the 'Playlist Downloader' tab.",
    "error_title": "Error",
    "ffmpeg_badge_ok": "FFmpeg Active",
    "ffmpeg_badge_missing": "FFmpeg Missing (Click to install)",
    "ffmpeg_modal_title": "Installing FFmpeg",
    "ffmpeg_modal_status_starting": "Initializing download...",
    "ffmpeg_modal_status_downloading": "Downloading FFmpeg...",
    "ffmpeg_modal_status_installing": "Extracting and installing...",
    "ffmpeg_modal_status_success": "FFmpeg installed successfully! ✓",
    "ffmpeg_modal_status_error": "FFmpeg installation failed",
    "ffmpeg_stat_size": "Size",
    "ffmpeg_stat_speed": "Speed",
    "ffmpeg_stat_eta": "Remaining",
    "ffmpeg_modal_note": "Closing this window will not stop the background download.",
    "update_title": "New update available! 🚀",
    "update_desc": "A new version ({version}) is now available. Download it to get the latest features and fixes.",
    "btn_update_download": "Download Now",
    "btn_update_close": "Close",
    "spotify_limit_title": "Spotify Playlist Parts (100 Track Limit)",
    "spotify_limit_desc": "Spotify allows downloading a maximum of 100 tracks at a time. You can download tracks in split parts.",
    "search_results_title": "Search Results",
    "selected_basket_title": "Selected Tracks",
    "btn_clear_basket": "Clear",
    "btn_download_all": "Download All",
    "basket_empty_desc": "No tracks selected yet. Click [+] to add.",
    "songs_unit": "tracks",
    "badge_downloaded": "Downloaded",
    "pager_prev": "Previous",
    "pager_next": "Next",
    "pager_info": "Page {page} / {totalPages} · {start}–{end} / {total} tracks",
    "all_completed": "All completed! ({count})",
    "wait_loading_part": "Please wait, loading {part} in progress...",
    "wait_preparing_playlist": "Please wait, playlist info is being processed...",
    "loading_part_notice": "Loading Part {part}, please wait...",
    "btn_download_folder_title": "Change download folder",
    "folder_changed_toast": "Download folder updated: ",
    "folder_default_lbl": "Download Folder"
  },
  "РУС": {
    "subtitle": "Современный загрузчик аудио и видео",
    "lbl_url": "Вставьте ссылку ниже:",
    "btn_paste": "Вставить",
    "btn_playlist_paste": "Вставить",
    "lbl_media": "Тип медиа:",
    "lbl_format": "Формат:",
    "lbl_quality": "Качество:",
    "lbl_download_btn": "Скачать",
    "btn_cancel": "Отменить",
    "btn_cancel_playlist": "Отмена",
    "lbl_fetch_btn": "Загрузить плейлист",
    "lbl_select_all": "Выбрать все",
    "lbl_download_selected": "Скачать выбранное",
    "history_title": "История загрузок",
    "history_empty": "Пока нет загрузок",
    "lbl_audio_segment": "Аудио (MP3)",
    "lbl_video_segment": "Видео (MP4)",
    "nav_single": "URL Загрузчик",
    "nav_playlist": "Плейлист загрузчик",
    "status_extracting": "Получение информации...",
    "status_downloading": "Загрузка...",
    "status_converting": "Загрузка...",
    "status_success": "✓ Успешно скачано!",
    "status_error": "✕ Произошла ошибка!",
    "status_cancelled": "⊘ Отменено!",
    "filter_all": "Все",
    "filter_downloaded": "Скачанные",
    "filter_pending": "Нескачанные",
    "search_placeholder": "Поиск трека или исполнителя...",
    "spotify_modal_title": "Настройка API ключа Spotify",
    "spotify_modal_desc": "Для загрузки плейлистов Spotify без ограничений (более 100 треков) требуется API ключ. Это абсолютно бесплатно.",
    "spotify_inst_title": "Как получить API ключ?",
    "spotify_inst_step1": "1. Нажмите зеленую кнопку и перейдите на developer.spotify.com.",
    "spotify_inst_step2": "2. Нажмите кнопку 'Create an App' и скопируйте созданный ключ.",
    "spotify_inst_step3": "3. Вставьте ключ в поле выше и нажмите 'Сохранить'.",
    "btn_spotify_site": "Перейти в Spotify",
    "btn_spotify_cancel": "Отмена",
    "btn_spotify_save": "Сохранить ключ",
    "btn_manage_api_key": "API Key",
    "spotify_key_invalid_toast": "Введенный API ключ Spotify недействителен или срок его действия истек! Пожалуйста, обновите его.",
    "gopro_title": "TrackDrop Premium ⚡",
    "gopro_desc": "Для вас абсолютно бесплатно!",
    "gopro_feat_1": "Сохраняйте любимую музыку за секунды",
    "gopro_feat_2": "Загрузка без рекламы и ожидания",
    "gopro_feat_3": "Без лимитов и скрытых комиссий",
    "gopro_feat_4": "Пожизненное использование без лишних подписок",
    "btn_gopro_purchase": "Активировать!",
    "btn_gopro_sidebar": "Купить Premium",
    "status_premium_active": "Premium Активен",
    "status_premium_btn_done": "Активировано",
    "placeholder_url": "Вставьте ссылку на Spotify или YouTube...",
    "placeholder_playlist_url": "Вставьте ссылку на плейлист Spotify или YouTube...",
    "error_playlist_in_single": "Эта ссылка предназначена для загрузки плейлистов. Пожалуйста, перейдите в раздел 'Плейлист загрузчик'.",
    "error_title": "Ошибка",
    "ffmpeg_badge_ok": "FFmpeg Активен",
    "ffmpeg_badge_missing": "FFmpeg Отсутствует (Нажмите для установки)",
    "ffmpeg_modal_title": "Установка FFmpeg",
    "ffmpeg_modal_status_starting": "Инициализация загрузки...",
    "ffmpeg_modal_status_downloading": "Загрузка FFmpeg...",
    "ffmpeg_modal_status_installing": "Распаковка и установка...",
    "ffmpeg_modal_status_success": "FFmpeg успешно установлен! ✓",
    "ffmpeg_modal_status_error": "Ошибка при установке FFmpeg",
    "ffmpeg_stat_size": "Размер",
    "ffmpeg_stat_speed": "Скорость",
    "ffmpeg_stat_eta": "Осталось",
    "ffmpeg_modal_note": "Закрытие окна не прервет фоновую загрузку.",
    "update_title": "Доступно обновление! 🚀",
    "update_desc": "Новая версия ({version}) уже доступна. Загрузите её, чтобы получить новые функции и исправления.",
    "btn_update_download": "Скачать",
    "btn_update_close": "Закрыть",
    "spotify_limit_title": "Части плейлиста Spotify (Лимит 100 треков)",
    "spotify_limit_desc": "Spotify позволяет загружать максимум 100 треков за раз. Вы можете скачать треки по частям.",
    "search_results_title": "Результаты поиска",
    "selected_basket_title": "Выбранные треки",
    "btn_clear_basket": "Очистить",
    "btn_download_all": "Скачать все",
    "basket_empty_desc": "Пока ничего не выбрано. Нажмите [+] в результатах.",
    "songs_unit": "треков",
    "badge_downloaded": "Скачано",
    "pager_prev": "Назад",
    "pager_next": "Вперед",
    "pager_info": "Страница {page} / {totalPages} · {start}–{end} / {total} треков",
    "all_completed": "Все завершено! ({count})",
    "wait_loading_part": "Пожалуйста, подождите, идет загрузка {part}...",
    "wait_preparing_playlist": "Пожалуйста, подождите, информация о плейлисте обрабатывается...",
    "loading_part_notice": "Загружается Part {part}, пожалуйста, подождите...",
    "btn_download_folder_title": "Изменить папку сохранения",
    "folder_changed_toast": "Папка сохранения обновлена: ",
    "folder_default_lbl": "Папка загрузки"
  }
};

let currentLanguage = "AZ";
let activeTab = "single";
let mediaType = "audio";
let isDownloading = false;
let fetchedTracks = [];
let currentPlaylistName = "";

const mediaConfig = {
  audio: {
    formats: ["MP3", "M4A", "WAV"],
    qualities: ["128 kbps", "192 kbps", "256 kbps", "320 kbps"]
  },
  video: {
    formats: ["MP4", "MKV"],
    qualities: ["144p", "360p", "480p", "720p", "1080p", "2K (1440p)", "4K (2160p)"]
  }
};

const playlistQualityConfig = {
  audio: ["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
  video: ["360p", "480p", "720p", "1080p", "2K (1440p)", "4K (2160p)"]
};

let playlistMediaType = "audio";
let playlistQuality = "320 kbps";

let currentDownloadFolder = "";

function updateFolderButtonDisplay() {
  const lbl = document.getElementById("lbl-download-folder");
  const btn = document.getElementById("btn-download-folder");
  if (!lbl) return;

  const t = translations[currentLanguage] || translations["AZ"];
  if (currentDownloadFolder) {
    const parts = currentDownloadFolder.replace(/\\/g, '/').split('/').filter(Boolean);
    const folderName = parts.length > 0 ? parts[parts.length - 1] : currentDownloadFolder;
    lbl.textContent = folderName;
    if (btn) {
      btn.title = `${t.btn_download_folder_title || "Yükləmə qovluğunu dəyiş"}\n${currentDownloadFolder}`;
    }
  } else {
    lbl.textContent = t.folder_default_lbl || "Yükləmə qovluğu";
    if (btn) {
      btn.title = t.btn_download_folder_title || "Yükləmə qovluğunu dəyiş";
    }
  }
}

function loadDownloadFolder() {
  if (window.pywebview && window.pywebview.api && window.pywebview.api.get_download_dir) {
    window.pywebview.api.get_download_dir().then(dir => {
      if (dir) {
        currentDownloadFolder = dir;
        updateFolderButtonDisplay();
      }
    }).catch(err => {
      console.warn("Could not get download dir:", err);
    });
  }
}

function changeDownloadFolder() {
  if (window.pywebview && window.pywebview.api && window.pywebview.api.choose_download_dir) {
    window.pywebview.api.choose_download_dir().then(chosen => {
      if (chosen) {
        currentDownloadFolder = chosen;
        updateFolderButtonDisplay();
        const t = translations[currentLanguage] || translations["AZ"];
        showInAppToast((t.folder_changed_toast || "Yükləmə qovluğu yeniləndi: ") + chosen, "success");
      }
    }).catch(err => {
      console.error("Change download dir error:", err);
    });
  }
}

// Initialize Application UI
document.addEventListener("DOMContentLoaded", () => {
  setMediaType("audio");
  changeLanguage("AZ");

  // Expose API check to python loaded hook
  setTimeout(() => {
    checkFfmpeg();
    loadDownloadFolder();
    if (window.pywebview && window.pywebview.api && window.pywebview.api.check_updates) {
      window.pywebview.api.check_updates();
    }
  }, 1000);
});

function changeLanguage(lang) {
  currentLanguage = lang;
  const htmlLangMap = { "AZ": "az", "EN": "en", "РУС": "ru" };
  document.documentElement.lang = htmlLangMap[lang] || "en";
  const t = translations[lang] || translations["AZ"];

  // 1. Instant active state animation on language pills
  const activeLangClass = "px-3 py-1.5 text-[11px] font-bold rounded-lg bg-[#9D4EDD] text-white shadow-md shadow-[#9D4EDD]/30 transition-all duration-300 ease-out cursor-pointer scale-105";
  const inactiveLangClass = "px-3 py-1.5 text-[11px] font-bold rounded-lg text-[#A0A0A0] hover:text-white hover:bg-white/5 transition-all duration-300 ease-out cursor-pointer scale-100";

  const btnAz = document.getElementById("lang-az");
  const btnEn = document.getElementById("lang-en");
  const btnRus = document.getElementById("lang-rus");

  if (btnAz) btnAz.className = (lang === "AZ") ? activeLangClass : inactiveLangClass;
  if (btnEn) btnEn.className = (lang === "EN") ? activeLangClass : inactiveLangClass;
  if (btnRus) btnRus.className = (lang === "РУС") ? activeLangClass : inactiveLangClass;

  const safeSetText = (id, text) => {
    const el = document.getElementById(id);
    if (el && text !== undefined && text !== null) el.textContent = text;
  };

  // 2. Safe UI labels
  safeSetText("header-subtitle", t.subtitle);
  safeSetText("lbl-url", t.lbl_url);
  safeSetText("btn-paste", t.btn_paste);
  safeSetText("btn-playlist-paste", t.btn_playlist_paste);
  safeSetText("lbl-media", t.lbl_media);
  safeSetText("lbl-format", t.lbl_format);
  safeSetText("lbl-quality", t.lbl_quality);
  safeSetText("lbl-audio-segment", t.lbl_audio_segment);
  safeSetText("lbl-video-segment", t.lbl_video_segment);
  safeSetText("lbl-fetch-btn", t.lbl_fetch_btn);
  safeSetText("lbl-select-all", t.lbl_select_all);
  safeSetText("lbl-download-selected", t.lbl_download_selected);
  safeSetText("history-title", t.history_title);
  safeSetText("nav-single-label", t.nav_single);
  safeSetText("nav-playlist-label", t.nav_playlist);

  const folderBtn = document.getElementById("btn-download-folder");
  if (folderBtn && t.btn_download_folder_title) {
    folderBtn.title = t.btn_download_folder_title;
  }
  updateFolderButtonDisplay();

  // Status Filter Labels (Hamısı, Yüklənənlər, Yüklənməyənlər)
  safeSetText("lbl-filter-all", t.filter_all || "Hamısı");
  safeSetText("lbl-filter-downloaded", t.filter_downloaded || "Yüklənənlər");
  safeSetText("lbl-filter-pending", t.filter_pending || "Yüklənməyənlər");

  // Input placeholders
  const urlInput = document.getElementById("url-input");
  if (urlInput) {
    urlInput.placeholder = currentLanguage === "AZ"
      ? "YouTube və ya Spotify linki yapışdırın..."
      : (currentLanguage === "РУС" ? "Вставьте ссылку на YouTube или Spotify..." : "Paste YouTube or Spotify link here...");
  }
  const playlistUrlInput = document.getElementById("playlist-url-input");
  if (playlistUrlInput) playlistUrlInput.placeholder = t.placeholder_playlist_url;
  const plSearchInput = document.getElementById("playlist-search");
  if (plSearchInput) plSearchInput.placeholder = t.search_placeholder || "Mahnı və ya sənətçi axtar...";

  // Modals & Toolbar Buttons
  safeSetText("btn-manage-api-key", t.btn_manage_api_key || "API Key");
  safeSetText("spotify-modal-title", t.spotify_modal_title);
  safeSetText("spotify-modal-desc", t.spotify_modal_desc);
  safeSetText("spotify-inst-title", t.spotify_inst_title);
  safeSetText("btn-spotify-site-text", t.btn_spotify_site || "Spotify-a Keç");
  safeSetText("btn-spotify-cancel", t.btn_spotify_cancel);
  safeSetText("btn-spotify-save", t.btn_spotify_save);

  const instList = document.getElementById("spotify-inst-list");
  if (instList) {
    instList.innerHTML = `
      <p>${t.spotify_inst_step1}</p>
      <p>${t.spotify_inst_step2}</p>
      <p>${t.spotify_inst_step3}</p>
    `;
  }

  safeSetText("ffmpeg-modal-title", t.ffmpeg_modal_title);
  safeSetText("ffmpeg-stat-lbl-size", t.ffmpeg_stat_size);
  safeSetText("ffmpeg-stat-lbl-speed", t.ffmpeg_stat_speed);
  safeSetText("ffmpeg-stat-lbl-eta", t.ffmpeg_stat_eta);
  safeSetText("ffmpeg-modal-note", t.ffmpeg_modal_note);
  safeSetText("lbl-cancel-playlist", t.btn_cancel_playlist);
  safeSetText("spotify-limit-title", t.spotify_limit_title);
  safeSetText("spotify-limit-desc", t.spotify_limit_desc);

  safeSetText("gopro-title", t.gopro_title);
  safeSetText("gopro-desc", t.gopro_desc);
  safeSetText("gopro-feat-1", t.gopro_feat_1);
  safeSetText("gopro-feat-2", t.gopro_feat_2);
  safeSetText("gopro-feat-3", t.gopro_feat_3);
  safeSetText("gopro-feat-4", t.gopro_feat_4);
  safeSetText("btn-gopro-purchase", isPremiumActive ? t.status_premium_btn_done : t.btn_gopro_purchase);

  const sidebarBtnSpan = document.querySelector("#btn-gopro-sidebar");
  if (sidebarBtnSpan) {
    sidebarBtnSpan.textContent = isPremiumActive ? t.status_premium_active : t.btn_gopro_sidebar;
  }

  const goproDetail = document.getElementById("gopro-desc-detail");
  if (goproDetail) {
    if (lang === "AZ") {
      goproDetail.textContent = "TrackDrop-u seçdiyin üçün təşəkkürlər. Bu proqramdan istifadə edirsənsə, bütün premium funksiyalar sənə tamamilə pulsuzdur:";
      goproDetail.style.display = "block";
    } else if (lang === "EN") {
      goproDetail.textContent = "Thanks for choosing TrackDrop. Since you are using this app, all premium features are completely free for you:";
      goproDetail.style.display = "block";
    } else if (lang === "РУС") {
      goproDetail.textContent = "Спасибо, что выбрали TrackDrop. Поскольку вы используете это приложение, все премиум-функции для вас абсолютно бесплатны:";
      goproDetail.style.display = "block";
    } else {
      goproDetail.style.display = "none";
    }
  }

  // Footer
  safeSetText("footer-version", "v1.8");

  // History empty state
  const historyList = document.getElementById("history-list");
  if (historyList && historyList.children.length === 1 && historyList.children[0].id === "history-empty") {
    safeSetText("history-empty", t.history_empty);
  }

  // Update playlist status text
  updatePlaylistStatusMsg();

  // Re-render track list and parts if loaded
  try {
    if (fetchedTracks && fetchedTracks.length > 0) {
      renderTrackPage();
      if (currentPlaylistTotal > 100) {
        renderPlaylistPartButtons(currentPlaylistTotal, currentPlaylistOffset, currentPlaylistLimit);
      }
    }
  } catch (e) {
    console.error("Error updating playlist tracks on language change:", e);
  }

  // Update download button labels
  updateDownloadButtonLabel();
  updateDownloadSelectedButtonText();
}

function updatePlaylistStatusMsg() {
  const plStatus = document.getElementById("playlist-status-msg");
  if (!plStatus || !currentPlaylistName) return;
  if (currentPlaylistTotal > 100) {
    const partNum = Math.floor(currentPlaylistOffset / currentPlaylistLimit) + 1;
    const startNum = currentPlaylistOffset + 1;
    const endNum = Math.min(currentPlaylistOffset + (fetchedTracks ? fetchedTracks.length : 0), currentPlaylistTotal);
    const partWord = currentLanguage === "AZ" ? "Part" : (currentLanguage === "EN" ? "Part" : "Часть");
    plStatus.textContent = `${currentPlaylistName} — ${partWord} ${partNum} (${startNum}-${endNum} / ${currentPlaylistTotal})`;
  } else if (currentPlaylistTotal > 0) {
    const trackWord = currentLanguage === "AZ" ? "mahnı" : (currentLanguage === "EN" ? "tracks" : "треков");
    plStatus.textContent = `${currentPlaylistName} (${currentPlaylistTotal} ${trackWord})`;
  }
}

function updateDownloadButtonLabel() {
  const btn = document.getElementById("btn-download");
  const t = translations[currentLanguage];
  if (isDownloading) {
    btn.innerHTML = `<i class="fa-solid fa-xmark text-sm"></i> <span>${t.btn_cancel}</span>`;
    btn.className = "w-full py-4 bg-[#7F1D1D] hover:bg-[#991B1B] text-white font-extrabold text-sm rounded-xl flex items-center justify-center gap-2.5 tracking-wide transition-all active:scale-98 shadow-lg shadow-[#7F1D1D]/15";
  } else {
    btn.innerHTML = `<i class="fa-solid fa-cloud-arrow-down text-base"></i> <span>${t.lbl_download_btn}</span>`;
    btn.className = "w-full py-4 bg-[#9D4EDD] hover:bg-[#8A2BE2] text-white font-extrabold text-sm rounded-xl flex items-center justify-center gap-2.5 tracking-wide transition-all active:scale-98 shadow-lg shadow-[#9D4EDD]/15";
  }
}

function switchTab(tab) {
  activeTab = tab;

  // Update nav menu active styles
  const btnSingle = document.getElementById("nav-single");
  const btnPlaylist = document.getElementById("nav-playlist");

  const activeClass = "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-semibold transition-all duration-200 bg-[#9D4EDD] text-white shadow-lg shadow-[#9D4EDD]/20";
  const inactiveClass = "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left text-sm font-semibold text-[#A0A0A0] hover:text-white hover:bg-[#282828] transition-all duration-200";

  if (btnSingle) btnSingle.className = tab === "single" ? activeClass : inactiveClass;
  if (btnPlaylist) btnPlaylist.className = tab === "playlist" ? activeClass : inactiveClass;

  const tabSingleContent = document.getElementById("tab-single-content");
  const tabPlaylistContent = document.getElementById("tab-playlist-content");

  if (tabSingleContent) {
    if (tab === "single") tabSingleContent.classList.add("active");
    else tabSingleContent.classList.remove("active");
  }
  if (tabPlaylistContent) {
    if (tab === "playlist") tabPlaylistContent.classList.add("active");
    else tabPlaylistContent.classList.remove("active");
  }
}

function setMediaType(type) {
  mediaType = type;

  const btnAudio = document.getElementById("media-audio");
  const btnVideo = document.getElementById("media-video");

  const activeClass = "px-4 py-2 rounded-full text-xs font-bold bg-[#9D4EDD] text-white border border-[#9D4EDD] transition-all";
  const inactiveClass = "px-4 py-2 rounded-full text-xs font-bold text-[#A0A0A0] border border-[#3A3A3A] hover:border-[#9D4EDD] hover:text-white transition-all";

  if (type === "audio") {
    btnAudio.className = activeClass;
    btnVideo.className = inactiveClass;
  } else {
    btnVideo.className = activeClass;
    btnAudio.className = inactiveClass;
  }

  renderPills();
}

let selectedExt = "";
let selectedQuality = "";

function renderPills() {
  const config = mediaConfig[mediaType];

  selectedExt = config.formats[0];
  
  if (mediaType === "video") {
    selectedQuality = config.qualities.includes("1080p") ? "1080p" : config.qualities[config.qualities.length - 1];
  } else {
    selectedQuality = config.qualities.includes("320 kbps") ? "320 kbps" : config.qualities[config.qualities.length - 1];
  }

  const extContainer = document.getElementById("ext-pills");
  const qualityContainer = document.getElementById("quality-pills");

  const pillActive = "px-3 py-1.5 rounded-full text-[11px] font-bold transition-all border bg-[#9D4EDD] text-white border-[#9D4EDD]";
  const pillInactive = "px-3 py-1.5 rounded-full text-[11px] font-bold transition-all border text-[#A0A0A0] border-[#3A3A3A] hover:border-[#9D4EDD] hover:text-white";

  extContainer.innerHTML = config.formats.map(f =>
    `<button onclick="selectExt('${f}')" id="ext-pill-${f}" class="${f === selectedExt ? pillActive : pillInactive}">${f}</button>`
  ).join("");

  // Video quality: flex wrap; Audio: single row
  if (mediaType === "video") {
    qualityContainer.className = "flex gap-1.5 flex-wrap";
  } else {
    qualityContainer.className = "flex gap-2 flex-wrap";
  }

  qualityContainer.innerHTML = config.qualities.map(q =>
    `<button onclick="selectQuality('${q}')" id="quality-pill-${q.replace(/[^a-zA-Z0-9]/g, '_')}" class="${q === selectedQuality ? pillActive : pillInactive}">${q}</button>`
  ).join("");
}

function selectExt(val) {
  selectedExt = val;
  const config = mediaConfig[mediaType];
  config.formats.forEach(f => {
    const btn = document.getElementById(`ext-pill-${f}`);
    if (btn) btn.className = `px-3 py-1.5 rounded-full text-[11px] font-bold transition-all border ${f === val ? 'bg-[#9D4EDD] text-white border-[#9D4EDD]' : 'text-[#A0A0A0] border-[#3A3A3A] hover:border-[#9D4EDD] hover:text-white'}`;
  });
}

function selectQuality(val) {
  selectedQuality = val;
  const config = mediaConfig[mediaType];
  config.qualities.forEach(q => {
    const btn = document.getElementById(`quality-pill-${q.replace(/[^a-zA-Z0-9]/g, '_')}`);
    if (btn) btn.className = `px-3 py-1.5 rounded-full text-[11px] font-bold transition-all border ${q === val ? 'bg-[#9D4EDD] text-white border-[#9D4EDD]' : 'text-[#A0A0A0] border-[#3A3A3A] hover:border-[#9D4EDD] hover:text-white'}`;
  });
}

// Check FFmpeg status and update badge
function checkFfmpeg() {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.check_ffmpeg().then(hasFfmpeg => {
      const badge = document.getElementById("ffmpeg-badge");
      if (!badge) return;
      const t = translations[currentLanguage];
      if (hasFfmpeg) {
        badge.className = "text-[10px] bg-[#10B981] text-white px-2.5 py-1 rounded-full font-bold cursor-default";
        badge.innerHTML = `<i class="fa-solid fa-circle-check mr-1"></i> ${t.ffmpeg_badge_ok}`;
        badge.onclick = null;
      } else {
        badge.className = "text-[10px] bg-[#EF4444] text-white px-2.5 py-1 rounded-full font-bold cursor-pointer hover:opacity-90 transition-all";
        badge.innerHTML = `<i class="fa-solid fa-circle-exclamation mr-1"></i> ${t.ffmpeg_badge_missing}`;
        badge.onclick = installFfmpeg;
      }
    });
  }
}

function installFfmpeg() {
  showFfmpegModal();
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.download_ffmpeg();
  }
}

// FFmpeg Modal Animation and Logic
window.showFfmpegModal = (existingData) => {
  const modal = document.getElementById("ffmpeg-modal");
  const card = document.getElementById("ffmpeg-modal-card");
  if (!modal || !card) return;

  modal.classList.remove("hidden");
  // Trigger smooth enter animation
  requestAnimationFrame(() => {
    modal.classList.remove("opacity-0");
    modal.classList.add("opacity-100");
    card.classList.remove("scale-95");
    card.classList.add("scale-100");
  });

  if (existingData) {
    window.updateFfmpegModalProgress(existingData);
  }
};

window.closeFfmpegModal = () => {
  const modal = document.getElementById("ffmpeg-modal");
  const card = document.getElementById("ffmpeg-modal-card");
  if (!modal || !card) return;

  modal.classList.remove("opacity-100");
  modal.classList.add("opacity-0");
  card.classList.remove("scale-100");
  card.classList.add("scale-95");

  setTimeout(() => {
    modal.classList.add("hidden");
  }, 250);
};

window.updateFfmpegModalProgress = (data) => {
  const t = translations[currentLanguage];
  const pct = data.pct || 0;
  const status = data.status || "downloading";
  const dlMb = data.downloaded_mb || 0;
  const totMb = data.total_mb || 0;
  const remMb = data.remaining_mb || 0;
  const speedStr = data.speed_str || "0.0 MB/s";
  const etaSec = data.eta_sec || 0;

  const pctEl = document.getElementById("ffmpeg-modal-pct");
  const fillEl = document.getElementById("ffmpeg-modal-bar-fill");
  const statusEl = document.getElementById("ffmpeg-modal-status");
  const sizeEl = document.getElementById("ffmpeg-modal-size");
  const speedEl = document.getElementById("ffmpeg-modal-speed");
  const etaEl = document.getElementById("ffmpeg-modal-eta");

  if (pctEl) pctEl.textContent = `${pct}%`;
  if (fillEl) fillEl.style.width = `${pct}%`;

  if (statusEl) {
    if (status === "downloading") {
      statusEl.textContent = `${t.ffmpeg_modal_status_downloading} (${pct}%)`;
    } else if (status === "installing") {
      statusEl.textContent = t.ffmpeg_modal_status_installing;
    }
  }

  if (sizeEl) {
    sizeEl.textContent = totMb > 0 ? `${dlMb} / ${totMb} MB` : `${dlMb} MB`;
  }
  if (speedEl) {
    speedEl.textContent = speedStr;
  }
  if (etaEl) {
    if (status === "installing") {
      etaEl.textContent = "...";
    } else if (etaSec > 60) {
      const m = Math.floor(etaSec / 60);
      const s = etaSec % 60;
      etaEl.textContent = `${m}m ${s}s`;
    } else if (etaSec > 0) {
      etaEl.textContent = `${etaSec}s`;
    } else {
      etaEl.textContent = "--";
    }
  }
};

window.onFfmpegSuccess = () => {
  const t = translations[currentLanguage];
  const icon = document.getElementById("ffmpeg-modal-icon");
  const title = document.getElementById("ffmpeg-modal-title");
  const status = document.getElementById("ffmpeg-modal-status");
  const fill = document.getElementById("ffmpeg-modal-bar-fill");
  const pct = document.getElementById("ffmpeg-modal-pct");

  if (icon) {
    icon.className = "fa-solid fa-circle-check text-[#10B981] text-2xl";
  }
  if (title) title.textContent = t.ffmpeg_badge_ok;
  if (status) status.textContent = t.ffmpeg_modal_status_success;
  if (fill) fill.style.width = "100%";
  if (pct) {
    pct.textContent = "100%";
    pct.className = "text-lg font-black text-[#10B981]";
  }

  checkFfmpeg();
  setTimeout(() => {
    window.closeFfmpegModal();
    // Reset icon and classes after closing
    setTimeout(() => {
      if (icon) icon.className = "fa-solid fa-cloud-arrow-down fa-bounce";
      if (pct) pct.className = "text-lg font-black text-[#9D4EDD]";
    }, 400);
  }, 1600);
};

window.onFfmpegError = (errorMsg) => {
  const t = translations[currentLanguage];
  const icon = document.getElementById("ffmpeg-modal-icon");
  const status = document.getElementById("ffmpeg-modal-status");
  if (icon) icon.className = "fa-solid fa-triangle-exclamation text-[#EF4444] text-2xl";
  if (status) status.textContent = `${t.ffmpeg_modal_status_error}: ${errorMsg}`;
  checkFfmpeg();
};

// Clipboard integration
function pasteFromClipboard() {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.get_clipboard_text().then(text => {
      if (text) {
        document.getElementById("url-input").value = text;
      }
    });
  }
}

function clearUrlInput() {
  const input = document.getElementById("url-input");
  if (input) input.value = "";
  hideSearchPanel();
}

function pastePlaylistUrl() {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.get_clipboard_text().then(text => {
      if (text) {
        document.getElementById("playlist-url-input").value = text;
      }
    });
  }
}

// Single Downloader Action
function startSingleDownload() {
  if (isDownloading) {
    if (window.pywebview && window.pywebview.api) {
      window.pywebview.api.cancel_download();
    }
    return;
  }

  // If user selected songs from Spotify/YouTube live search via (+) checkmarks
  if (persistentSelectedSongs && persistentSelectedSongs.length > 0) {
    downloadSelectedSearchResults();
    return;
  }

  const url = document.getElementById("url-input").value.trim();
  if (!url) {
    alert(translations[currentLanguage].error_title + ": " + (currentLanguage === "AZ" ? "Link və ya axtarış sözü daxil edin!" : "Please enter a URL or search track!"));
    return;
  }

  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.check_ffmpeg().then(hasFfmpeg => {
      if (!hasFfmpeg) {
        installFfmpeg();
        return;
      }

      isDownloading = true;
      updateDownloadButtonLabel();

      const ext = selectedExt;
      const quality = selectedQuality;

      document.getElementById("progress-box").classList.remove("hidden");
      window.pywebview.api.download_single(url, mediaType, quality, ext);
    });
  }
}

window.updateDownloadProgress = (pct, status, details) => {
  const fill = document.getElementById("progress-bar-fill");
  const pctLbl = document.getElementById("progress-pct");
  const statusLbl = document.getElementById("progress-status");
  const detailsLbl = document.getElementById("progress-details");
  const t = translations[currentLanguage];

  fill.style.width = `${pct}%`;
  pctLbl.textContent = `${pct}%`;

  if (status === "error" && details === "ERROR_PLAYLIST_IN_SINGLE") {
    detailsLbl.textContent = t.error_playlist_in_single;
  } else {
    detailsLbl.textContent = details;
  }

  if (status === "extracting") {
    statusLbl.textContent = t.status_extracting;
  } else if (status === "downloading") {
    statusLbl.textContent = t.status_downloading;
  } else if (status === "converting") {
    statusLbl.textContent = t.status_converting;
  } else if (status === "success") {
    statusLbl.textContent = t.status_success;
    document.getElementById("progress-box").classList.add("hidden");
  } else if (status === "error") {
    statusLbl.textContent = t.status_error;
  } else if (status === "cancelled") {
    statusLbl.textContent = t.status_cancelled;
    document.getElementById("progress-box").classList.add("hidden");
  }
};

window.resetDownloadButton = () => {
  isDownloading = false;
  updateDownloadButtonLabel();
};

// History log
window.addHistoryItem = (filename) => {
  const list = document.getElementById("history-list");
  const empty = document.getElementById("history-empty");
  if (empty) {
    empty.remove();
  }

  const date = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const entry = document.createElement("div");
  entry.className = "flex items-center justify-between bg-[#242424] rounded-xl border border-[#282828] p-3 text-xs font-semibold hover:border-[#9D4EDD] transition-all";
  entry.innerHTML = `
    <div class="flex items-center gap-2 truncate">
      <span class="text-[#9D4EDD]"><i class="fa-solid fa-circle-check"></i></span>
      <span class="text-white truncate">${filename}</span>
    </div>
    <span class="text-[#A0A0A0] text-[10px] shrink-0">${date}</span>
  `;
  list.insertBefore(entry, list.firstChild);
};

// Playlist Downloader Actions
let lastPlaylistUrl = "";
let currentPlaylistOffset = 0;
let currentPlaylistLimit = 100;
let currentPlaylistTotal = 0;
const playlistPartCache = {}; // cacheKey: `${url}_${offset}_${limit}` -> res
let isPlaylistLoading = false;
let currentLoadingPartNum = null;

function fetchPlaylist(offset = 0, limit = 100) {
  const targetPart = Math.floor(offset / limit) + 1;

  if (isPlaylistLoading) {
    const activeMsg = currentLoadingPartNum ? `Part ${currentLoadingPartNum}` : "Part";
    const warnTemplate = translations[currentLanguage].wait_loading_part || "Zəhmət olmasa gözləyin, hazırda {part} yüklənir...";
    showInAppToast(warnTemplate.replace("{part}", activeMsg), "error");
    return;
  }

  const urlInput = document.getElementById("playlist-url-input");
  const url = (urlInput ? urlInput.value.trim() : "") || lastPlaylistUrl;
  if (!url) {
    alert(translations[currentLanguage].error_title + ": " + (currentLanguage === "AZ" ? "Link boş ola bilməz!" : "URL is empty!"));
    return;
  }
  lastPlaylistUrl = url;
  currentPlaylistOffset = offset;
  currentPlaylistLimit = limit;

  const cacheKey = `${url}_${offset}_${limit}`;
  if (playlistPartCache[cacheKey]) {
    displayTracks(playlistPartCache[cacheKey].playlist_name, playlistPartCache[cacheKey].tracks, playlistPartCache[cacheKey]);
    return;
  }

  isPlaylistLoading = true;
  currentLoadingPartNum = targetPart;

  let loadingNotice = "";
  if (offset === 0 && !currentPlaylistTotal) {
    loadingNotice = translations[currentLanguage].wait_preparing_playlist || "Zəhmət olmasa gözləyin, pleylist məlumatları alınır və hissələrə bölünür...";
  } else {
    const noticeTemplate = translations[currentLanguage].loading_part_notice || "Part {part} yüklənir, zəhmət olmasa gözləyin...";
    loadingNotice = noticeTemplate.replace("{part}", targetPart);
  }
  showInAppToast(loadingNotice, "success");

  const btn = document.getElementById("btn-fetch-playlist");
  if (btn) {
    btn.setAttribute("disabled", "true");
    btn.textContent = currentLanguage === "AZ" ? "Yüklənir..." : "Fetching...";
  }

  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.fetch_playlist(url, offset, limit).then(res => {
      isPlaylistLoading = false;
      currentLoadingPartNum = null;
      if (btn) {
        btn.removeAttribute("disabled");
        btn.innerHTML = `<span id="lbl-fetch-btn">${translations[currentLanguage].lbl_fetch_btn}</span>`;
      }

      if (res.error) {
        if (res.error === "spotify_auth_required") {
          window.showSpotifyAuthModal();
        } else if (res.error === "spotify_token_invalid") {
          showInAppToast(translations[currentLanguage].spotify_key_invalid_toast || "Spotify API açarı xətalıdır və ya vaxtı bitib!", "error");
          window.showSpotifyAuthModal();
        } else if (res.error === "single_track_in_playlist") {
          const tabName = translations[currentLanguage].nav_single || "URL Yükləyici";
          showInAppToast(currentLanguage === "AZ" 
            ? `Bu tək mahnı linkidir! Tək mahnıları yükləmək üçün sol tərəfdəki '${tabName}' bölməsindən istifadə edin.` 
            : (currentLanguage === "РУС" ? `Это ссылка на один трек! Используйте раздел '${tabName}'.` : `This is a single track link! Please use the '${tabName}' tab.`), "error");
        } else {
          showInAppToast("Error: " + res.error, "error");
        }
      } else {
        playlistPartCache[cacheKey] = res;
        displayTracks(res.playlist_name, res.tracks, res);
      }
    }).catch(err => {
      isPlaylistLoading = false;
      currentLoadingPartNum = null;
      if (btn) {
        btn.removeAttribute("disabled");
        btn.innerHTML = `<span id="lbl-fetch-btn">${translations[currentLanguage].lbl_fetch_btn}</span>`;
      }
      showInAppToast("Error: " + err, "error");
    });
  } else {
    isPlaylistLoading = false;
    currentLoadingPartNum = null;
  }
}

const TRACKS_PER_PAGE = 50;
let currentTrackPage = 0;
let trackStatusMap = {}; // globalIdx -> 'pending' | 'downloading' | 'downloaded' | 'error' | 'cancelled'
let currentTrackFilter = 'all'; // 'all' | 'downloaded' | 'pending'

function renderPlaylistPartButtons(totalTracks, activeOffset, limit) {
  const banner = document.getElementById("spotify-limit-banner");
  const container = document.getElementById("playlist-part-container");
  const badge = document.getElementById("spotify-total-badge");
  const countInfo = document.getElementById("spotify-parts-count-info");
  if (!banner || !container) return;

  if (!totalTracks || totalTracks <= 100) {
    banner.classList.add("hidden");
    return;
  }

  currentPlaylistTotal = totalTracks;
  banner.classList.remove("hidden");
  if (badge) {
    const trackWord = currentLanguage === "AZ" ? "mahnı" : (currentLanguage === "EN" ? "tracks" : "треков");
    badge.textContent = `${totalTracks} ${trackWord}`;
  }

  container.innerHTML = "";
  const totalParts = Math.ceil(totalTracks / limit);
  const currentPartIndex = Math.floor(activeOffset / limit) + 1;

  if (countInfo) {
    countInfo.textContent = currentLanguage === "AZ"
      ? `Hissə: ${currentPartIndex} / ${totalParts}`
      : (currentLanguage === "EN" ? `Part: ${currentPartIndex} / ${totalParts}` : `Часть: ${currentPartIndex} / ${totalParts}`);
  }

  for (let p = 0; p < totalParts; p++) {
    const partOffset = p * limit;
    const startNum = partOffset + 1;
    const endNum = Math.min(partOffset + limit, totalTracks);
    const isActive = (partOffset === activeOffset);

    const btn = document.createElement("button");
    btn.className = isActive
      ? "flex items-center justify-between px-3 py-2 rounded-xl text-[12px] font-black bg-[#1DB954] text-black shadow-md shadow-[#1DB954]/25 transition-all truncate border border-[#1DB954] cursor-pointer"
      : "flex items-center justify-between px-3 py-2 rounded-xl text-[12px] font-semibold bg-[#202020] hover:bg-[#282828] text-[#E5E7EB] hover:text-white border border-[#2F2F2F] hover:border-[#1DB954]/60 transition-all truncate cursor-pointer";
    
    btn.innerHTML = `
      <span class="flex items-center gap-2 truncate">
        <i class="fa-brands fa-spotify text-xs ${isActive ? 'text-black' : 'text-[#1DB954]'} shrink-0"></i>
        <span class="font-extrabold tracking-wide truncate">Part ${p + 1}</span>
      </span>
      <span class="text-[10px] ${isActive ? 'text-black/85 font-black' : 'text-[#9CA3AF] font-medium'} ml-2 shrink-0">(${startNum}-${endNum})</span>
    `;
    btn.title = `Part ${p + 1} (${startNum} - ${endNum})`;
    btn.onclick = () => {
      fetchPlaylist(partOffset, limit);
    };
    container.appendChild(btn);
  }
}

function displayTracks(playlistName, tracks, resInfo = null) {
  fetchedTracks = tracks;
  currentTrackPage = 0;
  trackStatusMap = {};
  currentTrackFilter = 'all';
  initSelectedTracks();
  const results = document.getElementById("playlist-results");
  results.classList.remove("hidden");

  const total = resInfo && resInfo.total_tracks ? resInfo.total_tracks : tracks.length;
  const offset = resInfo && resInfo.offset !== undefined ? resInfo.offset : 0;
  const limit = resInfo && resInfo.limit ? resInfo.limit : 100;

  currentPlaylistName = playlistName || "";
  currentPlaylistTotal = total;
  currentPlaylistOffset = offset;
  currentPlaylistLimit = limit;

  updatePlaylistStatusMsg();

  // Render part pagination if 100+ tracks
  renderPlaylistPartButtons(total, offset, limit);

  updateFilterButtonsUI();
  renderTrackPage();
  renderPlaylistQualityPills();
}

function getFilteredTrackIndices() {
  const query = (document.getElementById("playlist-search")?.value || "").toLowerCase().trim();
  const indices = [];

  for (let i = 0; i < fetchedTracks.length; i++) {
    const track = fetchedTracks[i];
    const status = trackStatusMap[i] || 'pending';

    // Status filter match
    if (currentTrackFilter === 'downloaded' && status !== 'downloaded') continue;
    if (currentTrackFilter === 'pending' && status === 'downloaded') continue;

    // Search query match
    if (query) {
      const title = (track.title || "").toLowerCase();
      const artist = (track.artist || "").toLowerCase();
      if (!title.includes(query) && !artist.includes(query)) continue;
    }

    indices.push(i);
  }

  return indices;
}

function setTrackStatusFilter(filter) {
  currentTrackFilter = filter;
  currentTrackPage = 0;
  updateFilterButtonsUI();
  renderTrackPage();
}

function updateFilterButtonsUI() {
  const activeClass = "px-3 py-1 text-[11px] font-bold rounded-lg bg-[#9D4EDD] text-white transition-all shadow-sm";
  const inactiveClass = "px-3 py-1 text-[11px] font-bold rounded-lg text-[#A0A0A0] hover:text-white transition-all";

  const btnAll = document.getElementById("filter-all");
  const btnDl = document.getElementById("filter-downloaded");
  const btnPend = document.getElementById("filter-pending");

  if (btnAll) btnAll.className = currentTrackFilter === 'all' ? activeClass : inactiveClass;
  if (btnDl) btnDl.className = `${currentTrackFilter === 'downloaded' ? activeClass : inactiveClass} flex items-center gap-1.5`;
  if (btnPend) btnPend.className = `${currentTrackFilter === 'pending' ? activeClass : inactiveClass} flex items-center gap-1.5`;
}

function clearPlaylistSearch() {
  const input = document.getElementById("playlist-search");
  if (input) input.value = "";
  const clearBtn = document.getElementById("btn-clear-pl-search");
  if (clearBtn) clearBtn.classList.add("hidden");
  currentTrackPage = 0;
  renderTrackPage();
}

function filterTracks() {
  const input = document.getElementById("playlist-search");
  const clearBtn = document.getElementById("btn-clear-pl-search");
  if (input && clearBtn) {
    if (input.value.trim().length > 0) {
      clearBtn.classList.remove("hidden");
    } else {
      clearBtn.classList.add("hidden");
    }
  }
  currentTrackPage = 0;
  renderTrackPage();
}

function renderTrackPage() {
  const container = document.getElementById("tracklist-container");
  container.innerHTML = "";

  const filteredIndices = getFilteredTrackIndices();
  const total = filteredIndices.length;
  const totalPages = Math.ceil(total / TRACKS_PER_PAGE) || 1;
  const start = currentTrackPage * TRACKS_PER_PAGE;
  const end = Math.min(start + TRACKS_PER_PAGE, total);
  const pageIndices = filteredIndices.slice(start, end);

  if (total === 0) {
    const empty = document.createElement("div");
    empty.className = "text-xs text-[#A0A0A0] italic text-center py-8";
    empty.textContent = currentLanguage === "AZ" ? "Uyğun mahnı tapılmadı" : (currentLanguage === "EN" ? "No matching tracks found" : "Треки не найдены");
    container.appendChild(empty);
    return;
  }

  pageIndices.forEach((globalIdx) => {
    const track = fetchedTracks[globalIdx];
    const status = trackStatusMap[globalIdx] || 'pending';
    const isSelected = selectedTrackIndices.has(globalIdx);

    const row = document.createElement("div");
    row.id = `track-row-${globalIdx}`;
    const rowActiveClass = status === 'downloading' ? "border-[#9D4EDD] bg-[#251b2e]" : "";
    row.className = `flex items-center justify-between bg-[#242424] rounded-xl border border-[#282828] p-3 text-xs font-semibold hover:border-[#9D4EDD]/60 transition-all ${rowActiveClass}`;

    let statusIconHtml = `<span class="text-[#A0A0A0] text-[10px] w-5 text-center shrink-0">${globalIdx + 1}</span>`;
    if (status === 'downloaded') {
      statusIconHtml = `<span class="w-5 text-center shrink-0 text-[#10B981]" title="Yüklənib"><i class="fa-solid fa-circle-check text-xs"></i></span>`;
    } else if (status === 'downloading') {
      statusIconHtml = `<span class="w-5 text-center shrink-0 text-[#9D4EDD]"><i class="fa-solid fa-spinner fa-spin text-xs"></i></span>`;
    } else if (status === 'error') {
      statusIconHtml = `<span class="w-5 text-center shrink-0 text-[#EF4444]" title="Xəta"><i class="fa-solid fa-circle-xmark text-xs"></i></span>`;
    } else if (status === 'cancelled') {
      statusIconHtml = `<span class="w-5 text-center shrink-0 text-[#A0A0A0]"><i class="fa-solid fa-ban text-xs"></i></span>`;
    }

    const downloadedBadgeText = translations[currentLanguage].badge_downloaded || "Yüklənib";
    const downloadedBadge = status === 'downloaded'
      ? `<span class="text-[9px] font-bold px-2 py-0.5 rounded-full bg-[#10B981]/20 text-[#10B981] border border-[#10B981]/30 shrink-0">${downloadedBadgeText}</span>`
      : '';

    row.innerHTML = `
      <div class="flex items-center gap-3 flex-1 min-w-0">
        <input type="checkbox" id="track-cb-${globalIdx}" ${isSelected ? 'checked' : ''} onchange="onTrackCheckboxChange(${globalIdx}, this.checked)" class="track-checkbox accent-[#9D4EDD] h-4 w-4 rounded border-[#282828] text-[#9D4EDD] focus:ring-[#9D4EDD] cursor-pointer">
        <span id="track-status-${globalIdx}" class="flex items-center justify-center">${statusIconHtml}</span>
        ${track.thumbnail ? `<img src="${track.thumbnail}" class="w-8 h-8 rounded object-cover shrink-0">` : `<div class="w-8 h-8 rounded bg-[#181818] flex items-center justify-center shrink-0 text-[#9D4EDD] text-xs"><i class="fa-solid fa-music"></i></div>`}
        <div class="truncate flex-1 min-w-0">
          <div class="text-white font-bold truncate flex items-center gap-2">
            <span class="truncate">${track.title}</span>
            ${downloadedBadge}
          </div>
          <div class="text-[#A0A0A0] text-[10px] truncate">${track.artist}</div>
        </div>
      </div>
      <span class="text-[#A0A0A0] text-[10px] shrink-0 ml-4">${formatDuration(track.duration)}</span>
    `;
    container.appendChild(row);
  });

  // Pagination
  if (totalPages > 1) {
    const pager = document.createElement("div");
    pager.style.cssText = "display:flex;align-items:center;justify-content:space-between;margin-top:12px;padding-top:12px;border-top:1px solid #282828;";

    const makePagerBtn = (label, icon, pageTarget, disabled) => {
      const btn = document.createElement("button");
      btn.innerHTML = icon + label;
      btn.onclick = () => !disabled && goTrackPage(pageTarget);
      btn.style.cssText = `
        display:inline-flex;align-items:center;gap:5px;
        padding:5px 12px;border-radius:8px;font-size:11px;font-weight:700;
        border:1px solid ${disabled ? '#2a2a2a' : '#3A3A3A'};
        background:${disabled ? '#1a1a1a' : '#282828'};
        color:${disabled ? '#444' : '#fff'};
        cursor:${disabled ? 'not-allowed' : 'pointer'};
        transition:background 0.15s;
      `;
      if (!disabled) {
        btn.onmouseenter = () => { btn.style.background = '#3A3A3A'; };
        btn.onmouseleave = () => { btn.style.background = '#282828'; };
      }
      return btn;
    };

    const prevLabel = translations[currentLanguage].pager_prev || "Əvvəlki";
    const nextLabel = translations[currentLanguage].pager_next || "Növbəti";

    const prevBtn = makePagerBtn(
      prevLabel,
      '<i class="fa-solid fa-chevron-left" style="font-size:9px"></i>',
      currentTrackPage - 1,
      currentTrackPage === 0
    );

    const info = document.createElement("span");
    info.style.cssText = "font-size:11px;color:#A0A0A0;font-weight:700;";
    const rawInfo = translations[currentLanguage].pager_info || "Səhifə {page} / {totalPages} · {start}–{end} / {total} mahnı";
    info.textContent = rawInfo
      .replace("{page}", currentTrackPage + 1)
      .replace("{totalPages}", totalPages)
      .replace("{start}", start + 1)
      .replace("{end}", end)
      .replace("{total}", total);

    const nextBtn = makePagerBtn(
      nextLabel,
      '',
      currentTrackPage + 1,
      currentTrackPage >= totalPages - 1
    );
    nextBtn.innerHTML = `${nextLabel} <i class="fa-solid fa-chevron-right" style="font-size:9px"></i>`;
    if (currentTrackPage < totalPages - 1) {
      nextBtn.onmouseenter = () => { nextBtn.style.background = '#3A3A3A'; };
      nextBtn.onmouseleave = () => { nextBtn.style.background = '#282828'; };
    }
    nextBtn.onclick = () => currentTrackPage < totalPages - 1 && goTrackPage(currentTrackPage + 1);

    pager.appendChild(prevBtn);
    pager.appendChild(info);
    pager.appendChild(nextBtn);
    container.appendChild(pager);
  }

  updateDownloadSelectedButtonText();
}

function onTrackCheckboxChange(globalIdx, isChecked) {
  if (isChecked) {
    selectedTrackIndices.add(globalIdx);
  } else {
    selectedTrackIndices.delete(globalIdx);
  }
  updateDownloadSelectedButtonText();
}

function goTrackPage(page) {
  const filteredIndices = getFilteredTrackIndices();
  const totalPages = Math.ceil(filteredIndices.length / TRACKS_PER_PAGE);
  if (page < 0 || page >= totalPages) return;
  currentTrackPage = page;
  renderTrackPage();
  document.getElementById("tracklist-container").scrollTop = 0;
}

function setPlaylistFormat(type) {
  playlistMediaType = type;
  const activeClass = "px-3 py-1.5 rounded-full text-[11px] font-bold bg-[#9D4EDD] text-white border border-[#9D4EDD] transition-all";
  const inactiveClass = "px-3 py-1.5 rounded-full text-[11px] font-bold text-[#A0A0A0] border border-[#3A3A3A] hover:border-[#9D4EDD] hover:text-white transition-all";
  document.getElementById("pf-audio").className = type === "audio" ? activeClass : inactiveClass;
  document.getElementById("pf-video").className = type === "video" ? activeClass : inactiveClass;
  renderPlaylistQualityPills();
}

function renderPlaylistQualityPills() {
  const qualities = playlistQualityConfig[playlistMediaType];
  playlistQuality = qualities[qualities.length - 1]; // default: highest
  const container = document.getElementById("playlist-quality-pills");
  if (!container) return;
  container.innerHTML = qualities.map(q => `
    <button onclick="selectPlaylistQuality('${q}')" id="pq-${q.replace(/[^a-zA-Z0-9]/g, '_')}"
      class="px-3 py-1.5 rounded-full text-[11px] font-bold transition-all border ${q === playlistQuality ? 'bg-[#9D4EDD] text-white border-[#9D4EDD]' : 'text-[#A0A0A0] border-[#3A3A3A] hover:border-[#9D4EDD] hover:text-white'}">
      ${q}
    </button>
  `).join("");
}

function selectPlaylistQuality(val) {
  playlistQuality = val;
  const qualities = playlistQualityConfig[playlistMediaType];
  qualities.forEach(q => {
    const btn = document.getElementById(`pq-${q.replace(/[^a-zA-Z0-9]/g, '_')}`);
    if (btn) btn.className = `px-3 py-1.5 rounded-full text-[11px] font-bold transition-all border ${q === val ? 'bg-[#9D4EDD] text-white border-[#9D4EDD]' : 'text-[#A0A0A0] border-[#3A3A3A] hover:border-[#9D4EDD] hover:text-white'}`;
  });
}

function formatDuration(sec) {
  if (!sec) return "--:--";
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${s < 10 ? "0" + s : s}`;
}

// Global set of selected track indices (works across pages)
let selectedTrackIndices = new Set();

function initSelectedTracks() {
  selectedTrackIndices = new Set();
  const masterCb = document.getElementById("master-cb");
  if (masterCb) masterCb.checked = false;
}

function toggleSelectAllTracks(master) {
  if (master.checked) {
    selectedTrackIndices = new Set(fetchedTracks.map((_, i) => i));
  } else {
    selectedTrackIndices.clear();
  }
  // Sync visible checkboxes
  document.querySelectorAll(".track-checkbox").forEach(cb => {
    cb.checked = master.checked;
  });
  updateDownloadSelectedButtonText();
}

function updateDownloadSelectedButtonText() {
  const count = selectedTrackIndices.size;
  const btn = document.getElementById("btn-download-playlist");
  if (btn) {
    btn.textContent = `${translations[currentLanguage].lbl_download_selected} (${count})`;
  }
  const masterCb = document.getElementById("master-cb");
  if (masterCb) {
    masterCb.checked = fetchedTracks.length > 0 && selectedTrackIndices.size === fetchedTracks.length;
  }
}

function downloadSelectedTracks() {
  // Sync visible checkboxes before reading
  updateDownloadSelectedButtonText();
  const tracksToDownload = [...selectedTrackIndices].sort((a,b) => a-b).map(i => fetchedTracks[i]);

  if (tracksToDownload.length === 0) {
    alert(currentLanguage === "AZ" ? "Heç bir mahnı seçilməyib." : "No tracks selected.");
    return;
  }

  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.check_ffmpeg().then(hasFfmpeg => {
      if (!hasFfmpeg) {
        installFfmpeg();
        return;
      }

      const ext = playlistMediaType === "audio" ? "MP3" : "MP4";
      const quality = playlistQuality;
      const isAudio = playlistMediaType === "audio";

      const btn = document.getElementById("btn-download-playlist");
      btn.setAttribute("disabled", "true");
      btn.textContent = currentLanguage === "AZ" ? "Yüklənir..." : "Downloading...";

      // Show cancel button and playlist progress panel
      const cancelBtn = document.getElementById("btn-cancel-playlist");
      if (cancelBtn) cancelBtn.classList.remove("hidden");
      const progPanel = document.getElementById("playlist-progress-panel");
      if (progPanel) progPanel.classList.remove("hidden");

      window.pywebview.api.download_selected_tracks(tracksToDownload, isAudio, isAudio ? "audio" : "video", quality, ext);
    });
  }
}

function cancelPlaylistDownload() {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.cancel_download();
  }
}

window.onPlaylistTrackStart = (trackIdx) => {
  trackStatusMap[trackIdx] = 'downloading';
  const statusEl = document.getElementById(`track-status-${trackIdx}`);
  const rowEl = document.getElementById(`track-row-${trackIdx}`);
  if (statusEl) {
    statusEl.innerHTML = `<span class="w-5 text-center shrink-0 text-[#9D4EDD]"><i class="fa-solid fa-spinner fa-spin text-xs"></i></span>`;
  }
  if (rowEl) {
    rowEl.classList.add("border-[#9D4EDD]", "bg-[#251b2e]");
  }
};

window.updatePlaylistDownloadProgress = (overallPct, currentIdx, totalTracks, trackTitle, trackPct, dlMb, totMb, speedStr) => {
  const pctEl = document.getElementById("pl-prog-overall-pct");
  const barFill = document.getElementById("pl-prog-bar-fill");
  const titleEl = document.getElementById("pl-prog-track-title");
  const countEl = document.getElementById("pl-prog-count-info");
  const speedEl = document.getElementById("pl-prog-speed-info");

  if (pctEl) pctEl.textContent = `${overallPct}%`;
  if (barFill) barFill.style.width = `${overallPct}%`;
  if (titleEl) titleEl.textContent = `(${currentIdx + 1}/${totalTracks}) ${trackTitle}`;
  if (countEl) {
    const unit = translations[currentLanguage].songs_unit || "mahnı";
    if (totMb > 0) {
      countEl.textContent = `${currentIdx + 1} / ${totalTracks} ${unit} (${dlMb} / ${totMb} MB)`;
    } else {
      countEl.textContent = `${currentIdx + 1} / ${totalTracks} ${unit}`;
    }
  }
  if (speedEl) {
    const spdLbl = translations[currentLanguage].ffmpeg_stat_speed || "Sürət";
    speedEl.textContent = `${spdLbl}: ${speedStr}`;
  }
  
  // Also update single downloader progress if visible
  const detailStr = `(${currentIdx + 1}/${totalTracks}) ${trackTitle}`;
  window.updateDownloadProgress(overallPct, 'downloading', detailStr);
};

window.onPlaylistTrackFinished = (trackIdx, status, trackTitle) => {
  if (status === "success") {
    trackStatusMap[trackIdx] = 'downloaded';
  } else if (status === "error") {
    trackStatusMap[trackIdx] = 'error';
  } else if (status === "cancelled") {
    trackStatusMap[trackIdx] = 'cancelled';
  }
  renderTrackPage();
};

window.updatePlaylistStatus = (text) => {
  document.getElementById("playlist-status-msg").textContent = text;
};

window.resetPlaylistDownloadState = () => {
  const btn = document.getElementById("btn-download-playlist");
  if (btn) {
    btn.removeAttribute("disabled");
  }
  const cancelBtn = document.getElementById("btn-cancel-playlist");
  if (cancelBtn) cancelBtn.classList.add("hidden");
  const progPanel = document.getElementById("playlist-progress-panel");
  if (progPanel) {
    setTimeout(() => {
      progPanel.classList.add("hidden");
    }, 2500);
  }
  updateDownloadSelectedButtonText();
  const singleProg = document.getElementById("progress-box");
  if (singleProg) {
    setTimeout(() => {
      singleProg.classList.add("hidden");
    }, 2500);
  }
};

// Spotify credentials setup
function openSpotifyDeveloperSite() {
  const targetUrl = "https://developer.spotify.com/dashboard";
  if (window.pywebview && window.pywebview.api && window.pywebview.api.open_external_url) {
    window.pywebview.api.open_external_url(targetUrl);
  } else {
    window.open(targetUrl, "_blank");
  }
}

function pasteSpotifyKey() {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.paste_from_clipboard().then(text => {
      if (text) {
        document.getElementById("spotify-api-key").value = text.trim();
      }
    });
  } else if (navigator.clipboard) {
    navigator.clipboard.readText().then(text => {
      if (text) {
        document.getElementById("spotify-api-key").value = text.trim();
      }
    });
  }
}

window.showSpotifyAuthModal = () => {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.get_spotify_config().then(config => {
      const keyInput = document.getElementById("spotify-api-key");
      const secretInput = document.getElementById("spotify-client-secret");
      if (keyInput) {
        keyInput.value = config.client_id || config.api_key || "";
      }
      if (secretInput) {
        secretInput.value = config.client_secret || "";
      }
    });
  }
  document.getElementById("spotify-modal").classList.remove("hidden");
};

function closeSpotifyModal() {
  document.getElementById("spotify-modal").classList.add("hidden");
}

function showInAppToast(message, type = "success") {
  const toast = document.getElementById("app-toast");
  const textEl = document.getElementById("app-toast-text");
  const iconEl = document.getElementById("app-toast-icon");
  if (!toast || !textEl) return;

  textEl.textContent = message;
  if (type === "success") {
    iconEl.className = "w-8 h-8 rounded-lg bg-[#10B981]/20 flex items-center justify-center text-[#10B981] text-sm shrink-0";
    iconEl.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
    toast.className = "fixed top-6 right-6 z-50 bg-[#181818]/95 backdrop-blur-md border border-[#10B981]/40 px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 transition-all duration-300 transform translate-y-0 opacity-100";
  } else {
    iconEl.className = "w-8 h-8 rounded-lg bg-[#EF4444]/20 flex items-center justify-center text-[#EF4444] text-sm shrink-0";
    iconEl.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i>';
    toast.className = "fixed top-6 right-6 z-50 bg-[#181818]/95 backdrop-blur-md border border-[#EF4444]/40 px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 transition-all duration-300 transform translate-y-0 opacity-100";
  }

  setTimeout(() => {
    toast.className = "fixed top-6 right-6 z-50 bg-[#181818]/95 backdrop-blur-md border border-[#2e2e2e] px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 transition-all duration-300 transform -translate-y-8 opacity-0 pointer-events-none";
  }, 3500);
}

function saveSpotifyConfig() {
  const keyInput = document.getElementById("spotify-api-key");
  const secretInput = document.getElementById("spotify-client-secret");
  const apiKey = keyInput ? keyInput.value.trim() : "";
  const clientSecret = secretInput ? secretInput.value.trim() : "";

  if (!apiKey) {
    showInAppToast(currentLanguage === "AZ" ? "Zəhmət olmasa API açarını və ya Client ID daxil edin." : "Please enter the API key or Client ID.", "error");
    return;
  }

  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.save_spotify_config(apiKey, clientSecret).then(res => {
      if (res.success) {
        closeSpotifyModal();
        showInAppToast(currentLanguage === "AZ" ? "Spotify açarları saxlanıldı! Pleylist yüklənir..." : "Spotify credentials saved! Fetching playlist...", "success");
        fetchPlaylist(0, 100);
      } else {
        showInAppToast("Error: " + res.error, "error");
      }
    });
  }
}

let isPremiumActive = false;

// GoPro (Premium) modal
function openGoProModal() {
  const purchaseBtn = document.getElementById("btn-gopro-purchase");
  if (purchaseBtn) {
    const t = translations[currentLanguage];
    purchaseBtn.textContent = isPremiumActive ? t.status_premium_btn_done : (t.btn_gopro_purchase || "Aktiv Et!");
  }
  document.getElementById("gopro-modal").classList.remove("hidden");
}

function closeGoProModal() {
  document.getElementById("gopro-modal").classList.add("hidden");
}

function activatePremium(event) {
  const container = document.body;
  isPremiumActive = true;
  const t = translations[currentLanguage];

  // Update button texts to reflect activated state using translation dictionary
  const purchaseBtn = document.getElementById("btn-gopro-purchase");
  if (purchaseBtn) {
    purchaseBtn.textContent = t.status_premium_btn_done;
  }
  const sidebarBtn = document.getElementById("btn-gopro-sidebar");
  if (sidebarBtn) {
    sidebarBtn.textContent = t.status_premium_active;
  }

  // Confetti from left-bottom and right-bottom corners
  const colors = ["#9D4EDD", "#FFD166", "#FF007F", "#06B6D4", "#C77DFF", "#50FA7B"];
  const screenHeight = window.innerHeight;
  const screenWidth = window.innerWidth;
  const confettiCount = 50; // 25 from each side

  for (let i = 0; i < confettiCount; i++) {
    const confetti = document.createElement("div");
    confetti.className = "confetti";

    const sizeW = Math.floor(Math.random() * 8) + 6;
    const sizeH = Math.floor(Math.random() * 12) + 8;
    confetti.style.width = `${sizeW}px`;
    confetti.style.height = `${sizeH}px`;

    // Pick color
    const color = colors[Math.floor(Math.random() * colors.length)];
    confetti.style.backgroundColor = color;

    // Choose side: 0 = Left-Bottom, 1 = Right-Bottom
    const side = i % 2;
    if (side === 0) {
      confetti.style.left = "0px";
      confetti.style.top = `${screenHeight}px`;
      const targetX = (Math.random() * 0.4 + 0.1) * screenWidth; // lands in left-mid area
      confetti.style.setProperty("--target-x", `${targetX}px`);
    } else {
      confetti.style.left = `${screenWidth}px`;
      confetti.style.top = `${screenHeight}px`;
      const targetX = -((Math.random() * 0.4 + 0.1) * screenWidth); // lands in right-mid area
      confetti.style.setProperty("--target-x", `${targetX}px`);
    }

    const targetY = -(Math.random() * 0.6 + 0.3) * screenHeight; // fly up to 30%-90% height
    confetti.style.setProperty("--target-y", `${targetY}px`);

    // Rotations & timings
    const rotateStart = Math.random() * 360;
    const rotateEnd = rotateStart + (Math.random() * 720 + 360) * (side === 0 ? 1 : -1);
    confetti.style.setProperty("--rotate-start", `${rotateStart}deg`);
    confetti.style.setProperty("--rotate-end", `${rotateEnd}deg`);

    confetti.style.animationDuration = `${(Math.random() * 1.2) + 1.2}s`;
    confetti.style.animationDelay = `${Math.random() * 0.2}s`;

    confetti.addEventListener("animationend", () => confetti.remove());
    container.appendChild(confetti);
  }

  // Close the premium modal with longer delay so user sees "Aktiv Edildi" text change
  setTimeout(() => {
    closeGoProModal();
  }, 1000);
}

let updateUrl = "";
let updateExeUrl = "";
let isUpdatingNow = false;

window.showUpdateNotification = (version, url, exeUrl = "") => {
  updateUrl = url;
  updateExeUrl = exeUrl;
  
  const t = translations[currentLanguage];
  const titleEl = document.getElementById("update-toast-title");
  const descEl = document.getElementById("update-toast-desc");
  const closeBtn = document.getElementById("btn-update-close");
  const dlBtn = document.getElementById("btn-update-download");
  
  if (titleEl) titleEl.textContent = t.update_title || "Yeni yenilənmə var! 🚀";
  if (descEl) descEl.textContent = (t.update_desc || "Yeni versiya ({version}) artıq hazırdır. Yenilikləri və təkmilləşdirmələri əldə etmək üçün yükləyin.").replace("{version}", version);
  if (closeBtn) closeBtn.textContent = t.btn_update_close || "Bağla";
  if (dlBtn) {
    dlBtn.textContent = t.btn_update_download || "İndi Yüklə";
    dlBtn.removeAttribute("disabled");
  }
  
  const toast = document.getElementById("update-toast");
  if (toast) {
    toast.classList.remove("pointer-events-none", "translate-y-12", "opacity-0");
    toast.classList.add("translate-y-0", "opacity-100");
  }
};

function closeUpdateToast() {
  if (isUpdatingNow) return;
  const toast = document.getElementById("update-toast");
  if (toast) {
    toast.classList.add("pointer-events-none", "translate-y-12", "opacity-0");
    toast.classList.remove("translate-y-0", "opacity-100");
  }
}

function downloadUpdate() {
  if (isUpdatingNow) return;

  const dlBtn = document.getElementById("btn-update-download");
  const descEl = document.getElementById("update-toast-desc");

  if (window.pywebview && window.pywebview.api && window.pywebview.api.download_and_install_update) {
    isUpdatingNow = true;
    if (dlBtn) {
      dlBtn.setAttribute("disabled", "true");
      dlBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Yüklənir...';
    }
    if (descEl) {
      descEl.textContent = "Yenilənmə faylı birbaşa yüklənir və tətbiq quraşdırılır...";
    }
    window.pywebview.api.download_and_install_update(updateExeUrl);
  } else if (updateUrl && window.pywebview && window.pywebview.api && window.pywebview.api.open_external_url) {
    window.pywebview.api.open_external_url(updateUrl);
    closeUpdateToast();
  }
}

window.updateUpdaterProgress = (pct, message) => {
  const descEl = document.getElementById("update-toast-desc");
  const dlBtn = document.getElementById("btn-update-download");
  if (descEl && message) {
    descEl.textContent = message;
  }
  if (dlBtn) {
    dlBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1"></i> ${pct}%`;
  }
};

window.onUpdaterError = (errMsg) => {
  isUpdatingNow = false;
  const dlBtn = document.getElementById("btn-update-download");
  const descEl = document.getElementById("update-toast-desc");
  if (dlBtn) {
    dlBtn.removeAttribute("disabled");
    dlBtn.textContent = translations[currentLanguage].btn_update_download || "İndi Yüklə";
  }
  if (descEl) {
    descEl.textContent = "Yenilənmə xətası: " + errMsg;
  }
  showInAppToast("Yenilənmə xətası: " + errMsg, "error");
};

// ── Spotify-Style Search & Single URL Downloader Engine ──
let searchPlatform = "youtube"; // 'youtube' or 'spotify'
let searchDebounceTimer = null;
let activeSearchQuery = "";
let searchCache = {};
let currentSearchResults = [];
let persistentSelectedSongs = []; // Persistent across searches
let isSearching = false;

function setSearchPlatform(platform) {
  searchPlatform = (platform === "spotify") ? "spotify" : "youtube";
  const urlInput = document.getElementById("url-input");
  if (urlInput) {
    urlInput.placeholder = currentLanguage === "AZ"
      ? "YouTube və ya Spotify linki yapışdırın..."
      : (currentLanguage === "РУС" ? "Вставьте ссылку на YouTube или Spotify..." : "Paste YouTube or Spotify link here...");
  }

  // If user already typed something, re-trigger search for newly active platform
  if (urlInput && urlInput.value.trim().length >= 2 && !urlInput.value.trim().startsWith("http")) {
    handleUrlInputChange(urlInput.value.trim());
  }
}

function handleUrlInputChange(val) {
  if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
  const q = (val || "").trim();
  if (!q || q.length < 2 || q.startsWith("http://") || q.startsWith("https://")) {
    closeSearchDropdown();
    return;
  }
  searchDebounceTimer = setTimeout(() => {
    triggerLiveSearch(q);
  }, 250);
}

function handleUrlInputFocus(val) {
  const q = (val || "").trim();
  if (q.length >= 2 && !q.startsWith("http://") && !q.startsWith("https://")) {
    triggerLiveSearch(q);
  }
}

function closeSearchDropdown() {
  const dd = document.getElementById("search-dropdown");
  if (dd) dd.classList.add("hidden");
  showSearchSpinner(false);
}

function showSearchSpinner(show) {
  const spinner = document.getElementById("search-spinner");
  if (spinner) {
    if (show) spinner.classList.remove("hidden");
    else spinner.classList.add("hidden");
  }
}

function triggerLiveSearch(query) {
  const q = (query || "").trim();
  if (!q || q.length < 2) {
    closeSearchDropdown();
    return;
  }

  activeSearchQuery = q;
  const cacheKey = `${searchPlatform}:${q.toLowerCase()}`;

  if (searchCache[cacheKey]) {
    renderSearchDropdownResults(searchCache[cacheKey], q);
    return;
  }

  showSearchSpinner(true);
  isSearching = true;

  if (window.pywebview && window.pywebview.api && window.pywebview.api.search_tracks) {
    window.pywebview.api.search_tracks(q, searchPlatform, 20).then(results => {
      showSearchSpinner(false);
      isSearching = false;
      if (activeSearchQuery === q) {
        searchCache[cacheKey] = results || [];
        renderSearchDropdownResults(results || [], q);
      }
    }).catch(err => {
      showSearchSpinner(false);
      isSearching = false;
      console.error("Live search error:", err);
    });
  } else {
    showSearchSpinner(false);
    isSearching = false;
  }
}

function getSongUniqueKey(song) {
  if (!song) return "";
  return song.id ? `${song.source || searchPlatform}:${song.id}` : `${song.artist} - ${song.title}`;
}

function isSongSelected(song) {
  const key = getSongUniqueKey(song);
  return persistentSelectedSongs.some(s => getSongUniqueKey(s) === key);
}

function renderSearchDropdownResults(results, query) {
  const dropdown = document.getElementById("search-dropdown");
  const list = document.getElementById("search-dropdown-list");
  const title = document.getElementById("search-dropdown-title");
  const countBadge = document.getElementById("search-dropdown-count");
  if (!dropdown || !list) return;

  currentSearchResults = results || [];
  list.innerHTML = "";

  if (title) {
    title.textContent = searchPlatform === "youtube" ? "YouTube Nəticələri" : "Spotify Nəticələri";
  }
  if (countBadge) {
    countBadge.textContent = `${results ? results.length : 0} mahnı`;
  }

  if (!results || results.length === 0) {
    list.innerHTML = `
      <div class="px-4 py-8 text-center text-xs text-[#737373]">
        <i class="fa-regular fa-face-frown text-2xl mb-2 text-[#525252] block"></i>
        <span>"${escapeHtml(query)}" ${currentLanguage === "AZ" ? "üçün heç bir mahnı tapılmadı" : "heç bir mahnı tapılmadı"}</span>
      </div>
    `;
    dropdown.classList.remove("hidden");
    return;
  }

  results.forEach((item, index) => {
    const isSelected = isSongSelected(item);
    const row = document.createElement("div");
    row.id = `dropdown-row-${index}`;
    row.className = `flex items-center justify-between rounded-xl border p-2 text-xs font-semibold transition-all duration-150 cursor-pointer ${
      isSelected
        ? "bg-[#2b1736] border-[#9D4EDD] shadow-sm shadow-[#9D4EDD]/20"
        : "bg-[#1c1c1c] hover:bg-[#252525] border-[#262626] hover:border-[#383838]"
    }`;

    // Clicking track row toggles selection instead of populating input
    row.onclick = (e) => {
      if (e.target.closest(`#btn-toggle-dd-${index}`)) return;
      toggleDropdownTrack(index, e);
    };

    const defaultThumb = (searchPlatform === "youtube" || item.source === "youtube")
      ? "<div class='w-10 h-10 rounded-lg bg-[#141414] flex items-center justify-center text-[#FF0000] shrink-0 border border-white/5'><i class='fa-brands fa-youtube text-base'></i></div>"
      : "<div class='w-10 h-10 rounded-lg bg-[#141414] flex items-center justify-center text-[#1DB954] shrink-0 border border-white/5'><i class='fa-brands fa-spotify text-base'></i></div>";

    const thumbHtml = item.thumbnail
      ? `<img src="${item.thumbnail}" class="w-10 h-10 rounded-lg object-cover bg-[#121212] shrink-0 border border-white/5 shadow-sm" onerror="this.onerror=null;this.parentElement.innerHTML='${defaultThumb.replace(/'/g, "\\'")}'" />`
      : defaultThumb;

    const subtitle = `Şarkı • ${escapeHtml(item.artist || "Artist")}${item.duration_str ? ` • ${item.duration_str}` : ""}`;

    row.innerHTML = `
      <div class="flex items-center gap-2.5 flex-1 min-w-0 mr-2">
        ${thumbHtml}
        <div class="truncate flex-1 min-w-0">
          <div class="text-white font-bold truncate ${isSelected ? 'text-[#C77DFF]' : 'hover:text-[#9D4EDD]'} transition-colors">
            ${escapeHtml(item.title || "Unknown Title")}
          </div>
          <div class="text-[#A0A0A0] text-[11px] truncate mt-0.5">
            ${subtitle}
          </div>
        </div>
      </div>

      <!-- Spotify-Style (+) / (✓) Action Button -->
      <div class="flex items-center gap-2 shrink-0">
        <button type="button" onclick="toggleDropdownTrack(${index}, event)" id="btn-toggle-dd-${index}"
          class="w-7 h-7 rounded-full transition-all flex items-center justify-center text-xs font-bold cursor-pointer ${
            isSelected
              ? "bg-[#1DB954] text-black border border-[#1DB954] shadow-md shadow-[#1DB954]/30"
              : "bg-transparent text-[#A0A0A0] hover:text-white border border-[#444444] hover:border-white"
          }"
          title="${isSelected ? "Seçildi" : "Əlavə et"}">
          <i class="fa-solid ${isSelected ? 'fa-check text-xs' : 'fa-plus text-[10px]'}"></i>
        </button>
      </div>
    `;

    list.appendChild(row);
  });

  updateSelectedIndicator();
  dropdown.classList.remove("hidden");
}

function selectTrackToInput(track) {
  const urlInput = document.getElementById("url-input");
  if (!urlInput || !track) return;

  const targetUrl = track.url || (track.id ? (track.source === "youtube" ? `https://www.youtube.com/watch?v=${track.id}` : `https://open.spotify.com/track/${track.id}`) : `ytsearch1:${track.artist} - ${track.title}`);
  urlInput.value = targetUrl;

  closeSearchDropdown();
  urlInput.focus();
  showInAppToast(`${track.title} seçildi ✓`, "success");
}

function toggleDropdownTrack(index, event) {
  if (event) event.stopPropagation();
  const track = currentSearchResults[index];
  if (!track) return;

  const key = getSongUniqueKey(track);
  const existingIdx = persistentSelectedSongs.findIndex(s => getSongUniqueKey(s) === key);

  if (existingIdx >= 0) {
    persistentSelectedSongs.splice(existingIdx, 1);
  } else {
    persistentSelectedSongs.push(track);
  }

  const btn = document.getElementById(`btn-toggle-dd-${index}`);
  const row = document.getElementById(`dropdown-row-${index}`);
  const isSelected = isSongSelected(track);

  if (btn) {
    btn.className = `w-7 h-7 rounded-full transition-all flex items-center justify-center text-xs font-bold cursor-pointer ${
      isSelected
        ? "bg-[#1DB954] text-black border border-[#1DB954] shadow-md shadow-[#1DB954]/30"
        : "bg-transparent text-[#A0A0A0] hover:text-white border border-[#444444] hover:border-white"
    }`;
    btn.innerHTML = `<i class="fa-solid ${isSelected ? 'fa-check text-xs' : 'fa-plus text-[10px]'}"></i>`;
  }
  if (row) {
    row.className = `flex items-center justify-between rounded-xl border p-2 text-xs font-semibold transition-all duration-150 cursor-pointer ${
      isSelected
        ? "bg-[#2b1736] border-[#9D4EDD] shadow-sm shadow-[#9D4EDD]/20"
        : "bg-[#1c1c1c] hover:bg-[#252525] border-[#262626] hover:border-[#383838]"
    }`;
  }

  updateSelectedIndicator();
  updateSingleDownloadButton();
}

function updateSelectedIndicator() {
  const indicator = document.getElementById("search-selected-indicator");
  const numSpan = document.getElementById("search-selected-num");
  const urlInput = document.getElementById("url-input");
  const count = persistentSelectedSongs.length;

  if (indicator && numSpan) {
    if (count > 0) {
      numSpan.textContent = count;
      indicator.classList.remove("hidden");
    } else {
      indicator.classList.add("hidden");
    }
  }
  
  if (urlInput) {
    if (count > 0) {
      urlInput.value = currentLanguage === "AZ" ? `Seçilmiş Mahnılar (${count})` : `Selected Tracks (${count})`;
      // The platform icon is already managed by setSearchPlatform(), no need to force YouTube here.
    } else if (urlInput.value.startsWith("Seçilmiş Mahnılar") || urlInput.value.startsWith("Selected Tracks")) {
      urlInput.value = "";
    }
  }
}

function updateSingleDownloadButton() {
  const btn = document.getElementById("btn-download");
  const lbl = document.getElementById("lbl-download-btn");
  if (!btn || !lbl) return;

  const count = persistentSelectedSongs.length;
  if (count > 0) {
    const t = translations[currentLanguage] || translations["AZ"];
    const baseWord = t.lbl_download_btn || "Yüklə";
    const songUnit = t.songs_unit || (currentLanguage === "РУС" ? "треков" : (currentLanguage === "EN" ? "tracks" : "mahnı"));
    lbl.textContent = `${baseWord} (${count} ${songUnit})`;
  } else {
    const t = translations[currentLanguage] || translations["AZ"];
    lbl.textContent = t.lbl_download_btn || "Yüklə";
  }
}

function downloadSelectedSearchResults() {
  if (!persistentSelectedSongs || persistentSelectedSongs.length === 0) {
    const msg = currentLanguage === "AZ" ? "Əvvəlcə ən azı 1 mahnı seçin!" : 
               (currentLanguage === "РУС" ? "Сначала выберите хотя бы 1 трек!" : "Select at least 1 track first!");
    showInAppToast(msg, "error");
    return;
  }

  const tracksToDownload = persistentSelectedSongs.map(s => ({
    id: s.id,
    title: `${s.artist ? s.artist + " - " : ""}${s.title}`,
    url: s.url || (s.id ? (s.source === "youtube" ? `https://www.youtube.com/watch?v=${s.id}` : `https://open.spotify.com/track/${s.id}`) : `ytsearch1:${s.artist} - ${s.title}`),
    thumbnail: s.thumbnail,
    duration: s.duration,
    duration_str: s.duration_str,
    status: 'pending'
  }));

  const ext = selectedExt;
  const isAudio = mediaType === "audio";
  const quality = selectedQuality;

  const executeDownload = () => {
    const btn = document.getElementById("btn-download-searched-batch");
    const btnText = document.getElementById("lbl-download-searched-btn");

    if (btn) btn.setAttribute("disabled", "true");
    if (btnText) {
      const txt = currentLanguage === "AZ" ? "Yüklənir..." : (currentLanguage === "РУС" ? "Загрузка..." : "Downloading...");
      btnText.innerHTML = `<i class="fa-solid fa-spinner fa-spin text-sm"></i> <span>${txt}</span>`;
    }

    const tMsg = currentLanguage === "AZ" ? "mahnının yüklənməsi başladıldı..." : (currentLanguage === "РУС" ? "треков загружаются..." : "tracks downloading...");
    showInAppToast(`${tracksToDownload.length} ${tMsg}`, "info");

    const progBox = document.getElementById("progress-box");
    if (progBox) progBox.classList.remove("hidden");
    
    const prepMsg = currentLanguage === "AZ" ? "Hazırlanır..." : (currentLanguage === "РУС" ? "Подготовка..." : "Preparing...");
    window.updateDownloadProgress(0, 'extracting', prepMsg);

    window.pywebview.api.download_selected_tracks(tracksToDownload, isAudio, isAudio ? "audio" : "video", quality, ext).then(() => {
      if (btn) btn.removeAttribute("disabled");
      persistentSelectedSongs = [];
      updateSelectedIndicator();
      updateSingleDownloadButton();
      closeSearchDropdown();
    }).catch(err => {
      if (btn) btn.removeAttribute("disabled");
      const errMsg = currentLanguage === "AZ" ? "Xəta baş verdi!" : (currentLanguage === "РУС" ? "Произошла ошибка!" : "Error occurred!");
      window.updateDownloadProgress(100, 'error', errMsg);
      console.error("Batch search download error:", err);
    });
  };

  if (isAudio && window.pywebview && window.pywebview.api && window.pywebview.api.check_ffmpeg) {
    window.pywebview.api.check_ffmpeg().then(hasFfmpeg => {
      if (!hasFfmpeg) {
        if (window.pywebview.api.download_ffmpeg) {
          window.pywebview.api.download_ffmpeg();
        }
        return;
      }
      executeDownload();
    });
  } else {
    executeDownload();
  }
}



