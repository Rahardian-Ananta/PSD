class_selection_summary = (
    final_manifest.groupby("label_name")
    .agg(
        n_files=("relative_path", "size"),
        n_nim=("nim", "nunique"),
        n_take_1=("take", lambda values: int((values == 1).sum())),
        n_take_2=("take", lambda values: int((values == 2).sum())),
        n_take_3=("take", lambda values: int((values == 3).sum())),
    )
    .reindex(LABEL_ORDER)
    .reset_index()
)

nim_final_counts = (
    final_manifest.pivot_table(
        index="nim",
        columns="label_name",
        values="relative_path",
        aggfunc="count",
        fill_value=0,
    )
    .rename(columns={"berisik": "n_berisik", "non-berisik": "n_non_berisik"})
)
for column in ["n_berisik", "n_non_berisik"]:
    if column not in nim_final_counts.columns:
        nim_final_counts[column] = 0
nim_final_counts = nim_final_counts[["n_non_berisik", "n_berisik"]]
nim_final_counts["n_files"] = nim_final_counts.sum(axis=1)
nim_final_counts["kedua_kelas"] = (
    nim_final_counts["n_non_berisik"].gt(0) & nim_final_counts["n_berisik"].gt(0)
)
nim_final_counts = nim_final_counts.reset_index().sort_values("nim")

take_coverage = (
    final_manifest.pivot_table(
        index="label_name",
        columns="take",
        values="relative_path",
        aggfunc="count",
        fill_value=0,
    )
    .reindex(LABEL_ORDER)
    .reset_index()
)
for take in [1, 2, 3]:
    if take not in take_coverage.columns:
        take_coverage[take] = 0
take_coverage = take_coverage.rename(columns={1: "take_1", 2: "take_2", 3: "take_3"})

selection_summary = pd.DataFrame(
    {
        "metrik": [
            "file awal",
            "file final",
            "file karantina",
            "NIM awal",
            "NIM final",
            "NIM dua kelas",
            "NIM satu kelas",
            "file berisik final",
            "file non-berisik final",
            "grup duplikat same-label",
            "wakil duplikat dipilih",
        ],
        "nilai": [
            len(manifest),
            len(final_manifest),
            len(quarantine_manifest),
            manifest["nim"].nunique(),
            len(final_nims),
            nims_both,
            len(nims_one),
            int(final_manifest["label"].eq(1).sum()),
            int(final_manifest["label"].eq(0).sum()),
            len(group_choices),
            len(selected_representatives),
        ],
    }
)

display(class_selection_summary)
display(nim_final_counts)
display(take_coverage)
display(selection_summary)

class_selection_summary.to_csv(ARTIFACT_DIR / "class_selection_summary.csv", index=False)
nim_final_counts.to_csv(ARTIFACT_DIR / "nim_selection_summary.csv", index=False)
take_coverage.to_csv(ARTIFACT_DIR / "take_coverage.csv", index=False)
selection_summary.to_csv(ARTIFACT_DIR / "selection_summary.csv", index=False)

print("NIM yang tidak memiliki file final:", ", ".join(search_summary["dropped_nims"]) or "-")
