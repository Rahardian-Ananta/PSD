# Catatan Perkuliahan PSD - Pertemuan 04

## Topik: Ekstraksi Fitur Time Series (TSFEL), Reduksi Dimensi PCA, dan K-Means Clustering

---

## Materi Utama

### 1. Konsep Dasar Statistik untuk Fitur Time Series

Sebelum melakukan ekstraksi fitur, penting untuk memahami konsep dasar statistik yang menjadi fondasi banyak fitur TSFEL:

| Konsep | Rumus | Keterangan |
|--------|-------|------------|
| **Mean (Rata-rata)** | μ = (1/N) × Σxᵢ | Rata-rata aritmatika seluruh nilai |
| **Median** | Nilai tengah setelah diurutkan | Tahan terhadap outlier |
| **Standar Deviasi** | σ = √[(1/N) × Σ(xᵢ - μ)²] | Ukuran penyebaran data |
| **Variansi** | σ² = (1/N) × Σ(xᵢ - μ)² | Kuadrat standar deviasi |
| **Skewness** | (1/N) × Σ[(xᵢ - μ)/σ]³ | Kemencengan distribusi |
| **Kurtosis** | (1/N) × Σ[(xᵢ - μ)/σ]⁴ - 3 | Ketajaman puncak distribusi |
| **IQR** | Q3 - Q1 | Interquartile range, ukuran dispersi |
| **RMS** | √[(1/N) × Σxᵢ²] | Root mean square |
| **Entropy** | -Σ p(xᵢ) × log₂p(xᵢ) | Ukuran ketidakpastian/kemajemukan |

### 2. Domain Fitur TSFEL

TSFEL (Time Series Feature Extraction Library) mengelompokkan 68 fitur ke dalam 3 domain:

**A. Domain Statistik** (~28 fitur)
Contoh: `abs_energy`, `calc_mean`, `calc_median`, `calc_std`, `calc_var`, `skewness`, `kurtosis`, `rms`, `entropy`, `interq_range`, `median_abs_deviation`, `mean_abs_deviation`, `mean_abs_diff`, `median_abs_diff`, `sum_abs_diff`, `mean_diff`, `median_diff`, `slope`, `pk_pk_distance`, `neighbourhood_peaks`, `positive_turning`, `negative_turning`, `hist_mode`, `auc`, `calc_max`, `calc_min`, `distance`, `zero_cross`

**B. Domain Temporal** (~22 fitur)
Contoh: `autocorr`, `dfa`, `hurst_exponent`, `lecmtel_ziv`, `fundamental_frequency`, `max_frequency`, `median_frequency`, `power_bandwidth`, `spectral_centroid`, `spectral_decrease`, `spectral_distance`, `spectral_entropy`, `spectral_kurtosis`, `spectral_skewness`, `spectral_slope`, `spectral_spread`, `spectral_variation`, `spectral_roll_off`, `spectral_roll_on`, `spectral_positive_turning`, `average_power`, `max_power_spectrum`, `human_range_energy`, `calc_centroid`

**C. Domain Fraktal/Wavelet** (~18 fitur)
Contoh: `higuchi_fractal_dimension`, `petrosian_fractal_dimension`, `maximum_fractal_length`, `wavelet_energy`, `wavelet_entropy`, `wavelet_std`, `wavelet_var`, `wavelet_abs_mean`, `mfcc`, `lpcc`, `ecdf`, `ecdf_percentile`, `ecdf_percentile_count`, `ecdf_slope`, `mse`, `dfa`, `spectrogram_mean_coeff`

---

## Tugas

### Deskripsi

Melakukan analisis lengkap terhadap data polutan atmosfer (CO, NO₂, SO₂) dari Kecamatan Jabon, mulai dari ekstraksi fitur time series menggunakan TSFEL, reduksi dimensi PCA, hingga clustering dengan K-Means. Seluruh alur harus dijalankan di **dua platform**: Python (Jupyter Notebook) dan KNIME Analytics Platform.

### Pembagian Fitur (Rahardian Ananta — No. 4)

| Fitur | Fungsi TSFEL | Domain |
|-------|-------------|--------|
| **Fitur 1** | `calc_mean(signal)` | Statistik |
| **Fitur 2** | `calc_median(signal)` | Statistik |

