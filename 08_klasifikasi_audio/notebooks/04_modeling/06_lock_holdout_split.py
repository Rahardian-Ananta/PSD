nims_all_array = np.array(nims_all)

holdout_splitter = GroupShuffleSplit(
    n_splits=1, test_size=TEST_SIZE, random_state=RANDOM_STATE
)
train_nim_idx, test_nim_idx = next(
    holdout_splitter.split(np.zeros(len(nims_all_array)), groups=nims_all_array)
)
nims_train = sorted(nims_all_array[train_nim_idx].tolist())
nims_test = sorted(nims_all_array[test_nim_idx].tolist())

expected_n_test = int(np.ceil(TEST_SIZE * len(nims_all_array)))
assert len(nims_test) == expected_n_test, (
    f"NIM test {len(nims_test)} tidak sama dengan pembulatan {expected_n_test}."
)
assert set(nims_train).isdisjoint(set(nims_test)), "NIM train dan test beririsan."
assert set(nims_train) | set(nims_test) == set(nims_all), "NIM train + test tidak menutup semua NIM."

features["split"] = np.where(features["nim"].isin(nims_test), "test", "train")
assert set(features.loc[features["split"] == "train", "nim"]) == set(nims_train)
assert set(features.loc[features["split"] == "test", "nim"]) == set(nims_test)

holdout_split = (
    features.groupby(["nim", "split"])
    .agg(
        n_files=("file", "size"),
        n_class_0=("label", lambda values: int((values == 0).sum())),
        n_class_1=("label", lambda values: int((values == 1).sum())),
    )
    .reset_index()
    .sort_values(["split", "nim"])
    .reset_index(drop=True)
)
holdout_split.to_csv(HOLDOUT_SPLIT_PATH, index=False)

holdout_file_split = features[IDENTITY_COLUMNS + ["split"]].copy()
holdout_file_split.to_csv(HOLDOUT_FILE_PATH, index=False)

split_summary = (
    features.groupby("split")
    .agg(
        n_files=("file", "size"),
        n_nim=("nim", "nunique"),
        n_class_0=("label", lambda values: int((values == 0).sum())),
        n_class_1=("label", lambda values: int((values == 1).sum())),
    )
    .reindex(["train", "test"])
)
display(split_summary)

classes_per_nim = features.groupby(["nim", "split"])["label"].nunique()
assert (classes_per_nim == 2).all(), "Ada NIM yang kehilangan satu kelas pada salah satu sisi split."

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
class_by_split = split_summary[["n_class_0", "n_class_1"]].rename(
    columns={"n_class_0": "non-berisik", "n_class_1": "berisik"}
)
class_by_split.plot(kind="bar", ax=axes[0], color=["#457b9d", "#e76f51"])
axes[0].set_title("Jumlah file per kelas")
axes[0].set_xlabel("split")
axes[0].set_ylabel("jumlah file")
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)
axes[0].legend(title="kelas")

split_summary["n_nim"].plot(kind="bar", ax=axes[1], color="#2a9d8f")
axes[1].set_title("Jumlah NIM per split")
axes[1].set_xlabel("split")
axes[1].set_ylabel("jumlah NIM")
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)
fig.tight_layout()
fig.savefig(FIGURE_DIR / "holdout_composition.png")
plt.show()

print(f"NIM train ({len(nims_train)}): {', '.join(nims_train)}")
print(f"NIM test  ({len(nims_test)}): {', '.join(nims_test)}")
