### 3.3 Window Hann simetris

#### A. Rumus

Untuk \(n=0,1,\ldots,L-1\):

\[
w[n]=0{,}5-0{,}5\cos\left(\frac{2\pi n}{L-1}\right)
\]

Window ini simetris dan bernilai nol di kedua ujung. Tujuannya mengurangi kebocoran spektral akibat pemotongan frame.

#### B. Ilustrasi manual

Untuk \(L=4\):

\[
w[0]=0,\quad w[1]=0{,}75,\quad w[2]=0{,}75,\quad w[3]=0
\]

Jadi \(w=[0,\;0{,}75,\;0{,}75,\;0]\).

#### C. Implementasi pada data nyata
