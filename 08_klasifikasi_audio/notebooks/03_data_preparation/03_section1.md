## 1. Audit seleksi file dan duplikasi eksak

Section ini memeriksa ulang manifest Data Understanding sebelum file dipakai. Fokusnya bukan menghapus file, melainkan menetapkan status setiap file:

- `final`: file unik atau wakil eksplisit dari satu grup duplikat.
- `quarantine`: file duplikat yang tidak dipilih atau duplikat lintas label.

Aturan yang dipakai:

1. Kesamaan ditentukan dari **SHA-256 byte file**, bukan kemiripan sinyal atau label.
2. Duplikat **lintas label** tidak boleh menjadi satu pun kelas; semua anggotanya dikarantina.
3. Untuk duplikat **sama label**, dipilih tepat satu wakil per hash.
4. Pemilihan wakil memaksimalkan jumlah NIM yang mempertahankan kedua kelas, lalu menekan NIM satu kelas, baru memaksimalkan jumlah NIM yang masih terwakili.
5. `raw_audio/` tidak disentuh. File karantina akan **disalin** ke folder `quarantine/`.
