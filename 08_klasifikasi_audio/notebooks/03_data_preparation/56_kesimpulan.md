## Kesimpulan dan keputusan untuk tahap 04

1. **Jumlah aktual:** 176 file final dari 200 file mentah, 24 file dikarantina dengan salinan dan alasan. Dataset final: **34 NIM**, **88 non-berisik : 88 berisik**, semua NIM memiliki kedua kelas. NIM `24-123` gugur karena seluruh file-nya menjadi duplikat non-wakil.
2. **Duplikasi selesai:** dari 18 grup duplikat eksak Tahap 02, 1 grup lintas label (DUP04) dikarantina seluruhnya dan 17 grup same-label memilih satu wakil. Kombinasi yang dievaluasi **995.328**; solusi terpilih memberi 34 NIM dua kelas dan 0 NIM satu kelas.
3. **Format seragam:** `data_mp3/` adalah salinan byte-identik 176 MP3 (bukan transcode ganda), `data_final/` adalah 176 WAV PCM_16 mono 16000 Hz tepat 480.000 sampel dengan peak normalization. `raw_audio/` tidak diubah: 200 file dan seluruh SHA-256 cocok manifest Tahap 02.
4. **Fitur:** 12 fitur terekstrak manual (frame 400, hop 160, Hann simetris, N_FFT 512, 2.998 frame per file). `features.csv` berisi 176 baris tanpa NaN/Inf dan seluruh rentang fitur valid. Pemeriksaan rFFT vs FFT penuh selisih maksimum 1.819e-12.
5. **Frame hening:** 1.677 frame daya-nol pada 52 file. Frame tidak dihapus; centroid, flatness, rolloff, dan bandwidth frame tersebut ditetapkan 0. Hening adalah bagian data, bukan missing value.
6. **Validasi:** 28/28 pemeriksaan **PASS**; traceability `raw_audio -> data_mp3 -> data_final -> features.csv` lengkap dan 176 hash WAV unik.
7. **Kandidat fitur:** 8 kandidat eksploratif (`rms_mean`, `mse_energy`, `rms_std`, `spectral_rolloff_mean`, `spectral_centroid_mean`, `zcr_mean`, `rms_max`, `spectral_centroid_std`). Angka-angka pemilihan fitur bersifat eksploratif dan wajib dipelajari ulang di dalam training fold.
8. **Rencana 04:** split berbasis NIM (hold-out per NIM dan/atau GroupKFold/StratifiedGroupKFold), satu `Pipeline` berisi seleksi fitur, scaling, dan model agar tidak ada kebocoran preprocessing, lalu `GridSearchCV`, evaluasi hold-out per NIM, dan penyimpanan `best_model.joblib`. Tidak ada PCA.

**Data Preparation selesai dan tervalidasi. Model belum dilatih.**
