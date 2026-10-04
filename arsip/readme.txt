================================================================================
DOKUMENTASI PROYEK SAINS DATA (PSD)
Analisis Polutan Atmosfer Kecamatan Jabon Berdasarkan Citra Satelit Sentinel-5P
================================================================================

Repository : https://github.com/Rahardian-Ananta/PSD
Website    : https://rahardian-ananta.github.io/PSD/
Mata Kuliah: Proyek Sains Data (IF2231) - Teknik Informatika, Universitas Trunojoyo Madura

--------------------------------------------------------------------------------
1. TENTANG REPOSITORI INI
--------------------------------------------------------------------------------
Repositori ini merupakan dokumen hidup (Living Document) berbasis Jupyter Book yang
mencatat seluruh siklus analisis data kualitas udara di Kecamatan Jabon, Kabupaten
Sidoarjo. Pemantauan memanfaatkan data satelit Sentinel-5P TROPOMI (Copernicus Data
Space Ecosystem) untuk mengamati 6 polutan utama:
- NO2 (Nitrogen Dioksida)
- CO (Karbon Monoksida)
- HCHO (Formaldehida)
- SO2 (Sulfur Dioksida)
- O3 (Ozon Permukaan)
- CH4 (Metana)

Periode observasi mencakup 366 hari deret waktu (31 Agustus 2025 - 31 Agustus 2026).

--------------------------------------------------------------------------------
2. STRUKTUR METODOLOGI (CRISP-DM)
--------------------------------------------------------------------------------
- BAB 1: Business Understanding
  Latar belakang geospasial Jabon (perbatasan industri Sidoarjo-Pasuruan & luapan lumpur),
  perumusan masalah ketiadaan stasiun pemantau darat, serta tujuan proyek.

- BAB 2: Data Understanding
  Akuisisi data satelit via openEO (jabon.geojson), Exploratory Data Analysis (EDA),
  integrasi cloud database PostgreSQL Aiven, alur analisis KNIME Analytics Platform,
  serta identifikasi missing value dan outlier.

- BAB 3: Data Preprocessing
  Pembersihan format waktu, penanganan outlier (metode IQR), teknik imputasi nilai
  hilang (Interpolasi Linear Time-based), serta validasi integritas dataset bersih.

- BAB 4: Feature Extraction
  Ekstraksi fitur time-series menggunakan pustaka TSFEL menghasilkan 68 fitur
  komprehensif yang mencakup 3 domain:
  * Domain Statistik (mean, variance, skewness, kurtosis, IQR, histogram, dll.)
  * Domain Temporal (autocorrelation, peak analysis, zero crossing rate, dll.)
  * Domain Spektral (FFT mean, spectral distance, fundamental frequency, dll.)

--------------------------------------------------------------------------------
3. STRUKTUR DIREKTORI UTAMA
--------------------------------------------------------------------------------
├── 01_business_understanding.md        -> Bab 1: Pemahaman bisnis & wilayah Jabon
├── 02_data_understanding/              -> Bab 2: Data understanding & skrip analisis
│   ├── 2.7_analisis_no2_aiven_knime.md -> Dokumentasi lengkap Aiven & KNIME
│   └── jabon_pollutants.csv            -> Dataset multi-polutan
├── 03_data_preprocessing/             -> Bab 3: Outlier, imputasi interpolasi linear
├── 04_feature_extraction/              -> Bab 4: Ekstraksi 68 fitur TSFEL
├── private/                            -> [TIDAK DI-UPLOAD] Skrip dengan password Aiven
├── ingest_aiven_jabon.py               -> Skrip publik upload Aiven (pakai os.getenv)
├── run_all_jabon.py                    -> Skrip orkestrasi EDA & ekstraksi fitur
├── jabon.geojson                       -> Koordinat batas poligon Kecamatan Jabon
├── build.bat                           -> Script kompilasi Jupyter Book lokal
├── push.bat                            -> Script 1-klik push git & deploy GitHub Pages
├── _config.yml                         -> Konfigurasi judul, logo, dan repo book
└── _toc.yml                            -> Daftar isi struktur bab Jupyter Book

--------------------------------------------------------------------------------
4. PANDUAN PENGGUNAAN SKRIP BATCH
--------------------------------------------------------------------------------
- Mem-build Website Secara Lokal:
  Cukup klik dua kali (double click) pada file `build.bat`.
  Hasil render HTML dapat dilihat di folder `_build/html/index.html`.

- Mengunggah Pembaruan ke GitHub & Live Web:
  Cukup klik dua kali pada file `push.bat`. Skrip akan otomatis:
  1. Menambahkan semua perubahan ke git (git add .)
  2. Melakukan commit dengan pesan Anda
  3. Mendorong kode sumber ke branch `main`
  4. Mengompilasi Jupyter Book dan men-deploy ke branch `gh-pages`

--------------------------------------------------------------------------------
5. KEAMANAN KREDENSIAL (AIVEN CLOUD)
--------------------------------------------------------------------------------
Seluruh kredensial rahasia (password, connection string URI) disimpan secara aman
pada folder `private/` dan file `.env` yang secara otomatis dikecualikan oleh
`.gitignore` agar tidak pernah terunggah ke repositori publik GitHub.
================================================================================