def json_safe(value):
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


selector = best_pipeline.named_steps["select"]
selected_mask = selector.get_support()
selected_features_final = [
    feature for feature, keep in zip(FEATURE_COLUMNS, selected_mask) if keep
]

joblib.dump(best_pipeline, MODEL_PATH)

model_config = {
    "stage": "04_modeling",
    "model_name": best_reference_name,
    "model_class": type(best_pipeline.named_steps["clf"]).__name__,
    "pipeline_steps": [name for name, _ in best_pipeline.steps],
    "best_params": json_safe(search.best_params_),
    "best_cv_roc_auc": float(search.best_score_),
    "reference_cv_roc_auc_mean": float(
        reference_comparison.loc[
            reference_comparison["model"] == best_reference_name, "cv_roc_auc_mean"
        ].iloc[0]
    ),
    "baseline_cv_roc_auc": baseline_roc_auc,
    "cv": {
        "splitter": "GroupKFold",
        "n_splits": N_SPLITS,
        "groups": "nim",
        "scoring": SCORING,
    },
    "holdout": {
        "splitter": "GroupShuffleSplit",
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "n_nim_train": len(nims_train),
        "n_nim_test": len(nims_test),
        "nims_train": nims_train,
        "nims_test": nims_test,
        "n_files_train": int(len(model_train)),
        "n_files_test": int(len(model_test)),
        "class_counts_train": {
            str(key): int(value)
            for key, value in model_train["label"].value_counts().sort_index().items()
        },
        "class_counts_test": {
            str(key): int(value)
            for key, value in model_test["label"].value_counts().sort_index().items()
        },
    },
    "random_state": RANDOM_STATE,
    "feature_columns": FEATURE_COLUMNS,
    "n_features_total": len(FEATURE_COLUMNS),
    "n_features_selected": int(selected_mask.sum()),
    "selected_features_final": selected_features_final,
    "train_rows": int(len(model_train)),
    "library_versions": library_versions.set_index("komponen")["versi"].to_dict(),
    "preprocessing_note": (
        "fitur diambil dari artifacts/features.csv; prapemrosesan audio mengikuti "
        "artifacts/03_data_preparation/preprocessing_contract.json"
    ),
    "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}
model_config = json_safe(model_config)
MODEL_CONFIG_PATH.write_text(
    json.dumps(model_config, ensure_ascii=False, indent=2), encoding="utf-8"
)

feature_list_lines = [
    "# Daftar fitur untuk artifacts/best_model.joblib (Tahap 04)",
    f"# k_fitur_terpilih: {model_config['n_features_selected']} dari "
    f"{model_config['n_features_total']} (SelectKBest f_classif, dipelajari pada training fold)",
    f"# model: {model_config['model_name']} ({model_config['model_class']})",
    "# peringatan: angka fitur pada Tahap 03 bersifat eksploratif; pipeline inilah yang berlaku",
    *model_config["feature_columns"],
]
FEATURE_LIST_PATH.write_text("\n".join(feature_list_lines) + "\n", encoding="utf-8")

display(
    pd.DataFrame(
        {
            "item": [
                "model_name",
                "model_class",
                "best_cv_roc_auc",
                "baseline_cv_roc_auc",
                "best_params",
                "n_features_selected",
                "selected_features_final",
                "n_files_train / n_files_test",
                "n_nim_train / n_nim_test",
                "random_state",
            ],
            "nilai": [
                model_config["model_name"],
                model_config["model_class"],
                f"{model_config['best_cv_roc_auc']:.4f}",
                f"{model_config['baseline_cv_roc_auc']:.4f}",
                str(model_config["best_params"]),
                model_config["n_features_selected"],
                ", ".join(model_config["selected_features_final"]),
                f"{model_config['holdout']['n_files_train']} / "
                f"{model_config['holdout']['n_files_test']}",
                f"{model_config['holdout']['n_nim_train']} / "
                f"{model_config['holdout']['n_nim_test']}",
                model_config["random_state"],
            ],
        }
    )
)
print(f"Model disimpan: {MODEL_PATH}")
print(f"Konfigurasi: {MODEL_CONFIG_PATH}")
print(f"Daftar fitur: {FEATURE_LIST_PATH}")
