if not (final_manifest["extension"] == ".mp3").all():
    raise ValueError("Ada file final yang bukan MP3; staging memerlukan aturan konversi tambahan.")

staging_rows = []
for row in final_manifest.sort_values("relative_path").itertuples():
    source = RAW_DIR / row.relative_path
    destination = DATA_MP3_DIR / row.relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)

    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if source_hash != row.sha256:
        raise ValueError(f"Hash sumber berubah: {row.relative_path}")

    if destination.exists():
        destination_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
        if destination_hash != source_hash:
            raise ValueError(f"File staging lama berbeda: {destination}")
    else:
        shutil.copy2(source, destination)

    destination_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
    if destination_hash != source_hash:
        raise ValueError(f"Salinan staging tidak identik: {destination}")

    staging_rows.append(
        {
            "source_relative_path": row.relative_path,
            "mp3_relative_path": row.relative_path,
            "file_mp3": row.file,
            "nim": row.nim,
            "take": int(row.take),
            "label": int(row.label),
            "label_name": row.label_name,
            "sha256": source_hash,
            "source_bytes": int(source.stat().st_size),
            "mp3_bytes": int(destination.stat().st_size),
            "staging_action": "copy_byte_identical_already_mp3",
        }
    )

staging_manifest = pd.DataFrame(staging_rows)
expected_mp3_paths = set(staging_manifest["mp3_relative_path"])
actual_mp3_paths = {
    path.relative_to(DATA_MP3_DIR).as_posix()
    for path in DATA_MP3_DIR.rglob("*")
    if path.is_file()
}
if actual_mp3_paths != expected_mp3_paths:
    extra = sorted(actual_mp3_paths - expected_mp3_paths)
    missing = sorted(expected_mp3_paths - actual_mp3_paths)
    raise ValueError(f"Struktur data_mp3 tidak sesuai. Ekstra: {extra}; hilang: {missing}")

display(staging_manifest.groupby("label_name").agg(n_files=("file_mp3", "size")).reindex(LABEL_ORDER))
print(f"File staging: {len(staging_manifest)}")
print(f"Total ukuran MP3 staging: {staging_manifest['mp3_bytes'].sum() / 1024**2:.2f} MB")

staging_manifest.to_csv(ARTIFACT_DIR / "staging_manifest.csv", index=False)
