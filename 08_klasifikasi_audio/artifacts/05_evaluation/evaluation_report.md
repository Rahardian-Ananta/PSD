# 05 — Evaluation: Laporan Aktual

## Ringkasan

Model dari Tahap 04 diuji **satu kali** pada NIM hold-out yang dikunci; tidak ada pelatihan atau penalaan ulang di tahap ini.

- Model: **Logistic Regression** (`LogisticRegression`), threshold keputusan 0.5.
- Data uji: **40 file** dari **7 NIM test**: `24-068`, `24-100`, `24-119`, `24-131`, `24-145`, `24-168`, `24-169`.
- **ROC-AUC = 0.8296** dengan CI95 bootstrap [0.6767, 0.9549] terhadap baseline 0,50 dan syarat kelayakan 0,85.
- Status syarat kelayakan awal: **DI BAWAH SYARAT AWAL**.
- PR-AUC = 0.8481 (baseline prevalensi 0.4750); accuracy = 0.7750; F1 kelas berisik = 0.7692.
- File salah prediksi: 9 dari 40.
- Pemeriksaan validasi: 28/28 PASS.

## Metrik hold-out

| metrik | nilai | acuan |
|---|---|---|
| ROC-AUC | 0.8296 | baseline 0,5000; syarat 0,85 |
| ROC-AUC CI 95% (bootstrap) | [0.6767, 0.9549] | 2.000 pengambilan ulang |
| PR-AUC | 0.8481 | baseline prevalensi 0.4750 |
| accuracy | 0.7750 | kelas hampir seimbang |
| precision (kelas 1) | 0.7500 | kelas positif = berisik |
| recall (kelas 1) | 0.7895 | kelas positif = berisik |
| F1 (kelas 1) | 0.7692 | precision dan recall |
| accuracy per NIM (rata-rata) | 0.7857 | rentang 0.1667 - 1.0000 |

Confusion matrix (threshold 0.5):

| aktual | pred_non_berisik | pred_berisik |
|---|---|---|
| actual_non_berisik | 16 | 5 |
| actual_berisik | 4 | 15 |

Classification report:

| kelas | precision | recall | f1-score | support |
|---|---|---|---|---|
| non-berisik | 0.8 | 0.7619 | 0.7805 | 21 |
| berisik | 0.75 | 0.7895 | 0.7692 | 19 |
| accuracy | 0.775 | 0.775 | 0.775 | 0.775 |
| macro avg | 0.775 | 0.7757 | 0.7749 | 40 |
| weighted avg | 0.7762 | 0.775 | 0.7751 | 40 |

Keterangan baris: TN=16, FP=5, FN=4, TP=15. Kelas 1 = berisik adalah kelas positif.

## Rincian per NIM test

| nim | n_files | n_class_0 | n_class_1 | n_benar | n_pred_1 | n_salah | accuracy |
|---|---|---|---|---|---|---|---|
| 24-068 | 6 | 3 | 3 | 4 | 5 | 2 | 0.6667 |
| 24-100 | 6 | 3 | 3 | 6 | 3 | 0 | 1 |
| 24-119 | 6 | 3 | 3 | 6 | 3 | 0 | 1 |
| 24-131 | 6 | 3 | 3 | 6 | 3 | 0 | 1 |
| 24-145 | 6 | 3 | 3 | 4 | 3 | 2 | 0.6667 |
| 24-168 | 6 | 3 | 3 | 1 | 2 | 5 | 0.1667 |
| 24-169 | 4 | 3 | 1 | 4 | 1 | 0 | 1 |

- NIM dengan accuracy sempurna: **4 dari 7** (24-100, 24-119, 24-131, 24-169).
- Accuracy per NIM rata-rata 0.7857, terendah **24-168 = 0.1667** (5 kesalahan dari 6 file).
- 5 dari 9 kesalahan berasal dari satu NIM (`24-168`), sehingga hasil sangat dipengaruhi subjek/perangkat tersebut.

## File yang salah prediksi

