# Tujuan: memeriksa integritas teknis file dan menyusun manifest mentah terpadu.
# Proses: menggabungkan identitas, hash, dan metadata; memeriksa file rusak, sinyal kosong, NaN/Inf, durasi, dan level sinyal sangat rendah.
# Output: manifest mentah, tabel pemeriksaan integritas, dan daftar file level rendah.

manifest_raw = hashed_inventory.merge(
    audio_metadata,
    on="relative_path",
    how="left",
    validate="one_to_one",
)

manifest_raw["duration_delta_s"] = manifest_raw["duration_decoded_s"] - EXPECTED_DURATION_S
manifest_raw["duration_status"] = np.select(
    [
        manifest_raw["duration_delta_s"].abs() <= DURATION_TOLERANCE_S,
        manifest_raw["duration_delta_s"] < 0,
        manifest_raw["duration_delta_s"] > 0,
    ],
    ["tepat_30_detik", "lebih_pendek", "lebih_panjang"],
    default="tidak_diketahui",
)
manifest_raw["all_zero"] = manifest_raw["peak_abs"].fillna(0).eq(0)
manifest_raw["low_level"] = manifest_raw["peak_abs"].fillna(0).lt(LOW_PEAK_THRESHOLD)
manifest_raw["numeric_invalid"] = manifest_raw["nan_count"].fillna(0).gt(0) | manifest_raw["inf_count"].fillna(0).gt(0)
manifest_raw["critical_failure"] = (
    ~manifest_raw["read_ok"].fillna(False)
    | manifest_raw["decoded_frames"].fillna(0).le(0)
    | ~manifest_raw["extension_ok"].fillna(False)
    | manifest_raw["all_zero"].fillna(False)
    | manifest_raw["numeric_invalid"].fillna(False)
)

integrity_checks = pd.DataFrame(
    {
        "pemeriksaan": [
            "file berhasil dibaca",
            "file gagal dibaca",
            "frame hasil decode > 0",
            "file dengan NaN",
            "file dengan Inf",
            "file dengan sinyal semua nol",
            "durasi tepat 30 detik",
            "durasi di luar toleransi",
            "peak > 1.0 (overshoot MP3)",
            "peak < 0.05 (level sangat rendah)",
            "kegagalan kritis",
        ],
        "jumlah": [
            int(manifest_raw["read_ok"].fillna(False).sum()),
            int((~manifest_raw["read_ok"].fillna(False)).sum()),
            int(manifest_raw["decoded_frames"].fillna(0).gt(0).sum()),
            int(manifest_raw["nan_count"].fillna(0).gt(0).sum()),
            int(manifest_raw["inf_count"].fillna(0).gt(0).sum()),
            int(manifest_raw["all_zero"].sum()),
            int(manifest_raw["duration_status"].eq("tepat_30_detik").sum()),
            int(manifest_raw["duration_status"].ne("tepat_30_detik").sum()),
            int(manifest_raw["peak_over_one"].fillna(False).sum()),
            int(manifest_raw["low_level"].sum()),
            int(manifest_raw["critical_failure"].sum()),
        ],
    }
)

low_level_files = manifest_raw.loc[
    manifest_raw["low_level"],
    ["relative_path", "nim", "label", "take", "peak_abs", "rms", "duration_decoded_s"],
].sort_values("peak_abs")

display(integrity_checks)
display(manifest_raw["duration_decoded_s"].describe().to_frame().T)
display(
    pd.crosstab(manifest_raw["samplerate"], manifest_raw["channels"])
    .rename_axis(index="samplerate", columns="channels")
)

if len(low_level_files):
    display(low_level_files)
else:
    print("Tidak ada file dengan level sangat rendah.")

manifest_raw.to_csv(ARTIFACT_DIR / "manifest_raw.csv", index=False)
integrity_checks.to_csv(ARTIFACT_DIR / "integrity_checks.csv", index=False)
low_level_files.to_csv(ARTIFACT_DIR / "low_level_files.csv", index=False)
print(f"Manifest mentah disimpan: {ARTIFACT_DIR / 'manifest_raw.csv'} ({len(manifest_raw)} baris)")
