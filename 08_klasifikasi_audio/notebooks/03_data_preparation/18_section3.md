## 3. Framing dan ekstraksi 12 fitur

Setiap file final sudah berupa mono 16 kHz dengan 480.000 sampel. Fitur dihitung dengan pengaturan yang sama untuk semua file:

| Komponen | Nilai |
|---|---|
| Sample rate | 16.000 Hz |
| Panjang frame | 400 sampel = 25 ms |
| Hop | 160 sampel = 10 ms |
| Overlap | 240 sampel = 60% |
| FFT | 512 titik (zero-padding dari 400) |
| Window | Hann simetris |
| Resolusi frekuensi | 31,25 Hz |
| Jumlah bin rFFT | 257 (0–8.000 Hz) |

Tidak ada `center=True`. Frame hanya diambil jika seluruh 400 sampel tersedia. Konsekuensinya, 80 sampel terakhir dari 480.000 sampel tidak masuk frame terakhir, tetapi tetap dipakai untuk `mse_energy` yang dihitung dari seluruh sinyal.
