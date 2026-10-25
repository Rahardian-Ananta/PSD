roc_auc_value = float(roc_auc_score(y_test, proba_1))
pr_auc_value = float(average_precision_score(y_test, proba_1))
accuracy_value = float(accuracy_score(y_test, pred_label))
precision_value = float(precision_score(y_test, pred_label, zero_division=0))
recall_value = float(recall_score(y_test, pred_label, zero_division=0))
f1_value = float(f1_score(y_test, pred_label, zero_division=0))

cm_array = confusion_matrix(y_test, pred_label, labels=[0, 1])
tn, fp, fn, tp = (int(value) for value in cm_array.ravel())
assert tn + fp + fn + tp == len(y_test), "Confusion matrix tidak berjumlah 40."

report_dict = classification_report(
    y_test,
    pred_label,
    labels=[0, 1],
    target_names=["non-berisik", "berisik"],
    output_dict=True,
    zero_division=0,
)
report_frame = pd.DataFrame(report_dict).T.round(4)
report_frame.index.name = "kelas"
report_frame.to_csv(REPORT_METRICS_PATH)

cm_frame = pd.DataFrame(
    cm_array, index=["actual_non_berisik", "actual_berisik"], columns=["pred_non_berisik", "pred_berisik"]
)
cm_frame.to_csv(CONFUSION_PATH)

prevalence_value = float(y_test.mean())
meets_kelayakan = bool(roc_auc_value >= ROC_AUC_THRESHOLD)

metrics = {
    "stage": "05_evaluation",
    "model_name": model_config["model_name"],
    "model_class": model_config["model_class"],
    "model_file": str(MODEL_PATH.relative_to(PROJECT_ROOT)),
    "n_files_test": int(len(y_test)),
    "n_nim_test": int(len(nims_test)),
    "nims_test": nims_test,
    "class_counts_test": {
        "0": int((y_test == 0).sum()),
        "1": int((y_test == 1).sum()),
    },
    "test_threshold": TEST_THRESHOLD,
    "roc_auc": roc_auc_value,
    "pr_auc": pr_auc_value,
    "accuracy": accuracy_value,
    "precision_class_1": precision_value,
    "recall_class_1": recall_value,
    "f1_class_1": f1_value,
    "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
    "baseline_roc_auc": BASELINE_ROC_AUC,
    "pr_baseline_prevalence": prevalence_value,
    "roc_auc_threshold": ROC_AUC_THRESHOLD,
    "roc_auc_meets_threshold": meets_kelayakan,
    "kelayakan_status": (
        "LOLOS SYARAT AWAL" if meets_kelayakan else "DI BAWAH SYARAT AWAL"
    ),
    "best_cv_roc_auc_tahap_04": float(model_config["best_cv_roc_auc"]),
    "random_state": RANDOM_STATE,
}
METRICS_PATH.write_text(
    json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
)

metrics_table = pd.DataFrame(
    {
        "metrik": [
            "ROC-AUC",
            "PR-AUC",
            "accuracy",
            "precision (kelas 1)",
            "recall (kelas 1)",
            "F1 (kelas 1)",
            "confusion TN / FP / FN / TP",
            "baseline ROC-AUC",
            "baseline PR (prevalensi)",
            "syarat kelayakan ROC-AUC",
            "status syarat",
        ],
        "nilai": [
            f"{roc_auc_value:.4f}",
            f"{pr_auc_value:.4f}",
            f"{accuracy_value:.4f}",
            f"{precision_value:.4f}",
            f"{recall_value:.4f}",
            f"{f1_value:.4f}",
            f"{tn} / {fp} / {fn} / {tp}",
            f"{BASELINE_ROC_AUC:.4f}",
            f"{prevalence_value:.4f}",
            f"{ROC_AUC_THRESHOLD:.2f}",
            metrics["kelayakan_status"],
        ],
    }
)
display(metrics_table)
display(report_frame)
display(cm_frame)
print(f"Metrik disimpan: {METRICS_PATH}")
