### 3.4 Windowing

#### A. Rumus

Untuk setiap frame \(m\) dan indeks \(n=0,\ldots,L-1\):

\[
x_w[m,n]=x[m,n]\,w[n]
\]

Window yang sama dipakai untuk semua frame dan semua file.

#### B. Ilustrasi manual

Dengan \(x=[1,2,3,4]\) dan \(w=[0,\;0{,}75,\;0{,}75,\;0]\):

\[
x_w=[1\cdot0,\;2\cdot0{,}75,\;3\cdot0{,}75,\;4\cdot0]
=[0,\;1{,}5,\;2{,}25,\;0]
\]

#### C. Implementasi pada data nyata
