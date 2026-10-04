"""Peta clustering Folium — 2 varian (LINEAR & POLYNOMIAL), tugas PSD 5.7.
Lapisan ganda:
  (a) Peta PEMENANG 5.6a/5.6b (k dari best_config, nama file lama, tidak berubah).
  (b) Peta EKSPERIMEN k yang bisa diatur: K_LIN / K_POLY (2..5) pada dim 204,
      file berekstensi _kN. Perbandingan k=2..5 + ARI linear-vs-poly dicetak.
Join dengan boundary data/spasial/daftar_kecamatan.csv (kunci koma-insensitif,
seragam di kedua sisi). Wilayah tanpa boundary/label DILAPORKAN, tidak dikarang.
Jalankan via: python 05_clustering/run_57.py  (dari root repo)
"""
import json
import os
import re
from pathlib import Path

import folium
import geopandas as gpd
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

SEED = 42
VARIANTS = ["linear", "poly"]
K_LIN = 2   # UBAH 2..5 untuk eksperimen linear
K_POLY = 2  # UBAH 2..5 untuk eksperimen polynomial
PALET = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd",
         "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

ROOT = Path(__file__).resolve().parent.parent  # root repo


def P(rel):
    """Path absolut dari path repo-root-relatif (kerja dari cwd mana pun)."""
    return str(ROOT / rel)


def norm(s):
    """Kunci join peta: huruf kecil + koma dianggap spasi + rapatkan spasi."""
    s = str(s).strip().lower().replace(",", " ")
    return " ".join(re.split(r"\s+", s))


# Alias manual TERDOKUMENTASI (bukan tebakan): kunci label -> kunci daftar.
# 'sidoarjo wonoayu' (label) = 'wonoayu' (daftar: kabupaten tafsir Sidoarjo,
# boundary data/spasial/Wonoayu/Wonoayu.geojson, status OK). Tanpa alias ini,
# Wonoayu hilang dari peta dan Jabon tampak sendirian padahal secluster.
ALIAS = {"sidoarjo wonoayu": "wonoayu"}


def apply_alias(keys):
    return keys.map(lambda k: ALIAS.get(k, k))


def cluster_at(variant, k, dim=204):
    assert 2 <= k <= 5, f"k={k} di luar rentang eksperimen 2..5"
    Xd = pd.read_csv(P(f"data/processed/X_{variant}_{dim}.csv")).to_numpy()
    daerah = pd.read_csv(P(f"data/processed/clustering_{variant}_{dim}.csv"))["daerah"].tolist()
    lab = KMeans(n_clusters=k, random_state=SEED, n_init=10,
                 max_iter=300).fit_predict(Xd)
    sil = float(silhouette_score(Xd, lab))
    sizes = pd.Series(lab).value_counts().sort_index().tolist()
    if min(sizes) == 1:
        print(f"[{variant} k={k}] PERINGATAN: mengandung singleton {sizes} "
              f"— peta tetap dibuat, tafsirkan hati-hati.")
    labels = pd.DataFrame({"daerah": daerah, "cluster": lab})
    labels.to_csv(P(f"data/processed/labels_{variant}_k{k}.csv"), index=False)
    return labels, sil, sizes


def comparison_table():
    print("=== Perbandingan k=2..5 (dim 204) + kesepakatan linear-vs-poly (ARI) ===")
    labs = {}
    rows = []
    for v in VARIANTS:
        Xd = pd.read_csv(P(f"data/processed/X_{v}_204.csv")).to_numpy()
        for k in range(2, 6):
            lab = KMeans(n_clusters=k, random_state=SEED, n_init=10,
                         max_iter=300).fit_predict(Xd)
            labs[(v, k)] = lab
            sizes = pd.Series(lab).value_counts().sort_index().tolist()
            rows.append({"varian": v, "k": k,
                         "silhouette": round(float(silhouette_score(Xd, lab)), 4),
                         "ukuran": ";".join(map(str, sizes)),
                         "singleton": min(sizes) == 1})
    grid = pd.DataFrame(rows)
    print(grid.to_string(index=False))
    print("--- ARI (linear vs poly, k sama; selaras via kunci koma-insensitif) ---")
    for k in range(2, 6):
        dl = pd.read_csv(P("data/processed/clustering_linear_204.csv"))["daerah"].map(norm)
        dp = pd.read_csv(P("data/processed/clustering_poly_204.csv"))["daerah"].map(norm)
        common = sorted(set(dl) & set(dp))
        ml = dict(zip(dl, labs[("linear", k)]))
        mp = dict(zip(dp, labs[("poly", k)]))
        ari = adjusted_rand_score([ml[c] for c in common], [mp[c] for c in common])
        print(f"k={k}: ARI={ari:.3f} (n_selaras={len(common)})")
    return grid


