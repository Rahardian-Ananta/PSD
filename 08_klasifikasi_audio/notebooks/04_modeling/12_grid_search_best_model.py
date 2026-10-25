param_grids = {
    "Logistic Regression": {
        "clf__C": [0.01, 0.1, 1.0, 10.0],
    },
    "SVM-RBF": {
        "clf__C": [0.1, 1.0, 10.0],
        "clf__gamma": ["scale", 0.1, 0.01],
    },
    "Random Forest": {
        "clf__n_estimators": [300, 600],
        "clf__max_depth": [None, 6, 12],
        "clf__min_samples_leaf": [1, 2],
    },
    "Gradient Boosting": {
        "clf__n_estimators": [100, 200],
        "clf__learning_rate": [0.05, 0.1],
        "clf__max_depth": [2, 3],
    },
}

k_candidates = [4, 8, 12]
active_param_grid = {"select__k": k_candidates, **param_grids[best_reference_name]}
n_combinations = 1
for values in active_param_grid.values():
    n_combinations *= len(values)

search = GridSearchCV(
    estimator=make_pipeline(reference_models[best_reference_name]),
    param_grid=active_param_grid,
    scoring=SCORING,
    cv=GroupKFold(n_splits=N_SPLITS),
    n_jobs=1,
    refit=True,
    return_train_score=True,
    error_score="raise",
)
search.fit(X_train, y_train, groups=groups_train)

grid_results = pd.DataFrame(search.cv_results_)
grid_results = grid_results[
    [
        "rank_test_score",
        "params",
        "mean_test_score",
        "std_test_score",
        "mean_train_score",
        "std_train_score",
        "mean_fit_time",
    ]
].sort_values("rank_test_score")
grid_results.to_csv(ARTIFACT_DIR / "grid_search_results.csv", index=False)

best_pipeline = search.best_estimator_
assert set(best_pipeline.named_steps) == {"scaler", "select", "clf"}

print(f"Model yang ditala: {best_reference_name}")
print(f"Jumlah kombinasi: {n_combinations} kombinasi x {N_SPLITS} fold")
print(f"ROC-AUC terbaik (CV): {search.best_score_:.4f}")
print(f"Parameter terbaik: {search.best_params_}")

display(grid_results.head(10).round(4))

fig, ax = plt.subplots(figsize=(9.5, 4.4))
ordered = grid_results.sort_values("mean_test_score", ascending=False).reset_index(drop=True)
ax.plot(ordered.index + 1, ordered["mean_test_score"], "o-", color="#457b9d", label="CV uji")
ax.fill_between(
    ordered.index + 1,
    ordered["mean_test_score"] - ordered["std_test_score"],
    ordered["mean_test_score"] + ordered["std_test_score"],
    alpha=0.2,
    color="#457b9d",
)
ax.plot(ordered.index + 1, ordered["mean_train_score"], "--", color="#e76f51", label="CV latih")
ax.axvline(1, color="#adb5bd", linewidth=1.2, linestyle=":")
ax.set_xlabel("Peringkat kombinasi parameter (1 = terbaik)")
ax.set_ylabel("ROC-AUC")
ax.set_title(f"GridSearchCV: {best_reference_name}")
ax.legend()
fig.tight_layout()
fig.savefig(FIGURE_DIR / "grid_search_scores.png")
plt.show()
