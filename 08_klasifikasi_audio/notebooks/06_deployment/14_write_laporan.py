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


metrics_by_nim = pd.read_csv(ARTIFACT_ROOT / "test_results" / "metrics_by_nim.csv")
worst_nim = metrics_by_nim.loc[metrics_by_nim["accuracy"].idxmin()]
cm = metrics["confusion_matrix"]

data_view = pd.DataFrame(
    {
        "besaran": [
            "File awal (raw_audio)",
            "File final",
            "File karantina",
            "NIM final",
            "Distribusi kelas",
            "NIM gugur",
            "Format final",
            "Durasi",
            "Frame daya nol",
        ],
        "nilai": [
            stage3_summary["n_raw"],
            stage3_summary["n_final"],
            stage3_summary["n_quarantine"],
            stage3_summary["n_nim_final"],
            f"{stage3_summary['class_counts']['0']} non-berisik : {stage3_summary['class_counts']['1']} berisik",
            ", ".join(stage3_summary["dropped_nims"]),
            "WAV PCM_16, mono, 16000 Hz",
            f"{stage3_summary['target_samples']} sampel (30 detik)",
            f"{stage3_summary['n_zero_power_frames']} pada {stage3_summary['n_files_with_zero_power_frames']} file",
        ],
    }
)

feature_view = pd.DataFrame(
    {
        "posisi": ["Input model (12)", "Dipakai classifier (8)"],
        "daftar": [
            ", ".join(FEATURE_COLUMNS),
            ", ".join(selected_from_model),
        ],
    }
)

model_view = pd.DataFrame(
    {
        "komponen": [
            "Algoritma",
            "Pipeline",
            "Parameter terbaik",
            "ROC-AUC CV (GroupKFold 5, grup=NIM)",
            "Baseline dummy",
            "Hold-out",
            "NIM train / test",
            "random_state",
            "Sidik jari file model (sha256)",
            "Versi scikit-learn",
        ],
        "nilai": [
            model_config["model_name"],
            " -> ".join(model_config["pipeline_steps"]),
            str(model_config["best_params"]),
            f"{model_config['best_cv_roc_auc']:.4f}",
            f"{model_config['baseline_cv_roc_auc']:.4f}",
            f"{model_config['holdout']['splitter']} test_size={model_config['holdout']['test_size']}",
            f"{model_config['holdout']['n_nim_train']} NIM ({model_config['holdout']['n_files_train']} file) / "
            f"{model_config['holdout']['n_nim_test']} NIM ({model_config['holdout']['n_files_test']} file)",
            model_config["random_state"],
            model_file_sha256,
            model_config["library_versions"]["scikit-learn"],
        ],
    }
)

eval_view = pd.DataFrame(
    {
        "metrik": [
            "ROC-AUC",
            "CI95 bootstrap",
            "PR-AUC",
            "accuracy",
            "precision (berisik)",
            "recall (berisik)",
            "F1 (berisik)",
            "Confusion matrix",
            "File salah prediksi",
            "Status syarat ROC-AUC >= 0,85",
        ],
        "nilai": [
            f"{metrics['roc_auc']:.4f}",
            f"[{metrics['roc_auc_ci_low']:.4f}, {metrics['roc_auc_ci_high']:.4f}]",
            f"{metrics['pr_auc']:.4f}",
            f"{metrics['accuracy']:.4f}",
            f"{metrics['precision_class_1']:.4f}",
            f"{metrics['recall_class_1']:.4f}",
            f"{metrics['f1_class_1']:.4f}",
            f"TN {cm['tn']} / FP {cm['fp']} / FN {cm['fn']} / TP {cm['tp']}",
            f"{metrics['n_files_wrong']} dari {metrics['n_files_test']}",
            metrics["kelayakan_status"],
        ],
        "acuan": [
            "baseline 0,5000",
            f"{metrics['n_bootstrap']} pengambilan ulang, random_state={metrics['random_state']}",
            f"baseline prevalensi {int(metrics['class_counts_test']['1']) / metrics['n_files_test']:.4f}",
            "40 file uji",
            "kelas positif = berisik",
            "kelas positif = berisik",
            "precision dan recall",
            "threshold 0,50",
            f"terbanyak di NIM {worst_nim['nim']} ({int(worst_nim['n_salah'])} kesalahan)",
            "syarat kelayakan awal",
        ],
    }
)

