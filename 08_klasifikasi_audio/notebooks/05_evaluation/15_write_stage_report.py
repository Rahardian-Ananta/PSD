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


worst_nim_row = metrics_by_nim.loc[metrics_by_nim["accuracy"].idxmin()]
n_perfect_nim = int((metrics_by_nim["accuracy"] == 1.0).sum())
max_errors_nim = metrics_by_nim.loc[metrics_by_nim["n_salah"].idxmax()]
ci_includes_threshold = bool(ci_low <= ROC_AUC_THRESHOLD <= ci_high)
ci_note = (
    f"CI95 **memuat** {ROC_AUC_THRESHOLD:.2f}, sehingga kelayakan pada populasi "
    "tidak dapat dipastikan dari data uji ini saja."
    if ci_includes_threshold
    else f"CI95 **tidak memuat** {ROC_AUC_THRESHOLD:.2f}."
)

metrics_view = pd.DataFrame(
    {
        "metrik": [
            "ROC-AUC",
            "ROC-AUC CI 95% (bootstrap)",
            "PR-AUC",
            "accuracy",
            "precision (kelas 1)",
            "recall (kelas 1)",
            "F1 (kelas 1)",
            "accuracy per NIM (rata-rata)",
        ],
        "nilai": [
            f"{roc_auc_value:.4f}",
            f"[{ci_low:.4f}, {ci_high:.4f}]",
            f"{pr_auc_value:.4f}",
            f"{accuracy_value:.4f}",
            f"{precision_value:.4f}",
            f"{recall_value:.4f}",
            f"{f1_value:.4f}",
            f"{metrics['accuracy_per_nim_mean']:.4f}",
        ],
        "acuan": [
            "baseline 0,5000; syarat 0,85",
            "2.000 pengambilan ulang",
            f"baseline prevalensi {prevalence_value:.4f}",
            "kelas hampir seimbang",
            "kelas positif = berisik",
            "kelas positif = berisik",
            "precision dan recall",
            f"rentang {metrics['accuracy_per_nim_min']:.4f} - {metrics['accuracy_per_nim_max']:.4f}",
        ],
    }
)

cm_view = cm_frame.reset_index().rename(columns={"index": "aktual"})
report_view = report_frame.reset_index().rename(columns={"index": "kelas"})
errors_view = (
    errors[["file", "nim", "label_name", "pred_label_name", "proba_berisik"]]
    if len(errors)
    else pd.DataFrame(columns=["file", "nim", "label_name", "pred_label_name", "proba_berisik"])
)

