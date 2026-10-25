SCORING_SET = {
    "roc_auc": "roc_auc",
    "accuracy": "accuracy",
    "precision": make_scorer(precision_score, zero_division=0),
    "recall": make_scorer(recall_score, zero_division=0),
    "f1": make_scorer(f1_score, zero_division=0),
}


def make_pipeline(estimator, k=len(FEATURE_COLUMNS)):
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("select", SelectKBest(score_func=f_classif, k=k)),
            ("clf", estimator),
        ]
    )


model_train = features.loc[features["split"] == "train"].reset_index(drop=True)
model_test = features.loc[features["split"] == "test"].reset_index(drop=True)

X_train = model_train[FEATURE_COLUMNS].to_numpy(dtype=float)
y_train = model_train["label"].to_numpy(dtype=int)
groups_train = model_train["nim"].to_numpy()

assert set(model_train["nim"]).isdisjoint(set(model_test["nim"])), "NIM train dan test beririsan."
assert not set(model_train["nim"]) & set(nims_test), "Data latih mengandung NIM hold-out."

cv_splitter = GroupKFold(n_splits=N_SPLITS)

baseline_estimator = DummyClassifier(strategy="prior")
baseline_pipe = make_pipeline(baseline_estimator, k=len(FEATURE_COLUMNS))
baseline_cv = cross_validate(
    baseline_pipe,
    X_train,
    y_train,
    groups=groups_train,
    cv=cv_splitter,
    scoring=SCORING_SET,
    n_jobs=1,
    return_train_score=True,
)
baseline_roc_auc = float(np.mean(baseline_cv["test_roc_auc"]))
assert abs(baseline_roc_auc - 0.5) < 1e-9, f"Baseline ROC-AUC = {baseline_roc_auc}, bukan 0.50."

pipeline_frame = pd.DataFrame(
    {
        "langkah": [name for name, _ in baseline_pipe.steps],
        "estimator": [type(estimator).__name__ for _, estimator in baseline_pipe.steps],
        "fit_pada": ["training fold", "training fold", "training fold"],
    }
)
display(pipeline_frame)
print(f"Baseline ROC-AUC (GroupKFold, {N_SPLITS} fold): {baseline_roc_auc:.4f}")
print(
    f"Data latih: {len(model_train)} file, {model_train['nim'].nunique()} NIM, "
    f"kelas {model_train['label'].value_counts().sort_index().to_dict()}"
)
