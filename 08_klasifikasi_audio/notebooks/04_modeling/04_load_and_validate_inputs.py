stage3_validation = json.loads(STAGE3_VALIDATION_PATH.read_text(encoding="utf-8"))
assert stage3_validation["status"] == "PASS", "Validasi Tahap 03 berstatus bukan PASS."
assert (
    stage3_validation["checks_passed"] == stage3_validation["checks_total"]
), "Terdapat pemeriksaan Tahap 03 yang gagal."
assert stage3_validation["n_final"] == 176, "Jumlah file final berubah dari 176."

features = pd.read_csv(FEATURES_PATH)
features["label"] = features["label"].astype(int)
features["take"] = features["take"].astype(int)
features["label_name"] = features["label"].map(LABEL_NAME_MAP)

assert len(features) == 176, f"features.csv berisi {len(features)} baris, bukan 176."
assert list(features.columns[:4]) == IDENTITY_COLUMNS, "Kolom identitas tidak sesuai."
assert set(FEATURE_COLUMNS).issubset(features.columns), "Kolom fitur hilang."
extra_columns = set(features.columns) - set(IDENTITY_COLUMNS + FEATURE_COLUMNS)
assert extra_columns <= {"label_name"}, f"Kolom tak dikenal: {extra_columns}."

feature_values = features[FEATURE_COLUMNS].to_numpy(dtype=float)
assert not features[FEATURE_COLUMNS].isna().any().any(), "features.csv mengandung NaN."
assert np.isfinite(feature_values).all(), "features.csv mengandung Inf."
assert features["file"].is_unique, "Kolom file tidak unik."
assert not features.duplicated(IDENTITY_COLUMNS).any(), "Identitas file/nim/take/label ganda."

class_counts = features["label"].value_counts().to_dict()
assert int(class_counts.get(0, 0)) == 88 and int(class_counts.get(1, 0)) == 88, (
    f"Distribusi kelas berubah: {class_counts}"
)

nims_all = sorted(features["nim"].unique())
assert len(nims_all) == 34, f"Jumlah NIM berubah: {len(nims_all)}"
per_nim_classes = features.groupby("nim")["label"].nunique()
assert (per_nim_classes == 2).all(), "Ada NIM yang tidak memiliki kedua kelas."

selected_features = [
    line.split("|")[-1].strip()
    for line in SELECTED_FEATURES_PATH.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]
assert len(selected_features) == 8, f"Kandidat fitur berjumlah {len(selected_features)}, bukan 8."
assert set(selected_features).issubset(
    set(FEATURE_COLUMNS)
), "Kandidat fitur tidak ada di FEATURE_COLUMNS."

input_summary = pd.DataFrame(
    {
        "pemeriksaan": [
            "status validasi Tahap 03",
            "jumlah pemeriksaan Tahap 03 lulus",
            "baris features.csv",
            "fitur numerik tanpa NaN/Inf",
            "distribusi kelas (0 : 1)",
            "jumlah NIM (semua berdua kelas)",
            "kandidat fitur eksploratif",
        ],
        "nilai": [
            stage3_validation["status"],
            f"{stage3_validation['checks_passed']}/{stage3_validation['checks_total']}",
            len(features),
            f"{len(FEATURE_COLUMNS)} fitur",
            f"{int(class_counts[0])} : {int(class_counts[1])}",
            len(nims_all),
            len(selected_features),
        ],
    }
)
display(input_summary)
print("Pintu masuk Tahap 04: LULUS")
