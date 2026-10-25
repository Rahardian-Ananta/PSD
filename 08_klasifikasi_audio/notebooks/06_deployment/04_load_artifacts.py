stage3_validation = json.loads(STAGE3_VALIDATION_PATH.read_text(encoding="utf-8"))
stage4_validation = json.loads(STAGE4_VALIDATION_PATH.read_text(encoding="utf-8"))
stage5_validation = json.loads(STAGE5_VALIDATION_PATH.read_text(encoding="utf-8"))

for stage_name, summary in {
    "03": stage3_validation,
    "04": stage4_validation,
    "05": stage5_validation,
}.items():
    assert summary["status"] == "PASS", f"Validasi Tahap {stage_name} bukan PASS."
    assert summary["checks_passed"] == summary["checks_total"], (
        f"Ada pemeriksaan gagal pada Tahap {stage_name}."
    )
assert stage4_validation["holdout_tested_in_stage_04"] is False, (
    "Hold-out sudah pernah diuji di Tahap 04."
)

assert MODEL_PATH.is_file(), "best_model.joblib tidak ditemukan."
model_config = json.loads(MODEL_CONFIG_PATH.read_text(encoding="utf-8"))
saved_model = joblib.load(MODEL_PATH)

assert list(saved_model.named_steps) == ["scaler", "select", "clf"], (
    f"Struktur pipeline berubah: {list(saved_model.named_steps)}"
)
assert model_config["model_name"] == "Logistic Regression"
assert model_config["feature_columns"] == FEATURE_COLUMNS, "Daftar fitur config tidak cocok."
assert int(saved_model.n_features_in_) == len(FEATURE_COLUMNS)

for param_key, param_value in model_config["best_params"].items():
    assert saved_model.get_params()[param_key] == param_value, f"Parameter berubah: {param_key}"

selected_from_model = list(
    saved_model.named_steps["select"].get_feature_names_out(FEATURE_COLUMNS)
)
assert selected_from_model == model_config["selected_features_final"], (
    "Fitur terpilih pada pipeline berubah."
)
assert int(saved_model.named_steps["select"].k) == int(model_config["best_params"]["select__k"])
assert list(saved_model.classes_) == [0, 1], "Urutan kelas model berubah."

contract = json.loads(PREPROCESSING_CONTRACT_PATH.read_text(encoding="utf-8"))
assert contract["sample_rate"] == SR, "Sample rate kontrak berubah."
assert contract["target_samples"] == TARGET_SAMPLES, "Jumlah sampel kontrak berubah."
assert contract["frame_length"] == FRAME_LENGTH, "Frame length kontrak berubah."
assert contract["hop_length"] == HOP_LENGTH, "Hop length kontrak berubah."
assert contract["n_fft"] == N_FFT, "n_fft kontrak berubah."
assert contract["rolloff_percent"] == ROLLOFF_PERCENT, "Rolloff kontrak berubah."
assert float(contract["flatness_epsilon"]) == float(EPS), "Epsilon flatness kontrak berubah."

model_file_sha256 = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()
model_fingerprint = hashlib.sha256(pickle.dumps(saved_model)).hexdigest()
assert len(model_file_sha256) == 64 and len(model_fingerprint) == 64

features = pd.read_csv(FEATURES_PATH)
features["label"] = features["label"].astype(int)
features["take"] = features["take"].astype(int)
assert len(features) == 176, f"features.csv berisi {len(features)} baris."
assert np.isfinite(features[FEATURE_COLUMNS].to_numpy(dtype=float)).all(), "Fitur mengandung NaN/Inf."

holdout_file_split = pd.read_csv(HOLDOUT_FILE_PATH)
assert len(holdout_file_split) == 176 and set(holdout_file_split["split"]) == {"train", "test"}

transformation_manifest = pd.read_csv(TRANSFORMATION_MANIFEST_PATH)
assert len(transformation_manifest) == 176
assert transformation_manifest["file"].is_unique, "Manifest transformasi memiliki file ganda."
assert set(transformation_manifest["file"]) == set(features["file"]), (
    "Manifest transformasi dan features.csv tidak seisi."
)

test_predictions = pd.read_csv(PREDICTIONS_PATH)
assert len(test_predictions) == 40, "test_predictions.csv tidak berisi 40 baris."
assert set(test_predictions["split"]) == {"test"}

metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
evaluation_summary = json.loads(EVALUATION_SUMMARY_PATH.read_text(encoding="utf-8"))
stage3_summary = json.loads(STAGE3_SUMMARY_PATH.read_text(encoding="utf-8"))
assert int(metrics["n_files_test"]) == 40

nims_test = sorted(model_config["holdout"]["nims_test"])
nims_train = sorted(model_config["holdout"]["nims_train"])
assert len(nims_test) == 7 and len(nims_train) == 27

X_test_direct = features.set_index("file").loc[test_predictions["file"], FEATURE_COLUMNS]
proba_direct = saved_model.predict_proba(X_test_direct.to_numpy(dtype=float))[:, 1]
model_identity_max_diff = float(np.max(np.abs(proba_direct - test_predictions["proba_berisik"])))
assert model_identity_max_diff < MODEL_IDENTITY_TOL, (
    f"Probabilitas model berbeda dari Tahap 05: {model_identity_max_diff}"
)
pred_direct = (proba_direct >= TEST_THRESHOLD).astype(int)
assert int((pred_direct != test_predictions["pred_label"].to_numpy()).sum()) == 0

gate_summary = pd.DataFrame(
    {
        "pemeriksaan": [
            "validasi Tahap 03 / 04 / 05",
            "model",
            "pipeline",
            "parameter terbaik",
            "fitur input",
            "fitur terpilih",
            "kontrak prapemrosesan",
            "selisih probabilitas vs Tahap 05",
            "sidik jari file model (sha256)",
            "NIM test",
            "file uji",
        ],
        "nilai": [
            "PASS / PASS / PASS",
            model_config["model_name"],
            " -> ".join(list(saved_model.named_steps)),
            str(model_config["best_params"]),
            len(FEATURE_COLUMNS),
            len(selected_from_model),
            f"{SR} Hz / {TARGET_SAMPLES} sampel / frame {FRAME_LENGTH} / hop {HOP_LENGTH}",
            f"{model_identity_max_diff:.3e}",
            model_file_sha256[:16],
            ", ".join(nims_test),
            len(test_predictions),
        ],
    }
)
display(gate_summary)
print("Pintu masuk Tahap 06: LULUS — model identik dengan yang dievaluasi Tahap 05.")
