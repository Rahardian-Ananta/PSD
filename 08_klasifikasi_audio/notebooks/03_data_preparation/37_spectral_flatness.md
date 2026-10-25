### 3.10 Spectral flatness

#### A. Rumus

Untuk setiap frame:

\[
\text{GM}_m=\exp\left(\frac{1}{K}\sum_{k=0}^{K-1}\log(P[m,k]+\epsilon)\right)
\]

\[
\text{AM}_m=\frac{1}{K}\sum_{k=0}^{K-1}(P[m,k]+\epsilon)
\]

\[
\text{flatness}_m=\frac{\text{GM}_m}{\text{AM}_m}
\]

Nilai mendekati 1 berarti spektrum mirip noise/merata; nilai mendekati 0 berarti energi terkonsentrasi pada sebagian bin. \(\epsilon\) adalah epsilon kecil agar `log` tetap terdefinisi. Untuk frame dengan daya total nol (hening digital), flatness ditetapkan 0 karena tidak ada konten spektral yang dapat diukur. Fitur akhir adalah rata-rata flatness seluruh frame.

#### B. Ilustrasi manual

Misalkan \(P=[4,1,1,0{,}25]\) (tanpa epsilon untuk ilustrasi).

\[
\text{GM}=(4\cdot1\cdot1\cdot0{,}25)^{1/4}=1
\]

\[
\text{AM}=\frac{4+1+1+0{,}25}{4}=1{,}5625
\]

\[
\text{flatness}=\frac{1}{1{,}5625}=0{,}64
\]

#### C. Implementasi pada data nyata
