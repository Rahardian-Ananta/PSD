X_test = test_frame[FEATURE_COLUMNS].to_numpy(dtype=float)
y_test = test_frame["label"].to_numpy(dtype=int)

assert np.isfinite(X_test).all(), "Fitur uji mengandung NaN/Inf."
assert X_test.shape == (40, len(FEATURE_COLUMNS))

class_index_1 = int(np.where(saved_model.classes_ == 1)[0][0])
proba = saved_model.predict_proba(X_test)
assert proba.shape == (40, 2), f"Bentuk probabilitas {proba.shape} tidak sesuai."
assert np.allclose(proba.sum(axis=1), 1.0), "Probabilitas per baris tidak berjumlah 1."

proba_1 = proba[:, class_index_1]
proba_0 = proba[:, 1 - class_index_1]
pred_label = (proba_1 >= TEST_THRESHOLD).astype(int)
pred_from_model = saved_model.predict(X_test)
assert np.array_equal(pred_label, pred_from_model), (
    "Threshold 0,50 tidak konsisten dengan predict() pipeline."
)

test_predictions = test_frame[
    ["file", "nim", "take", "label", "label_name", "split"]
].copy()
test_predictions["proba_non_berisik"] = proba_0
test_predictions["proba_berisik"] = proba_1
test_predictions["pred_label"] = pred_label
test_predictions["pred_label_name"] = pd.Series(pred_label).map(LABEL_NAME_MAP).values
test_predictions["proba_diprediksi"] = np.maximum(proba_0, proba_1)
test_predictions["benar"] = pred_label == y_test

assert not test_predictions[["proba_non_berisik", "proba_berisik"]].isna().any().any()
assert set(test_predictions["nim"]).issubset(set(nims_test))
assert len(test_predictions) == 40 and test_predictions["file"].is_unique

test_predictions = test_predictions.sort_values("nim").reset_index(drop=True)
test_predictions.to_csv(PREDICTIONS_PATH, index=False)

prediction_summary = pd.DataFrame(
    {
        "baris": ["semua", "aktual_0", "aktual_1", "diprediksi_0", "diprediksi_1", "benar"],
        "jumlah": [
            len(test_predictions),
            int((y_test == 0).sum()),
            int((y_test == 1).sum()),
            int((pred_label == 0).sum()),
            int((pred_label == 1).sum()),
            int((pred_label == y_test).sum()),
        ],
    }
)
display(prediction_summary)
display(test_predictions.head(10).round(4))
print(f"Prediksi disimpan: {PREDICTIONS_PATH}")
