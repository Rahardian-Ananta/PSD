## Kesimpulan dan keputusan untuk tahap 06

1. **Evaluasi independen:** model dimuat tanpa di-fit ulang (sidik jari memori dan hash file identik sejak dimuat), evaluasi memakai **tepat 40 file dari 7 NIM test** (`24-068`, `24-100`, `24-119`, `24-131`, `24-145`, `24-168`, `24-169`), threshold 0,50 tidak dituning, dan seluruh pemeriksaan **28/28 PASS**.
2. **Hasil utama:** **ROC-AUC = 0,8296** terhadap baseline 0,50 — **DI BAWAH SYARAT AWAL 0,85**; CI95 bootstrap [0,6767, 0,9549] **memuat 0,85**, sehingga kelayakan pada populasi tidak dapat dipastikan dari 40 file ini. Dilaporkan apa adanya, tidak disesuaikan.
3. **Metrik lain:** PR-AUC 0,8481 (baseline prevalensi 0,475), accuracy 0,7750, precision berisik 0,7500, recall berisik 0,7895, F1 berisik 0,7692; confusion **TN 16, FP 5, FN 4, TP 15** (9 file salah dari 40).
4. **Sebaran kesalahan:** 4 NIM sempurna (`24-100`, `24-119`, `24-131`, `24-169`), `24-068` dan `24-145` benar 4/6, sedangkan `24-168` hanya benar 1/6 — 5 dari 9 kesalahan menumpuk pada satu subjek; hal ini menunjukkan sensitivitas subjek/perangkat dan diperiksa kembali di `errors.csv`.
5. **Artefak resmi:** `artifacts/test_results/` berisi `metrics.json`, `test_predictions.csv`, `classification_report.csv`, `confusion_matrix.csv`, `metrics_by_nim.csv`, `errors.csv`, dan 5 gambar; laporan tahap di `artifacts/05_evaluation/evaluation_report.md`.
6. **Tahap 06:** memakai `best_model.joblib` apa adanya (tanpa training/penalaan), membangun `predict_audio(path)` dengan prapemrosesan identik Tahap 03, mendemokan pada file asli, lalu menulis `artifacts/LAPORAN.md` yang memuat angka-angka di atas **beserta status di bawah syarat 0,85 dan seluruh limitasinya**.

**Evaluation selesai dan tervalidasi. Metrik hold-out dilaporkan apa adanya.**
