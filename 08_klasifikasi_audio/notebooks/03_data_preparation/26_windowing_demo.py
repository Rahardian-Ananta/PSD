example_windowed = example_frames * hann_window[None, :]

if example_windowed.shape != example_frames.shape:
    raise ValueError("Windowing tidak boleh mengubah bentuk frame.")
if not np.allclose(example_windowed[:, [0, -1]], 0):
    raise ValueError("Sampel tepi frame setelah windowing harus nol.")

fig, axes = plt.subplots(2, 1, figsize=(9, 4.8), sharex=True)
axes[0].plot(example_frames[0], color="#6c757d")
axes[0].set_title("Frame 0 sebelum windowing")
axes[0].set_ylabel("Amplitudo")
axes[1].plot(example_windowed[0], color="#1d6b3f")
axes[1].set_title("Frame 0 setelah windowing Hann")
axes[1].set_xlabel("Indeks sampel dalam frame")
axes[1].set_ylabel("Amplitudo")
fig.tight_layout()
fig.savefig(FIGURE_DIR / "windowing_example.png", bbox_inches="tight")
plt.show()

display(
    pd.DataFrame(
        {
            "besaran": [
                "bentuk frame sebelum",
                "bentuk frame sesudah",
                "sampel awal frame 0",
                "sampel akhir frame 0",
                "energi frame 0 sebelum",
                "energi frame 0 sesudah",
            ],
            "nilai": [
                str(example_frames.shape),
                str(example_windowed.shape),
                float(example_windowed[0, 0]),
                float(example_windowed[0, -1]),
                float(np.sum(example_frames[0] ** 2)),
                float(np.sum(example_windowed[0] ** 2)),
            ],
        }
    )
)
