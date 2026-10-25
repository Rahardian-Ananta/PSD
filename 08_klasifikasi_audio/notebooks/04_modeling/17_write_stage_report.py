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


best_params_text = (
    ", ".join(f"`{key}` = `{value}`" for key, value in saved_config["best_params"].items())
)
split_view = split_summary.reset_index()
comparison_view = comparison.round(4)
grid_top = grid_results.head(5).copy()
grid_top["params"] = grid_top["params"].astype(str)
fold_view = cv_fold_audit

report = f"""# 04 — Modeling: Laporan Aktual

## Ringkasan

Tahap 04 membandingkan empat model pada data latih berbasis NIM, lalu menala kandidat terbaik dengan `GridSearchCV`. Hold-out 20% NIM dikunci lebih dulu dan **belum** disentuh evaluasi.

- Model terpilih: **{best_reference_name}** (`{saved_config['model_class']}`).
- ROC-AUC CV terbaik: **{search.best_score_:.4f}** (std {grid_results.sort_values('rank_test_score').iloc[0]['std_test_score']:.4f}); baseline prior: **{baseline_roc_auc:.4f}**.
- Konfigurasi CV: `GroupKFold(n_splits={N_SPLITS})`, grup = NIM, scoring `{SCORING}`, `random_state={RANDOM_STATE}`.
- Hold-out: {len(nims_test)} NIM test ({len(model_test)} file) dan {len(nims_train)} NIM train ({len(model_train)} file) dari total {len(nims_all)} NIM / {len(features)} file.
- Fitur terpilih setelah refit: {saved_config['n_features_selected']} dari {len(FEATURE_COLUMNS)} fitur, dipelajari di dalam pipeline.
- Pemeriksaan validasi: {check_table['lulus'].sum()}/{len(check_table)} PASS.

## Penguncian hold-out

{md_table(split_view)}

NIM test: {", ".join(f"`{nim}`" for nim in nims_test)}.

NIM ini tidak pernah masuk perbandingan model maupun `GridSearchCV`; uji terhadap NIM tersebut baru dilakukan di Tahap 05.

## Baseline dan perbandingan empat model

Baseline `DummyClassifier(strategy="prior")` memberi ROC-AUC {baseline_roc_auc:.4f} karena dua kelas hampir seimbang. Angka model harus dibaca relatif terhadap baseline ini.

{md_table(comparison_view)}

Selisih ROC-AUC antar fold tersimpan di `cv_fold_audit.csv` dan `cv_fold_scores.csv`. Semua model berada di atas baseline, tetapi peringkat CV ini belum membuktikan generalisasi ke NIM yang belum pernah dilihat.

## GridSearchCV kandidat terbaik

- Model yang ditala: **{best_reference_name}**; kombinasi: **{len(grid_results)}** dengan {N_SPLITS} fold.
- Parameter terbaik: {best_params_text}.
- Skor CV terbaik: **{search.best_score_:.4f}**; skor latih: {grid_results.sort_values('rank_test_score').iloc[0]['mean_train_score']:.4f}.
- Kandidat fitur: `select__k` ikut dicari sehingga jumlah fitur ditentukan di dalam fold latih.

Kandidat terbaik (5 kombinasi teratas):

{md_table(grid_top[['rank_test_score', 'params', 'mean_test_score', 'std_test_score', 'mean_train_score']])}

Audit per fold:

{md_table(fold_view)}

## Artefak model

- `artifacts/best_model.joblib`: pipeline `scaler -> select -> clf` hasil refit pada seluruh NIM train.
- `artifacts/04_modeling/model_config.json`: model, parameter, skor, versi paket, dan daftar NIM train/test.
- `artifacts/04_modeling/feature_list.txt`: daftar 12 fitur beserta catatan jumlah fitur terpilih.
- `artifacts/04_modeling/holdout_split.csv` dan `holdout_file_split.csv`: pembagian terkunci.
- `artifacts/04_modeling/model_comparison.csv`, `grid_search_results.csv`, `cv_fold_scores.csv`, `cv_fold_audit.csv`.
- `artifacts/04_modeling/validation_report.md` dan `validation_summary.json`.
- Gambar: `holdout_composition.png`, `cv_model_comparison.png`, `grid_search_scores.png`.

## Validasi akhir

Semua pemeriksaan lulus: **{check_table['lulus'].sum()}/{len(check_table)}**.

{md_table(check_table[['pemeriksaan', 'status']])}

## Batasan

- Hold-out **belum** dievaluasi; skor {search.best_score_:.4f} adalah CV pada {len(nims_train)} NIM train, bukan angka kelayakan.
- Kelayakan ROC-AUC ≥ 0,85 hanya dinilai pada Tahap 05 terhadap {len(nims_test)} NIM test.
- Kandidat terbaik memperoleh keuntungan tuning, sementara tiga model lain memakai parameter bawaan; perbandingan adil akhir ada di hasil hold-out.
- Seleksi fitur (`SelectKBest` berbasis ANOVA) bergantung pada fold; daftar fitur terpilih pada pipeline dapat berbeda dari kandidat eksploratif Tahap 03.
- Probabilitas keluaran (terutama `SVC(probability=True)`) adalah skor model, bukan probabilitas terkalibrasi.
- Tidak ada PCA, tidak ada data karantina yang dipakai, dan `raw_audio/` tidak diubah.

## Kesimpulan dan keputusan untuk Tahap 05

1. Muat `artifacts/best_model.joblib` dan `artifacts/04_modeling/model_config.json`; jangan melatih ulang model.
2. Pakai **hanya** NIM test: {", ".join(f"`{nim}`" for nim in nims_test)}; NIM train tidak boleh muncul di metrik hold-out.
3. Ekstraksi fitur pada file uji harus identik dengan Tahap 03 (kontrak `preprocessing_contract.json`).
4. Laporkan ROC-AUC, PR-AUC, precision, recall, F1, accuracy, confusion matrix, dan classification report, lengkap dengan jumlah NIM test.
5. Bandingkan hasil dengan baseline 0,50 dan syarat kelayakan ROC-AUC ≥ 0,85; bila di bawah syarat, laporkan apa adanya.

**Modeling selesai dan tervalidasi. Hold-out belum diuji.**
"""

(ARTIFACT_DIR / "modeling_report.md").write_text(report, encoding="utf-8")

modeling_summary = {
    "status": "PASS",
    "model_name": best_reference_name,
    "model_class": saved_config["model_class"],
    "best_cv_roc_auc": float(search.best_score_),
    "baseline_cv_roc_auc": baseline_roc_auc,
    "n_combinations": int(len(grid_results)),
    "best_params": saved_config["best_params"],
    "n_features_selected": int(saved_config["n_features_selected"]),
    "selected_features_final": saved_config["selected_features_final"],
    "n_nim_train": len(nims_train),
    "n_nim_test": len(nims_test),
    "n_files_train": int(len(model_train)),
    "n_files_test": int(len(model_test)),
    "n_splits": N_SPLITS,
    "scoring": SCORING,
    "random_state": RANDOM_STATE,
    "nims_test": nims_test,
    "holdout_tested_in_stage_04": False,
}
(ARTIFACT_DIR / "modeling_summary.json").write_text(
    json.dumps(modeling_summary, ensure_ascii=False, indent=2), encoding="utf-8"
)

print(f"Laporan tahap: {ARTIFACT_DIR / 'modeling_report.md'}")
display(Markdown(report))
