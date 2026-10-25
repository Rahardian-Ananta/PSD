# Tujuan: memvalidasi identitas NIM, take, label, dan kelengkapan protokol 6 file per NIM.
# Proses: menghitung NIM unik, distribusi kelas/take, kombinasi yang hilang, dan benturan identitas.
# Output: tabel pemeriksaan identitas, daftar take yang hilang, dan ringkasan per NIM.

valid_identity = inventory.loc[inventory["name_parse_ok"] & inventory["label"].notna()].copy()
valid_identity["label"] = valid_identity["label"].astype(int)
valid_identity["take"] = valid_identity["take"].astype(int)

nim_values = sorted(valid_identity["nim"].dropna().unique())
expected_index = pd.MultiIndex.from_product(
    [nim_values, [0, 1], [1, 2, 3]],
    names=["nim", "label", "take"],
)
actual_index = pd.MultiIndex.from_frame(valid_identity[["nim", "label", "take"]])
missing_index = expected_index.difference(actual_index)

missing_takes = missing_index.to_frame(index=False)
missing_takes["label_name"] = missing_takes["label"].map(LABEL_NAME_MAP)
missing_takes = missing_takes.sort_values(["nim", "label", "take"]).reset_index(drop=True)

files_per_nim = valid_identity.groupby("nim").size().rename("jumlah_file")
incomplete_nims = files_per_nim.loc[files_per_nim != 6]
missing_per_nim = missing_takes.groupby("nim").size().rename("take_hilang")

nim_class_matrix = (
    valid_identity.pivot_table(index="nim", columns="label", values="relative_path", aggfunc="count", fill_value=0)
    .rename(columns=LABEL_NAME_MAP)
)
nim_class_matrix["total"] = nim_class_matrix.sum(axis=1)
nim_class_matrix["take_hilang"] = missing_per_nim.reindex(nim_class_matrix.index).fillna(0).astype(int)
nim_class_matrix["lengkap_6_file"] = nim_class_matrix["total"].eq(6)

identity_checks = pd.DataFrame(
    {
        "pemeriksaan": [
            "total file",
            "path unik",
            "nama file unik",
            "NIM unik",
            "nama file gagal diparse",
            "label folder vs nama tidak cocok",
            "identitas NIM-label-take duplikat",
            "NIM hanya memiliki satu kelas",
            "NIM dengan jumlah file != 6",
            "kombinasi NIM-kelas-take hilang",
            "file jika semua NIM lengkap 6 file",
            "persentase kelengkapan terhadap 6 file/NIM",
        ],
        "nilai": [
            len(inventory),
            inventory["relative_path"].nunique(),
            inventory["file"].nunique(),
            len(nim_values),
            int((~inventory["name_parse_ok"]).sum()),
            int((~inventory["label_match"]).sum()),
            int(valid_identity.duplicated(["nim", "label", "take"], keep=False).sum()),
            int((nim_class_matrix[["berisik", "non-berisik"]] == 0).any(axis=1).sum()),
            int((files_per_nim != 6).sum()),
            int(len(missing_takes)),
            int(len(nim_values) * 6),
            f"{len(valid_identity) / (len(nim_values) * 6) * 100:.2f}%",
        ],
    }
)

display(identity_checks)
display(valid_identity.groupby(["label", "take"]).size().unstack(fill_value=0).rename(index=LABEL_NAME_MAP))
display(files_per_nim.value_counts().sort_index().rename_axis("file_per_NIM").reset_index(name="jumlah_NIM"))
display(nim_class_matrix)

if len(missing_takes):
    print(f"Take yang hilang: {len(missing_takes)} kombinasi pada {missing_takes['nim'].nunique()} NIM")
    display(missing_takes)
else:
    print("Semua kombinasi NIM-kelas-take lengkap.")

missing_takes.to_csv(ARTIFACT_DIR / "missing_takes.csv", index=False)
nim_class_matrix.reset_index().to_csv(ARTIFACT_DIR / "nim_class_matrix.csv", index=False)
print(f"Daftar take hilang disimpan: {ARTIFACT_DIR / 'missing_takes.csv'}")
