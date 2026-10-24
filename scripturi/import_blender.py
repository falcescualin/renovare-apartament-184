"""Ruleaza cu: blender --background --python import_blender.py
Importa bundle-ul OBJ + manifest exportat din FreeCAD si salveaza apartament_184.blend."""
import bpy, json, os, sys

BASE = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
BUNDLE = os.path.join(BASE, "blender_export")
OUT_BLEND = os.path.join(BASE, "apartament_184.blend")

# scena goala
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

with open(os.path.join(BUNDLE, "furniture_manifest.json"), encoding="utf-8") as f:
    manifest = json.load(f)


def ensure_collection(name, parent):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if col.name not in parent.children:
        parent.children.link(col)
    return col


root = ensure_collection("APARTAMENT_184", scene.collection)
hidden_col = ensure_collection("ASCUNSE_IN_FREECAD", root)
materials = {}


def material_for(rgb, transp):
    key = (tuple(round(c, 3) for c in rgb), transp)
    if key in materials:
        return materials[key]
    name = "FC_%02x%02x%02x_t%d" % (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), transp)
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Roughness"].default_value = 0.5
    if transp > 0:
        bsdf.inputs["Alpha"].default_value = max(0.05, 1.0 - transp / 100.0)
        try:
            mat.blend_method = 'BLEND'
        except Exception:
            pass
    mat.diffuse_color = (rgb[0], rgb[1], rgb[2], max(0.05, 1.0 - transp / 100.0))
    materials[key] = mat
    return mat


errors, imported = [], []
for rec in manifest["parts"]:
    path = os.path.join(BUNDLE, rec["mesh_file"])
    before = set(bpy.data.objects)
    # FreeCAD este Z-up, in mm: pastram axele asa cum sunt
    bpy.ops.wm.obj_import(filepath=path, forward_axis='Y', up_axis='Z')
    new = [o for o in set(bpy.data.objects) - before if o.type == 'MESH']
    if len(new) != 1:
        errors.append({"part_id": rec["part_id"], "error": "obiecte importate: %d" % len(new)})
        continue
    obj = new[0]
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    if rec.get("hidden"):
        target = hidden_col
    else:
        target = ensure_collection(rec["assembly"][:60], root)
    target.objects.link(obj)
    obj.name = rec["part_id"][:63]
    obj.data.name = obj.name
    # mm -> m, o singura data, apoi aplicam scara
    obj.scale = (0.001, 0.001, 0.001)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.select_set(False)
    obj.data.materials.clear()
    obj.data.materials.append(material_for(rec["color_rgb"], rec.get("transparency", 0)))
    for k in ("part_id", "source_document", "source_object", "label", "assembly"):
        obj[k] = rec.get(k, "")
    obj["manufactured_part"] = True
    if rec.get("hidden"):
        obj.hide_render = True
        obj.hide_set(True)
    exp = sorted(float(v) for v in rec["bbox_mm"])
    act = sorted(d * 1000 for d in obj.dimensions)
    if any(abs(a - b) > 0.5 for a, b in zip(exp, act)):
        errors.append({"part_id": rec["part_id"], "expected_mm": exp, "actual_mm": [round(a, 2) for a in act]})
    imported.append(obj.name)

root["source_manifest"] = os.path.join(BUNDLE, "furniture_manifest.json")
root["import_errors_json"] = json.dumps(errors)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
report = {"imported": len(imported), "intended": manifest["intended_part_count"],
          "errors": errors[:20], "error_count": len(errors), "materials": len(materials),
          "collections": [c.name for c in root.children]}
with open(os.path.join(BUNDLE, "import_report.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("IMPORT_REPORT", json.dumps(report, ensure_ascii=False))
