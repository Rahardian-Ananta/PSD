# Laporan Validasi Tahap 03

Status: **PASS**

## Angka aktual

- File awal: 200
- File final: 176
- File karantina: 24
- NIM final: 34
- Distribusi kelas: {'0': 88, '1': 88}
- Baris features.csv: 176
- Hash WAV final unik: 176
- NIM tidak pasti: 0
- Frame dengan daya nol: 1677 pada 52 file
- Pemeriksaan lulus: 28/28

## Catatan

- `24-123` tidak memiliki file final karena seluruh file-nya menjadi duplikat non-wakil.
- Frame dengan daya nol adalah hening digital yang nyata; frame tidak dihapus. Centroid, flatness, rolloff, dan bandwidth frame tersebut ditetapkan 0.
- Split berbasis NIM belum dibuat; itu menjadi tanggung jawab Tahap 04.
- Fitur kandidat bersifat eksploratif dan harus dipelajari ulang di dalam Pipeline pada training fold.
