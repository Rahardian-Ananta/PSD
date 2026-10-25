reference_models = {
    "Logistic Regression": LogisticRegression(
        C=1.0,
        solver="lbfgs",
        max_iter=5000,
        random_state=RANDOM_STATE,
    ),
    "SVM-RBF": SVC(
        C=1.0,
        kernel="rbf",
        gamma="scale",
        probability=True,
        random_state=RANDOM_STATE,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=500,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=RANDOM_STATE,
    ),
}

assert sorted(reference_models) == sorted(MODEL_CANDIDATES), "Daftar model tidak sesuai config."

comparison_rows = []
fold_rows = []

for model_name, estimator in reference_models.items():
    pipe = make_pipeline(estimator, k=len(FEATURE_COLUMNS))
    cv_scores = cross_validate(
        pipe,
        X_train,
        y_train,
        groups=groups_train,
        cv=cv_splitter,
        scoring=SCORING_SET,
        n_jobs=1,
        return_train_score=True,
    )
    comparison_rows.append(
        {
            "model": model_name,
            "cv_roc_auc_mean": float(np.mean(cv_scores["test_roc_auc"])),
            "cv_roc_auc_std": float(np.std(cv_scores["test_roc_auc"])),
            "train_roc_auc_mean": float(np.mean(cv_scores["train_roc_auc"])),
            "cv_accuracy_mean": float(np.mean(cv_scores["test_accuracy"])),
            "cv_precision_mean": float(np.mean(cv_scores["test_precision"])),
            "cv_recall_mean": float(np.mean(cv_scores["test_recall"])),
            "cv_f1_mean": float(np.mean(cv_scores["test_f1"])),
        }
    )
    for fold_index, score in enumerate(cv_scores["test_roc_auc"]):
        fold_rows.append(
            {"model": model_name, "fold": fold_index, "roc_auc": float(score)}
        )

comparison_rows.append(
    {
        "model": "Baseline (prior)",
        "cv_roc_auc_mean": baseline_roc_auc,
        "cv_roc_auc_std": float(np.std(baseline_cv["test_roc_auc"])),
        "train_roc_auc_mean": float(np.mean(baseline_cv["train_roc_auc"])),
        "cv_accuracy_mean": float(np.mean(baseline_cv["test_accuracy"])),
        "cv_precision_mean": float(np.mean(baseline_cv["test_precision"])),
        "cv_recall_mean": float(np.mean(baseline_cv["test_recall"])),
        "cv_f1_mean": float(np.mean(baseline_cv["test_f1"])),
    }
)
for fold_index, score in enumerate(baseline_cv["test_roc_auc"]):
    fold_rows.append({"model": "Baseline (prior)", "fold": fold_index, "roc_auc": float(score)})

comparison = (
    pd.DataFrame(comparison_rows)
    .sort_values("cv_roc_auc_mean", ascending=False)
    .reset_index(drop=True)
)
cv_fold_scores = pd.DataFrame(fold_rows)

comparison.to_csv(ARTIFACT_DIR / "model_comparison.csv", index=False)
cv_fold_scores.to_csv(ARTIFACT_DIR / "cv_fold_scores.csv", index=False)

reference_comparison = comparison.loc[comparison["model"] != "Baseline (prior)"]
best_reference_name = reference_comparison.iloc[0]["model"]
baseline_rank = int(
    comparison.reset_index().loc[comparison["model"] == "Baseline (prior)", "index"].iloc[0]
) + 1

display(comparison.round(4))

fig, ax = plt.subplots(figsize=(9, 4.6))
plot_frame = comparison.sort_values("cv_roc_auc_mean")
colors = ["#adb5bd" if name == "Baseline (prior)" else "#457b9d" for name in plot_frame["model"]]
ax.barh(
    plot_frame["model"],
    plot_frame["cv_roc_auc_mean"],
    xerr=plot_frame["cv_roc_auc_std"],
    color=colors,
    capsize=4,
)
ax.axvline(0.5, color="#e76f51", linestyle="--", linewidth=1.4, label="baseline 0,50")
ax.set_xlim(0, 1.0)
ax.set_xlabel("ROC-AUC rata-rata (GroupKFold, NIM)")
ax.set_title("Perbandingan empat model pada data latih")
for position, value in enumerate(plot_frame["cv_roc_auc_mean"]):
    ax.text(value + 0.012, position, f"{value:.3f}", va="center", fontsize=9)
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(FIGURE_DIR / "cv_model_comparison.png")
plt.show()

print(f"Kandidat terbaik dari perbandingan: {best_reference_name}")
print(f"Posisi baseline pada peringkat: {baseline_rank} dari {len(comparison)}")
