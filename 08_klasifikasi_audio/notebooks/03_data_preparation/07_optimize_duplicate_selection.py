def popcount64(values):
    values = np.asarray(values, dtype=np.uint64)
    if hasattr(np, "bitwise_count"):
        return np.bitwise_count(values).astype(np.int16)
    return (
        np.unpackbits(values.view(np.uint8), axis=-1, bitorder="little")
        .sum(axis=-1)
        .astype(np.int16)
    )


same_label_group_ids = sorted(
    manifest.loc[
        (manifest["duplicate_group_id"] != "")
        & (manifest["duplicate_scope"] != "cross_label"),
        "duplicate_group_id",
    ].unique()
)
group_choices = []
for group_id in same_label_group_ids:
    group = manifest.loc[
        manifest["duplicate_group_id"] == group_id
    ].sort_values("relative_path")
    if group["label"].nunique() != 1:
        raise ValueError(f"Grup same-label {group_id} memiliki lebih dari satu label.")
    group_choices.append(group)

nims = sorted(manifest["nim"].unique())
nim_bit = {nim: np.uint64(1) << np.uint64(index) for index, nim in enumerate(nims)}
unique_files = manifest.loc[~manifest["is_exact_duplicate"]].copy()

base_pos = np.uint64(0)
base_neg = np.uint64(0)
for row in unique_files.itertuples():
    if int(row.label) == 1:
        base_pos |= nim_bit[row.nim]
    else:
        base_neg |= nim_bit[row.nim]

choice_pos = []
choice_neg = []
for group in group_choices:
    bits = np.array([nim_bit[nim] for nim in group["nim"]], dtype=np.uint64)
    pos_bits = np.where(group["label"].to_numpy() == 1, bits, np.uint64(0))
    neg_bits = np.where(group["label"].to_numpy() == 0, bits, np.uint64(0))
    choice_pos.append(pos_bits)
    choice_neg.append(neg_bits)

dimensions = tuple(len(group) for group in group_choices)
grid = np.indices(dimensions).reshape(len(dimensions), -1).T.astype(np.int16)
n_combinations = len(grid)

pos_union = np.full(n_combinations, base_pos, dtype=np.uint64)
neg_union = np.full(n_combinations, base_neg, dtype=np.uint64)
for index in range(len(group_choices)):
    choice_index = grid[:, index]
    pos_union |= choice_pos[index][choice_index]
    neg_union |= choice_neg[index][choice_index]

both = popcount64(pos_union & neg_union)
one_class = popcount64(pos_union ^ neg_union)
represented = popcount64(pos_union | neg_union)
score = (
    both.astype(np.int64) * 1_000_000
    - one_class.astype(np.int64) * 10_000
    + represented.astype(np.int64) * 100
)
best_index = int(np.argmax(score))
best_choices = grid[best_index].astype(int)

selected_representatives = [
    group_choices[index].iloc[best_choices[index]]
    for index in range(len(group_choices))
]
selected_paths = {row["relative_path"] for row in selected_representatives}

selection = manifest.copy()
selection["selection_status"] = "quarantine"
selection["selection_reason"] = "duplikat_sama_label_bukan_wakil"
selection.loc[~selection["is_exact_duplicate"], "selection_status"] = "final"
selection.loc[~selection["is_exact_duplicate"], "selection_reason"] = "hash_unik"
selection.loc[
    selection["relative_path"].isin(selected_paths), "selection_status"
] = "final"
selection.loc[
    selection["relative_path"].isin(selected_paths), "selection_reason"
] = "wakil_grup_duplikat_sama_label"
selection.loc[
    selection["duplicate_scope"] == "cross_label", "selection_reason"
] = "duplikat_lintas_label"

final_manifest = selection.loc[selection["selection_status"] == "final"].copy()
final_manifest = final_manifest.sort_values(["nim", "label", "take"]).reset_index(drop=True)
quarantine_manifest = selection.loc[
    selection["selection_status"] == "quarantine"
].copy()

