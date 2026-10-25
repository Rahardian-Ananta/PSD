feature_parts = [
    features_mse,
    features_rms,
    features_zcr,
    features_centroid,
    features_flatness,
    features_rolloff,
    features_bandwidth,
]
features = reduce(
    lambda left, right: left.merge(right, on=["file", "nim", "take", "label"], validate="one_to_one"),
    feature_parts,
)
features = features[IDENTITY_COLUMNS + FEATURE_COLUMNS].copy()
features = features.sort_values(["nim", "label", "take"]).reset_index(drop=True)

if len(features) != 176:
    raise ValueError(f"features.csv harus 176 baris, ditemukan {len(features)}.")
if features["file"].duplicated().any():
    raise ValueError("Ada file duplikat di features.csv.")
if list(features.columns) != IDENTITY_COLUMNS + FEATURE_COLUMNS:
    raise ValueError("Urutan kolom features.csv tidak sesuai kontrak.")
if features[FEATURE_COLUMNS].isna().any().any():
    raise ValueError("features.csv mengandung nilai kosong.")
if not np.isfinite(features[FEATURE_COLUMNS].to_numpy(dtype=np.float64)).all():
    raise ValueError("features.csv mengandung NaN atau Inf.")

display(features.head(8))
display(
    features.groupby("label")[FEATURE_COLUMNS]
    .median()
    .rename(index=LABEL_NAME_MAP)
    .T.rename(columns=LABEL_NAME_MAP)
)

features.to_csv(ARTIFACT_ROOT / "features.csv", index=False)
(
    features.groupby("label")[FEATURE_COLUMNS]
    .agg(["mean", "std", "median", "min", "max"])
    .T.to_csv(ARTIFACT_DIR / "feature_summary_by_class.csv")
)

print(f"features.csv: {ARTIFACT_ROOT / 'features.csv'}")
print(f"Bentuk: {features.shape}; 12 fitur + 4 kolom identitas")
