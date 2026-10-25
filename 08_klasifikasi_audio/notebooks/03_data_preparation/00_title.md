# 03 — Data Preparation

Notebook ini menjalankan tahap **Data Preparation** CRISP-DM untuk klasifikasi biner audio:

- `1 = berisik`
- `0 = non-berisik`

Tujuan tahap ini adalah menghasilkan dataset final yang dapat diaudit, bebas duplikat eksak, memiliki format audio seragam, dan memiliki 12 fitur yang dihitung dengan prosedur yang sama seperti deployment.

## Masukan

- `raw_audio/` (200 file MP3, read-only).
- `artifacts/02_data_understanding/manifest_raw.csv`.
- `artifacts/02_data_understanding/duplicate_groups.csv`.

## Keluaran utama

- `data_mp3/`: staging MP3 untuk file yang lolos seleksi.
- `data_final/`: WAV mono 16 kHz, tepat 480.000 sampel.
- `quarantine/03_data_preparation/`: salinan file yang dikarantina beserta catatan.
- `artifacts/features.csv`: 176 baris file final dan 12 fitur.
- `artifacts/selected_features.txt`: kandidat fitur eksploratif untuk Tahap 04.
- `artifacts/03_data_preparation/`: manifest, laporan, validasi, dan gambar.

## Batasan yang dipegang

1. `raw_audio/` tidak diubah atau dihapus.
2. Tidak ada label, NIM, atau take yang ditebak.
3. Duplikat dideteksi dari hash SHA-256, bukan dari kemiripan audio atau label.
4. Split berbasis NIM belum dibuat pada tahap ini.
5. Tidak ada training model, GridSearchCV, atau klaim model terbaik pada tahap ini.
6. Semua angka dan grafik berasal dari eksekusi data nyata.
