### 4.1 Cohen's d per fitur

#### A. Rumus

Untuk kelas berisik (1) dan non-berisik (0):

\[
d=\frac{\bar{x}_1-\bar{x}_0}{s_p}
\]

\[
s_p=\sqrt{\frac{(n_1-1)s_1^2+(n_0-1)s_0^2}{n_1+n_0-2}}
\]

Jika \(s_p=0\):

- \(d=0\) bila kedua rata-rata sama;
- \(d=+\infty\) atau \(-\infty\) bila rata-rata berbeda, dengan tanda mengikuti \(\bar{x}_1-\bar{x}_0\).

Nilai absolut besar berarti pemisahan rata-rata relatif besar terhadap variasi dalam kelas. Ini bukan ukuran performa model.

#### B. Ilustrasi manual

Kelas 0: \([1,2,3]\), rata-rata 2, varians sampel 1.

Kelas 1: \([4,5,6]\), rata-rata 5, varians sampel 1.

\[
s_p=\sqrt{\frac{2\cdot1+2\cdot1}{4}}=1
\]

\[
d=\frac{5-2}{1}=3
\]

#### C. Implementasi pada data nyata
