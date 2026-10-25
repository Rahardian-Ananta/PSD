quarantine_rows = []
for row in quarantine_manifest.sort_values("relative_path").itertuples():
    source = RAW_DIR / row.relative_path
    destination = QUARANTINE_DIR / row.relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)

    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if source_hash != row.sha256:
        raise ValueError(f"Hash sumber berubah sebelum karantina: {row.relative_path}")

    if destination.exists():
        destination_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
        if destination_hash != source_hash:
            raise ValueError(f"File karantina lama berbeda: {destination}")
    else:
        shutil.copy2(source, destination)

    destination_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
    if destination_hash != source_hash:
        raise ValueError(f"Salinan karantina tidak identik: {destination}")

    quarantine_rows.append(
        {
            "relative_path": row.relative_path,
            "file": row.file,
            "nim": row.nim,
            "take": int(row.take),
            "label": int(row.label),
            "label_name": row.label_name,
            "selection_reason": row.selection_reason,
            "duplicate_group_id": row.duplicate_group_id,
            "duplicate_scope": row.duplicate_scope,
            "sha256": row.sha256,
            "source_path": str(source),
            "quarantine_path": str(destination),
            "detected_stage": "03_data_preparation",
            "action": "copied_no_raw_deletion",
        }
    )

quarantine_log = pd.DataFrame(quarantine_rows)
quarantine_log.to_csv(QUARANTINE_DIR / "CATATAN_KARANTINA.csv", index=False)

with open(QUARANTINE_DIR / "README.md", "w", encoding="utf-8") as handle:
    handle.write(
        "# Karantina Tahap 03\n\n"
        "File di folder ini adalah **salinan** dari `raw_audio/`, bukan file asli yang dipindahkan.\n\n"
        "- Alasan utama: duplikat eksak lintas label atau duplikat same-label yang bukan wakil terpilih.\n"
        "- Rincian asal, hash SHA-256, grup duplikat, dan alasan ada di `CATATAN_KARANTINA.csv`.\n"
        "- File di sini tidak dipakai untuk `data_final/`, `features.csv`, atau modeling.\n"
    )

display(
    quarantine_log.groupby(["selection_reason", "label_name"])
    .size()
    .rename("n_files")
    .reset_index()
)
print(f"Total file dikarantina: {len(quarantine_log)}")
print(f"Catatan: {QUARANTINE_DIR / 'CATATAN_KARANTINA.csv'}")
