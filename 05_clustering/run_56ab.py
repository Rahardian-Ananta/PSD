"""Eksperimen gabungan 204 fitur — varian LINEAR vs POLYNOMIAL (tugas PSD 5.6a/5.6b).
Sumber: data/ekstraksi_fitur_linear.csv & data/ekstraksi_fitur_polynomial.csv
(36 baris x 204 fitur = 68 NO2 + 68 SO2 + 68 CO, sudah gabungan 3 polutan).
Ladder reduksi (tugas: 204 -> 74 -> 37) via peringkat variansi + StandardScaler.
Tiap tahap x k=2..10 KMeans (seed 42) dinilai silhouette; pemenang = silhouette
tertinggi dengan min_size>=2 (tanpa singleton). Dijalankan via:
  python 05_clustering/run_56ab.py
Keluaran: data/processed/*_{linear,poly}.*, data/images/eksperimen204_{linear,poly}/*
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

SEED = 42
LADDER = [204, 74, 37]  # tugas: 204 (penuh) -> 74 -> 37. "203" di soal = typo 204=68x3.
SRC = {
    "linear": "data/ekstraksi_fitur_linear.csv",
    "poly": "data/ekstraksi_fitur_polynomial.csv",
}
OUT = "data/processed"


def norm(s):
    return " ".join(str(s).strip().lower().split())


def run_variant(name, src):
    img = f"data/images/eksperimen204_{name}"
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(img, exist_ok=True)
    df = pd.read_csv(src)
    feats_all = [c for c in df.columns if c not in ("id", "nama", "daerah")]
    assert len(feats_all) == 204, f"{name}: {len(feats_all)} fitur, bukan 204!"
    pref = pd.Series([c.split("_")[0] for c in feats_all]).value_counts().to_dict()
    assert pref == {"no2": 68, "so2": 68, "co": 68}, f"{name}: komposisi {pref}"
    df["key"] = df["daerah"].map(norm)
    dup = df[df.duplicated("key", keep=False)].sort_values("key")
    g = df.groupby("key")
    agg = g[feats_all].mean()  # observasi ganda (Kamal, Kwanyar) -> mean
    agg.insert(0, "daerah", g["daerah"].first())
    agg = agg.reset_index(drop=True)
    print(f"[{name}] {src}: {len(df)} baris -> {len(agg)} daerah unik "
          f"(duplikat diagregasi mean: {sorted(dup['daerah'].unique().tolist())}), "
          f"missing={int(agg[feats_all].isna().sum().sum())}")
    agg[["daerah"] + feats_all].to_csv(f"{OUT}/clustering_{name}_204.csv", index=False)

    Xraw = agg[feats_all].to_numpy()
    var_rank = np.argsort(Xraw.var(axis=0))[::-1]
    total_var = float(Xraw.var(axis=0).sum())
    lad_rows = []
    for d in LADDER:
        keep = sorted(var_rank[:d].tolist())
        cols = [feats_all[i] for i in keep]
        Xs = StandardScaler().fit_transform(agg[cols].to_numpy())
        pd.DataFrame(Xs, columns=cols).to_csv(f"{OUT}/X_{name}_{d}.csv", index=False)
        retained = float(Xraw[:, var_rank[:d]].var(axis=0).sum() / total_var)
        lad_rows.append({"dimensi": d, "n_fitur": len(cols), "retained_var": round(retained, 4)})
    lad_df = pd.DataFrame(lad_rows)
    lad_df.to_csv(f"{OUT}/ladder_{name}.csv", index=False)
    print(f"[{name}] ladder:\n{lad_df.to_string(index=False)}")

    res = []
    for d in LADDER:
        Xd = pd.read_csv(f"{OUT}/X_{name}_{d}.csv").to_numpy()
        for k in range(2, 11):
            km = KMeans(n_clusters=k, random_state=SEED, n_init=10, max_iter=300)
            lab = km.fit_predict(Xd)
            sil = float(silhouette_score(Xd, lab))
            sizes = pd.Series(lab).value_counts().sort_index()
            res.append({"dimensi": d, "k": k, "silhouette": sil,
                        "inertia": float(km.inertia_), "seed": SEED,
                        "min_size": int(sizes.min()),
                        "ukuran_cluster": ";".join(map(str, sizes.tolist()))})
    grid = pd.DataFrame(res)
    grid.to_csv(f"{OUT}/clustering_grid_{name}.csv", index=False)
    valid = grid[grid["min_size"] >= 2].sort_values("silhouette", ascending=False)
    win = valid.iloc[0]
    best = {"varian": name, "dimensi": int(win["dimensi"]), "k": int(win["k"]),
            "silhouette": float(win["silhouette"]), "inertia": float(win["inertia"]),
            "seed": SEED, "ukuran_cluster": str(win["ukuran_cluster"]),
            "aturan": "silhouette tertinggi dengan min_size>=2 (tanpa singleton)"}
    with open(f"{OUT}/best_config_{name}.json", "w") as f:
        json.dump(best, f, indent=2)
    Xd = pd.read_csv(f"{OUT}/X_{name}_{best['dimensi']}.csv").to_numpy()
    lab = KMeans(n_clusters=best["k"], random_state=SEED, n_init=10,
                 max_iter=300).fit_predict(Xd)
    pd.DataFrame({"daerah": agg["daerah"].tolist(), "cluster": lab}).to_csv(
        f"{OUT}/labels_best_{name}.csv", index=False)
    print(f"[{name}] grid top5 mentah:\n"
          f"{grid.sort_values('silhouette', ascending=False).head(5).to_string(index=False)}")
    print(f"[{name}] PEMENANG valid: {best}")

    # --- gambar: heatmap silhouette + elbow ---
    piv = grid.pivot(index="dimensi", columns="k", values="silhouette").loc[LADDER]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    im = axes[0].imshow(piv.to_numpy(), aspect="auto", cmap="YlGn")
    axes[0].set_xticks(range(len(piv.columns)))
    axes[0].set_xticklabels(piv.columns)
    axes[0].set_yticks(range(len(piv.index)))
    axes[0].set_yticklabels(piv.index)
    axes[0].set_xlabel("k")
    axes[0].set_ylabel("dimensi tahap")
    axes[0].set_title(f"Heatmap silhouette ({name})")
    fig.colorbar(im, ax=axes[0], label="silhouette")
    for d in LADDER:
        gg = grid[grid["dimensi"] == d].sort_values("k")
        axes[1].plot(gg["k"], gg["inertia"], marker="o", ms=3, label=f"dim {d}")
    axes[1].set_title(f"Elbow inertia ({name})")
    axes[1].set_xlabel("k")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(f"{img}/fig_heatmap_elbow.png", dpi=100)
    plt.close(fig)

    # --- gambar: silhouette per tahap (wajib tugas: bandingkan tiap dimensi) ---
    fig, ax = plt.subplots(figsize=(8, 4))
    for d in LADDER:
        gg = grid[grid["dimensi"] == d].sort_values("k")
        ax.plot(gg["k"], gg["silhouette"], marker="o", ms=4, label=f"dim {d}")
    ax.set_xlabel("k (jumlah cluster)")
    ax.set_ylabel("silhouette")
    ax.set_title(f"Silhouette vs k per dimensi ({name}) — titik = hasil clustering tiap dimensi")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{img}/fig_silhouette_per_dim.png", dpi=100)
    plt.close(fig)
    return best


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
              if os.path.basename(os.getcwd()) == "05_clustering" else os.getcwd())
    out = {}
    for name, src in SRC.items():
        out[name] = run_variant(name, src)
    print("SELESAI:", json.dumps(out, indent=2))
