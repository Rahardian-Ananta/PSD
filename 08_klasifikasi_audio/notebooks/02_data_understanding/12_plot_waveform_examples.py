# Tujuan: menampilkan contoh waveform dari file asli untuk setiap kelas.
# Proses: memilih file non-duplikat pada persentil RMS rendah/tengah/tinggi, lalu memuat audio pada 16 kHz mono untuk visualisasi.
# Output: figures/waveform_examples.png dan daftar file contoh.

example_rows = []
for label_name in ["non-berisik", "berisik"]:
    candidates = manifest_raw.loc[
        (manifest_raw["label_name"] == label_name) & (~manifest_raw["is_exact_duplicate"])
    ].sort_values("rms").reset_index(drop=True)
    if len(candidates) < 3:
        candidates = manifest_raw.loc[manifest_raw["label_name"] == label_name].sort_values("rms").reset_index(drop=True)

    positions = [round(q * (len(candidates) - 1)) for q in (0.10, 0.50, 0.90)]
    positions = sorted(set(positions))
    while len(positions) < 3 and len(positions) < len(candidates):
        for candidate_position in range(len(candidates)):
            if candidate_position not in positions:
                positions.append(candidate_position)
                break
        positions = sorted(positions)

    for level, position in zip(["Rendah (P10)", "Median (P50)", "Tinggi (P90)"], positions):
        row = candidates.iloc[position]
        example_rows.append(
            {
                "label_name": label_name,
                "level": level,
                "relative_path": row["relative_path"],
                "nim": row["nim"],
                "take": int(row["take"]),
                "rms_native": float(row["rms"]),
                "peak_native": float(row["peak_abs"]),
                "samplerate_native": int(row["samplerate"]),
                "channels_native": int(row["channels"]),
            }
        )

waveform_examples = pd.DataFrame(example_rows)

fig, axes = plt.subplots(2, 3, figsize=(17, 7.2), sharex=True, sharey=True)
for row_index, label_name in enumerate(["non-berisik", "berisik"]):
    subset = waveform_examples.loc[waveform_examples["label_name"] == label_name].reset_index(drop=True)
    for column_index, row in subset.iterrows():
        ax = axes[row_index, column_index]
        path = RAW_DIR / row["relative_path"]
        signal, sr = librosa.load(path, sr=16000, mono=True)
        times = np.arange(len(signal)) / sr
        ax.plot(times, signal, color=palette[label_name], linewidth=0.35)
        ax.axhline(0, color="black", linewidth=0.4, alpha=0.5)
        ax.set_title(
            f"{label_name} | {row['level']}\n{row['relative_path']}\nRMS={row['rms_native']:.4f}",
            fontsize=9,
        )
        ax.set_xlim(0, times[-1] if len(times) else EXPECTED_DURATION_S)
        ax.set_ylim(-1.05, 1.05)
        if row_index == 1:
            ax.set_xlabel("Waktu (detik)")
        if column_index == 0:
            ax.set_ylabel("Amplitudo")

fig.suptitle("Contoh Waveform Audio Mentah (16 kHz mono untuk tampilan)", fontsize=15, fontweight="bold")
fig.tight_layout()
figure_path = FIGURE_DIR / "waveform_examples.png"
fig.savefig(figure_path, bbox_inches="tight")
plt.show()

display(waveform_examples)
waveform_examples.to_csv(ARTIFACT_DIR / "waveform_example_files.csv", index=False)
print(f"Grafik disimpan: {figure_path}")