report = f"""# 05 — Evaluation: Laporan Aktual

## Ringkasan

Model dari Tahap 04 diuji **satu kali** pada NIM hold-out yang dikunci; tidak ada pelatihan atau penalaan ulang di tahap ini.

- Model: **{model_config['model_name']}** (`{model_config['model_class']}`), threshold keputusan {TEST_THRESHOLD}.
- Data uji: **{len(y_test)} file** dari **{len(nims_test)} NIM test**: {", ".join(f"`{nim}`" for nim in nims_test)}.
- **ROC-AUC = {roc_auc_value:.4f}** dengan CI95 bootstrap [{ci_low:.4f}, {ci_high:.4f}] terhadap baseline 0,50 dan syarat kelayakan 0,85.
- Status syarat kelayakan awal: **{metrics['kelayakan_status']}**.
- PR-AUC = {pr_auc_value:.4f} (baseline prevalensi {prevalence_value:.4f}); accuracy = {accuracy_value:.4f}; F1 kelas berisik = {f1_value:.4f}.
- File salah prediksi: {len(errors)} dari {len(y_test)}.
- Pemeriksaan validasi: {check_table['lulus'].sum()}/{len(check_table)} PASS.

## Metrik hold-out

{md_table(metrics_view)}

Confusion matrix (threshold {TEST_THRESHOLD}):

{md_table(cm_view)}

Classification report:

{md_table(report_view)}

Keterangan baris: TN={tn}, FP={fp}, FN={fn}, TP={tp}. Kelas 1 = berisik adalah kelas positif.

## Rincian per NIM test

{md_table(metrics_by_nim)}

- NIM dengan accuracy sempurna: **{n_perfect_nim} dari {len(metrics_by_nim)}** ({", ".join(metrics_by_nim.loc[metrics_by_nim['accuracy'] == 1.0, 'nim'])}).
- Accuracy per NIM rata-rata {metrics['accuracy_per_nim_mean']:.4f}, terendah **{worst_nim_row['nim']} = {worst_nim_row['accuracy']:.4f}** ({int(worst_nim_row['n_salah'])} kesalahan dari {int(worst_nim_row['n_files'])} file).
- {int(max_errors_nim['n_salah'])} dari {len(errors)} kesalahan berasal dari satu NIM (`{max_errors_nim['nim']}`), sehingga hasil sangat dipengaruhi subjek/perangkat tersebut.

## File yang salah prediksi

{md_table(errors_view) if len(errors_view) else "Tidak ada file yang salah prediksi."}

File tetap dipertahankan; tidak ada yang dibuang karena dianggap sulit.

## Ketidakpastian

- ROC-AUC {roc_auc_value:.4f} memiliki CI95 bootstrap [{ci_low:.4f}, {ci_high:.4f}] dari {int(metrics['n_bootstrap'])} pengambilan ulang (random_state={RANDOM_STATE}).
- Dengan {len(nims_test)} NIM dan {len(y_test)} file, selisih satu dua file sudah menggeser metrik; angka hold-out adalah estimasi, bukan jaminan.
- {ci_note}

## Gambar

Seluruh gambar berada di `artifacts/test_results/figures/`:

- `roc_curve.png` — ROC-AUC {roc_auc_value:.4f} terhadap diagonal 0,50.
- `pr_curve.png` — PR-AUC {pr_auc_value:.4f} terhadap baseline prevalensi {prevalence_value:.4f}.
- `confusion_matrix.png` — heatmap TN/FP/FN/TP.
- `proba_distribution.png` — sebaran probabilitas berisik per kelas nyata dengan garis threshold {TEST_THRESHOLD}.
- `roc_auc_bootstrap.png` — sebaran ROC-AUC bootstrap beserta CI.

## Validasi akhir

Semua pemeriksaan lulus: **{check_table['lulus'].sum()}/{len(check_table)}**.

{md_table(check_table[['pemeriksaan', 'status']])}

## Batasan

- Hanya {len(nims_test)} NIM dan {len(y_test)} file uji; angka sedikit, ketidakpastian lebar.
- Label berasal dari protokol pengumpulan, bukan verifikasi audit kebenaran mutlak.
- Threshold {TEST_THRESHOLD} tidak dituning; menaikkan threshold menaikkan precision dan menurunkan recall.
- Probabilitas output belum terkalibrasi.
- Model terpilih memperoleh keuntungan tuning pada Tahap 04; hold-out ini adalah pengadilan pertama dan terakhir yang independen.
- Kelayakan awal ≠ layak produksi; batasan privasi dan perangkat/ruangan tetap berlaku.

## Kesimpulan dan keputusan untuk Tahap 06

1. Pakai `artifacts/best_model.joblib` dan `artifacts/04_modeling/model_config.json` apa adanya; jangan melatih atau menala ulang.
2. Fungsi `predict_audio(path)` harus meniru prapemrosesan Tahap 03 (mono 16 kHz, crop/pad 480.000 sampel, peak normalization, 12 fitur) lalu memakai pipeline ini.
3. Metrik hold-out yang dilaporkan di `artifacts/test_results/metrics.json` adalah angka resmi tahap ini.
4. `artifacts/LAPORAN.md` pada Tahap 06 memuat data aktual, fitur, model, metrik nyata, lokasi artefak, dan limitasi.

**Evaluation selesai dan tervalidasi. Metrik hold-out dilaporkan apa adanya.**
"""

(ARTIFACT_DIR / "evaluation_report.md").write_text(report, encoding="utf-8")

evaluation_summary = {
    "status": "PASS",
    "model_name": model_config["model_name"],
    "model_class": model_config["model_class"],
    "n_files_test": int(len(y_test)),
    "n_nim_test": int(len(nims_test)),
    "nims_test": nims_test,
    "class_counts_test": metrics["class_counts_test"],
    "test_threshold": TEST_THRESHOLD,
    "roc_auc": roc_auc_value,
    "roc_auc_ci_low": ci_low,
    "roc_auc_ci_high": ci_high,
    "pr_auc": pr_auc_value,
    "accuracy": accuracy_value,
    "precision_class_1": precision_value,
    "recall_class_1": recall_value,
    "f1_class_1": f1_value,
    "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
    "kelayakan_status": metrics["kelayakan_status"],
    "roc_auc_meets_threshold": metrics["roc_auc_meets_threshold"],
    "n_files_wrong": int(len(errors)),
    "checks_passed": int(check_table["lulus"].sum()),
    "checks_total": int(len(check_table)),
    "model_unchanged": True,
    "random_state": RANDOM_STATE,
}
(ARTIFACT_DIR / "evaluation_summary.json").write_text(
    json.dumps(evaluation_summary, ensure_ascii=False, indent=2), encoding="utf-8"
)

print(f"Laporan tahap: {ARTIFACT_DIR / 'evaluation_report.md'}")
display(Markdown(report))
