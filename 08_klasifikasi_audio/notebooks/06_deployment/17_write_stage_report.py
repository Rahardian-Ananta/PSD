report = f"""# 06 — Deployment: Laporan Aktual

## Ringkasan

Fungsi **`predict_audio(path)`** dibangun memakai `artifacts/best_model.joblib` **tanpa training ulang**, dengan prapemrosesan identik Tahap 03, dan didemokan pada file asli dataset.

- Model: **{model_config['model_name']}** (pipeline `{' -> '.join(model_config['pipeline_steps'])}`), parameter {model_config['best_params']}, sidik jari file `{model_file_sha256[:16]}...`.
- Identitas model: selisih probabilitas vs `test_predictions.csv` Tahap 05 **{model_identity_max_diff:.3e}** (toleransi 1e-12) — model tidak diganti, tidak di-fit ulang.
- Identitas prapemrosesan: **{identity_summary['n_files_checked']}/176 file** diperiksa; selisih fitur relatif maksimum **{identity_summary['max_feature_rel_diff']:.3e}** (toleransi {FEATURE_REL_TOL:g}), label cocok {identity_summary['label_match_vs_direct_176']}/176.
- Reproduksi Tahap 05: 40/40 label cocok, selisih probabilitas maksimum {identity_summary['test_max_proba_diff_vs_tahap05']:.3e} (toleransi {PROBA_MATCH_TOL:g}); accuracy 40 file uji {identity_summary['test_accuracy_pipeline']:.4f} = accuracy Tahap 05.
- Demo: 2 file utama (satu per kelas) + 2 cabang durasi (pad 10 detik, crop 60 detik), seluruhnya berjalan nyata.
- Laporan akhir: **`artifacts/LAPORAN.md`** ({laporan_size} bytes).
- Pemeriksaan validasi: {check_table['lulus'].sum()}/{len(check_table)} PASS.

## Yang dibangun

Fungsi `predict_audio(path)` (cell `08_predict_audio.py`):

1. `librosa.load(path, sr=16000, mono=True)`;
2. crop/pad tengah ke {TARGET_SAMPLES} sampel;
3. peak normalization `y / max(|y|)`, hasil `float32`;
4. 12 fitur dengan framing {FRAME_LENGTH}/{HOP_LENGTH}, Hann simetris, rFFT {N_FFT};
5. pipeline tersimpan (scaler + seleksi fitur + klasifikasi) -> label pada threshold {TEST_THRESHOLD} beserta probabilitas kedua kelas.

Fungsi menolak file tidak ada dan sinyal peak nol; seluruh konstanta cocok dengan `preprocessing_contract.json`.

## Demo nyata

{md_table(demo_view)}

- Dua file utama diambil deterministik dari 40 file uji dan dijalankan lewat **file MP3 asli** (`data_mp3/`), bukan salinan hasil.
- Hasil dilaporkan apa adanya: file yang keliru tetap ditulis sebagai keliru.
- Cabang `pad` (10 detik) dan `crop` (60 detik) teruji sesuai kontrak durasi.

## Bukti identitas prapemrosesan

{md_table(identity_view)}

Sumber perbedaan yang tersisa hanyalah kuantisasi ulang PCM16 ketika file final dinormalisasi kembali (faktor ~3e-5) — jauh di bawah toleransi dan tidak mengubah satu pun label uji.

## Laporan akhir

`artifacts/LAPORAN.md` memuat: data aktual Tahap 02-03, 12 fitur dan 8 fitur terpilih, model dan konfigurasi Tahap 04, metrik hold-out Tahap 05 **apa adanya** (ROC-AUC {metrics['roc_auc']:.4f}, status {metrics['kelayakan_status']}), cara pemakaian `predict_audio`, lokasi seluruh artefak, serta limitasi dan etika.

## Validasi akhir

Semua pemeriksaan lulus: **{check_table['lulus'].sum()}/{len(check_table)}**.

{md_table(check_table[['pemeriksaan', 'status']])}

## Batasan

- Probabilitas adalah skor model, bukan keyakinan terkalibrasi; threshold {TEST_THRESHOLD} tidak dituning.
- ROC-AUC {metrics['roc_auc']:.4f} tetap **di bawah syarat awal 0,85**; CI95 [{metrics['roc_auc_ci_low']:.4f}, {metrics['roc_auc_ci_high']:.4f}] memuat 0,85.
- Evaluasi hanya {metrics['n_nim_test']} NIM / {metrics['n_files_test']} file; kesalahan menumpuk pada NIM {worst_nim['nim']}.
- Fungsi mengasumsikan audio berdurasi mendekati 30 detik; durasi ekstrem dikenali lewat crop/pad tetapi kualitas prediksi menurun bila bahan utama terbuang.
- Rekaman berisi suara orang: gunakan hanya untuk proyek pembelajaran; tanpa pengenalan pembicara.

## Kesimpulan dan arah lanjut

1. Deployment selesai: `predict_audio(path)` terbukti identik prapemrosesannya untuk 176 file dan mereproduksi evaluasi Tahap 05 untuk 40 file uji.
2. `artifacts/LAPORAN.md` berisi seluruh angka aktual, lokasi artefak, dan limitasi untuk konsumen laporan.
3. Bila kelayakan 0,85 ingin dipenuhi, langkah berikutnya adalah siklus data/model baru (data lebih banyak dan lebih beragam), bukan penilaian ulang pada hold-out yang sama.

**Deployment selesai dan tervalidasi. Tanpa training ulang; metrik dilaporkan apa adanya.**
"""

ARTIFACT_DIR.joinpath("deployment_report.md").write_text(report, encoding="utf-8")

deployment_summary = {
    "status": "PASS",
    "model_name": model_config["model_name"],
    "model_class": model_config["model_class"],
    "model_file_sha256": model_file_sha256,
    "model_identity_max_diff": model_identity_max_diff,
    "predict_audio_callable": True,
    "test_threshold": TEST_THRESHOLD,
    "identity": identity_summary,
    "demo_main": demo_main[["file", "kelas_asli", "prediksi", "proba_berisik", "cocok"]].to_dict(
        orient="records"
    ),
    "demo_duration_actions": {
        row.skenario: row.duration_action for row in demo_results.itertuples()
    },
    "laporan_bytes": int(laporan_size),
    "roc_auc_tahap05": metrics["roc_auc"],
    "kelayakan_status": metrics["kelayakan_status"],
    "checks_passed": int(check_table["lulus"].sum()),
    "checks_total": int(len(check_table)),
    "random_state": RANDOM_STATE,
}
ARTIFACT_DIR.joinpath("deployment_summary.json").write_text(
    json.dumps(deployment_summary, ensure_ascii=False, indent=2), encoding="utf-8"
)

print(f"Laporan tahap: {ARTIFACT_DIR / 'deployment_report.md'}")
display(Markdown(report))
