features_saved = pd.read_csv(ARTIFACT_ROOT / "features.csv")
final_dataset_manifest = transformation_manifest.merge(
    features_saved,
    on=["file", "nim", "take", "label"],
    how="inner",
    validate="one_to_one",
)
final_dataset_manifest = final_dataset_manifest.sort_values(
    ["nim", "label", "take"]
).reset_index(drop=True)

features_by_file_check = features_saved.set_index("file")
audio_checks = []
for row in final_dataset_manifest.itertuples():
    final_path = DATA_FINAL_DIR / row.final_relative_path
    mp3_path = DATA_MP3_DIR / row.mp3_relative_path
    raw_path = RAW_DIR / row.source_relative_path
    y, sr = sf.read(final_path, dtype="float32")
    info = sf.info(final_path)
    audio_checks.append(
        {
            "file": row.file,
            "raw_ada": raw_path.is_file(),
            "mp3_ada": mp3_path.is_file(),
            "final_ada": final_path.is_file(),
            "raw_mp3_hash_sama": row.source_sha256
            == hashlib.sha256(mp3_path.read_bytes()).hexdigest(),
            "final_hash_sama": row.final_sha256
            == hashlib.sha256(final_path.read_bytes()).hexdigest(),
            "sr_16k": sr == SR,
            "mono": info.channels == 1,
            "pcm16": info.subtype == "PCM_16",
            "frames_480000": len(y) == TARGET_SAMPLES,
            "no_nan": int(np.isnan(y).sum()) == 0,
            "no_inf": int(np.isinf(y).sum()) == 0,
            "peak_ok": float(np.max(np.abs(y))) <= 1.00001,
        }
    )
audio_check_frame = pd.DataFrame(audio_checks)

nim_final_check = (
    features_saved.groupby(["nim", "label"]).size().unstack(fill_value=0)
)
for label in [0, 1]:
    if label not in nim_final_check.columns:
        nim_final_check[label] = 0
all_nims_both = bool(
    ((nim_final_check[0] > 0) & (nim_final_check[1] > 0)).all()
)

feature_ranges = {
    "mse_energy": (0, None),
    "rms_mean": (0, None),
    "rms_std": (0, None),
    "rms_max": (0, None),
    "rms_min": (0, None),
    "zcr_mean": (0, 1),
    "zcr_std": (0, None),
    "spectral_centroid_mean": (0, SR / 2),
    "spectral_centroid_std": (0, SR / 2),
    "spectral_flatness_mean": (0, 1),
    "spectral_rolloff_mean": (0, SR / 2),
    "spectral_bandwidth_mean": (0, SR / 2),
}
range_failures = []
for feature, (lower, upper) in feature_ranges.items():
    values = features_saved[feature]
    if lower is not None and (values < lower).any():
        range_failures.append(f"{feature} < {lower}")
    if upper is not None and (values > upper + 1e-9).any():
        range_failures.append(f"{feature} > {upper}")

