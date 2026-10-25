### 2.3 Crop dan pad ke 30 detik

Semua file mentah berdurasi 30 detik, sehingga pada dataset ini seharusnya tidak ada crop atau pad. Meskipun demikian, kontraknya tetap harus ada agar deployment menangani durasi lain secara identik.

Urutan operasi: **decode -> mono 16 kHz -> crop/pad -> peak normalization -> tulis WAV**.

#### A. Rumus crop

Jika \(N > N_{\text{target}}\), ambil potongan di tengah:

\[
s=\left\lfloor\frac{N-N_{\text{target}}}{2}\right\rfloor
\]

\[
y_{\text{crop}}[n]=y[s+n],\qquad n=0,\ldots,N_{\text{target}}-1
\]

#### B. Ilustrasi crop

Misalkan \(y=[10,11,12,13,14,15]\) dan \(N_{\text{target}}=4\).

\[
s=\lfloor(6-4)/2\rfloor=1
\]

Hasil: \([11,12,13,14]\). Sampel awal dan akhir dibuang seimbang.

#### A. Rumus pad

Jika \(N < N_{\text{target}}\):

\[
P=N_{\text{target}}-N,\qquad L_{\text{pad}}=\left\lfloor\frac{P}{2}\right\rfloor,\qquad R_{\text{pad}}=P-L_{\text{pad}}
\]

\[
y_{\text{pad}}=[\underbrace{0,\ldots,0}_{L_{\text{pad}}},y_0,\ldots,y_{N-1},\underbrace{0,\ldots,0}_{R_{\text{pad}}}]
\]

Jika \(P\) ganjil, satu sampel nol tambahan diletakkan di kanan.

#### B. Ilustrasi pad

Misalkan \(y=[10,11,12]\), \(N_{\text{target}}=5\), maka \(P=2\), \(L_{\text{pad}}=1\), \(R_{\text{pad}}=1\):

\[
y_{\text{pad}}=[0,10,11,12,0]
\]

#### C. Implementasi pada data nyata
