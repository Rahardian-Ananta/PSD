# Dokumentasi Proyek Sains Data (PSD)
## Analisis Polutan Atmosfer Kecamatan Jabon Berdasarkan Citra Satelit Sentinel-5P

[![Jupyter Book](https://img.shields.io/badge/docs-Jupyter%20Book-blue.svg)](https://rahardian-ananta.github.io/PSD/)
[![GitHub Pages](https://img.shields.io/badge/deployment-gh--pages-brightgreen.svg)](https://rahardian-ananta.github.io/PSD/)
[![Database](https://img.shields.io/badge/database-PostgreSQL%20Aiven-orange.svg)](https://aiven.io/)

* **Repositori:** [https://github.com/Rahardian-Ananta/PSD](https://github.com/Rahardian-Ananta/PSD)
* **Website Dokumentasi:** [https://rahardian-ananta.github.io/PSD/](https://rahardian-ananta.github.io/PSD/)
* **Mata Kuliah:** Proyek Sains Data (IF2231) – Teknik Informatika, Universitas Trunojoyo Madura

---

## 📌 1. Gambaran Umum Proyek

Proyek ini merupakan kajian sains data berbasis deret waktu (*time-series*) yang memantau dinamika kualitas udara di **Kecamatan Jabon, Kabupaten Sidoarjo** selama kurun waktu 366 hari observasi (31 Agustus 2025 s.d. 31 Agustus 2026).

Karena keterbatasan stasiun pemantauan terestrial darat di wilayah pinggiran industri Sidoarjo–Pasuruan, proyek ini memanfaatkan data satelit **Sentinel-5P TROPOMI** (*Copernicus Data Space Ecosystem*) menggunakan delineasi area poligon `jabon.geojson` ($\approx 82\text{ km}^2$).

### Parameter Polutan yang Dianalisis:
1. **$\text{NO}_2$** (Nitrogen Dioksida) — Emisi kendaraan bermotor dan cerobong kawasan industri
2. **$\text{CO}$** (Karbon Monoksida) — Pembakaran bahan bakar tidak sempurna
3. **$\text{HCHO}$** (Formaldehida) — Senyawa organik volatil sekunder atmosfer
4. **$\text{SO}_2$** (Sulfur Dioksida) — Emisi bahan bakar fosil tinggi belerang
5. **$\text{O}_3$** (Ozon Permukaan) — Polutan fotokimia troposfer
6. **$\text{CH}_4$** (Metana) — Aktivitas dekomposisi organik dan gas alam

---

## 🔬 2. Metodologi CRISP-DM

| Bab | Tahapan | Fokus & Luaran |
| :--- | :--- | :--- |
| **Bab 1** | **Business Understanding** | Pemahaman masalah lingkungan Jabon, ketiadaan stasiun sensor lokal, dan formulasi kebutuhan data. |
| **Bab 2** | **Data Understanding** | Akuisisi data openEO satelit, Exploratory Data Analysis (EDA), integrasi PostgreSQL Aiven Cloud, dan analisis alur KNIME Analytics Platform. |
| **Bab 3** | **Data Preprocessing** | Deteksi outlier menggunakan metode Interquartile Range (IQR), penanganan missing values berbasis **Interpolasi Linear Waktu**, dan validasi integritas dataset 366 hari. |
| **Bab 4** | **Feature Extraction** | Ekstraksi **68 fitur deret waktu** komprehensif menggunakan pustaka **TSFEL** (domain Statistik, Temporal, dan Spektral) untuk pemodelan prediktif lanjutan. |

---

## 📁 3. Struktur Repositori

```text
PSD/
├── 01_business_understanding.md         # Bab 1: Pemahaman bisnis & latar belakang Jabon
├── 02_data_understanding/               # Bab 2: Eksplorasi data, skrip Aiven & KNIME
│   ├── 2.7_analisis_no2_aiven_knime.md  # Dokumentasi arsitektur Aiven & alur KNIME
│   └── jabon_pollutants.csv             # Data multi-polutan Kecamatan Jabon
├── 03_data_preprocessing/              # Bab 3: Pembersihan, outlier & imputasi
├── 04_feature_extraction/               # Bab 4: Ekstraksi 68 fitur TSFEL
├── private/                             # 🔒 [LOKAL] Skrip berisi kredensial Aiven (di-ignore)
├── jabon.geojson                        # Batas poligon spasial Kecamatan Jabon
├── ingest_aiven_jabon.py                # Skrip publik upload Aiven (menggunakan env vars)
├── run_all_jabon.py                     # Skrip otomasi analisis & ekstraksi fitur
├── build.bat                            # Skrip praktis kompilasi Jupyter Book lokal
├── push.bat                             # Skrip 1-klik commit, push main, & deploy gh-pages
├── _config.yml                          # Konfigurasi Jupyter Book
└── _toc.yml                             # Struktur tabel daftar isi buku
```

---

## ⚡ 4. Panduan Menjalankan Otomasi

### A. Mem-build Buku Lokal
Cukup jalankan (atau klik dua kali):
```cmd
build.bat
```
Hasil file HTML interaktif dapat langsung diakses pada `_build\html\index.html`.

### B. Mendorong ke GitHub & Deploy Live Web (1-Klik)
Cukup jalankan (atau klik dua kali):
```cmd
push.bat
```
Skrip ini akan secara otomatis:
1. Mengumpulkan perubahan file (`git add .`)
2. Melakukan commit (`git commit`)
3. Mendorong ke branch utama (`git push origin main`)
4. Mem-build HTML Jupyter Book terbaru
5. Men-deploy hasil web statis ke branch `gh-pages` sehingga website langsung terbarui.

---

## 🔒 5. Keamanan Kredensial Database

Semua kredensial cloud (URI Aiven, sandi basis data) diatur secara aman:
* Kredensial lokal tersimpan di folder `private/` atau file `.env` yang secara ketat diblokir oleh `.gitignore`.
* Kode yang terpublikasi di branch publik hanya menggunakan placeholder atau pembacaan aman via variabel lingkungan (`os.getenv`).
