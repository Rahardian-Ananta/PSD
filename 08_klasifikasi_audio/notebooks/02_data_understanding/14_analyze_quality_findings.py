# Tujuan: merangkum temuan kualitas data menjadi daftar yang dapat ditindaklanjuti.
# Proses: menggabungkan hasil inventaris, validasi identitas, duplikasi, integritas, dan metadata aktual.
# Output: quality_findings.csv dan tabel temuan berprioritas.

cross_nim_rows = manifest_raw.loc[manifest_raw["duplicate_scope"] == "cross_nim"]
cross_nim_nims = sorted(cross_nim_rows["nim"].dropna().unique().tolist())
cross_label_rows = manifest_raw.loc[manifest_raw["duplicate_scope"] == "cross_label"]
cross_label_detail = "; ".join(
    sorted(
        f"{row.duplicate_group_id}: {row.files}"
        for row in duplicate_groups.loc[duplicate_groups["scope"] == "cross_label"].itertuples()
    )
)
incomplete_nims = nim_summary.loc[~nim_summary["lengkap_6_file"], "nim"].tolist()
single_class_nims = nim_summary.loc[~nim_summary["memiliki_dua_kelas"], "nim"].tolist()
low_level_paths = "; ".join(low_level_files["relative_path"].tolist())

findings = [
    {
        "finding_id": "F01",
        "kategori": "Duplikasi",
        "temuan": (
            f"{len(duplicate_groups)} grup duplikat eksak melibatkan "
            f"{int(manifest_raw['is_exact_duplicate'].sum())} file; hanya "
            f"{manifest_raw['sha256'].nunique()} hash unik dari {len(manifest_raw)} file."
        ),
        "jumlah": int(manifest_raw["is_exact_duplicate"].sum()),
        "severity": "Tinggi",
        "implikasi": "File kembar tidak menambah informasi baru dan dapat membocorkan konten antar-split.",
        "tindakan_03": "Tinjau setiap grup; jangan langsung hapus; putuskan representasi dan karantina secara eksplisit.",
    },
    {
        "finding_id": "F02",
        "kategori": "Duplikasi lintas NIM",
        "temuan": (
            f"{int((duplicate_groups['scope'] == 'cross_nim').sum())} grup duplikat eksak melintasi NIM "
            f"({len(cross_nim_rows)} file; NIM: {', '.join(cross_nim_nims)})."
        ),
        "jumlah": int(len(cross_nim_rows)),
        "severity": "Kritis",
        "implikasi": (
            "GroupKFold berbasis NIM tidak mencegah kebocoran bila audio identik muncul pada NIM berbeda; "
            "konten yang sama dapat masuk train dan test."
        ),
        "tindakan_03": "Selesaikan duplikasi lintas NIM sebelum split; jangan mengandalkan GroupKFold saja.",
    },
    {
        "finding_id": "F03",
        "kategori": "Konflik label",
        "temuan": (
            f"{int((duplicate_groups['scope'] == 'cross_label').sum())} grup duplikat eksak memiliki label berbeda: "
            f"{cross_label_detail}."
        ),
        "jumlah": int(len(cross_label_rows)),
        "severity": "Kritis",
        "implikasi": "Dua file identik tidak mungkin memiliki label ground truth yang berbeda; minimal satu label salah.",
        "tindakan_03": "Karantina atau minta adjudikasi manusia; jangan memakai keduanya sebagai dua kelas.",
    },
    {
        "finding_id": "F04",
        "kategori": "Duplikasi dalam NIM",
        "temuan": (
            f"{int((duplicate_groups['scope'] == 'within_nim').sum())} grup duplikat berada dalam NIM yang sama "
            "dan mencakup beberapa take sekaligus."
        ),
        "jumlah": int((manifest_raw["duplicate_scope"] == "within_nim").sum()),
        "severity": "Tinggi",
        "implikasi": "Take yang seharusnya berbeda ternyata rekaman identik; jumlah sampel efektif lebih kecil dari 200.",
        "tindakan_03": "Perlakukan take kembar sebagai satu observasi atau karantina sesuai kebijakan yang terdokumentasi.",
    },
    {
        "finding_id": "F05",
        "kategori": "Kelengkapan NIM",
        "temuan": (
            f"{len(incomplete_nims)} NIM tidak memiliki 6 file: {', '.join(incomplete_nims)}; "
            f"{len(missing_takes)} kombinasi NIM-kelas-take hilang."
        ),
        "jumlah": int(len(missing_takes)),
        "severity": "Sedang",
        "implikasi": "Protokol 3 take per kelas tidak terpenuhi untuk sebagian NIM; data tidak seimbang per subjek.",
        "tindakan_03": "Pertahankan identitas apa adanya, tandai NIM tidak lengkap, dan putuskan inklusi dengan kriteria eksplisit.",
    },
    {
        "finding_id": "F06",
        "kategori": "NIM satu kelas",
        "temuan": (
            f"{len(single_class_nims)} NIM hanya memiliki satu kelas: {', '.join(single_class_nims)}."
        ),
        "jumlah": int(len(single_class_nims)),
        "severity": "Sedang",
        "implikasi": "NIM tersebut tidak dapat berkontribusi pada kedua kelas dan dapat memengaruhi kestabilan evaluasi.",
        "tindakan_03": "Putuskan apakah tetap dipakai; jika dipakai, laporkan komposisinya dan jangan menyembunyikan keterbatasan.",
    },
    {
        "finding_id": "F07",
        "kategori": "Integritas file",
        "temuan": (
            f"{int((~manifest_raw['read_ok'].fillna(False)).sum())} file gagal dibaca, "
            f"{int(manifest_raw['all_zero'].sum())} sinyal semua nol, "
            f"{int(manifest_raw['nan_count'].fillna(0).gt(0).sum())} file ber-NaN, "
            f"{int(manifest_raw['inf_count'].fillna(0).gt(0).sum())} file ber-Inf."
        ),
        "jumlah": int(manifest_raw["critical_failure"].sum()),
        "severity": "Info",
        "implikasi": "Tidak ada kerusakan teknis yang terdeteksi pada tahap ini.",
        "tindakan_03": "Tetap jalankan pemeriksaan ulang setelah konversi dan setelah ekstraksi fitur.",
    },
    {
        "finding_id": "F08",
        "kategori": "Durasi",
        "temuan": (
            f"{int(manifest_raw['duration_status'].eq('tepat_30_detik').sum())} dari {len(manifest_raw)} file "
            f"berdurasi tepat 30 detik (min={manifest_raw['duration_decoded_s'].min():.3f}, "
            f"max={manifest_raw['duration_decoded_s'].max():.3f})."
        ),
        "jumlah": int(manifest_raw["duration_status"].eq("tepat_30_detik").sum()),
        "severity": "Info",
        "implikasi": "Pada data mentah tidak ada kebutuhan crop/pad karena durasi; aturan tetap wajib diterapkan setelah resampling.",
        "tindakan_03": "Pastikan hasil akhir tepat 480.000 sampel dan catat tindakan aktual per file.",
    },
    {
        "finding_id": "F09",
        "kategori": "Heterogenitas format",
        "temuan": (
            f"Sample rate: {manifest_raw['samplerate'].value_counts().sort_index().to_dict()}; "
            f"channel: {manifest_raw['channels'].value_counts().sort_index().to_dict()}."
        ),
        "jumlah": int(manifest_raw["samplerate"].nunique()),
        "severity": "Sedang",
        "implikasi": "Audio belum seragam; ekstraksi fitur harus dilakukan setelah konversi ke 16 kHz mono.",
        "tindakan_03": "Resample ke 16 kHz, downmix mono, dan validasi 480.000 sampel.",
    },
    {
        "finding_id": "F10",
        "kategori": "Level sinyal",
        "temuan": (
            f"{int(manifest_raw['low_level'].sum())} file memiliki peak < {LOW_PEAK_THRESHOLD:.2f}: "
            f"{low_level_paths if low_level_paths else 'tidak ada'}."
        ),
        "jumlah": int(manifest_raw["low_level"].sum()),
        "severity": "Rendah",
        "implikasi": "Peak normalization akan memperkuat sinyal dan noise floor secara bersamaan.",
        "tindakan_03": "Audit level dan dengarkan file tersebut; jangan menghapus hanya karena levelnya rendah.",
    },
    {
        "finding_id": "F11",
        "kategori": "Overshoot MP3",
        "temuan": f"{int(manifest_raw['peak_over_one'].fillna(False).sum())} file memiliki peak > 1.0 setelah decode.",
        "jumlah": int(manifest_raw["peak_over_one"].fillna(False).sum()),
        "severity": "Rendah",
        "implikasi": "Nilai > 1.0 dapat muncul dari decoding MP3 dan bukan bukti file rusak.",
        "tindakan_03": "Peak normalization wajib menangani nilai absolut > 1.0 dan sinyal nol.",
    },
    {
        "finding_id": "F12",
        "kategori": "Label",
        "temuan": (
            f"Label folder dan nama file cocok untuk {int(manifest_raw['label_match'].sum())} file; "
            "namun kecocokan ini hanya konsistensi metadata, bukan verifikasi isi audio."
        ),
        "jumlah": int(manifest_raw["label_match"].sum()),
        "severity": "Sedang",
        "implikasi": "Label semantik belum tentu benar; duplikat lintas label sudah membuktikan adanya konflik.",
        "tindakan_03": "Pertahankan label yang dapat dilacak; karantina kasus konflik; jangan memberi label baru dari kemiripan audio.",
    },
    {
        "finding_id": "F13",
        "kategori": "Lingkungan",
        "temuan": f"FFmpeg di PATH: {shutil.which('ffmpeg') or 'tidak ditemukan'}.",
        "jumlah": 0 if shutil.which("ffmpeg") else 1,
        "severity": "Sedang" if not shutil.which("ffmpeg") else "Info",
        "implikasi": "Konversi MP3 pada Data Preparation memerlukan FFmpeg yang dapat dipanggil.",
        "tindakan_03": "Pasang/daftarkan FFmpeg sebelum menjalankan konversi.",
    },
    {
        "finding_id": "F14",
        "kategori": "Keseimbangan kelas",
        "temuan": (
            f"Data mentah: {dict(zip(class_summary['label_name'], class_summary['n_files']))}; "
            f"setelah duplikasi dan karantina, komposisi harus dihitung ulang."
        ),
        "jumlah": int(len(manifest_raw)),
        "severity": "Info",
        "implikasi": "Keseimbangan 100/100 pada data mentah tidak otomatis bertahan setelah pembersihan.",
        "tindakan_03": "Laporkan distribusi final dan pertimbangkan class_weight di dalam pipeline bila perlu.",
    },
]

quality_findings = pd.DataFrame(findings)
severity_order = {"Kritis": 0, "Tinggi": 1, "Sedang": 2, "Rendah": 3, "Info": 4}
quality_findings["severity_order"] = quality_findings["severity"].map(severity_order)
quality_findings = quality_findings.sort_values(["severity_order", "finding_id"]).drop(columns="severity_order")

display(quality_findings[["finding_id", "kategori", "severity", "jumlah", "temuan"]])
quality_findings.to_csv(ARTIFACT_DIR / "quality_findings.csv", index=False)
print(f"Temuan kualitas disimpan: {ARTIFACT_DIR / 'quality_findings.csv'} ({len(quality_findings)} temuan)")
