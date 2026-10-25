### 3.14 Pengecekan silang dengan librosa

Fitur manual dihitung dari **spektrum daya** \(P=|S|^2\). Librosa menghitung beberapa fitur dari **magnitudo** \(|S|\):

- `spectral_centroid`
- `spectral_bandwidth`
- `spectral_rolloff`
- `spectral_flatness`

Karena itu, perbedaan kecil sampai menengah adalah konsekuensi definisi, bukan otomatis bug. Pengecekan internal rFFT vs FFT penuh dilakukan pada Section 3.5. STFT manual tidak dibandingkan langsung dengan `librosa.stft` karena librosa membingkai berdasarkan `n_fft` dan memusatkan window saat `win_length < n_fft`, sedangkan implementasi manual membingkai 400 sampel lalu menambahkan 112 nol di akhir. Perbedaan ZCR juga dicatat karena konvensi tepi frame dapat berbeda.

Korelasi Pearson dan rata-rata selisih absolut dihitung per fitur antar-file. Tujuannya memastikan arah fitur konsisten, bukan memaksa dua definisi menjadi identik.
