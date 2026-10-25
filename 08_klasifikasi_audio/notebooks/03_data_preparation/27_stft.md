### 3.5 Short-Time Fourier Transform dan spektrum daya

#### A. Rumus

Frame yang sudah diberi window dan di-zero-pad dari 400 ke 512 sampel dihitung dengan rFFT:

\[
S[m,k]=\sum_{n=0}^{L-1}x_w[m,n]\,
e^{-j2\pi kn/N_{\text{FFT}}},
\qquad k=0,\ldots,N_{\text{FFT}}/2
\]

\[
P[m,k]=|S[m,k]|^2
\]

Dengan \(N_{\text{FFT}}=512\), jumlah bin rFFT adalah 257 (0 sampai 8.000 Hz). Zero-padding 112 sampel tidak menambah informasi, tetapi memperhalus grid frekuensi dan menghasilkan 512 titik FFT.

#### B. Ilustrasi manual

Ambil \(x=[1,0,-1,0]\), window persegi, dan \(N_{\text{FFT}}=4\). Maka:

- \(S[0]=1+0-1+0=0\)
- \(S[1]=1-(-1)=2\)
- \(S[2]=1-1=0\)
- \(S[3]=1-(-1)=2\)

Jadi \(P=[0,4,0,4]\). Bin dengan daya terbesar adalah bin 1 dan 3.

#### C. Implementasi pada data nyata
