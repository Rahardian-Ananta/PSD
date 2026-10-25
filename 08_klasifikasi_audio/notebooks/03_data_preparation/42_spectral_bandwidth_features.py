bandwidth_rows = []
for row in transformation_manifest.itertuples():
    y, sr = sf.read(DATA_FINAL_DIR / row.final_relative_path, dtype="float32")
    frames = frame_signal(y).astype(np.float64)
    P = np.abs(np.fft.rfft(frames * hann_window[None, :], n=N_FFT, axis=1)) ** 2
    power_sum = P.sum(axis=1)
    centroids = np.divide(
        P @ FREQS,
        power_sum,
        out=np.zeros_like(power_sum),
        where=power_sum > 0,
    )
    variance = np.divide(
        (P * (FREQS[None, :] - centroids[:, None]) ** 2).sum(axis=1),
        power_sum,
        out=np.zeros_like(power_sum),
        where=power_sum > 0,
    )
    bandwidth_frames = np.sqrt(np.maximum(variance, 0))
    bandwidth_rows.append(
        {
            "file": row.file,
            "spectral_bandwidth_mean": float(np.mean(bandwidth_frames)),
        }
    )

features_bandwidth = pd.DataFrame(bandwidth_rows)
if len(features_bandwidth) != 176 or not np.isfinite(
    features_bandwidth["spectral_bandwidth_mean"]
).all():
    raise ValueError("Fitur spectral bandwidth tidak valid.")
if not (features_bandwidth["spectral_bandwidth_mean"] >= 0).all():
    raise ValueError("Spectral bandwidth bernilai negatif.")
features_bandwidth = features_base.merge(
    features_bandwidth, on="file", validate="one_to_one"
)

display(
    features_bandwidth.groupby("label")[["spectral_bandwidth_mean"]]
    .median()
    .rename(index=LABEL_NAME_MAP)
)
features_bandwidth.to_csv(ARTIFACT_DIR / "features_bandwidth.csv", index=False)
