## 6. Validasi akhir dan serah-terima Tahap 06

Validasi memastikan evaluasi ini independen, lengkap, dan dapat dipakai untuk laporan akhir tanpa perbaikan diam-diam.

### Checklist

1. Gerbang Tahap 04 lulus dan `holdout_tested_in_stage_04 = false`.
2. Model dan file `best_model.joblib` **tidak berubah** selama tahap ini (sidik jari memori dan hash file identik dengan saat dimuat).
3. Evaluasi memakai tepat 40 file dari 7 NIM test; NIM train tidak pernah muncul.
4. Probabilitas sah, threshold 0,50 konsisten dengan `predict()`, dan tidak ada NaN.
5. ROC-AUC, PR-AUC, accuracy, precision, recall, F1, confusion matrix, dan classification report saling konsisten dan berjumlah 40 file.
6. Syarat ROC-AUC ≥ 0,85 dinilai dari angka nyata dan statusnya ikut tersimpan apa adanya.
7. Confidence interval bootstrap (2.000 ulang) dan rincian per NIM tersimpan.
8. Seluruh file keluaran dan kelima gambar tersedia di `artifacts/test_results/`.
9. Tidak ada pelatihan, penalaan threshold, atau pemilihan fitur di tahap ini.
