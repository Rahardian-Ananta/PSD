# Tujuan: menampilkan keragaman format teknis audio mentah.
# Proses: membuat grafik sample rate, jumlah channel, dan estimasi bitrate per kelas.
# Output: figures/format_characteristics.png dan ringkasan format.

fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))

sr_pivot = format_summary.pivot_table(
    index="samplerate", columns="label_name", values="n_files", aggfunc="sum", fill_value=0
)
sr_pivot.plot(kind="bar", ax=axes[0], color=[palette.get(c, "#999999") for c in sr_pivot.columns])
axes[0].set_title("Sample rate per kelas")
axes[0].set_xlabel("Sample rate (Hz)")
axes[0].set_ylabel("Jumlah file")
axes[0].tick_params(axis="x", rotation=0)

ch_pivot = format_summary.pivot_table(
    index="channels", columns="label_name", values="n_files", aggfunc="sum", fill_value=0
)
ch_pivot.plot(kind="bar", ax=axes[1], color=[palette.get(c, "#999999") for c in ch_pivot.columns])
axes[1].set_title("Jumlah channel per kelas")
axes[1].set_xlabel("Jumlah channel")
axes[1].set_ylabel("Jumlah file")
axes[1].tick_params(axis="x", rotation=0)

sns.boxplot(
    data=manifest_raw,
    x="label_name",
    y="bitrate_kbps_estimate",
    hue="label_name",
    palette=palette,
    legend=False,
    width=0.45,
    ax=axes[2],
)
sns.stripplot(
    data=manifest_raw,
    x="label_name",
    y="bitrate_kbps_estimate",
    color="black",
    size=2,
    alpha=0.3,
    ax=axes[2],
)
axes[2].set_title("Estimasi bitrate per kelas")
axes[2].set_xlabel("Kelas")
axes[2].set_ylabel("Estimasi bitrate (kbps)")

fig.suptitle("Karakteristik Format Audio Mentah", fontsize=15, fontweight="bold")
fig.tight_layout()
figure_path = FIGURE_DIR / "format_characteristics.png"
fig.savefig(figure_path, bbox_inches="tight")
plt.show()

print(f"Grafik disimpan: {figure_path}")
print("Format file:", manifest_raw["format"].value_counts().to_dict())
print("Sample rate:", manifest_raw["samplerate"].value_counts().sort_index().to_dict())
print("Channel:", manifest_raw["channels"].value_counts().sort_index().to_dict())
