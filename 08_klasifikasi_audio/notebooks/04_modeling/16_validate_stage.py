loaded_model = joblib.load(MODEL_PATH)
probe_X = X_train[:8]
probe_pred = loaded_model.predict(probe_X)
probe_pred_again = loaded_model.predict(probe_X)
probe_proba = loaded_model.predict_proba(probe_X)

saved_config = json.loads(MODEL_CONFIG_PATH.read_text(encoding="utf-8"))
feature_list = [
    line.strip()
    for line in FEATURE_LIST_PATH.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]

cv_disjoint = True
cv_within_train = True
fold_audit_rows = []
train_nims_set = set(nims_train)
for fold_index, (fit_idx, val_idx) in enumerate(
    GroupKFold(n_splits=N_SPLITS).split(X_train, y_train, groups=groups_train)
):
    fit_nims = set(model_train["nim"].iloc[fit_idx])
    val_nims = set(model_train["nim"].iloc[val_idx])
    if fit_nims & val_nims:
        cv_disjoint = False
    if not val_nims.issubset(train_nims_set):
        cv_within_train = False
    fold_audit_rows.append(
        {
            "fold": fold_index,
            "n_nim_fit": len(fit_nims),
            "n_nim_validate": len(val_nims),
            "overlap_nim": len(fit_nims & val_nims),
            "n_file_validate": int(len(val_idx)),
            "n_class_0_validate": int((y_train[val_idx] == 0).sum()),
            "n_class_1_validate": int((y_train[val_idx] == 1).sum()),
        }
    )
cv_fold_audit = pd.DataFrame(fold_audit_rows)
cv_fold_audit.to_csv(ARTIFACT_DIR / "cv_fold_audit.csv", index=False)

pipeline_steps = list(loaded_model.named_steps)
required_config_keys = {
    "stage",
    "model_name",
    "best_params",
    "best_cv_roc_auc",
    "baseline_cv_roc_auc",
    "cv",
    "holdout",
    "random_state",
    "feature_columns",
    "n_features_selected",
    "selected_features_final",
}
figures_expected = [
    "holdout_composition.png",
    "cv_model_comparison.png",
    "grid_search_scores.png",
]
class_counts = features["label"].value_counts().to_dict()

checks = {
    "gate03_pass": (
        stage3_validation["status"] == "PASS"
        and stage3_validation["checks_passed"] == stage3_validation["checks_total"]
    ),
    "features_176": len(features) == 176,
    "fitur_12_bersih": (
        set(FEATURE_COLUMNS).issubset(features.columns)
        and not features[FEATURE_COLUMNS].isna().any().any()
        and np.isfinite(features[FEATURE_COLUMNS].to_numpy(dtype=float)).all()
    ),
    "kelas_88_88": int(class_counts.get(0, 0)) == 88 and int(class_counts.get(1, 0)) == 88,
    "holdout_nim_test_sebesar_20persen": len(nims_test)
    == int(np.ceil(TEST_SIZE * len(nims_all))),
    "holdout_disjoint": set(nims_train).isdisjoint(set(nims_test)),
    "holdout_menutup_34_nim": set(nims_train) | set(nims_test) == set(nims_all),
    "holdout_file_176": (
        len(holdout_file_split) == 176
        and int(holdout_file_split["split"].isin(["train", "test"]).sum()) == 176
    ),
    "holdout_kelas_terlapor": (
        int(holdout_file_split.loc[holdout_file_split["split"] == "train"].shape[0]) > 0
        and int(holdout_file_split.loc[holdout_file_split["split"] == "test"].shape[0]) > 0
    ),
    "cv_groups_disjoint": cv_disjoint,
    "cv_hanya_nim_train": cv_within_train,
    "data_latih_tanpa_holdout": (
        set(model_train["nim"]).isdisjoint(set(nims_test))
        and len(model_train) + len(model_test) == 176
    ),
    "empat_model_dibandingkan": len(reference_comparison) == 4,
    "baseline_roc_auc_050": abs(baseline_roc_auc - 0.5) < 1e-9,
    "grid_search_selesai": bool(
        np.isfinite(search.best_score_) and len(grid_results) > 0
    ),
    "pipeline_tiga_langkah": pipeline_steps == ["scaler", "select", "clf"],
    "seleksi_fitur_dalam_pipeline": isinstance(
        loaded_model.named_steps["select"], SelectKBest
    ),
    "tanpa_pca": "pca" not in pipeline_steps,
    "joblib_dimuat": MODEL_PATH.is_file() and isinstance(loaded_model, Pipeline),
    "prediksi_valid": (
        len(probe_pred) == len(probe_X)
        and set(np.unique(probe_pred)).issubset({0, 1})
        and probe_proba.shape == (len(probe_X), 2)
        and float(probe_proba.min()) >= 0.0
        and float(probe_proba.max()) <= 1.0
        and bool(np.allclose(probe_proba.sum(axis=1), 1.0))
    ),
    "prediksi_deterministik": bool(np.array_equal(probe_pred, probe_pred_again)),
    "konfigurasi_lengkap": required_config_keys.issubset(saved_config.keys()),
    "konfigurasi_konsisten": (
        saved_config["model_name"] == best_reference_name
        and abs(saved_config["best_cv_roc_auc"] - float(search.best_score_)) < 1e-12
        and saved_config["holdout"]["nims_train"] == nims_train
        and saved_config["holdout"]["nims_test"] == nims_test
    ),
    "daftar_fitur_12": set(feature_list) == set(FEATURE_COLUMNS),
    "fitur_terpilih_valid": (
        0
        < int(saved_config["n_features_selected"])
        <= len(FEATURE_COLUMNS)
        and set(saved_config["selected_features_final"]).issubset(set(FEATURE_COLUMNS))
        and len(saved_config["selected_features_final"])
        == int(saved_config["n_features_selected"])
    ),
    "random_state_tercatat": saved_config["random_state"] == RANDOM_STATE,
    "cv_tercatat": (
        saved_config["cv"]["n_splits"] == N_SPLITS
        and saved_config["cv"]["scoring"] == SCORING
        and saved_config["cv"]["groups"] == "nim"
    ),
    "holdout_nims_tercatat": (
        saved_config["holdout"]["nims_train"] == nims_train
        and saved_config["holdout"]["nims_test"] == nims_test
    ),
    "figures_tersimpan": all(
        (FIGURE_DIR / name).is_file() for name in figures_expected
    ),
}

