zcr_rows = []
for row in transformation_manifest.itertuples():
    y, sr = sf.read(DATA_FINAL_DIR / row.final_relative_path, dtype="float32")
    frames = frame_signal(y).astype(np.float64)
    zcr_frames = np.mean((frames[:, :-1] * frames[:, 1:]) < 0, axis=1)
    zcr_rows.append(
        {
            "file": row.file,
            "zcr_mean": float(np.mean(zcr_frames)),
            "zcr_std": float(np.std(zcr_frames, ddof=0)),
        }
    )

features_zcr = pd.DataFrame(zcr_rows)
if len(features_zcr) != 176 or not np.isfinite(features_zcr.iloc[:, 1:]).all().all():
    raise ValueError("Fitur ZCR tidak valid.")
features_zcr = features_base.merge(features_zcr, on="file", validate="one_to_one")

display(
    features_zcr.groupby("label")[["zcr_mean", "zcr_std"]]
    .median()
    .rename(index=LABEL_NAME_MAP)
)
features_zcr.to_csv(ARTIFACT_DIR / "features_zcr.csv", index=False)
