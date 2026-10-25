### 3.12 Spectral bandwidth

#### A. Rumus

Untuk setiap frame, dengan centroid \(C_m\):

\[
B_m=\sqrt{
\frac{\sum_{k=0}^{K-1}P[m,k](f_k-C_m)^2}
{\sum_{k=0}^{K-1}P[m,k]}
}
\]

Fitur `spectral_bandwidth_mean` adalah rata-rata \(B_m\) seluruh frame. Ini adalah simpangan baku spektrum berbobot daya, bukan bandwidth fisik codec.

#### B. Ilustrasi manual

Misalkan \(f=[0,1000,2000]\) Hz dan \(P=[1,0,1]\).

\[
C=\frac{0+0+2000}{2}=1000\text{ Hz}
\]

\[
B=\sqrt{\frac{1(0-1000)^2+0+1(2000-1000)^2}{2}}
=\sqrt{1.000.000}=1000\text{ Hz}
\]

#### C. Implementasi pada data nyata
