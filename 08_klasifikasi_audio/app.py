"""
Aplikasi Streamlit: deteksi suasana kelas BERISIK vs NON-BERISIK.

Alur:
  rekam / upload audio  ->  diubah ke WAV mono 16 kHz  ->  potong/tambah ke 30 detik
  ->  samakan volume  ->  hitung 12 fitur  ->  model best_model.joblib  ->  hasil

Seluruh rumus pemrosesan SAMA PERSIS dengan notebook 03 dan 06 (predict_audio).

Cara jalan (dari folder mana pun):
    pip install -r 08_klasifikasi_audio/requirements.txt
    streamlit run 08_klasifikasi_audio/app.py
"""

import io
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import joblib
import librosa
import numpy as np
import pandas as pd
import soundfile as sf
import streamlit as st

# --------------------------------------------------------------------------- #
# Konstanta: harus sama dengan preprocessing_contract.json (notebook 03 / 06)
# --------------------------------------------------------------------------- #
SR = 16000
TARGET_DURATION_S = 30.0
TARGET_SAMPLES = int(SR * TARGET_DURATION_S)  # 480.000
FRAME_LENGTH = 400
HOP_LENGTH = 160
N_FFT = 512
ROLLOFF_PERCENT = 0.85
TARGET_PEAK = 1.0
EPS = np.finfo(np.float64).eps
THRESHOLD = 0.5

FEATURE_COLUMNS = [
    "mse_energy", "rms_mean", "rms_std", "rms_max", "rms_min",
    "zcr_mean", "zcr_std",
    "spectral_centroid_mean", "spectral_centroid_std",
    "spectral_flatness_mean", "spectral_rolloff_mean", "spectral_bandwidth_mean",
]
LABEL_NAME_MAP = {0: "non-berisik", 1: "berisik"}

# Lokasi model: bisa diganti lewat variabel lingkungan MODEL_PATH.
# Path default dihitung dari folder app.py (bukan cwd), supaya tetap benar
# meski dijalankan sebagai `streamlit run 08_klasifikasi_audio/app.py` dari root.
APP_DIR = Path(__file__).resolve().parent
_env_model = os.environ.get("MODEL_PATH")
DEFAULT_MODEL_PATH = Path(_env_model) if _env_model else APP_DIR / "artifacts" / "best_model.joblib"

AUDIO_TYPES = ["wav", "mp3", "m4a", "aac", "ogg", "oga", "opus", "flac", "webm", "wma", "amr", "mp4", "3gp"]

FREQS = np.fft.rfftfreq(N_FFT, d=1 / SR)
HANN_WINDOW = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(FRAME_LENGTH) / (FRAME_LENGTH - 1))


# --------------------------------------------------------------------------- #
# Pemrosesan audio (disalin dari notebook 06)
# --------------------------------------------------------------------------- #
def fit_duration_to_target(y, target_samples=TARGET_SAMPLES):
    """Potong dari tengah kalau terlalu panjang, tambah nol kiri-kanan kalau terlalu pendek."""
    y = np.asarray(y)
    n = int(len(y))
    if n > target_samples:
        start = (n - target_samples) // 2
        return y[start:start + target_samples].copy(), "crop"
    if n < target_samples:
        total_pad = target_samples - n
        left = total_pad // 2
        right = total_pad - left
        return np.pad(y, (left, right), mode="constant", constant_values=0.0), "pad"
    return y.copy(), "none"


def peak_normalize(y, target_peak=TARGET_PEAK):
    y = np.asarray(y)
    if y.size == 0:
        raise ValueError("Audio kosong.")
    if not np.isfinite(y).all():
        raise ValueError("Audio mengandung nilai rusak (NaN/Inf).")
    peak = float(np.max(np.abs(y)))
    if peak <= 0:
        raise ValueError("Audio sunyi total (semua sampel nol), tidak bisa dianalisis.")
    return (y / peak * target_peak).astype(np.float32), peak


