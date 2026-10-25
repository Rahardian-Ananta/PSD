test_features = features.loc[features["file"].isin(test_predictions["file"])]
demo_picks = pd.concat(
    [
        test_features.loc[test_features["label"] == 0].sort_values("file").head(1),
        test_features.loc[test_features["label"] == 1].sort_values("file").head(1),
    ]
).sort_values("label")

manifest_by_file = transformation_manifest.set_index("file")
demo_rows = []

for row in demo_picks.itertuples():
    mp3_path = DATA_MP3_DIR / manifest_by_file.at[row.file, "mp3_relative_path"]
    result = predict_audio(mp3_path)
    demo_rows.append(
        {
            "skenario": "demo_utama",
            "file": mp3_path.name,
            "path": str(mp3_path),
            "kelas_asli": LABEL_NAME_MAP[int(row.label)],
            "prediksi": result["label_name"],
            "proba_berisik": result["proba_berisik"],
            "cocok": bool(result["label"] == int(row.label)),
            "duration_action": result["duration_action"],
            "durasi_asli_detik": result["original_duration_16k_s"],
            "peak_sebelum_normalisasi": result["peak_before_norm"],
        }
    )

base_row = demo_picks.iloc[0]
other_row = demo_picks.iloc[1]
base_path = DATA_FINAL_DIR / manifest_by_file.at[base_row["file"], "final_relative_path"]
other_path = DATA_FINAL_DIR / manifest_by_file.at[other_row["file"], "final_relative_path"]
base_y, _ = sf.read(base_path, dtype="float32")
other_y, _ = sf.read(other_path, dtype="float32")

short_path = DEMO_AUDIO_DIR / "demo_10_detik.wav"
long_path = DEMO_AUDIO_DIR / "demo_60_detik.wav"
sf.write(short_path, base_y[: int(10 * SR)], SR, subtype="PCM_16")
sf.write(long_path, np.concatenate([base_y, other_y]), SR, subtype="PCM_16")

for scenario, temp_path, reference_label, expected_action in [
    ("cabang_pad_10_detik", short_path, int(base_row["label"]), "pad"),
    ("cabang_crop_60_detik", long_path, int(base_row["label"]), "crop"),
]:
    result = predict_audio(temp_path)
    assert result["duration_action"] == expected_action, (
        f"Aksi durasi {scenario} = {result['duration_action']}, bukan {expected_action}."
    )
    demo_rows.append(
        {
            "skenario": scenario,
            "file": temp_path.name,
            "path": str(temp_path),
            "kelas_asli": LABEL_NAME_MAP[reference_label],
            "prediksi": result["label_name"],
            "proba_berisik": result["proba_berisik"],
            "cocok": bool(result["label"] == reference_label),
            "duration_action": result["duration_action"],
            "durasi_asli_detik": result["original_duration_16k_s"],
            "peak_sebelum_normalisasi": result["peak_before_norm"],
        }
    )

demo_results = pd.DataFrame(demo_rows)
assert len(demo_results) == 4
assert set(demo_results.loc[demo_results["skenario"] == "demo_utama", "kelas_asli"]) == set(
    LABEL_ORDER
)
demo_results.to_csv(DEMO_RESULTS_PATH, index=False)

display(demo_results)
main_demos = demo_results.loc[demo_results["skenario"] == "demo_utama"]
for row in main_demos.itertuples():
    print(
        f"{row.file}: asli {row.kelas_asli} -> prediksi {row.prediksi} "
        f"(p berisik {row.proba_berisik:.4f}), {'cocok' if row.cocok else 'SALAH'}"
    )
print(
    "Cabang durasi teruji: "
    + ", ".join(
        f"{row.skenario} ({row.duration_action}, {row.durasi_asli_detik:.1f} detik)"
        for row in demo_results.loc[demo_results["skenario"] != "demo_utama"].itertuples()
    )
)
