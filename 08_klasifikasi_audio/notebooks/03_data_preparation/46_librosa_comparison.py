features_by_file = features.set_index("file")
comparison_pairs = {
    "spectral_centroid_mean": "spectral_centroid",
    "spectral_bandwidth_mean": "spectral_bandwidth",
    "spectral_rolloff_mean": "spectral_rolloff",
    "spectral_flatness_mean": "spectral_flatness",
    "zcr_mean": "zero_crossing_rate",
}
comparison_notes = {
    "spectral_centroid_mean": "manual=P, librosa=magnitudo",
    "spectral_bandwidth_mean": "manual=P, librosa=magnitudo",
    "spectral_rolloff_mean": "manual=P, librosa=magnitudo",
    "spectral_flatness_mean": "manual=P, librosa=magnitudo",
    "zcr_mean": "konvensi zero-crossing dapat berbeda di tepi frame",
}

comparison_rows = []
for row in transformation_manifest.itertuples():
    y, sr = sf.read(DATA_FINAL_DIR / row.final_relative_path, dtype="float32")
    frames = frame_signal(y).astype(np.float64)
    P = np.abs(np.fft.rfft(frames * hann_window[None, :], n=N_FFT, axis=1)) ** 2
    magnitude = np.sqrt(P).T

    librosa_values = {
        "spectral_centroid_mean": float(
            np.mean(librosa.feature.spectral_centroid(S=magnitude, sr=SR, freq=FREQS))
        ),
        "spectral_bandwidth_mean": float(
            np.mean(librosa.feature.spectral_bandwidth(S=magnitude, sr=SR, freq=FREQS))
        ),
        "spectral_rolloff_mean": float(
            np.mean(
                librosa.feature.spectral_rolloff(
                    S=magnitude,
                    sr=SR,
                    freq=FREQS,
                    roll_percent=ROLLOFF_PERCENT,
                )
            )
        ),
        "spectral_flatness_mean": float(
            np.mean(librosa.feature.spectral_flatness(S=magnitude))
        ),
        "zcr_mean": float(
            np.mean(
                librosa.feature.zero_crossing_rate(
                    y,
                    frame_length=FRAME_LENGTH,
                    hop_length=HOP_LENGTH,
                    center=False,
                )
            )
        ),
    }

    manual_values = {
        feature: float(features_by_file.loc[row.file, feature])
        for feature in comparison_pairs
    }
    for feature, method_name in comparison_pairs.items():
        comparison_rows.append(
            {
                "file": row.file,
                "feature": feature,
                "librosa_function": method_name,
                "manual": manual_values[feature],
                "librosa": librosa_values[feature],
                "difference": manual_values[feature] - librosa_values[feature],
            }
        )

comparison_detail = pd.DataFrame(comparison_rows)
comparison_detail["abs_difference"] = comparison_detail["difference"].abs()

summary_rows = []
for feature, group in comparison_detail.groupby("feature", sort=False):
    manual = group["manual"].to_numpy()
    library = group["librosa"].to_numpy()
    if np.std(manual) > 0 and np.std(library) > 0:
        correlation = float(np.corrcoef(manual, library)[0, 1])
    else:
        correlation = float("nan")
    summary_rows.append(
        {
            "feature": feature,
            "manual_mean": float(np.mean(manual)),
            "librosa_mean": float(np.mean(library)),
            "mean_abs_difference": float(np.mean(group["abs_difference"])),
            "max_abs_difference": float(np.max(group["abs_difference"])),
            "pearson_r": correlation,
            "note": comparison_notes[feature],
        }
    )
comparison_summary = pd.DataFrame(summary_rows)

display(comparison_summary)
print(f"Selisih maksimum daya rFFT vs FFT penuh: {fft_rfft_max_abs_diff:.3e}")

comparison_detail.to_csv(ARTIFACT_DIR / "librosa_comparison_detail.csv", index=False)
comparison_summary.to_csv(ARTIFACT_DIR / "librosa_comparison_summary.csv", index=False)
with open(ARTIFACT_DIR / "librosa_comparison.json", "w", encoding="utf-8") as handle:
    json.dump(
        {
            "fft_rfft_max_abs_diff": fft_rfft_max_abs_diff,
            "summary": comparison_summary.to_dict(orient="records"),
        },
        handle,
        ensure_ascii=False,
        indent=2,
    )
