hann_window = 0.5 - 0.5 * np.cos(
    2 * np.pi * np.arange(FRAME_LENGTH) / (FRAME_LENGTH - 1)
)
if not np.allclose(hann_window, np.hanning(FRAME_LENGTH), atol=1e-15):
    raise ValueError("Window Hann tidak sesuai definisi simetris.")
if not (hann_window[0] == 0 and hann_window[-1] == 0):
    raise ValueError("Window Hann harus nol di kedua ujung.")

fig, ax = plt.subplots(figsize=(8, 3.2))
ax.plot(np.arange(FRAME_LENGTH) / SR * 1000, hann_window, color="#2a6f97")
ax.set_title("Window Hann simetris, L = 400 (25 ms)")
ax.set_xlabel("Waktu dalam frame (ms)")
ax.set_ylabel("Bobot")
ax.set_ylim(-0.05, 1.05)
fig.tight_layout()
fig.savefig(FIGURE_DIR / "hann_window.png", bbox_inches="tight")
plt.show()

display(
    pd.DataFrame(
        {
            "besaran": [
                "panjang window",
                "nilai awal",
                "nilai akhir",
                "nilai maksimum",
                "simetris",
                "identik dengan np.hanning",
            ],
            "nilai": [
                FRAME_LENGTH,
                hann_window[0],
                hann_window[-1],
                hann_window.max(),
                np.allclose(hann_window, hann_window[::-1]),
                np.allclose(hann_window, np.hanning(FRAME_LENGTH)),
            ],
        }
    )
)
