## 1. Pintu masuk: artefak tanpa training ulang

Section ini memuat seluruh artefak yang dibutuhkan deployment dan membuktikan bahwa model yang dipakai adalah model yang sama persis dengan yang diuji pada Tahap 05.

Syarat yang diverifikasi:

1. `validation_summary.json` Tahap 03, 04, dan 05 semuanya berstatus **PASS** dengan seluruh pemeriksaan lulus.
2. `best_model.joblib` ada, pipeline `scaler -> select -> clf`, seluruh parameter cocok dengan `model_config.json`, dan 12 kolom fitur tidak berubah.
3. Kontrak prapemrosesan `preprocessing_contract.json` (16 kHz, 480.000 sampel, frame 400, hop 160, n_fft 512, rolloff 0,85) cocok dengan konstanta notebook ini.
4. **Identitas model**: `predict_proba` langsung pada baris `features.csv` untuk 40 file uji menghasilkan probabilitas identik (selisih < 1e-12) dengan `test_predictions.csv` Tahap 05 — bukti model tidak diganti maupun di-fit ulang.

Sidik jari SHA-256 file model dan sidik jari pickle pipeline dicatat saat dimuat untuk laporan dan validasi akhir.
