### 3.6 MSE energy

#### A. Rumus

\[
\text{MSE} = \frac{1}{N}\sum_{n=0}^{N-1}y[n]^2
\]

Ini adalah rata-rata kuadrat amplitudo untuk **seluruh sinyal 480.000 sampel**, bukan total energi dan bukan rata-rata dari fitur frame.

#### B. Ilustrasi manual

Misalkan \(y=[0{,}1,\;-0{,}2,\;0{,}3,\;-0{,}4]\).

\[
\text{MSE}=\frac{0{,}01+0{,}04+0{,}09+0{,}16}{4}=0{,}075
\]

#### C. Implementasi pada data nyata