> **Catatan:** Setiap mahasiswa mengerjakan 2 fitur. Total 68 fitur × 3 polutan = **204 kolom** hasil ekstraksi gabungan.

---

### Langkah Pengerjaan

#### FASE 1 — Exploratory Data Analysis (EDA)

**Tujuan:** Memetakan tren data polutan dan mengidentifikasi kemiripan pola antar polutan.

1. Baca data mentah 3 polutan: `jabon_CO.csv`, `jabon_NO2.csv`, `jabon_SO2.csv`
2. Visualisasikan time series harian masing-masing polutan
3. Tambahkan rolling mean 30 hari untuk melihat tren jangka panjang
4. Analisis tren: kapan puncak, kapan rendah, ada pola musiman atau tidak

```python
import pandas as pd
import matplotlib.pyplot as plt

# Baca data
for polutan in ['CO', 'NO2', 'SO2']:
    df = pd.read_csv(f'data/downloads/jabon_pollutants_data/jabon_{polutan}.csv')
    df['date'] = pd.to_datetime(df['date'])
    # Plot time series...
```

#### FASE 2 — Deskripsi Fitur + Perhitungan Manual

**Tujuan:** Mendeskripsikan teori di balik setiap fitur dan membuktikan perhitungan manual vs komputasi TSFEL.

**Untuk `calc_mean` dan `calc_median`:**

**A. Deskripsi Teori**

**calc_mean (Rata-rata Aritmatika):**
- **Definisi:** Jumlah seluruh nilai sinyal dibagi dengan jumlah titik data
- **Rumus:** `μ = (1/N) × Σ(i=1 to N) xᵢ`
- **Interpretasi:** Menunjukkan tingkat konsentrasi rata-rata polutan selama periode pengamatan
- **Karakteristik:** Sensitif terhadap outlier

**calc_median (Nilai Tengah):**
- **Definisi:** Nilai tengah saat seluruh data diurutkan dari kecil ke besar
- **Rumus (N ganjil):** `median = x_{(N+1)/2}`
- **Rumus (N genap):** `median = (x_{N/2} + x_{N/2+1}) / 2`
- **Interpretasi:** Pusat distribusi polutan, lebih robust terhadap outlier dibanding mean
- **Karakteristik:** Tidak sensitif terhadap outlier ekstrem

**B. Contoh Perhitungan Manual**

Ambil 10 sampel pertama dari sinyal NO₂ yang sudah bersih:

```
Data sampel: [0.0000115, 0.0000199, -0.0000001, 0.0000163, 0.0000118,
              0.0000150, 0.0000095, 0.0000130, 0.0000110, 0.0000140]
N = 10
```

**Perhitungan Manual `calc_mean`:**
```
μ = (0.0000115 + 0.0000199 + (-0.0000001) + 0.0000163 + 0.0000118 +
     0.0000150 + 0.0000095 + 0.0000130 + 0.0000110 + 0.0000140) / 10
μ = 0.0001219 / 10
μ = 0.00001219
```

**Perhitungan Manual `calc_median`:**
```
Urutkan data: [-0.0000001, 0.0000095, 0.0000110, 0.0000115, 0.0000118,
                0.0000130, 0.0000140, 0.0000150, 0.0000163, 0.0000199]
N = 10 (genap) → ambil rata-rata posisi ke-5 dan ke-6
median = (0.0000118 + 0.0000130) / 2 = 0.0000124
```

**C. Verifikasi dengan TSFEL**

```python
import numpy as np
import tsfel

# Sinyal sampel
signal = np.array([0.0000115, 0.0000199, -0.0000001, 0.0000163, 0.0000118,
                   0.0000150, 0.0000095, 0.0000130, 0.0000110, 0.0000140])

# Ekstraksi pakai TSFEL
cfg = tsfel.get_features_single_channel(domains=['statistical'])
features = tsfel.time_series_features_extractor(cfg, signal, fs=1)

# Bandingkan
print(f"Manual mean:   0.00001219")
print(f"TSFEL mean:    {features['calc_mean'].values[0]}")
print(f"Manual median: 0.0000124")
print(f"TSFEL median:  {features['calc_median'].values[0]}")
# → Hasil harus SAMA PERSIS
```

