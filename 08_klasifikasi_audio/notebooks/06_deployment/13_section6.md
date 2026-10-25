## 6. Laporan akhir `artifacts/LAPORAN.md`

Dokumen wajib akhir proyek adalah `artifacts/LAPORAN.md`. Isinya mengikuti ketentuan Tahap 06:

1. **Data aktual** — 176 file final, 34 NIM, kelas 88:88, 24 file karantina, format WAV PCM_16 mono 16 kHz × 480.000 sampel, ditulis dari ringkasan Tahap 02–03.
2. **Fitur** — 12 fitur akustik, parameter framing/FFT, dan 8 fitur yang benar-benar dipakai model (hasil `SelectKBest` di dalam pipeline).
3. **Model** — Logistic Regression dalam pipeline `scaler -> select -> clf`, parameter terbaik, skor CV GroupKFold, pembagian hold-out, dan sidik jari file.
4. **Metrik nyata** — hasil hold-out Tahap 05 apa adanya, termasuk status **DI BAWAH SYARAT AWAL 0,85** beserta confidence interval bootstrap.
5. **Deployment** — cara memakai `predict_audio`, hasil demo nyata, dan bukti identitas prapemrosesan 176 file.
6. **Lokasi artefak** dan **limitasi/etika** — privasi, kecilnya jumlah NIM, probabilitas tidak terkalibrasi, dan batas penggunaan alat.

Laporan ditulis dari variabel hasil komputasi (bukan angka ketik manual), disimpan ke `artifacts/LAPORAN.md`, dan dirender di notebook.
