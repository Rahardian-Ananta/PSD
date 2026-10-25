## 3. Baseline jujur dan pipeline anti-bocor

Sebelum membandingkan model, dua hal ditetapkan:

**Baseline jujur.** `DummyClassifier(strategy="prior")` hanya mengeluarkan probabilitas prior kelas. Dua kelas hampir seimbang, jadi ROC-AUC baseline adalah **0,50**. Semua model di bawah harus dibandingkan dengan angka ini; accuracy saja tidak cukup.

**Pipeline.** Setiap kandidat dibungkus satu `Pipeline`:

1. `StandardScaler` — menyeragamkan skala fitur (logika tetap untuk model berbasis jarak dan koefisien).
2. `SelectKBest(score_func=f_classif, k=...)` — seleksi fitur dipelajari dari data fold latih saja, bukan ditentukan dari seluruh data.
3. klasifier — Logistic Regression, SVM-RBF, Random Forest, atau Gradient Boosting.

Konsekuensinya scaler dan seleksi fitur **tidak pernah** melihat fold uji, tidak ada PCA, dan model akhir yang disimpan adalah pipeline utuh sehingga Tahap 05/06 cukup memuat `best_model.joblib` tanpa langkah tambahan.
