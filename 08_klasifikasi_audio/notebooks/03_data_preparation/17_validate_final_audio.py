file_checks = []
for row in transformation_manifest.itertuples():
    final_path = DATA_FINAL_DIR / row.final_relative_path
    mp3_path = DATA_MP3_DIR / row.mp3_relative_path
    y, sr = sf.read(final_path, dtype="float32")
    info = sf.info(final_path)

    checks = {
        "file_ada": final_path.is_file(),
        "mp3_sama_dengan_raw": row.source_sha256 == row.mp3_sha256,
        "mp3_ada": mp3_path.is_file(),
        "sample_rate_16k": sr == SR,
        "mono": y.ndim == 1 and info.channels == 1,
        "pcm16": info.subtype == "PCM_16",
        "tepat_480000": len(y) == TARGET_SAMPLES,
        "durasi_30_detik": abs(len(y) / SR - TARGET_DURATION_S) < 1e-9,
        "tidak_nan": int(np.isnan(y).sum()) == 0,
        "tidak_inf": int(np.isinf(y).sum()) == 0,
        "tidak_kosong": bool(np.any(y != 0)),
        "peak_maksimal_1": float(np.max(np.abs(y))) <= 1.00001,
    }
    file_checks.append(
        {
            "file": row.file,
            "final_relative_path": row.final_relative_path,
            **checks,
            "peak": float(np.max(np.abs(y))),
            "rms": float(np.sqrt(np.mean(y.astype(np.float64) ** 2))),
        }
    )

final_audio_validation = pd.DataFrame(file_checks)
failed_rows = final_audio_validation.loc[
    ~final_audio_validation.drop(columns=["file", "final_relative_path", "peak", "rms"]).all(axis=1)
]
if len(failed_rows):
    raise ValueError(f"Ada file final yang gagal validasi: {len(failed_rows)}")

transition_summary = (
    transformation_manifest.groupby(["duration_action", "label_name"])
    .agg(n_files=("file", "size"), min_peak=("peak_pcm16", "min"), max_peak=("peak_pcm16", "max"))
    .reset_index()
)

display(transition_summary)
display(
    final_audio_validation[["file", "peak", "rms"]]
    .describe(percentiles=[0.5])
    .T.reset_index()
    .rename(columns={"index": "metrik"})
)

final_audio_summary = {
    "n_files": int(len(final_audio_validation)),
    "n_unique_final_hashes": int(transformation_manifest["final_sha256"].nunique()),
    "sample_rate": int(SR),
    "channels": 1,
    "samples_per_file": int(TARGET_SAMPLES),
    "duration_s": float(TARGET_DURATION_S),
    "duration_actions": {
        str(k): int(v)
        for k, v in transformation_manifest["duration_action"].value_counts().items()
    },
    "all_checks_passed": bool(len(failed_rows) == 0),
}
with open(ARTIFACT_DIR / "final_audio_summary.json", "w", encoding="utf-8") as handle:
    json.dump(final_audio_summary, handle, ensure_ascii=False, indent=2)

final_audio_validation.to_csv(ARTIFACT_DIR / "final_audio_validation.csv", index=False)
print("Validasi audio final: PASS")
