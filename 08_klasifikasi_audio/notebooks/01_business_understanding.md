# 01 — Business Understanding

**Proyek:** Klasifikasi biner audio kelas: berisik vs non-berisik  
**Kelas:** Proyek Sains Data A (PSD-A), Universitas Trunojoyo Madura  
**Pendekatan:** CRISP-DM  
**Status dokumen:** pemahaman masalah dan rencana; belum memuat hasil analisis data

---

## Ringkasan eksekutif

Proyek ini bertujuan membangun model yang dapat membedakan rekaman suasana kelas ke dalam dua kelas:

- **Berisik (label 1):** kelas ramai karena mahasiswa/siswa berbicara sendiri-sendiri.
- **Non-berisik (label 0):** kelas tenang, diskusi antar beberapa siswa, dosen menjelaskan materi, atau sesi tanya jawab.

Keluaran akhir adalah pipeline yang dapat menerima satu file audio, melakukan prapemrosesan yang sama dengan data latih, lalu mengembalikan label beserta probabilitas kelas prediksi. Model ini adalah alat bantu penyaringan awal, bukan penilai disiplin, bukan pengenal pembicara, dan bukan pengganti observasi manusia.

Laporan awal menyebutkan 200 file, 100 per kelas, dengan 6 file per NIM. Angka tersebut **belum menjadi fakta proyek**. Jumlah aktual, NIM unik, duplikat, label, dan file rusak wajib dihitung dari isi `raw_audio/` pada tahap 02. Jika data aktual berbeda dari laporan awal, data aktual yang dipakai.

---

## 1. Tujuan bisnis

### 1.1 Konteks

Suasana kelas memengaruhi efektivitas pembelajaran. Kelas yang terlalu ramai oleh percakapan antar mahasiswa berbeda kondisinya dari kelas yang tenang, berdiskusi dalam kelompok kecil, mendengarkan dosen, atau mengikuti tanya jawab. Perekaman audio berdurasi pendek dapat menjadi sinyal awal untuk mengidentifikasi kelas yang memerlukan perhatian.

### 1.2 Pertanyaan bisnis

1. Apakah sebuah rekaman kelas cenderung **berisik** atau **non-berisik**?
2. Seberapa dapat diandalkan model membedakan kedua kondisi tersebut pada NIM yang belum pernah dilihat model?
3. Dalam kondisi data dan sumber daya yang ada, apakah performa model cukup untuk digunakan sebagai alat bantu penyaringan, dan apa batasannya?

### 1.3 Keputusan yang didukung

Model dapat membantu:

- menandai rekaman yang perlu ditinjau manusia;
- memprioritaskan observasi kelas;
- memberi gambaran awal pola akustik yang membedakan suasana kelas.

Model **tidak** digunakan untuk:

- menghukum individu atau kelompok;
- mengidentifikasi pembicara;
- menentukan kualitas pengajaran;
- mengambil keputusan otomatis tanpa peninjauan manusia.

### 1.4 Definisi operasional label

| Kelas | Label | Definisi |
|---|---:|---|
| Berisik | 1 | Kelas ramai; banyak mahasiswa/siswa berbicara sendiri-sendiri secara bersamaan |
| Non-berisik | 0 | Kelas tenang; diskusi antar beberapa siswa, dosen menjelaskan, atau sesi tanya jawab |

Label mengikuti protokol pengumpulan data. Batas antar kelas dapat kabur, misalnya dosen menjelaskan sambil beberapa mahasiswa berbicara. Kasus seperti ini tidak boleh diberi label baru berdasarkan tebakan atau kemiripan audio. Jika identitas, take, atau label tidak dapat dipastikan, file ditandai dan dikarantina pada tahap 03.

### 1.5 Ruang lingkup

**Termasuk:**

- klasifikasi biner pada tingkat file audio 30 detik;
- data yang dikumpulkan mahasiswa PSD-A;
- evaluasi berbasis NIM;
- artefak model dan fungsi prediksi untuk demonstrasi.

**Tidak termasuk:**

- deteksi jenis kebisingan (misalnya suara kendaraan, musik, atau percakapan);
- diarization atau pengenalan pembicara;
- transkripsi;
- klasifikasi per segmen di dalam file;
- jaminan performa produksi.

---

## 2. Menilai situasi

### 2.1 Sumber dan bentuk data

Data dibuat oleh mahasiswa kelas Proyek Sains Data A (PSD-A), Universitas Trunojoyo Madura. Setiap mahasiswa diminta merekam 6 audio di laboratorium:

- 3 take berisik;
- 3 take non-berisik;
- total 6 file per NIM;
- format MP3;
- dikumpulkan melalui Google Drive bersama.