identity_view = pd.DataFrame(
    {
        "pemeriksaan": [
            "File diperiksa ulang dengan predict_audio",
            "Label cocok vs pipeline langsung",
            "Selisih fitur relatif maksimum",
            "Label cocok vs Tahap 05 (40 file uji)",
            "Selisih probabilitas vs Tahap 05",
            "Accuracy 40 file uji",
        ],
        "nilai": [
            identity_summary["n_files_checked"],
            f"{identity_summary['label_match_vs_direct_176']} / 176",
            f"{identity_summary['max_feature_rel_diff']:.3e}",
            f"{identity_summary['test_label_match_vs_tahap05']} / 40",
            f"{identity_summary['test_max_proba_diff_vs_tahap05']:.3e}",
            f"{identity_summary['test_accuracy_pipeline']:.4f}",
        ],
    }
)

demo_view = demo_results[
    [
        "skenario",
        "file",
        "kelas_asli",
        "prediksi",
        "proba_berisik",
        "cocok",
        "duration_action",
        "durasi_asli_detik",
    ]
]

usage_snippet = """import joblib
from pathlib import Path

# definisi predict_audio ada di notebooks/06_deployment/08_predict_audio.py
model = joblib.load("artifacts/best_model.joblib")
result = predict_audio("data_final/24-068_berisik_1.wav")
print(result["label_name"], result["proba_berisik"])"""

