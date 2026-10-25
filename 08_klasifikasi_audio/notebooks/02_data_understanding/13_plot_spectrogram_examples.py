# Tujuan: menampilkan spektrogram contoh audio asli untuk setiap kelas.
# Proses: memakai file contoh yang sama dengan waveform, menghitung STFT 16 kHz, dan menampilkan spektrum daya dalam dB.
# Output: figures/spectrogram_examples.png.

fig, axes = plt.subplots(2, 3, figsize=(17, 7.2), sharex=True, sharey=True)
last_mesh = None
for row_index, label_name in enumerate(["non-berisik", "berisik"]):
    subset = waveform_examples.loc[waveform_examples["label_name"] == label_name].reset_index(drop=True)
    for column_index, row in subset.iterrows():
        ax = axes[row_index, column_index]
        path = RAW_DIR / row["relative_path"]
        signal, sr = librosa.load(path, sr=16000, mono=True)
        stft = librosa.stft(
            signal,
            n_fft=512,
            hop_length=160,
            win_length=400,
            window="hann",
            center=True,
        )
        power = np.abs(stft) ** 2
        power_db = librosa.power_to_db(power, ref=np.max)
        times = librosa.times_like(power, sr=sr, hop_length=160)
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=512)
        last_mesh = ax.pcolormesh(
            times,
            frequencies,
            power_db,
            shading="auto",
            cmap="magma",
            vmin=-80,
            vmax=0,
        )
        ax.set_ylim(0, 8000)
        ax.set_title(
            f"{label_name} | {row['level']}\n{row['relative_path']}\nRMS={row['rms_native']:.4f}",
            fontsize=9,
        )
        if row_index == 1:
            ax.set_xlabel("Waktu (detik)")
        if column_index == 0:
            ax.set_ylabel("Frekuensi (Hz)")

fig.suptitle("Contoh Spektrogram Audio Mentah (16 kHz mono, STFT 25 ms / hop 10 ms)", fontsize=15, fontweight="bold")
fig.tight_layout()
if last_mesh is not None:
    colorbar = fig.colorbar(last_mesh, ax=axes.ravel().tolist(), shrink=0.65, pad=0.02)
    colorbar.set_label("Daya relatif (dB)")
figure_path = FIGURE_DIR / "spectrogram_examples.png"
fig.savefig(figure_path, bbox_inches="tight")
plt.show()

print(f"Grafik disimpan: {figure_path}")
display(waveform_examples[["label_name", "level", "relative_path", "rms_native"]])
