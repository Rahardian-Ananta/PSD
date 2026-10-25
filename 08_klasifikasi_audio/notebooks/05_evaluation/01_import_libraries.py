import hashlib
import json
import pickle
import platform
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message="IProgress not found.*")

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import Markdown, display
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 180)
pd.set_option("display.max_rows", 120)

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
            "scikit-learn",
            "joblib",
            "matplotlib",
            "seaborn",
        ],
        "versi": [
            platform.python_version(),
            np.__version__,
            pd.__version__,
            __import__("sklearn").__version__,
            joblib.__version__,
            plt.matplotlib.__version__,
            sns.__version__,
        ],
    }
)

display(library_versions)
