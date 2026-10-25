example_S = np.fft.rfft(example_windowed, n=N_FFT, axis=1)
example_P = np.abs(example_S) ** 2
FREQS = np.fft.rfftfreq(N_FFT, d=1 / SR)

S_full_fft = np.fft.fft(example_windowed, n=N_FFT, axis=1)
P_full_fft = np.abs(S_full_fft[:, : N_FFT // 2 + 1]) ** 2
fft_rfft_max_abs_diff = float(np.max(np.abs(P_full_fft - example_P)))

if example_P.shape != (example_frames.shape[0], N_FFT // 2 + 1):
    raise ValueError("Bentuk spektrum daya tidak sesuai.")
if fft_rfft_max_abs_diff > 1e-6:
    raise ValueError("rFFT dan FFT penuh berbeda terlalu besar.")

fig, ax = plt.subplots(figsize=(10, 3.8))
ax.imshow(
    10 * np.log10(example_P.T + EPS),
    origin="lower",
    aspect="auto",
    extent=[0, TARGET_DURATION_S, 0, SR / 2],
    cmap="magma",
)
ax.set_title(f"Spektrum daya contoh: {example_row['file']}")
ax.set_xlabel("Waktu (detik)")
ax.set_ylabel("Frekuensi (Hz)")
fig.tight_layout()
fig.savefig(FIGURE_DIR / "power_spectrum_example.png", bbox_inches="tight")
plt.show()

display(
    pd.DataFrame(
        {
            "besaran": [
                "bentuk frame",
                "bentuk STFT manual",
                "bentuk FFT penuh (pemeriksaan)",
                "jumlah bin frekuensi",
                "resolusi frekuensi (Hz)",
                "selisih maksimum daya rFFT vs FFT penuh",
            ],
            "nilai": [
                str(example_windowed.shape),
                str(example_S.shape),
                str(S_full_fft.shape),
                len(FREQS),
                FREQS[1] - FREQS[0],
                fft_rfft_max_abs_diff,
            ],
        }
    )
)
