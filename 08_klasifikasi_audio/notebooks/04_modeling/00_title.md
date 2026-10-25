# 04 — Modeling

Notebook ini menjalankan tahap **Modeling** CRISP-DM untuk klasifikasi biner audio:

- `1 = berisik`
- `0 = non-berisik`

Tujuan tahap ini adalah membandingkan empat model (Logistic Regression, SVM-RBF, Random Forest, Gradient Boosting) dengan validasi silang berbasis NIM, mengunci hold-out NIM sebelum pemilihan model, memilih dan menala hyperparameter lewat `GridSearchCV` berbasis `GroupKFold`, lalu menyimpan pipeline terpilih beserta konfigurasi dan daftar fiturnya.

## Masukan

- `artifacts/features.csv`: 176 baris file final dan 12 fitur dari Tahap 03.
- `artifacts/selected_features.txt`: kandidat fitur eksploratif (hanya referensi; seleksi final dipelajari di dalam `Pipeline`).
- `artifacts/03_data_preparation/validation_summary.json`: gerbang validasi Tahap 03.

## Keluaran utama

- `artifacts/best_model.joblib`: pipeline terpilih (scaler + seleksi fitur + klasifier).
- `artifacts/04_modeling/model_config.json`: konfigurasi, parameter terbaik, dan daftar NIM train/test.
- `artifacts/04_modeling/holdout_split.csv` dan `holdout_file_split.csv`: pembagian hold-out terkunci per NIM dan per file.
- `artifacts/04_modeling/model_comparison.csv`, `cv_fold_scores.csv`, `grid_search_results.csv`.
- `artifacts/04_modeling/`: laporan, validasi, ringkasan, dan gambar.

## Batasan yang dipegang

1. Hold-out 20% NIM dikunci sebelum pemilihan model dan **tidak pernah** dipakai oleh `GridSearchCV` atau perbandingan model; uji hold-out dilakukan di Tahap 05.
2. Split selalu berbasis NIM: satu NIM tidak boleh muncul di dua sisi split maupun antar fold.
3. Scaler, seleksi fitur, dan klasifier berada di dalam satu `Pipeline` sehingga hanya di-fit pada training fold.
4. Tidak ada PCA dan tidak ada training pada file karantina.
5. Semua angka dan grafik berasal dari eksekusi data nyata; klaim ROC-AUC hold-out ≥ 0,85 baru dinilai pada Tahap 05.
6. `raw_audio/` tidak diubah.
