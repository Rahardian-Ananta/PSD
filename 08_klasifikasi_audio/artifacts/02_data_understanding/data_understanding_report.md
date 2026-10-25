# 02 — Data Understanding: Laporan Aktual

## Ringkasan data

- Total file mentah: **200**
- NIM unik: **35**
- Kelas berisik: **100 file**
- Kelas non-berisik: **100 file**
- File berdurasi tepat 30 detik: **200 / 200**
- File berhasil dibaca: **200 / 200**
- Hash unik: **177**
- File terlibat duplikat eksak: **41**
- NIM lengkap 6 file: **30 / 35**
- Kombinasi NIM-kelas-take yang hilang: **10**

## Distribusi kelas

| label_name | n_files | n_nim | n_unique_hashes | n_duplicate_files | n_low_level | duration_min_s | duration_max_s | size_median_mb | peak_median | rms_median |
|---|---|---|---|---|---|---|---|---|---|---|
| berisik | 100 | 35 | 89 | 21 | 0 | 30.0000 | 30.0000 | 0.4649 | 0.8900 | 0.0858 |
| non-berisik | 100 | 34 | 89 | 20 | 3 | 30.0000 | 30.0000 | 0.4487 | 0.3957 | 0.0262 |

## Kelengkapan per NIM

| nim | n_berisik | n_non_berisik | n_files | n_unique_hashes | n_duplicate_files | lengkap_6_file | memiliki_dua_kelas |
|---|---|---|---|---|---|---|---|
| 24-003 | 3 | 2 | 5 | 5 | 5 | False | True |
| 24-006 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-007 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-026 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-027 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-031 | 3 | 3 | 6 | 6 | 3 | True | True |
| 24-034 | 3 | 3 | 6 | 5 | 2 | True | True |
| 24-053 | 2 | 3 | 5 | 5 | 2 | False | True |
| 24-068 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-071 | 3 | 3 | 6 | 6 | 6 | True | True |
| 24-078 | 3 | 3 | 6 | 4 | 3 | True | True |
| 24-079 | 3 | 3 | 6 | 6 | 3 | True | True |
| 24-081 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-087 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-098 | 3 | 3 | 6 | 6 | 3 | True | True |
| 24-100 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-101 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-115 | 3 | 3 | 6 | 6 | 3 | True | True |
| 24-118 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-119 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-123 | 2 | 0 | 2 | 2 | 2 | False | False |
| 24-125 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-131 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-137 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-141 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-145 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-157 | 3 | 3 | 6 | 4 | 3 | True | True |
| 24-168 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-169 | 1 | 3 | 4 | 4 | 0 | False | True |
| 24-179 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-190 | 3 | 3 | 6 | 6 | 2 | True | True |
| 24-196 | 3 | 3 | 6 | 4 | 3 | True | True |
| 24-201 | 3 | 3 | 6 | 6 | 1 | True | True |
| 24-202 | 3 | 3 | 6 | 6 | 0 | True | True |
| 24-228 | 2 | 2 | 4 | 4 | 0 | False | True |

## Format dan metadata

| label_name | samplerate | channels | n_files |
|---|---|---|---|
| berisik | 16000 | 1 | 3 |
| berisik | 44100 | 2 | 34 |
| berisik | 48000 | 1 | 26 |
| berisik | 48000 | 2 | 37 |
| non-berisik | 16000 | 1 | 3 |
| non-berisik | 44100 | 2 | 35 |
| non-berisik | 48000 | 1 | 24 |
| non-berisik | 48000 | 2 | 38 |

| metrik | count | mean | std | min | 25% | 50% | 75% | max |
|---|---|---|---|---|---|---|---|---|
| duration_decoded_s | 200.0000 | 30.0000 | 0.0000 | 30.0000 | 30.0000 | 30.0000 | 30.0000 | 30.0000 |
| size_mb | 200.0000 | 0.4496 | 0.1468 | 0.1197 | 0.3251 | 0.4569 | 0.5646 | 0.7267 |
| bitrate_kbps_estimate | 200.0000 | 125.7221 | 41.0441 | 33.4680 | 90.8920 | 127.7525 | 157.8816 | 203.1939 |
| peak_abs | 200.0000 | 0.6420 | 0.3477 | 0.0220 | 0.3649 | 0.6743 | 0.9204 | 1.5118 |
| rms | 200.0000 | 0.0738 | 0.0693 | 0.0012 | 0.0234 | 0.0502 | 0.1135 | 0.3144 |

