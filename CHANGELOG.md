# LOG PERUBAHAN — Fix Baris Jabon (2026-10-03)

## 1. Diagnosis (fakta, bukan tebakan)

Baris Jabon (Rahardian Ananta, `Jabon , Sidoarjo` / `Jabon, Sidoarjo`) di kedua file
sumber hampir datar setelah ekstraksi: `no2_std` peringkat **1/36 terkecil** di kedua
varian, `autocorr` mentok di lag maksimum untuk 3 polutan (linear), 72–74 dari 204 fitur
menyimpang ekstrem (|z|>3). Akibatnya Jabon selalu terisolasi di cluster kecil.

File mentah (`data/downloads/jabon_pollutants_data/`) dinyatakan **SEHAT**:
NO₂ 48/366, CO 44, SO₂ 40, HCHO 95, CH₄ 312 missing; interpolasi linear yang benar atas
48 lubang NO₂ menghasilkan std 1.152e-05 ≈ std mentah 1.191e-05 — sedangkan baris fitur
mengklaim 7.07e-07 (**16× lebih kecil**). Jadi kerusakan terjadi di **langkah ekstraksi
fitur baris tersebut**, bukan di data mentah.

## 2. Validasi pipeline perbaikan

Pipeline acuan = sel 4 + 6 + 14 notebook `04_feature_extraction/4.2_ekstraksi_fitur_tsfel.ipynb`
(IQR → imputasi → 68 fitur TSFEL, fs=1). Re-run atas `jabon_pollutants.csv` **identik
dengan file referensi** `04_feature_extraction/All-Pollutants-Jabon_TSFEL*.csv`
(max rel.diff ~7e-13, 0 sel >1%).

## 3. Yang diubah (file)

| File | Perubahan |
| :--- | :--- |
| `data/ekstraksi_fitur_linear.csv` | Baris Rahardian Ananta (id 16): 187/204 fitur diganti baris referensi fill=`time`. id/nama/daerah tetap. Asumsi terdokumentasi: file `linear` = imputasi linear `time` |
| `data/ekstraksi_fitur_polynomial.csv` | Baris Rahardian Ananta (id 15): 54/204 fitur diganti baris referensi fill=`poly3` (POLY_DEG=3). Asumsi: file `polynomial` = imputasi polynomial derajat 3 |
| Backup | `arsip/ekstraksi_fitur_{linear,polynomial}_SEBELUM_fix_jabon.csv` (byte-asli) |
| Turunan (regenerasi penuh) | `data/processed/clustering_{linear,poly}_204.csv`, `X_*`, `ladder_*`, `clustering_grid_*`, `best_config_*`, `labels_best_*`, `labels_*_kN`, `data/spasial/cluster_map_*`, `05_clustering/peta_clustering_*.html` |
| Teks | `05_clustering/5.6_eksperimen_gabungan_204.md` (tabel pemenang), sel kesimpulan 5.7 |
| Skrip | `05_clustering/run_57.py`: path absolut dari ROOT + perbaikan closure palet peta interaktif (folium render lazy) |

Noise tidak terhindarkan: 23 (linear) + 25 (poly) sel di baris LAIN berubah pada
desimal ke-16 (~1e-16, artefak tulis-ulang float CSV). Dampak analitik = nol.

## 4. Dampak hasil (apa yang BERUBAH)

**Linear — BERUBAH BESAR:**
- Pemenang: dim 204/k=2/sil 0.477 [31;3] → **dim 37/k=2/sil 0.497 [2;32]**.
  Cluster kecil baru = **Labang + Nunukan** (pasangan yang dulu muncul di k=4).
- Jabon, Tanah Merah, Wonoayu kini SEMUA di cluster besar (diff kasar "29 pindah"
  sebagian besar hanya penomoran ulang label 0/1 + regrouping 5 daerah).
- dim 204/k=2 kini singleton **[33;1] = Wonoayu** (tersaring) — Wonoayu menjadi outlier
  tersisa; dim 74/k=2 ikut sembuh: [33;1] → **[4;30]**.

**Polynomial — praktis TETAP:**
- Pemenang tetap dim 204/k=2 ([32;2]); sil berubah hanya di desimal ke-10;
  **partisi label identik**. Baris poly lama memang sudah ≈ referensi poly3 —
  outlier-nya Jabon di poly bersifat **bawaan metode** (poly3 atas 126 missing di file
  gabungan), bukan kesalahan mahasiswa.

**ARI linear-vs-poly:** k=2: 0.757→**0.631**; k=3: 0.446→**0.574**;
k=4: 0.553→**0.396**; k=5: 0.638→**0.273**.

