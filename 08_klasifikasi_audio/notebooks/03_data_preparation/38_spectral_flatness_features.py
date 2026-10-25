flatness_rows = []
for row in transformation_manifest.itertuples():
    y, sr = sf.read(DATA_FINAL_DIR / row.final_relative_path, dtype="float32")
    frames = frame_signal(y).astype(np.float64)
    P = np.abs(np.fft.rfft(frames * hann_window[None, :], n=N_FFT, axis=1)) ** 2
    P_eps = P + EPS
    flatness_frames = np.exp(np.mean(np.log(P_eps), axis=1)) / np.mean(P_eps, axis=1)
    flatness_frames[P.sum(axis=1) == 0] = 0
    flatness_rows.append(
        {
            "file": row.file,
            "spectral_flatness_mean": float(np.mean(flatness_frames)),
        }
    )

features_flatness = pd.DataFrame(flatness_rows)
if len(features_flatness) != 176 or not np.isfinite(
    features_flatness["spectral_flatness_mean"]
).all():
    raise ValueError("Fitur spectral flatness tidak valid.")
if not features_flatness["spectral_flatness_mean"].between(0, 1).all():
    raise ValueError("Spectral flatness berada di luar rentang [0, 1].")
features_flatness = features_base.merge(
    features_flatness, on="file", validate="one_to_one"
)

display(
    features_flatness.groupby("label")[["spectral_flatness_mean"]]
    .median()
    .rename(index=LABEL_NAME_MAP)
)
features_flatness.to_csv(ARTIFACT_DIR / "features_flatness.csv", index=False)