## Duplikasi eksak

| duplicate_group_id | n_files | labels | nims | takes | scope |
|---|---|---|---|---|---|
| DUP01 | 2 | berisik | 24-003, 24-053 | 1, 3 | cross_nim |
| DUP02 | 2 | berisik | 24-003, 24-079 | 2 | cross_nim |
| DUP03 | 3 | berisik | 24-003, 24-079, 24-123 | 1, 3 | cross_nim |
| DUP04 | 2 | non-berisik, berisik | 24-034 | 1 | cross_label |
| DUP05 | 2 | berisik | 24-071, 24-098 | 1 | cross_nim |
| DUP06 | 2 | berisik | 24-071, 24-098 | 2 | cross_nim |
| DUP07 | 2 | berisik | 24-071, 24-098 | 3 | cross_nim |
| DUP08 | 2 | berisik | 24-115, 24-190 | 3 | cross_nim |
| DUP09 | 2 | berisik | 24-123, 24-201 | 1, 2 | cross_nim |
| DUP10 | 3 | berisik | 24-157 | 1, 2, 3 | within_nim |
| DUP11 | 2 | non-berisik | 24-003, 24-053 | 1, 2 | cross_nim |
| DUP12 | 2 | non-berisik | 24-003, 24-079 | 1, 3 | cross_nim |
| DUP13 | 2 | non-berisik | 24-031, 24-071 | 1, 3 | cross_nim |
| DUP14 | 3 | non-berisik | 24-031, 24-071, 24-115 | 2 | cross_nim |
| DUP15 | 2 | non-berisik | 24-031, 24-071 | 1, 3 | cross_nim |
| DUP16 | 3 | non-berisik | 24-078 | 1, 2, 3 | within_nim |
| DUP17 | 2 | non-berisik | 24-115, 24-190 | 1, 3 | cross_nim |
| DUP18 | 3 | non-berisik | 24-196 | 1, 2, 3 | within_nim |

Interpretasi:

- **1 grup** memiliki label berbeda untuk audio identik. Ini adalah konflik label yang harus dikarantina atau diadjudikasi.
- **14 grup** melintasi NIM. `GroupKFold` saja **tidak** mencegah kebocoran untuk kasus ini karena konten identik dapat muncul pada NIM train dan test.
- **3 grup** berada dalam NIM yang sama dan mencakup beberapa take, sehingga take tersebut bukan observasi independen.

## Temuan kualitas berprioritas

