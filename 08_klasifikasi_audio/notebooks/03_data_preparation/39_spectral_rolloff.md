### 3.11 Spectral rolloff 85%

#### A. Rumus

Untuk setiap frame, hitung kumulatif daya:

\[
\Gamma[m,k]=\sum_{j=0}^{k}P[m,j]
\]

Cari indeks terkecil \(k^*\) sehingga:

\[
\Gamma[m,k^*]\ge 0{,}85\sum_{j=0}^{K-1}P[m,j]
\]

\[
R_m=f_{k^*}
\]

Fitur `spectral_rolloff_mean` adalah rata-rata \(R_m\) seluruh frame. Jika total daya frame nol, rolloff frame tersebut ditetapkan 0.

#### B. Ilustrasi manual

Misalkan \(f=[0,1000,2000,3000]\) Hz dan \(P=[1,1,1,1]\).

Total daya \(=4\), ambang \(=0{,}85\times4=3{,}4\).

Kumulatif: \(1,2,3,4\). Nilai pertama yang \(\ge3{,}4\) adalah 4 pada indeks 3, sehingga:

\[
R=3000\text{ Hz}
\]

#### C. Implementasi pada data nyata