laporan = f"""# LAPORAN Akhir — Klasifikasi Audio Berisik vs Non-Berisik

**Proyek:** Proyek Sains Data A (PSD-A), Universitas Trunojoyo Madura
**Pendekatan:** CRISP-DM (Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment)
**Tanggal laporan:** {pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M UTC")}
**Model:** {model_config["model_name"]} — pipeline `{" -> ".join(model_config["pipeline_steps"])}`

## 1. Ringkasan eksekutif

Model membedakan rekaman kelas **berisik (1)** vs **non-berisik (0)** dari 12 fitur akustik pada audio 30 detik, dan diserahkan sebagai fungsi `predict_audio(path)`.

- **ROC-AUC hold-out = {metrics['roc_auc']:.4f}** (CI95 bootstrap [{metrics['roc_auc_ci_low']:.4f}, {metrics['roc_auc_ci_high']:.4f}], baseline 0,50).
- **Status syarat kelayakan awal ROC-AUC >= 0,85: {metrics['kelayakan_status']}** — dilaporkan apa adanya, tidak disesuaikan.
- Accuracy {metrics['accuracy']:.4f}, precision {metrics['precision_class_1']:.4f}, recall {metrics['recall_class_1']:.4f}, F1 {metrics['f1_class_1']:.4f} pada 40 file uji (7 NIM hold-out); {metrics['n_files_wrong']} file salah prediksi.
- Deployment: prapemrosesan identik Tahap 03 terbukti untuk **{identity_summary['n_files_checked']} file**; demo nyata berjalan pada file MP3 asli.

## 2. Data aktual

{md_table(data_view)}

Catatan: 24 file karantina adalah duplikat hasil seleksi hash, tetap disimpan untuk audit; `raw_audio/` berisi 200 file dan tidak diubah.

## 3. Fitur

{md_table(feature_view)}

Parameter ekstraksi: sr={SR} Hz, frame_length={FRAME_LENGTH}, hop_length={HOP_LENGTH}, n_fft={N_FFT}, window Hann simetris, tanpa `center`, rolloff {ROLLOFF_PERCENT}, epsilon `{EPS:.3e}`; kontrak lengkap di `artifacts/03_data_preparation/preprocessing_contract.json`. Scaling dan seleksi fitur dipelajari **di dalam pipeline** pada data latih, bukan di muka data.

## 4. Model dan validasi (Tahap 04)

{md_table(model_view)}

## 5. Evaluasi hold-out (Tahap 05)

Diuji **sekali** pada 7 NIM test yang dikunci sejak Tahap 04; model tidak di-fit ulang.

{md_table(eval_view)}

Rincian per NIM test:

{md_table(metrics_by_nim)}

## 6. Deployment

Pemakaian:

```python
{usage_snippet}
```

Fungsi `predict_audio` melakukan: dekode `librosa.load(sr=16000, mono=True)` -> crop/pad tengah ke {TARGET_SAMPLES} sampel -> peak normalization -> 12 fitur -> pipeline tersimpan -> label dan probabilitas (threshold {TEST_THRESHOLD}).

### Demo nyata

{md_table(demo_view)}

### Bukti identitas prapemrosesan

{md_table(identity_view)}

## 7. Lokasi artefak

- `artifacts/best_model.joblib` — model pipeline siap pakai.
- `artifacts/features.csv` — 176 baris fitur Tahap 03.
- `artifacts/02_data_understanding/`, `artifacts/03_data_preparation/` — laporan data dan manifest.
- `artifacts/04_modeling/` — konfigurasi model, split hold-out, laporan modeling.
- `artifacts/test_results/` — prediksi, metrik, confusion, per-NIM, kesalahan, dan 5 gambar evaluasi.
- `artifacts/05_evaluation/` — laporan evaluasi dan validasi.
- `artifacts/06_deployment/` — bukti identitas, hasil demo, laporan, dan validasi tahap ini.
- `notebooks/06_deployment/` — sumber cell notebook deployment.

## 8. Limitasi dan etika

1. **Kelayakan:** ROC-AUC {metrics['roc_auc']:.4f} **di bawah syarat awal 0,85**, dan CI95 [{metrics['roc_auc_ci_low']:.4f}, {metrics['roc_auc_ci_high']:.4f}] memuat 0,85 — kelayakan pada populasi tidak dapat dipastikan dari 40 file ini saja.
2. **Jumlah kecil:** hanya {metrics['n_nim_test']} NIM test / {metrics['n_files_test']} file; {int(worst_nim['n_salah'])} dari {metrics['n_files_wrong']} kesalahan menumpuk pada NIM `{worst_nim['nim']}`.
3. **Probabilitas** adalah skor model, belum terkalibrasi; threshold {TEST_THRESHOLD} tidak dituning.
4. **Label** berasal dari protokol pengumpulan, bukan audit kebenaran mutlak.
5. **Privasi:** rekaman berisi suara orang; gunakan hanya untuk proyek pembelajaran, batasi akses, jangan melakukan pengenalan pembicara.
6. **Bukan penilai disiplin:** alat ini penyaringan awal, bukan pengganti observasi manusia; batas perangkat/ruangan berlaku.

## 9. Kesimpulan

1. Pipeline CRISP-DM lengkap 01-06 berjalan dari 200 file mentah menjadi model teruji dan fungsi prediksi yang terbukti identik prapemrosesannya.
2. Metrik hold-out dilaporkan apa adanya, termasuk status {metrics["kelayakan_status"].lower()} terhadap syarat 0,85.
3. `predict_audio(path)` siap dipakai dengan artefak yang ada; perbaikan selanjutnya (bila diperlukan) harus melalui siklus data/model baru, bukan penalaan pada data uji.
"""

LAPORAN_PATH.write_text(laporan, encoding="utf-8")
assert LAPORAN_PATH.is_file() and LAPORAN_PATH.stat().st_size > 3000

print(f"Laporan akhir: {LAPORAN_PATH} ({LAPORAN_PATH.stat().st_size} bytes)")
display(Markdown(laporan))