#### FASE 3 — Ekstraksi Fitur (68 fitur × 3 polutan)

**Tujuan:** Mengekstrak 68 fitur TSFEL dari masing-masing polutan (CO, NO₂, SO2) untuk Kecamatan Jabon.

1. Bersihkan data: deteksi outlier (IQR), imputasi missing value (interpolasi waktu)
2. Maks missing value: **15%**
3. Ekstrak 68 fitur per polutan menggunakan TSFEL
4. Output: 3 file CSV (satu per polutan), masing-masing berisi 68 kolom fitur
5. Gabungkan jadi satu tabel 204 kolom (68 × 3 polutan)
6. Tambah kolom `nama` dan `daerah`

```python
import pandas as pd
import numpy as np
import inspect
import tsfel.feature_extraction.features as tsfel_features

# Daftar 68 fitur
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

def extract_one(fn_name, signal, fs):
    fn = getattr(tsfel_features, fn_name)
    params = inspect.signature(fn).parameters
    result = fn(signal, fs) if "fs" in params else fn(signal)
    # Convert ke scalar jika perlu
    if isinstance(result, dict) and "values" in result:
        result = result["values"]
    if isinstance(result, (list, tuple, np.ndarray)):
        return float(np.nanmean(np.asarray(result, dtype=float)))
    return float(result)

# Ekstraksi per polutan
for polutan in ['CO', 'NO2', 'SO2']:
    df = pd.read_csv(f'data/downloads/jabon_clean_data/jabon_{polutan}_clean.csv')
    signal = df[polutan].astype(float).values
    row = {}
    for fn_name in FEATURE_LIST:
        try:
            row[fn_name] = extract_one(fn_name, signal, fs=1)
        except:
            row[fn_name] = np.nan
    features_df = pd.DataFrame([row])
    features_df.insert(0, 'nama', 'Rahardian Ananta')
    features_df.insert(1, 'daerah', 'Kecamatan Jabon')
    features_df.to_csv(f'{polutan}_Jabon_TSFEL.csv', index=False)
```

#### FASE 4 — Reduksi Dimensi PCA (68 → 37)

**Tujuan:** Menyusutkan 68 fitur menjadi 37 komponen utama yang paling representatif.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Gabungkan fitur 3 polutan
combined_features = pd.concat([
    pd.read_csv('CO_Jabon_TSFEL.csv'),
    pd.read_csv('NO2_Jabon_TSFEL.csv'),
    pd.read_csv('SO2_Jabon_TSFEL.csv')
], axis=1)

# Standarisasi
scaler = StandardScaler()
X_scaled = scaler.fit_transform(combined_features)

# PCA 68 → 37
pca = PCA(n_components=37)
X_pca = pca.fit_transform(X_scaled)

print(f"Variance explained: {sum(pca.explained_variance_ratio_) * 100:.2f}%")
```

#### FASE 5 — K-Means Clustering (2 Skenario)

**Tujuan:** Menentukan jumlah cluster optimal dan membandingkan hasil tanpa vs dengan reduksi dimensi.

**Skenario 1: Tanpa Reduksi Dimensi (68 fitur)**
```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Elbow Method
inertias = []
silhouettes = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))

# Plot Elbow + Silhouette
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(K_range, inertias, 'bo-')
ax1.set_xlabel('Jumlah Cluster (K)')
ax1.set_ylabel('Inertia')
ax1.set_title('Elbow Method — 68 Fitur')
ax2.plot(K_range, silhouettes, 'ro-')
ax2.set_xlabel('Jumlah Cluster (K)')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Score — 68 Fitur')
plt.tight_layout()
plt.show()

# Tentukan K terbaik (silhouette tertinggi)
best_k = K_range[np.argmax(silhouettes)]
print(f"K terbaik: {best_k} (silhouette={max(silhouettes):.4f})")
```

**Skenario 2: Dengan Reduksi Dimensi (37 fitur PCA)**
```python
# Ulangi langkah yang sama dengan X_pca (37 fitur)
inertias_pca = []
silhouettes_pca = []

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_pca)
    inertias_pca.append(km.inertia_)
    silhouettes_pca.append(silhouette_score(X_pca, labels))

