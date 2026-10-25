# Laporan Validasi Tahap 05

Status: **PASS**

## Angka aktual

- File uji: 40 dari 7 NIM test
- ROC-AUC: 0.8296 (CI95 bootstrap 0.6767 - 0.9549)
- PR-AUC: 0.8481
- Precision / recall / F1 kelas 1: 0.7500 / 0.7895 / 0.7692
- Confusion TN/FP/FN/TP: 16/5/4/15
- Status syarat 0,85: DI BAWAH SYARAT AWAL
- Pemeriksaan lulus: 28/28

## Catatan

- Model tidak di-fit ulang; sidik jari memori dan hash file identik saat dimuat.
- Metrik hanya memakai NIM test; NIM train tidak muncul.
- Threshold keputusan tetap 0,50 dan tidak dituning pada data uji.
