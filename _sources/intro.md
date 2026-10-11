% Proyek Sains Data IF2231

# Proyek Sains Data IF2231

## Analitik Citra Satelit untuk Pemantauan Lingkungan: Klasterisasi Polutan Udara dan Klasifikasi Tutupan Lahan

Buku ini menyajikan dua kajian sains data yang dibangun di atas data penginderaan jauh multispektral dan diterapkan pada dua persoalan lingkungan yang berbeda di Jawa Timur. Kedua kajian dikerjakan secara terpisah dengan kerangka kerja **CRISP-DM** (Cross-Industry Standard Process for Data Mining), namun dihimpun dalam satu dokumentasi agar mudah ditelusuri dari pertanyaan bisnis, data, metode, hingga evaluasi dan penyajian hasil.

---

## Dua Kajian dalam Satu Dokumentasi

### Proyek 1 — Klasterisasi Polutan Udara Kawasan Jabon (Bab 1–6)

Kajian ini memantau dinamika kualitas udara di **Kecamatan Jabon, Kabupaten Sidoarjo** dari deret waktu **Sentinel-5P TROPOMI**. Ketiadaan stasiun pemantauan terestrial di wilayah pinggiran industri Sidoarjo–Pasuruan menjadikan citra satelit sebagai sumber data utama. Enam parameter polutan dianalisis — **NO₂, CO, HCHO, SO₂, O₃, dan CH₄** — melalui tahapan pembersihan data, ekstraksi **68 fitur deret waktu (TSFEL)**, reduksi dimensi, hingga klasterisasi dan analisis komparatif antar daerah. Bab 6 melengkapi kajian ini dengan klasifikasi sawah *versus* non-sawah pada citra Sentinel-2A di kawasan Jabon.

### Proyek 2 — Klasifikasi Tutupan Lahan Jawa Timur (Bab 7)

Kajian ini melakukan **klasifikasi tutupan lahan enam kelas** untuk wilayah Provinsi Jawa Timur menggunakan komposit median **Sentinel-2 L2A**. Sembilan fitur spektral (enam band ditambah indeks **NDVI, NDWI, dan NDBI**) dilatihkan pada sepuluh kombinasi model machine learning dengan validasi silang berbasis poligon. Hasil klasifikasi disajikan sebagai peta interaktif (WebGIS) beserta aplikasi web untuk penelusuran metrik, peta, dan berkas keluaran.

---

## Ruang Lingkup dan Kerangka Kerja

Setiap kajian mengikuti alur CRISP-DM yang sama, sehingga pembaca dapat membandingkan penanganan masalah, kualitas data, dan pilihan metode pada dua domain yang berbeda.

| Bab | Tahapan | Proyek 1 — Polutan Jabon | Proyek 2 — Tutupan Lahan Jawa Timur |
| :-- | :-- | :-- | :-- |
| 1 | Business Understanding | Latar belakang lingkungan Jabon dan kebutuhan data satelit | Tujuan klasifikasi tutupan lahan dan definisi enam kelas |
| 2 | Data Understanding | Akuisisi Sentinel-5P, EDA, integrasi Aiven, alur KNIME | Profil raster Sentinel-2, inventaris poligon label, EDA |
| 3 | Data Preprocessing | Deteksi outlier IQR, imputasi interpolasi linear | Validasi poligon (V1–V6), seleksi sampel, split per poligon |
| 4 | Feature Extraction / Modeling | Ekstraksi 68 fitur TSFEL | Pelatihan 10 kombinasi model dan validasi silang |
| 5 | Evaluation / Clustering | Klasterisasi dan analisis komparatif antar daerah | Evaluasi sekali pada data uji, interval kepercayaan bootstrap |
| 6 | Deployment / WebGIS | Klasifikasi sawah Jabon pada Sentinel-2A | Peta klasifikasi interaktif dan aplikasi web |
| 7 | Deployment | — | Inferensi seluruh raster, penyajian, dan aplikasi Streamlit |

---

## Tautan

- Dokumentasi daring: <https://rahardian-ananta.github.io/PSD/>
- Repositori sumber: <https://github.com/Rahardian-Ananta/PSD>
- Aplikasi web interaktif (Proyek 2): <https://rahardian-ananta-psd-klasifikasi-lahan-app-bs77za.streamlit.app/>

*Mata kuliah Proyek Sains Data (IF2231), Program Studi Teknik Informatika, Universitas Trunojoyo Madura.*
