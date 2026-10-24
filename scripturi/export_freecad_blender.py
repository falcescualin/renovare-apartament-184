"""Ruleaza in FreeCAD. Exporta apartamentul (inclusiv componentele legate) ca OBJ per piesa + manifest JSON.

Fiecare piesa vizibila devine un OBJ in coordonate globale (mm). Componentele importate prin App::Link
(dulap, bucatarie, debara, dressing, baie etc.) sunt parcurse recursiv, cu plasarea link-ului aplicata.
"""
import FreeCAD as App
import MeshPart
import json, math, os, re
from datetime import datetime, timezone

OUT_DIR = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\blender_export"
LINEAR_DEFLECTION_MM = 0.5
ANGULAR_DEFLECTION_DEG = 10.0
INCLUDE_HIDDEN = {"Balcon_tavan"}          # ascuns in FreeCAD, dar util la randare (marcat hidden)


def safe_id(value):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_") or "PART"


def visible(o):
    try:
        return bool(o.ViewObject.Visibility)
    except Exception:
        return True


def color_of(o):
    try:
        c = o.ViewObject.ShapeColor
        t = o.ViewObject.Transparency
        return [round(c[0], 4), round(c[1], 4), round(c[2], 4)], int(t)
    except Exception:
        return [0.8, 0.8, 0.8], 0


def parent_group(o):
    for p in o.InList:
        if p.TypeId in ("App::DocumentObjectGroup", "App::Part"):
            return p.Label
    return "Structura"


def leaves(container):
    """Toate piesele cu solide dintr-un App::Part, recursiv."""
    out = []
    for c in getattr(container, "Group", []):
        if c.TypeId in ("App::Part", "App::DocumentObjectGroup"):
            if visible(c):
                out += leaves(c)
        elif hasattr(c, "Shape") and not c.Shape.isNull() and c.Shape.Solids and visible(c):
            out.append(c)
    return out


def collect(doc):
    items = []   # (part_id, obj, global_placement, assembly, hidden)
    for o in doc.Objects:
        if o.TypeId == "App::Link":
            if not visible(o) or o.LinkedObject is None:
                continue
            seen = set()
            for c in leaves(o.LinkedObject):
                if c.Name in seen:          # aceeasi piesa referita din doua grupuri
                    continue
                seen.add(c.Name)
                pl = o.Placement.multiply(c.getGlobalPlacement())
                items.append((safe_id(o.Name + "__" + c.Name), c, pl, o.Name, False))
            continue
        if o.TypeId in ("App::Part", "App::DocumentObjectGroup"):
            continue
        if not hasattr(o, "Shape") or o.Shape.isNull() or not o.Shape.Solids:
            continue
        hidden = not visible(o)
        if hidden and o.Name not in INCLUDE_HIDDEN:
            continue
        items.append((safe_id(o.Name), o, o.getGlobalPlacement(), parent_group(o), hidden))
    return items


def export_bundle(doc, out_dir=OUT_DIR, start=0, count=None):
    os.makedirs(out_dir, exist_ok=True)
    items = collect(doc)
    ids = [i[0] for i in items]
    dup = {x for x in ids if ids.count(x) > 1}
    if dup:
        raise RuntimeError("part_id duplicate: %s" % sorted(dup))
    end = len(items) if count is None else min(len(items), start + count)
    records = []
    for pid, obj, pl, asm, hidden in items[start:end]:
        shape = obj.Shape.copy()
        shape.Placement = pl
        mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=LINEAR_DEFLECTION_MM,
                                      AngularDeflection=math.radians(ANGULAR_DEFLECTION_DEG), Relative=False)
        fn = pid + ".obj"
        mesh.write(os.path.join(out_dir, fn))
        bb = shape.BoundBox
        rgb, transp = color_of(obj)
        records.append({
            "part_id": pid, "source_document": obj.Document.Name, "source_object": obj.Name,
            "label": obj.Label, "mesh_file": fn, "assembly": asm, "hidden": hidden,
            "global_matrix": [float(pl.toMatrix().A[i]) for i in range(16)],
            "bbox_mm": [bb.XLength, bb.YLength, bb.ZLength],
            "bbox_min_mm": [bb.XMin, bb.YMin, bb.ZMin],
            "color_rgb": rgb, "transparency": transp,
            "material_brand": "", "decor_code": "", "decor_name": "", "grain_axis": "",
        })
    return records, len(items)


def write_manifest(doc, records, out_dir=OUT_DIR):
    manifest = {"schema": "freecad-blender-furniture/1.0", "document": doc.Name,
                "freecad_version": ".".join(map(str, App.Version()[:3])),
                "created_utc": datetime.now(timezone.utc).isoformat(), "units": "mm",
                "linear_deflection_mm": LINEAR_DEFLECTION_MM, "angular_deflection_deg": ANGULAR_DEFLECTION_DEG,
                "intended_part_count": len(records), "parts": records}
    with open(os.path.join(out_dir, "furniture_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest
