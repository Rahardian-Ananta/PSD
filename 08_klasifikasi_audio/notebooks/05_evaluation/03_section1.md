## 1. Pintu masuk: model dan pembagian dari Tahap 04

Section ini memuat artefak Tahap 04 tanpa menyentuhnya dan mengunci siapa yang berhak diuji.

Syarat yang diverifikasi:

1. `validation_summary.json` Tahap 04 berstatus **PASS** dengan seluruh pemeriksaan lulus dan `holdout_tested_in_stage_04 = false`.
2. `best_model.joblib` ada, berisi pipeline `scaler -> select -> clf`, dan konfigurasinya cocok dengan daftar fitur yang dipakai.
3. `holdout_file_split.csv` menetapkan 40 file pada **split test** yang seluruhnya berasal dari 7 NIM test; tidak ada file train yang ikut.
4. Sidik jari model dicatat saat dimuat dan dicek ulang di validasi akhir, sehingga terbukti model tidak di-fit ulang di tahap ini.

Bila satu saja syarat gagal, evaluasi berhenti.
