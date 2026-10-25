# LAPORAN Akhir — Klasifikasi Audio Berisik vs Non-Berisik

**Proyek:** Proyek Sains Data A (PSD-A), Universitas Trunojoyo Madura
**Pendekatan:** CRISP-DM (Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment)
**Tanggal laporan:** 2026-10-24 02:42 UTC
**Model:** Logistic Regression — pipeline `scaler -> select -> clf`

## 1. Ringkasan eksekutif

Model membedakan rekaman kelas **berisik (1)** vs **non-berisik (0)** dari 12 fitur akustik pada audio 30 detik, dan diserahkan sebagai fungsi `predict_audio(path)`.

- **ROC-AUC hold-out = 0.8296** (CI95 bootstrap [0.6767, 0.9549], baseline 0,50).
- **Status syarat kelayakan awal ROC-AUC >= 0,85: DI BAWAH SYARAT AWAL** — dilaporkan apa adanya, tidak disesuaikan.
- Accuracy 0.7750, precision 0.7500, recall 0.7895, F1 0.7692 pada 40 file uji (7 NIM hold-out); 9 file salah prediksi.
- Deployment: prapemrosesan identik Tahap 03 terbukti untuk **176 file**; demo nyata berjalan pada file MP3 asli.

## 2. Data aktual

| besaran | nilai |
|---|---|
| File awal (raw_audio) | 200 |
| File final | 176 |
| File karantina | 24 |
| NIM final | 34 |
| Distribusi kelas | 88 non-berisik : 88 berisik |
| NIM gugur | 24-123 |
| Format final | WAV PCM_16, mono, 16000 Hz |
| Durasi | 480000 sampel (30 detik) |
| Frame daya nol | 1677 pada 52 file |

Catatan: 24 file karantina adalah duplikat hasil seleksi hash, tetap disimpan untuk audit; `raw_audio/` berisi 200 file dan tidak diubah.

## 3. Fitur

| posisi | daftar |
|---|---|
| Input model (12) | mse_energy, rms_mean, rms_std, rms_max, rms_min, zcr_mean, zcr_std, spectral_centroid_mean, spectral_centroid_std, spectral_flatness_mean, spectral_rolloff_mean, spectral_bandwidth_mean |
| Dipakai classifier (8) | mse_energy, rms_mean, rms_std, rms_max, rms_min, zcr_mean, spectral_centroid_mean, spectral_rolloff_mean |

Parameter ekstraksi: sr=16000 Hz, frame_length=400, hop_length=160, n_fft=512, window Hann simetris, tanpa `center`, rolloff 0.85, epsilon `2.220e-16`; kontrak lengkap di `artifacts/03_data_preparation/preprocessing_contract.json`. Scaling dan seleksi fitur dipelajari **di dalam pipeline** pada data latih, bukan di muka data.

## 4. Model dan validasi (Tahap 04)

| komponen | nilai |
|---|---|
| Algoritma | Logistic Regression |
| Pipeline | scaler -> select -> clf |
| Parameter terbaik | {'clf__C': 10.0, 'select__k': 8} |
| ROC-AUC CV (GroupKFold 5, grup=NIM) | 0.8442 |
| Baseline dummy | 0.5000 |
| Hold-out | GroupShuffleSplit test_size=0.2 |
| NIM train / test | 27 NIM (136 file) / 7 NIM (40 file) |
| random_state | 42 |
| Sidik jari file model (sha256) | 964a1550c9c06123e00599a17546de694e64de19aee833a771c9d6ceaa35390a |
| Versi scikit-learn | 1.8.0 |

## 5. Evaluasi hold-out (Tahap 05)

Diuji **sekali** pada 7 NIM test yang dikunci sejak Tahap 04; model tidak di-fit ulang.

| metrik | nilai | acuan |
|---|---|---|
| ROC-AUC | 0.8296 | baseline 0,5000 |
| CI95 bootstrap | [0.6767, 0.9549] | 2000 pengambilan ulang, random_state=42 |
| PR-AUC | 0.8481 | baseline prevalensi 0.4750 |
| accuracy | 0.7750 | 40 file uji |
| precision (berisik) | 0.7500 | kelas positif = berisik |
| recall (berisik) | 0.7895 | kelas positif = berisik |
| F1 (berisik) | 0.7692 | precision dan recall |
| Confusion matrix | TN 16 / FP 5 / FN 4 / TP 15 | threshold 0,50 |
| File salah prediksi | 9 dari 40 | terbanyak di NIM 24-168 (5 kesalahan) |
| Status syarat ROC-AUC >= 0,85 | DI BAWAH SYARAT AWAL | syarat kelayakan awal |

