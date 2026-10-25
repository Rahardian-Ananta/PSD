## 2. Prapemrosesan dan ekstraksi fitur identik Tahap 03

Deployment hanya benar bila file masuk diproses persis seperti data latih. Bagian ini mendefinisikan fungsi-fungsi berikut dengan rumus dan parameter yang sama persis dengan Tahap 03:

1. **Dekode** — `librosa.load(path, sr=16000, mono=True)`, sama seperti kontrak `preprocessing_contract.json`.
2. **Penyesuaian durasi** — crop tengah bila lebih panjang, zero-pad tengah bila lebih pendek, target tepat 480.000 sampel.
3. **Peak normalization** — `y / max(|y|) * 1.0` setelah crop/pad, hasil di-cast `float32`; sinyal dengan peak nol ditolak, bukan dinormalisasi.
4. **Ekstraksi 12 fitur** — framing `frame_length=400`, `hop=160` tanpa `center`, window Hann simetris, rFFT 512 titik, daya `P = |S|^2`, epsilon `np.finfo(np.float64).eps`, rolloff 0,85; seluruh formula disalin apa adanya dari sel Tahap 03.

Setiap fitur dihitung dari sinyal yang sama dengan yang dipakai `features.csv`, termasuk perlakuan frame daya nol (centroid, flatness, rolloff, dan bandwidth frame tersebut ditetapkan 0). Kelas `predict_audio` berikutnya membungkus fungsi-fungsi ini.
