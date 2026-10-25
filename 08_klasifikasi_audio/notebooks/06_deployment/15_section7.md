## 7. Validasi akhir Tahap 06

Seluruh klaim deployment diverifikasi dari artefak dan eksekusi nyata, bukan dari asumsi:

1. **Pintu masuk** — validasi Tahap 03, 04, 05 berstatus PASS; struktur pipeline, parameter, 12 fitur, dan kontrak prapemrosesan tidak berubah.
2. **Identitas model** — probabilitas langsung dari `features.csv` identik dengan `test_predictions.csv` (selisih < 1e-12); sidik jari SHA-256 file model tercatat.
3. **Identitas prapemrosesan** — seluruh 176 file menghasilkan fitur relatif selisihnya di bawah toleransi, label konsisten, dan reproduksi 40 file uji cocok dengan Tahap 05.
4. **Demo** — dua kelas terwakili, cabang pad dan crop teruji, file demo tersimpan.
5. **Laporan** — `artifacts/LAPORAN.md` ada, memuat metrik nyata beserta status syarat 0,85, lokasi artefak, dan limitasi.
6. **Kebutuhan tahap lain** — keluaran `artifacts/test_results/` lengkap; `raw_audio/` tetap 200 file; `data_final/` tetap 176 WAV.

Bila satu saja pemeriksaan gagal, tahap dianggap tidak lulus.
