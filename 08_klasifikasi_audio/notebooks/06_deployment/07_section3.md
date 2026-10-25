## 3. Fungsi `predict_audio(path)`

Fungsi ini adalah keluaran utama tahap deployment. Alurnya, sesuai rincian Tahap 06 di `01_business_understanding.md`:

1. memuat file audio apa pun (MP3 maupun WAV) lewat `librosa.load(..., sr=16000, mono=True)`;
2. menyetel durasi ke tepat 30 detik (crop/pad tengah);
3. melakukan peak normalization dengan aturan yang sama seperti training;
4. mengekstraksi 12 fitur dengan definisi dan parameter yang sama;
5. memakai `best_model.joblib` yang sudah dimuat (pipeline menangani scaling dan seleksi fitur di dalamnya);
6. mengembalikan **label prediksi** dan **probabilitas kelas yang diprediksi** beserta probabilitas kedua kelas, catatan durasi, dan nilai fiturnya.

Catatan yang dipegang:

- Threshold keputusan tetap **0,50** — konsisten dengan `predict` bawaan pipeline dan dengan evaluasi Tahap 05; tidak ada penalaan.
- Probabilitas keluaran adalah **skor model**, bukan keyakinan terkalibrasi.
- Fungsi menolak file yang tidak ada, sinyal kosong, atau peak nol dengan pesan galat yang jelas, bukan menghasilkan angka semu.
