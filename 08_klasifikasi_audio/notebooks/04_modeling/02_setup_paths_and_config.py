PROJECT_ROOT = None
for candidate in [Path.cwd(), *Path.cwd().parents]:
    if (candidate / "raw_audio").is_dir() and (candidate / "artifacts").is_dir():
        PROJECT_ROOT = candidate.resolve()
        break
if PROJECT_ROOT is None:
    raise FileNotFoundError("Folder proyek dengan raw_audio/ dan artifacts/ tidak ditemukan.")

ARTIFACT_ROOT = PROJECT_ROOT / "artifacts"
ARTIFACT_DIR = ARTIFACT_ROOT / "04_modeling"
FIGURE_DIR = ARTIFACT_DIR / "figures"

FEATURES_PATH = ARTIFACT_ROOT / "features.csv"
SELECTED_FEATURES_PATH = ARTIFACT_ROOT / "selected_features.txt"
STAGE3_VALIDATION_PATH = ARTIFACT_ROOT / "03_data_preparation" / "validation_summary.json"

MODEL_PATH = ARTIFACT_ROOT / "best_model.joblib"
HOLDOUT_SPLIT_PATH = ARTIFACT_DIR / "holdout_split.csv"
HOLDOUT_FILE_PATH = ARTIFACT_DIR / "holdout_file_split.csv"
MODEL_CONFIG_PATH = ARTIFACT_DIR / "model_config.json"
FEATURE_LIST_PATH = ARTIFACT_DIR / "feature_list.txt"

for directory in [ARTIFACT_DIR, FIGURE_DIR]:
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

N_SPLITS = 5
TEST_SIZE = 0.2
SCORING = "roc_auc"
RANDOM_STATE = 42

MODEL_CANDIDATES = [
    "Logistic Regression",
    "SVM-RBF",
    "Random Forest",
    "Gradient Boosting",
]

CONFIG = pd.DataFrame(
    {
        "parameter": [
            "project_root",
            "artifact_dir",
            "n_splits (GroupKFold)",
            "test_size NIM (GroupShuffleSplit)",
            "scoring",
            "random_state",
            "jumlah fitur",
            "kandidat model",
        ],
        "nilai": [
            str(PROJECT_ROOT),
            str(ARTIFACT_DIR),
            N_SPLITS,
            TEST_SIZE,
            SCORING,
            RANDOM_STATE,
            len(FEATURE_COLUMNS),
            ", ".join(MODEL_CANDIDATES),
        ],
    }
)

display(CONFIG)
print(f"Model akan disimpan di: {MODEL_PATH}")
