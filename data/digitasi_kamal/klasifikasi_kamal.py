"""
klasifikasi_kamal.py
Kandidat Sawah vs Non-Sawah, Kecamatan Kamal (Sentinel-2, satu tanggal)

Alur:
  citra -> preprocessing -> fitur (band + indeks + tekstur)
        -> K-Means -> pelabelan klaster oleh analis (interpretasi visual)
        -> bersihkan patch kecil -> polygonisasi -> seleksi 100 sample -> SHP

Sumber label: interpretasi visual analis terhadap tiap klaster (komposit
warna + profil spektral). Tidak ada ambang NDVI/tekstur otomatis, karena
pada satu tanggal kemarau sawah bera dan pohon rapat tidak bisa dipisah
oleh ambang tunggal.

PENTING: hasil adalah KANDIDAT, bukan ground truth.
Validasi dengan citra resolusi tinggi / survei lapangan (kolom `validasi`).
"""

import os

import numpy as np
import pandas as pd
import rasterio
import geopandas as gpd
from scipy import ndimage
from rasterio.features import shapes
from affine import Affine
from shapely.geometry import shape
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# ============================================================
# KONFIGURASI
# ============================================================

INPUT = "s2_kamal.tif"

OUTPUT_RASTER = "klasifikasi_kamal.tif"
OUTPUT_SHP = "klasifikasi_kamal.shp"
OUTPUT_SAMPLE = "sample_polygon_100_kamal.shp"

RANDOM_STATE = 42

JUMLAH_KLASTER = 8      # sengaja berlebih, lalu digabung lewat pelabelan
JENDELA_TEKSTUR = 3     # jendela tekstur lokal (piksel)
MIN_PIKSEL_SAWAH = 50   # patch sawah < 50 piksel (~0,5 ha) dianggap bukan hamparan sawah

OUTPUT_KLASTER = "klaster_kamal.tif"   # peta klaster mentah, buka di QGIS

# LABEL KLASTER (hasil interpretasi visual, lihat profil klaster yang dicetak)
#   klaster: (kode_kelas, NDVI_acuan)
#   kode_kelas: 1 Sawah | 2 Pohon/Kebun/Vegetasi lain | 3 Terbangun/Lahan terbuka
#               4 Air/Tergenang
#   NDVI_acuan dipakai untuk memastikan klaster belum berubah (toleransi 0,05).
#   Jika script gagal di pengecekan ini, label ulang klaster.
LABEL_KLASTER = {
    0: (2, 0.81),   # tajuk rapat (NDVI tinggi, SWIR rendah)
    1: (1, 0.31),   # hamparan lahan pertanian terbuka/bera (dataran utara)
    2: (4, 0.25),   # air dangkal/tambak
    3: (3, 0.05),   # atap/objek sangat terang
    4: (2, 0.56),   # vegetasi campur/pekarangan/kebun
    5: (4, 0.24),   # air dangkal/tambak
    6: (3, 0.17),   # permukiman/lahan terbangun
    7: (1, 0.29),   # hamparan lahan pertanian terbuka/bera
}

MIN_PIKSEL = 25         # polygon sample minimal 25 piksel (~0,25 ha)
MAX_PIKSEL = 120        # polygon sample maksimal 120 piksel (~1,2 ha)
MIN_JARAK = 3           # jarak minimum antar polygon sample (piksel)
KUOTA = {1: 50, 2: 25, 3: 25}   # Sawah 50 | Non-Sawah: pohon 25 + terbangun 25

# kode kelas detail pada peta hasil
NAMA_DETAIL = {
    1: "Sawah",
    2: "Pohon/Kebun/Vegetasi lain",
    3: "Terbangun/Lahan terbuka",
    4: "Air/Tergenang",
}


# ============================================================
# 1. BACA CITRA
# ============================================================

with rasterio.open(INPUT) as src:
    image = src.read().astype(np.float32)
    profile = src.profile.copy()
    transform = src.transform
    crs = src.crs
    nodata = src.nodata
    height = src.height
    width = src.width

print("Ukuran raster :", width, "x", height)
print("Jumlah band   :", image.shape[0])
print("CRS           :", crs)

if image.shape[0] != 6:
    raise RuntimeError("Citra harus 6 band: B02, B03, B04, B08, B11, B12.")

