### 4.2 Mutual information dan Random Forest importance

Dua metode memberi sudut pandang berbeda:

- **Mutual information** mengukur ketergantungan antara satu fitur dan label, termasuk hubungan non-linear.
- **Random Forest importance** mengukur kontribusi fitur terhadap penurunan impurity di hutan pohon.

Keduanya dihitung pada seluruh data final hanya untuk menyusun kandidat eksploratif. Ini tidak boleh dipakai sebagai seleksi final model.

#### A. Rumus mutual information

\[
I(X;Y)=\sum_{x}\sum_{y}p(x,y)\log\frac{p(x,y)}{p(x)p(y)}
\]

`mutual_info_classif` memakai logaritma natural dan estimator berbasis tetangga untuk fitur kontinu, dengan `random_state=42`.

#### B. Ilustrasi manual

Misalkan \(y=[0,0,1,1]\) dan fitur \(X=[0,0,1,1]\). Fitur tersebut sempurna memisahkan kelas.

\[
p(0,0)=0{,}5,\quad p(1,1)=0{,}5
\]

\[
I(X;Y)=0{,}5\ln\frac{0{,}5}{0{,}5\cdot0{,}5}
+0{,}5\ln\frac{0{,}5}{0{,}5\cdot0{,}5}
=\ln2\approx0{,}693
\]

Fitur yang tidak memberi informasi tentang label memiliki \(I(X;Y)\approx0\).

#### A. Definisi Random Forest importance

Untuk setiap fitur \(j\), kepentingan adalah rata-rata penurunan impurity pada semua node yang memakai fitur tersebut, dibobot jumlah sampel node:

\[
\text{Importance}_j=
\frac{1}{T}\sum_{t=1}^{T}\sum_{\text{node }v\text{ memakai }j}
\frac{N_v}{N}\left[i(v)-\frac{N_{v,L}}{N_v}i(v_L)-\frac{N_{v,R}}{N_v}i(v_R)\right]
\]

dengan \(i(v)\) impurity node, \(N_v\) jumlah sampel node, dan \(T\) jumlah pohon. Nilai dinormalisasi agar total seluruh fitur menjadi 1.

#### B. Ilustrasi

Fitur yang memisahkan kelas hampir sempurna pada banyak pohon akan sering menurunkan impurity besar, sehingga importance-nya tinggi. Fitur acak cenderung jarang terpilih dan rata-rata penurunan impurity-nya rendah. Importance bukan arah pengaruh dan bukan causal effect.

#### C. Implementasi pada data nyata
