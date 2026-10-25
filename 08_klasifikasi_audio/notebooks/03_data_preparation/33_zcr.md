### 3.8 Zero-crossing rate

#### A. Rumus

Untuk setiap frame \(m\):

\[
\text{ZCR}_m=\frac{1}{L-1}\sum_{n=0}^{L-2}
\mathbf{1}\left[x[m,n]\cdot x[m,n+1]<0\right]
\]

Fitur:

\[
\text{zcr\_mean}=\frac{1}{M}\sum_m \text{ZCR}_m,\qquad
\text{zcr\_std}=\text{std populasi}(\text{ZCR}_m)
\]

Produk negatif berarti pasangan sampel berpindah tanda. Konvensi ini dicatat karena librosa dapat menghitung zero crossing dengan definisi tepi yang sedikit berbeda.

#### B. Ilustrasi manual

Untuk \(x=[1,-1,1,1]\):

\[
x_nx_{n+1}=[-1,-1,1]
\]

Ada dua perkalian negatif dari tiga pasangan:

\[
\text{ZCR}=\frac{2}{3}\approx0{,}6667
\]

#### C. Implementasi pada data nyata
