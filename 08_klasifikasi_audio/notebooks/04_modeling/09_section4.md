## 4. Perbandingan empat model dengan GroupKFold

Empat kandidat dibandingkan pada **data latih saja** (NIM hold-out tidak disentuh) memakai `GroupKFold(n_splits=5)` dengan `groups = NIM`, sehingga satu NIM selalu berada di satu sisi fold.

Kondisi perbandingan:

1. Semua model memakai pipeline yang sama dan **seluruh 12 fitur** (`k=12`) dengan parameter bawaan yang dirujuk secara eksplisit; penyesuaian hyperparameter dilakukan pada Section 5 untuk kandidat terbaik.
2. Metrik utama `roc_auc`; accuracy, precision, recall, dan F1 dilaporkan pendamping.
3. Skor per fold disimpan (`cv_fold_scores.csv`) agar selisih antar fold terlihat, bukan hanya rata-rata.
4. Baseline ditampilkan pada tabel dan grafik yang sama sebagai garis pembanding 0,50.
5. Perbandingan ini **bukan** klaim kelayakan; kelayakan (ROC-AUC ≥ 0,85) diukur pada hold-out di Tahap 05.