# Bandingkan hasil
print(f"68 fitur — K terbaik: {K_range[np.argmax(silhouettes)]}, silhouette: {max(silhouettes):.4f}")
print(f"37 fitur — K terbaik: {K_range[np.argmax(silhouettes_pca)]}, silhouette: {max(silhouettes_pca):.4f}")
```

**Evaluasi & Komparasi:**
- Bandingkan Silhouette Score kedua skenario
- Bandingkan interpretasi cluster
- Tentukan mana yang lebih representatif

#### FASE 6 — Interpretasi Karakteristik Spasial

- Analisis hasil cluster: Kecamatan dalam cluster sama → karakteristik polutan mirip
- Visualisasikan hasil cluster pada peta (Folium/GeoPandas)
- Catatan pengembangan: ke depan bisa digabung 3 polutan sekaligus (68 × 3 = 204 fitur gabungan)

#### FASE 7 — Implementasi KNIME (Workflow Lengkap)

Seluruh alur analisis harus dijalankan ulang di **KNIME Analytics Platform** menggunakan node-node visual. Berikut workflow lengkap dari awal hingga akhir.

---

##### Workflow Diagram (Alur Node)

```
[CSV Reader]
     │
     ▼
[Missing Value]  ──→  [Numeric Outliers]
     │                       │
     │                       ▼
     │               [Missing Value 2]  (imputasi pasca-outlier)
     │                       │
     ▼                       ▼
[Column Filter]  ←──────────┘
     │
     ├─── SKENARIO 1 (68 Fitur) ──────────────────────────────┐
     │                                                        │
     │   [Normalize] ──→ [K-Means] ──→ [Silhouette]          │
     │                      │                                  │
     │                      ▼                                  │
     │               [Scatter Plot]                            │
     │                                                        │
     ├─── SKENARIO 2 (37 Fitur PCA) ─────────────────────────┐│
     │                                                       ││
     │   [Normalize] ──→ [PCA] ──→ [K-Means] ──→ [Silhouette]│
     │                        │              │                  │
     │                        ▼              ▼                  │
     │               [PCA Expl. Variance] [Scatter Plot]       │
     │                                                        │
     └─────────────── KOMPARASI HASIL ────────────────────────┘│
                                                               │
     [Table Creator] (ringkasan metrik) ←──────────────────────┘
              │
              ▼
     [Excel Writer]  /  [CSV Writer]
