duplicate_groups = pd.read_csv(DU_ARTIFACT_DIR / "duplicate_groups.csv")
duplicate_groups["duplicate_group_id"] = duplicate_groups["duplicate_group_id"].astype(str)

manifest["sha256_recomputed"] = [
    hashlib.sha256((RAW_DIR / rel).read_bytes()).hexdigest()
    for rel in manifest["relative_path"]
]
if not (manifest["sha256"] == manifest["sha256_recomputed"]).all():
    raise ValueError("Hash SHA-256 tidak konsisten dengan manifest Data Understanding.")

hash_groups = (
    manifest.groupby("sha256")
    .agg(
        n_files=("relative_path", "size"),
        nims=("nim", lambda values: ", ".join(sorted(values.unique()))),
        n_nims=("nim", "nunique"),
        labels=("label", lambda values: ", ".join(str(int(v)) for v in sorted(values.unique()))),
        n_labels=("label", "nunique"),
        files=("relative_path", lambda values: " | ".join(sorted(values))),
    )
    .reset_index()
)
hash_groups = hash_groups.loc[hash_groups["n_files"] > 1].copy()
hash_groups["scope"] = np.where(
    hash_groups["n_labels"] > 1,
    "cross_label",
    np.where(hash_groups["n_nims"] > 1, "cross_nim", "within_nim"),
)

if len(hash_groups) != len(duplicate_groups):
    raise ValueError("Jumlah grup duplikat tidak konsisten dengan Tahap 02.")

expected_duplicate = manifest["sha256"].map(hash_groups.set_index("sha256")["n_files"]).fillna(1).gt(1)
if not (expected_duplicate == manifest["is_exact_duplicate"]).all():
    raise ValueError("Penandaan file duplikat tidak konsisten.")

scope_counts = (
    hash_groups["scope"]
    .value_counts()
    .rename_axis("scope")
    .reset_index(name="n_groups")
)
scope_counts["n_files"] = scope_counts["scope"].map(
    hash_groups.groupby("scope")["n_files"].sum()
).astype(int)

display(
    pd.DataFrame(
        {
            "pemeriksaan": [
                "total file",
                "hash unik",
                "file terlibat duplikat",
                "grup duplikat",
                "grup lintas label",
                "grup lintas NIM",
                "grup dalam NIM sama",
            ],
            "nilai": [
                len(manifest),
                manifest["sha256"].nunique(),
                int(manifest["is_exact_duplicate"].sum()),
                len(hash_groups),
                int(hash_groups["scope"].eq("cross_label").sum()),
                int(hash_groups["scope"].eq("cross_nim").sum()),
                int(hash_groups["scope"].eq("within_nim").sum()),
            ],
        }
    )
)
display(scope_counts)
display(
    hash_groups.loc[
        hash_groups["scope"] == "cross_label",
        ["files", "nims", "labels", "n_files"],
    ]
)

hash_groups.to_csv(ARTIFACT_DIR / "duplicate_audit.csv", index=False)
