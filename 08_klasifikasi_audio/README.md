# Klasifikasi Audio Berisik vs Non-Berisik

Pipeline CRISP-DM untuk mengklasifikasikan rekaman kelas menjadi:

- **1 = berisik**: kelas ramai karena banyak mahasiswa/siswa berbicara sendiri-sendiri.
- **0 = non-berisik**: kelas tenang, diskusi beberapa siswa, dosen menjelaskan, atau sesi tanya jawab.

Target awal adalah 200 file (100 per kelas), 6 file per NIM (3 take berisik + 3 take non-berisik). Angka tersebut adalah laporan awal dan **wajib diverifikasi** dari isi `raw_audio/`. Perhatikan bahwa 200 tidak habis dibagi 6 (200 ÷ 6 = 33,33), sehingga jumlah final tidak boleh dipaksakan; jumlah file, NIM unik, duplikat, distribusi label, dan file bermasalah dihitung pada tahap Data Understanding.

## Prinsip kerja

- `raw_audio/` hanya dibaca; isinya tidak diubah atau dihapus.
- Tidak ada data dummy, NIM tebakan, take tebakan, atau label tebakan. Data yang meragukan dikarantina beserta alasannya.
- Semua angka dan visualisasi dihasilkan dari komputasi nyata.
- Split train/test dilakukan **berbasis NIM** (`GroupKFold` / `GroupShuffleSplit`), bukan per file.
- Seleksi fitur dan preprocessing model dipelajari hanya pada training fold.
- Peak normalization, crop/pad 30 detik, dan ekstraksi fitur harus identik antara training dan deployment.

## Struktur folder

```text
project/
├── raw_audio/        # MP3 mentah dari pengumpulan data (read-only)
├── data_mp3/         # hasil penyamaan format ke MP3
├── data_final/       # WAV mono 16 kHz, tepat 480.000 sampel (30 detik)
├── quarantine/       # file bermasalah + catatan asal dan alasan
├── artifacts/        # features.csv, model, grafik, laporan
├── notebooks/        # dokumentasi dan notebook per tahap CRISP-DM
├── requirements.txt
└── README.md
```

Setiap notebook di `notebooks/` dibangun dari folder berisi file `.py` berurutan. Satu file `.py` menjadi satu code cell setelah kode dijalankan dan divalidasi; file `.ipynb` dibuat setelah seluruh bagian tahap tersebut selesai.

## Instalasi

Prasyarat: Python 3.10+. FFmpeg opsional: tidak dipakai oleh pipeline ini karena sumber dataset sudah MP3 dan decoding/penulisan memakai `soundfile`/`librosa`; pasang hanya bila Anda menambah format lain yang butuh transcode.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Pasang FFmpeg bila perlu (opsional):

```powershell
winget install Gyan.FFmpeg
```

Pastikan perintah berikut berhasil sebelum menjalankan pipeline:

```powershell
python --version
ffmpeg -version   # opsional, dilewati bila tidak dipasang
```

## Cara menjalankan

1. Letakkan seluruh rekaman MP3 asli di `raw_audio/`.
2. Jalankan notebook secara berurutan: `02_data_understanding`, `03_data_preparation`, `04_modeling`, `05_evaluation`, `06_deployment`.
3. Periksa artefak keluaran setiap tahap sebelum melanjutkan. Tahap berikutnya tidak boleh dijalankan bila validasi tahap sebelumnya gagal.
4. Notebook dapat dibuka dengan:

```powershell
jupyter lab
```

atau:

```powershell
jupyter notebook
```

## Artefak utama

- `artifacts/features.csv`: satu baris per file final, berisi identitas dan 12 fitur.
- `artifacts/selected_features.txt`: kandidat fitur eksploratif beserta metodenya.
- `artifacts/best_model.joblib`: pipeline terpilih beserta konfigurasinya.
- `artifacts/test_results/`: hasil evaluasi hold-out berbasis NIM.
- `artifacts/LAPORAN.md`: ringkasan hasil, metrik nyata, dan limitasi.
- `quarantine/`: file yang tidak dipakai beserta alasan karantina.