final_class_counts = final_manifest["label"].value_counts().sort_index().to_dict()
final_nims = sorted(final_manifest["nim"].unique())
nim_class_counts = final_manifest.groupby(["nim", "label"]).size().unstack(fill_value=0)
for label in [0, 1]:
    if label not in nim_class_counts.columns:
        nim_class_counts[label] = 0
nims_both = int(((nim_class_counts[0] > 0) & (nim_class_counts[1] > 0)).sum())
nims_one = sorted(
    nim_class_counts.index[
        (nim_class_counts[0] == 0) | (nim_class_counts[1] == 0)
    ].tolist()
)

if len(final_manifest) != 176:
    raise ValueError(f"Jumlah file final {len(final_manifest)}, bukan 176.")
if len(final_nims) != 34:
    raise ValueError(f"Jumlah NIM final {len(final_nims)}, bukan 34.")
if final_class_counts.get(1, 0) != 88 or final_class_counts.get(0, 0) != 88:
    raise ValueError(f"Distribusi kelas final tidak seimbang: {final_class_counts}.")
if nims_one:
    raise ValueError(f"Masih ada NIM satu kelas: {nims_one}.")
if not final_manifest["sha256"].is_unique:
    raise ValueError("File final masih memiliki hash duplikat.")

resolution_rows = []
for index, group in enumerate(group_choices):
    chosen = selected_representatives[index]
    resolution_rows.append(
        {
            "duplicate_group_id": group.iloc[0]["duplicate_group_id"],
            "label_name": LABEL_NAME_MAP[int(group.iloc[0]["label"])],
            "n_candidates": len(group),
            "candidates": " | ".join(group["relative_path"].tolist()),
            "selected": chosen["relative_path"],
            "selected_nim": chosen["nim"],
            "selected_take": int(chosen["take"]),
        }
    )
duplicate_resolution = pd.DataFrame(resolution_rows)

search_summary = {
    "n_same_label_groups": len(group_choices),
    "n_search_combinations": int(n_combinations),
    "best_both_class_nims": int(both[best_index]),
    "best_represented_nims": int(represented[best_index]),
    "best_one_class_nims": int(one_class[best_index]),
    "final_files": int(len(final_manifest)),
    "final_unique_hashes": int(final_manifest["sha256"].nunique()),
    "final_nims": int(len(final_nims)),
    "final_class_counts": {str(k): int(v) for k, v in final_class_counts.items()},
    "quarantined_files": int(len(quarantine_manifest)),
    "dropped_nims": sorted(set(manifest["nim"]) - set(final_nims)),
}

display(
    pd.DataFrame(
        {
            "metrik": [
                "kombinasi yang dievaluasi",
                "NIM dua kelas pada solusi terbaik",
                "NIM terwakili pada solusi terbaik",
                "NIM satu kelas pada solusi terbaik",
                "file final",
                "file karantina",
                "NIM final",
                "NIM hilang",
            ],
            "nilai": [
                n_combinations,
                search_summary["best_both_class_nims"],
                search_summary["best_represented_nims"],
                search_summary["best_one_class_nims"],
                len(final_manifest),
                len(quarantine_manifest),
                len(final_nims),
                ", ".join(search_summary["dropped_nims"]) or "-",
            ],
        }
    )
)
display(duplicate_resolution)
display(nim_class_counts.rename(columns={0: "non_berisik", 1: "berisik"}))

selection.to_csv(ARTIFACT_DIR / "selection_manifest_all.csv", index=False)
final_manifest.to_csv(ARTIFACT_DIR / "final_selection.csv", index=False)
quarantine_manifest.to_csv(ARTIFACT_DIR / "quarantine_manifest.csv", index=False)
duplicate_resolution.to_csv(ARTIFACT_DIR / "duplicate_resolution.csv", index=False)
with open(ARTIFACT_DIR / "duplicate_selection_summary.json", "w", encoding="utf-8") as handle:
    json.dump(search_summary, handle, ensure_ascii=False, indent=2)
