def frame_signal(y, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH):
    y = np.asarray(y)
    if len(y) < frame_length:
        raise ValueError("Sinyal lebih pendek dari satu frame.")
    frames = np.lib.stride_tricks.sliding_window_view(y, frame_length)[::hop_length]
    return frames


example_row = transformation_manifest.sort_values("final_relative_path").iloc[0]
example_path = DATA_FINAL_DIR / example_row["final_relative_path"]
example_y, example_sr = sf.read(example_path, dtype="float32")

if len(example_y) != TARGET_SAMPLES or example_sr != SR:
    raise ValueError("File contoh tidak sesuai kontrak 16 kHz / 480.000 sampel.")

example_frames = frame_signal(example_y)
expected_frames = 1 + (len(example_y) - FRAME_LENGTH) // HOP_LENGTH

if example_frames.shape != (expected_frames, FRAME_LENGTH):
    raise ValueError("Bentuk frame tidak sesuai rumus jumlah frame.")

last_covered_sample = (example_frames.shape[0] - 1) * HOP_LENGTH + FRAME_LENGTH - 1
uncovered_samples = len(example_y) - last_covered_sample - 1

display(
    pd.DataFrame(
        {
            "besaran": [
                "file contoh",
                "panjang sinyal N",
                "frame length L",
                "hop H",
                "jumlah frame aktual",
                "jumlah frame rumus",
                "bentuk matriks frame",
                "sampel terakhir yang tercakup",
                "sampel tidak tercakup",
            ],
            "nilai": [
                example_row["file"],
                len(example_y),
                FRAME_LENGTH,
                HOP_LENGTH,
                example_frames.shape[0],
                expected_frames,
                str(example_frames.shape),
                last_covered_sample,
                uncovered_samples,
            ],
        }
    )
)
