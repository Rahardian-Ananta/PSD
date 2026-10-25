from IPython.display import Markdown


def md_table(frame, max_rows=None):
    view = frame if max_rows is None else frame.head(max_rows)
    columns = [str(column) for column in view.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "|" + "|".join(["---"] * len(columns)) + "|",
    ]
    for row in view.itertuples(index=False):
        values = []
        for value in row:
            if isinstance(value, (float, np.floating)):
                text = f"{value:.6g}"
            elif isinstance(value, (bool, np.bool_)):
                text = str(bool(value))
            else:
                text = str(value)
            values.append(text.replace("|", "\\|").replace("\n", " "))
        lines.append("| " + " | ".join(values) + " |")
    if len(frame) > len(view):
        lines.append("")
        lines.append(f"*Menampilkan {len(view)} dari {len(frame)} baris.*")
    return "\n".join(lines)


cross_label_excluded = quarantine_manifest.loc[
    quarantine_manifest["selection_reason"] == "duplikat_lintas_label",
    ["file", "nim", "label_name", "duplicate_group_id"],
]
top_correlations = high_corr_pairs.head(5)
top_cohens = cohens_d_table.head(5)
top_mi = feature_importance.sort_values("mutual_info", ascending=False).head(5)
top_rf = feature_importance.sort_values("rf_importance", ascending=False).head(5)

report = f"""# 03 — Data Preparation: Laporan Aktual

## Ringkasan

Dataset final Tahap 03 berisi **{len(final_dataset_manifest)} file**, **{features['nim'].nunique()} NIM**, dan distribusi **{int(features['label'].eq(0).sum())} non-berisik : {int(features['label'].eq(1).sum())} berisik**. Semua NIM final memiliki kedua kelas.

- File awal: {len(manifest)}.
- File final: {len(final_dataset_manifest)}.
- File dikarantina: {len(quarantine_manifest)} (salinan, bukan pemindahan dari `raw_audio/`).
- Grup duplikat same-label: {len(group_choices)}; wakil dipilih: {len(selected_representatives)}.
- NIM yang hilang dari dataset final: {", ".join(search_summary["dropped_nims"]) or "-"}.
- `24-123` tidak punya file final karena seluruh file-nya menjadi duplikat non-wakil.

## Seleksi dan duplikasi

Pemilihan wakil memakai hash SHA-256, bukan kemiripan audio. Duplikat lintas label tidak dipertahankan. Duplikat same-label dipilih satu wakil per hash dengan prioritas: jumlah NIM yang memiliki kedua kelas, jumlah NIM terwakili, lalu menekan NIM satu kelas.

Kombinasi yang dievaluasi: **{n_combinations:,}**. Solusi terpilih memiliki **{search_summary["best_both_class_nims"]} NIM dua kelas**, **{search_summary["best_one_class_nims"]} NIM satu kelas**, dan **{search_summary["best_represented_nims"]} NIM terwakili**.

File duplikat lintas label yang dikarantina:

{md_table(cross_label_excluded) if len(cross_label_excluded) else "Tidak ada."}

## Audio final

- `data_mp3/`: {len(staging_manifest)} file, seluruhnya salinan byte-identik karena sumber sudah MP3.
- `data_final/`: {len(transformation_manifest)} WAV.
- Format: WAV PCM_16, mono, {SR} Hz.
- Panjang: tepat {TARGET_SAMPLES} sampel = {TARGET_DURATION_S:.0f} detik.
- Aksi durasi: {transformation_manifest['duration_action'].value_counts().to_dict()}.
- Peak sebelum normalisasi: min {transformation_manifest['peak_before_norm'].min():.5f}, median {transformation_manifest['peak_before_norm'].median():.5f}, max {transformation_manifest['peak_before_norm'].max():.5f}.
- Peak WAV setelah PCM16: min {transformation_manifest['peak_pcm16'].min():.5f}, max {transformation_manifest['peak_pcm16'].max():.5f}.
- Semua WAV memiliki hash unik: {final_dataset_manifest['final_sha256'].is_unique}.

Kontrak preprocessing lengkap tersimpan di `artifacts/03_data_preparation/preprocessing_contract.json`.

## Fitur

- Jumlah fitur: 12.
- Jumlah frame per file: {example_frames.shape[0]} (frame 400 sampel, hop 160, tanpa `center=True`).
- Window: Hann simetris 400 sampel.
- FFT: 512 titik; 257 bin rFFT; resolusi {FREQS[1] - FREQS[0]:.2f} Hz.
- Pemeriksaan rFFT vs FFT penuh, selisih daya maksimum: {fft_rfft_max_abs_diff:.3e}.
- Frame dengan daya nol: {int(silent_frame_audit['empty_power_frames'].sum())} pada {int((silent_frame_audit['empty_power_frames'] > 0).sum())} file. Hening tidak dihapus; fitur spektral frame tersebut ditetapkan 0.
- `features.csv`: {len(features)} baris, tanpa NaN/Inf, seluruh rentang fitur valid.

### Korelasi tinggi (|r| > 0,90)

{md_table(top_correlations) if len(top_correlations) else "Tidak ada."}

Korelasi tinggi ditandai, tetapi tidak ada fitur yang dihapus otomatis.

### Cohen's d teratas

{md_table(top_cohens[['feature', 'mean_non_berisik', 'mean_berisik', 'pooled_sd', 'cohens_d']])}

### Mutual information teratas

{md_table(top_mi[['feature', 'mutual_info', 'mi_rank']])}

### Random Forest importance teratas

{md_table(top_rf[['feature', 'rf_importance', 'rf_rank']])}

### Kandidat top-8

Kandidat dipilih dari rata-rata peringkat mutual information dan Random Forest importance:

{chr(10).join(f"- {feature}" for feature in selected_features_from_file)}

Kandidat ini **eksploratif**. Seleksi final dan scaling wajib dipelajari ulang di dalam `Pipeline` pada training fold Tahap 04. Tidak ada PCA.

## Pengecekan librosa

{md_table(comparison_summary[['feature', 'manual_mean', 'librosa_mean', 'mean_abs_difference', 'pearson_r', 'note']])}

Perbedaan centroid, bandwidth, rolloff, dan flatness sebagian berasal dari definisi manual berbasis daya \\(P=|S|^2\\) versus librosa berbasis magnitudo. ZCR dapat berbeda karena konvensi tepi frame.

## Validasi akhir

Semua pemeriksaan lulus: **{int(check_table['lulus'].sum())}/{len(check_table)}**.

{md_table(check_table[['pemeriksaan', 'status']])}

Traceability `raw_audio -> data_mp3 -> data_final -> features.csv` lengkap untuk {len(final_dataset_manifest)} file.

## Batasan

- Split train/test belum dibuat pada tahap ini.
- Tidak ada training model final atau GridSearchCV; Random Forest hanya dipakai untuk importance eksploratif.
- Dataset final hanya berisi file yang bukan duplikat non-wakil dan bukan duplikat lintas label.
- File karantina tetap tersedia untuk audit, bukan untuk modeling.
- `raw_audio/` tidak diubah.

## Artefak

- `artifacts/features.csv`
- `artifacts/selected_features.txt`
- `artifacts/03_data_preparation/final_dataset_manifest.csv`
- `artifacts/03_data_preparation/validation_report.md`
- `artifacts/03_data_preparation/validation_summary.json`
- `artifacts/03_data_preparation/librosa_comparison_summary.csv`
- `quarantine/03_data_preparation/CATATAN_KARANTINA.csv`

## Kesimpulan dan keputusan untuk Tahap 04

1. **Jumlah aktual:** 176 file final, 24 file karantina, 34 NIM, kelas 88 non-berisik : 88 berisik, semua NIM berdua kelas, `24-123` gugur.
2. **Duplikasi selesai:** 1 grup lintas label (DUP04) dikarantina seluruhnya; 17 grup same-label memilih satu wakil; tidak ada data kembar yang lolos ke modeling.
3. **Format seragam:** semua final adalah WAV PCM_16 mono 16000 Hz tepat 480000 sampel dengan peak normalization; `data_mp3/` hanya salinan byte-identik.
4. **Fitur:** 12 fitur numerik tervalidasi untuk 176 file; tidak ada NaN/Inf; pemeriksaan rFFT vs FFT penuh konsisten.
5. **Kandidat fitur:** 8 kandidat eksploratif disimpan di `artifacts/selected_features.txt`; wajib dipelajari ulang di training fold, bukan dipakai sebagai keputusan final.
6. **Belum dilakukan:** split berbasis NIM, training model, GridSearchCV, dan evaluasi hold-out.

**Data Preparation selesai dan tervalidasi. Model belum dilatih.**
"""

