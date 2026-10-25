X_features = features[FEATURE_COLUMNS].to_numpy(dtype=float)
y_labels = features["label"].to_numpy(dtype=int)

mi_scores = mutual_info_classif(
    X_features,
    y_labels,
    random_state=RANDOM_STATE,
    n_neighbors=3,
)
rf_model = RandomForestClassifier(
    n_estimators=500,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    class_weight="balanced",
)
rf_model.fit(X_features, y_labels)
rf_importances = rf_model.feature_importances_

feature_importance = pd.DataFrame(
    {
        "feature": FEATURE_COLUMNS,
        "mutual_info": mi_scores,
        "rf_importance": rf_importances,
    }
)
feature_importance["mi_rank"] = feature_importance["mutual_info"].rank(
    method="min", ascending=False
).astype(int)
feature_importance["rf_rank"] = feature_importance["rf_importance"].rank(
    method="min", ascending=False
).astype(int)
feature_importance["mean_rank"] = (
    feature_importance["mi_rank"] + feature_importance["rf_rank"]
) / 2
feature_importance = feature_importance.merge(
    cohens_d_table[["feature", "cohens_d", "abs_cohens_d"]],
    on="feature",
    validate="one_to_one",
)
feature_importance = feature_importance.sort_values(
    ["mean_rank", "abs_cohens_d", "feature"],
    ascending=[True, False, True],
).reset_index(drop=True)

selected_features = feature_importance.head(8)["feature"].tolist()
selected_features_detail = feature_importance.head(8).copy()
selected_features_detail["selection_method"] = (
    "rata-rata peringkat mutual_info_classif dan RandomForest.feature_importances_"
)
selected_features_detail["usage_note"] = (
    "kandidat eksploratif; seleksi final wajib dipelajari ulang di training fold"
)

display(
    feature_importance[["feature", "mutual_info", "mi_rank"]]
    .sort_values("mi_rank")
    .reset_index(drop=True)
)
display(
    feature_importance[["feature", "rf_importance", "rf_rank"]]
    .sort_values("rf_rank")
    .reset_index(drop=True)
)
display(selected_features_detail)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
mi_order = feature_importance.sort_values("mutual_info", ascending=True)
rf_order = feature_importance.sort_values("rf_importance", ascending=True)
axes[0].barh(mi_order["feature"], mi_order["mutual_info"], color="#457b9d")
axes[0].set_title("Mutual information")
axes[0].set_xlabel("Skor")
axes[1].barh(rf_order["feature"], rf_order["rf_importance"], color="#e76f51")
axes[1].set_title("Random Forest importance")
axes[1].set_xlabel("Skor")
fig.tight_layout()
fig.savefig(FIGURE_DIR / "feature_importance.png", bbox_inches="tight")
plt.show()

feature_importance.to_csv(ARTIFACT_DIR / "feature_importance.csv", index=False)
selected_features_detail.to_csv(ARTIFACT_DIR / "selected_features_detail.csv", index=False)

with open(ARTIFACT_ROOT / "selected_features.txt", "w", encoding="utf-8") as handle:
    handle.write("# Kandidat fitur eksploratif untuk Tahap 04\n")
    handle.write("# Metode: rata-rata peringkat mutual_info_classif dan RandomForest.feature_importances_\n")
    handle.write("# Peringatan: seleksi final dan scaling wajib dipelajari ulang di dalam Pipeline pada training fold.\n")
    handle.write("# mi_rank rf_rank mean_rank cohens_d | feature\n")
    for row in selected_features_detail.itertuples():
        handle.write(
            f"{int(row.mi_rank)} {int(row.rf_rank)} {row.mean_rank:.1f} "
            f"{row.cohens_d:.6f} | {row.feature}\n"
        )

print("Kandidat top-8:", ", ".join(selected_features))
print(f"File kandidat: {ARTIFACT_ROOT / 'selected_features.txt'}")
