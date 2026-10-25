## 4. Kurva dan matriks

Empat gambar ditulis ke `artifacts/test_results/figures/`:

1. **Kurva ROC** — TPR vs FPR dengan luas kurva (ROC-AUC) dan diagonal acak 0,50 sebagai acuan.
2. **Kurva PR** — precision vs recall untuk kelas berisik; garis datar = prevalensi kelas berisik pada data uji, yaitu baseline PR yang jujur.
3. **Confusion matrix** — heatmap TN/FP/FN/TP dengan angka sel di dalam sel.
4. **Distribusi probabilitas** — histogram `proba(berisik)` untuk file berisik dan non-berisik, dengan garis threshold 0,50; gambar ini menunjukkan seberapa tumpang tindih kedua kelas.

Semua gambar dihasilkan dari 40 file uji yang sama dengan tabel metrik.
