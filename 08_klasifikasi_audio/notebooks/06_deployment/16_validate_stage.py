expected_test_results = [
    "test_predictions.csv",
    "metrics.json",
    "classification_report.csv",
    "confusion_matrix.csv",
    "metrics_by_nim.csv",
    "errors.csv",
]
expected_figures = [
    "roc_curve.png",
    "pr_curve.png",
    "confusion_matrix.png",
    "proba_distribution.png",
    "roc_auc_bootstrap.png",
]
test_results_ok = all(
    (ARTIFACT_ROOT / "test_results" / name).is_file() for name in expected_test_results
) and all((ARTIFACT_ROOT / "test_results" / "figures" / name).is_file() for name in expected_figures)

deployment_artifacts_ok = all(path.is_file() for path in [
    IDENTITY_CHECK_PATH,
    IDENTITY_SUMMARY_PATH,
    DEMO_RESULTS_PATH,
    LAPORAN_PATH,
])
n_raw_now = sum(1 for path in RAW_DIR.rglob("*") if path.is_file())
n_final_now = sum(1 for path in DATA_FINAL_DIR.rglob("*.wav") if path.is_file())

demo_main = demo_results.loc[demo_results["skenario"] == "demo_utama"]
demo_classes_ok = set(demo_main["kelas_asli"]) == set(LABEL_ORDER)
demo_pad_ok = bool(
    (demo_results["skenario"] == "cabang_pad_10_detik").any()
    and demo_results.loc[
        demo_results["skenario"] == "cabang_pad_10_detik", "duration_action"
    ].iloc[0]
    == "pad"
)
demo_crop_ok = bool(
    (demo_results["skenario"] == "cabang_crop_60_detik").any()
    and demo_results.loc[
        demo_results["skenario"] == "cabang_crop_60_detik", "duration_action"
    ].iloc[0]
    == "crop"
)
demo_files_ok = (DEMO_AUDIO_DIR / "demo_10_detik.wav").is_file() and (
    DEMO_AUDIO_DIR / "demo_60_detik.wav"
).is_file()

laporan_text = LAPORAN_PATH.read_text(encoding="utf-8") if LAPORAN_PATH.is_file() else ""
laporan_size = LAPORAN_PATH.stat().st_size if LAPORAN_PATH.is_file() else 0
roc_text = f"{metrics['roc_auc']:.4f}"

checks = {
    "gate03_pass": stage3_validation["status"] == "PASS",
    "gate04_pass": stage4_validation["status"] == "PASS",
    "gate05_pass": stage5_validation["status"] == "PASS",
    "pipeline_struktur": list(saved_model.named_steps) == ["scaler", "select", "clf"],
    "parameter_tidak_berubah": all(
        saved_model.get_params()[key] == value
        for key, value in model_config["best_params"].items()
    ),
    "fitur_input_12": list(features.columns)[4:] == FEATURE_COLUMNS
    and int(saved_model.n_features_in_) == 12,
    "fitur_terpilih_8": selected_from_model == model_config["selected_features_final"]
    and len(selected_from_model) == 8,
    "kontrak_prapemrosesan_cocok": contract["sample_rate"] == SR
    and contract["target_samples"] == TARGET_SAMPLES
    and contract["frame_length"] == FRAME_LENGTH
    and contract["hop_length"] == HOP_LENGTH
    and contract["n_fft"] == N_FFT,
    "sidik_jari_model_tercatat": len(model_file_sha256) == 64 and len(model_fingerprint) == 64,
    "proba_model_identik": model_identity_max_diff < MODEL_IDENTITY_TOL,
    "predict_audio_terdefinisi": callable(globals().get("predict_audio")),
    "fitur_predict_audio_sah": list(smoke_result["features"]) == FEATURE_COLUMNS
    and all(np.isfinite(smoke_result["features"][c]) for c in FEATURE_COLUMNS),
    "identitas_fitur_176": identity_summary["n_files_checked"] == 176
    and identity_summary["max_feature_rel_diff"] < FEATURE_REL_TOL,
    "label_konsisten_176": identity_summary["label_match_vs_direct_176"] == 176,
    "reproduksi_test_40": identity_summary["test_label_match_vs_tahap05"] == 40,
    "probabilitas_test_konsisten": identity_summary["test_max_proba_diff_vs_tahap05"]
    <= PROBA_MATCH_TOL,
    "accuracy_sama_tahap05": abs(
        identity_summary["test_accuracy_pipeline"] - identity_summary["test_accuracy_tahap05"]
    )
    < 1e-12,
    "demo_duakelas": demo_classes_ok,
    "demo_empat_skenario": len(demo_results) == 4,
    "cabang_pad_teruji": demo_pad_ok,
    "cabang_crop_teruji": demo_crop_ok,
    "file_demo_tersimpan": demo_files_ok,
    "laporan_ada": laporan_size > 3000,
    "laporan_memuat_metrik": roc_text in laporan_text
    and metrics["kelayakan_status"] in laporan_text,
    "laporan_memuat_limitasi": "Limitasi dan etika" in laporan_text,
    "laporan_memuat_artefak": "artifacts/best_model.joblib" in laporan_text,
    "test_results_lengkap": test_results_ok,
    "artefak_06_lengkap": deployment_artifacts_ok,
    "raw_audio_tetap_200": n_raw_now == 200,
    "data_final_tetap_176": n_final_now == 176,
    "threshold_konsisten": TEST_THRESHOLD == 0.5
    and float(metrics["test_threshold"]) == TEST_THRESHOLD,
}

