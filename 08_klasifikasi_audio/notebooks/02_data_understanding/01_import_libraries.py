# Tujuan: menyiapkan pustaka dan pengaturan dasar untuk analisis Data Understanding.
# Proses: mengimpor pustaka, menetapkan opsi tampilan, tema grafik, dan random seed.
# Output: ringkasan versi pustaka yang benar-benar digunakan.

import hashlib
import json
import math
import platform
import re
import shutil
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message="IProgress not found.*")

import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import soundfile as sf
from IPython.display import display

pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 160)
pd.set_option("display.max_rows", 100)

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.dpi"] = 110
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["axes.titleweight"] = "bold"

RANDOM_STATE = 42

library_versions = pd.DataFrame(
    {
        "komponen": [
            "Python",
            "numpy",
            "pandas",
            "librosa",
            "soundfile",
            "matplotlib",
            "seaborn",
            "FFmpeg (PATH)",
        ],
        "versi": [
            platform.python_version(),
            np.__version__,
            pd.__version__,
            librosa.__version__,
            sf.__version__,
            plt.matplotlib.__version__,
            sns.__version__,
            shutil.which("ffmpeg") or "tidak ditemukan",
        ],
    }
)

display(library_versions)
