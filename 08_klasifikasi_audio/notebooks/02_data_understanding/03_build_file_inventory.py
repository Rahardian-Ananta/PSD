# Tujuan: menginventarisasi seluruh file mentah dan mem-parse identitas dari nama file.
# Proses: membaca struktur folder, mengekstrak NIM/kelas/take, dan membandingkan label folder dengan label nama file.
# Output: tabel inventaris per file dan ringkasan hasil parsing.

inventory_rows = []

for path in sorted(RAW_DIR.rglob("*")):
    if not path.is_file():
        continue

    relative_path = path.relative_to(RAW_DIR).as_posix()
    relative_parts = Path(relative_path).parts
    folder = relative_parts[0] if len(relative_parts) > 1 else "(root)"
    match = FILENAME_PATTERN.match(path.name)

    folder_label = FOLDER_LABEL_MAP.get(folder.lower(), np.nan)
    filename_label = np.nan
    nim = pd.NA
    take = pd.NA

    if match:
        nim = match.group("nim")
        take = int(match.group("take"))
        filename_label = 1 if match.group("label_text").lower() == "berisik" else 0

    label_match = (
        pd.notna(folder_label)
        and pd.notna(filename_label)
        and int(folder_label) == int(filename_label)
    )
    label = int(folder_label) if label_match else np.nan

    inventory_rows.append(
        {
            "relative_path": relative_path,
            "file": path.name,
            "folder": folder,
            "extension": path.suffix.lower(),
            "size_bytes": path.stat().st_size,
            "name_parse_ok": bool(match),
            "nim": nim,
            "take": take,
            "label_from_folder": folder_label,
            "label_from_filename": filename_label,
            "label_match": label_match,
            "label": label,
            "extension_ok": path.suffix.lower() in AUDIO_EXTENSIONS,
        }
    )

inventory = pd.DataFrame(inventory_rows)
inventory = inventory.sort_values("relative_path").reset_index(drop=True)

inventory_counts = pd.DataFrame(
    {
        "pemeriksaan": [
            "total file",
            "nama file sesuai pola",
            "nama file tidak sesuai pola",
            "ekstensi MP3",
            "label folder = label nama file",
            "label tidak dapat dipastikan",
        ],
        "jumlah": [
            len(inventory),
            int(inventory["name_parse_ok"].sum()),
            int((~inventory["name_parse_ok"]).sum()),
            int(inventory["extension_ok"].sum()),
            int(inventory["label_match"].sum()),
            int(inventory["label"].isna().sum()),
        ],
    }
)

display(inventory_counts)
display(inventory["folder"].value_counts().rename_axis("folder").reset_index(name="jumlah"))
display(inventory.head(8))

unparsed = inventory.loc[~inventory["name_parse_ok"], ["relative_path"]]
if len(unparsed):
    display(unparsed)
else:
    print("Tidak ada file yang gagal diparse.")

mismatched = inventory.loc[~inventory["label_match"], ["relative_path", "label_from_folder", "label_from_filename"]]
if len(mismatched):
    display(mismatched)
else:
    print("Tidak ada pertentangan label folder vs nama file.")

inventory.to_csv(ARTIFACT_DIR / "inventory_raw.csv", index=False)
print(f"Inventaris disimpan: {ARTIFACT_DIR / 'inventory_raw.csv'} ({len(inventory)} baris)")
