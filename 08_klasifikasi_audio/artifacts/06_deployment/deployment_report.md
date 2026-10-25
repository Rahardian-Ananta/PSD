# 06 — Deployment: Laporan Aktual

## Ringkasan

Fungsi **`predict_audio(path)`** dibangun memakai `artifacts/best_model.joblib` **tanpa training ulang**, dengan prapemrosesan identik Tahap 03, dan didemokan pada file asli dataset.

- Model: **Logistic Regression** (pipeline `scaler -> select -> clf`), parameter {'clf__C': 10.0, 'select__k': 8}, sidik jari file `964a1550c9c06123...`.
- Identitas model: selisih probabilitas vs `test_predictions.csv` Tahap 05 **1.110e-16** (toleransi 1e-12) — model tidak diganti, tidak di-fit ulang.
- Identitas prapemrosesan: **176/176 file** diperiksa; selisih fitur relatif maksimum **6.105e-05** (toleransi 0.001), label cocok 176/176.
- Reproduksi Tahap 05: 40/40 label cocok, selisih probabilitas maksimum 2.342e-05 (toleransi 0.005); accuracy 40 file uji 0.7750 = accuracy Tahap 05.
- Demo: 2 file utama (satu per kelas) + 2 cabang durasi (pad 10 detik, crop 60 detik), seluruhnya berjalan nyata.
- Laporan akhir: **`artifacts/LAPORAN.md`** (7326 bytes).
- Pemeriksaan validasi: 31/31 PASS.

## Yang dibangun

Fungsi `predict_audio(path)` (cell `08_predict_audio.py`):

1. `librosa.load(path, sr=16000, mono=True)`;
2. crop/pad tengah ke 480000 sampel;
3. peak normalization `y / max(|y|)`, hasil `float32`;
4. 12 fitur dengan framing 400/160, Hann simetris, rFFT 512;
5. pipeline tersimpan (scaler + seleksi fitur + klasifikasi) -> label pada threshold 0.5 beserta probabilitas kedua kelas.

Fungsi menolak file tidak ada dan sinyal peak nol; seluruh konstanta cocok dengan `preprocessing_contract.json`.

## Demo nyata

| skenario | file | kelas_asli | prediksi | proba_berisik | cocok | duration_action | durasi_asli_detik |
|---|---|---|---|---|---|---|---|
| demo_utama | 24-068_non-berisik_1.mp3 | non-berisik | berisik | 0.740319 | False | none | 30 |
| demo_utama | 24-068_berisik_1.mp3 | berisik | berisik | 0.911437 | True | none | 30 |
| cabang_pad_10_detik | demo_10_detik.wav | non-berisik | non-berisik | 0.0516325 | True | pad | 10 |
| cabang_crop_60_detik | demo_60_detik.wav | non-berisik | berisik | 0.85682 | False | crop | 60 |

- Dua file utama diambil deterministik dari 40 file uji dan dijalankan lewat **file MP3 asli** (`data_mp3/`), bukan salinan hasil.
- Hasil dilaporkan apa adanya: file yang keliru tetap ditulis sebagai keliru.
- Cabang `pad` (10 detik) dan `crop` (60 detik) teruji sesuai kontrak durasi.

## Bukti identitas prapemrosesan

| pemeriksaan | nilai |
|---|---|
| File diperiksa ulang dengan predict_audio | 176 |
| Label cocok vs pipeline langsung | 176 / 176 |
| Selisih fitur relatif maksimum | 6.105e-05 |
| Label cocok vs Tahap 05 (40 file uji) | 40 / 40 |
| Selisih probabilitas vs Tahap 05 | 2.342e-05 |
| Accuracy 40 file uji | 0.7750 |

Sumber perbedaan yang tersisa hanyalah kuantisasi ulang PCM16 ketika file final dinormalisasi kembali (faktor ~3e-5) — jauh di bawah toleransi dan tidak mengubah satu pun label uji.

## Laporan akhir

`artifacts/LAPORAN.md` memuat: data aktual Tahap 02-03, 12 fitur dan 8 fitur terpilih, model dan konfigurasi Tahap 04, metrik hold-out Tahap 05 **apa adanya** (ROC-AUC 0.8296, status DI BAWAH SYARAT AWAL), cara pemakaian `predict_audio`, lokasi seluruh artefak, serta limitasi dan etika.

## Validasi akhir

Semua pemeriksaan lulus: **31/31**.

| pemeriksaan | status |
|---|---|
| gate03_pass | PASS |
| gate04_pass | PASS |
| gate05_pass | PASS |
| pipeline_struktur | PASS |
| parameter_tidak_berubah | PASS |
| fitur_input_12 | PASS |
| fitur_terpilih_8 | PASS |
| kontrak_prapemrosesan_cocok | PASS |
| sidik_jari_model_tercatat | PASS |
| proba_model_identik | PASS |
| predict_audio_terdefinisi | PASS |
| fitur_predict_audio_sah | PASS |
| identitas_fitur_176 | PASS |
| label_konsisten_176 | PASS |
| reproduksi_test_40 | PASS |
| probabilitas_test_konsisten | PASS |
| accuracy_sama_tahap05 | PASS |
| demo_duakelas | PASS |
| demo_empat_skenario | PASS |
| cabang_pad_teruji | PASS |
| cabang_crop_teruji | PASS |
| file_demo_tersimpan | PASS |
| laporan_ada | PASS |
| laporan_memuat_metrik | PASS |
| laporan_memuat_limitasi | PASS |
| laporan_memuat_artefak | PASS |
| test_results_lengkap | PASS |
| artefak_06_lengkap | PASS |
| raw_audio_tetap_200 | PASS |
| data_final_tetap_176 | PASS |
| threshold_konsisten | PASS |

## Batasan

- Probabilitas adalah skor model, bukan keyakinan terkalibrasi; threshold 0.5 tidak dituning.
- ROC-AUC 0.8296 tetap **di bawah syarat awal 0,85**; CI95 [0.6767, 0.9549] memuat 0,85.
- Evaluasi hanya 7 NIM / 40 file; kesalahan menumpuk pada NIM 24-168.
- Fungsi mengasumsikan audio berdurasi mendekati 30 detik; durasi ekstrem dikenali lewat crop/pad tetapi kualitas prediksi menurun bila bahan utama terbuang.
- Rekaman berisi suara orang: gunakan hanya untuk proyek pembelajaran; tanpa pengenalan pembicara.

## Kesimpulan dan arah lanjut

1. Deployment selesai: `predict_audio(path)` terbukti identik prapemrosesannya untuk 176 file dan mereproduksi evaluasi Tahap 05 untuk 40 file uji.
2. `artifacts/LAPORAN.md` berisi seluruh angka aktual, lokasi artefak, dan limitasi untuk konsumen laporan.
3. Bila kelayakan 0,85 ingin dipenuhi, langkah berikutnya adalah siklus data/model baru (data lebih banyak dan lebih beragam), bukan penilaian ulang pada hold-out yang sama.

**Deployment selesai dan tervalidasi. Tanpa training ulang; metrik dilaporkan apa adanya.**
