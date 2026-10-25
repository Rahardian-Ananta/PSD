# 03 — Data Preparation: Laporan Aktual

## Ringkasan

Dataset final Tahap 03 berisi **176 file**, **34 NIM**, dan distribusi **88 non-berisik : 88 berisik**. Semua NIM final memiliki kedua kelas.

- File awal: 200.
- File final: 176.
- File dikarantina: 24 (salinan, bukan pemindahan dari `raw_audio/`).
- Grup duplikat same-label: 17; wakil dipilih: 17.
- NIM yang hilang dari dataset final: 24-123.
- `24-123` tidak punya file final karena seluruh file-nya menjadi duplikat non-wakil.

## Seleksi dan duplikasi

Pemilihan wakil memakai hash SHA-256, bukan kemiripan audio. Duplikat lintas label tidak dipertahankan. Duplikat same-label dipilih satu wakil per hash dengan prioritas: jumlah NIM yang memiliki kedua kelas, jumlah NIM terwakili, lalu menekan NIM satu kelas.

Kombinasi yang dievaluasi: **995,328**. Solusi terpilih memiliki **34 NIM dua kelas**, **0 NIM satu kelas**, dan **34 NIM terwakili**.

File duplikat lintas label yang dikarantina:

| file | nim | label_name | duplicate_group_id |
|---|---|---|---|
| 24-034_berisik_1.mp3 | 24-034 | berisik | DUP04 |
| 24-034_non-berisik_1.mp3 | 24-034 | non-berisik | DUP04 |

## Audio final

- `data_mp3/`: 176 file, seluruhnya salinan byte-identik karena sumber sudah MP3.
- `data_final/`: 176 WAV.
- Format: WAV PCM_16, mono, 16000 Hz.
- Panjang: tepat 480000 sampel = 30 detik.
- Aksi durasi: {'none': 176}.
- Peak sebelum normalisasi: min 0.02124, median 0.58248, max 1.34783.
- Peak WAV setelah PCM16: min 0.99997, max 1.00000.
- Semua WAV memiliki hash unik: True.

Kontrak preprocessing lengkap tersimpan di `artifacts/03_data_preparation/preprocessing_contract.json`.

## Fitur

- Jumlah fitur: 12.
- Jumlah frame per file: 2998 (frame 400 sampel, hop 160, tanpa `center=True`).
- Window: Hann simetris 400 sampel.
- FFT: 512 titik; 257 bin rFFT; resolusi 31.25 Hz.
- Pemeriksaan rFFT vs FFT penuh, selisih daya maksimum: 1.819e-12.
- Frame dengan daya nol: 1677 pada 52 file. Hening tidak dihapus; fitur spektral frame tersebut ditetapkan 0.
- `features.csv`: 176 baris, tanpa NaN/Inf, seluruh rentang fitur valid.

### Korelasi tinggi (|r| > 0,90)

| feature_1 | feature_2 | pearson_r | abs_r |
|---|---|---|---|
| zcr_std | spectral_centroid_std | 0.986955 | 0.986955 |
| zcr_mean | spectral_centroid_mean | 0.986658 | 0.986658 |
| spectral_centroid_mean | spectral_rolloff_mean | 0.983018 | 0.983018 |
| zcr_mean | spectral_rolloff_mean | 0.982277 | 0.982277 |
| mse_energy | rms_mean | 0.963291 | 0.963291 |

Korelasi tinggi ditandai, tetapi tidak ada fitur yang dihapus otomatis.

### Cohen's d teratas

| feature | mean_non_berisik | mean_berisik | pooled_sd | cohens_d |
|---|---|---|---|---|
| rms_mean | 0.0615274 | 0.109967 | 0.0429107 | 1.12885 |
| mse_energy | 0.00745723 | 0.0196392 | 0.0116492 | 1.04574 |
| rms_std | 0.0467297 | 0.0677468 | 0.0201577 | 1.04263 |
| rms_max | 0.394431 | 0.45196 | 0.105703 | 0.544251 |
| spectral_centroid_mean | 656.283 | 825.702 | 365.16 | 0.463961 |

