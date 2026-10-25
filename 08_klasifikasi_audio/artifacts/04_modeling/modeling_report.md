# 04 — Modeling: Laporan Aktual

## Ringkasan

Tahap 04 membandingkan empat model pada data latih berbasis NIM, lalu menala kandidat terbaik dengan `GridSearchCV`. Hold-out 20% NIM dikunci lebih dulu dan **belum** disentuh evaluasi.

- Model terpilih: **Logistic Regression** (`LogisticRegression`).
- ROC-AUC CV terbaik: **0.8442** (std 0.0810); baseline prior: **0.5000**.
- Konfigurasi CV: `GroupKFold(n_splits=5)`, grup = NIM, scoring `roc_auc`, `random_state=42`.
- Hold-out: 7 NIM test (40 file) dan 27 NIM train (136 file) dari total 34 NIM / 176 file.
- Fitur terpilih setelah refit: 8 dari 12 fitur, dipelajari di dalam pipeline.
- Pemeriksaan validasi: 29/29 PASS.

## Penguncian hold-out

| split | n_files | n_nim | n_class_0 | n_class_1 |
|---|---|---|---|---|
| train | 136 | 27 | 67 | 69 |
| test | 40 | 7 | 21 | 19 |

NIM test: `24-068`, `24-100`, `24-119`, `24-131`, `24-145`, `24-168`, `24-169`.

NIM ini tidak pernah masuk perbandingan model maupun `GridSearchCV`; uji terhadap NIM tersebut baru dilakukan di Tahap 05.

## Baseline dan perbandingan empat model

Baseline `DummyClassifier(strategy="prior")` memberi ROC-AUC 0.5000 karena dua kelas hampir seimbang. Angka model harus dibaca relatif terhadap baseline ini.

| model | cv_roc_auc_mean | cv_roc_auc_std | train_roc_auc_mean | cv_accuracy_mean | cv_precision_mean | cv_recall_mean | cv_f1_mean |
|---|---|---|---|---|---|---|---|
| Logistic Regression | 0.8349 | 0.0795 | 0.8875 | 0.7204 | 0.7633 | 0.7026 | 0.7096 |
| Random Forest | 0.7811 | 0.0712 | 1 | 0.6989 | 0.6995 | 0.7641 | 0.7167 |
| SVM-RBF | 0.7738 | 0.0842 | 0.911 | 0.7127 | 0.7667 | 0.6892 | 0.6978 |
| Gradient Boosting | 0.7569 | 0.0899 | 1 | 0.6859 | 0.6931 | 0.7508 | 0.7084 |
| Baseline (prior) | 0.5 | 0 | 0.5 | 0.4777 | 0.3931 | 0.8 | 0.5268 |

Selisih ROC-AUC antar fold tersimpan di `cv_fold_audit.csv` dan `cv_fold_scores.csv`. Semua model berada di atas baseline, tetapi peringkat CV ini belum membuktikan generalisasi ke NIM yang belum pernah dilihat.

## GridSearchCV kandidat terbaik

- Model yang ditala: **Logistic Regression**; kombinasi: **12** dengan 5 fold.
- Parameter terbaik: `clf__C` = `10.0`, `select__k` = `8`.
- Skor CV terbaik: **0.8442**; skor latih: 0.8716.
- Kandidat fitur: `select__k` ikut dicari sehingga jumlah fitur ditentukan di dalam fold latih.

Kandidat terbaik (5 kombinasi teratas):

| rank_test_score | params | mean_test_score | std_test_score | mean_train_score |
|---|---|---|---|---|
| 1 | {'clf__C': 10.0, 'select__k': 8} | 0.844245 | 0.0810337 | 0.871605 |
| 2 | {'clf__C': 1.0, 'select__k': 12} | 0.834938 | 0.0794608 | 0.887479 |
| 3 | {'clf__C': 0.1, 'select__k': 12} | 0.827464 | 0.050196 | 0.856319 |
| 4 | {'clf__C': 1.0, 'select__k': 8} | 0.820797 | 0.0622585 | 0.846709 |
| 5 | {'clf__C': 10.0, 'select__k': 12} | 0.819663 | 0.0786385 | 0.900944 |

Audit per fold:

| fold | n_nim_fit | n_nim_validate | overlap_nim | n_file_validate | n_class_0_validate | n_class_1_validate |
|---|---|---|---|---|---|---|
| 0 | 21 | 6 | 0 | 29 | 14 | 15 |
| 1 | 21 | 6 | 0 | 29 | 16 | 13 |
| 2 | 22 | 5 | 0 | 26 | 13 | 13 |
| 3 | 22 | 5 | 0 | 26 | 11 | 15 |
| 4 | 22 | 5 | 0 | 26 | 13 | 13 |

## Artefak model

- `artifacts/best_model.joblib`: pipeline `scaler -> select -> clf` hasil refit pada seluruh NIM train.
- `artifacts/04_modeling/model_config.json`: model, parameter, skor, versi paket, dan daftar NIM train/test.
- `artifacts/04_modeling/feature_list.txt`: daftar 12 fitur beserta catatan jumlah fitur terpilih.
- `artifacts/04_modeling/holdout_split.csv` dan `holdout_file_split.csv`: pembagian terkunci.
- `artifacts/04_modeling/model_comparison.csv`, `grid_search_results.csv`, `cv_fold_scores.csv`, `cv_fold_audit.csv`.
- `artifacts/04_modeling/validation_report.md` dan `validation_summary.json`.
- Gambar: `holdout_composition.png`, `cv_model_comparison.png`, `grid_search_scores.png`.

## Validasi akhir

Semua pemeriksaan lulus: **29/29**.

| pemeriksaan | status |
|---|---|
| gate03_pass | PASS |
| features_176 | PASS |
| fitur_12_bersih | PASS |
| kelas_88_88 | PASS |
| holdout_nim_test_sebesar_20persen | PASS |
| holdout_disjoint | PASS |
| holdout_menutup_34_nim | PASS |
| holdout_file_176 | PASS |
| holdout_kelas_terlapor | PASS |
| cv_groups_disjoint | PASS |
| cv_hanya_nim_train | PASS |
| data_latih_tanpa_holdout | PASS |
| empat_model_dibandingkan | PASS |
| baseline_roc_auc_050 | PASS |
| grid_search_selesai | PASS |
| pipeline_tiga_langkah | PASS |
| seleksi_fitur_dalam_pipeline | PASS |
| tanpa_pca | PASS |
| joblib_dimuat | PASS |
| prediksi_valid | PASS |
| prediksi_deterministik | PASS |
| konfigurasi_lengkap | PASS |
| konfigurasi_konsisten | PASS |
| daftar_fitur_12 | PASS |
| fitur_terpilih_valid | PASS |
| random_state_tercatat | PASS |
| cv_tercatat | PASS |
| holdout_nims_tercatat | PASS |
| figures_tersimpan | PASS |

## Batasan

- Hold-out **belum** dievaluasi; skor 0.8442 adalah CV pada 27 NIM train, bukan angka kelayakan.
- Kelayakan ROC-AUC ≥ 0,85 hanya dinilai pada Tahap 05 terhadap 7 NIM test.
- Kandidat terbaik memperoleh keuntungan tuning, sementara tiga model lain memakai parameter bawaan; perbandingan adil akhir ada di hasil hold-out.
- Seleksi fitur (`SelectKBest` berbasis ANOVA) bergantung pada fold; daftar fitur terpilih pada pipeline dapat berbeda dari kandidat eksploratif Tahap 03.
- Probabilitas keluaran (terutama `SVC(probability=True)`) adalah skor model, bukan probabilitas terkalibrasi.
- Tidak ada PCA, tidak ada data karantina yang dipakai, dan `raw_audio/` tidak diubah.

## Kesimpulan dan keputusan untuk Tahap 05

1. Muat `artifacts/best_model.joblib` dan `artifacts/04_modeling/model_config.json`; jangan melatih ulang model.
2. Pakai **hanya** NIM test: `24-068`, `24-100`, `24-119`, `24-131`, `24-145`, `24-168`, `24-169`; NIM train tidak boleh muncul di metrik hold-out.
3. Ekstraksi fitur pada file uji harus identik dengan Tahap 03 (kontrak `preprocessing_contract.json`).
4. Laporkan ROC-AUC, PR-AUC, precision, recall, F1, accuracy, confusion matrix, dan classification report, lengkap dengan jumlah NIM test.
5. Bandingkan hasil dengan baseline 0,50 dan syarat kelayakan ROC-AUC ≥ 0,85; bila di bawah syarat, laporkan apa adanya.

**Modeling selesai dan tervalidasi. Hold-out belum diuji.**