**Peta 5.7:** seluruh peta diregenerasi (pemenang + `_kN` + interaktif k=2..5).
Peta linear kini menampilkan segmentasi Labang–Nunukan vs 32 daerah lain.

## 5. Yang BELUM diperbaiki (terbuka)

- **Tanah Merah** (datar kedua, linear): file mentahnya tidak ada di repo → tidak bisa
  diekstraksi ulang. Uji sensitivitas (buang Tanah Merah, linear dim204, tanpa ubah file):
  k=2 → [32;1] singleton = **Wonoayu** (sil 0.55, tersaring); k=3 → [18;14;1];
  k=4 → [26;1;2;4]; k=5 → [22;5;2;1;3].
- **Wonoayu**: outlier tersisa di linear dim204; file mentahnya juga tidak ada di repo.
- Narasi `05_clustering/5.5_narasi_bab5.md` masih merujuk eksperimen generik lama
  (dim 37/k=3/sil 0.837) — perlu revisi lanjutan (di luar cakupan fix ini).

## 7. Addendum — alias Wonoayu (peta menampilkan pasangan Jabon)

Temuan susulan: cluster poly berisi 2 anggota {Jabon, Sidoarjo-Wonoayu}, tetapi peta hanya
menampilkan Jabon sendirian — label `Sidoarjo, Wonoayu` tidak tersambung ke entri daftar
`Wonoayu` (kunci `sidoarjo wonoayu` vs `wonoayu`). Terverifikasi tempat yang sama
(daftar: kabupaten tafsir Sidoarjo, boundary `Wonoayu.geojson` status OK), sehingga
ditambahkan **alias manual terdokumentasi** `sidoarjo wonoayu → wonoayu` di `run_57.py`
(+ cermin di notebook 5.7). Setelahnya cluster 1 peta poly = {Wonoayu, Jabon} berpasangan.
Alias lain yang tersisa (Bandung-Jogoroto, Bangkalan Kota, Banyuajuh Kamal, Kertosono)
sengaja TIDAK dipaksakan (tidak terverifikasi) dan tetap dilaporkan sebagai NA.

## 8. Migrasi Bab 6 ke Jabon (2.1b + klasifikasi sawah)

2.1b: kode sejak awal sudah berjalan di Jabon (`jabon.geojson` → `s2_jabon.tif`,
bbox W112.70 E112.88); yang diperbaiki hanya teks tersisa "Kamal" (judul, Input/Output,
nama job, `s2_kamal_metadata.json` → `s2_jabon_metadata.json`, kotak unduh) + tabel induk
2.1 + copy `build.bat`. Satu output basi (`Selesai: s2_kamal.tif`) dibiarkan apa adanya —
ia milik eksekusi lama dan refresh saat notebook dijalankan ulang.

`data/digitasi_kamal/klasifikasi_jabon.py` (adaptasi Kamal): K-Means 8 klaster pada 11 fitur
(6 band + NDVI/NDWI/NDBI + 2 tekstur), pelabelan analis dari profil spektral Jabon
(sawah = klaster 0/NDVI 0,36 + klaster 4/NDVI 0,28 hamparan terluas; cek ragam absolut NIR
identik ~0,029), lolos guard NDVI ±0,05. Hasil: peta 4-kelas (sawah 26,0% / veg 44,8% /
terbangun 2,7% / air 26,6%) + 100 sampel (50/25/25) → `data/spasial/jabon_sawah.shp`
(S001..S050/N001..N050, EPSG:32749).

6.1 ditulis ulang penuh untuk Jabon (arsip Kamal:
`arsip/6.1_persiapan_klasifikasi_KAMAL.ipynb`): tabel inventaris data, definisi 4→2 kelas,
dokumentasi 7 fitur (6 band + NDVI diagnostik), RF 300 pohon (test 20: F1 1,0 sirkular;
CV5 mean 0,99; importance B12>B11>B08), peta `jabon_classified.tif` (fraksi sawah 0,547 vs
acuan 26,0% — over-prediksi ~29 poin karena tambak tak disampel), 13 gambar di
`data/images/eksperimenjabon/`, kotak unduh 7 berkas.

## 6. Cara revert

```powershell
Copy-Item arsip/ekstraksi_fitur_linear_SEBELUM_fix_jabon.csv data/ekstraksi_fitur_linear.csv -Force
Copy-Item arsip/ekstraksi_fitur_polynomial_SEBELUM_fix_jabon.csv data/ekstraksi_fitur_polynomial.csv -Force
python 05_clustering/run_56ab.py
python 05_clustering/run_57.py
```
Lalu eksekusi ulang notebook 5.6a/5.6b/5.7 dan build ulang buku.
Skrip perbaikan: `fix_jabon.py` di root repo (idempoten).
