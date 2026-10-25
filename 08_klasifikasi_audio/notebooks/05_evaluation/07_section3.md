## 3. Metrik hold-out

Metrik dihitung dari 40 file uji saja:

| Metrik | Peran |
|---|---|
| ROC-AUC | Kemampuan memberi skor berisik lebih tinggi; dibandingkan dengan baseline 0,50 dan syarat kelayakan 0,85 |
| PR-AUC (average precision) | Pemeringkatan kelas berisik dengan baseline = prevalensi kelas berisik pada data uji |
| Precision, recall, F1 kelas 1 | Kualitas penandaan berisik pada ambang 0,50 |
| Accuracy | Pelengkap; dibaca bersama confusion matrix |
| Confusion matrix | Jumlah TN, FP, FN, TP secara langsung |
| Classification report | Metrik per kelas lengkap dengan support |

Status syarat kelayakan (`ROC-AUC ≥ 0,85`) dihitung dari angka nyata; bila tidak terpenuhi, hasil tetap dilaporkan sebagai **di bawah syarat awal**, tidak disesuaikan.