(ARTIFACT_DIR / "data_preparation_report.md").write_text(report, encoding="utf-8")

data_preparation_summary = {
    "status": "PASS",
    "n_raw": int(len(manifest)),
    "n_final": int(len(final_dataset_manifest)),
    "n_quarantine": int(len(quarantine_manifest)),
    "n_nim_final": int(features["nim"].nunique()),
    "class_counts": {str(k): int(v) for k, v in features["label"].value_counts().sort_index().items()},
    "n_features": len(FEATURE_COLUMNS),
    "n_frames_per_file": int(example_frames.shape[0]),
    "n_zero_power_frames": int(silent_frame_audit["empty_power_frames"].sum()),
    "n_files_with_zero_power_frames": int((silent_frame_audit["empty_power_frames"] > 0).sum()),
    "sample_rate": SR,
    "target_samples": TARGET_SAMPLES,
    "duration_actions": {str(k): int(v) for k, v in transformation_manifest["duration_action"].value_counts().items()},
    "top8_candidates": selected_features_from_file,
    "dropped_nims": search_summary["dropped_nims"],
    "fft_rfft_max_abs_diff": float(fft_rfft_max_abs_diff),
}
with open(ARTIFACT_DIR / "data_preparation_summary.json", "w", encoding="utf-8") as handle:
    json.dump(data_preparation_summary, handle, ensure_ascii=False, indent=2)

print(f"Laporan tahap: {ARTIFACT_DIR / 'data_preparation_report.md'}")
display(Markdown(report))
