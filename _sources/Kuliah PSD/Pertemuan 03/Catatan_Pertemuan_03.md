# Catatan Perkuliahan PSD - Pertemuan 03

## Topik: [Judul Topik]

---

## Materi Utama

### 1. [Sub Judul 1]

[Isi materi]

### 2. [Sub Judul 2]

[Isi materi]

---

## Tugas

### Deskripsi
[Deskripsi tugas]

### Langkah Pengerjaan
1. [Langkah 1]
2. [Langkah 2]

### Catatan Penting
- [Catatan]

---

## Referensi
- [Referensi 1]






ambil data x misal kota ini dan itu lalu di olah itu harus bisa di lakukan di uas
harus bisa missing value


data crawling
explorasi data
note : tambahkan preprosesing sebelum extraksi fitur,data harus bersih sebelum extraksi fitur gak tau apa intinya dosenku tiba tiba 65fitur dan tiba tiba domain 
jadi harus extrax fitur jadi 65
extraxsi fitur/preprosesing
interpolasi linear 




data uderstanding didalamnya ada missing value





bagaimana cara menggunakan interpolasi linear untuk mencari nan 


missing value =  noise





Tugas 3:
Preprocessing sebelum ekstraksi fitur 
- Data diganti sesuai kecamatan masing - masing
- Deteksi outliers pada data kemarin
- Lakukan imputasi missing value sampai terisi semua
- setelah itu dilakukan, maka lakukan ekstraksi fitur menjadi 65 (lihat di tsfel)
- kelompokkan mana domain statistic, temporal, spectral
- upload web statis


ini untuk fitur polutan yang di ekstraksi menjadi 68 fitur hanya 1 fitur aja, dan di sepakati satu kelas kita ambil fitur NO2 ya guyss


ini bisa deteksi outliers dulu, habis itu imputasi missing values. setelahnya bisa ekstraksi fitur untuk no2 ya

untuk code ekstraksi fitur menjadi 68 bisa pake code ini spy struktur tabelnya sama

import pandas as pd
import numpy as np
import inspect
import tsfel.feature_extraction.features as tsfel_features