Rincian per NIM test:

| nim | n_files | n_class_0 | n_class_1 | n_benar | n_pred_1 | n_salah | accuracy |
|---|---|---|---|---|---|---|---|
| 24-068 | 6 | 3 | 3 | 4 | 5 | 2 | 0.6667 |
| 24-100 | 6 | 3 | 3 | 6 | 3 | 0 | 1 |
| 24-119 | 6 | 3 | 3 | 6 | 3 | 0 | 1 |
| 24-131 | 6 | 3 | 3 | 6 | 3 | 0 | 1 |
| 24-145 | 6 | 3 | 3 | 4 | 3 | 2 | 0.6667 |
| 24-168 | 6 | 3 | 3 | 1 | 2 | 5 | 0.1667 |
| 24-169 | 4 | 3 | 1 | 4 | 1 | 0 | 1 |

## 6. Deployment

Pemakaian:

```python
import joblib
from pathlib import Path

# definisi predict_audio ada di notebooks/06_deployment/08_predict_audio.py
model = joblib.load("artifacts/best_model.joblib")
result = predict_audio("data_final/24-068_berisik_1.wav")
print(result["label_name"], result["proba_berisik"])
```

Fungsi `predict_audio` melakukan: dekode `librosa.load(sr=16000, mono=True)` -> crop/pad tengah ke 480000 sampel -> peak normalization -> 12 fitur -> pipeline tersimpan -> label dan probabilitas (threshold 0.5).

### Demo nyata

| skenario | file | kelas_asli | prediksi | proba_berisik | cocok | duration_action | durasi_asli_detik |
|---|---|---|---|---|---|---|---|
| demo_utama | 24-068_non-berisik_1.mp3 | non-berisik | berisik | 0.740319 | False | none | 30 |
| demo_utama | 24-068_berisik_1.mp3 | berisik | berisik | 0.911437 | True | none | 30 |
| cabang_pad_10_detik | demo_10_detik.wav | non-berisik | non-berisik | 0.0516325 | True | pad | 10 |
| cabang_crop_60_detik | demo_60_detik.wav | non-berisik | berisik | 0.85682 | False | crop | 60 |

### Bukti identitas prapemrosesan

| pemeriksaan | nilai |
|---|---|
| File diperiksa ulang dengan predict_audio | 176 |
| Label cocok vs pipeline langsung | 176 / 176 |
| Selisih fitur relatif maksimum | 6.105e-05 |
| Label cocok vs Tahap 05 (40 file uji) | 40 / 40 |
| Selisih probabilitas vs Tahap 05 | 2.342e-05 |
| Accuracy 40 file uji | 0.7750 |

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

1. **Kelayakan:** ROC-AUC 0.8296 **di bawah syarat awal 0,85**, dan CI95 [0.6767, 0.9549] memuat 0,85 — kelayakan pada populasi tidak dapat dipastikan dari 40 file ini saja.
2. **Jumlah kecil:** hanya 7 NIM test / 40 file; 5 dari 9 kesalahan menumpuk pada NIM `24-168`.
3. **Probabilitas** adalah skor model, belum terkalibrasi; threshold 0.5 tidak dituning.
4. **Label** berasal dari protokol pengumpulan, bukan audit kebenaran mutlak.
5. **Privasi:** rekaman berisi suara orang; gunakan hanya untuk proyek pembelajaran, batasi akses, jangan melakukan pengenalan pembicara.
6. **Bukan penilai disiplin:** alat ini penyaringan awal, bukan pengganti observasi manusia; batas perangkat/ruangan berlaku.

## 9. Kesimpulan

1. Pipeline CRISP-DM lengkap 01-06 berjalan dari 200 file mentah menjadi model teruji dan fungsi prediksi yang terbukti identik prapemrosesannya.
2. Metrik hold-out dilaporkan apa adanya, termasuk status di bawah syarat awal terhadap syarat 0,85.
3. `predict_audio(path)` siap dipakai dengan artefak yang ada; perbaikan selanjutnya (bila diperlukan) harus melalui siklus data/model baru, bukan penalaan pada data uji.
