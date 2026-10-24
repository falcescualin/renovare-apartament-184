"""Rulează: blender --background apartament_184_randare.blend --python sincronizare_freecad_blender.py
Aduce în scena de randare diferențele găsite de compara_freecad_blender.py (tmp/diferente_freecad_blender.json),
fără să atingă camerele, luminile, materialele de randare sau decorul:
- piese noi în FreeCAD → importate din blender_export_2026-10-06, cu materialul pieselor similare din scenă;
- piese cu geometrie schimbată → li se înlocuiește doar plasa (mesh), materialele rămân;
- piese scoase / ascunse în FreeCAD → ascunse la randare (nu se șterg).
Salvează .blend, cu copie înainte în _arhiva/2026-10-06_sincronizare_freecad."""
import bpy, json, os, shutil

ROOT = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
BUNDLE = os.path.join(ROOT, "blender_export_2026-10-06")
DIF = json.load(open(os.path.join(ROOT, "tmp", "diferente_freecad_blender.json"), encoding="utf-8"))
MAN = {p["part_id"][:63]: p for p in json.load(open(os.path.join(BUNDLE, "furniture_manifest.json"), encoding="utf-8"))["parts"]}
bak = os.path.join(ROOT, "_arhiva", "2026-10-06_sincronizare_freecad", "apartament_184_randare_inainte.blend")
os.makedirs(os.path.dirname(bak), exist_ok=True)
if not os.path.exists(bak):
    shutil.copy2(bpy.data.filepath, bak)


def import_obj(pid):
    rec = MAN[pid]
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=os.path.join(BUNDLE, rec["mesh_file"]), forward_axis='Y', up_axis='Z')
    new = [o for o in set(bpy.data.objects) - before if o.type == 'MESH']
    assert len(new) == 1, (pid, len(new))
    o = new[0]
    o.scale = (0.001, 0.001, 0.001)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.select_set(False)
    return o, rec


def material_for(name):
    """materialul pieselor de același fel deja din scenă"""
    if "port" in name:
        return bpy.data.materials.get("FC_1f2429_t0")           # port negru, ca la modulele TV
    if any(k in name for k in ("Schuko", "RJ45", "Priza", "Intrerupator")):
        return bpy.data.materials.get("R_Egger_W1000_ST9_alb")  # ramă albă, ca restul aparatajului
    return None


log = []
for r in DIF["noi_in_freecad"]:
    pid = r["id"]
    if bpy.data.objects.get(pid):
        continue
    o, rec = import_obj(pid)
    for c in list(o.users_collection):
        c.objects.unlink(o)
    col = bpy.data.collections.get("Electric") if any(k in pid for k in ("Schuko", "RJ45", "Priza")) else None
    if col is None:
        col = bpy.data.collections.get(rec["assembly"][:60]) or bpy.data.collections.new(rec["assembly"][:60])
        if col.name not in bpy.data.collections["APARTAMENT_184"].children:
            bpy.data.collections["APARTAMENT_184"].children.link(col)
    col.objects.link(o)
    o.name = pid
    o.data.name = pid
    o.data.materials.clear()
    m = material_for(pid)
    if m:
        o.data.materials.append(m)
    for k in ("part_id", "source_document", "source_object", "label", "assembly"):
        o[k] = rec.get(k, "")
    o["manufactured_part"] = True
    log.append(("nou", pid, col.name, m.name if m else None))

for r in DIF["geometrie_diferita"]:
    pid = r["id"]
    tgt = bpy.data.objects.get(pid)
    if tgt is None:
        continue
    o, rec = import_obj(pid)
    mats = list(tgt.data.materials)
    old = tgt.data
    tgt.data = o.data
    tgt.data.materials.clear()
    for m in mats:
        tgt.data.materials.append(m)
    bpy.data.objects.remove(o)
    tgt.data.name = pid
    log.append(("geometrie", pid, r["diferenta_mm"]))

for r in DIF["scoase_din_freecad"]:
    o = bpy.data.objects.get(r["id"])
    if o is not None and not o.hide_render:
        o.hide_render = True
        o.hide_set(True)
        log.append(("ascuns", r["id"]))

bpy.ops.wm.save_mainfile()
for x in log:
    print("SYNC", x)
print("SYNC_OK", len(log))