def extract_features(y):
    y = np.asarray(y)
    if len(y) != TARGET_SAMPLES:
        raise ValueError(f"Fitur hanya boleh dihitung dari {TARGET_SAMPLES} sampel.")

    features = {"mse_energy": float(np.mean(y.astype(np.float64) ** 2))}

    frames = np.lib.stride_tricks.sliding_window_view(y, FRAME_LENGTH)[::HOP_LENGTH].astype(np.float64)
    rms_frames = np.sqrt(np.mean(frames ** 2, axis=1))
    zcr_frames = np.mean((frames[:, :-1] * frames[:, 1:]) < 0, axis=1)

    P = np.abs(np.fft.rfft(frames * HANN_WINDOW[None, :], n=N_FFT, axis=1)) ** 2
    power_sum = P.sum(axis=1)
    centroids = np.divide(P @ FREQS, power_sum, out=np.zeros_like(power_sum), where=power_sum > 0)

    P_eps = P + EPS
    flatness_frames = np.exp(np.mean(np.log(P_eps), axis=1)) / np.mean(P_eps, axis=1)
    flatness_frames[P.sum(axis=1) == 0] = 0

    cumulative = np.cumsum(P, axis=1)
    total_power = cumulative[:, -1]
    rolloff_idx = np.argmax(cumulative >= (ROLLOFF_PERCENT * total_power)[:, None], axis=1)
    rolloff_frames = FREQS[rolloff_idx].copy()
    rolloff_frames[total_power == 0] = 0

    variance = np.divide(
        (P * (FREQS[None, :] - centroids[:, None]) ** 2).sum(axis=1),
        power_sum, out=np.zeros_like(power_sum), where=power_sum > 0,
    )
    bandwidth_frames = np.sqrt(np.maximum(variance, 0))

    features.update({
        "rms_mean": float(np.mean(rms_frames)),
        "rms_std": float(np.std(rms_frames, ddof=0)),
        "rms_max": float(np.max(rms_frames)),
        "rms_min": float(np.min(rms_frames)),
        "zcr_mean": float(np.mean(zcr_frames)),
        "zcr_std": float(np.std(zcr_frames, ddof=0)),
        "spectral_centroid_mean": float(np.mean(centroids)),
        "spectral_centroid_std": float(np.std(centroids, ddof=0)),
        "spectral_flatness_mean": float(np.mean(flatness_frames)),
        "spectral_rolloff_mean": float(np.mean(rolloff_frames)),
        "spectral_bandwidth_mean": float(np.mean(bandwidth_frames)),
    })
    if list(features) != FEATURE_COLUMNS:
        features = {k: features[k] for k in FEATURE_COLUMNS}
    if not all(np.isfinite(v) for v in features.values()):
        raise ValueError("Fitur mengandung NaN/Inf.")
    return features


# --------------------------------------------------------------------------- #
# Dekode + konversi ke WAV 16 kHz mono
# --------------------------------------------------------------------------- #
def decode_to_16k_mono(raw_bytes, filename):
    """
    Ubah audio format apa pun menjadi sinyal mono 16 kHz.
    1) coba librosa (sama dengan saat pelatihan);
    2) kalau gagal (misalnya webm/m4a), konversi dulu dengan FFmpeg lalu baca lagi.
    """
    suffix = Path(filename).suffix.lower() or ".audio"
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / f"input{suffix}"
        src.write_bytes(raw_bytes)

        try:
            y, _ = librosa.load(str(src), sr=SR, mono=True)
            if y.size > 0:
                return y
        except Exception:
            pass

        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg is None:
            raise RuntimeError(
                "Format audio ini tidak bisa dibaca dan FFmpeg tidak ditemukan. "
                "Pasang FFmpeg, atau unggah file WAV/MP3."
            )
        dst = Path(tmp) / "converted.wav"
        proc = subprocess.run(
            [ffmpeg, "-y", "-i", str(src), "-ac", "1", "-ar", str(SR), "-vn", str(dst)],
            capture_output=True, text=True,
        )
        if proc.returncode != 0 or not dst.exists():
            raise RuntimeError("Gagal mengubah file ke WAV. Pastikan file benar-benar berisi audio.")
        y, _ = librosa.load(str(dst), sr=SR, mono=True)
        if y.size == 0:
            raise RuntimeError("Audio kosong.")
        return y


def to_wav_bytes(y):
    """Sinyal 16 kHz mono -> isi file WAV (PCM 16-bit) untuk diputar/diunduh."""
    buf = io.BytesIO()
    sf.write(buf, np.clip(y, -1.0, 1.0), SR, format="WAV", subtype="PCM_16")
    return buf.getvalue()


# --------------------------------------------------------------------------- #
# Prediksi
# --------------------------------------------------------------------------- #
@st.cache_resource(show_spinner="Memuat model...")
def load_model(path_str):
    return joblib.load(path_str)


def predict_signal(y, model, threshold=THRESHOLD):
    y_fit, action = fit_duration_to_target(y)
    y_norm, peak_before = peak_normalize(y_fit)
    feats = extract_features(y_norm)

    X = np.array([[feats[c] for c in FEATURE_COLUMNS]], dtype=float)
    proba = model.predict_proba(X)[0]
    proba_map = {int(c): float(p) for c, p in zip(model.classes_, proba)}
    p_noisy = proba_map[1]
    label = int(p_noisy >= threshold)
    return {
        "label": label,
        "label_name": LABEL_NAME_MAP[label],
        "p_berisik": p_noisy,
        "p_non_berisik": proba_map[0],
        "duration_action": action,
        "original_duration_s": len(y) / SR,
        "peak_before_norm": peak_before,
        "features": feats,
    }