### Mutual information teratas

| feature | mutual_info | mi_rank |
|---|---|---|
| rms_mean | 0.153564 | 1 |
| mse_energy | 0.129229 | 2 |
| spectral_rolloff_mean | 0.115857 | 3 |
| rms_std | 0.0819795 | 4 |
| zcr_mean | 0.061038 | 5 |

### Random Forest importance teratas

| feature | rf_importance | rf_rank |
|---|---|---|
| mse_energy | 0.147023 | 1 |
| rms_mean | 0.131773 | 2 |
| rms_std | 0.117807 | 3 |
| spectral_centroid_mean | 0.0989899 | 4 |
| spectral_rolloff_mean | 0.0875027 | 5 |

### Kandidat top-8

Kandidat dipilih dari rata-rata peringkat mutual information dan Random Forest importance:

- rms_mean
- mse_energy
- rms_std
- spectral_rolloff_mean
- spectral_centroid_mean
- zcr_mean
- rms_max
- spectral_centroid_std

Kandidat ini **eksploratif**. Seleksi final dan scaling wajib dipelajari ulang di dalam `Pipeline` pada training fold Tahap 04. Tidak ada PCA.

## Pengecekan librosa

| feature | manual_mean | librosa_mean | mean_abs_difference | pearson_r | note |
|---|---|---|---|---|---|
| spectral_centroid_mean | 740.993 | 1467.94 | 726.948 | 0.894871 | manual=P, librosa=magnitudo |
| spectral_bandwidth_mean | 674.805 | 1478.61 | 803.804 | 0.78573 | manual=P, librosa=magnitudo |
| spectral_rolloff_mean | 1170.78 | 2904.78 | 1734 | 0.793539 | manual=P, librosa=magnitudo |
| spectral_flatness_mean | 0.0235638 | 0.0268005 | 0.00323671 | 0.776373 | manual=P, librosa=magnitudo |
| zcr_mean | 0.111755 | 0.11296 | 0.00133051 | 0.996371 | konvensi zero-crossing dapat berbeda di tepi frame |

Perbedaan centroid, bandwidth, rolloff, dan flatness sebagian berasal dari definisi manual berbasis daya \(P=|S|^2\) versus librosa berbasis magnitudo. ZCR dapat berbeda karena konvensi tepi frame.

## Validasi akhir

Semua pemeriksaan lulus: **28/28**.

| pemeriksaan | status |
|---|---|
| file_awal_200 | PASS |
| file_final_176 | PASS |
| file_karantina_24 | PASS |
| final_plus_karantina_200 | PASS |
| data_mp3_176 | PASS |
| data_final_176 | PASS |
| quarantine_24_mp3 | PASS |
| raw_tetap_200 | PASS |
| features_176 | PASS |
| features_unik | PASS |
| fitur_lengkap_12 | PASS |
| fitur_numerik | PASS |
| fitur_tanpa_nan | PASS |
| fitur_tanpa_inf | PASS |
| rentang_fitur_valid | PASS |
| file_identitas_unik | PASS |
| kelas_seimbang_88_88 | PASS |
| nim_final_34 | PASS |
| semua_nim_dua_kelas | PASS |
| semua_audio_valid | PASS |
| final_hash_unik | PASS |
| traceability_lengkap | PASS |
| rfft_fft_konsisten | PASS |
| librosa_comparison_5_fitur | PASS |
| top8_kandidat | PASS |
| top8_semua_ada | PASS |
| tidak_ada_nim_satu_kelas | PASS |
| silent_frames_terdokumentasi | PASS |

Traceability `raw_audio -> data_mp3 -> data_final -> features.csv` lengkap untuk 176 file.

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
