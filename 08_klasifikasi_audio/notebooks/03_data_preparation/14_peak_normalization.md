### 2.4 Peak normalization

Peak normalization menyamakan skala amplitudo tanpa mengubah bentuk gelombang, durasi, atau kecepatan.

#### A. Rumus

\[
p=\max_{n}|y[n]|
\]

\[
y_{\text{norm}}[n]=
\begin{cases}
y[n]/p, & p>0\\
\text{error}, & p=0
\end{cases}
\]

Target peak adalah \(1.0\). Normalisasi dilakukan **setelah** crop/pad dan sebelum WAV ditulis. Jika \(p=0\), sinyal kosong tidak boleh dinormalisasi diam-diam; file harus ditolak.

#### B. Ilustrasi manual

Misalkan \(y=[0{,}2,\;-0{,}4,\;0{,}1]\).

\[
p=\max(0{,}2;0{,}4;0{,}1)=0{,}4
\]

\[
y_{\text{norm}}=[0{,}5,\;-1{,}0,\;0{,}25]
\]

Jika seluruh sampel nol, \(p=0\), maka operasi harus menghasilkan error, bukan pembagian dengan nol.

#### C. Implementasi pada data nyata
