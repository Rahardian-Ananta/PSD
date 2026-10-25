## 4. Kualitas fitur dan kandidat seleksi

Section ini bersifat **eksploratif**. Semua analisis memakai seluruh 176 file final untuk memahami struktur fitur dan menyusun kandidat. Kandidat ini **bukan** seleksi final untuk model: seleksi dan scaling wajib dipelajari ulang di dalam `Pipeline` pada training fold di Tahap 04.

Prinsip:

1. Korelasi tinggi ditandai, tetapi fitur tidak dihapus otomatis.
2. Outlier divisualisasikan, tetapi tidak dibuang tanpa alasan domain.
3. Cohen's d dihitung eksplisit, termasuk penanganan \(s_p=0\).
4. Mutual information dan Random Forest importance ditampilkan terpisah.
5. Tidak memakai PCA.
6. `selected_features.txt` hanya berisi kandidat eksploratif dan catatan anti-leakage.
