path_by_file = transformation_manifest.set_index("file")
split_by_file = holdout_file_split.set_index("file")["split"]
recorded = test_predictions.set_index("file")

identity_rows = []
for row in features.sort_values("file").itertuples():
    final_path = DATA_FINAL_DIR / path_by_file.at[row.file, "final_relative_path"]
    result = predict_audio(final_path)

    ref_features = {column: float(getattr(row, column)) for column in FEATURE_COLUMNS}
    rel_diffs = {}
    abs_diffs = {}
    for column in FEATURE_COLUMNS:
        pipeline_value = float(result["features"][column])
        reference_value = ref_features[column]
        abs_diffs[column] = abs(pipeline_value - reference_value)
        denom = max(abs(pipeline_value), abs(reference_value), 1e-12)
        rel_diffs[column] = abs_diffs[column] / denom

    frame_direct = pd.DataFrame([[ref_features[c] for c in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
    proba_direct = float(saved_model.predict_proba(frame_direct.to_numpy(dtype=float))[0][1])
    pred_direct = int(proba_direct >= TEST_THRESHOLD)
    split_value = split_by_file.at[row.file]

    proba_recorded = float(recorded.at[row.file, "proba_berisik"]) if split_value == "test" else np.nan
    pred_recorded = int(recorded.at[row.file, "pred_label"]) if split_value == "test" else -1

    identity_rows.append(
        {
            "file": row.file,
            "nim": row.nim,
            "label": int(row.label),
            "split": split_value,
            "duration_action": result["duration_action"],
            "proba_direct": proba_direct,
            "proba_pipeline": result["proba_berisik"],
            "proba_recorded": proba_recorded,
            "pred_direct": pred_direct,
            "pred_pipeline": result["label"],
            "pred_recorded": pred_recorded,
            "proba_pipeline_vs_direct": abs(result["proba_berisik"] - proba_direct),
            "proba_pipeline_vs_recorded": (
                abs(result["proba_berisik"] - proba_recorded)
                if split_value == "test"
                else np.nan
            ),
            "feature_max_rel_diff": max(rel_diffs.values()),
            "feature_max_abs_diff": max(abs_diffs.values()),
            "feature_worst": max(rel_diffs, key=rel_diffs.get),
        }
    )

identity_check = pd.DataFrame(identity_rows)
assert len(identity_check) == 176
assert np.isfinite(
    identity_check[["proba_direct", "proba_pipeline", "feature_max_rel_diff"]].to_numpy()
).all()

max_feature_rel_diff = float(identity_check["feature_max_rel_diff"].max())
max_feature_abs_diff = float(identity_check["feature_max_abs_diff"].max())
max_proba_diff_direct = float(identity_check["proba_pipeline_vs_direct"].max())
n_label_match_176 = int((identity_check["pred_pipeline"] == identity_check["pred_direct"]).sum())

test_identity = identity_check.loc[identity_check["split"] == "test"]
assert len(test_identity) == 40
n_test_label_match = int((test_identity["pred_pipeline"] == test_identity["pred_recorded"]).sum())
max_test_proba_diff = float(test_identity["proba_pipeline_vs_recorded"].max())
test_accuracy = float(
    (identity_check["pred_pipeline"] == identity_check["label"]).loc[
        identity_check["split"] == "test"
    ].mean()
)

identity_summary = {
    "n_files_checked": int(len(identity_check)),
    "max_feature_rel_diff": max_feature_rel_diff,
    "max_feature_abs_diff": max_feature_abs_diff,
    "max_proba_diff_pipeline_vs_direct": max_proba_diff_direct,
    "label_match_vs_direct_176": n_label_match_176,
    "test_label_match_vs_tahap05": n_test_label_match,
    "test_max_proba_diff_vs_tahap05": max_test_proba_diff,
    "test_accuracy_pipeline": test_accuracy,
    "test_accuracy_tahap05": float(metrics["accuracy"]),
    "feature_rel_tolerance": FEATURE_REL_TOL,
    "proba_match_tolerance": PROBA_MATCH_TOL,
}
IDENTITY_SUMMARY_PATH.write_text(
    json.dumps(identity_summary, ensure_ascii=False, indent=2), encoding="utf-8"
)
identity_check.to_csv(IDENTITY_CHECK_PATH, index=False)

identity_view = pd.DataFrame(
    {
        "pemeriksaan": [
            "file diperiksa",
            "selisih fitur relatif maksimum",
            "selisih fitur absolut maksimum",
            "selisih probabilitas vs model langsung",
            "label cocok vs model langsung",
            "label cocok vs Tahap 05 (40 file uji)",
            "selisih probabilitas vs Tahap 05",
            "accuracy pipeline pada 40 file uji",
            "accuracy Tahap 05",
        ],
        "nilai": [
            identity_summary["n_files_checked"],
            f"{max_feature_rel_diff:.3e}",
            f"{max_feature_abs_diff:.3e}",
            f"{max_proba_diff_direct:.3e}",
            f"{n_label_match_176} / 176",
            f"{n_test_label_match} / 40",
            f"{max_test_proba_diff:.3e}",
            f"{test_accuracy:.4f}",
            f"{metrics['accuracy']:.4f}",
        ],
        "acuan": [
            "seluruh data_final/",
            f"toleransi {FEATURE_REL_TOL:g}",
            "kuantisasi PCM16 ulang",
            "toleransi 1e-12",
            "harus 176 / 176",
            "harus 40 / 40",
            f"toleransi {PROBA_MATCH_TOL:g}",
            "harus sama",
            "dari metrics.json",
        ],
    }
)
display(identity_view)
display(
    identity_check.sort_values("feature_max_rel_diff", ascending=False).head(5)[
        [
            "file",
            "split",
            "feature_max_rel_diff",
            "feature_worst",
            "proba_pipeline_vs_recorded",
            "pred_pipeline",
            "pred_recorded",
        ]
    ]
)
print(
    f"Identitas prapemrosesan: 176/176 label cocok, "
    f"selisih fitur relatif maks {max_feature_rel_diff:.3e}, "
    f"selisih probabilitas vs Tahap 05 maks {max_test_proba_diff:.3e}."
)
