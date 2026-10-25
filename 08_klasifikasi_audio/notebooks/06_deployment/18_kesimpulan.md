## Kesimpulan dan status akhir proyek

1. **Deployment selesai tanpa training ulang.** `predict_audio(path)` dibangun dari `artifacts/best_model.joblib` (sidik jari file `964a1550c9c06123...`); probabilitas langsung dari `features.csv` identik dengan `test_predictions.csv` Tahap 05 (selisih **1,1e-16**), sehingga model yang dipakai terbukti model yang sama.
2. **Prapemrosesan terbukti identik.** Seluruh **176 file** diperiksa ulang lewat `predict_audio`: selisih fitur relatif maksimum **6,1e-05** (hanya kuantisasi PCM16 ulang, toleransi 1e-03), label cocok **176/176** terhadap pipeline langsung, dan 40 file uji **40/40** cocok dengan Tahap 05 (selisih probabilitas maksimum **2,3e-05**); accuracy 40 file uji **0,7750** sama persis dengan Tahap 05.
3. **Demo nyata berjalan:** `24-068_berisik_1.mp3` → **berisik (p = 0,9114)** benar; `24-068_non-berisik_1.mp3` → **berisik (p = 0,7403)** keliru — konsisten dengan kesalahan FP yang sama pada Tahap 05, dilaporkan apa adanya; file 10 detik teruji pada cabang **pad** dan file 60 detik pada cabang **crop**.
4. **Laporan akhir `artifacts/LAPORAN.md`** memuat data aktual (176 file, 34 NIM, 88:88), 12 fitur + 8 fitur terpilih, model dan konfigurasinya, metrik hold-out nyata **ROC-AUC 0,8296 — DI BAWAH SYARAT AWAL 0,85** dengan CI95 [0,6767; 0,9549], cara pemakaian `predict_audio`, lokasi seluruh artefak, serta limitasi dan etika.
5. **Validasi akhir Tahap 06: 31/31 pemeriksaan PASS** (`artifacts/06_deployment/validation_report.md`); `raw_audio/` tetap 200 file dan `data_final/` tetap 176 WAV.
6. **Status CRISP-DM:** Tahap 01-06 seluruhnya selesai dan tervalidasi. Peningkatan menuju syarat ROC-AUC 0,85 hanya lewat siklus data/model baru — bukan penalaan pada hold-out yang sudah dipakai.

**Deployment selesai dan tervalidasi. Seluruh tahap 01-06 selesai; angka dilaporkan apa adanya.**