# ---------- 1. Muat dan bersihkan data ----------
df = pd.read_csv('mystorage/NO2-Kerek.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

target_pollutant = 'NO2'

# --- FIX: paksa kolom target jadi numerik, nilai yang gagal dikonversi -> NaN ---
df[target_pollutant] = pd.to_numeric(df[target_pollutant], errors='coerce')

n_missing_before = df[target_pollutant].isna().sum()
print(f"Jumlah nilai non-numerik/kosong yang dikonversi jadi NaN: {n_missing_before}")

Q1 = df[target_pollutant].quantile(0.25)
Q3 = df[target_pollutant].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df.loc[(df[target_pollutant] < lower_bound) | (df[target_pollutant] > upper_bound), target_pollutant] = np.nan

df_clean = df.set_index('date').interpolate(method='time').ffill().bfill()

fs = 1
signal_1d = df_clean[target_pollutant].astype(float).values

# ---------- 2. Daftar PERSIS fitur yang diminta ----------
FEATURE_LIST = """abs_energy auc autocorr average_power calc_centroid calc_max calc_mean
calc_median calc_min calc_std calc_var dfa distance ecdf ecdf_percentile ecdf_percentile_count
ecdf_slope entropy fundamental_frequency higuchi_fractal_dimension hist_mode human_range_energy
hurst_exponent interq_range kurtosis lempel_ziv lpcc max_frequency max_power_spectrum
maximum_fractal_length mean_abs_deviation mean_abs_diff mean_diff median_abs_deviation
median_abs_diff median_diff median_frequency mfcc mse negative_turning neighbourhood_peaks
petrosian_fractal_dimension pk_pk_distance positive_turning power_bandwidth rms skewness slope
spectral_centroid spectral_decrease spectral_distance spectral_entropy spectral_kurtosis
spectral_positive_turning spectral_roll_off spectral_roll_on spectral_skewness spectral_slope
spectral_spread spectral_variation spectrogram_mean_coeff sum_abs_diff wavelet_abs_mean
wavelet_energy wavelet_entropy wavelet_std wavelet_var zero_cross""".split()

print("Jumlah fitur yang diminta:", len(FEATURE_LIST))


def to_scalar(result):
    if isinstance(result, dict) and "values" in result:
        result = result["values"]
    if isinstance(result, (list, tuple, np.ndarray)):
        arr = np.asarray(result, dtype=float)
        return float(np.nanmean(arr))
    return float(result)


def extract_one(fn_name, signal, fs):
    fn = getattr(tsfel_features, fn_name)
    params = inspect.signature(fn).parameters
    if "fs" in params:
        result = fn(signal, fs)
    else:
        result = fn(signal)
    return to_scalar(result)


row = {}
for fn_name in FEATURE_LIST:
    row[fn_name] = extract_one(fn_name, signal_1d, fs)

extracted_features_final = pd.DataFrame([row])

print(f"Berhasil! Jumlah fitur yang dihasilkan untuk {target_pollutant}: {extracted_features_final.shape[1]}")
extracted_features_final.to_csv(f'{target_pollutant}_Kerek_TSFEL.csv', index=False)

nama kecamatan/daerahnya bisa di sesuaikan



ada file gambar juga namanya pertemuan_3.jpg
ini ada connection limitnya, jadi cuma 20 aja yang bisa login. kalo udah masukkan datanya bisa log out

oiya, setelah kalian dapet file ekstraksi fitur nanti waktu masukkan ke tabel yang ada di database ada tambahan kolom "nama" dan "daerah"




code:


import pandas as pd
import numpy as np
import inspect
import tsfel.feature_extraction.features as tsfel_features

# ---------- 1. Muat dan bersihkan data ----------
df = pd.read_csv('mystorage/NO2-Kerek.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

target_pollutant = 'NO2'

# --- FIX: paksa kolom target jadi numerik, nilai yang gagal dikonversi -> NaN ---
df[target_pollutant] = pd.to_numeric(df[target_pollutant], errors='coerce')

n_missing_before = df[target_pollutant].isna().sum()
print(f"Jumlah nilai non-numerik/kosong yang dikonversi jadi NaN: {n_missing_before}")

Q1 = df[target_pollutant].quantile(0.25)
Q3 = df[target_pollutant].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df.loc[(df[target_pollutant] < lower_bound) | (df[target_pollutant] > upper_bound), target_pollutant] = np.nan

df_clean = df.set_index('date').interpolate(method='time').ffill().bfill()

fs = 1
signal_1d = df_clean[target_pollutant].astype(float).values

# ---------- 2. Daftar PERSIS fitur yang diminta ----------
FEATURE_LIST = """abs_energy auc autocorr average_power calc_centroid calc_max calc_mean
calc_median calc_min calc_std calc_var dfa distance ecdf ecdf_percentile ecdf_percentile_count
ecdf_slope entropy fundamental_frequency higuchi_fractal_dimension hist_mode human_range_energy
hurst_exponent interq_range kurtosis lempel_ziv lpcc max_frequency max_power_spectrum
maximum_fractal_length mean_abs_deviation mean_abs_diff mean_diff median_abs_deviation
median_abs_diff median_diff median_frequency mfcc mse negative_turning neighbourhood_peaks
petrosian_fractal_dimension pk_pk_distance positive_turning power_bandwidth rms skewness slope
spectral_centroid spectral_decrease spectral_distance spectral_entropy spectral_kurtosis
spectral_positive_turning spectral_roll_off spectral_roll_on spectral_skewness spectral_slope
spectral_spread spectral_variation spectrogram_mean_coeff sum_abs_diff wavelet_abs_mean
wavelet_energy wavelet_entropy wavelet_std wavelet_var zero_cross""".split()

print("Jumlah fitur yang diminta:", len(FEATURE_LIST))


def to_scalar(result):
    if isinstance(result, dict) and "values" in result:
        result = result["values"]
    if isinstance(result, (list, tuple, np.ndarray)):
        arr = np.asarray(result, dtype=float)
        return float(np.nanmean(arr))
    return float(result)


def extract_one(fn_name, signal, fs):
    fn = getattr(tsfel_features, fn_name)
    params = inspect.signature(fn).parameters
    if "fs" in params:
        result = fn(signal, fs)
    else:
        result = fn(signal)
    return to_scalar(result)


row = {}
for fn_name in FEATURE_LIST:
    row[fn_name] = extract_one(fn_name, signal_1d, fs)

extracted_features_final = pd.DataFrame([row])

print(f"Berhasil! Jumlah fitur yang dihasilkan untuk {target_pollutant}: {extracted_features_final.shape[1]}")
extracted_features_final.to_csv(f'{target_pollutant}_Kerek_TSFEL.csv', index=False)




ini tugasnya itu sama kaya kemarin guys, tapi di ganti
- ambil data dari kecamatan masing masing
- data di ambil dari tgl 31-08-2025 sampai 31-08-2026
- deteksi outliers
- imputasi missing value
- jika data sudah sempurna tidak ada outliers dan missing value lanjut ekstraksi fitur sebanyak 68 fitur sesuai dengan library tsfel (fitur polutan yang di ekstraksi NO2)
- setelah dapet file ekstraksi fitur masukkan ke table yanga ada di database aiven itu (informasinya sudah ada di overview)
- sudah selesai, selamat mengerjakan