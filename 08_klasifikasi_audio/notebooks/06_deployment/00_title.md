# 06 — Deployment

Notebook ini menjalankan tahap **Deployment** CRISP-DM untuk klasifikasi biner audio:

- `1 = berisik`
- `0 = non-berisik`

Tujuan tahap ini adalah membangun **`predict_audio(path)`** yang melakukan prapemrosesan identik dengan Tahap 03, memakai model tersimpan dari Tahap 04 **tanpa training ulang**, mendemokan fungsi pada file asli dataset, dan menulis laporan akhir `artifacts/LAPORAN.md` berisi data aktual, fitur, model, metrik nyata, lokasi artefak, dan limitasi.

## Masukan

- `artifacts/best_model.joblib` dan `artifacts/04_modeling/model_config.json`.
- `artifacts/03_data_preparation/preprocessing_contract.json`: kontrak prapemrosesan yang wajib diikuti.
- `artifacts/features.csv` dan `artifacts/03_data_preparation/transformation_manifest.csv`.
- `artifacts/04_modeling/holdout_file_split.csv` dan `artifacts/test_results/` dari Tahap 05.
- `data_mp3/` dan `data_final/` untuk demo.

## Keluaran utama

- Fungsi `predict_audio(path)` di notebook ini (cell `08_predict_audio.py`).
- `artifacts/06_deployment/feature_identity_check.csv` dan `identity_summary.json`: bukti prapemrosesan identik untuk 176 file.
- `artifacts/06_deployment/demo_results.csv`: hasil demo nyata (dua kelas) plus uji cabang crop/pad.
- `artifacts/LAPORAN.md`: laporan akhir proyek.
- `artifacts/06_deployment/`: laporan dan validasi tahap.

## Batasan yang dipegang

1. Model **tidak** di-fit ulang, tidak ada penalaan threshold, tidak ada pemilihan fitur baru.
2. Probabilitas keluaran adalah skor model, bukan keyakinan terkalibrasi.
3. Syarat kelayakan awal ROC-AUC ≥ 0,85 dilaporkan **apa adanya** dari Tahap 05.
4. Demo memakai file asli dataset; seluruh angka berasal dari eksekusi nyata; `raw_audio/` tidak diubah.
