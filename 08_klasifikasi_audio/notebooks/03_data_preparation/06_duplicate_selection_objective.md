### 1.1 Aturan pemilihan wakil duplikat

Untuk setiap grup duplikat **sama label**, pilih tepat satu file. Semua file unik selalu dipertahankan. File dari grup **lintas label** tidak boleh menjadi wakil dan seluruh anggotanya dikarantina.

#### A. Rumus keputusan

Untuk himpunan file final \(F\), hitung:

\[
B(F)=\sum_{g=1}^{G}\mathbf{1}\left[\text{NIM }g\text{ memiliki kedua kelas}\right]
\]

\[
R(F)=\sum_{g=1}^{G}\mathbf{1}\left[\text{NIM }g\text{ masih terwakili}\right]
\]

\[
O(F)=\sum_{g=1}^{G}\mathbf{1}\left[\text{NIM }g\text{ hanya memiliki satu kelas}\right]
\]

Pilih kombinasi wakil dengan skor prioritas:

\[
Q(F)=1.000.000\,B(F)-10.000\,O(F)+100\,R(F)
\]

\[
F^{*}=\arg\max_{F} Q(F)
\]

Skor ini membuat jumlah NIM dengan kedua kelas menjadi prioritas utama. Jika masih seri, NIM satu kelas ditekan lebih dahulu, baru jumlah NIM yang terwakili dimaksimalkan. Urutan kandidat dibuat deterministik dari `duplicate_group_id` dan `relative_path`.

#### B. Ilustrasi manual

Misalkan ada dua NIM: A dan B. File unik awal hanya memberi A kelas berisik dan B kelas non-berisik. Ada dua grup duplikat:

- Grup 1 (berisik): kandidat dari A atau B.
- Grup 2 (non-berisik): kandidat dari A atau B.

| Pilihan | A berisik | A non | B berisik | B non | B | R | O |
|---|---:|---:|---:|---:|---:|---:|---:|
| Grup 1 → A, Grup 2 → A | 1 | 1 | 0 | 1 | 1 | 2 | 1 |
| Grup 1 → A, Grup 2 → B | 1 | 0 | 0 | 1 | 0 | 2 | 2 |

Pilihan pertama menang karena \(B=1\), meskipun sama-sama memiliki \(R=2\). Ini sesuai tujuan: mempertahankan kedua kelas pada sebanyak mungkin NIM.

#### C. Implementasi pada data nyata