if not crs.is_projected:
    print("PERINGATAN: CRS bukan projected, kolom luas bukan meter persegi.")


# ============================================================
# 2. PREPROCESSING: MASK PIKSEL VALID + SKALA REFLEKTANSI
# ============================================================

valid = np.all(np.isfinite(image), axis=0)
valid &= ~np.all(image == 0, axis=0)
if nodata is not None and np.isfinite(nodata):
    valid &= ~np.any(image == nodata, axis=0)

image = np.nan_to_num(image)
image[:, ~valid] = 0    # nilai nodata (mis. -32768) dinolkan agar tidak mencemari tekstur

# Jika nilai masih DN Sentinel-2 (0-10000), ubah ke reflektansi 0-1
if image[:, valid].max() > 2:
    image = image / 10000.0

B02, B03, B04, B08, B11, B12 = image


# ============================================================
# 3. INDEKS SPEKTRAL
# ============================================================

def safe_div(a, b):
    return np.divide(a, b, out=np.zeros_like(a), where=b != 0)


NDVI = safe_div(B08 - B04, B08 + B04)   # kehijauan vegetasi
NDWI = safe_div(B03 - B08, B03 + B08)   # air (McFeeters)
NDBI = safe_div(B11 - B08, B11 + B08)   # lahan terbangun / tanah


# ============================================================
# 4. FITUR SPASIAL (TEKSTUR LOKAL)
#
# Sawah: ditanam seragam per petak  -> NIR halus (tekstur rendah)
# Pohon/kebun: tajuk + bayangan     -> NIR bervariasi (tekstur tinggi)
# ============================================================

BOBOT = valid.astype(np.float32)
BOBOT_LOKAL = ndimage.uniform_filter(BOBOT, JENDELA_TEKSTUR)


def rata_lokal(a):
    # rata-rata hanya dari piksel valid di sekitar (tepi data tidak mencemari)
    return safe_div(ndimage.uniform_filter(a * BOBOT, JENDELA_TEKSTUR),
                    BOBOT_LOKAL)


def std_lokal(a):
    rata = rata_lokal(a)
    rata2 = rata_lokal(a * a)
    return np.sqrt(np.maximum(rata2 - rata ** 2, 0))


TEX_NIR = safe_div(std_lokal(B08), rata_lokal(B08))   # koef. variasi NIR
TEX_NDVI = std_lokal(NDVI)


# ============================================================
# 5. FEATURE STACK
# ============================================================

NAMA_FITUR = [
    "B02", "B03", "B04", "B08", "B11", "B12",
    "NDVI", "NDWI", "NDBI", "TEX_NIR", "TEX_NDVI",
]

fitur = np.stack(
    [B02, B03, B04, B08, B11, B12, NDVI, NDWI, NDBI, TEX_NIR, TEX_NDVI],
    axis=-1,
)

X = fitur.reshape(-1, len(NAMA_FITUR))[valid.ravel()]
print("Piksel valid  :", len(X))


# ============================================================
# 6. K-MEANS (FITUR DISTANDARISASI)
#
# Standardisasi wajib: tanpa itu reflektansi mengalahkan indeks.
# ============================================================

print("\nMenjalankan K-Means...")

X_std = StandardScaler().fit_transform(X)

rng = np.random.default_rng(RANDOM_STATE)
idx = rng.choice(len(X_std), min(50000, len(X_std)), replace=False)

kmeans = KMeans(
    n_clusters=JUMLAH_KLASTER,
    random_state=RANDOM_STATE,
    n_init=10,
)
kmeans.fit(X_std[idx])
label_klaster = kmeans.predict(X_std)


# ============================================================
# 7. PROFIL KLASTER (rata-rata fitur, satuan asli)
# ============================================================

profil = pd.DataFrame(X, columns=NAMA_FITUR)
profil["klaster"] = label_klaster
ringkas = profil.groupby("klaster")[NAMA_FITUR].mean()
ringkas["persen"] = 100 * profil.groupby("klaster").size() / len(profil)


# ============================================================
# 8. SIMPAN PETA KLASTER MENTAH (UNTUK DICEK DI QGIS)
# ============================================================