| file | nim | label_name | pred_label_name | proba_berisik |
|---|---|---|---|---|
| 24-068_non-berisik_1.wav | 24-068 | non-berisik | berisik | 0.735735 |
| 24-068_non-berisik_2.wav | 24-068 | non-berisik | berisik | 0.552531 |
| 24-145_non-berisik_3.wav | 24-145 | non-berisik | berisik | 0.52914 |
| 24-145_berisik_3.wav | 24-145 | berisik | non-berisik | 0.309293 |
| 24-168_non-berisik_1.wav | 24-168 | non-berisik | berisik | 0.884149 |
| 24-168_non-berisik_3.wav | 24-168 | non-berisik | berisik | 0.892399 |
| 24-168_berisik_1.wav | 24-168 | berisik | non-berisik | 0.0333481 |
| 24-168_berisik_2.wav | 24-168 | berisik | non-berisik | 0.218829 |
| 24-168_berisik_3.wav | 24-168 | berisik | non-berisik | 0.345816 |

File tetap dipertahankan; tidak ada yang dibuang karena dianggap sulit.

## Ketidakpastian

- ROC-AUC 0.8296 memiliki CI95 bootstrap [0.6767, 0.9549] dari 2000 pengambilan ulang (random_state=42).
- Dengan 7 NIM dan 40 file, selisih satu dua file sudah menggeser metrik; angka hold-out adalah estimasi, bukan jaminan.
- CI95 **memuat** 0.85, sehingga kelayakan pada populasi tidak dapat dipastikan dari data uji ini saja.

## Gambar

Seluruh gambar berada di `artifacts/test_results/figures/`:

- `roc_curve.png` — ROC-AUC 0.8296 terhadap diagonal 0,50.
- `pr_curve.png` — PR-AUC 0.8481 terhadap baseline prevalensi 0.4750.
- `confusion_matrix.png` — heatmap TN/FP/FN/TP.
- `proba_distribution.png` — sebaran probabilitas berisik per kelas nyata dengan garis threshold 0.5.
- `roc_auc_bootstrap.png` — sebaran ROC-AUC bootstrap beserta CI.

## Validasi akhir

Semua pemeriksaan lulus: **28/28**.

| pemeriksaan | status |
|---|---|
| gate04_pass | PASS |
| konfigurasi_model_lengkap | PASS |
| feature_columns_cocok | PASS |
| model_file_tidak_berubah | PASS |
| model_memori_tidak_diubah | PASS |
| pipeline_struktur | PASS |
| evaluasi_hanya_40_file | PASS |
| evaluasi_hanya_nim_test | PASS |
| n_nim_test_7 | PASS |
| prediksi_tanpa_nan | PASS |
| probabilitas_sah | PASS |
| threshold_konsisten | PASS |
| label_prediksi_sah | PASS |
| roc_auc_sah | PASS |
| pr_auc_sah | PASS |
| accuracy_sah | PASS |
| confusion_40 | PASS |
| classification_report_lengkap | PASS |
| metrics_json_lengkap | PASS |
| status_085_konsisten | PASS |
| baseline_05_tercatat | PASS |
| ci_bootstrap_sah | PASS |
| per_nim_7_lengkap | PASS |
| errors_konsisten | PASS |
| holdout_tidak_dilatih | PASS |
| random_state_tercatat | PASS |
| test_results_lengkap | PASS |
| figures_tersimpan | PASS |

## Batasan

- Hanya 7 NIM dan 40 file uji; angka sedikit, ketidakpastian lebar.
- Label berasal dari protokol pengumpulan, bukan verifikasi audit kebenaran mutlak.
- Threshold 0.5 tidak dituning; menaikkan threshold menaikkan precision dan menurunkan recall.
- Probabilitas output belum terkalibrasi.
- Model terpilih memperoleh keuntungan tuning pada Tahap 04; hold-out ini adalah pengadilan pertama dan terakhir yang independen.
- Kelayakan awal ≠ layak produksi; batasan privasi dan perangkat/ruangan tetap berlaku.

## Kesimpulan dan keputusan untuk Tahap 06

1. Pakai `artifacts/best_model.joblib` dan `artifacts/04_modeling/model_config.json` apa adanya; jangan melatih atau menala ulang.
2. Fungsi `predict_audio(path)` harus meniru prapemrosesan Tahap 03 (mono 16 kHz, crop/pad 480.000 sampel, peak normalization, 12 fitur) lalu memakai pipeline ini.
3. Metrik hold-out yang dilaporkan di `artifacts/test_results/metrics.json` adalah angka resmi tahap ini.
4. `artifacts/LAPORAN.md` pada Tahap 06 memuat data aktual, fitur, model, metrik nyata, lokasi artefak, dan limitasi.

**Evaluation selesai dan tervalidasi. Metrik hold-out dilaporkan apa adanya.**
