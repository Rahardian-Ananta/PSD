# 05 — Evaluation

Notebook ini menjalankan tahap **Evaluation** CRISP-DM untuk klasifikasi biner audio:

- `1 = berisik`
- `0 = non-berisik`

Tujuan tahap ini adalah menguji **satu kali** model yang sudah tersimpan pada **NIM hold-out yang dikunci di Tahap 04**, melaporkan metrik aktual beserta ketidakpastiannya, dan menilai syarat kelayakan awal ROC-AUC ≥ 0,85 apa adanya. Tidak ada pelatihan, penalaan, atau pemilihan model di tahap ini.

## Masukan

- `artifacts/best_model.joblib`: pipeline terpilih dari Tahap 04.
- `artifacts/04_modeling/model_config.json` dan `validation_summary.json`.
- `artifacts/04_modeling/holdout_file_split.csv`: pembagian NIM train/test terkunci.
- `artifacts/features.csv`: 176 baris fitur Tahap 03 (dipakai hanya untuk baris NIM test).

## Keluaran utama

- `artifacts/test_results/test_predictions.csv`: prediksi per file uji.
- `artifacts/test_results/metrics.json`: ROC-AUC, PR-AUC, accuracy, precision, recall, F1, confusion matrix, confidence interval bootstrap, dan status syarat 0,85.
- `artifacts/test_results/classification_report.csv`, `confusion_matrix.csv`, `metrics_by_nim.csv`, `errors.csv`.
- `artifacts/test_results/figures/`: kurva ROC, kurva PR, confusion matrix, distribusi probabilitas, dan distribusi bootstrap ROC-AUC.
- `artifacts/05_evaluation/`: laporan dan validasi tahap.

## Batasan yang dipegang

1. Evaluasi hanya memakai **7 NIM test / 40 file**; NIM train tidak pernah muncul di metrik.
2. Model **tidak** di-fit ulang, tidak ada threshold baru, dan tidak ada pemilihan fitur di tahap ini.
3. Threshold keputusan tetap 0,50 sesuai pipeline, bukan hasil penalaan pada data uji.
4. Syarat ROC-AUC ≥ 0,85 adalah syarat kelayakan awal; hasil di bawahnya dilaporkan apa adanya.
5. Semua angka berasal dari eksekusi nyata; `raw_audio/` tidak diubah.
