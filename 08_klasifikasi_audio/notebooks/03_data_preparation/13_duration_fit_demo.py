def fit_duration_to_target(y, target_samples=TARGET_SAMPLES):
    y = np.asarray(y)
    original_samples = int(len(y))
    crop_start = 0
    pad_left = 0
    pad_right = 0

    if original_samples > target_samples:
        action = "crop"
        crop_start = (original_samples - target_samples) // 2
        y_out = y[crop_start : crop_start + target_samples].copy()
    elif original_samples < target_samples:
        action = "pad"
        total_pad = target_samples - original_samples
        pad_left = total_pad // 2
        pad_right = total_pad - pad_left
        y_out = np.pad(y, (pad_left, pad_right), mode="constant", constant_values=0.0)
    else:
        action = "none"
        y_out = y.copy()

    if len(y_out) != target_samples:
        raise ValueError("Panjang sinyal tidak sama dengan target sampel.")

    return y_out, {
        "original_samples_16k": original_samples,
        "original_duration_16k_s": original_samples / SR,
        "action": action,
        "crop_start": int(crop_start),
        "pad_left": int(pad_left),
        "pad_right": int(pad_right),
        "final_samples": int(len(y_out)),
    }


staging_meta = staging_manifest.merge(
    manifest[["relative_path", "samplerate", "channels"]],
    left_on="source_relative_path",
    right_on="relative_path",
    how="left",
    validate="one_to_one",
)
preview_rows = (
    staging_meta.sort_values("source_relative_path")
    .groupby("samplerate", sort=True)
    .head(1)
)

duration_preview = []
for row in preview_rows.itertuples():
    y_preview, preview_sr = librosa.load(
        DATA_MP3_DIR / row.mp3_relative_path, sr=SR, mono=True
    )
    if preview_sr != SR:
        raise ValueError("librosa tidak mengembalikan sample rate yang diminta.")
    _, preview_meta = fit_duration_to_target(y_preview)
    duration_preview.append(
        {
            "file": row.file_mp3,
            "source_samplerate": int(row.samplerate),
            "source_channels": int(row.channels),
            "decoded_samples_16k": len(y_preview),
            "decoded_duration_16k_s": len(y_preview) / SR,
            "action": preview_meta["action"],
            "final_samples": preview_meta["final_samples"],
        }
    )

duration_preview = pd.DataFrame(duration_preview)
display(duration_preview)