Laporan awal: 100 file per kelas, total 200 file. **Ini baru laporan, bukan hasil audit.** Tahap 02 akan menghitung jumlah file, NIM unik, distribusi label, format aktual, durasi, sample rate, channel, ukuran file, dan metadata lain yang tersedia.

### 2.2 Inkonsistensi aritmetika pada angka awal

Target 200 file tidak konsisten dengan aturan 6 file per NIM:

```text
200 file ÷ 6 file/NIM = 33,33 NIM
```

Karena NIM adalah identitas diskrit, 33 NIM menghasilkan 198 file dan 34 NIM menghasilkan 204 file, sebelum memperhitungkan file hilang, duplikat, atau take yang tidak lengkap. Dengan demikian:

- angka **100 file per kelas** tidak boleh dipaksakan;
- angka **200 file** tidak boleh dijadikan target yang mengalahkan kejujuran data;
- distribusi aktual per kelas dan per NIM harus dilaporkan apa adanya;
- kekurangan atau kelebihan file adalah temuan, bukan sesuatu yang ditutupi.

### 2.3 Sumber daya

| Komponen | Ketersediaan |
|---|---|
| Data mentah | Disediakan pengguna di `raw_audio/` |
| Komputasi | CPU lokal; sekitar 200 file berdurasi pendek masih terjangkau |
| Perangkat lunak | Python, librosa, soundfile, pydub, FFmpeg, pandas, scikit-learn, matplotlib, seaborn, joblib |
| Tenaga kerja | Agen AI sebagai pelaksana teknis; pengguna sebagai pemilik data dan pengambil keputusan |
| Penyimpanan | Ringan untuk MP3, WAV 16 kHz mono 30 detik, fitur, model, dan grafik |
| Waktu | Dikerjakan bertahap; setiap tahap harus divalidasi sebelum lanjut |

### 2.4 Kendala

1. `raw_audio/` bersifat read-only; tidak boleh diubah atau dihapus.
2. Tidak boleh membuat data dummy atau mengarang NIM, take, dan label.
3. Semua angka dan grafik harus berasal dari komputasi nyata.
4. Split wajib berbasis NIM agar identitas subjek tidak bocor.
5. Data MP3 bersifat lossy dan dapat memiliki bitrate, sample rate, serta channel berbeda.
6. Durasi rekaman belum tentu 30 detik; sebagian mungkin lebih pendek.
7. Kualitas rekaman dapat berbeda karena perangkat, posisi, dan kondisi ruangan.
8. Ketidakseimbangan kelas dapat muncul setelah file bermasalah dikeluarkan.
9. Jumlah NIM yang valid mungkin kecil, sehingga estimasi performa tidak stabil.
10. FFmpeg harus tersedia sebagai dependensi sistem, bukan hanya paket Python.

### 2.5 Risiko dan mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| File yang sama muncul lebih dari sekali | Data bocor atau distribusi kelas bias | Deteksi hash file; jangan langsung hapus; catat dan tinjau sebelum keputusan |
| Duplikat halus (re-encode/trim) | Duplikasi tidak terdeteksi hash | Periksa metadata, durasi, dan kemiripan waveform; tandai untuk tinjauan; jangan memberi label baru berdasarkan kemiripan |
| Satu NIM masuk train dan test | Evaluasi terlalu optimistis | `GroupKFold` dan `GroupShuffleSplit` dengan `groups=NIM`; verifikasi overlap nol |
| NIM salah baca dari nama file | Split dan ketertelusuran salah | Parsing konservatif, validasi silang manifest, karantina jika ragu |
| Take tidak dikenal | Identitas file tidak lengkap | Karantina; jangan memaksakan take tebakan |
| Label tidak sesuai isi | Model belajar sinyal yang salah | Audit label dan metadata; kasus ambigu dikarantina; tidak mengarang label |
| Kelas tidak seimbang | Akurasi menyesatkan | Laporkan precision, recall, F1, ROC-AUC, confusion matrix; pertimbangkan `class_weight` di dalam pipeline |
| Perbedaan perangkat/ruangan | Model menghafal kondisi rekaman, bukan kelas | Laporkan limitasi; evaluasi pada NIM hold-out; hindari klaim generalisasi berlebihan |
| MP3 lossy | Informasi frekuensi tinggi hilang | Dekode konsisten; jangan mengklaim kualitas studio |
| Durasi < 30 detik | Event penting hilang atau padding mendominasi | Pad konsisten; catat durasi asli dan tindakan; terapkan aturan yang sama saat deployment |
| Durasi > 30 detik | Sebagian rekaman terbuang | Crop deterministik dan terdokumentasi; aturan sama saat deployment |
| Normalisasi tidak konsisten | Distribusi fitur bergeser saat prediksi | Fungsi prapemrosesan bersama; uji ulang pada file nyata |
| Sinyal kosong / `max|y| = 0` | Pembagian nol, NaN, atau Inf | Deteksi dan tangani eksplisit; karantina bila tidak layak |
| Kebocoran seleksi fitur | Performa validasi terlalu tinggi | Seleksi fitur dan scaler hanya di-fit pada training fold di dalam `Pipeline` |
| NIM valid terlalu sedikit | Variance evaluasi tinggi | Kurangi jumlah fold bila perlu dan jelaskan; laporkan jumlah NIM test; jangan menyimpulkan terlalu kuat |
| Data berisi suara orang | Risiko privasi | Gunakan hanya untuk proyek pembelajaran; batasi akses; jangan melakukan pengenalan pembicara |
| Lingkungan tidak reprodusibel | Hasil berubah antar mesin | Catat versi paket, FFmpeg, parameter, dan `random_state` |