# --------------------------------------------------------------------------- #
# Tampilan
# --------------------------------------------------------------------------- #
def analyze(raw_bytes, filename, model):
    with st.spinner("Mengubah ke WAV 16 kHz mono..."):
        y = decode_to_16k_mono(raw_bytes, filename)
    wav_bytes = to_wav_bytes(y)

    st.markdown("**Audio setelah dikonversi ke WAV (16 kHz, mono)**")
    st.audio(wav_bytes, format="audio/wav")
    st.download_button(
        "Unduh WAV hasil konversi",
        data=wav_bytes,
        file_name=f"{Path(filename).stem}_16k_mono.wav",
        mime="audio/wav",
    )

    with st.spinner("Menghitung fitur dan memprediksi..."):
        result = predict_signal(y, model)

    dur = result["original_duration_s"]
    if result["duration_action"] == "pad":
        st.warning(
            f"Durasi audio {dur:.1f} detik, kurang dari 30 detik. Sisanya diisi hening (nol) di kiri dan kanan. "
            "Model dilatih dengan rekaman 30 detik, jadi hasilnya bisa kurang akurat."
        )
    elif result["duration_action"] == "crop":
        st.info(
            f"Durasi audio {dur:.1f} detik, lebih dari 30 detik. Yang dianalisis hanya 30 detik di bagian tengah."
        )
    else:
        st.success("Durasi audio tepat 30 detik.")

    st.divider()
    noisy = result["label"] == 1
    p_noisy = result["p_berisik"]
    p_pred = p_noisy if noisy else result["p_non_berisik"]

    if noisy:
        st.error(f"## BERISIK\nSkor model: {p_pred:.1%}")
    else:
        st.success(f"## NON-BERISIK\nSkor model: {p_pred:.1%}")

    c1, c2 = st.columns(2)
    c1.metric("Skor berisik", f"{p_noisy:.1%}")
    c2.metric("Skor non-berisik", f"{result['p_non_berisik']:.1%}")
    st.progress(min(max(p_noisy, 0.0), 1.0), text=f"Skor berisik {p_noisy:.1%} (batas keputusan {THRESHOLD:.0%})")

    if 0.35 <= p_noisy <= 0.65:
        st.caption("Skor berada dekat batas 50%, jadi hasilnya kurang pasti. Sebaiknya dicek manual.")

    with st.expander("Lihat 12 fitur suara yang dihitung"):
        st.dataframe(
            pd.DataFrame({"fitur": list(result["features"]), "nilai": list(result["features"].values())}),
            hide_index=True, use_container_width=True,
        )


def main():
    st.set_page_config(page_title="Deteksi Kelas Berisik", page_icon="🎙️", layout="centered")
    st.title("Deteksi Kelas Berisik")
    st.write(
        "Rekam suara kelas atau unggah file audio. Audio akan diubah ke WAV (16 kHz, mono), "
        "lalu dicek apakah suasananya **berisik** atau **non-berisik**."
    )

    with st.sidebar:
        model_path = st.text_input("Lokasi model", value=str(DEFAULT_MODEL_PATH))

    if not Path(model_path).is_file():
        st.error(
            f"File model tidak ditemukan: `{model_path}`. "
            "Jalankan aplikasi dari folder proyek yang berisi `artifacts/best_model.joblib`, "
            "atau isi lokasi model yang benar di sidebar."
        )
        st.stop()

    try:
        model = load_model(model_path)
    except Exception as exc:
        st.error(f"Model gagal dimuat: {exc}. Pastikan versi scikit-learn sama dengan saat melatih (1.8.0).")
        st.stop()

    tab_rec, tab_up = st.tabs(["Rekam suara", "Upload file"])
    raw, name = None, None

    with tab_rec:
        st.caption("Rekam sekitar 30 detik suasana kelas untuk hasil terbaik.")
        if hasattr(st, "audio_input"):
            rec = st.audio_input("Klik untuk mulai merekam")
            if rec is not None:
                raw, name = rec.getvalue(), "rekaman.wav"
        else:
            st.warning("Versi Streamlit ini belum mendukung perekam. Perbarui dengan `pip install -U streamlit`.")

    with tab_up:
        up = st.file_uploader("Pilih file audio (format apa pun, mis. MP3, WAV, M4A, OGG)", type=AUDIO_TYPES)
        if up is not None:
            raw, name = up.getvalue(), up.name

    if raw is None:
        st.info("Belum ada audio. Rekam atau unggah file untuk mulai.")
        return

    try:
        analyze(raw, name, model)
    except Exception as exc:
        st.error(f"Gagal memproses audio: {exc}")


if __name__ == "__main__":
    main()