klaster_flat = np.full(height * width, 255, dtype=np.uint8)
klaster_flat[valid.ravel()] = label_klaster
profile_klaster = profile.copy()
profile_klaster.update(count=1, dtype="uint8", nodata=255, compress="lzw")
with rasterio.open(OUTPUT_KLASTER, "w", **profile_klaster) as dst:
    dst.write(klaster_flat.reshape(height, width), 1)


# ============================================================
# 9. PELABELAN KLASTER (INTERPRETASI VISUAL ANALIS)
#
# Mengapa bukan ambang otomatis? Uji pada citra Kamal menunjukkan
# aturan "vegetasi + tekstur halus = sawah" melabeli tajuk pohon rapat
# sebagai sawah, sementara sawah bera (NDVI rendah) dianggap tanah.
# Maka label tiap klaster ditentukan analis dan dicatat di LABEL_KLASTER.
# ============================================================

tabel_kode = np.zeros(JUMLAH_KLASTER, dtype=np.uint8)

for c in range(JUMLAH_KLASTER):
    kode, ndvi_acuan = LABEL_KLASTER[c]
    if abs(ringkas.loc[c, "NDVI"] - ndvi_acuan) > 0.05:
        raise RuntimeError(
            f"Klaster {c} berubah (NDVI {ringkas.loc[c, 'NDVI']:.2f}, "
            f"acuan {ndvi_acuan:.2f}). Lihat profil & {OUTPUT_KLASTER}, "
            "lalu perbarui LABEL_KLASTER."
        )
    tabel_kode[c] = kode

ringkas["kelas_detail"] = [NAMA_DETAIL[tabel_kode[c]] for c in ringkas.index]

print("\nProfil klaster (rata-rata fitur):")
print(ringkas.round(3).to_string())


# ============================================================
# 10. PETA KELAS + BERSIHKAN PATCH SAWAH KECIL
# ============================================================

peta_flat = np.zeros(height * width, dtype=np.uint8)
peta_flat[valid.ravel()] = tabel_kode[label_klaster]
peta = peta_flat.reshape(height, width)

label_patch, _ = ndimage.label(peta == 1)
ukuran_patch = np.bincount(label_patch.ravel())
terlalu_kecil = ukuran_patch < MIN_PIKSEL_SAWAH
terlalu_kecil[0] = False
peta[terlalu_kecil[label_patch]] = 2   # jadi vegetasi lain

print("\nKomposisi peta hasil:")
for kode, nama in NAMA_DETAIL.items():
    print(f"  {nama:28s}: {100 * np.mean(peta[valid] == kode):5.1f} %")

profile.update(count=1, dtype="uint8", nodata=0, compress="lzw")
with rasterio.open(OUTPUT_RASTER, "w", **profile) as dst:
    dst.write(peta, 1)


# ============================================================
# 11. POLYGONISASI KANDIDAT
# ============================================================

print("\nMembuat polygon kandidat...")

geoms, kodes = [], []
for geom, nilai in shapes(peta, mask=peta > 0, transform=transform,
                          connectivity=4):
    geoms.append(shape(geom))
    kodes.append(int(nilai))

kandidat = gpd.GeoDataFrame(
    {"kelas": ["Sawah" if k == 1 else "Non-Sawah" for k in kodes]},
    geometry=geoms,
    crs=crs.to_string(),
)
kandidat["luas"] = kandidat.geometry.area
kandidat["id"] = np.arange(1, len(kandidat) + 1)
kandidat = kandidat[["id", "kelas", "luas", "geometry"]]

n_kand_sawah = int((kandidat["kelas"] == "Sawah").sum())
n_kand_non = int((kandidat["kelas"] == "Non-Sawah").sum())

kandidat.to_file(OUTPUT_SHP, driver="ESRI Shapefile")


# ============================================================
# 12. SELEKSI SAMPLE: REGION GROWING DI INTI KELAS
#
# Tiap sample tumbuh dari satu piksel "inti" (semua tetangga 8 arah
# sekelas) ke piksel tetangga sekelas, sampai MAX_PIKSEL atau sampai
# habis. Bentuk polygon mengikuti bentuk area kelas pada peta,
# batasnya tetap batas piksel, dan tiap sample terpisah dari yang lain.
# ============================================================

def inti_kelas(kode):
    return ndimage.binary_erosion(
        peta == kode, structure=np.ones((3, 3)), border_value=0
    )