def build_map(labels, variant, k, suffix):
    daftar = pd.read_csv(P("data/spasial/daftar_kecamatan.csv"))
    daftar["key"] = daftar["daerah"].map(norm)
    labels["key"] = apply_alias(labels["daerah"].map(norm))
    cl = labels.set_index("key")["cluster"].to_dict()

    recs, missing = [], []
    for _, r in daftar.iterrows():
        fp = r["file_geojson"]
        if not isinstance(fp, str) or not fp.strip() or not os.path.exists(ROOT / fp):
            missing.append(r["daerah"])
            continue
        g = gpd.read_file(ROOT / fp).to_crs(4326)
        g["daerah"] = r["daerah"]
        g["cluster"] = cl.get(r["key"])
        recs.append(g[["daerah", "cluster", "geometry"]])
    gj = pd.concat(recs, ignore_index=True)
    nan_lab = gj[gj["cluster"].isna()]["daerah"].tolist()
    print(f"[{variant} k={k}] terjoin: {len(gj)} poligon; cluster NaN: {nan_lab}")
    print(f"[{variant} k={k}] tanpa boundary: {missing}")
    nolink = labels[~labels["key"].isin(set(daftar["key"]))]["daerah"].tolist()
    print(f"[{variant} k={k}] label tanpa pasangan daftar: {nolink}")
    gj.to_file(P(f"data/spasial/cluster_map_{variant}{suffix}.geojson"), driver="GeoJSON")

    gj_plot = gj.dropna(subset=["cluster"]).copy()
    gj_plot["cluster"] = gj_plot["cluster"].astype(int).astype(str)
    gj_plot["geometry"] = gj_plot.geometry.simplify(0.001, preserve_topology=True)
    m = folium.Map(location=[-2.5, 118.0], zoom_start=5, tiles=None)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Esri (bawaan)").add_to(m)
    folium.TileLayer(tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
                     attr="OpenTopoMap", name="OpenTopoMap (cadangan)").add_to(m)
    kls = sorted(gj_plot["cluster"].unique())
    warna = {kk: PALET[i % len(PALET)] for i, kk in enumerate(kls)}
    for kk in kls:
        sub = gj_plot[gj_plot["cluster"] == kk]
        folium.GeoJson(
            sub.to_json(),
            style_function=lambda f, kk=kk: {
                "fillColor": warna[kk], "color": "black",
                "weight": 0.8, "fillOpacity": 0.65},
            tooltip=folium.GeoJsonTooltip(fields=["daerah", "cluster"],
                                          aliases=["Daerah", "Cluster"]),
            name=f"Cluster {kk} ({len(sub)} wilayah)"
        ).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    bars = "".join(
        f"<span style='color:{warna[kk]};'>&#9632;</span> Cluster {kk} "
        f"({(gj_plot['cluster'] == kk).sum()} wilayah)<br>" for kk in kls)
    legend = (
        "<div style='position:fixed;bottom:20px;left:20px;z-index:9999;background:white;"
        "padding:10px;border:2px solid grey;font-size:13px'>"
        f"<b>Peta clustering {variant} (k={k})</b><br>"
        "<b>Cara membaca:</b> warna sama = karakteristik polutan mirip<br>"
        + bars + "<i>Klik poligon untuk nama daerah.</i></div>")
    m.get_root().html.add_child(folium.Element(legend))
    out_html = P(f"05_clustering/peta_clustering_{variant}{suffix}.html")
    m.save(out_html)
    print(f"[{variant} k={k}] tersimpan: {out_html} ({len(gj_plot)} wilayah di peta)")
    return m