```

---

##### Langkah 1: Membaca Data

**Node:** `CSV Reader`

| Konfigurasi | Nilai |
|------------|-------|
| File | `jabon_CO_clean.csv` (ulangi untuk NO₂, SO₂) |
| Separator | Comma (,) |
| Header row | Centang (First row = column names) |
| Column types | `date` → String, kolom polutan → Double |

**Cara kerja:** Node ini membaca file CSV dan menampilkannya sebagai tabel di KNIME. Setelah connect, klik **OK**. Ulangi untuk ketiga polutan atau gunakan **Table Row to Variable** + loop.

---

##### Langkah 2: Deteksi Missing Value (Awal)

**Node:** `Missing Value`

| Konfigurasi | Nilai |
|------------|-------|
| Tab Missing Value Treatment | |
| Kolom polutan (CO/NO2/SO2) | **Remove rows** atau **Mean/Median** (tergantung % missing) |
| Kolom lainnya | Remove (kolom yang tidak relevan) |

**Cara kerja:**
1. Drag node `Missing Value` dari KNIME Node Repository
2. Connect output `CSV Reader` → input `Missing Value`
3. Double-click node → tab ** treat missing values in selected columns**
4. Jika missing < 15% → pilih **Mean** atau **Median**
5. Jika missing > 15% → pertimbangkan **Remove rows** (tapi harus tetap < 15%)
6. Klik **OK**, lalu **Execute**

---

##### Langkah 3: Deteksi Outlier (IQR)

**Node:** `Numeric Outliers`

| Konfigurasi | Nilai |
|------------|-------|
| Method | **IQR (Interquartile Range)** |
| Factor | **1.5** (standar: Q1 - 1.5×IQR s.d. Q3 + 1.5×IQR) |
| Column selection | Kolom polutan saja (CO / NO2 / SO2) |
| Output column | `outlier` (kolom baru: `true`/`false`) |

**Cara kerja:**
1. Drag `Numeric Outliers` dari Repository
2. Connect `Missing Value` output → `Numeric Outliers` input
3. Double-click → pilih kolom polutan sebagai **Selected columns**
4. Method: pilih **IQR**, Factor: **1.5**
5. Centang **Append column with outlier info**
6. **OK** → **Execute**
7. Output: tabel asli + kolom tambahan `Outlier` (TRUE jika outlier)

---

##### Langkah 4: Imputasi Pasca-Outlier

**Node:** `Missing Value` (kedua)

| Konfigurasi | Nilai |
|------------|-------|
| Treatment | **Linear Interpolation** (atau Mean) |
| Kolom polutan | **Linear Interpolation** |

**Cara kerja:**
1. Drag `Missing Value` baru
2. Connect `Numeric Outliers` → `Missing Value 2`
3. Double-click → pada kolom polutan, pilih **Linear interpolation**
4. **OK** → **Execute**
5. Sekarang semua outlier sudah diganti dengan nilai interpolasi → data bersih

---

##### Langkah 5: Filter Kolom

**Node:** `Column Filter`

| Konfigurasi | Nilai |
|------------|-------|
| Tab Include | Kolom polutan (CO / NO2 / SO2), kolom date |
| Tab Exclude | Kolom `outlier`, `feature_index`, kolom tidak relevan lainnya |

**Cara kerja:**
1. Drag `Column Filter`
2. Connect `Missing Value 2` → `Column Filter`
3. Double-click → pindahkan kolom yang **diperlukan** ke sisi **Include**
4. Pindahkan kolom `outlier` dan lainnya ke **Exclude**
5. **OK** → **Execute**

---

##### Langkah 6: Normalisasi

**Node:** `Normalize`

| Konfigurasi | Nilai |
|------------|-------|
| Normalization method | **Z-Score (Standardization)** |
| Apply to | Semua kolom numerik (kolom polutan) |

> **Penting:** Normalisasi wajib sebelum PCA dan K-Means agar fitur dengan skala besar tidak mendominasi.

**Cara kerja:**
1. Drag `Normalize`
2. Connect `Column Filter` → `Normalize`
3. Double-click → method: **Z-Score**
4. Apply to: **All numerical columns**
5. **OK** → **Execute**

---

##### SKENARIO 1: Clustering Tanpa Reduksi Dimensi (68 Fitur)

###### Langkah S1.1: K-Means Clustering

**Node:** `K-Means`

| Konfigurasi | Nilai |
|------------|-------|
| Number of clusters | **3** (mulai dari 3, lalu ubah ke 2, 4, 5 dst. untuk Elbow) |
| Random seed | **42** (agar hasil reproducible) |
| Max iterations | **100** (default) |
| Distance function | **Euclidean** |
| Initialize | **K-Means++** |

**Cara kerja:**
1. Drag `K-Means`
2. Connect `Normalize` → `K-Means`
3. Double-click → Number of clusters: **3** (awal)
4. **OK** → **Execute**
5. Output: tabel dengan kolom tambahan `Cluster` (label cluster: 0, 1, 2, ...)

> **Elbow Method:** Untuk mencari K optimal, jalankan node K-Means **berulang kali** dengan K = 2, 3, 4, 5, ..., 10. Catat inertia (within-cluster sum of squares) di masing-masing.

###### Langkah S1.2: Evaluasi Silhouette

**Node:** `Silhouette Coefficient` (atau gunakan Python Script untuk hitung manual)

| Konfigurasi | Nilai |
|------------|-------|
| Distance function | **Euclidean** |
| Column | Kolom hasil cluster label |

```python
# Jika pakai Python Script node di KNIME:
from sklearn.metrics import silhouette_score
import numpy as np

