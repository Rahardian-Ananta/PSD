overlap_samples = FRAME_LENGTH - HOP_LENGTH
overlap_ratio = overlap_samples / FRAME_LENGTH
overlap_ms = overlap_samples / SR * 1000
hop_ms = HOP_LENGTH / SR * 1000

actual_overlap_matches = np.array_equal(
    example_frames[0, HOP_LENGTH:],
    example_frames[1, :FRAME_LENGTH - HOP_LENGTH],
)
if not actual_overlap_matches:
    raise ValueError("Frame berurutan tidak memiliki overlap yang diharapkan.")

display(
    pd.DataFrame(
        {
            "besaran": [
                "frame length",
                "hop",
                "overlap sampel",
                "overlap rasio",
                "overlap ms",
                "hop ms",
                "overlap frame 0 dan 1 identik",
            ],
            "nilai": [
                FRAME_LENGTH,
                HOP_LENGTH,
                overlap_samples,
                overlap_ratio,
                overlap_ms,
                hop_ms,
                actual_overlap_matches,
            ],
        }
    )
)
