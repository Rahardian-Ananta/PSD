## 2. Penguncian hold-out berbasis NIM

Hold-out dibentuk dari **NIM unik**, bukan dari file, menggunakan `GroupShuffleSplit(test_size=0.2, random_state=42)`.

Aturan yang dipegang:

1. Pembagian dibentuk **sebelum** pemilihan model dan disimpan ke `holdout_split.csv` (per NIM) serta `holdout_file_split.csv` (per file).
2. NIM pada sisi test **tidak boleh** muncul di data yang dipakai perbandingan model maupun `GridSearchCV`.
3. Uji terhadap NIM test dilakukan hanya di Tahap 05, sehingga hasil Tahap 04 tidak pernah menyentuh data evaluasi akhir.
4. Seluruh NIM, file, dan kelas yang masuk masing-masing sisi dilaporkan apa adanya, termasuk ketidakseimbangan kelas yang muncul secara alami.
