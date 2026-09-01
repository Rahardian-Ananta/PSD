# Catatan Perkuliahan PSD - Pertemuan 2

## Topik: Data, Measurements, and Data Preprocessing

---

## Materi Utama

### 1. Jenis-Jenis Data (Types of Data)

#### Record Data
- **Relational Record:** Tabel relasional dalam database
- **Data Matrix:** Numerical matrix, crosstabs
- **Transaction Data:** Data transaksi
- **Document Data:** Term frequency vector matrix dari teks

#### Graphs and Network
- Transport network
- World Wide Web
- Molecular structure
- Social/Information networks

#### Ordered Data
- Data dengan urutan atau ranking tertentu

#### Spatial, Image, and Multimedia Data
- **Spatial Data:** Peta
- **Image Data:** Citra
- **Video Data:** Video

---

### 2. Karakteristik Penting Data Terstruktur

| Karakteristik | Penjelasan |
| :--- | :--- |
| **Dimensionality** | Jumlah dimensi/atribut data. Curse of dimensionality: masalah pada data berdimensi tinggi |
| **Sparsity** | Hanya keberadaan (presence) yang dihitung, terutama pada data vektor |
| **Resolution** | Pola data tergantung pada skala pengukuran |
| **Distribution** | Penyebaran data: central tendency dan dispersion |

---

### 3. Data Objects & Attributes

- **Data Objects:** Unit terkecil dari dataset, merepresentasikan entitas
- **Attributes:** Properti atau karakteristik dari data objects

#### Jenis Atribut
- **Discrete:** Nilai terbatas atau diskrit (contoh: jumlah kendaraan)
- **Continuous:** Nilai kontinu pada rentang tertentu (contoh: suhu, konsentrasi polutan)

---

### 4. Statistik Deskriptif

#### Central Tendency (Ukuran Pusat)
- **Mean (Rata-rata):** Sum of values / Number of values
- **Median:** Nilai tengah saat data diurutkan
- **Mode:** Nilai yang paling sering muncul

#### Dispersion (Ukuran Sebaran)
- **Range:** Selisih nilai maksimum dan minimum
- **Variance:** Rata-rata kuadrat selisih dari mean
- **Standard Deviation:** Akar kuadrat dari variance
- **Interquartile Range (IQR):** Selisih Q3 - Q1

---

### 5. Similarity and Distance

- **Euclidean Distance:** Jarak lurus antara dua titik
- **Manhattan Distance:** Jarak sumbu-x + sumbu-y
- **Cosine Similarity:** Kemiripan sudut antara dua vektor

---

### 6. Data Quality, Cleaning, and Integration

#### Data Quality Issues
- Missing values (nilai kosong)
- Noise (data tidak relevan/outlier)
- Inconsistent data (ketidaksesuaian format)
- Duplicate data

#### Data Cleaning Techniques
- Handling missing values (imputation, deletion)
- Noise smoothing
- Data normalization
- Integration dari berbagai sumber data

---

### 7. Data Transformation

- **Normalization:** Scaling data ke rentang tertentu
- **Aggregation:** Penggabungan data
- **Generalization:** Penggunaan konsep hierarki
- **Attribute Selection:** Pemilihan atribut relevan

---

### 8. Dimensionality Reduction

- Mengurangi jumlah atribut/dimensi data
- **PCA (Principal Component Analysis):** Teknik reduksi dimensi populer
- **Feature Selection:** Memilih subset fitur terbaik
- **Feature Extraction:** Membuat fitur baru dari yang sudah ada

---

## Tugas 2

### Deskripsi
- Migrasi data time series dari Tugas 1 ke PostgreSQL di Aiven
- Ekstraksi data dari PostgreSQL ke KNIME
- Analisis statistik menggunakan node Statistics di KNIME

### Langkah Pengerjaan
1. Buat project PostgreSQL dan SQL di https://console.aiven.io/
2. Pindahkan data time series ke PostgreSQL Aiven
3. Tarik data ke KNIME
4. Pada node Statistics, tulis rumus setiap fitur beserta contoh perhitungan
5. Jelaskan setiap fitur pada node Statistics dengan contoh cara menghitung dan rumus

### Catatan Penting
- Tugas 2 sama dengan Tugas 1, dilakukan di web statis
- Penjelasan ada di Jupyter Notebook

---

## Referensi
- Aiven Console: https://console.aiven.io/
- KNIME Analytics Platform
- Documentation CDSE: https://documentation.dataspace.copernicus.eu/
