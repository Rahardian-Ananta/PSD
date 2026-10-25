### 3.2 Overlap antar-frame

#### A. Rumus

\[
O=L-H
\]

\[
r_{\text{overlap}}=\frac{L-H}{L}
\]

Dengan \(L=400\) dan \(H=160\):

\[
O=240,\qquad r_{\text{overlap}}=\frac{240}{400}=0{,}60
\]

Overlap 240 sampel setara 15 ms. Hop 160 sampel setara 10 ms.

#### B. Ilustrasi manual

Misalkan \(L=4\), \(H=2\). Maka \(O=2\) dan \(r=2/4=0{,}5\).

Frame 0: \([0,1,2,3]\). Frame 1: \([2,3,4,5]\). Dua sampel, yaitu \(2\) dan \(3\), dipakai dua kali.

#### C. Implementasi pada data nyata
