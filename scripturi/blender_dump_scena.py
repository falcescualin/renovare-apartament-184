"""Rulează: blender --background <fișier.blend> --python blender_dump_scena.py -- <ieșire.json>
Scrie lista obiectelor mesh din scenă: nume, part_id, colecție, vizibil la randare, gabarit global (mm), număr de
vârfuri, materiale. Folosit de compara_freecad_blender.py ca să vadă ce e diferit față de exportul din FreeCAD."""
import bpy, sys, json
from mathutils import Vector

out = sys.argv[sys.argv.index('--') + 1]
rows = []
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    mn = [min(p[i] for p in pts) * 1000 for i in range(3)]
    mx = [max(p[i] for p in pts) * 1000 for i in range(3)]
    rows.append(dict(name=o.name, part_id=o.get('part_id', ''), source_document=o.get('source_document', ''),
                     collection=o.users_collection[0].name if o.users_collection else '', hide_render=o.hide_render,
                     bbox_min=[round(v, 2) for v in mn], bbox_max=[round(v, 2) for v in mx], verts=len(o.data.vertices),
                     materials=[m.name for m in o.data.materials if m]))
json.dump(dict(file=bpy.data.filepath, objects=rows), open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('DUMP_OK', len(rows))
