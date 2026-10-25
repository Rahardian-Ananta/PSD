## 2. Penyamaan format dan kontrak preprocessing

Tujuan Section 2 adalah mengubah file final terpilih menjadi representasi seragam:

```text
raw_audio/ -> data_mp3/ -> data_final/
```

### 2.1 Keputusan staging MP3

Seluruh 200 file sumber sudah berformat MP3. Karena itu, `data_mp3/` dibuat sebagai **salinan byte-identik** dari file final terpilih, bukan transcode ulang MP3 ke MP3.

Alasannya:

1. Transcode ulang audio lossy menambah generasi kompresi kedua yang tidak diperlukan.
2. Dengan salinan byte-identik, sinyal yang didekode saat training sama dengan sinyal sumber yang akan dipakai saat deployment.
3. Keseragaman yang wajib untuk model tetap dilakukan di `data_final/`: mono, 16 kHz, tepat 480.000 sampel, dan peak normalization.

Jika kelak ada sumber non-MP3, file tersebut harus dikonversi ke MP3 sebelum masuk staging. Untuk dataset ini tidak ada sumber non-MP3.

### 2.2 Target sampel

\[
N_{\text{target}} = f_s \times 30 = 16.000 \times 30 = 480.000
\]

Setelah dekode ke mono 16 kHz, setiap sinyal harus memiliki panjang tepat \(N_{\text{target}}\). Kebijakan crop/pad harus deterministik dan sama persis dengan deployment.