### 2.6 Fakta versus asumsi

| Pernyataan | Status |
|---|---|
| Ada 200 file | Laporan awal; harus diverifikasi |
| Ada 100 file per kelas | Laporan awal; harus diverifikasi |
| Setiap NIM punya 6 file | Protokol pengumpulan; harus diverifikasi |
| Setiap NIM punya 3 take per kelas | Protokol pengumpulan; harus diverifikasi |
| Semua file berformat MP3 | Klaim awal; harus diperiksa |
| Semua rekaman memadai untuk klasifikasi | Belum diketahui; harus diperiksa |
| Label pada nama file benar | Belum diketahui; harus diverifikasi sejauh metadata memungkinkan |

---

## 3. Tujuan data mining

### 3.1 Perumusan masalah

Ini adalah masalah **klasifikasi biner tersupervisi**:

- unit observasi: satu file audio yang telah diseragamkan menjadi WAV mono 16 kHz dan tepat 30 detik;
- target: `label ∈ {0, 1}`, dengan 1 = berisik sebagai kelas positif;
- representasi: 12 fitur akustik yang dihitung dari sinyal 30 detik;
- keluaran: label prediksi dan probabilitas kelas yang diprediksi.

Fitur identitas (`file`, `nim`, `take`) hanya digunakan untuk ketertelusuran dan pengelompokan, **bukan** sebagai prediktor.

### 3.2 Tujuan teknis

1. Menyusun manifest data yang dapat ditelusuri dari file mentah ke file final dan baris fitur.
2. Menyeragamkan format dan durasi tanpa mengubah kecepatan putar atau menghapus hening secara otomatis.
3. Mengekstrak 12 fitur dengan definisi matematis dan parameter yang konsisten.
4. Membandingkan empat model: Logistic Regression, SVM-RBF, Random Forest, dan Gradient Boosting.
5. Memilih model melalui validasi silang berbasis NIM dan menyimpan pipeline lengkap.
6. Mengukur performa pada NIM hold-out yang tidak digunakan untuk pemilihan model.
7. Menyediakan fungsi prediksi yang memakai prosedur prapemrosesan identik.

### 3.3 Metrik dan alasan pemilihan

| Metrik | Fungsi dalam proyek |
|---|---|
| ROC-AUC | Mengukur kemampuan model memeringkat file berisik lebih tinggi daripada non-berisik; menjadi kriteria kelayakan awal |
| Precision (kelas 1) | Proporsi file yang diprediksi berisik dan memang berisik; penting agar penandaan tidak terlalu banyak salah |
| Recall (kelas 1) | Proporsi file berisik yang berhasil ditemukan; penting agar kelas bermasalah tidak terlewat |
| F1-score (kelas 1) | Keseimbangan precision dan recall |
| Confusion matrix | Menunjukkan jumlah TP, FP, FN, dan TN secara langsung |
| Accuracy | Pelengkap; tidak cukup bila kelas tidak seimbang |
| PR curve | Melengkapi ROC-AUC, terutama bila kelas positif lebih sedikit |

ROC-AUC **bukan** persentase prediksi yang benar. Nilai 0,85 berarti model memiliki peluang 0,85 untuk memberi skor lebih tinggi pada sampel positif acak dibanding sampel negatif acak, bukan berarti 85% file diprediksi benar.

### 3.4 Strategi validasi

