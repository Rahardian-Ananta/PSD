## Kesimpulan dan keputusan untuk tahap 05

1. **Hold-out terkunci:** `GroupShuffleSplit(test_size=0.2, random_state=42)` pada 34 NIM menghasilkan **27 NIM train (136 file, kelas 67 non-berisik : 69 berisik)** dan **7 NIM test (40 file, kelas 21 : 19)**. NIM test: `24-068`, `24-100`, `24-119`, `24-131`, `24-145`, `24-168`, `24-169`. Pembagian disimpan di `holdout_split.csv` dan `holdout_file_split.csv`, dan **belum pernah** dipakai untuk CV atau `GridSearchCV`.
2. **Baseline jujur:** `DummyClassifier(strategy="prior")` memberi ROC-AUC **0,50** pada GroupKFold 5 fold; seluruh kandidat dibaca relatif terhadap angka ini.
3. **Perbandingan empat model (data latih saja, grup = NIM, overlap fold 0):** Logistic Regression **0,8349**, Random Forest **0,7811**, SVM-RBF **0,7738**, Gradient Boosting **0,7569**.
4. **GridSearchCV kandidat terbaik:** pada Logistic Regression dengan 12 kombinasi (`C ∈ {0.01, 0.1, 1, 10}` × `select__k ∈ {4, 8, 12}`), terbaik **`C = 10`, `k = 8`** dengan ROC-AUC CV **0,8442** (std 0,0810).
5. **Model tersimpan:** `artifacts/best_model.joblib` = pipeline `StandardScaler -> SelectKBest -> LogisticRegression` hasil refit pada 136 file train, memakai **8 dari 12 fitur** yang dipilih di dalam pipeline: `mse_energy`, `rms_mean`, `rms_std`, `rms_max`, `rms_min`, `zcr_mean`, `spectral_centroid_mean`, `spectral_rolloff_mean`. Konfigurasi di `model_config.json`, daftar fitur di `feature_list.txt`.
6. **Validasi:** **29/29 pemeriksaan PASS** — gerbang Tahap 03, sisi split beririsan nol, fold CV tanpa NIM ganda, data latih bebas NIM hold-out, pipeline tiga langkah tanpa PCA, joblib dapat dimuat dan prediksi deterministik.
7. **Belum dilakukan:** uji terhadap 7 NIM test, kurva ROC/PR, confusion matrix, classification report, dan penilaian syarat ROC-AUC ≥ 0,85 — semuanya urusan Tahap 05.
8. **Rencana 05:** muat `best_model.joblib` tanpa melatih ulang, ekstraksi fitur identik dengan kontrak Tahap 03, evaluasi **hanya** pada NIM test, bandingkan dengan baseline 0,50 dan syarat kelayakan 0,85, lalu laporkan metrik aktual beserta limitasinya apa adanya.

**Modeling selesai dan tervalidasi. Hold-out belum diuji.**
