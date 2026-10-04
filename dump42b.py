import json

d = json.load(open("04_feature_extraction/4.2_ekstraksi_fitur_tsfel.ipynb", encoding="utf-8"))
for n in [4, 6, 14]:
    print("=" * 25, f"CELL {n}")
    print("".join(d["cells"][n]["source"]))
    print()
