## 4. Bukti identitas: 176 file, fitur dan prediksi

Klaim "prosedur training dan prediksi identik" harus dibuktikan, bukan ditegaskan. Section ini menjalankan `predict_audio` pada **seluruh 176 file `data_final/`** dan membandingkannya dengan `features.csv` dari Tahap 03:

1. **Fitur** — selisih relatif per fitur per file dibandingkan `features.csv`; seluruhnya wajib di bawah toleransi. Sumber perbedaan yang diperbolehkan hanya kuantisasi ulang PCM16 ketika file final dinormalisasi kembali (faktor ~3e-5).
2. **Probabilitas** — probabilitas dari `predict_audio` dibandingkan `predict_proba` langsung pada baris `features.csv` yang sama.
3. **Label** — label `predict_audio` harus sama dengan label pipeline langsung untuk semua file.
4. **Reproduksi Tahap 05** — untuk 40 file uji, label wajib identik dengan `test_predictions.csv` dan probabilitasnya berbeda paling banyak `PROBA_MATCH_TOL`.

Hasil per file disimpan di `feature_identity_check.csv` dan ringkasannya di `identity_summary.json`.
