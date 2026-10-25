rng = np.random.default_rng(RANDOM_STATE)
bootstrap_aucs = []
attempts = 0
n_samples = len(y_test)
while len(bootstrap_aucs) < BOOTSTRAP_N:
    attempts += 1
    if attempts > BOOTSTRAP_N * 100:
        raise RuntimeError("Bootstrap tidak konvergen; sampel satu kelas terlalu sering muncul.")
    sample_index = rng.integers(0, n_samples, n_samples)
    sampled_labels = y_test[sample_index]
    if np.unique(sampled_labels).size < 2:
        continue
    bootstrap_aucs.append(float(roc_auc_score(sampled_labels, proba_1[sample_index])))

bootstrap_aucs = np.asarray(bootstrap_aucs)
ci_low, ci_high = (float(value) for value in np.percentile(bootstrap_aucs, [2.5, 97.5]))

metrics_by_nim = (
    test_predictions.groupby("nim")
    .agg(
        n_files=("file", "size"),
        n_class_0=("label", lambda values: int((values == 0).sum())),
        n_class_1=("label", lambda values: int((values == 1).sum())),
        n_benar=("benar", "sum"),
        n_pred_1=("pred_label", "sum"),
    )
    .reset_index()
)
metrics_by_nim["n_salah"] = metrics_by_nim["n_files"] - metrics_by_nim["n_benar"]
metrics_by_nim["accuracy"] = (
    metrics_by_nim["n_benar"] / metrics_by_nim["n_files"]
).round(4)
metrics_by_nim = metrics_by_nim.sort_values("nim").reset_index(drop=True)
assert len(metrics_by_nim) == len(nims_test)
assert int(metrics_by_nim["n_files"].sum()) == len(y_test)
metrics_by_nim.to_csv(METRICS_BY_NIM_PATH, index=False)

errors = test_predictions.loc[~test_predictions["benar"]].copy()
errors.to_csv(ERRORS_PATH, index=False)
assert len(errors) == fn + fp, "Jumlah file salah tidak cocok dengan confusion matrix."

metrics.update(
    {
        "roc_auc_ci_low": ci_low,
        "roc_auc_ci_high": ci_high,
        "roc_auc_ci_level": 0.95,
        "n_bootstrap": int(len(bootstrap_aucs)),
        "bootstrap_attempts": int(attempts),
        "n_files_wrong": int(len(errors)),
        "accuracy_per_nim_mean": float(metrics_by_nim["accuracy"].mean()),
        "accuracy_per_nim_min": float(metrics_by_nim["accuracy"].min()),
        "accuracy_per_nim_max": float(metrics_by_nim["accuracy"].max()),
    }
)
METRICS_PATH.write_text(
    json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
)

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.hist(bootstrap_aucs, bins=30, color="#457b9d", alpha=0.75)
ax.axvline(roc_auc_value, color="#e76f51", linewidth=2, label=f"ROC-AUC uji {roc_auc_value:.4f}")
ax.axvline(ci_low, color="#2a9d8f", linestyle="--", linewidth=1.5, label=f"CI 95% bawah {ci_low:.4f}")
ax.axvline(ci_high, color="#2a9d8f", linestyle="--", linewidth=1.5, label=f"CI 95% atas {ci_high:.4f}")
ax.set_xlabel("ROC-AUC hasil bootstrap")
ax.set_ylabel("frekuensi")
ax.set_title(f"Bootstrap ROC-AUC ({len(bootstrap_aucs)} pengambilan ulang)")
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(TEST_FIGURE_DIR / "roc_auc_bootstrap.png")
plt.show()

print(f"ROC-AUC {roc_auc_value:.4f}; CI95 bootstrap [{ci_low:.4f}, {ci_high:.4f}]")
print(f"File salah: {len(errors)} dari {len(y_test)}")
display(metrics_by_nim)
if len(errors):
    display(
        errors[
            ["file", "nim", "label_name", "pred_label_name", "proba_berisik"]
        ].round(4)
    )
else:
    print("Tidak ada file yang salah prediksi pada data uji.")
