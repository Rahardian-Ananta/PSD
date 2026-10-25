features["label_name"] = features["label"].map(LABEL_NAME_MAP)
correlation_matrix = features[FEATURE_COLUMNS].corr(method="pearson")

high_corr_rows = []
for left_index, left_feature in enumerate(FEATURE_COLUMNS):
    for right_feature in FEATURE_COLUMNS[left_index + 1 :]:
        value = float(correlation_matrix.loc[left_feature, right_feature])
        if abs(value) > 0.90:
            high_corr_rows.append(
                {
                    "feature_1": left_feature,
                    "feature_2": right_feature,
                    "pearson_r": value,
                    "abs_r": abs(value),
                }
            )
high_corr_pairs = pd.DataFrame(
    high_corr_rows, columns=["feature_1", "feature_2", "pearson_r", "abs_r"]
).sort_values("abs_r", ascending=False, ignore_index=True)

fig, ax = plt.subplots(figsize=(10.5, 8.5))
sns.heatmap(
    correlation_matrix,
    cmap="vlag",
    center=0,
    vmin=-1,
    vmax=1,
    annot=True,
    fmt=".2f",
    annot_kws={"size": 7},
    linewidths=0.5,
    square=True,
    ax=ax,
)
ax.set_title("Korelasi Pearson 12 fitur (seluruh file final)")
fig.tight_layout()
fig.savefig(FIGURE_DIR / "feature_correlation_heatmap.png", bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(4, 3, figsize=(15, 12))
for ax, feature in zip(axes.ravel(), FEATURE_COLUMNS):
    sns.boxplot(
        data=features,
        x="label_name",
        y=feature,
        order=LABEL_ORDER,
        hue="label_name",
        palette={"non-berisik": "#74c69d", "berisik": "#e76f51"},
        legend=False,
        dodge=False,
        showfliers=True,
        ax=ax,
    )
    ax.set_title(feature)
    ax.set_xlabel("")
    ax.set_ylabel("")
fig.suptitle("Distribusi fitur per kelas; outlier tidak dihapus", y=1.002)
fig.tight_layout()
fig.savefig(FIGURE_DIR / "feature_boxplots_by_class.png", bbox_inches="tight")
plt.show()

outlier_rows = []
for label_name in LABEL_ORDER:
    label_values = features.loc[features["label_name"] == label_name]
    for feature in FEATURE_COLUMNS:
        values = label_values[feature]
        q1 = float(values.quantile(0.25))
        q3 = float(values.quantile(0.75))
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_rows.append(
            {
                "label_name": label_name,
                "feature": feature,
                "q1": q1,
                "q3": q3,
                "iqr": iqr,
                "lower_bound": lower,
                "upper_bound": upper,
                "n_outlier_iqr": int(((values < lower) | (values > upper)).sum()),
            }
        )
outlier_counts = pd.DataFrame(outlier_rows)

display(
    high_corr_pairs
    if len(high_corr_pairs)
    else pd.DataFrame({"catatan": ["Tidak ada pasangan fitur dengan |r| > 0,90"]})
)
display(
    outlier_counts.pivot(index="feature", columns="label_name", values="n_outlier_iqr")
    .reindex(FEATURE_COLUMNS)
    .fillna(0)
    .astype(int)
)

correlation_matrix.to_csv(ARTIFACT_DIR / "feature_correlation_pearson.csv")
high_corr_pairs.to_csv(ARTIFACT_DIR / "high_correlation_pairs.csv", index=False)
outlier_counts.to_csv(ARTIFACT_DIR / "outlier_counts_iqr.csv", index=False)
