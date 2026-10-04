import json

d = json.load(open("04_feature_extraction/4.2_ekstraksi_fitur_tsfel.ipynb", encoding="utf-8"))
print("cells:", len(d["cells"]))
for n, c in enumerate(d["cells"]):
    src = "".join(c["source"])
    tag = "CODE" if c["cell_type"] == "code" else "MD  "
    print(f"--- {tag}[{n}] ({len(src)} char): {src[:400]}")
    print()
