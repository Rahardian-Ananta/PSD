### 3.1 Framing

#### A. Rumus jumlah frame

Untuk sinyal \(y\) dengan panjang \(N\), frame length \(L\), dan hop \(H\), tanpa penambahan frame di awal atau akhir:

\[
M=1+\left\lfloor\frac{N-L}{H}\right\rfloor,\qquad N\ge L
\]

Frame ke-\(m\) adalah:

\[
\mathbf{x}_m=[y[mH],y[mH+1],\ldots,y[mH+L-1]]
\]

Dengan \(N=480.000\), \(L=400\), dan \(H=160\):

\[
M=1+\left\lfloor\frac{480.000-400}{160}\right\rfloor
=1+2.997=2.998
\]

Frame terakhir mulai pada sampel \(2.997\times160=479.520\) dan berakhir pada sampel \(479.919\). Sampel \(479.920\)–\(479.999\) tidak masuk frame, tetapi tetap dipakai untuk `mse_energy`.

#### B. Ilustrasi manual

Misalkan \(y=[0,1,2,3,4,5,6,7,8,9]\), \(L=4\), \(H=2\).

\[
M=1+\lfloor(10-4)/2\rfloor=1+3=4
\]

Frame yang terbentuk:

- \(m=0\): \([0,1,2,3]\)
- \(m=1\): \([2,3,4,5]\)
- \(m=2\): \([4,5,6,7]\)
- \(m=3\): \([6,7,8,9]\)

#### C. Implementasi pada data nyata