# df adalah tabel masukan KNIME
X = df.select_dtypes(include=[np.number]).values
labels = df['Cluster'].values
score = silhouette_score(X, labels)
print(f"Silhouette Score: {score:.4f}")
```

###### Langkah S1.3: Visualisasi Hasil

**Node:** `Scatter Plot`

| Konfigurasi | Nilai |
|------------|-------|
| X-Axis | Kolom pertama (atau PCA komponen 1 jika pakai) |
| Y-Axis | Kolom kedua (atau PCA komponen 2) |
| Color | Kolom `Cluster` |

**Cara kerja:**
1. Connect `K-Means` → `Scatter Plot`
2. Double-click → pilih X, Y, dan Color column
3. **OK** → **Execute** → muncul plot interaktif

---

##### SKENARIO 2: Clustering Dengan Reduksi Dimensi PCA (68 → 37 Fitur)

###### Langkah S2.1: PCA

**Node:** `PCA`

| Konfigurasi | Nilai |
|------------|-------|
| Number of components | **37** |
| Scaling | **Z-Score** (atau gunakan hasil Normalize sebelumnya) |
| Method | **SVD** (default) |

**Cara kerja:**
1. Drag `PCA` dari Repository
2. Connect `Normalize` (output dari Langkah 6) → `PCA`
3. Double-click → Number of components: **37**
4. **OK** → **Execute**
5. Output: tabel baru dengan 37 kolom (PC1 s.d. PC37) + kolom `Explained Variance`

###### Langkah S2.2: Cek Variance Explained

**Node:** `PCA` (sudah termasuk output variance)

Atau gunakan **Python Script**:
```python
# Di KNIME Python Script node
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X = df.select_dtypes(include=[np.number]).values
pca = PCA(n_components=37)
X_pca = pca.fit_transform(X)

total_var = sum(pca.explained_variance_ratio_) * 100
print(f"Total variance explained by 37 PCs: {total_var:.2f}%")

# Tampilkan variance per komponen
for i, var in enumerate(pca.explained_variance_ratio_):
    print(f"PC{i+1}: {var*100:.2f}%")
