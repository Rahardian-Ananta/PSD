PROJECT_ROOT = None
for candidate in [Path.cwd(), *Path.cwd().parents]:
    if (candidate / "raw_audio").is_dir() and (candidate / "artifacts").is_dir():
        PROJECT_ROOT = candidate.resolve()
        break
if PROJECT_ROOT is None:
    raise FileNotFoundError("Folder proyek dengan raw_audio/ dan artifacts/ tidak ditemukan.")

ARTIFACT_ROOT = PROJECT_ROOT / "artifacts"
ARTIFACT_DIR = ARTIFACT_ROOT / "05_evaluation"
FIGURE_DIR = ARTIFACT_DIR / "figures"
TEST_RESULTS_DIR = ARTIFACT_ROOT / "test_results"
TEST_FIGURE_DIR = TEST_RESULTS_DIR / "figures"

FEATURES_PATH = ARTIFACT_ROOT / "features.csv"
MODEL_PATH = ARTIFACT_ROOT / "best_model.joblib"
MODEL_CONFIG_PATH = ARTIFACT_ROOT / "04_modeling" / "model_config.json"
STAGE4_VALIDATION_PATH = ARTIFACT_ROOT / "04_modeling" / "validation_summary.json"
HOLDOUT_FILE_PATH = ARTIFACT_ROOT / "04_modeling" / "holdout_file_split.csv"

PREDICTIONS_PATH = TEST_RESULTS_DIR / "test_predictions.csv"
METRICS_PATH = TEST_RESULTS_DIR / "metrics.json"
REPORT_METRICS_PATH = TEST_RESULTS_DIR / "classification_report.csv"
CONFUSION_PATH = TEST_RESULTS_DIR / "confusion_matrix.csv"
METRICS_BY_NIM_PATH = TEST_RESULTS_DIR / "metrics_by_nim.csv"
ERRORS_PATH = TEST_RESULTS_DIR / "errors.csv"

for directory in [ARTIFACT_DIR, FIGURE_DIR, TEST_RESULTS_DIR, TEST_FIGURE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

IDENTITY_COLUMNS = ["file", "nim", "take", "label"]

FEATURE_COLUMNS = [
    "mse_energy",
    "rms_mean",
    "rms_std",
    "rms_max",
    "rms_min",
    "zcr_mean",
    "zcr_std",
    "spectral_centroid_mean",
    "spectral_centroid_std",
    "spectral_flatness_mean",
    "spectral_rolloff_mean",
    "spectral_bandwidth_mean",
]

LABEL_NAME_MAP = {0: "non-berisik", 1: "berisik"}

TEST_THRESHOLD = 0.5
ROC_AUC_THRESHOLD = 0.85
BASELINE_ROC_AUC = 0.5
BOOTSTRAP_N = 2000
RANDOM_STATE = 42

FIGURES_EXPECTED = [
    "roc_curve.png",
    "pr_curve.png",
    "confusion_matrix.png",
    "proba_distribution.png",
    "roc_auc_bootstrap.png",
]

CONFIG = pd.DataFrame(
    {
        "parameter": [
            "project_root",
            "model",
            "threshold keputusan",
            "syarat kelayakan ROC-AUC",
            "baseline ROC-AUC",
            "jumlah bootstrap",
            "output evaluasi",
            "random_state",
        ],
        "nilai": [
            str(PROJECT_ROOT),
            str(MODEL_PATH),
            TEST_THRESHOLD,
            ROC_AUC_THRESHOLD,
            BASELINE_ROC_AUC,
            BOOTSTRAP_N,
            str(TEST_RESULTS_DIR),
            RANDOM_STATE,
        ],
    }
)

display(CONFIG)