1. **Validasi silang:** `GroupKFold` dengan `groups=NIM` untuk membandingkan model. Jumlah fold awal 5; bila NIM valid tidak cukup, jumlah fold dikurangi dan alasannya dilaporkan.
2. **Hold-out:** `GroupShuffleSplit(test_size=0.2, random_state=42)` pada NIM unik.
3. **Penguncian hold-out:** pembagian hold-out dibentuk sebelum pemilihan model dan tidak digunakan dalam `GridSearchCV`. Dengan demikian, evaluasi tahap 05 benar-benar independen dan tidak sekadar mengulang data yang sudah dipakai memilih model.
4. **Tanpa kebocoran:** scaler, imputer (jika diperlukan), dan seleksi fitur berada di dalam `Pipeline`; hanya di-fit pada training fold.
5. **Tanpa PCA:** sesuai batasan proyek.
6. **Tanpa split per file:** satu NIM tidak boleh muncul di dua sisi split.

### 3.5 Kriteria keberhasilan

**Keberhasilan proses:**

- seluruh file di `raw_audio/` terinventarisasi;
- setiap file valid dapat ditelusuri ke file final dan satu baris `features.csv`;
- setiap file yang dikecualikan memiliki alasan;
- tidak ada NIM yang bocor antar-split;
- seluruh parameter dan `random_state` tercatat;
- tidak ada data dummy atau label tebakan.

**Keberhasilan data:**

- 12 fitur numerik tanpa NaN/Inf pada baris yang dipakai;
- identitas `file`, `nim`, `take`, dan `label` lengkap;
- distribusi kelas dan jumlah file per NIM dilaporkan aktual;
- hasil transformasi durasi dan normalisasi tercatat.

**Kelayakan awal model:**

- ROC-AUC hold-out **≥ 0,85**;
- precision, recall, dan F1 kelas berisik dilaporkan bersama jumlah NIM test;
- tidak ada NIM overlap antara train dan test;
- hasil dapat direproduksi dengan konfigurasi tersimpan.

Angka 0,85 adalah **syarat kelayakan awal**, bukan jaminan layak produksi. Dengan jumlah NIM yang kecil, satu atau dua kesalahan dapat mengubah metrik secara besar. Kesimpulan akhir harus mempertimbangkan precision, recall, confusion matrix, potensi bias perangkat/ruangan, keterbatasan data, dan ketidakpastian estimasi. Jika hasil di bawah 0,85, hasil tersebut dilaporkan apa adanya dan model tidak dipaksakan lolos.

### 3.6 Baseline yang jujur

Dengan dua kelas, prediksi konstan dapat memiliki accuracy sekitar 50% bila kelas seimbang, tetapi ROC-AUC sekitar 0,50. Model harus dibandingkan dengan angka tersebut. Accuracy tinggi saja tidak membuktikan model berguna, terutama bila kelas tidak seimbang.

---

## 4. Rencana proyek

### 4.1 Prinsip pelaksanaan

- Setiap tahap menghasilkan artefak nyata yang dapat diperiksa.
- Tahap berikutnya tidak dijalankan sebelum hasil tahap sebelumnya divalidasi.
- Notebook dibangun dari file `.py` berurutan; satu file menjadi satu code cell.
- Setiap proses berumus disajikan dalam tiga bagian: penjelasan rumus, contoh angka kecil, dan eksekusi pada data nyata.
- Keputusan yang tidak dapat dibuktikan dari data ditunda atau dikarantina, bukan ditebak.

### 4.2 Tahapan

| Tahap | Aktivitas utama | Artefak | Gerbang validasi |
|---|---|---|---|
| 01 Business Understanding | Menetapkan tujuan, label, metrik, risiko, dan rencana | `01_business_understanding.md` | Tujuan dan kriteria disetujui |
| 02 Data Understanding | Inventarisasi, statistik deskriptif, EDA, cek duplikat/kerusakan/label | Manifest awal, tabel, grafik, catatan kualitas | Jumlah aktual dan masalah data teridentifikasi |
| 03 Data Preparation | Seleksi, karantina, konversi MP3, WAV 30 detik, 12 fitur, analisis kualitas fitur, validasi akhir | `data_mp3/`, `data_final/`, `features.csv`, manifest final, laporan validasi | Satu file valid = satu baris fitur; tanpa NaN/Inf; identitas lengkap |
| 04 Modeling | Empat model, `GroupKFold` berbasis NIM, `GridSearchCV` pada kandidat terbaik | `best_model.joblib`, konfigurasi, daftar fitur | Hold-out terkunci; tidak ada kebocoran NIM |
| 05 Evaluation | Uji hold-out 20% NIM, ROC/PR curve, confusion matrix, classification report | `artifacts/test_results/` | Evaluasi hanya pada NIM test; metrik aktual dilaporkan |
| 06 Deployment | `predict_audio(path)` dan demo pada file asli | Fungsi prediksi, demo, `LAPORAN.md` | Prosedur training dan prediksi identik; demo nyata berhasil |

