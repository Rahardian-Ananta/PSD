## 1. Pintu masuk: hasil Tahap 03

Section ini memastikan data fitur dari Tahap 03 layak dipakai sebelum ada satu pun pelatihan model.

Syarat yang diverifikasi:

1. `validation_summary.json` Tahap 03 berstatus **PASS** dengan seluruh pemeriksaan lulus.
2. `features.csv` berisi tepat 176 baris, kolom identitas + 12 fitur, tanpa NaN/Inf, dan seluruh identitas unik.
3. Distribusi kelas 88 non-berisik : 88 berisik dan 34 NIM, semua NIM memiliki kedua kelas.
4. `selected_features.txt` berisi 8 kandidat eksploratif; daftar itu **hanya referensi** karena seleksi final wajib dipelajari di dalam `Pipeline` pada training fold.

Bila satu saja syarat gagal, notebook berhenti dan Tahap 04 tidak dianggap dimulai.
