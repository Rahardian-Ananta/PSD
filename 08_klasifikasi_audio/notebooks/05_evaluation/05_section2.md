## 2. Prediksi pada NIM test

Model yang dimuat langsung dipakai untuk memprediksi 40 file uji:

1. `predict_proba` menghasilkan probabilitas kelas 0 dan 1; label prediksi ditentukan dengan **threshold 0,50** yang sama dengan aturan `predict` dua kelas dan tidak dituning pada data uji.
2. Hasil per file disimpan di `test_predictions.csv` berisi probabilitas kedua kelas, label prediksi, label sebenarnya, dan penanda benar/salah.
3. Tidak ada langkah preprocessing tambahan: fitur berasal dari `features.csv` yang dihasilkan prosedur identik dengan deployment.
4. Threshold, pipeline, dan fitur persis seperti yang dipakai Tahap 04; tidak ada yang disesuaikan setelah melihat data uji.
