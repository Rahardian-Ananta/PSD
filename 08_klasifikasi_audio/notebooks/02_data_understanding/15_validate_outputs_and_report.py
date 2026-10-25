# Tujuan: memvalidasi keterhubungan seluruh artefak Data Understanding dan menulis laporan ringkas.
# Proses: memeriksa jumlah baris, keunikan path, kelengkapan metadata, konsistensi kelas, dan keberadaan grafik.
# Output: laporan validasi, manifest final Data Understanding, dan data_understanding_report.md.

from IPython.display import Markdown


def df_to_markdown(frame, max_rows=20):
    display_frame = frame.head(max_rows).copy()
    columns = [str(column) for column in display_frame.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "|" + "|".join(["---"] * len(columns)) + "|",
    ]
    for row in display_frame.itertuples(index=False):
        values = []
        for value in row:
            if isinstance(value, float):
                text = f"{value:.4f}"
            else:
                text = str(value)
            values.append(text.replace("|", "\\|").replace("\n", " "))
        lines.append("| " + " | ".join(values) + " |")
    if len(frame) > max_rows:
        lines.append(f"\n*Menampilkan {max_rows} dari {len(frame)} baris.*")
    return "\n".join(lines)


raw_file_count = sum(1 for path in RAW_DIR.rglob("*") if path.is_file())
figure_paths = [
    FIGURE_DIR / "class_distribution.png",
    FIGURE_DIR / "duration_distribution.png",
    FIGURE_DIR / "format_characteristics.png",
    FIGURE_DIR / "waveform_examples.png",
    FIGURE_DIR / "spectrogram_examples.png",
]

assert len(inventory) == raw_file_count, "Jumlah inventaris tidak sama dengan jumlah file mentah."
assert len(manifest_raw) == len(inventory), "Manifest tidak mencakup seluruh inventaris."
assert manifest_raw["relative_path"].is_unique, "Ada relative_path duplikat pada manifest."
assert manifest_raw["read_ok"].fillna(False).all(), "Ada file yang gagal dibaca."
assert manifest_raw["sha256"].notna().all(), "Ada file tanpa hash."
assert manifest_raw["nim"].notna().all(), "Ada NIM yang tidak terbaca."
assert manifest_raw["take"].notna().all(), "Ada take yang tidak terbaca."
assert manifest_raw["label"].notna().all(), "Ada label yang tidak dapat dipastikan."
assert len(duplicate_files) == int(manifest_raw["is_exact_duplicate"].sum()), "Jumlah file duplikat tidak konsisten."
assert int(duplicate_groups["n_files"].sum()) == len(duplicate_files), "Ukuran grup duplikat tidak konsisten."
assert manifest_raw["critical_failure"].sum() == 0, "Ada kegagalan integritas kritis."
assert all(path.exists() for path in figure_paths), "Ada grafik yang belum dihasilkan."
assert (ARTIFACT_DIR / "data_understanding_summary.json").exists(), "Ringkasan JSON belum dibuat."

manifest_raw.to_csv(ARTIFACT_DIR / "manifest_raw.csv", index=False)