| finding_id | kategori | severity | jumlah | temuan | tindakan_03 |
|---|---|---|---|---|---|
| F02 | Duplikasi lintas NIM | Kritis | 30 | 14 grup duplikat eksak melintasi NIM (30 file; NIM: 24-003, 24-031, 24-053, 24-071, 24-079, 24-098, 24-115, 24-123, 24-190, 24-201). | Selesaikan duplikasi lintas NIM sebelum split; jangan mengandalkan GroupKFold saja. |
| F03 | Konflik label | Kritis | 2 | 1 grup duplikat eksak memiliki label berbeda: DUP04: berisik/24-034_berisik_1.mp3 \| non-berisik/24-034_non-berisik_1.mp3. | Karantina atau minta adjudikasi manusia; jangan memakai keduanya sebagai dua kelas. |
| F01 | Duplikasi | Tinggi | 41 | 18 grup duplikat eksak melibatkan 41 file; hanya 177 hash unik dari 200 file. | Tinjau setiap grup; jangan langsung hapus; putuskan representasi dan karantina secara eksplisit. |
| F04 | Duplikasi dalam NIM | Tinggi | 9 | 3 grup duplikat berada dalam NIM yang sama dan mencakup beberapa take sekaligus. | Perlakukan take kembar sebagai satu observasi atau karantina sesuai kebijakan yang terdokumentasi. |
| F05 | Kelengkapan NIM | Sedang | 10 | 5 NIM tidak memiliki 6 file: 24-003, 24-053, 24-123, 24-169, 24-228; 10 kombinasi NIM-kelas-take hilang. | Pertahankan identitas apa adanya, tandai NIM tidak lengkap, dan putuskan inklusi dengan kriteria eksplisit. |
| F06 | NIM satu kelas | Sedang | 1 | 1 NIM hanya memiliki satu kelas: 24-123. | Putuskan apakah tetap dipakai; jika dipakai, laporkan komposisinya dan jangan menyembunyikan keterbatasan. |
| F09 | Heterogenitas format | Sedang | 3 | Sample rate: {16000: 6, 44100: 69, 48000: 125}; channel: {1: 56, 2: 144}. | Resample ke 16 kHz, downmix mono, dan validasi 480.000 sampel. |
| F12 | Label | Sedang | 200 | Label folder dan nama file cocok untuk 200 file; namun kecocokan ini hanya konsistensi metadata, bukan verifikasi isi audio. | Pertahankan label yang dapat dilacak; karantina kasus konflik; jangan memberi label baru dari kemiripan audio. |
| F13 | Lingkungan | Sedang | 1 | FFmpeg di PATH: tidak ditemukan. | Pasang/daftarkan FFmpeg sebelum menjalankan konversi. |
| F10 | Level sinyal | Rendah | 3 | 3 file memiliki peak < 0.05: non-berisik/24-006_non-berisik_3.mp3; non-berisik/24-007_non-berisik_1.mp3; non-berisik/24-053_non-berisik_2.mp3. | Audit level dan dengarkan file tersebut; jangan menghapus hanya karena levelnya rendah. |
| F11 | Overshoot MP3 | Rendah | 36 | 36 file memiliki peak > 1.0 setelah decode. | Peak normalization wajib menangani nilai absolut > 1.0 dan sinyal nol. |
| F07 | Integritas file | Info | 0 | 0 file gagal dibaca, 0 sinyal semua nol, 0 file ber-NaN, 0 file ber-Inf. | Tetap jalankan pemeriksaan ulang setelah konversi dan setelah ekstraksi fitur. |
| F08 | Durasi | Info | 200 | 200 dari 200 file berdurasi tepat 30 detik (min=30.000, max=30.000). | Pastikan hasil akhir tepat 480.000 sampel dan catat tindakan aktual per file. |
| F14 | Keseimbangan kelas | Info | 200 | Data mentah: {'berisik': 100, 'non-berisik': 100}; setelah duplikasi dan karantina, komposisi harus dihitung ulang. | Laporkan distribusi final dan pertimbangkan class_weight di dalam pipeline bila perlu. |

## Artefak

- `inventory_raw.csv`: inventaris awal.
- `manifest_raw.csv`: manifest mentah terpadu.
- `audio_metadata.csv`: metadata sinyal per file.
- `duplicate_groups.csv`, `duplicate_files.csv`: hasil deteksi duplikat.
- `missing_takes.csv`: kombinasi NIM-kelas-take yang tidak ada.
- `class_summary.csv`, `nim_summary.csv`, `format_summary.csv`, `metadata_summary.csv`.
- `quality_findings.csv`: temuan yang harus ditindaklanjuti pada tahap 03.
- `data_understanding_summary.json`: ringkasan untuk otomasi.
- `figures/`: distribusi kelas, durasi, format, waveform, dan spektrogram.

## Kesimpulan

Data mentah berjumlah **200 file** dan **35 NIM**, dengan distribusi kelas **100 berisik** dan **100 non-berisik**. Semua file dapat dibaca dan berdurasi 30 detik, tetapi dataset **belum siap dimodelkan** karena terdapat duplikasi eksak—termasuk duplikasi lintas NIM dan satu konflik label—serta 5 NIM yang tidak lengkap. Keputusan pembersihan, karantina, dan seleksi data harus dilakukan pada tahap 03 dengan ketertelusuran penuh. FFmpeg di PATH: **tidak ditemukan**.