def tumbuhkan(seed, inti, terlarang):
    tumbuh = set()
    perbatasan = [seed]
    terdaftar = {seed}
    while perbatasan and len(tumbuh) < MAX_PIKSEL:
        i = int(rng.integers(len(perbatasan)))
        perbatasan[i], perbatasan[-1] = perbatasan[-1], perbatasan[i]
        r, c = perbatasan.pop()
        tumbuh.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (r + dr, c + dc)
            if (0 <= n[0] < height and 0 <= n[1] < width
                    and inti[n] and not terlarang[n]
                    and n not in terdaftar):
                perbatasan.append(n)
                terdaftar.add(n)
    return tumbuh


def piksel_ke_polygon(piksel):
    rr = [p[0] for p in piksel]
    cc = [p[1] for p in piksel]
    r0, c0 = min(rr), min(cc)
    kecil = np.zeros((max(rr) - r0 + 1, max(cc) - c0 + 1), dtype=np.uint8)
    for r, c in piksel:
        kecil[r - r0, c - c0] = 1
    geom, _ = next(shapes(kecil, mask=kecil == 1,
                          transform=transform * Affine.translation(c0, r0),
                          connectivity=4))
    return shape(geom)


terlarang = np.zeros((height, width), dtype=bool)
baris = []
jumlah_per_kode = {}

for kode, jumlah in KUOTA.items():
    inti = inti_kelas(kode)
    seeds = np.argwhere(inti)
    seeds = seeds[rng.permutation(len(seeds))]
    dapat = 0
    for r, c in seeds:
        if dapat == jumlah:
            break
        if terlarang[r, c]:
            continue
        piksel = tumbuhkan((int(r), int(c)), inti, terlarang)
        if len(piksel) < MIN_PIKSEL:          # area inti terlalu kecil
            for p in piksel:
                terlarang[p] = True
            continue
        mask = np.zeros((height, width), dtype=bool)
        mask[tuple(zip(*piksel))] = True
        terlarang |= ndimage.binary_dilation(mask, iterations=MIN_JARAK)
        baris.append({
            "kelas": "Sawah" if kode == 1 else "Non-Sawah",
            "geometry": piksel_ke_polygon(piksel),
        })
        dapat += 1
    if dapat < jumlah:
        raise RuntimeError(
            f"Kelas '{NAMA_DETAIL[kode]}': hanya {dapat} polygon dari "
            f"{jumlah} yang diminta. Kecilkan MIN_PIKSEL atau MIN_JARAK."
        )
    jumlah_per_kode[NAMA_DETAIL[kode]] = dapat

sample = gpd.GeoDataFrame(
    pd.DataFrame(baris), geometry="geometry", crs=crs.to_string()
)
sample["luas"] = sample.geometry.area
sample["id"] = np.arange(1, len(sample) + 1)
sample = sample[["id", "kelas", "luas", "geometry"]]


# ============================================================
# 13. SIMPAN SAMPLE (DAN VERIFIKASI FILE TERTULIS)
# ============================================================

sample.to_file(OUTPUT_SAMPLE, driver="ESRI Shapefile")

cek = gpd.read_file(OUTPUT_SAMPLE)
if len(cek) != 100:
    raise RuntimeError(f"SHP sample terbaca {len(cek)} polygon, harusnya 100.")

n_samp_sawah = int((cek["kelas"] == "Sawah").sum())
n_samp_non = int((cek["kelas"] == "Non-Sawah").sum())


# ============================================================
# 14. RINGKASAN
# ============================================================

print("\n========================================")
print("RINGKASAN")
print("========================================")
print("Polygon kandidat Sawah     :", n_kand_sawah)
print("Polygon kandidat Non-Sawah :", n_kand_non)
print("Sample Sawah               :", n_samp_sawah)
print("Sample Non-Sawah           :", n_samp_non)
print("Rincian sample per jenis   :", jumlah_per_kode)
print("Luas sample (m2)           : min", round(float(cek["luas"].min())),
      "| maks", round(float(cek["luas"].max())))
print("Kolom SHP sample           :", [k for k in cek.columns if k != "geometry"])
print("\nFile output:")
for f in (OUTPUT_SAMPLE, OUTPUT_SHP, OUTPUT_RASTER, OUTPUT_KLASTER):
    print(" ", os.path.abspath(f))
print("\nCatatan: semua label masih KANDIDAT. Validasi dulu sebelum dipakai.")