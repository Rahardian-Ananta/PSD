FREQS = np.fft.rfftfreq(N_FFT, d=1 / SR)
HANN_WINDOW = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(FRAME_LENGTH) / (FRAME_LENGTH - 1))
if not np.allclose(HANN_WINDOW, np.hanning(FRAME_LENGTH), atol=1e-15):
    raise ValueError("Window Hann tidak sesuai definisi simetris.")


def fit_duration_to_target(y, target_samples=TARGET_SAMPLES):
    y = np.asarray(y)
    original_samples = int(len(y))
    crop_start = 0
    pad_left = 0
    pad_right = 0

    if original_samples > target_samples:
        action = "crop"
        crop_start = (original_samples - target_samples) // 2
        y_out = y[crop_start : crop_start + target_samples].copy()
    elif original_samples < target_samples:
        action = "pad"
        total_pad = target_samples - original_samples
        pad_left = total_pad // 2
        pad_right = total_pad - pad_left
        y_out = np.pad(y, (pad_left, pad_right), mode="constant", constant_values=0.0)
    else:
        action = "none"
        y_out = y.copy()

    if len(y_out) != target_samples:
        raise ValueError("Panjang sinyal tidak sama dengan target sampel.")

    return y_out, {
        "original_samples_16k": original_samples,
        "original_duration_16k_s": original_samples / SR,
        "action": action,
        "crop_start": int(crop_start),
        "pad_left": int(pad_left),
        "pad_right": int(pad_right),
        "final_samples": int(len(y_out)),
    }


def peak_normalize(y, target_peak=TARGET_PEAK):
    y = np.asarray(y)
    if y.size == 0:
        raise ValueError("Sinyal kosong tidak dapat dinormalisasi.")
    if not np.isfinite(y).all():
        raise ValueError("Sinyal mengandung NaN atau Inf.")
    peak_before = float(np.max(np.abs(y)))
    if peak_before <= 0:
        raise ValueError("Peak sinyal nol; file harus ditolak, bukan dinormalisasi.")
    y_norm = (y / peak_before * target_peak).astype(np.float32)
    peak_after = float(np.max(np.abs(y_norm)))
    return y_norm, {
        "peak_before": peak_before,
        "peak_after": peak_after,
        "target_peak": float(target_peak),
    }


def frame_signal(y, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH):
    y = np.asarray(y)
    if len(y) < frame_length:
        raise ValueError("Sinyal lebih pendek dari satu frame.")
    frames = np.lib.stride_tricks.sliding_window_view(y, frame_length)[::hop_length]
    return frames


def extract_features(y):
    y = np.asarray(y)
    if len(y) != TARGET_SAMPLES:
        raise ValueError(f"Fitur hanya boleh dihitung dari {TARGET_SAMPLES} sampel.")
    if not np.isfinite(y).all():
        raise ValueError("Sinyal mengandung NaN atau Inf.")

    features = {"mse_energy": float(np.mean(y.astype(np.float64) ** 2))}

    frames = frame_signal(y).astype(np.float64)
    rms_frames = np.sqrt(np.mean(frames**2, axis=1))
    zcr_frames = np.mean((frames[:, :-1] * frames[:, 1:]) < 0, axis=1)

    P = np.abs(np.fft.rfft(frames * HANN_WINDOW[None, :], n=N_FFT, axis=1)) ** 2
    power_sum = P.sum(axis=1)
    centroids = np.divide(
        P @ FREQS,
        power_sum,
        out=np.zeros_like(power_sum),
        where=power_sum > 0,
    )

    P_eps = P + EPS
    flatness_frames = np.exp(np.mean(np.log(P_eps), axis=1)) / np.mean(P_eps, axis=1)
    flatness_frames[P.sum(axis=1) == 0] = 0

    cumulative = np.cumsum(P, axis=1)
    total_power = cumulative[:, -1]
    thresholds = ROLLOFF_PERCENT * total_power
    rolloff_indices = np.argmax(cumulative >= thresholds[:, None], axis=1)
    rolloff_frames = FREQS[rolloff_indices].copy()
    rolloff_frames[total_power == 0] = 0

    variance = np.divide(
        (P * (FREQS[None, :] - centroids[:, None]) ** 2).sum(axis=1),
        power_sum,
        out=np.zeros_like(power_sum),
        where=power_sum > 0,
    )
    bandwidth_frames = np.sqrt(np.maximum(variance, 0))

    features.update(
        {
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
        }
    )

    if list(features) != FEATURE_COLUMNS:
        raise ValueError(f"Urutan fitur berubah: {list(features)}")
    if not all(np.isfinite(value) for value in features.values()):
        raise ValueError("Fitur mengandung NaN atau Inf.")
    return features


definition_table = pd.DataFrame(
    {
        "langkah": [
            "dekode",
            "durasi",
            "normalisasi",
            "frame",
            "window",
            "fft",
            "jumlah fitur",
        ],
        "definisi": [
            contract["decode"],
            f"crop/pad tengah ke {TARGET_SAMPLES} sampel",
            contract["peak_normalization"],
            f"frame_length={FRAME_LENGTH}, hop_length={HOP_LENGTH}, tanpa center",
            "Hann simetris L=400",
            f"rfft n={N_FFT} ({FREQS.size} bin, resolusi {SR / N_FFT:.2f} Hz)",
            len(FEATURE_COLUMNS),
        ],
    }
)
display(definition_table)
print("Fungsi prapemrosesan dan ekstraksi fitur siap.")
