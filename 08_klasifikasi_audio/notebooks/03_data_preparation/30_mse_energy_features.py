features_base = transformation_manifest[["file", "nim", "take", "label"]].copy()
features_mse = features_base.copy()
mse_values = []

for row in transformation_manifest.itertuples():
    y, sr = sf.read(DATA_FINAL_DIR / row.final_relative_path, dtype="float32")
    if sr != SR or len(y) != TARGET_SAMPLES:
        raise ValueError(f"File tidak sesuai kontrak: {row.file}")
    mse_values.append(float(np.mean(y.astype(np.float64) ** 2)))

features_mse["mse_energy"] = mse_values
if not np.isfinite(features_mse["mse_energy"]).all():
    raise ValueError("MSE mengandung NaN atau Inf.")

display(
    features_mse.groupby("label")
    .agg(
        n=("mse_energy", "size"),
        mean=("mse_energy", "mean"),
        median=("mse_energy", "median"),
        min=("mse_energy", "min"),
        max=("mse_energy", "max"),
    )
    .rename(index=LABEL_NAME_MAP)
)

features_mse.to_csv(ARTIFACT_DIR / "features_mse.csv", index=False)
