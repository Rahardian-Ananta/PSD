# Tujuan: menampilkan distribusi durasi hasil decode dan membandingkannya antar kelas.
# Proses: membuat histogram durasi dan boxplot durasi per label dari manifest aktual.
# Output: figures/duration_distribution.png dan ringkasan durasi.

fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))

ax = axes[0]
sns.histplot(
    data=manifest_raw,
    x="duration_decoded_s",
    bins=20,
    color="#7570B3",
    edgecolor="white",
    ax=ax,
)
ax.set_title("Histogram durasi hasil decode")
ax.set_xlabel("Durasi (detik)")
ax.set_ylabel("Jumlah file")

ax = axes[1]
sns.boxplot(
    data=manifest_raw,
    x="label_name",
    y="duration_decoded_s",
    hue="label_name",
    palette=palette,
    legend=False,
    width=0.45,
    ax=ax,
)
sns.stripplot(
    data=manifest_raw,
    x="label_name",
    y="duration_decoded_s",
    color="black",
    size=2,
    alpha=0.35,
    ax=ax,
)
ax.set_title("Durasi per kelas")
ax.set_xlabel("Kelas")
ax.set_ylabel("Durasi (detik)")

fig.suptitle("Distribusi Durasi Audio Mentah", fontsize=15, fontweight="bold")
fig.tight_layout()
figure_path = FIGURE_DIR / "duration_distribution.png"
fig.savefig(figure_path, bbox_inches="tight")
plt.show()

duration_stats = manifest_raw["duration_decoded_s"].describe()
print(f"Grafik disimpan: {figure_path}")
print(f"Durasi minimum: {duration_stats['min']:.3f} detik")
print(f"Durasi maksimum: {duration_stats['max']:.3f} detik")
print(f"File tepat 30 detik: {int(manifest_raw['duration_status'].eq('tepat_30_detik').sum())} dari {len(manifest_raw)}")
print(f"Durasi di luar toleransi: {int(manifest_raw['duration_status'].ne('tepat_30_detik').sum())}")