### 4.3 Rincian Data Preparation (5 section)

1. **Seleksi dan pemeriksaan awal:** baca manifest, validasi NIM/kelas/take, deteksi duplikat melalui hash, periksa file rusak dan penamaan. Duplikat tidak langsung dihapus.
2. **Penyamaan format dan durasi:** `raw_audio/` → `data_mp3/` → `data_final/`; WAV mono 16 kHz, tepat 480.000 sampel; crop/pad konsisten; peak normalization; pemeriksaan NaN/Inf/sinyal kosong.
3. **Framing dan ekstraksi fitur:** `sr=16000`, `frame_length=400`, `hop_length=160`, `n_fft=512`, Hann; 12 fitur; spektrum daya dihitung manual dengan NumPy dan dibandingkan dengan librosa.
4. **Kualitas dan seleksi fitur:** korelasi, boxplot, Cohen's d, mutual information, feature importance; top-8 kandidat eksploratif; tanpa PCA; seleksi final dipelajari di dalam pipeline.
5. **Validasi akhir:** satu baris per file valid, label konsisten, 12 fitur bersih, distribusi kelas/NIM/take, ketertelusuran manifest, daftar pengecualian.

### 4.4 Rincian Modeling dan Evaluation

- Model: Logistic Regression, SVM-RBF, Random Forest, Gradient Boosting.
- CV: `GroupKFold(n_splits=5)` dengan NIM sebagai group; kurangi fold bila perlu.
- Pencarian hyperparameter: `GridSearchCV(scoring='roc_auc', cv=GroupKFold)`.
- Hold-out: 20% NIM, `random_state=42`, dikunci sebelum pemilihan model.
- Model final: dilatih ulang pada NIM train dan diuji hanya pada NIM test.
- Output evaluasi: ROC curve, PR curve, confusion matrix, classification report, ROC-AUC, daftar NIM train/test.

### 4.5 Rincian Deployment

Fungsi `predict_audio(path)` harus melakukan:

1. memuat audio;
2. mengubah ke mono 16 kHz;
3. crop/pad tepat 30 detik;
4. peak normalization dengan aturan yang sama seperti training;
5. ekstraksi 12 fitur dengan definisi dan parameter yang sama;
6. memuat model;
7. mengembalikan label dan probabilitas kelas yang diprediksi.

Probabilitas keluaran adalah skor model, bukan tingkat keyakinan yang terkalibrasi. Demo dilakukan pada satu file berisik dan satu file non-berisik dari dataset asli, dengan hasil eksekusi nyata.

### 4.6 Pembagian peran

| Pihak | Peran |
|---|---|
| Pengguna | Menyediakan data, menyetujui keputusan label/karantina yang ambigu, meninjau hasil tiap tahap |
| Agen AI | Menulis kode, menjalankan analisis, memeriksa hasil, membangun notebook, melaporkan temuan dan limitasi |
| Peninjau manusia | Menjadi acuan untuk kasus label yang tidak dapat dipastikan dari data |

### 4.7 Definisi selesai

Proyek dinyatakan selesai untuk lingkup ini apabila:

- enam tahap CRISP-DM terdokumentasi;
- semua artefak dihasilkan dari eksekusi nyata;
- tidak ada pelanggaran aturan data mentah, split NIM, atau kebocoran fitur;
- performa hold-out dilaporkan dengan metrik yang diminta beserta limitasinya;
- fungsi prediksi dapat dijalankan pada file asli;
- `LAPORAN.md` menjelaskan jumlah data aktual, fitur penting, model, metrik, lokasi artefak, dan limitasi.

---

## 5. Keputusan yang masih menunggu data

Hal-hal berikut **tidak** diputuskan secara spekulatif pada tahap ini:

- jumlah file, NIM, dan distribusi kelas yang sebenarnya;
- pola penamaan file dan cara paling aman mengekstrak NIM/take/label;
- ada atau tidaknya duplikat dan file rusak;
- kebijakan crop 30 detik yang dipilih setelah durasi aktual diketahui;
- jumlah fold final bila NIM valid kurang dari lima;
- ada atau tidaknya ketidakseimbangan kelas setelah karantina;
- apakah model memenuhi ROC-AUC ≥ 0,85.

Keputusan tersebut diambil pada tahap terkait berdasarkan data dan hasil yang dapat diperiksa.
