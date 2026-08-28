# Analisis Polutan Atmosfer di Kabupaten Sidoarjo Berdasarkan Citra Satelit Sentinel-5P

## Business Understanding

Kualitas udara adalah salah satu penentu kesehatan masyarakat. Notebook ini bertujuan memahami bagaimana konsentrasi beberapa polutan udara berubah sepanjang satu tahun terakhir di Kabupaten Sidoarjo, Jawa Timur — sebuah wilayah yang padat aktivitas industri dan lalu lintas.

Alih-alih mengandalkan stasiun pemantauan di darat, kita memanfaatkan data satelit **Sentinel-5P TROPOMI** dari Copernicus Data Space Ecosystem. Satelit ini mengukur gas-gas polutan di atmosfer dari orbit, sehingga kita bisa mendapatkan gambaran kualitas udara di atas seluruh wilayah kabupaten.

Polutan yang dianalisis cukup beragam, dan masing-masing punya cerita sendiri:

- **NO₂ (Nitrogen Dioxide)** adalah gas yang terutama keluar dari knalpot kendaraan dan cerobong pabrik. Semakin ramai lalu lintas dan industri, semakin tinggi NO₂.
- **CO (Carbon Monoxide)** muncul dari pembakaran tidak sempurna bahan bakar, misalnya mesin kendaraan atau pembakaran biomassa.
- **HCHO (Formaldehida)** adalah indikator senyawa organik yang banyak dilepaskan industri maupun vegetasi, dan sering disebut sebagai "benih" pembentuk polusi udara lain.
- **SO₂ (Sulfur Dioxide)** umumnya berasal dari pembakaran bahan bakar yang mengandung belerang di industri dan pembangkit listrik.
- **O₃ (Ozon)** di permukaan tanah bukanlah ozon pelindung di langit, melainkan polutan yang terbentuk ketika sinar matahari bereaksi dengan gas-gas lain — biasanya meningkat saat cuaca cerah.
- **CH₄ (Metana)** adalah gas rumah kaca yang berasal dari aktivitas pertanian, kebocoran jaringan gas, dan pengolahan limbah. Kadar CH₄ yang tinggi turut berkontribusi terhadap pemanasan global.

Alur kerja analisis ini sederhana: siapkan batas wilayah Sidoarjo → ambil data satelit satu tahun terakhir untuk tiap polutan → rapikan dan gabungkan datanya → visualisasikan trennya → simpan hasilnya.

---

## Unduh Data Analisis

Semua file di bawah ini tersimpan di folder `data/downloads/`. Klik tombol untuk mengunduh.

### Batas Wilayah

- **sidoarjo.geojson** — batas administrasi Kabupaten Sidoarjo dalam format GeoJSON; dipakai sebagai area of interest saat mengambil data satelit.

<a href="data/downloads/sidoarjo.geojson" download
   style="display:inline-block;padding:8px 18px;margin:4px 6px 4px 0;background:#1a73e8;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;"> Unduh sidoarjo.geojson</a>

### Hasil Pengukuran Satelit per Polutan

Masing-masing berisi deret waktu harian: satu kolom tanggal dan satu kolom konsentrasi polutan (mol/m²) hasil rata-rata spasial di seluruh Sidoarjo:

- **sidoarjo_NO2.csv** — Nitrogen Dioxide — indikator emisi kendaraan dan industri.
- **sidoarjo_CO.csv** — Carbon Monoxide — hasil pembakaran tidak sempurna bahan bakar.
- **sidoarjo_HCHO.csv** — Formaldehyde — penanda senyawa organik volatil (VOC).
- **sidoarjo_SO2.csv** — Sulfur Dioxide — emisi industri/pembangkit listrik.
- **sidoarjo_O3.csv** — Ozon permukaan — polutan sekunder yang terbentuk oleh sinar matahari.
- **sidoarjo_CH4.csv** — Metana — gas rumah kaca dari aktivitas pertanian dan industri.

<a href="data/downloads/sidoarjo_pollutants_data/sidoarjo_NO2.csv" download
   style="display:inline-block;padding:8px 18px;margin:4px 6px 4px 0;background:#1a73e8;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;"> sidoarjo_NO2.csv</a>

<a href="data/downloads/sidoarjo_pollutants_data/sidoarjo_CO.csv" download
   style="display:inline-block;padding:8px 18px;margin:4px 6px 4px 0;background:#1a73e8;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;"> sidoarjo_CO.csv</a>

<a href="data/downloads/sidoarjo_pollutants_data/sidoarjo_HCHO.csv" download
   style="display:inline-block;padding:8px 18px;margin:4px 6px 4px 0;background:#1a73e8;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;"> sidoarjo_HCHO.csv</a>

<a href="data/downloads/sidoarjo_pollutants_data/sidoarjo_SO2.csv" download
   style="display:inline-block;padding:8px 18px;margin:4px 6px 4px 0;background:#1a73e8;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;"> sidoarjo_SO2.csv</a>

<a href="data/downloads/sidoarjo_pollutants_data/sidoarjo_O3.csv" download
   style="display:inline-block;padding:8px 18px;margin:4px 6px 4px 0;background:#1a73e8;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;"> sidoarjo_O3.csv</a>

<a href="data/downloads/sidoarjo_pollutants_data/sidoarjo_CH4.csv" download
   style="display:inline-block;padding:8px 18px;margin:4px 6px 4px 0;background:#1a73e8;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;"> sidoarjo_CH4.csv</a>

### Data Gabungan & Versi Tren

- **sidoarjo_pollutants.csv** — keenam polutan digabung dalam satu tabel dengan indeks tanggal yang sama (data harian mentah).
- **sidoarjo_pollutants_rolling30.csv** — versi rolling mean 30 hari dari tabel gabungan; kurvanya lebih halus sehingga tren jangka panjang lebih mudah dibaca.

<a href="data/downloads/sidoarjo_pollutants_data/sidoarjo_pollutants.csv" download
   style="display:inline-block;padding:8px 18px;margin:4px 6px 4px 0;background:#1a73e8;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;"> sidoarjo_pollutants.csv</a>

<a href="data/downloads/sidoarjo_pollutants_data/sidoarjo_pollutants_rolling30.csv" download
   style="display:inline-block;padding:8px 18px;margin:4px 6px 4px 0;background:#1a73e8;color:#ffffff;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;"> sidoarjo_pollutants_rolling30.csv</a>
