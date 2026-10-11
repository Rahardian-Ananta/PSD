# Proyek Sains Data (IF2231)

## Analitik Citra Satelit untuk Pemantauan Lingkungan: Klasterisasi Polutan Udara Kawasan Jabon dan Klasifikasi Tutupan Lahan Jawa Timur

[![Jupyter Book](https://img.shields.io/badge/docs-Jupyter%20Book-blue.svg)](https://rahardian-ananta.github.io/PSD/)
[![GitHub Pages](https://img.shields.io/badge/deployment-gh--pages-brightgreen.svg)](https://rahardian-ananta.github.io/PSD/)
[![Streamlit](https://img.shields.io/badge/app-Streamlit-red.svg)](https://rahardian-ananta-psd-klasifikasi-lahan-app-bs77za.streamlit.app/)
[![Database](https://img.shields.io/badge/database-PostgreSQL%20Aiven-orange.svg)](https://aiven.io/)

- **Repositori:** <https://github.com/Rahardian-Ananta/PSD>
- **Dokumentasi daring:** <https://rahardian-ananta.github.io/PSD/>
- **Aplikasi web interaktif (Proyek 2 — Klasifikasi Tutupan Lahan):** <https://rahardian-ananta-psd-klasifikasi-lahan-app-bs77za.streamlit.app/>
- **Mata kuliah:** Proyek Sains Data (IF2231) — Teknik Informatika, Universitas Trunojoyo Madura

---

## 1. Gambaran Umum

Repositori ini menghimpun dua kajian sains data berbasis penginderaan jauh yang dikerjakan dengan kerangka kerja **CRISP-DM**. Kedua kajian dikerjakan secara terpisah, namun disajikan dalam satu buku dokumentasi agar alur dari pertanyaan bisnis hingga evaluasi dan penyajian hasil dapat ditelusuri secara utuh.

### Proyek 1 — Klasterisasi Polutan Udara Kawasan Jabon (Bab 1–6)

Kajian deret waktu kualitas udara di **Kecamatan Jabon, Kabupaten Sidoarjo**, memanfaatkan citra satelit **Sentinel-5P TROPOMI** sebagai sumber data utama karena terbatasnya stasiun pemantauan terestrial di wilayah pinggiran industri Sidoarjo–Pasuruan. Enam parameter polutan dianalisis:

1. **NO₂** (Nitrogen Dioksida) — emisi kendaraan dan kawasan industri
2. **CO** (Karbon Monoksida) — pembakaran bahan bakar tidak sempurna
3. **HCHO** (Formaldehida) — senyawa organik volatil sekunder
4. **SO₂** (Sulfur Dioksida) — pembakaran bahan bakar fosil berbelerang tinggi
5. **O₃** (Ozon Permukaan) — polutan fotokimia troposfer
6. **CH₄** (Metana) — dekomposisi organik dan gas alam

Cakupan analisis meliputi akuisisi data, pembersihan dan imputasi, ekstraksi **68 fitur deret waktu** dengan pustaka **TSFEL**, reduksi dimensi (PCA), klasterisasi (K-Means), hingga analisis komparatif antar daerah. **Bab 6** melengkapi kajian dengan klasifikasi sawah *versus* non-sawah pada citra **Sentinel-2A** di kawasan Jabon.

### Proyek 2 — Klasifikasi Tutupan Lahan Jawa Timur (Bab 7)

Kajian klasifikasi **tutupan lahan enam kelas** untuk wilayah **Provinsi Jawa Timur** menggunakan komposit median **Sentinel-2 L2A**. Sembilan fitur spektral — enam band (B02, B03, B04, B08, B11, B12) ditambah indeks **NDVI, NDWI, dan NDBI** — digunakan untuk melatih sepuluh kombinasi model (Random Forest, ExtraTrees, LightGBM, SVM, dan Logistic Regression) dengan dua representasi data (per-piksel dan rata-rata poligon). Validasi silang berbasis poligon (*StratifiedGroupKFold*) menjaga netralitas data uji. Hasil akhir disajikan sebagai peta klasifikasi interaktif (WebGIS) dan aplikasi web untuk penelusuran metrik, peta, serta berkas keluaran.

---

## 2. Metodologi CRISP-DM

| Bab | Tahapan | Proyek 1 — Polutan Jabon | Proyek 2 — Tutupan Lahan Jawa Timur |
| :-- | :-- | :-- | :-- |
| 1 | Business Understanding | Latar belakang lingkungan Jabon, ketiadaan sensor lokal, formulasi kebutuhan data | Tujuan klasifikasi, definisi enam kelas tutupan lahan, pertanyaan analisis |
| 2 | Data Understanding | Akuisisi openEO, EDA, integrasi PostgreSQL Aiven, alur KNIME Analytics Platform | Profil raster Sentinel-2, inventaris dan validasi poligon label, EDA |
| 3 | Data Preprocessing | Deteksi outlier IQR, imputasi interpolasi linear waktu, validasi integritas 366 hari | Validasi poligon V1–V6, seleksi sampel per kelas, split per poligon |
| 4 | Feature Extraction / Modeling | Ekstraksi 68 fitur TSFEL (domain statistik, temporal, spektral) | Pelatihan 10 kombinasi model dan validasi silang berbasis poligon |
| 5 | Evaluation / Clustering | Reduksi dimensi, klasterisasi K-Means, analisis komparatif antar daerah | Evaluasi sekali pada data uji, interval kepercayaan bootstrap |
| 6 | Deployment / WebGIS | Klasifikasi sawah *versus* non-sawah pada Sentinel-2A (Jabon) | Peta klasifikasi interaktif (WebGIS) |
| 7 | Deployment | — | Inferensi seluruh raster, penyajian hasil, aplikasi Streamlit |

---

## 3. Struktur Repositori

```text
PSD/
├── 01_business_understanding/       # Bab 1: Pemahaman bisnis dan latar belakang
├── 02_data_understanding/           # Bab 2: Eksplorasi data, skrip Aiven, alur KNIME
├── 03_data_preprocessing/           # Bab 3: Pembersihan, outlier, imputasi
├── 04_feature_extraction/           # Bab 4: Ekstraksi 68 fitur TSFEL
├── 05_clustering/                   # Bab 5: Reduksi dimensi, klasterisasi, peta
├── 06_klasifikasi_sawah/            # Bab 6: Klasifikasi sawah Jabon (Sentinel-2A)
├── 07_klasifikasi_lahan_jatim/      # Bab 7: Klasifikasi tutupan lahan Jawa Timur
│   ├── notebooks/                   #   Notebook bab 7.1–7.6
│   ├── deployment.md                #   Bab 7.7 Deployment
│   ├── app.py                       #   Aplikasi Streamlit
│   ├── data/                        #   Data pendukung (geojson, metadata)
│   └── outputs/                     #   Tabel, figur, model, raster hasil
├── data/                            # Data proyek 1 (Aiven, polutan, spasial)
├── arsip/                           # Berkas arsip dan versi lama
├── private/                         # [LOKAL] Kredensial; diabaikan oleh Git
├── intro.md                         # Halaman muka dokumentasi
├── _config.yml                      # Konfigurasi Jupyter Book
├── _toc.yml                         # Struktur daftar isi
├── build.bat                        # Skrip kompilasi Jupyter Book lokal
└── push.bat                         # Skrip commit, push, dan deploy gh-pages
```

---

## 4. Menjalankan dan Men-deploy

### A. Membangun buku secara lokal

Jalankan (atau klik dua kali):

```cmd
build.bat
```

Hasil HTML interaktif tersedia pada `_build\html\index.html`.

### B. Mendorong ke GitHub dan memperbarui situs daring

Jalankan (atau klik dua kali):

```cmd
push.bat
```

Skrip ini secara otomatis: menambahkan berkas (`git add`), melakukan commit, mendorong ke branch `main`, membangun HTML Jupyter Book terbaru, lalu men-deploy hasilnya ke branch `gh-pages` sehingga situs daring langsung diperbarui.

---

## 5. Aplikasi Web Interaktif (Streamlit)

Aplikasi web Bab 7 menampilkan hasil klasifikasi tutupan lahan secara interaktif: ringkasan metrik kunci, alur data hingga model, peta klasifikasi, luas per kelas, evaluasi model, serta tautan unduh hasil inferensi.

- **Aplikasi:** <https://rahardian-ananta-psd-klasifikasi-lahan-app-bs77za.streamlit.app/>
- **Berkas utama:** `07_klasifikasi_lahan_jatim/app.py`

Berkas model berukuran besar (di atas 100 MB, melebihi batas GitHub) tidak disertakan di repositori dan disajikan melalui tautan rilis terpisah. Konstanta `MODEL_RELEASE_BASE` di `app.py` diisi setelah berkas tersebut diunggah.

---

## 6. Keamanan Kredensial

Seluruh kredensial layanan awan (URI dan sandi basis data Aiven) dikelola secara aman:

- Kredensial lokal disimpan pada folder `private/` atau berkas `.env` yang diblokir oleh `.gitignore`.
- Kode yang dipublikasikan hanya memuat placeholder atau pembacaan aman melalui variabel lingkungan (`os.getenv`).

---

## 7. Catatan dan Keterbatasan

- Analisis proyek 1 mengukur kualitas data deret waktu dan pola kemiripan antar daerah; hasil tidak dimaksudkan sebagai klaim kausal.
- Akurasi klasifikasi proyek 2 mengikuti kualitas label sumber sekunder (dataset Institut Pertanian, BIG Satupeta, Natural Earth) dan bukan referensi resmi per wilayah.
- Sebagian berkas output berukuran besar dikecualikan dari repositori agar tetap berada dalam batas layanan GitHub; berkas tersebut dapat dihasilkan ulang dengan menjalankan ulang notebook terkait.

---

*Program Studi Teknik Informatika, Universitas Trunojoyo Madura.*
