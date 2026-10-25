rolloff_rows = []
for row in transformation_manifest.itertuples():
    y, sr = sf.read(DATA_FINAL_DIR / row.final_relative_path, dtype="float32")
    frames = frame_signal(y).astype(np.float64)
    P = np.abs(np.fft.rfft(frames * hann_window[None, :], n=N_FFT, axis=1)) ** 2
    cumulative = np.cumsum(P, axis=1)
    total_power = cumulative[:, -1]
    thresholds = ROLLOFF_PERCENT * total_power
    rolloff_indices = np.argmax(cumulative >= thresholds[:, None], axis=1)
    rolloff_frames = FREQS[rolloff_indices].copy()
    rolloff_frames[total_power == 0] = 0
    rolloff_rows.append(
        {
            "file": row.file,
            "spectral_rolloff_mean": float(np.mean(rolloff_frames)),
        }
    )

features_rolloff = pd.DataFrame(rolloff_rows)
if len(features_rolloff) != 176 or not np.isfinite(
    features_rolloff["spectral_rolloff_mean"]
).all():
    raise ValueError("Fitur spectral rolloff tidak valid.")
if not features_rolloff["spectral_rolloff_mean"].between(0, SR / 2).all():
    raise ValueError("Spectral rolloff berada di luar rentang frekuensi.")
features_rolloff = features_base.merge(
    features_rolloff, on="file", validate="one_to_one"
)

display(
    features_rolloff.groupby("label")[["spectral_rolloff_mean"]]
    .median()
    .rename(index=LABEL_NAME_MAP)
)
features_rolloff.to_csv(ARTIFACT_DIR / "features_rolloff.csv", index=False)