selected_features_lines = [
    line.split("|")[-1].strip()
    for line in (ARTIFACT_ROOT / "selected_features.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]
selected_features_from_file = selected_features_lines

checks = {
    "file_awal_200": len(manifest) == 200,
    "file_final_176": len(final_dataset_manifest) == 176,
    "file_karantina_24": len(quarantine_manifest) == 24,
    "final_plus_karantina_200": len(final_dataset_manifest) + len(quarantine_manifest)
    == len(manifest),
    "data_mp3_176": len(list(DATA_MP3_DIR.rglob("*.mp3"))) == 176,
    "data_final_176": len(list(DATA_FINAL_DIR.rglob("*.wav"))) == 176,
    "quarantine_24_mp3": len(list(QUARANTINE_DIR.rglob("*.mp3"))) == 24,
    "raw_tetap_200": len(list(RAW_DIR.rglob("*.mp3"))) == 200,
    "features_176": len(features_saved) == 176,
    "features_unik": features_saved["file"].is_unique,
    "fitur_lengkap_12": list(features_saved.columns) == IDENTITY_COLUMNS + FEATURE_COLUMNS,
    "fitur_numerik": all(pd.api.types.is_numeric_dtype(features_saved[column]) for column in FEATURE_COLUMNS),
    "fitur_tanpa_nan": not features_saved[FEATURE_COLUMNS].isna().any().any(),
    "fitur_tanpa_inf": np.isfinite(features_saved[FEATURE_COLUMNS].to_numpy(dtype=float)).all(),
    "rentang_fitur_valid": len(range_failures) == 0,
    "file_identitas_unik": not features_saved.duplicated(["nim", "take", "label"]).any(),
    "kelas_seimbang_88_88": features_saved["label"].value_counts().to_dict() == {0: 88, 1: 88},
    "nim_final_34": features_saved["nim"].nunique() == 34,
    "semua_nim_dua_kelas": all_nims_both,
    "semua_audio_valid": audio_check_frame.drop(columns=["file"]).all().all(),
    "final_hash_unik": final_dataset_manifest["final_sha256"].is_unique,
    "traceability_lengkap": audio_check_frame[
        ["raw_ada", "mp3_ada", "final_ada", "raw_mp3_hash_sama", "final_hash_sama"]
    ].all().all(),
    "rfft_fft_konsisten": fft_rfft_max_abs_diff <= 1e-6,
    "librosa_comparison_5_fitur": len(comparison_summary) == 5,
    "top8_kandidat": len(selected_features_from_file) == 8,
    "top8_semua_ada": set(selected_features_from_file).issubset(set(FEATURE_COLUMNS)),
    "tidak_ada_nim_satu_kelas": not features_saved.groupby("nim")["label"].nunique().eq(1).any(),
    "silent_frames_terdokumentasi": len(silent_frame_audit) == 176,
}
check_table = pd.DataFrame(
    {
        "pemeriksaan": list(checks.keys()),
        "lulus": list(checks.values()),
    }
)
check_table["status"] = np.where(check_table["lulus"], "PASS", "FAIL")

if not all(checks.values()):
    display(check_table)
    raise ValueError("Validasi akhir Tahap 03 gagal.")

uncertain_nims = pd.DataFrame(columns=["nim", "reason", "action"])
excluded_files = quarantine_manifest[
    [
        "relative_path",
        "file",
        "nim",
        "take",
        "label",
        "label_name",
        "selection_reason",
        "duplicate_group_id",
        "duplicate_scope",
        "sha256",
    ]
].copy()

final_dataset_manifest.to_csv(ARTIFACT_DIR / "final_dataset_manifest.csv", index=False)
excluded_files.to_csv(ARTIFACT_DIR / "excluded_files.csv", index=False)
uncertain_nims.to_csv(ARTIFACT_DIR / "uncertain_nims.csv", index=False)
check_table.to_csv(ARTIFACT_DIR / "validation_checks.csv", index=False)
audio_check_frame.to_csv(ARTIFACT_DIR / "audio_validation_detail.csv", index=False)

validation_summary = {
    "status": "PASS",
    "n_raw": int(len(manifest)),
    "n_final": int(len(final_dataset_manifest)),
    "n_quarantine": int(len(quarantine_manifest)),
    "n_features": int(len(features_saved)),
    "n_nim": int(features_saved["nim"].nunique()),
    "class_counts": {str(k): int(v) for k, v in features_saved["label"].value_counts().sort_index().items()},
    "n_final_hashes": int(final_dataset_manifest["final_sha256"].nunique()),
    "n_uncertain_nims": int(len(uncertain_nims)),
    "n_zero_power_frames": int(silent_frame_audit["empty_power_frames"].sum()),
    "n_files_with_zero_power_frames": int((silent_frame_audit["empty_power_frames"] > 0).sum()),
    "selected_features": selected_features_from_file,
    "range_failures": range_failures,
    "fft_rfft_max_abs_diff": float(fft_rfft_max_abs_diff),
    "checks_passed": int(check_table["lulus"].sum()),
    "checks_total": int(len(check_table)),
}
with open(ARTIFACT_DIR / "validation_summary.json", "w", encoding="utf-8") as handle:
    json.dump(validation_summary, handle, ensure_ascii=False, indent=2)

report_lines = [
    "# Laporan Validasi Tahap 03",
    "",
    "Status: **PASS**",
    "",
    "## Angka aktual",
    "",
    f"- File awal: {len(manifest)}",
    f"- File final: {len(final_dataset_manifest)}",
    f"- File karantina: {len(quarantine_manifest)}",
    f"- NIM final: {features_saved['nim'].nunique()}",
    f"- Distribusi kelas: {validation_summary['class_counts']}",
    f"- Baris features.csv: {len(features_saved)}",
    f"- Hash WAV final unik: {final_dataset_manifest['final_sha256'].nunique()}",
    f"- NIM tidak pasti: {len(uncertain_nims)}",
    f"- Frame dengan daya nol: {int(silent_frame_audit['empty_power_frames'].sum())} pada {int((silent_frame_audit['empty_power_frames'] > 0).sum())} file",
    f"- Pemeriksaan lulus: {check_table['lulus'].sum()}/{len(check_table)}",
    "",
    "## Catatan",
    "",
    "- `24-123` tidak memiliki file final karena seluruh file-nya menjadi duplikat non-wakil.",
    "- Frame dengan daya nol adalah hening digital yang nyata; frame tidak dihapus. Centroid, flatness, rolloff, dan bandwidth frame tersebut ditetapkan 0.",
    "- Split berbasis NIM belum dibuat; itu menjadi tanggung jawab Tahap 04.",
    "- Fitur kandidat bersifat eksploratif dan harus dipelajari ulang di dalam Pipeline pada training fold.",
]
with open(ARTIFACT_DIR / "validation_report.md", "w", encoding="utf-8") as handle:
    handle.write("\n".join(report_lines) + "\n")

display(check_table)
print("Validasi akhir Tahap 03: PASS")
print(f"Laporan: {ARTIFACT_DIR / 'validation_report.md'}")