```

> **Target:** 37 komponen harus menjelaskan ≥ 85-95% total variance. Jika kurang, tambah jumlah komponen.

###### Langkah S2.3: K-Means pada 37 Fitur PCA

**Node:** `K-Means`

| Konfigurasi | Nilai |
|------------|-------|
| Number of clusters | **3** (awal, lalu variasikan untuk Elbow) |
| Random seed | **42** |
| Max iterations | **100** |
| Distance function | **Euclidean** |
| Initialize | **K-Means++** |

**Cara kerja:** Sama seperti Skenario 1, tapi inputnya dari output `PCA` (37 kolom).

###### Langkah S2.4: Evaluasi + Visualisasi

Sama seperti Skenario 1: `Silhouette Coefficient` + `Scatter Plot`.

---

##### KOMPARASI HASIL: 68 Fitur vs 37 Fitur PCA

**Node:** `Table Creator` (untuk merangkum hasil)

| Konfigurasi | Nilai |
|------------|-------|
| Kolom 1 | `Skenario` (String) |
| Kolom 2 | `Jumlah_Fitur` (Integer) |
| Kolom 3 | `K_Terbaik` (Integer) |
| Kolom 4 | `Silhouette_Score` (Double) |
| Kolom 5 | `Variance_Explained` (String) |

**Data yang dimasukkan:**

| Skenario | Jumlah Fitur | K Terbaik | Silhouette Score | Variance Explained |
|----------|-------------|-----------|-----------------|-------------------|
| Tanpa PCA | 68 | (dari Elbow) | (tertinggi) | 100% |
| Dengan PCA | 37 | (dari Elbow) | (tertinggi) | (dari output PCA) |

**Cara kerja:**
1. Drag `Table Creator`
2. Masukkan data komparasi di atas
3. Connect ke `Excel Writer` atau `CSV Writer` untuk export
4. **Execute**

---

##### Langkah Terakhir: Export Hasil

**Node:** `CSV Writer` atau `Excel Writer`

| Konfigurasi | Nilai |
|------------|-------|
| File path | `hasil_klastering_jabon.csv` (atau `.xlsx`) |
| Write header | Centang |

**Output:** File hasil clustering siap diupload ke web statis.

---

##### Ringkasan Seluruh Node KNIME

| No. | Node | Fungsi | Output |
|-----|------|--------|--------|
| 1 | CSV Reader | Membaca data mentah | Tabel data harian |
| 2 | Missing Value | Cek & handle missing value awal | Tabel tanpa NaN |
| 3 | Numeric Outliers | Deteksi outlier (IQR 1.5) | Tabel + kolom outlier |
| 4 | Missing Value (2) | Imputasi pasca-outlier (interpolasi) | Tabel bersih |
| 5 | Column Filter | Pilih kolom yang diperlukan | Tabel ringkas |
| 6 | Normalize | Standarisasi Z-Score | Tabel ternormalisasi |
| 7 | K-Means (Skenario 1) | Clustering 68 fitur | Tabel + label cluster |
| 8 | PCA | Reduksi dimensi 68→37 | Tabel 37 PC |
| 9 | K-Means (Skenario 2) | Clustering 37 fitur PCA | Tabel + label cluster |
| 10 | Silhouette Coefficient | Evaluasi kualitas cluster | Skor silhouette |
| 11 | Scatter Plot | Visualisasi cluster | Plot interaktif |
| 12 | Table Creator | Ringkasan komparasi | Tabel metrik |
| 13 | CSV/Excel Writer | Export hasil akhir | File CSV/XLSX |

---

##### Tips KNIME

- **Variasi K:** Untuk Elbow Method, duplikat sub-workflow K-Means dan ubah `Number of clusters` di masing-masing (K=2 s.d. K=10). Jalankan semua, lalu kumpulkan inertia-nya.
- **Loop (opsional):** Bisa pakai `Loop` node untuk otomasi variasi K, tapi untuk tugas ini cukup manual.
- **Python Integration:** Jika ada node yang tidak tersedia (misal TSFEL), gunakan `Python Script` node. Install TSFEL di environment KNIME: `pip install tsfel` di Python Preferences KNIME.
- **Metadata:** Tambahkan annotation (klik kanan workspace → **Add Annotation**) untuk menjelaskan setiap tahap workflow.
- **Save:** Save workflow dengan nama `PSD_Klastering_Jabon_(nama).knwf`

---

### Catatan Penting

- **Data:** Kecamatan Jabon, periode 31 Agustus 2025 — 31 Agustus 2026 (366 hari)
- **Polutan yang diekstraksi:** CO, NO₂, SO₂ (bukan 6 polutan, hanya 3 ini)
- **Maks missing value:** 15%
- **Jumlah fitur per polutan:** 68 fitur TSFEL
- **Total kolom fitur:** 68 × 3 polutan = **204 kolom**
- **Output per orang:** 1 file CSV per polutan (nama + daerah + 68 fitur)
- **Pengumpulan:** Upload ke https://psd.basisdata2-c.my.id/index.php
- **Deadline pengumpulan fitur:** Jumat malam, 18 September 2026
- **Deadline clustering:** Sabtu-Minggu (setelah semua fitur terkumpul)
- **Dual platform:** Python + KNIME
- **Preprocessing wajib sebelum ekstraksi:** deteksi outlier (IQR) → imputasi missing value (interpolasi waktu)
- **File data clean sudah tersedia:** `data/downloads/jabon_clean_data/jabon_{CO,NO2,SO2}_clean.csv`
- **Script otomatis:** `run_all_jabon.py` bisa dijadikan referensi untuk alur kerja

### Checklist Tugas Individu (Rahardian Ananta)

- [ ] EDA time series 3 polutan (CO, NO₂, SO₂) — plot harian + rolling mean
- [ ] Deskripsi teori `calc_mean` dan `calc_median`
- [ ] Perhitungan manual kedua fitur (dengan sampel data nyata)
- [ ] Verifikasi manual vs TSFEL → hasil harus sama
- [ ] Ekstraksi fitur `calc_mean` + `calc_median` untuk CO, NO₂, SO₂
- [ ] Output CSV: nama, daerah, 6 kolom fitur (2 fitur × 3 polutan)
- [ ] Upload ke web statis
- [ ] Implementasi di KNIME

---

## Referensi

- [TSFEL Documentation](https://tsfel.readthedocs.io/)
- [Scikit-learn PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
- [Scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [KNIME Analytics Platform](https://www.knime.com/)
- Data: Sentinel-5P L2 via Copernicus Data Space Ecosystem (openeo)
- Web pengumpulan: https://psd.basisdata2-c.my.id/index.php
