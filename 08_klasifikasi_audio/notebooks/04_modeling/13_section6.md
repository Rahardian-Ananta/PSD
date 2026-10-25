## 6. Simpan artefak model

Pipeline hasil `refit` pada seluruh data latih disimpan sebagai:

1. `artifacts/best_model.joblib` — pipeline utuh: `scaler -> select -> clf`, siap dimuat Tahap 05/06 tanpa langkah tambahan.
2. `artifacts/04_modeling/model_config.json` — nama model, parameter terbaik, skor CV, `random_state`, jumlah fold, daftar NIM train/test, 12 kolom fitur, serta fitur yang terpilih oleh `SelectKBest` setelah refit.
3. `artifacts/04_modeling/feature_list.txt` — daftar fitur dalam format ringkas untuk dibaca manusia.

Konfigurasi juga memuat versi paket yang dipakai pelatihan agar hasil dapat direproduksi. Model ini **belum** diuji pada NIM hold-out; itu urusan Tahap 05.