report = f"""# 02 — Data Understanding: Laporan Aktual

## Ringkasan data

- Total file mentah: **{len(manifest_raw)}**
- NIM unik: **{manifest_raw['nim'].nunique()}**
- Kelas berisik: **{int((manifest_raw['label'] == 1).sum())} file**
- Kelas non-berisik: **{int((manifest_raw['label'] == 0).sum())} file**
- File berdurasi tepat 30 detik: **{int(manifest_raw['duration_status'].eq('tepat_30_detik').sum())} / {len(manifest_raw)}**
- File berhasil dibaca: **{int(manifest_raw['read_ok'].fillna(False).sum())} / {len(manifest_raw)}**
- Hash unik: **{manifest_raw['sha256'].nunique()}**
- File terlibat duplikat eksak: **{int(manifest_raw['is_exact_duplicate'].sum())}**
- NIM lengkap 6 file: **{int(nim_summary['lengkap_6_file'].sum())} / {len(nim_summary)}**
- Kombinasi NIM-kelas-take yang hilang: **{len(missing_takes)}**

## Distribusi kelas

{df_to_markdown(class_summary)}

## Kelengkapan per NIM

{df_to_markdown(nim_summary, max_rows=40)}

## Format dan metadata

{df_to_markdown(format_summary)}

{df_to_markdown(metadata_summary)}

## Duplikasi eksak

{df_to_markdown(duplicate_groups[['duplicate_group_id', 'n_files', 'labels', 'nims', 'takes', 'scope']])}

Interpretasi:

- **{int((duplicate_groups['scope'] == 'cross_label').sum())} grup** memiliki label berbeda untuk audio identik. Ini adalah konflik label yang harus dikarantina atau diadjudikasi.
- **{int((duplicate_groups['scope'] == 'cross_nim').sum())} grup** melintasi NIM. `GroupKFold` saja **tidak** mencegah kebocoran untuk kasus ini karena konten identik dapat muncul pada NIM train dan test.
- **{int((duplicate_groups['scope'] == 'within_nim').sum())} grup** berada dalam NIM yang sama dan mencakup beberapa take, sehingga take tersebut bukan observasi independen.

## Temuan kualitas berprioritas

{df_to_markdown(quality_findings[['finding_id', 'kategori', 'severity', 'jumlah', 'temuan', 'tindakan_03']], max_rows=40)}

## Artefak

- `inventory_raw.csv`: inventaris awal.
- `manifest_raw.csv`: manifest mentah terpadu.
- `audio_metadata.csv`: metadata sinyal per file.
- `duplicate_groups.csv`, `duplicate_files.csv`: hasil deteksi duplikat.
- `missing_takes.csv`: kombinasi NIM-kelas-take yang tidak ada.
- `class_summary.csv`, `nim_summary.csv`, `format_summary.csv`, `metadata_summary.csv`.
- `quality_findings.csv`: temuan yang harus ditindaklanjuti pada tahap 03.
- `data_understanding_summary.json`: ringkasan untuk otomasi.
- `figures/`: distribusi kelas, durasi, format, waveform, dan spektrogram.

## Kesimpulan

Data mentah berjumlah **{len(manifest_raw)} file** dan **{manifest_raw['nim'].nunique()} NIM**, dengan distribusi kelas **{int((manifest_raw['label'] == 1).sum())} berisik** dan **{int((manifest_raw['label'] == 0).sum())} non-berisik**. Semua file dapat dibaca dan berdurasi 30 detik, tetapi dataset **belum siap dimodelkan** karena terdapat duplikasi eksak—termasuk duplikasi lintas NIM dan satu konflik label—serta {len(incomplete_nims)} NIM yang tidak lengkap. Keputusan pembersihan, karantina, dan seleksi data harus dilakukan pada tahap 03 dengan ketertelusuran penuh. FFmpeg di PATH: **{shutil.which('ffmpeg') or 'tidak ditemukan'}**.
"""

report_path = ARTIFACT_DIR / "data_understanding_report.md"
report_path.write_text(report, encoding="utf-8")

validation_summary = pd.DataFrame(
    {
        "pemeriksaan": [
            "inventaris = jumlah file mentah",
            "manifest = inventaris",
            "relative_path unik",
            "semua file terbaca",
            "semua NIM/take/label terisi",
            "konsistensi grup duplikat",
            "tidak ada kegagalan kritis",
            "semua grafik tersedia",
            "laporan Markdown tersedia",
        ],
        "status": [
            "LULUS",
            "LULUS",
            "LULUS",
            "LULUS",
            "LULUS",
            "LULUS",
            "LULUS",
            "LULUS",
            "LULUS",
        ],
    }
)

display(validation_summary)
print("VALIDASI 02: LULUS")
print(f"Laporan disimpan: {report_path}")
display(Markdown(report))
