# Laporan Validasi Tahap 06

Status: **PASS**

## Angka aktual
- Model: Logistic Regression (pipeline scaler -> select -> clf)
- Sidik jari file model: `964a1550c9c06123e00599a17546de694e64de19aee833a771c9d6ceaa35390a`
- File diperiksa identitas prapemrosesan: 176
- Selisih fitur relatif maksimum: 6.105e-05
- Label cocok vs Tahap 05 (40 file uji): 40/40
- Selisih probabilitas vs Tahap 05: 2.342e-05
- Demo: 24-068_non-berisik_1.mp3, 24-068_berisik_1.mp3 (kelas berisik, non-berisik)
- Cabang durasi teruji: pad (10 detik), crop (60 detik)
- `artifacts/LAPORAN.md`: 7326 bytes
- ROC-AUC Tahap 05 yang dilaporkan: 0.8296 — DI BAWAH SYARAT AWAL
- Pemeriksaan lulus: 31/31

## Catatan
- Tidak ada pelatihan, penalaan, atau pemilihan fitur pada tahap ini.
- Fungsi `predict_audio` memakai kontrak prapemrosesan Tahap 03 tanpa perubahan.
- Metrik hold-out dilaporkan apa adanya, termasuk status di bawah syarat 0,85.
