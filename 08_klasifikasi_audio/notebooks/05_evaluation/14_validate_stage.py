reloaded_model = joblib.load(MODEL_PATH)
in_memory_fingerprint = hashlib.sha256(pickle.dumps(saved_model)).hexdigest()
file_sha256_now = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()

pred_from_csv = pd.read_csv(PREDICTIONS_PATH)
metrics_saved = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
report_saved = pd.read_csv(REPORT_METRICS_PATH, index_col=0)
cm_saved = pd.read_csv(CONFUSION_PATH, index_col=0)
metrics_by_nim_csv = pd.read_csv(METRICS_BY_NIM_PATH)
errors_csv = pd.read_csv(ERRORS_PATH)

required_metric_keys = {
    "roc_auc",
    "pr_auc",
    "accuracy",
    "precision_class_1",
    "recall_class_1",
    "f1_class_1",
    "confusion_matrix",
    "baseline_roc_auc",
    "pr_baseline_prevalence",
    "roc_auc_threshold",
    "roc_auc_meets_threshold",
    "kelayakan_status",
    "roc_auc_ci_low",
    "roc_auc_ci_high",
    "n_bootstrap",
    "nims_test",
    "n_files_test",
    "n_nim_test",
    "random_state",
}
required_result_files = [
    PREDICTIONS_PATH,
    METRICS_PATH,
    REPORT_METRICS_PATH,
    CONFUSION_PATH,
    METRICS_BY_NIM_PATH,
    ERRORS_PATH,
]

proba_from_csv = pred_from_csv[["proba_non_berisik", "proba_berisik"]].to_numpy(dtype=float)
checks = {
    "gate04_pass": (
        stage4_validation["status"] == "PASS"
        and stage4_validation["checks_passed"] == stage4_validation["checks_total"]
        and stage4_validation["holdout_tested_in_stage_04"] is False
    ),
    "konfigurasi_model_lengkap": {
        "model_name",
        "feature_columns",
        "holdout",
        "best_cv_roc_auc",
        "train_rows",
    }.issubset(model_config.keys()),
    "feature_columns_cocok": model_config["feature_columns"] == FEATURE_COLUMNS,
    "model_file_tidak_berubah": file_sha256_now == model_file_sha256_at_load,
    "model_memori_tidak_diubah": in_memory_fingerprint == model_fingerprint_at_load,
    "pipeline_struktur": list(reloaded_model.named_steps) == ["scaler", "select", "clf"],
    "evaluasi_hanya_40_file": len(pred_from_csv) == 40
    and pred_from_csv["file"].is_unique
    and set(pred_from_csv["split"]) == {"test"},
    "evaluasi_hanya_nim_test": set(pred_from_csv["nim"]).issubset(set(nims_test))
    and set(pred_from_csv["nim"]).isdisjoint(set(nims_train)),
    "n_nim_test_7": int(pred_from_csv["nim"].nunique()) == 7,
    "prediksi_tanpa_nan": not pred_from_csv.isna().any().any()
    and np.isfinite(proba_from_csv).all(),
    "probabilitas_sah": float(proba_from_csv.min()) >= 0.0
    and float(proba_from_csv.max()) <= 1.0
    and bool(np.allclose(proba_from_csv.sum(axis=1), 1.0)),
    "threshold_konsisten": bool(
        np.array_equal(
            pred_from_csv["pred_label"].to_numpy(dtype=int),
            (pred_from_csv["proba_berisik"].to_numpy(dtype=float) >= TEST_THRESHOLD).astype(int),
        )
    ),
    "label_prediksi_sah": set(pred_from_csv["pred_label"].unique()).issubset({0, 1}),
    "roc_auc_sah": 0.0 <= roc_auc_value <= 1.0 and np.isfinite(roc_auc_value),
    "pr_auc_sah": 0.0 <= pr_auc_value <= 1.0 and np.isfinite(pr_auc_value),
    "accuracy_sah": abs(accuracy_value - float((pred_label == y_test).mean())) < 1e-12,
    "confusion_40": tn + fp + fn + tp == 40
    and int(metrics_saved["confusion_matrix"]["tn"]) == tn
    and int(cm_saved.to_numpy().sum()) == 40,
    "classification_report_lengkap": {
        "non-berisik",
        "berisik",
        "accuracy",
    }.issubset(set(report_saved.index.astype(str))),
    "metrics_json_lengkap": required_metric_keys.issubset(metrics_saved.keys()),
    "status_085_konsisten": (
        metrics_saved["roc_auc_meets_threshold"] == (roc_auc_value >= ROC_AUC_THRESHOLD)
        and metrics_saved["kelayakan_status"]
        == ("LOLOS SYARAT AWAL" if roc_auc_value >= ROC_AUC_THRESHOLD else "DI BAWAH SYARAT AWAL")
    ),
    "baseline_05_tercatat": abs(float(metrics_saved["baseline_roc_auc"]) - 0.5) < 1e-12,
    "ci_bootstrap_sah": (
        float(metrics_saved["roc_auc_ci_low"]) < float(metrics_saved["roc_auc_ci_high"])
        and 0.0 <= float(metrics_saved["roc_auc_ci_low"])
        and float(metrics_saved["roc_auc_ci_high"]) <= 1.0
        and int(metrics_saved["n_bootstrap"]) == BOOTSTRAP_N
    ),
    "per_nim_7_lengkap": len(metrics_by_nim_csv) == 7
    and int(metrics_by_nim_csv["n_files"].sum()) == 40
    and sorted(metrics_by_nim_csv["nim"].astype(str)) == nims_test,
    "errors_konsisten": len(errors_csv) == fn + fp == int(metrics_saved["n_files_wrong"]),
    "holdout_tidak_dilatih": (
        int(model_config["train_rows"]) == 136
        and int(model_config["holdout"]["n_files_test"]) == 40
        and len(train_frame) == 136
    ),
    "random_state_tercatat": int(metrics_saved["random_state"]) == RANDOM_STATE,
    "test_results_lengkap": all(path.is_file() for path in required_result_files),
    "figures_tersimpan": all((TEST_FIGURE_DIR / name).is_file() for name in FIGURES_EXPECTED),
}

