PROJECT_ROOT = None
for candidate in [Path.cwd(), *Path.cwd().parents]:
    if (candidate / "raw_audio").is_dir() and (candidate / "artifacts").is_dir():
        PROJECT_ROOT = candidate.resolve()
        break
if PROJECT_ROOT is None:
    raise FileNotFoundError("Folder proyek dengan raw_audio/ dan artifacts/ tidak ditemukan.")

RAW_DIR = PROJECT_ROOT / "raw_audio"
DATA_MP3_DIR = PROJECT_ROOT / "data_mp3"
DATA_FINAL_DIR = PROJECT_ROOT / "data_final"
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts"
ARTIFACT_DIR = ARTIFACT_ROOT / "06_deployment"
DEMO_AUDIO_DIR = ARTIFACT_DIR / "demo_audio"
LAPORAN_PATH = ARTIFACT_ROOT / "LAPORAN.md"

FEATURES_PATH = ARTIFACT_ROOT / "features.csv"
MODEL_PATH = ARTIFACT_ROOT / "best_model.joblib"
MODEL_CONFIG_PATH = ARTIFACT_ROOT / "04_modeling" / "model_config.json"
HOLDOUT_FILE_PATH = ARTIFACT_ROOT / "04_modeling" / "holdout_file_split.csv"
TRANSFORMATION_MANIFEST_PATH = (
    ARTIFACT_ROOT / "03_data_preparation" / "transformation_manifest.csv"
)
PREPROCESSING_CONTRACT_PATH = (
    ARTIFACT_ROOT / "03_data_preparation" / "preprocessing_contract.json"
)
STAGE3_VALIDATION_PATH = ARTIFACT_ROOT / "03_data_preparation" / "validation_summary.json"
STAGE4_VALIDATION_PATH = ARTIFACT_ROOT / "04_modeling" / "validation_summary.json"
STAGE5_VALIDATION_PATH = ARTIFACT_ROOT / "05_evaluation" / "validation_summary.json"
STAGE3_SUMMARY_PATH = ARTIFACT_ROOT / "03_data_preparation" / "data_preparation_summary.json"

PREDICTIONS_PATH = ARTIFACT_ROOT / "test_results" / "test_predictions.csv"
METRICS_PATH = ARTIFACT_ROOT / "test_results" / "metrics.json"
EVALUATION_SUMMARY_PATH = ARTIFACT_ROOT / "05_evaluation" / "evaluation_summary.json"

IDENTITY_CHECK_PATH = ARTIFACT_DIR / "feature_identity_check.csv"
IDENTITY_SUMMARY_PATH = ARTIFACT_DIR / "identity_summary.json"
DEMO_RESULTS_PATH = ARTIFACT_DIR / "demo_results.csv"

for directory in [ARTIFACT_DIR, DEMO_AUDIO_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

SR = 16000
TARGET_DURATION_S = 30.0
TARGET_SAMPLES = int(SR * TARGET_DURATION_S)
FRAME_LENGTH = 400
HOP_LENGTH = 160
N_FFT = 512
ROLLOFF_PERCENT = 0.85
TARGET_PEAK = 1.0
EPS = np.finfo(np.float64).eps

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
LABEL_ORDER = ["non-berisik", "berisik"]

TEST_THRESHOLD = 0.5
FEATURE_REL_TOL = 1e-3
PROBA_MATCH_TOL = 5e-3
MODEL_IDENTITY_TOL = 1e-12

CONFIG = pd.DataFrame(
    {
        "parameter": [
            "project_root",
            "model",
            "threshold keputusan",
            "toleransi fitur relatif",
            "toleransi probabilitas",
            "sample rate",
            "target sampel",
            "frame / hop / n_fft",
            "laporan akhir",
        ],
        "nilai": [
            str(PROJECT_ROOT),
            str(MODEL_PATH),
            TEST_THRESHOLD,
            FEATURE_REL_TOL,
            PROBA_MATCH_TOL,
            SR,
            TARGET_SAMPLES,
            f"{FRAME_LENGTH} / {HOP_LENGTH} / {N_FFT}",
            str(LAPORAN_PATH),
        ],
    }
)

display(CONFIG)
