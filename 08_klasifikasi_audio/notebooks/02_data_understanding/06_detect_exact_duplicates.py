# Tujuan: mendeteksi duplikat eksak berdasarkan hash SHA-256 tanpa menghapus file apa pun.
# Proses: menghitung hash setiap file, mengelompokkan hash identik, dan menandai duplikat lintas NIM/lintas label.
# Output: tabel duplikat per file, ringkasan grup duplikat, dan statistik duplikasi.

hashed_inventory = inventory.copy()
hashed_inventory["sha256"] = [
    hashlib.sha256((RAW_DIR / rel).read_bytes()).hexdigest()
    for rel in hashed_inventory["relative_path"]
]

hash_groups = hashed_inventory.groupby("sha256", sort=False)
duplicate_group_rows = []
group_ids = {}
group_counter = 0

for sha256, group in sorted(hash_groups, key=lambda item: item[1]["relative_path"].min()):
    if len(group) <= 1:
        continue
    group_counter += 1
    group_id = f"DUP{group_counter:02d}"
    group_ids[sha256] = group_id
    labels = sorted(group["label"].dropna().astype(int).unique().tolist())
    nims = sorted(group["nim"].dropna().unique().tolist())
    takes = sorted(group["take"].dropna().astype(int).unique().tolist())
    if len(labels) > 1:
        scope = "cross_label"
    elif len(nims) > 1:
        scope = "cross_nim"
    else:
        scope = "within_nim"
    duplicate_group_rows.append(
        {
            "duplicate_group_id": group_id,
            "sha256": sha256,
            "n_files": len(group),
            "labels": ", ".join(LABEL_NAME_MAP[label] for label in labels),
            "n_labels": len(labels),
            "nims": ", ".join(nims),
            "n_nims": len(nims),
            "takes": ", ".join(str(take) for take in takes),
            "scope": scope,
            "files": " | ".join(sorted(group["relative_path"].tolist())),
        }
    )

duplicate_groups = pd.DataFrame(duplicate_group_rows)

hashed_inventory["duplicate_group_id"] = hashed_inventory["sha256"].map(group_ids).fillna("")
hashed_inventory["duplicate_group_size"] = hashed_inventory["sha256"].map(
    hashed_inventory["sha256"].value_counts()
).astype(int)
hashed_inventory["is_exact_duplicate"] = hashed_inventory["duplicate_group_size"].gt(1)

scope_map = (
    duplicate_groups.set_index("duplicate_group_id")["scope"].to_dict()
    if len(duplicate_groups)
    else {}
)
hashed_inventory["duplicate_scope"] = hashed_inventory["duplicate_group_id"].map(scope_map).fillna("unique")

duplicate_files = hashed_inventory.loc[
    hashed_inventory["is_exact_duplicate"],
    ["duplicate_group_id", "relative_path", "file", "nim", "label", "take", "duplicate_scope", "sha256"],
].sort_values(["duplicate_group_id", "relative_path"])

duplicate_counts = pd.DataFrame(
    {
        "pemeriksaan": [
            "total file",
            "hash unik",
            "file terlibat duplikat eksak",
            "grup duplikat eksak",
            "grup duplikat lintas NIM",
            "grup duplikat lintas label",
            "grup duplikat dalam NIM yang sama",
        ],
        "jumlah": [
            len(hashed_inventory),
            hashed_inventory["sha256"].nunique(),
            int(hashed_inventory["is_exact_duplicate"].sum()),
            len(duplicate_groups),
            int((duplicate_groups["scope"] == "cross_nim").sum()) if len(duplicate_groups) else 0,
            int((duplicate_groups["scope"] == "cross_label").sum()) if len(duplicate_groups) else 0,
            int((duplicate_groups["scope"] == "within_nim").sum()) if len(duplicate_groups) else 0,
        ],
    }
)

display(duplicate_counts)
if len(duplicate_groups):
    display(duplicate_groups.drop(columns=["sha256", "files"]))
    display(duplicate_files.drop(columns=["sha256"]))
else:
    print("Tidak ada duplikat eksak.")

hashed_inventory.to_csv(ARTIFACT_DIR / "inventory_with_hash.csv", index=False)
duplicate_groups.to_csv(ARTIFACT_DIR / "duplicate_groups.csv", index=False)
duplicate_files.to_csv(ARTIFACT_DIR / "duplicate_files.csv", index=False)
print(f"Tabel duplikat disimpan: {ARTIFACT_DIR / 'duplicate_groups.csv'}")