check_table = pd.DataFrame(
    {"pemeriksaan": list(checks.keys()), "lulus": list(checks.values())}
)
check_table["status"] = np.where(check_table["lulus"], "PASS", "FAIL")

if not all(checks.values()):
    display(check_table)
    raise ValueError("Validasi akhir Tahap 05 gagal.")

check_table.to_csv(ARTIFACT_DIR / "validation_checks.csv", index=False)

validation_summary = {
    "status": "PASS",
    "model_name": model_config["model_name"],
    "n_files_test": 40,
    "n_nim_test": 7,
    "roc_auc": roc_auc_value,
    "roc_auc_ci": [ci_low, ci_high],
    "pr_auc": pr_auc_value,
    "accuracy": accuracy_value,
    "precision_class_1": precision_value,
    "recall_class_1": recall_value,
    "f1_class_1": f1_value,
    "kelayakan_status": metrics["kelayakan_status"],
    "model_unchanged": True,
    "holdout_only": True,
    "checks_passed": int(check_table["lulus"].sum()),
    "checks_total": int(len(check_table)),
}
(ARTIFACT_DIR / "validation_summary.json").write_text(
    json.dumps(validation_summary, ensure_ascii=False, indent=2), encoding="utf-8"
)

validation_report_lines = [
    "# Laporan Validasi Tahap 05",
    "",
    "Status: **PASS**",
    "",
    "## Angka aktual",
    "",
    f"- File uji: 40 dari {len(nims_test)} NIM test",
    f"- ROC-AUC: {roc_auc_value:.4f} (CI95 bootstrap {ci_low:.4f} - {ci_high:.4f})",
    f"- PR-AUC: {pr_auc_value:.4f}",
    f"- Precision / recall / F1 kelas 1: {precision_value:.4f} / {recall_value:.4f} / {f1_value:.4f}",
    f"- Confusion TN/FP/FN/TP: {tn}/{fp}/{fn}/{tp}",
    f"- Status syarat 0,85: {metrics['kelayakan_status']}",
    f"- Pemeriksaan lulus: {check_table['lulus'].sum()}/{len(check_table)}",
    "",
    "## Catatan",
    "",
    "- Model tidak di-fit ulang; sidik jari memori dan hash file identik saat dimuat.",
    "- Metrik hanya memakai NIM test; NIM train tidak muncul.",
    "- Threshold keputusan tetap 0,50 dan tidak dituning pada data uji.",
]
(ARTIFACT_DIR / "validation_report.md").write_text(
    "\n".join(validation_report_lines) + "\n", encoding="utf-8"
)

display(check_table)
print("Validasi akhir Tahap 05: PASS")
print(f"Laporan: {ARTIFACT_DIR / 'validation_report.md'}")
