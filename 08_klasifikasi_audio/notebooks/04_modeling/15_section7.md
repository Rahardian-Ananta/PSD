## 7. Validasi akhir dan serah-terima Tahap 05

Validasi memastikan hasil Tahap 04 dapat dipakai Tahap 05 tanpa perbaikan diam-diam.

### Checklist

1. Gerbang Tahap 03 (PASS, 176 baris fitur, 12 fitur bersih) tetap terpenuhi.
2. Hold-out terkunci: 20% NIM, train dan test tidak beririsan, seluruh NIM tercakup, dan komposisi per file/kelas dilaporkan.
3. `GroupKFold` tidak pernah mencampur satu NIM ke dua sisi fold; seluruh baris CV berasal dari NIM train.
4. NIM hold-out tidak pernah masuk `GridSearchCV` maupun data refit.
5. Empat model kandidat dibandingkan dan baseline 0,50 tercatat.
6. Pipeline tersimpan memiliki tepat tiga langkah `scaler`, `select`, `clf`; tidak ada PCA.
7. `best_model.joblib` dapat dimuat ulang, mengeluarkan label {0,1} dan probabilitas berada di [0,1] dengan jumlah baris 1.
8. `model_config.json` dan `feature_list.txt` memuat parameter, fold, scoring, `random_state`, dan daftar fitur.
9. Tahap 05 hanya boleh memakai NIM test yang sudah dikunci; model **belum** diuji pada tahap ini.
