centroid_rows = []
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
    centroid_rows.append(
        {
            "file": row.file,
            "spectral_centroid_mean": float(np.mean(centroids)),
            "spectral_centroid_std": float(np.std(centroids, ddof=0)),
            "empty_power_frames": int((power_sum == 0).sum()),
        }
    )

features_centroid = pd.DataFrame(centroid_rows)
if len(features_centroid) != 176 or not np.isfinite(
    features_centroid[["spectral_centroid_mean", "spectral_centroid_std"]]
).all().all():
    raise ValueError("Fitur spectral centroid tidak valid.")
silent_frame_audit = features_centroid[["file", "empty_power_frames"]].copy()
features_centroid = features_base.merge(
    features_centroid.drop(columns=["empty_power_frames"]), on="file", validate="one_to_one"
)

display(
    features_centroid.groupby("label")[
        ["spectral_centroid_mean", "spectral_centroid_std"]
    ].median().rename(index=LABEL_NAME_MAP)
)
print(
    "Frame dengan daya nol:",
    int(silent_frame_audit["empty_power_frames"].sum()),
    "pada",
    int((silent_frame_audit["empty_power_frames"] > 0).sum()),
    "file; centroid frame tersebut ditetapkan 0.",
)
features_centroid.to_csv(ARTIFACT_DIR / "features_centroid.csv", index=False)
silent_frame_audit.to_csv(ARTIFACT_DIR / "silent_frames.csv", index=False)
