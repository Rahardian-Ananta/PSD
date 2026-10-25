# Laporan Validasi Tahap 04

Status: **PASS**

## Angka aktual

- Model terpilih: Logistic Regression (LogisticRegression)
- ROC-AUC CV terbaik: 0.8442 (baseline 0.50)
- Kombinasi hyperparameter: 12
- Fitur terpilih setelah refit: 8 dari 12
- NIM train/test: 27 / 7
- File train/test: 136 / 40
- Fold GroupKFold: 5 (grup = NIM, overlap 0)
- Pemeriksaan lulus: 29/29

## Catatan

- Hold-out NIM **belum** dipakai untuk evaluasi pada tahap ini.
- Uji hold-out, kurva ROC/PR, confusion matrix, dan classification report dikerjakan di Tahap 05.
- Scaler dan seleksi fitur berada di dalam pipeline sehingga tidak ada kebocoran preprocessing.
- Tidak ada PCA.
