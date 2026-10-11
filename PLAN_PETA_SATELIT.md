# PLAN — Peta Interaktif 6.1 + Basemap Satelit (5.7 & 6.1)

Status: PERENCANAAN (belum dieksekusi) — dibuat karena ada pekerjaan mendesak lain.
Keputusan user: basemap **Esri + Google** · isi peta 6.1 **lengkap**.

## 1. Latar & temuan survei (read-only)

- 5.7: interaktif ✓ (7 HTML folium) — basemap hanya Esri Street + OpenTopoMap. **Tanpa satelit, tanpa WMS.**
- 6.1: **nol peta interaktif** — hanya PNG statis + TIF unduhan, tanpa folium/leaflet.
- File siap pakai: `data/processed/jabon_classified.tif`, `jabon_rf.joblib`,
  `data/spasial/jabon_sawah.shp` (+sidecar), `data/spasial/s2_jabon.tif`.

## 2. Target

### A. Peta baru `05_clustering/../peta_sawah_jabon.html` (tepatnya `06_klasifikasi_sawah/`)
Satu HTML folium + LayerControl:
- **Basemap**: Esri World Imagery + Google Satellite (`https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}`, atribusi `© Google`) + Esri World Street Map.
- **Overlay**: (1) prediksi biner — PNG transparan dari `jabon_classified.tif` via
  `ImageOverlay(bounds=[[S,W],[N,E]] lat/lon)`; (2) probabilitas sawah (PNG viridis);
  (3) 100 poligon sampel (GeoJson hijau/merah + tooltip id/kelas/luas).
- Bounds lat/lon via `rasterio.warp.transform_bounds(EPSG:32749 → EPSG:4326)`.
- Implementasi: **1 sel kode baru** di `6.1_persiapan_klasifikasi.ipynb` (pakai
  joblib/tif yang ada — **tanpa retraining**), output tersimpan agar tampil di buku.

### B. Satelit untuk 5.7
- Tambah 2 basemap yang sama ke `05_clustering/run_57.py` (`build_map` +
  `build_interactive_map`) dan cerminnya di 2 sel peta notebook 5.7
  (`map7`, `interaktif7`).
- Eksekusi ulang 5.7 (URL tile tertanam di output tersimpan → wajib refresh).

### C. Penyaluran & buku
- `build.bat`: copy `06_klasifikasi_sawah/peta_sawah_jabon.html`.
- Kotak unduh 6.1: + tombol HTML peta.
- Rebuild + bukti screenshot headless (pola `kampus_3d`: Chrome `--headless --screenshot`).

## 3. Urutan eksekusi (nanti)

1. Sel peta 6.1 → eksekusi notebook → cek `peta_sawah_jabon.html` ada.
2. Basemap 5.7 (`run_57.py` + 2 sel notebook) → eksekusi ulang 5.7.
3. `build.bat` (copy peta) + tombol unduh 6.1.
4. Clean rebuild → screenshot bukti → verifikasi href.

## 4. Catatan jujur (jangan dihapus saat eksekusi)

- Tile Google/Esri butuh internet saat dibuka (offline → basemap abu-abu, overlay
  prediksi/sampel tetap tampil karena inline). Untuk skripsi, cantumkan citra latar
  sebagai "non-analisis" + atribusi Esri/Google.
- Tile Google (`mt1...lyrs=s`) melanggar ToS Google untuk produksi — sebutkan di thesis.
- Estimasi: ±1–2 jam (eksekusi 5.7 ulang yang paling lama).
