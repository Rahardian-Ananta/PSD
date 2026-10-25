cohens_rows = []
for feature in FEATURE_COLUMNS:
    group_0 = features.loc[features["label"] == 0, feature].to_numpy(dtype=float)
    group_1 = features.loc[features["label"] == 1, feature].to_numpy(dtype=float)
    n_0, n_1 = len(group_0), len(group_1)
    mean_0, mean_1 = float(np.mean(group_0)), float(np.mean(group_1))
    var_0 = float(np.var(group_0, ddof=1))
    var_1 = float(np.var(group_1, ddof=1))
    pooled_var = ((n_1 - 1) * var_1 + (n_0 - 1) * var_0) / (n_1 + n_0 - 2)
    pooled_sd = float(np.sqrt(pooled_var))
    mean_difference = mean_1 - mean_0

    if pooled_sd == 0:
        if mean_difference == 0:
            cohens_d = 0.0
        else:
            cohens_d = math.copysign(float("inf"), mean_difference)
        note = "s_p=0; d mengikuti aturan eksplisit"
    else:
        cohens_d = mean_difference / pooled_sd
        note = ""

    cohens_rows.append(
        {
            "feature": feature,
            "mean_non_berisik": mean_0,
            "mean_berisik": mean_1,
            "mean_difference": mean_difference,
            "sd_non_berisik": float(np.sqrt(var_0)),
            "sd_berisik": float(np.sqrt(var_1)),
            "pooled_sd": pooled_sd,
            "cohens_d": cohens_d,
            "abs_cohens_d": abs(cohens_d),
            "note": note,
        }
    )

cohens_d_table = (
    pd.DataFrame(cohens_rows)
    .sort_values("abs_cohens_d", ascending=False)
    .reset_index(drop=True)
)
display(cohens_d_table)
cohens_d_table.to_csv(ARTIFACT_DIR / "cohens_d.csv", index=False)
