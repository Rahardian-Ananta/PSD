"""
Script lengkap otomatis:
1. Hitung statistik riil tiap polutan (EDA, Missing Value, Outlier)
2. Update 2.3, 2.4, 2.5, 2.6
3. Buat data clean (imputasi IQR + interpolasi)
4. Update 3.3, 3.4
5. Ekstraksi 68 fitur TSFEL untuk NO2
"""

import pandas as pd
import numpy as np
import os
import json
import warnings
warnings.filterwarnings('ignore')

BASE_RAW  = 'data/downloads/jabon_pollutants_data'
BASE_CLEAN = 'data/downloads/jabon_clean_data'
os.makedirs(BASE_CLEAN, exist_ok=True)

POLLUTANTS = ['CO', 'SO2']

# ─────────────────────────────────────────────
# 1. BACA SEMUA DATA MENTAH
# ─────────────────────────────────────────────
raw = {}
for p in POLLUTANTS:
    df = pd.read_csv(f'{BASE_RAW}/jabon_{p}.csv')
    df['date'] = pd.to_datetime(df['date'], utc=True)
    df = df.sort_values('date').reset_index(drop=True)
    df[p] = pd.to_numeric(df[p], errors='coerce')
    raw[p] = df
    print(f'[READ] {p}: {len(df)} baris, {df[p].isna().sum()} missing')

# ─────────────────────────────────────────────
# 2. HITUNG STATISTIK DESKRIPTIF & OUTLIER PER POLUTAN
# ─────────────────────────────────────────────
stats = {}
outlier_info = {}

for p in POLLUTANTS:
    s = raw[p][p]
    Q1 = s.quantile(0.25)
    Q3 = s.quantile(0.75)
    IQR = Q3 - Q1
    lb  = Q1 - 1.5 * IQR
    ub  = Q3 + 1.5 * IQR
    n_outlier = ((s < lb) | (s > ub)).sum()
    stats[p] = {
        'N'         : len(s),
        'Missing'   : s.isna().sum(),
        'Missing_pct': round(s.isna().sum() / len(s) * 100, 2),
        'Min'       : round(s.min(), 8),
        'Q1'        : round(Q1, 8),
        'Median'    : round(s.median(), 8),
        'Mean'      : round(s.mean(), 8),
        'Q3'        : round(Q3, 8),
        'Max'       : round(s.max(), 8),
        'Std'       : round(s.std(), 8),
        'Skewness'  : round(s.skew(), 4),
        'Kurtosis'  : round(s.kurtosis(), 4),
        'IQR'       : round(IQR, 8),
        'LB'        : round(lb, 8),
        'UB'        : round(ub, 8),
        'Outlier_n' : int(n_outlier),
    }
    outlier_info[p] = {'LB': lb, 'UB': ub, 'n': int(n_outlier)}
    print(f'[STATS] {p}: mean={stats[p]["Mean"]:.4g}, missing={stats[p]["Missing"]}, outlier={n_outlier}')

# ─────────────────────────────────────────────
# 3. PREPROCESSING: OUTLIER → NaN, LALU INTERPOLASI
# ─────────────────────────────────────────────
clean = {}
for p in POLLUTANTS:
    df = raw[p].copy()
    s  = df[p]
    lb = outlier_info[p]['LB']
    ub = outlier_info[p]['UB']
    # tandai outlier jadi NaN
    df.loc[(s < lb) | (s > ub), p] = np.nan
    # set index datetime lalu interpolasi
    df2 = df.set_index('date')[[p]].interpolate(method='time').ffill().bfill()
    df2 = df2.reset_index()
    clean[p] = df2
    # simpan
    out_path = f'{BASE_CLEAN}/jabon_{p}_clean.csv'
    df2.to_csv(out_path, index=False)
    print(f'[CLEAN] {p}: {df2[p].isna().sum()} sisa NaN -> disimpan ke {out_path}')

# ─────────────────────────────────────────────
# 4. SIMPAN HASIL STATISTIK KE JSON untuk template
# ─────────────────────────────────────────────
with open('data/downloads/jabon_stats.json', 'w', encoding='utf-8') as f:
    json.dump({p: {k: (int(v) if hasattr(v, 'item') and isinstance(v, (np.integer,)) else float(v) if hasattr(v, 'item') else v) for k, v in d.items()} for p, d in stats.items()}, f, ensure_ascii=False, indent=2)
print('\n[JSON] Statistik disimpan ke data/downloads/jabon_stats.json')

# ─────────────────────────────────────────────
# 5. EKSTRAKSI 68 FITUR TSFEL UNTUK NO2
# ─────────────────────────────────────────────
import inspect
import tsfel.feature_extraction.features as tsfel_features

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
    result = fn(signal, fs) if "fs" in params else fn(signal)
    return to_scalar(result)

fs = 1
signal_no2 = clean['NO2']['NO2'].astype(float).values
print(f'\n[TSFEL] Sinyal NO2: {signal_no2.shape}, NaN={np.isnan(signal_no2).sum()}')

row = {}
failed = []
for fn_name in FEATURE_LIST:
    try:
        row[fn_name] = extract_one(fn_name, signal_no2, fs)
    except Exception as e:
        row[fn_name] = np.nan
        failed.append(fn_name)
        print(f'  [WARN] {fn_name}: {e}')

features_df = pd.DataFrame([row])
# Tambah kolom identitas
features_df.insert(0, 'nama', 'Rahardian Ananta')
features_df.insert(1, 'daerah', 'Kecamatan Jabon')

out_features = 'NO2_Jabon_TSFEL.csv'
features_df.to_csv(out_features, index=False)
print(f'[TSFEL] {features_df.shape[1]-2} fitur diekstraksi -> disimpan ke {out_features}')
if failed:
    print(f'[TSFEL] Gagal: {failed}')

# Simpan juga ringkasan fitur ke JSON
features_dict = row.copy()
with open('data/downloads/jabon_no2_features.json', 'w', encoding='utf-8') as f:
    json.dump(features_dict, f, ensure_ascii=False, indent=2)
print('[JSON] Fitur NO2 disimpan ke data/downloads/jabon_no2_features.json')

print('\n=== SELESAI SEMUA ===')
