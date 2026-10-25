## 5. GridSearchCV pada kandidat terbaik

Kandidat terbaik dari Section 4 ditala dengan `GridSearchCV`:

- `scoring = roc_auc`, `cv = GroupKFold(n_splits=5)`, `groups = NIM` — konfigurasi yang sama dengan perbandingan.
- `select__k ∈ {4, 8, 12}` ikut dicari, sehingga **jumlah fitur diputuskan di dalam fold latih**, bukan dari hasil Tahap 03.
- Grid hyperparameter per model:

| Model | Grid |
|---|---|
| Logistic Regression | `C ∈ {0.01, 0.1, 1, 10}` |
| SVM-RBF | `C ∈ {0.1, 1, 10}`, `gamma ∈ {scale, 0.1, 0.01}` |
| Random Forest | `n_estimators ∈ {300, 600}`, `max_depth ∈ {None, 6, 12}`, `min_samples_leaf ∈ {1, 2}` |
| Gradient Boosting | `n_estimators ∈ {100, 200}`, `learning_rate ∈ {0.05, 0.1}`, `max_depth ∈ {2, 3}` |

Catatan pembacaan: kandidat terbaik memperoleh keuntungan tuning sementara tiga model lain dinilai dengan parameter bawaan. Perbandingan adil terakhir adalah hasil hold-out Tahap 05, bukan skor CV Section 4. Seluruh hasil kombinasi disimpan di `grid_search_results.csv`.
