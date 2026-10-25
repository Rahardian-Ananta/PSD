rms_rows = []
for row in transformation_manifest.itertuples():
    y, sr = sf.read(DATA_FINAL_DIR / row.final_relative_path, dtype="float32")
    frames = frame_signal(y).astype(np.float64)
    rms_frames = np.sqrt(np.mean(frames**2, axis=1))
    rms_rows.append(
        {
            "file": row.file,
            "rms_mean": float(np.mean(rms_frames)),
            "rms_std": float(np.std(rms_frames, ddof=0)),
            "rms_max": float(np.max(rms_frames)),
            "rms_min": float(np.min(rms_frames)),
        }
    )

features_rms = pd.DataFrame(rms_rows)
if len(features_rms) != 176 or not np.isfinite(features_rms.iloc[:, 1:]).all().all():
    raise ValueError("Fitur RMS tidak valid.")
features_rms = features_base.merge(features_rms, on="file", validate="one_to_one")

display(
    features_rms.groupby("label")[
        ["rms_mean", "rms_std", "rms_max", "rms_min"]
    ].median().rename(index=LABEL_NAME_MAP)
)
features_rms.to_csv(ARTIFACT_DIR / "features_rms.csv", index=False)
