# Tujuan: memvisualisasikan distribusi file, NIM, dan kelengkapan file per NIM.
# Proses: membuat tiga panel grafik dari tabel ringkasan aktual.
# Output: figures/class_distribution.png.

palette = {"berisik": "#D95F02", "non-berisik": "#1B9E77"}

fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

ax = axes[0]
bars = ax.bar(class_summary["label_name"], class_summary["n_files"], color=[palette[x] for x in class_summary["label_name"]])
ax.set_title("Jumlah file per kelas")
ax.set_xlabel("Kelas")
ax.set_ylabel("Jumlah file")
ax.bar_label(bars, padding=3)
ax.margins(y=0.15)

ax = axes[1]
bars = ax.bar(class_summary["label_name"], class_summary["n_nim"], color=[palette[x] for x in class_summary["label_name"]])
ax.set_title("Jumlah NIM yang memiliki kelas")
ax.set_xlabel("Kelas")
ax.set_ylabel("Jumlah NIM")
ax.bar_label(bars, padding=3)
ax.margins(y=0.15)

ax = axes[2]
files_per_nim_counts = nim_summary["n_files"].value_counts().sort_index()
bars = ax.bar(files_per_nim_counts.index.astype(str), files_per_nim_counts.values, color="#7570B3")
ax.set_title("Distribusi jumlah file per NIM")
ax.set_xlabel("Jumlah file dalam satu NIM")
ax.set_ylabel("Jumlah NIM")
ax.bar_label(bars, padding=3)
ax.margins(y=0.15)

fig.suptitle("Distribusi Dataset Mentah", fontsize=15, fontweight="bold")
fig.tight_layout()
figure_path = FIGURE_DIR / "class_distribution.png"
fig.savefig(figure_path, bbox_inches="tight")
plt.show()

print(f"Grafik disimpan: {figure_path}")
print(f"File per kelas: {dict(zip(class_summary['label_name'], class_summary['n_files']))}")
print(f"NIM per kelas: {dict(zip(class_summary['label_name'], class_summary['n_nim']))}")
print(f"NIM dengan 6 file: {int(nim_summary['lengkap_6_file'].sum())} dari {len(nim_summary)}")