## Status

- `01_business_understanding.md`: selesai.
- `02_data_understanding`: selesai dan tervalidasi. Hasil aktual: 200 file, 35 NIM, 100 file per kelas, 18 grup duplikat eksak, dan 5 NIM tidak lengkap. Laporan: `artifacts/02_data_understanding/data_understanding_report.md`.
- `03_data_preparation`: selesai dan tervalidasi (28/28 pemeriksaan PASS). Hasil aktual: 176 file final, 24 file karantina, 34 NIM (semua berdua kelas), kelas 88:88, `data_mp3/` salinan byte-identik 176 MP3, `data_final/` 176 WAV PCM_16 mono 16000 Hz × 480000 sampel, 12 fitur valid di `artifacts/features.csv`, 1677 frame daya-nol pada 52 file (tidak dihapus), 8 kandidat fitur eksploratif di `artifacts/selected_features.txt`. Laporan: `artifacts/03_data_preparation/data_preparation_report.md` dan `validation_report.md`.
- `04_modeling`: selesai dan tervalidasi (29/29 pemeriksaan PASS). Hasil aktual: hold-out terkunci 27 NIM train (136 file) dan 7 NIM test (40 file, `random_state=42`, tidak dipakai CV); baseline ROC-AUC 0,50; perbandingan GroupKFold 5 fold grup=NIM: Logistic Regression 0,8349, Random Forest 0,7811, SVM-RBF 0,7738, Gradient Boosting 0,7569; GridSearchCV pada Logistic Regression (12 kombinasi) terbaik `C=10`, `select__k=8` dengan ROC-AUC CV **0,8442**; `artifacts/best_model.joblib` (pipeline `scaler -> select -> clf`, 8 fitur terpilih). Laporan: `artifacts/04_modeling/modeling_report.md` dan `validation_report.md`.
- `05_evaluation`: selesai dan tervalidasi (28/28 pemeriksaan PASS), uji hold-out sekali saja tanpa refit (sidik jari model identik). Hasil aktual pada 40 file / 7 NIM test: **ROC-AUC 0,8296** (CI95 bootstrap [0,6767, 0,9549], baseline 0,50) — **DI BAWAH SYARAT AWAL 0,85**, PR-AUC 0,8481, accuracy 0,7750, precision 0,7500, recall 0,7895, F1 0,7692, confusion TN 16 / FP 5 / FN 4 / TP 15 (9 file salah); 5 dari 9 kesalahan menumpuk pada NIM `24-168`. Output: `artifacts/test_results/` (`metrics.json`, `test_predictions.csv`, classification report, confusion, per-NIM, errors, 5 gambar) dan laporan `artifacts/05_evaluation/evaluation_report.md`.
- `06_deployment`: selesai dan tervalidasi (31/31 pemeriksaan PASS). `predict_audio(path)` dibangun tanpa training ulang (sidik jari file `964a1550c9c06123...`); identitas prapemrosesan terbukti pada 176 file (selisih fitur relatif maksimum 6,1e-05, label 176/176) dan reproduksi Tahap 05 40/40 label (selisih probabilitas 2,3e-05). Demo nyata: `24-068_berisik_1.mp3` benar (p=0,9114), `24-068_non-berisik_1.mp3` keliru (p=0,7403, konsisten FP Tahap 05), cabang pad 10 detik dan crop 60 detik teruji. Laporan akhir: `artifacts/LAPORAN.md`; rincian `artifacts/06_deployment/`.
- Seluruh tahap CRISP-DM 01-06 selesai. ROC-AUC hold-out 0,8296 tetap **di bawah syarat awal 0,85** dan dilaporkan apa adanya.
- `raw_audio/` tetap 200 file dan seluruh SHA-256 cocok dengan manifest Tahap 02.
- FFmpeg tidak ditemukan di `PATH` mesin ini; tidak diperlukan untuk Tahap 01-03 dan menjadi opsional.
