### 3.9 Spectral centroid

#### A. Rumus

Untuk setiap frame dengan spektrum daya \(P[m,k]\) dan frekuensi \(f_k\):

\[
C_m=\frac{\sum_{k=0}^{K-1} f_k P[m,k]}
{\sum_{k=0}^{K-1} P[m,k]}
\]

Fitur:

\[
\text{centroid\_mean}=\frac{1}{M}\sum_m C_m,\qquad
\text{centroid\_std}=\text{std populasi}(C_m)
\]

Jika jumlah daya satu frame nol, centroid frame tersebut ditetapkan 0 dan dicatat sebagai frame kosong.

#### B. Ilustrasi manual

Misalkan \(f=[0,1000,2000]\) Hz dan \(P=[1,3,0]\).

\[
C=\frac{0\cdot1+1000\cdot3+2000\cdot0}{1+3+0}
=\frac{3000}{4}=750\text{ Hz}
\]

#### C. Implementasi pada data nyata
