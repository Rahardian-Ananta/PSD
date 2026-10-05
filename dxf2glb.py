"""Konversi MESH DXF kampus -> data/3d_model/kampus.glb (interaktif via model-viewer).
DXF Z-up (x,y,z) -> glTF Y-up (x,z,-y). Normal flat per segitiga."""
import ezdxf
import numpy as np
from pygltflib import (GLTF2, Accessor, Asset, Buffer, BufferView, Material,
                       Mesh, Node, Primitive, Scene)

LAYER_COLORS = {
    "TPX_BUILDINGS": (0.35, 0.55, 0.75, 1.0),
    "TPX_ROADS_HATCH": (0.25, 0.25, 0.28, 1.0),
    "TPX_VEGETATION_GREEN_SPACES_HATCH": (0.30, 0.60, 0.32, 1.0),
    "TPX_TERRAIN_TERRAIN_MESH": (0.62, 0.58, 0.42, 1.0),
}

doc = ezdxf.readfile("data/3d_model/topoexport_3D_modeling.dxf")
msp = doc.modelspace()

tris_by_layer = {}
for e in msp:
    if e.dxftype() != "MESH":
        continue
    verts = [tuple(v) for v in e.vertices]
    for f in e.faces:
        idx = list(f)
        if len(idx) < 3:
            continue
        v0 = verts[idx[0]]
        for j in range(1, len(idx) - 1):  # fan triangulation
            tris_by_layer.setdefault(e.dxf.layer, []).append(
                (verts[idx[0]], verts[idx[j]], verts[idx[j + 1]]))

gltf = GLTF2()
gltf.asset = Asset(version="2.0", generator="psd-dxf2glb")
blob = bytearray()
scene = Scene(nodes=[])
total_tri = 0
for li, (layer, tris) in enumerate(sorted(tris_by_layer.items())):
    pos = np.array(
        [[x, z, -y] for tri in tris for (x, y, z) in tri], dtype=np.float32)
    ntri = len(tris)
    p0, p1, p2 = pos[0::3], pos[1::3], pos[2::3]
    n = np.cross(p1 - p0, p2 - p0)
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    ln[ln == 0] = 1.0
    n = (n / ln).astype(np.float32)
    nrm = np.repeat(n, 3, axis=0)
    idx = np.arange(len(pos), dtype=np.uint32)
    total_tri += ntri
    for arr, ctype, ncomp in ((pos, 5126, 3), (nrm, 5126, 3), (idx, 5125, 1)):
        off = len(blob)
        raw = arr.tobytes()
        blob += raw
        gltf.bufferViews.append(BufferView(
            buffer=0, byteOffset=off, byteLength=len(raw)))
        amin = arr.min(axis=0).tolist() if ncomp > 1 else [float(arr.min())]
        amax = arr.max(axis=0).tolist() if ncomp > 1 else [float(arr.max())]
        gltf.accessors.append(Accessor(
            bufferView=len(gltf.bufferViews) - 1, componentType=ctype,
            count=len(arr), type="VEC3" if ncomp == 3 else "SCALAR",
            min=amin, max=amax))
    (r, gg, bb, aa) = LAYER_COLORS.get(layer, (0.6, 0.6, 0.6, 1.0))
    gltf.materials.append(Material(
        pbrMetallicRoughness={"baseColorFactor": [r, gg, bb, aa],
                              "metallicFactor": 0.0, "roughness": 0.9},
        doubleSided=True, name=layer))
    base = li * 3
    gltf.meshes.append(Mesh(primitives=[Primitive(
        attributes={"POSITION": base, "NORMAL": base + 1},
        indices=base + 2, material=li, mode=4)]))
    gltf.nodes.append(Node(mesh=li, name=layer))
    scene.nodes.append(li)

gltf.scenes.append(scene)
gltf.scene = 0
gltf.buffers.append(Buffer(byteLength=len(blob)))
gltf.set_binary_blob(bytes(blob))
gltf.save("data/3d_model/kampus.glb")

# verifikasi: baca ulang + cocokkan jumlah segitiga & bounds
chk = GLTF2().load("data/3d_model/kampus.glb")
n_acc_tri = sum(a.count // 3 for a in chk.accessors
                if a.type == "SCALAR" and a.componentType == 5125)
print(f"layer: {sorted(tris_by_layer)} | segitiga DXF={total_tri} vs GLB={n_acc_tri}")
pa = chk.accessors[0]
print("bounds GLB:", [round(v, 1) for v in pa.min], [round(v, 1) for v in pa.max])
import os
print("ukuran:", round(os.path.getsize("data/3d_model/kampus.glb") / 1024), "KB")
assert total_tri == n_acc_tri
print("GLB VALID")
