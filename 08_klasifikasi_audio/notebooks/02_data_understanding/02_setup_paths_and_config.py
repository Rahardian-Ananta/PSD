# Tujuan: menemukan lokasi proyek dan menetapkan konfigurasi analisis.
# Proses: memeriksa folder proyek, membuat folder artefak, dan menetapkan pola identitas file.
# Output: path proyek, path data, folder artefak, dan konfigurasi pemeriksaan yang akan dipakai.


def locate_project_root(start):
    for candidate in [start, *start.parents]:
        if (candidate / "raw_audio").is_dir() and (candidate / "notebooks").is_dir():
            return candidate
    raise FileNotFoundError("Folder proyek dengan raw_audio/ dan notebooks/ tidak ditemukan.")


PROJECT_ROOT = locate_project_root(Path.cwd().resolve())
RAW_DIR = PROJECT_ROOT / "raw_audio"
ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "02_data_understanding"
FIGURE_DIR = ARTIFACT_DIR / "figures"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

FILENAME_PATTERN = re.compile(
    r"^(?P<nim>\d{2}-\d{3})_(?P<label_text>berisik|non-berisik)_(?P<take>\d+)\.mp3$",
    flags=re.IGNORECASE,
)
FOLDER_LABEL_MAP = {"berisik": 1, "non-berisik": 0}
LABEL_NAME_MAP = {1: "berisik", 0: "non-berisik"}

EXPECTED_DURATION_S = 30.0
DURATION_TOLERANCE_S = 0.01
LOW_PEAK_THRESHOLD = 0.05
AUDIO_EXTENSIONS = {".mp3"}

config = pd.DataFrame(
    {
        "parameter": [
            "PROJECT_ROOT",
            "RAW_DIR",
            "ARTIFACT_DIR",
            "FIGURE_DIR",
            "durasi acuan",
            "toleransi durasi",
            "ambang peak level rendah",
            "pola nama file",
        ],
        "nilai": [
            str(PROJECT_ROOT),
            str(RAW_DIR),
            str(ARTIFACT_DIR),
            str(FIGURE_DIR),
            f"{EXPECTED_DURATION_S:.1f} detik",
            f"{DURATION_TOLERANCE_S:.2f} detik",
            f"peak < {LOW_PEAK_THRESHOLD:.2f}",
            FILENAME_PATTERN.pattern,
        ],
    }
)

display(config)
print("FFmpeg di PATH:", shutil.which("ffmpeg") or "tidak ditemukan")