check_table = pd.DataFrame(
    {"pemeriksaan": list(checks.keys()), "lulus": list(checks.values())}
)
check_table["status"] = np.where(check_table["lulus"], "PASS", "FAIL")

if not all(checks.values()):
    display(check_table)
    raise ValueError("Validasi akhir Tahap 04 gagal.")

check_table.to_csv(ARTIFACT_DIR / "validation_checks.csv", index=False)

validation_summary = {
    "status": "PASS",
    "model_name": best_reference_name,
    "model_class": saved_config["model_class"],
    "best_cv_roc_auc": float(search.best_score_),
    "baseline_cv_roc_auc": baseline_roc_auc,
    "n_combinations": int(len(grid_results)),
    "best_params": saved_config["best_params"],
    "n_features_total": len(FEATURE_COLUMNS),
    "n_features_selected": int(saved_config["n_features_selected"]),
    "selected_features_final": saved_config["selected_features_final"],
    "n_nim_total": len(nims_all),
    "n_nim_train": len(nims_train),
    "n_nim_test": len(nims_test),
    "n_files_train": int(len(model_train)),
    "n_files_test": int(len(model_test)),
    "class_counts_train": saved_config["holdout"]["class_counts_train"],
    "class_counts_test": saved_config["holdout"]["class_counts_test"],
    "n_splits": N_SPLITS,
    "scoring": SCORING,
    "random_state": RANDOM_STATE,
    "checks_passed": int(check_table["lulus"].sum()),
    "checks_total": int(len(check_table)),
    "holdout_tested_in_stage_04": False,
}
(ARTIFACT_DIR / "validation_summary.json").write_text(
    json.dumps(validation_summary, ensure_ascii=False, indent=2), encoding="utf-8"
)

validation_report_lines = [
    "# Laporan Validasi Tahap 04",
    "",
    "Status: **PASS**",
    "",
    "## Angka aktual",
    "",
    f"- Model terpilih: {best_reference_name} ({saved_config['model_class']})",
    f"- ROC-AUC CV terbaik: {search.best_score_:.4f} (baseline {baseline_roc_auc:.2f})",
    f"- Kombinasi hyperparameter: {len(grid_results)}",
    f"- Fitur terpilih setelah refit: {saved_config['n_features_selected']} dari {len(FEATURE_COLUMNS)}",
    f"- NIM train/test: {len(nims_train)} / {len(nims_test)}",
    f"- File train/test: {len(model_train)} / {len(model_test)}",
    f"- Fold GroupKFold: {N_SPLITS} (grup = NIM, overlap 0)",
    f"- Pemeriksaan lulus: {check_table['lulus'].sum()}/{len(check_table)}",
    "",
    "## Catatan",
    "",
    "- Hold-out NIM **belum** dipakai untuk evaluasi pada tahap ini.",
    "- Uji hold-out, kurva ROC/PR, confusion matrix, dan classification report dikerjakan di Tahap 05.",
    "- Scaler dan seleksi fitur berada di dalam pipeline sehingga tidak ada kebocoran preprocessing.",
    "- Tidak ada PCA.",
]
(ARTIFACT_DIR / "validation_report.md").write_text(
    "\n".join(validation_report_lines) + "\n", encoding="utf-8"
)

display(check_table)
print("Validasi akhir Tahap 04: PASS")
print(f"Laporan: {ARTIFACT_DIR / 'validation_report.md'}")
