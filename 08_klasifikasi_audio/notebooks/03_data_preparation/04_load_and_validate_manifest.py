manifest = pd.read_csv(DU_ARTIFACT_DIR / "manifest_raw.csv")
manifest["label"] = manifest["label"].astype(int)
manifest["take"] = manifest["take"].astype(int)
manifest["duplicate_group_id"] = manifest["duplicate_group_id"].fillna("").astype(str)
manifest["label_name"] = manifest["label"].map(LABEL_NAME_MAP)

required_columns = [
    "relative_path",
    "file",
    "nim",
    "take",
    "label",
    "sha256",
    "duplicate_group_id",
    "is_exact_duplicate",
    "duplicate_scope",
    "read_ok",
    "critical_failure",
]
missing_columns = [column for column in required_columns if column not in manifest.columns]
if missing_columns:
    raise ValueError(f"Kolom wajib tidak ditemukan: {missing_columns}")

checks = {
    "jumlah_file_200": len(manifest) == 200,
    "relatif_path_unik": manifest["relative_path"].is_unique,
    "identitas_lengkap": manifest[["nim", "take", "label"]].notna().all().all(),
    "label_valid_0_1": manifest["label"].isin([0, 1]).all(),
    "nama_file_terurai": manifest["name_parse_ok"].fillna(False).all(),
    "semua_file_terbaca": manifest["read_ok"].fillna(False).all(),
    "tidak_ada_kegagalan_kritis": not manifest["critical_failure"].fillna(True).any(),
    "tidak_ada_nan_inf": (
        manifest["nan_count"].fillna(1).eq(0) & manifest["inf_count"].fillna(1).eq(0)
    ).all(),
    "tidak_ada_sinyal_kosong": not manifest["all_zero"].fillna(True).any(),
    "sha256_lengkap": manifest["sha256"].notna().all(),
}
check_table = pd.DataFrame(
    {"pemeriksaan": list(checks), "lulus": list(checks.values())}
)
check_table["status"] = np.where(check_table["lulus"], "PASS", "FAIL")

if not all(checks.values()):
    raise ValueError("Manifest tidak lolos audit awal. Periksa tabel pemeriksaan.")

display(check_table)
display(
    manifest.groupby("label_name")
    .agg(
        n_files=("relative_path", "size"),
        n_nim=("nim", "nunique"),
        n_duplicate_files=("is_exact_duplicate", "sum"),
        n_peak_over_one=("peak_over_one", "sum"),
        n_low_level=("low_level", "sum"),
    )
    .reindex(LABEL_ORDER)
)

check_table.to_csv(ARTIFACT_DIR / "section1_input_checks.csv", index=False)
