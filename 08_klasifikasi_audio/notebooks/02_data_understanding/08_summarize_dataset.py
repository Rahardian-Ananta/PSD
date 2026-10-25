# Tujuan: merangkum karakteristik dataset aktual menurut kelas, NIM, format, dan metadata sinyal.
# Proses: menghitung tabel agregat, statistik deskriptif, dan menyimpan ringkasan JSON untuk tahap berikutnya.
# Output: class_summary.csv, nim_summary.csv, format_summary.csv, metadata_summary.csv, dan data_understanding_summary.json.

manifest_raw["label_name"] = manifest_raw["label"].map(LABEL_NAME_MAP)
manifest_raw["size_mb"] = manifest_raw["size_bytes"] / (1024**2)

class_summary = (
    manifest_raw.groupby("label_name", dropna=False)
    .agg(
        n_files=("relative_path", "size"),
        n_nim=("nim", "nunique"),
        n_unique_hashes=("sha256", "nunique"),
        n_duplicate_files=("is_exact_duplicate", "sum"),
        n_low_level=("low_level", "sum"),
        duration_min_s=("duration_decoded_s", "min"),
        duration_max_s=("duration_decoded_s", "max"),
        size_median_mb=("size_mb", "median"),
        peak_median=("peak_abs", "median"),
        rms_median=("rms", "median"),
    )
    .reset_index()
)

class_summary["n_files"] = class_summary["n_files"].astype(int)
class_summary["n_nim"] = class_summary["n_nim"].astype(int)
class_summary["n_unique_hashes"] = class_summary["n_unique_hashes"].astype(int)
class_summary["n_duplicate_files"] = class_summary["n_duplicate_files"].astype(int)
class_summary["n_low_level"] = class_summary["n_low_level"].astype(int)

nim_pivot = (
    manifest_raw.pivot_table(
        index="nim",
        columns="label_name",
        values="relative_path",
        aggfunc="count",
        fill_value=0,
    )
    .rename(columns={"berisik": "n_berisik", "non-berisik": "n_non_berisik"})
)
for column in ["n_berisik", "n_non_berisik"]:
    if column not in nim_pivot.columns:
        nim_pivot[column] = 0

nim_summary = nim_pivot.reset_index()
nim_summary["n_files"] = nim_summary["n_berisik"] + nim_summary["n_non_berisik"]
nim_summary["n_unique_hashes"] = manifest_raw.groupby("nim")["sha256"].nunique().reindex(nim_summary["nim"]).values
nim_summary["n_duplicate_files"] = (
    manifest_raw.groupby("nim")["is_exact_duplicate"].sum().reindex(nim_summary["nim"]).astype(int).values
)
nim_summary["lengkap_6_file"] = nim_summary["n_files"].eq(6)
nim_summary["memiliki_dua_kelas"] = (nim_summary["n_berisik"] > 0) & (nim_summary["n_non_berisik"] > 0)
nim_summary = nim_summary.sort_values("nim").reset_index(drop=True)

format_summary = (
    manifest_raw.groupby(["label_name", "samplerate", "channels"])
    .size()
    .rename("n_files")
    .reset_index()
    .sort_values(["label_name", "samplerate", "channels"])
)

metadata_columns = ["duration_decoded_s", "size_mb", "bitrate_kbps_estimate", "peak_abs", "rms"]
metadata_summary = (
    manifest_raw[metadata_columns]
    .describe(percentiles=[0.25, 0.5, 0.75])
    .T.reset_index()
    .rename(columns={"index": "metrik"})
)

duplicate_scope_counts = manifest_raw.loc[
    manifest_raw["is_exact_duplicate"], "duplicate_scope"
].value_counts()

summary = {
    "total_files": int(len(manifest_raw)),
    "total_nim": int(manifest_raw["nim"].nunique()),
    "class_files": {str(k): int(v) for k, v in manifest_raw["label_name"].value_counts().sort_index().items()},
    "class_nims": {str(k): int(v) for k, v in manifest_raw.groupby("label_name")["nim"].nunique().items()},
    "complete_nim": int(nim_summary["lengkap_6_file"].sum()),
    "incomplete_nim": nim_summary.loc[~nim_summary["lengkap_6_file"], "nim"].tolist(),
    "missing_take_combinations": int(len(missing_takes)),
    "read_failures": int((~manifest_raw["read_ok"].fillna(False)).sum()),
    "critical_failures": int(manifest_raw["critical_failure"].sum()),
    "duration_exact_30s": int(manifest_raw["duration_status"].eq("tepat_30_detik").sum()),
    "duration_min_s": float(manifest_raw["duration_decoded_s"].min()),
    "duration_max_s": float(manifest_raw["duration_decoded_s"].max()),
    "sample_rates": {str(int(k)): int(v) for k, v in manifest_raw["samplerate"].value_counts().sort_index().items()},
    "channels": {str(int(k)): int(v) for k, v in manifest_raw["channels"].value_counts().sort_index().items()},
    "unique_hashes": int(manifest_raw["sha256"].nunique()),
    "duplicate_groups": int(len(duplicate_groups)),
    "duplicate_files": int(manifest_raw["is_exact_duplicate"].sum()),
    "duplicate_scopes": {str(k): int(v) for k, v in duplicate_scope_counts.items()},
    "cross_label_groups": int((duplicate_groups["scope"] == "cross_label").sum()) if len(duplicate_groups) else 0,
    "cross_nim_groups": int((duplicate_groups["scope"] == "cross_nim").sum()) if len(duplicate_groups) else 0,
    "within_nim_groups": int((duplicate_groups["scope"] == "within_nim").sum()) if len(duplicate_groups) else 0,
    "low_level_files": int(manifest_raw["low_level"].sum()),
    "peak_over_one_files": int(manifest_raw["peak_over_one"].fillna(False).sum()),
    "empty_signal_files": int(manifest_raw["all_zero"].sum()),
    "nan_files": int(manifest_raw["nan_count"].fillna(0).gt(0).sum()),
    "inf_files": int(manifest_raw["inf_count"].fillna(0).gt(0).sum()),
}

display(class_summary)
display(nim_summary)
display(format_summary)
display(metadata_summary)

class_summary.to_csv(ARTIFACT_DIR / "class_summary.csv", index=False)
nim_summary.to_csv(ARTIFACT_DIR / "nim_summary.csv", index=False)
format_summary.to_csv(ARTIFACT_DIR / "format_summary.csv", index=False)
metadata_summary.to_csv(ARTIFACT_DIR / "metadata_summary.csv", index=False)
with open(ARTIFACT_DIR / "data_understanding_summary.json", "w", encoding="utf-8") as handle:
    json.dump(summary, handle, ensure_ascii=False, indent=2)

print(f"Ringkasan disimpan: {ARTIFACT_DIR / 'data_understanding_summary.json'}")
print(json.dumps(summary, ensure_ascii=False, indent=2))
