fpr, tpr, roc_thresholds = roc_curve(y_test, proba_1)

fig, ax = plt.subplots(figsize=(6.4, 5.4))
ax.plot(fpr, tpr, color="#457b9d", linewidth=2, label=f"ROC (AUC = {roc_auc_value:.4f})")
ax.plot([0, 1], [0, 1], color="#adb5bd", linestyle="--", linewidth=1.4, label="akurasi acak (0,50)")
ax.fill_between(fpr, tpr, alpha=0.15, color="#457b9d")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title(f"Kurva ROC — hold-out {len(nims_test)} NIM ({len(y_test)} file)")
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(TEST_FIGURE_DIR / "roc_curve.png")
plt.show()

pr_precision, pr_recall, _ = precision_recall_curve(y_test, proba_1)

fig, ax = plt.subplots(figsize=(6.4, 5.4))
ax.plot(pr_recall, pr_precision, color="#e76f51", linewidth=2, label=f"PR (AP = {pr_auc_value:.4f})")
ax.axhline(
    prevalence_value,
    color="#adb5bd",
    linestyle="--",
    linewidth=1.4,
    label=f"baseline prevalensi ({prevalence_value:.4f})",
)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)
ax.set_xlabel("Recall (kelas berisik)")
ax.set_ylabel("Precision (kelas berisik)")
ax.set_title(f"Kurva PR — hold-out {len(nims_test)} NIM ({len(y_test)} file)")
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig(TEST_FIGURE_DIR / "pr_curve.png")
plt.show()

fig, ax = plt.subplots(figsize=(5.6, 4.8))
sns.heatmap(
    cm_array,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["non-berisik", "berisik"],
    yticklabels=["non-berisik", "berisik"],
    cbar=False,
    ax=ax,
)
ax.set_xlabel("label prediksi")
ax.set_ylabel("label sebenarnya")
ax.set_title(f"Confusion matrix (threshold {TEST_THRESHOLD})")
fig.tight_layout()
fig.savefig(TEST_FIGURE_DIR / "confusion_matrix.png")
plt.show()

fig, ax = plt.subplots(figsize=(7.2, 4.8))
bins = np.linspace(0, 1, 21)
ax.hist(
    proba_1[y_test == 0],
    bins=bins,
    alpha=0.65,
    color="#457b9d",
    label=f"aktual non-berisik (n={int((y_test == 0).sum())})",
)
ax.hist(
    proba_1[y_test == 1],
    bins=bins,
    alpha=0.65,
    color="#e76f51",
    label=f"aktual berisik (n={int((y_test == 1).sum())})",
)
ax.axvline(TEST_THRESHOLD, color="#2a9d8f", linestyle="--", linewidth=1.6, label=f"threshold {TEST_THRESHOLD}")
ax.set_xlabel("probabilitas prediksi kelas berisik")
ax.set_ylabel("jumlah file")
ax.set_title("Distribusi probabilitas pada data uji")
ax.legend(loc="upper center")
fig.tight_layout()
fig.savefig(TEST_FIGURE_DIR / "proba_distribution.png")
plt.show()

print("Gambar evaluasi:", ", ".join(FIGURES_EXPECTED[:4]))
