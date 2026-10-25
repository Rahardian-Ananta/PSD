conversion_meta = staging_meta.merge(
    manifest[["relative_path", "duration_decoded_s"]].rename(
        columns={"relative_path": "source_relative_path"}
    ),
    on="source_relative_path",
    how="left",
    validate="one_to_one",
)

transformation_rows = []
for row in conversion_meta.sort_values("mp3_relative_path").itertuples():
    mp3_path = DATA_MP3_DIR / row.mp3_relative_path
    final_relative_path = Path(row.mp3_relative_path).with_suffix(".wav").as_posix()
    final_path = DATA_FINAL_DIR / final_relative_path
    final_path.parent.mkdir(parents=True, exist_ok=True)

    y, loaded_sr = librosa.load(mp3_path, sr=SR, mono=True)
    if loaded_sr != SR:
        raise ValueError(f"Sample rate hasil dekode bukan 16 kHz: {mp3_path}")

    y_fit, fit_meta = fit_duration_to_target(y)
    y_norm, peak_meta = peak_normalize(y_fit)
    sf.write(final_path, y_norm, SR, subtype="PCM_16")

    info = sf.info(final_path)
    y_written, written_sr = sf.read(final_path, dtype="float32")
    if written_sr != SR:
        raise ValueError(f"Sample rate WAV salah: {final_path}")
    if info.frames != TARGET_SAMPLES:
        raise ValueError(f"Jumlah sampel WAV salah: {final_path}")
    if info.channels != 1:
        raise ValueError(f"Jumlah kanal WAV salah: {final_path}")
    if info.subtype != "PCM_16":
        raise ValueError(f"Subtype WAV salah: {final_path}")

    transformation_rows.append(
        {
            "file": Path(final_relative_path).name,
            "nim": row.nim,
            "take": int(row.take),
            "label": int(row.label),
            "label_name": row.label_name,
            "source_relative_path": row.source_relative_path,
            "mp3_relative_path": row.mp3_relative_path,
            "final_relative_path": final_relative_path,
            "source_sha256": row.sha256,
            "mp3_sha256": hashlib.sha256(mp3_path.read_bytes()).hexdigest(),
            "final_sha256": hashlib.sha256(final_path.read_bytes()).hexdigest(),
            "source_samplerate": int(row.samplerate),
            "source_channels": int(row.channels),
            "source_duration_s": float(row.duration_decoded_s),
            "loaded_sr": int(loaded_sr),
            "decoded_samples_16k": int(len(y)),
            "decoded_duration_16k_s": float(len(y) / SR),
            "duration_action": fit_meta["action"],
            "crop_start": fit_meta["crop_start"],
            "pad_left": fit_meta["pad_left"],
            "pad_right": fit_meta["pad_right"],
            "final_samples": int(info.frames),
            "final_format": info.format,
            "final_subtype": info.subtype,
            "final_channels": int(info.channels),
            "final_samplerate": int(info.samplerate),
            "peak_before_norm": peak_meta["peak_before"],
            "peak_after_norm": peak_meta["peak_after"],
            "peak_pcm16": float(np.max(np.abs(y_written))),
            "target_peak": peak_meta["target_peak"],
            "normalization_applied": True,
            "status": "ok",
        }
    )

transformation_manifest = pd.DataFrame(transformation_rows)
expected_wav_paths = set(transformation_manifest["final_relative_path"])
actual_wav_paths = {
    path.relative_to(DATA_FINAL_DIR).as_posix()
    for path in DATA_FINAL_DIR.rglob("*")
    if path.is_file()
}
if actual_wav_paths != expected_wav_paths:
    extra = sorted(actual_wav_paths - expected_wav_paths)
    missing = sorted(expected_wav_paths - actual_wav_paths)
    raise ValueError(f"Struktur data_final tidak sesuai. Ekstra: {extra}; hilang: {missing}")

if len(transformation_manifest) != 176:
    raise ValueError("Jumlah file hasil konversi bukan 176.")
if not transformation_manifest["final_sha256"].is_unique:
    raise ValueError("Ada WAV final dengan hash identik.")

with open(ARTIFACT_DIR / "preprocessing_contract.json", "w", encoding="utf-8") as handle:
    json.dump(PREPROCESSING_CONTRACT, handle, ensure_ascii=False, indent=2)

display(
    transformation_manifest.groupby(["duration_action", "label_name"])
    .agg(
        n_files=("file", "size"),
        min_samples=("final_samples", "min"),
        max_samples=("final_samples", "max"),
        min_peak=("peak_pcm16", "min"),
        max_peak=("peak_pcm16", "max"),
    )
    .reset_index()
)
print(f"File WAV final: {len(transformation_manifest)}")
print(f"Total ukuran WAV: {sum((DATA_FINAL_DIR / p).stat().st_size for p in expected_wav_paths) / 1024**2:.2f} MB")

transformation_manifest.to_csv(ARTIFACT_DIR / "transformation_manifest.csv", index=False)
