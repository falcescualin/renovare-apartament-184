"""Rulează: blender --background apartament_184_randare.blend --python oglinda_led_laterale_blender.py
Oglinda de machiaj din dormitor, la fel ca în FreeCAD (06.10.2026): LED-ul nu mai e o placă în spatele oglinzii,
ci bandă pe laterale. Placa din spate e scoasă din randare (păstrată ascunsă), se adaugă banda dinspre fereastră
(profil 16 mm, de la blat la tavan, la 3 mm de oglindă), cu același material ca banda riflajelor. Salvează .blend
(copia de dinainte în _arhiva/2026-10-06_oglinda_machiaj). Afișează camerele în care se vede banda nouă."""
import bpy, bmesh, os, shutil
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

ROOT = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
bak = os.path.join(ROOT, '_arhiva', '2026-10-06_oglinda_machiaj', 'apartament_184_randare_inainte.blend')
if not os.path.exists(bak):
    shutil.copy2(bpy.data.filepath, bak)

P = 'Perete_TV_dormitor_custom__'
col = bpy.data.collections['Perete_TV_dormitor_custom']
mir = bpy.data.objects[P + 'Machiaj_oglinda_LED']
back = bpy.data.objects[P + 'Machiaj_LED_spate_oglinda']
ref = bpy.data.objects[P + 'LED_vertical_margine_riflaje']

back.hide_render = True
back.hide_viewport = True
back['inlocuit'] = '06.10.2026: LED pe laterale, nu în spatele oglinzii'

name = P + 'Machiaj_LED_lateral_fereastra'
side = bpy.data.objects.get(name)
if side is None:
    me = bpy.data.meshes.new(name)
    side = bpy.data.objects.new(name, me)
    col.objects.link(side)
# x 3525–3550, y -357…-341, z 755–2495 mm (coordonate FreeCAD = Blender × 1000)
x0, x1, y0, y1, z0, z1 = 3.525, 3.550, -0.357, -0.341, 0.755, 2.495
bm = bmesh.new()
vs = [bm.verts.new((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
    bm.faces.new([vs[i] for i in f])
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(side.data)
bm.free()
side.data.materials.clear()
for m in ref.data.materials:
    side.data.materials.append(m)
for k in ref.keys():
    if k not in ('_RNA_UI',):
        side[k] = ref[k]
side['part_id'] = 'Machiaj_LED_lateral_fereastra'
side['source_object'] = 'Machiaj_LED_lateral_fereastra'
print('MAT', [m.name for m in side.data.materials], 'oglinda', [m.name for m in mir.data.materials])

# camerele în care se vede banda nouă sau oglinda
sc = bpy.context.scene
pts = [Vector(((x0 + x1) / 2, (y0 + y1) / 2, z)) for z in (0.9, 1.6, 2.3)] + [Vector((3.525, -0.76, 1.6))]
for cam in bpy.data.collections['CAMERE'].objects:
    vis = []
    for p in pts:
        c = world_to_camera_view(sc, cam, p)
        vis.append(0 <= c.x <= 1 and 0 <= c.y <= 1 and c.z > 0)
    if any(vis):
        print('VEDE', cam.name, vis)
bpy.ops.wm.save_mainfile()
print('OGLINDA_OK')