check_table = pd.DataFrame(
    {
        "pemeriksaan": list(checks),
        "lulus": [bool(value) for value in checks.values()],
    }
)
check_table["status"] = check_table["lulus"].map({True: "PASS", False: "FAIL"})
display(check_table)

if not check_table["lulus"].all():
    failed = check_table.loc[~check_table["lulus"], "pemeriksaan"].tolist()
    raise ValueError(f"Validasi akhir Tahap 06 gagal: {failed}")

checks_passed = int(check_table["lulus"].sum())
validation_summary = {
    "status": "PASS",
    "model_name": model_config["model_name"],
    "model_class": model_config["model_class"],
    "model_file_sha256": model_file_sha256,
    "model_unchanged": bool(model_identity_max_diff < MODEL_IDENTITY_TOL),
    "predict_audio_defined": True,
    "n_files_identity_checked": int(identity_summary["n_files_checked"]),
    "max_feature_rel_diff": identity_summary["max_feature_rel_diff"],
    "test_label_match_vs_tahap05": identity_summary["test_label_match_vs_tahap05"],
    "test_max_proba_diff_vs_tahap05": identity_summary["test_max_proba_diff_vs_tahap05"],
    "demo_main_files": demo_main["file"].tolist(),
    "demo_classes": sorted(demo_main["kelas_asli"].tolist()),
    "laporan_bytes": int(laporan_size),
    "roc_auc_tahap05": metrics["roc_auc"],
    "kelayakan_status": metrics["kelayakan_status"],
    "checks_passed": checks_passed,
    "checks_total": int(len(check_table)),
}
ARTIFACT_DIR.joinpath("validation_checks.csv").write_text(
    check_table.to_csv(index=False), encoding="utf-8"
)
ARTIFACT_DIR.joinpath("validation_summary.json").write_text(
    json.dumps(validation_summary, ensure_ascii=False, indent=2), encoding="utf-8"
)

report_lines = [
    "# Laporan Validasi Tahap 06",
    "",
    f"Status: **PASS**",
    "",
    "## Angka aktual",
    f"- Model: {model_config['model_name']} (pipeline {' -> '.join(model_config['pipeline_steps'])})",
    f"- Sidik jari file model: `{model_file_sha256}`",
    f"- File diperiksa identitas prapemrosesan: {identity_summary['n_files_checked']}",
    f"- Selisih fitur relatif maksimum: {identity_summary['max_feature_rel_diff']:.3e}",
    f"- Label cocok vs Tahap 05 (40 file uji): {identity_summary['test_label_match_vs_tahap05']}/40",
    f"- Selisih probabilitas vs Tahap 05: {identity_summary['test_max_proba_diff_vs_tahap05']:.3e}",
    f"- Demo: {', '.join(demo_main['file'])} (kelas {', '.join(sorted(demo_main['kelas_asli']))})",
    f"- Cabang durasi teruji: pad (10 detik), crop (60 detik)",
    f"- `artifacts/LAPORAN.md`: {laporan_size} bytes",
    f"- ROC-AUC Tahap 05 yang dilaporkan: {metrics['roc_auc']:.4f} — {metrics['kelayakan_status']}",
    f"- Pemeriksaan lulus: {checks_passed}/{len(check_table)}",
    "",
    "## Catatan",
    "- Tidak ada pelatihan, penalaan, atau pemilihan fitur pada tahap ini.",
    "- Fungsi `predict_audio` memakai kontrak prapemrosesan Tahap 03 tanpa perubahan.",
    "- Metrik hold-out dilaporkan apa adanya, termasuk status di bawah syarat 0,85.",
    "",
]
ARTIFACT_DIR.joinpath("validation_report.md").write_text(
    "\n".join(report_lines), encoding="utf-8"
)

print(f"Validasi akhir Tahap 06: PASS ({checks_passed}/{len(check_table)})")
print(f"Laporan: {ARTIFACT_DIR / 'validation_report.md'}")
