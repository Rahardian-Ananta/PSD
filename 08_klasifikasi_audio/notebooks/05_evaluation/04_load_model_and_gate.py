stage4_validation = json.loads(STAGE4_VALIDATION_PATH.read_text(encoding="utf-8"))
assert stage4_validation["status"] == "PASS", "Validasi Tahap 04 berstatus bukan PASS."
assert (
    stage4_validation["checks_passed"] == stage4_validation["checks_total"]
), "Terdapat pemeriksaan Tahap 04 yang gagal."
assert stage4_validation["holdout_tested_in_stage_04"] is False, (
    "Hold-out sudah pernah diuji pada Tahap 04; evaluasi menjadi tidak independen."
)

assert MODEL_PATH.is_file(), "best_model.joblib tidak ditemukan."
model_config = json.loads(MODEL_CONFIG_PATH.read_text(encoding="utf-8"))
saved_model = joblib.load(MODEL_PATH)

assert list(saved_model.named_steps) == ["scaler", "select", "clf"], (
    f"Struktur pipeline berubah: {list(saved_model.named_steps)}"
)
assert model_config["model_name"] == "Logistic Regression"
assert model_config["feature_columns"] == FEATURE_COLUMNS, "Daftar fitur config tidak cocok."
assert int(model_config["train_rows"]) == 136, "Jumlah file train Tahap 04 berubah."
assert int(saved_model.n_features_in_) == len(FEATURE_COLUMNS)

model_fingerprint_at_load = hashlib.sha256(pickle.dumps(saved_model)).hexdigest()
model_file_sha256_at_load = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()

features = pd.read_csv(FEATURES_PATH)
features["label"] = features["label"].astype(int)
features["take"] = features["take"].astype(int)
features["label_name"] = features["label"].map(LABEL_NAME_MAP)
assert len(features) == 176, f"features.csv berisi {len(features)} baris."
assert np.isfinite(features[FEATURE_COLUMNS].to_numpy(dtype=float)).all(), "Fitur mengandung NaN/Inf."

holdout_file_split = pd.read_csv(HOLDOUT_FILE_PATH)
assert len(holdout_file_split) == 176, "holdout_file_split.csv tidak berisi 176 baris."
assert set(holdout_file_split["split"]) == {"train", "test"}, "Nilai split tidak sesuai."

nims_train = sorted(model_config["holdout"]["nims_train"])
nims_test = sorted(model_config["holdout"]["nims_test"])
assert len(nims_test) == 7 and len(nims_train) == 27, "Jumlah NIM train/test berubah."
assert set(nims_train).isdisjoint(set(nims_test)), "NIM train dan test beririsan."

test_files = holdout_file_split.loc[holdout_file_split["split"] == "test"]
assert len(test_files) == 40, f"File test berjumlah {len(test_files)}, bukan 40."
assert sorted(test_files["nim"].unique()) == nims_test, "NIM test tidak cocok dengan config."

merged = features.merge(
    holdout_file_split[["file", "split"]],
    on="file",
    how="inner",
    validate="one_to_one",
)
assert len(merged) == 176, "Gabungan features dan holdout tidak 176 baris."

test_frame = merged.loc[merged["split"] == "test"].reset_index(drop=True)
train_frame = merged.loc[merged["split"] == "train"].reset_index(drop=True)
assert len(test_frame) == 40 and len(train_frame) == 136
assert sorted(test_frame["nim"].unique()) == nims_test
assert set(test_frame["nim"]).isdisjoint(set(nims_train)), "Data uji mengandung NIM train."
assert (
    int((test_frame["label"] == 0).sum()) == 21 and int((test_frame["label"] == 1).sum()) == 19
), "Komposisi kelas data uji berubah."

gate_summary = pd.DataFrame(
    {
        "pemeriksaan": [
            "status validasi Tahap 04",
            "hold-out belum diuji di Tahap 04",
            "model dimuat",
            "sidik jari model",
            "file uji (NIM test)",
            "file latih (NIM train)",
            "NIM test",
            "kelas uji (0 : 1)",
        ],
        "nilai": [
            stage4_validation["status"],
            stage4_validation["holdout_tested_in_stage_04"],
            model_config["model_name"],
            model_fingerprint_at_load[:16],
            len(test_frame),
            len(train_frame),
            len(nims_test),
            f"{int((test_frame['label'] == 0).sum())} : {int((test_frame['label'] == 1).sum())}",
        ],
    }
)
display(gate_summary)
print("Pintu masuk Tahap 05: LULUS")
