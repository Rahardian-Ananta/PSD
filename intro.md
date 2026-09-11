---
title: "Dokumentasi Proyek Sains Data: Analisis Polutan Atmosfer di Kecamatan Jabon Berdasarkan Citra Satelit Sentinel-5P"
---

# Introduction

## Dokumentasi Proyek Sains Data: Analisis Polutan Atmosfer di Kecamatan Jabon Berdasarkan Citra Satelit Sentinel-5P

> **"From Raw Satellite Data to Actionable Air Quality Insights"**

Selamat datang di dokumentasi interaktif proyek sains data kami. Halaman ini berfungsi sebagai **Living Document** (dokumen hidup) yang mencatat seluruh siklus pengembangan solusi berbasis data untuk mata kuliah **Proyek Sains Data (IF2231)** di Program Studi Teknik Informatika, Universitas Trunojoyo Madura.

Dokumentasi ini disusun menggunakan **Jupyter Book** untuk memastikan transparansi proses, reproduktibilitas kode, dan kemudahan dalam menelusuri alur analisis dari tahap awal perolehan data mentah hingga ekstraksi fitur deret waktu.

---

## Latar Belakang & Wilayah Studi

### Permasalahan Utama di Kecamatan Jabon

Kualitas udara merupakan salah satu penentu kesehatan lingkungan dan masyarakat. **Kecamatan Jabon**, yang terletak di perbatasan selatan Kabupaten Sidoarjo dengan Kabupaten Pasuruan, merupakan wilayah strategis dengan lalu lintas logistik industri yang padat serta kedekatannya dengan kawasan terdampak lingkungan luapan lumpur Lapindo. Namun, stasiun pemantauan terestrial di darat memiliki keterbatasan jumlah dan tidak menjangkau wilayah Kecamatan Jabon secara langsung.

**Bagaimana cara memantau, menganalisis, dan mengekstraksi karakteristik polutan udara di seluruh wilayah Kecamatan Jabon secara komprehensif tanpa bergantung pada stasiun darat?**

### Solusi Penginderaan Jauh Satelit

Kami memanfaatkan data satelit **Sentinel-5P TROPOMI** dari *Copernicus Data Space Ecosystem* menggunakan batas poligon Area of Interest (AOI) `jabon.geojson`. Pendekatan ini memungkinkan:

1. Pemantauan kualitas udara secara spasial di seluruh wilayah Kecamatan Jabon ($\approx 82\text{ km}^2$).
2. Analisis deret waktu harian untuk 6 polutan utama ($\text{NO}_2, \text{CO}, \text{HCHO}, \text{SO}_2, \text{O}_3, \text{CH}_4$) selama periode **31 Agustus 2025 hingga 31 Agustus 2026** (366 hari observasi).
3. Pembersihan, penanganan nilai hilang berbasis **Interpolasi Linear**, serta ekstraksi **68 fitur deret waktu** (*TSFEL*) untuk pemodelan prediktif lanjutan.

---

## Metodologi: CRISP-DM

Sesuai dengan kurikulum mata kuliah, proyek ini mengikuti kerangka kerja standar industri **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*). Struktur Jupyter Book ini dirancang mengikuti tahapan utama:

| Tahapan Bab | Fokus Aktivitas & Luaran |
| :--- | :--- |
| **BAB 1 — Business Understanding** | Definisi masalah kualitas udara di Kecamatan Jabon, tujuan proyek, dan perumusan pertanyaan analisis. |
| **BAB 2 — Data Understanding** | Pengumpulan data satelit Sentinel-5P via openEO (`jabon.geojson`), deskripsi dataset, EDA, analisis skema PostgreSQL Aiven & KNIME, identifikasi 102 missing value, dan analisis pencilan (*outliers*). |
| **BAB 3 — Data Preprocessing** | Pembersihan indeks waktu, strategi penanganan pencilan, imputasi missing value (**3.3.1 Interpolasi Linear**), dan validasi integritas data bersih 366 hari. |
| **BAB 4 — Feature Extraction** | Penyiapan sinyal kontinu, konfigurasi pustaka TSFEL, ekstraksi domain statistik, domain temporal, domain spektral, dan tabulasi matriks 68 fitur. |

---

## Tech Stack & Tools

*   **Bahasa Pemrograman:** Python 3.x
*   **Pengambilan Data:** openEO (*Copernicus Data Space Ecosystem*)
*   **Basis Data Cloud:** PostgreSQL Aiven (SSL Mode, Float 53-bit)
*   **Workflow Analitik Visual:** KNIME Analytics Platform
*   **Library Analisis:** Pandas, NumPy, GeoPandas, SQLAlchemy, TSFEL
*   **Dokumentasi:** Jupyter Book & MyST Markdown
*   **Version Control:** GitHub ([github.com/Rahardian-Ananta/PSD](https://github.com/Rahardian-Ananta/PSD))

---

## Tim Pengembang

| Nama | NIM |
| :--- | :--- |
| **Rahardian Ananta** | 240411100071 |

**Dosen Pengampu:** MULA'AB, S.Si., M.Kom  
*Program Studi Teknik Informatika, Fakultas Teknik, Universitas Trunojoyo Madura*

---

## Navigasi Dokumen

Gunakan menu navigasi di sebelah kiri untuk menelusuri setiap bagian:

1. **BAB 1 — BUSINESS UNDERSTANDING**:
   - 1.1 Latar Belakang / Permasalahan
   - 1.2 Tujuan
   - 1.3 Pertanyaan / Kebutuhan Analisis
2. **BAB 2 — DATA UNDERSTANDING**:
   - 2.1 Data Collection (openEO & Sentinel-5P)
   - 2.2 Deskripsi Dataset (6 Polutan & Unduh Data)
   - 2.3 Exploratory Data Analysis (Struktur DB, Kalkulasi Statistik, Aiven & KNIME)
   - 2.4 Identifikasi Missing Value (Analisis 102 Data Kosong)
   - 2.5 Identifikasi Outlier (Deteksi Batas IQR & Z-Score)
   - 2.6 Kesimpulan Data Understanding
3. **BAB 3 — DATA PREPROCESSING**:
   - 3.1 Pembersihan Data
   - 3.2 Penanganan Outlier
   - 3.3 Imputasi Missing Value (3.3.1 Interpolasi Linear)
   - 3.4 Validasi Data Bersih
4. **BAB 4 — FEATURE EXTRACTION**:
   - 4.1 Persiapan Data untuk Ekstraksi
   - 4.2 Ekstraksi Fitur Menggunakan TSFEL
   - 4.3 Fitur Domain Statistical
   - 4.4 Fitur Domain Temporal
   - 4.5 Fitur Domain Spectral
   - 4.6 Hasil Ekstraksi 68 Fitur

---

```{tableofcontents}
```
