## 5. Demo nyata pada file dataset

Demo memakai file asli, bukan data sintetis:

1. **Satu file berisik dan satu file non-berisik** — dipilih deterministik dari 40 file uji (nama terurut per kelas), dijalankan lewat `predict_audio` pada **file MP3 asli di `data_mp3/`**, sehingga seluruh rantai dekode → durasi → normalisasi → fitur → model berjalan dari awal. Label asli dan hasil prediksi dilaporkan apa adanya, termasuk bila salah.
2. **Uji cabang durasi** — file 10 detik (potongan) untuk cabang **pad** dan file 60 detik (gabungan dua rekaman) untuk cabang **crop**, dibuat sementara di `artifacts/06_deployment/demo_audio/`, memastikan aturan durasi bekerja persis seperti kontrak.

Hasil seluruh demo disimpan di `demo_results.csv` dan ditampilkan lengkap dengan probabilitas, aksi durasi, dan status kecocokan.
