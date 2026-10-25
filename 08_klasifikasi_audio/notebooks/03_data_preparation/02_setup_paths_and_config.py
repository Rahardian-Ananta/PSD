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
QUARANTINE_DIR = PROJECT_ROOT / "quarantine" / "03_data_preparation"
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts"
ARTIFACT_DIR = ARTIFACT_ROOT / "03_data_preparation"
FIGURE_DIR = ARTIFACT_DIR / "figures"
DU_ARTIFACT_DIR = ARTIFACT_ROOT / "02_data_understanding"

for directory in [
    DATA_MP3_DIR,
    DATA_FINAL_DIR,
    QUARANTINE_DIR,
    ARTIFACT_DIR,
    FIGURE_DIR,
]:
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
RANDOM_STATE = 42

LABEL_NAME_MAP = {0: "non-berisik", 1: "berisik"}
LABEL_ORDER = ["non-berisik", "berisik"]

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

SPECTRAL_FEATURES = [
    "spectral_centroid_mean",
    "spectral_centroid_std",
    "spectral_flatness_mean",
    "spectral_rolloff_mean",
    "spectral_bandwidth_mean",
]

IDENTITY_COLUMNS = ["file", "nim", "take", "label"]

PREPROCESSING_CONTRACT = {
    "sample_rate": SR,
    "channels": 1,
    "target_duration_seconds": TARGET_DURATION_S,
    "target_samples": TARGET_SAMPLES,
    "decode": "librosa.load(path, sr=16000, mono=True)",
    "longer_than_target": "center crop; start=(n_samples-target_samples)//2",
    "shorter_than_target": "center zero pad; left=pad//2, right=pad-left",
    "peak_normalization": "after crop/pad; y/max(abs(y))*1.0; error if max(abs(y))==0",
    "output_format": "WAV PCM_16, mono, 16000 Hz",
    "frame_length": FRAME_LENGTH,
    "hop_length": HOP_LENGTH,
    "n_fft": N_FFT,
    "window": "Hann simetris: 0.5 - 0.5*cos(2*pi*n/(L-1))",
    "rolloff_percent": ROLLOFF_PERCENT,
    "flatness_epsilon": float(EPS),
}

CONFIG = pd.DataFrame(
    {
        "parameter": [
            "project_root",
            "sample_rate",
            "target_duration_s",
            "target_samples",
            "frame_length",
            "hop_length",
            "n_fft",
            "rolloff_percent",
            "target_peak",
            "random_state",
        ],
        "nilai": [
            str(PROJECT_ROOT),
            SR,
            TARGET_DURATION_S,
            TARGET_SAMPLES,
            FRAME_LENGTH,
            HOP_LENGTH,
            N_FFT,
            ROLLOFF_PERCENT,
            TARGET_PEAK,
            RANDOM_STATE,
        ],
    }
)

display(CONFIG)
print(f"Artifact directory: {ARTIFACT_DIR}")
