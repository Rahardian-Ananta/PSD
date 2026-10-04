"""Perbaikan baris Jabon: backup + ganti dengan baris referensi pipeline 4.2.
linear <- fill time | poly <- fill poly3. Simpan snapshot output lama utk diff."""
import json
import shutil

import pandas as pd

# 0. snapshot output lama (sebelum re-run) untuk diff
shutil.copy("data/processed/best_config_linear.json", "data/processed/_prev_best_linear.json")
shutil.copy("data/processed/best_config_poly.json", "data/processed/_prev_best_poly.json")
shutil.copy("data/processed/labels_best_linear.csv", "data/processed/_prev_labels_linear.csv")
shutil.copy("data/processed/labels_best_poly.csv", "data/processed/_prev_labels_poly.csv")
print("snapshot output lama disimpan (_prev_*)")

# 1. backup CSV sumber asli
shutil.copy("data/ekstraksi_fitur_linear.csv",
            "arsip/ekstraksi_fitur_linear_SEBELUM_fix_jabon.csv")
shutil.copy("data/ekstraksi_fitur_polynomial.csv",
            "arsip/ekstraksi_fitur_polynomial_SEBELUM_fix_jabon.csv")
print("backup sumber asli -> arsip/")

# 2. baris referensi (tervalidasi identik dgn 04_*_Jabon_TSFEL*.csv)
ref_time = pd.read_csv("04_feature_extraction/All-Pollutants-Jabon_TSFEL.csv")
ref_poly = pd.read_csv("04_feature_extraction/All-Pollutants-Jabon_TSFEL_poly3.csv")
for _r in (ref_time, ref_poly):  # selaraskan kapitalisasi prefix dgn file kelas
    _r.columns = [c.lower() if c.split("_")[0] in ("NO2", "SO2", "CO") else c
                  for c in _r.columns]
assert ref_time.shape == (1, 204) and ref_poly.shape == (1, 204)

for path, ref, tag in [("data/ekstraksi_fitur_linear.csv", ref_time, "linear"),
                       ("data/ekstraksi_fitur_polynomial.csv", ref_poly, "poly")]:
    df = pd.read_csv(path)
    assert list(df.columns[3:]) == list(ref.columns), f"urutan kolom {tag} beda!"
    mask = df["nama"] == "Rahardian Ananta"
    assert int(mask.sum()) == 1, f"baris Rahardian di {tag}: {int(mask.sum())}"
    old = df.loc[mask].iloc[0]
    print(f"[{tag}] sebelum: id={old['id']} daerah={old['daerah']!r} "
          f"no2_std={old['no2_calc_std']:.3g}")
    for c in ref.columns:
        df.loc[mask, c] = float(ref.iloc[0][c])
    new = df.loc[mask].iloc[0]
    print(f"[{tag}] sesudah: id={new['id']} daerah={new['daerah']!r} "
          f"no2_std={new['no2_calc_std']:.3g} (id/nama/daerah TIDAK berubah)")
    df.to_csv(path, index=False)
    print(f"[{tag}] tersimpan: {path} {df.shape}")

prev = json.load(open("data/processed/_prev_best_linear.json"))
print("pemenang lama linear:", {k: prev[k] for k in ("dimensi", "k", "silhouette", "ukuran_cluster")})
prev = json.load(open("data/processed/_prev_best_poly.json"))
print("pemenang lama poly:", {k: prev[k] for k in ("dimensi", "k", "silhouette", "ukuran_cluster")})
