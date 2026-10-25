### 3.7 RMS per frame

#### A. Rumus

Untuk setiap frame \(m\):

\[
\text{RMS}_m=\sqrt{\frac{1}{L}\sum_{n=0}^{L-1}x[m,n]^2}
\]

Fitur agregat:

\[
\text{rms\_mean}=\frac{1}{M}\sum_{m=0}^{M-1}\text{RMS}_m
\]

`rms_std` adalah simpangan baku populasi dari \(M\) nilai RMS frame, `rms_max` nilai maksimum, dan `rms_min` nilai minimum.

#### B. Ilustrasi manual

Misalkan satu frame \(x=[0{,}5,\;-0{,}5,\;1{,}0,\;-1{,}0]\).

\[
\text{RMS}=\sqrt{\frac{0{,}25+0{,}25+1+1}{4}}
=\sqrt{0{,}625}\approx0{,}7906
\]

#### C. Implementasi pada data nyata
