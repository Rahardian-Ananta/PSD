# Catatan Perkuliahan PSD - Pertemuan 1

## Pengenalan Rencana Pembelajaran Semester (RPS)

Pada pertemuan perdana, fokus utama adalah pengenalan RPS, penyiapan repositori proyek, pemahaman ekosistem tools pengolahan data spasial, serta pengenalan library visualisasi geospasial interaktif.

---

## Aktivitas & Setup

- **GitHub Repository:** Repositori `PSD` telah dibuat
- **Deployment:** Repositori di-deploy ke GitHub Pages: https://rahardian-ananta.github.io/PSD
- **Library Utama:** Mempelajari **Folium** (library Python berbasis Leaflet.js) untuk visualisasi peta interaktif
- **Dokumen:** Rencana Pembelajaran Semester (RPS) telah diterima

---

## Ekosistem Software & Tools

| Software / Platform | Kategori | Fungsi Utama |
| :--- | :--- | :--- |
| **Python & Folium** | Scripting & Web Maps | Pemrosesan data, API crawling, visualisasi peta interaktif |
| **KNIME Analytics** | Data Science Workflow | Visual programming untuk data pipeline, preprocessing, ETL |
| **QGIS** | Desktop GIS | Analisis spasial, layer manajemen vektor/raster, kartografi |
| **Orange Data Mining** | Data Exploration & ML | Analisis data visual, eksplorasi statistik, pemodelan interaktif |
| **CDSE JupyterHub** | Cloud Remote Sensing | Ekstraksi dan pengolahan data citra satelit Copernicus via OpenEO API |
| **GeoJSON.io** | Web Spatial Utility | Penentuan Bounding Box / poligon area studi dalam format GeoJSON |

---

## Sumber Belajar & Referensi

- **Earth Lab Data Science:** https://earthdatascience.org/courses/
- **CDSE JupyterHub:** https://jupyterhub.dataspace.copernicus.eu/
- **GeoJSON Tool:** https://geojson.io/

---

## Tugas 1: Analisis Polutan Atmosfer

### Deskripsi Tugas
Melakukan crawling data time-series konsentrasi polutan atmosfer untuk area studi, mengeksplorasi data, dan menyajikannya dalam bentuk narasi data (data storytelling) berbasis CRISP-DM.

### Spesifikasi Data
- **Sumber:** Sentinel-5P TROPOMI via CDSE
- **Pilihan Polutan:**
  - NO2 (Nitrogen Dioxide) - emisi transportasi dan industri
  - CO (Carbon Monoxide) - pembakaran tidak sempurna
  - HCHO (Formaldehyde) - prekursor VOC dan polusi industri
  - SO2 / O3 / Aerosol Index (opsional lainnya)
- **Rentang Waktu:** 1 tahun terakhir (hingga akhir Agustus)
- **Format:** File `.csv`

### Metodologi CRISP-DM (Adaptif)

```
[1. Business Understanding]  -->  [2. Data Understanding]
* Definisi Polutan & Masalah      * Crawling Data CSV (CDSE)
* Sumber Emisi & Dampak           * Eksplorasi Statistik (EDA)
* Sudut Pandang Storyteller       * Visualisasi Grafik & Tren

[3. Preprocessing] (Dasar)   -->  [4. Modeling & Evaluasi]
* Filter & Agregasi Temporal      * (Tidak diwajibkan)
```

> **Catatan:** Tugas ini hanya fokus pada Business Understanding, Data Understanding, serta Visualisasi & Eksplorasi Data. Tidak diwajibkan membangun model Machine Learning.

### Struktur Pembahasan (Storytelling)

#### 1. Business & Domain Understanding
- Latar belakang masalah kualitas udara di wilayah studi
- Karakteristik polutan yang dipilih
- Sumber utama pelepasan emisi
- Dampak paparan terhadap kesehatan dan lingkungan

#### 2. Data Understanding & Eksplorasi
- Metadata dataset (sumber, resolusi spasial, koordinat)
- Eksplorasi statistik (rata-rata, median, min, max)
- Identifikasi spike atau anomali polusi
- Visualisasi grafis (time-series, pola musiman, peta interaktif)

### Checklist Pengerjaan
- [ ] Menentukan area studi dan membuat poligon di geojson.io
- [ ] Memilih jenis polutan dari katalog CDSE
- [ ] Mengambil data time-series 1 tahun terakhir
- [ ] Menyimpan hasil ke file `.csv`
- [ ] Melakukan pembersihan data sederhana
- [ ] Membuat grafik visualisasi (Time-Series Plot & Heatmap)
- [ ] Menulis narasi data (storytelling)
- [ ] Memperbarui repositori GitHub

---

## Catatan Tambahan
- Jangan lupa tampilkan data time series untuk kode data understanding di tugas 1
