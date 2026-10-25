def predict_audio(path, model=None, threshold=TEST_THRESHOLD):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"File audio tidak ditemukan: {path}")

    active_model = saved_model if model is None else model

    y, loaded_sr = librosa.load(path, sr=SR, mono=True)
    if loaded_sr != SR:
        raise ValueError(f"Sample rate hasil dekode {loaded_sr} bukan {SR}.")

    y_fit, fit_meta = fit_duration_to_target(y)
    y_norm, peak_meta = peak_normalize(y_fit)
    feature_values = extract_features(y_norm)

    frame = pd.DataFrame([[feature_values[column] for column in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
    proba = active_model.predict_proba(frame.to_numpy(dtype=float))[0]
    proba_map = {int(cls): float(value) for cls, value in zip(active_model.classes_, proba)}
    proba_berisik = proba_map[1]
    pred_label = int(proba_berisik >= threshold)

    return {
        "path": str(path),
        "file": path.name,
        "label": pred_label,
        "label_name": LABEL_NAME_MAP[pred_label],
        "proba_non_berisik": proba_map[0],
        "proba_berisik": proba_berisik,
        "proba_diprediksi": max(proba_map.values()),
        "threshold": float(threshold),
        "duration_action": fit_meta["action"],
        "original_samples_16k": fit_meta["original_samples_16k"],
        "original_duration_16k_s": fit_meta["original_duration_16k_s"],
        "peak_before_norm": peak_meta["peak_before"],
        "features": feature_values,
    }


smoke_path = DATA_FINAL_DIR / transformation_manifest.sort_values("file").iloc[0]["final_relative_path"]
smoke_result = predict_audio(smoke_path)
smoke_view = pd.DataFrame(
    {
        "kunci": [key for key in smoke_result if key != "features"],
        "nilai": [value for key, value in smoke_result.items() if key != "features"],
    }
)
display(smoke_view)
print(f"predict_audio siap: {smoke_path.name} -> {smoke_result['label_name']} (p={smoke_result['proba_berisik']:.4f})")
