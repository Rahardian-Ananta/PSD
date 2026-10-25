## 5. Validasi akhir dan serah-terima Tahap 03

Validasi ini memastikan bahwa keluaran Tahap 03 konsisten dan dapat dipakai Tahap 04 tanpa perbaikan diam-diam.

### Checklist

1. Setiap file final memiliki tepat satu baris di `features.csv`.
2. Identitas `file`, `nim`, `take`, dan `label` konsisten antara manifest, WAV, dan fitur.
3. Semua 12 fitur bertipe numerik, tidak mengandung NaN/Inf, dan berada pada rentang logis.
4. Setiap WAV final berdurasi 30 detik, mono 16 kHz, PCM 16-bit, dan tepat 480.000 sampel.
5. Jalur traceability `raw_audio -> data_mp3 -> data_final -> features.csv` lengkap.
6. Distribusi kelas dan NIM final dilaporkan.
7. NIM yang tidak pasti atau tidak memenuhi syarat tidak dimasukkan diam-diam ke split.
8. File yang dikarantina memiliki salinan dan catatan alasan.
9. Split berbasis NIM belum dibuat pada tahap ini.
