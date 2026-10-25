## 5. Ketidakpastian dan analisis kesalahan

Dengan 40 file dari 7 NIM, satu dua kesalahan dapat menggeser metrik dengan jelas. Karena itu dua hal dilaporkan bersama angka titik:

1. **Confidence interval bootstrap** untuk ROC-AUC: 2.000 pengambilan ulang dengan pengacakan tetap (`random_state=42`), memakai persentil 2,5% dan 97,5%. Sampel yang hanya berisi satu kelas dilewati karena ROC-AUC tidak terdefinisi.
2. **Rincian per NIM** — jumlah file, komposisi kelas, jumlah benar/salah per NIM, sehingga terlihat apakah kesalahan menumpuk pada subjek tertentu.
3. **Daftar file yang salah** (`errors.csv`) beserta probabilitasnya; file tetap dipertahankan, tidak ada yang dibuang karena dianggap sulit.

CI bootstrap menggambarkan ketidakpastian akibat jumlah file yang kecil; ia bukan jaminan generalisasi ke ruang kelas atau perangkat lain.
