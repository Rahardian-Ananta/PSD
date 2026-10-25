def peak_normalize(y, target_peak=TARGET_PEAK):
    y = np.asarray(y)
    if y.size == 0:
        raise ValueError("Sinyal kosong tidak dapat dinormalisasi.")
    if not np.isfinite(y).all():
        raise ValueError("Sinyal mengandung NaN atau Inf.")
    peak_before = float(np.max(np.abs(y)))
    if peak_before <= 0:
        raise ValueError("Peak sinyal nol; file harus ditolak, bukan dinormalisasi.")
    y_norm = (y / peak_before * target_peak).astype(np.float32)
    peak_after = float(np.max(np.abs(y_norm)))
    return y_norm, {
        "peak_before": peak_before,
        "peak_after": peak_after,
        "target_peak": float(target_peak),
    }


example_row = staging_manifest.sort_values("mp3_relative_path").iloc[0]
example_y, example_sr = librosa.load(
    DATA_MP3_DIR / example_row["mp3_relative_path"], sr=SR, mono=True
)
example_fitted, example_fit_meta = fit_duration_to_target(example_y)
example_normalized, example_peak_meta = peak_normalize(example_fitted)

display(
    pd.DataFrame(
        {
            "pemeriksaan": [
                "file contoh",
                "sample rate",
                "sampel setelah fit durasi",
                "peak sebelum normalisasi",
                "peak setelah normalisasi",
                "target peak",
                "NaN",
                "Inf",
            ],
            "nilai": [
                example_row["file_mp3"],
                example_sr,
                len(example_fitted),
                example_peak_meta["peak_before"],
                example_peak_meta["peak_after"],
                example_peak_meta["target_peak"],
                int(np.isnan(example_normalized).sum()),
                int(np.isinf(example_normalized).sum()),
            ],
        }
    )
)
