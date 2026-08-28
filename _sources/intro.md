# Dokumentasi Proyek Sains Data: Analisis Polutan Atmosfer di Kabupaten Sidoarjo Berdasarkan Citra Satelit Sentinel-5P

> **"From Raw Satellite Data to Actionable Air Quality Insights"**

Selamat datang di dokumentasi interaktif proyek sains data kami. Halaman ini berfungsi sebagai **Living Document** (dokumen hidup) yang mencatat seluruh siklus pengembangan solusi berbasis data untuk mata kuliah **Proyek Sains Data (IF2231)** di Program Studi Teknik Informatika, Universitas Trunojoyo Madura.

Dokumentasi ini disusun menggunakan **Jupyter Book** untuk memastikan transparansi proses, reproduktibilitas kode, dan kemudahan dalam menelusuri alur analisis dari tahap awal hingga deployment.

---

## Latar Belakang & Tujuan Bisnis

### Permasalahan Utama

Kualitas udara merupakan salah satu penentu kesehatan masyarakat. Kabupaten Sidoarjo, sebagai wilayah padat aktivitas industri dan lalu lintas, memerlukan pemantauan kualitas udara yang berkelanjutan. Namun, stasiun pemantauan di darat memiliki keterbatasan jumlah dan cakupan spasial. **Bagaimana cara memantau dan menganalisis konsentrasi polutan udara di seluruh wilayah Sidoarjo secara komprehensif?**

### Solusi yang Ditawarkan

Kami memanfaatkan data satelit **Sentinel-5P TROPOMI** dari Copernicus Data Space Ecosystem untuk menganalisis konsentrasi polutan atmosfer di Kabupaten Sidoarjo. Pendekatan ini memungkinkan:

1. Pemantauan kualitas udara secara spasial di seluruh wilayah kabupaten tanpa bergantung pada stasiun darat.
2. Analisis tren polutan NO₂, CO, HCHO, SO₂, O₃, dan CH₄ selama satu tahun terakhir.
3. Identifikasi pola temporal dan spasial emisi polutan untuk mendukung pengambilan keputusan berbasis data.

---

## Metodologi: CRISP-DM

Sesuai dengan kurikulum mata kuliah, proyek ini mengikuti standar industri **CRISP-DM** (Cross-Industry Standard Process for Data Mining). Struktur Jupyter Book ini dirancang mengikuti tahapan utama tersebut:

| Tahapan | Fokus Aktivitas |
| :--- | :--- |
| **1. Business Understanding** | Definisi masalah kualitas udara Sidoarjo, tujuan analisis, dan identifikasi polutan yang relevan. |
| **2. Data Understanding** | Pengumpulan data satelit Sentinel-5P, EDA, dan identifikasi kualitas data. |
| **3. Data Preparation** | Cleaning, normalisasi, dan transformasi data satelit menjadi siap analisis. |
| **4. Analisis & Visualisasi** | Analisis tren temporal dan spasial polutan serta visualisasi hasilnya. |
| **5. Deployment** | Penyajian hasil analisis dalam bentuk dokumentasi interaktif berbasis Jupyter Book. |

---

## Tech Stack & Tools

*   **Bahasa Pemrograman:** Python 3.x
*   **Pengambilan Data:** OpenEO (Copernicus Data Space Ecosystem)
*   **Library Analisis:** Pandas, NumPy, GeoPandas
*   **Visualisasi:** Matplotlib, Seaborn, Folium
*   **Dokumentasi:** Jupyter Book
*   **Version Control:** GitHub ([github.com/Rahardian-Ananta/PSD](https://github.com/Rahardian-Ananta/PSD))

---

## Tim Pengembang

| Nama | NIM |
| :--- | :--- |
| **Rahardian Ananta** | 240411100071 |

**Dosen Pengampu:** MULA'AB, S.Si., M.Kom

---

## Navigasi Dokumen

Gunakan menu di sebelah kiri untuk menelusuri setiap bagian:

1. **Data Understanding** -- Pengunduhan data satelit Sentinel-5P, pemrosesan, dan visualisasi tren keenam polutan (NO₂, CO, HCHO, SO₂, O₃, CH₄).

---

## Catatan Perkembangan (Project Progress)

Dokumentasi ini bersifat **progresif**. Setiap perubahan metode, temuan baru, atau perbaikan akan dicatat di sini.

*   **Status Saat Ini:** In Progress
*   **Terakhir Diperbarui:** 24 Agustus 2026

> **Tips:** Jika Anda ingin mereproduksi hasil analisis ini, silakan clone repositori GitHub kami dan jalankan perintah `pip install -r requirements.txt` sebelum membuka file `.ipynb`.

---
*Dokumen ini disusun sebagai pemenuhan Capaian Pembelajaran Mata Kuliah (CPMK) IF2231 Proyek Sains Data.*

```{tableofcontents}
```
