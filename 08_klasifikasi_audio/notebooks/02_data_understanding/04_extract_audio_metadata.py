# Tujuan: membaca metadata dan statistik sinyal dasar dari setiap file audio mentah.
# Proses: membuka file dengan soundfile, membaca seluruh sampel, menghitung durasi, sample rate, channel, peak, RMS, dan pemeriksaan NaN/Inf.
# Output: tabel metadata per file dan ringkasan kualitas pembacaan.

metadata_rows = []

for row in inventory.itertuples(index=False):
    path = RAW_DIR / row.relative_path
    record = {
        "relative_path": row.relative_path,
        "read_ok": False,
        "read_error": "",
    }

    try:
        info = sf.info(str(path))
        data, samplerate = sf.read(str(path), dtype="float32", always_2d=True)
        data_float = data.astype(np.float64)

        peak_abs = float(np.max(np.abs(data_float))) if data_float.size else 0.0
        rms = float(np.sqrt(np.mean(np.square(data_float)))) if data_float.size else 0.0
        zero_fraction = float(np.mean(data_float == 0.0)) if data_float.size else 1.0

        record.update(
            {
                "read_ok": True,
                "format": info.format,
                "subtype": info.subtype,
                "samplerate": int(info.samplerate),
                "channels": int(info.channels),
                "frames": int(info.frames),
                "duration_info_s": float(info.duration),
                "decoded_frames": int(data.shape[0]),
                "duration_decoded_s": float(data.shape[0] / samplerate),
                "peak_abs": peak_abs,
                "rms": rms,
                "zero_fraction": zero_fraction,
                "nan_count": int(np.isnan(data_float).sum()),
                "inf_count": int(np.isinf(data_float).sum()),
                "bitrate_kbps_estimate": float(row.size_bytes * 8 / info.duration / 1000) if info.duration > 0 else np.nan,
                "peak_over_one": bool(peak_abs > 1.0),
            }
        )
    except Exception as exc:
        record["read_error"] = f"{type(exc).__name__}: {exc}"

    metadata_rows.append(record)

audio_metadata = pd.DataFrame(metadata_rows)

read_summary = pd.DataFrame(
    {
        "pemeriksaan": [
            "file berhasil dibaca",
            "file gagal dibaca",
            "file dengan NaN",
            "file dengan Inf",
            "file dengan peak > 1.0",
        ],
        "jumlah": [
            int(audio_metadata["read_ok"].sum()),
            int((~audio_metadata["read_ok"]).sum()),
            int((audio_metadata["nan_count"] > 0).sum()),
            int((audio_metadata["inf_count"] > 0).sum()),
            int(audio_metadata["peak_over_one"].fillna(False).sum()),
        ],
    }
)

display(read_summary)
display(
    audio_metadata[
        ["duration_decoded_s", "samplerate", "channels", "peak_abs", "rms", "bitrate_kbps_estimate"]
    ].describe().T
)
display(audio_metadata["samplerate"].value_counts().rename_axis("samplerate").reset_index(name="jumlah"))
display(audio_metadata["channels"].value_counts().rename_axis("channels").reset_index(name="jumlah"))

failed = audio_metadata.loc[~audio_metadata["read_ok"], ["relative_path", "read_error"]]
if len(failed):
    display(failed)
else:
    print("Tidak ada file yang gagal dibaca.")

audio_metadata.to_csv(ARTIFACT_DIR / "audio_metadata.csv", index=False)
print(f"Metadata disimpan: {ARTIFACT_DIR / 'audio_metadata.csv'} ({len(audio_metadata)} baris)")