def build_interactive_map(variant):
    """Satu HTML per varian berisi SEMUA k=2..5 sebagai layer yang bisa dicentang.
    k diatur langsung di peta via LayerControl (bukan statis)."""
    import geopandas as gpd  # noqa: F811 (redundan, demi notebook-mirror)
    daftar = pd.read_csv(P("data/spasial/daftar_kecamatan.csv"))
    daftar["key"] = daftar["daerah"].map(norm)
    m = folium.Map(location=[-2.5, 118.0], zoom_start=5, tiles=None)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Esri (bawaan)").add_to(m)
    folium.TileLayer(tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
                     attr="OpenTopoMap", name="OpenTopoMap (cadangan)").add_to(m)
    for k in range(2, 6):
        Xd = pd.read_csv(P(f"data/processed/X_{variant}_204.csv")).to_numpy()
        lab = KMeans(n_clusters=k, random_state=SEED, n_init=10,
                     max_iter=300).fit_predict(Xd)
        lab_df = pd.DataFrame({
            "daerah": pd.read_csv(
                P(f"data/processed/clustering_{variant}_204.csv"))["daerah"].tolist(),
            "cluster": lab, "k": k})
        lab_df["key"] = apply_alias(lab_df["daerah"].map(norm))
        cl = lab_df.set_index("key")["cluster"].to_dict()
        gj = None
        recs = []
        for _, r in daftar.iterrows():
            fp = r["file_geojson"]
            if not isinstance(fp, str) or not fp.strip() or not os.path.exists(ROOT / fp):
                continue
            g = gpd.read_file(ROOT / fp).to_crs(4326)
            g["daerah"] = r["daerah"]
            g["cluster"] = cl.get(r["key"])
            g["k"] = k
            recs.append(g[["daerah", "cluster", "k", "geometry"]])
        gj = pd.concat(recs, ignore_index=True)
        gjp = gj.dropna(subset=["cluster"]).copy()
        gjp["cluster"] = gjp["cluster"].astype(int).astype(str)
        gjp["geometry"] = gjp.geometry.simplify(0.001, preserve_topology=True)
        kls = sorted(gjp["cluster"].unique())
        warna = {kk: PALET[i % len(PALET)] for i, kk in enumerate(kls)}
        for kk in kls:
            sub = gjp[gjp["cluster"] == kk]
            folium.GeoJson(
                sub.to_json(),
                style_function=lambda f, kk=kk, _w=dict(warna): {
                    "fillColor": _w[kk], "color": "black",
                    "weight": 0.8, "fillOpacity": 0.65},
                tooltip=folium.GeoJsonTooltip(fields=["daerah", "cluster", "k"],
                                              aliases=["Daerah", "Cluster", "k"]),
                name=f"k={k} · Cluster {kk} ({len(sub)} wilayah)",
                show=(k == 2),
            ).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    legend = (
        "<div style='position:fixed;bottom:20px;left:20px;z-index:9999;background:white;"
        "padding:10px;border:2px solid grey;font-size:13px'>"
        f"<b>Peta interaktif {variant}</b> — centang layer k=2..5 untuk atur k<br>"
        "<b>Cara membaca:</b> warna sama = karakteristik polutan mirip<br>"
        "<i>Klik poligon untuk nama daerah.</i></div>")
    m.get_root().html.add_child(folium.Element(legend))
    out_html = P(f"05_clustering/peta_clustering_{variant}_interaktif.html")
    m.save(out_html)
    print(f"[{variant}] tersimpan: {out_html} (layer k=2..5, default tampil k=2)")
    return m


if __name__ == "__main__":
    comparison_table()
    # (a) peta pemenang (nama file lama dipertahankan)
    for v in VARIANTS:
        best = json.load(open(P(f"data/processed/best_config_{v}.json")))
        lab = pd.read_csv(P(f"data/processed/labels_best_{v}.csv"))
        print(f"[{v}] pemenang: dim {best['dimensi']}, k={best['k']}, "
              f"sil={best['silhouette']:.4f}")
        build_map(lab, v, best["k"], suffix="")
    # (b) peta eksperimen k yang bisa diatur
    for v, k in [("linear", K_LIN), ("poly", K_POLY)]:
        lab, sil, sizes = cluster_at(v, k)
        print(f"[{v}] eksperimen k={k}: sil={sil:.4f} sizes={sizes}")
        build_map(lab, v, k, suffix=f"_k{k}")
    # (c) peta interaktif: k diatur langsung di peta (layer k=2..5)
    for v in VARIANTS:
        build_interactive_map(v)
    print("SELESAI")
