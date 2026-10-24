"""Importa modelele CAD (tmp/feronerie_R2/obj/*.obj, mm) in Blender, le randeaza (Cycles, fundal transparent) si salveaza biblioteca .blend.
Rulare:  blender --background --python feronerie_blender_R2.py -- [id ...]
Iese: tmp/feronerie_R2/png/<id>.png, ansambluri (balama_ansamblu.png), feronerie_3d.blend (obiecte HW_<id>, mesh in mm, scala obiect 0.001)."""
import bpy, sys, os, json, math
from mathutils import Vector, Matrix

ROOT = r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14'
sys.path.insert(0, os.path.join(ROOT, 'scripturi'))
from feronerie_catalog import CATALOG, COL, METAL

D = os.path.join(ROOT, 'tmp', 'feronerie_R2')
PNG = os.path.join(D, 'png')
os.makedirs(PNG, exist_ok=True)
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ONLY = set(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
MATS = {}


def mat(c):
    if c in MATS:
        return MATS[c]
    m = bpy.data.materials.new('HW_' + c)
    r, g, b = [((v + 0.055) / 1.055) ** 2.4 for v in COL[c]]          # culorile din catalog sunt sRGB -> liniar
    m.diffuse_color = (r, g, b, 1)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (r, g, b, 1)
    met = c in METAL
    bs.inputs['Metallic'].default_value = 1.0 if met else 0.0
    bs.inputs['Roughness'].default_value = {'crom': 0.12, 'inox': 0.25, 'nichel': 0.22, 'zinc': 0.32, 'zinc_galben': 0.30, 'otel': 0.38,
                                             'magnet': 0.45, 'lemn': 0.65, 'negru': 0.45}.get(c, 0.5)
    if not met:
        bs.inputs['Roughness'].default_value = max(bs.inputs['Roughness'].default_value, 0.62)
        try:
            bs.inputs['Specular IOR Level'].default_value = 0.22
        except Exception:
            pass
    m.metallic = 1.0 if met else 0.0
    m.roughness = bs.inputs['Roughness'].default_value
    MATS[c] = m
    return m


def import_model(mid):
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=os.path.join(D, 'obj', mid + '.obj'), forward_axis='Y', up_axis='Z', global_scale=1.0)
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        for slot in o.material_slots:
            nm = slot.material.name.split('.')[0] if slot.material else 'zinc'
            old = slot.material
            slot.material = mat(nm if nm in COL else 'zinc')
            if old and old.users == 0:
                bpy.data.materials.remove(old)
    bpy.ops.object.select_all(action='DESELECT')
    for o in new:
        o.select_set(True)
    bpy.context.view_layer.objects.active = new[0]
    if len(new) > 1:
        bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active
    o.name = 'HW_' + mid
    o.data.name = 'HW_' + mid
    o.data.shade_smooth()
    try:
        o.data.set_sharp_from_angle(angle=math.radians(32))
    except Exception:
        pass
    o.scale = (0.001,) * 3
    return o


# --------------------------------------------------------------- scena de randare
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 64
sc.cycles.use_denoising = True
sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y = 1000, 720
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast'
sc.view_settings.exposure = 0.0
w = bpy.data.worlds.new('w'); sc.world = w
w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.62, 0.64, 0.67, 1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.30
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); cd.type = 'ORTHO'; sc.camera = cam
DIRV = Vector((0.9, -1.0, 0.75)).normalized()
rig = []
for nm, loc, en, sz in (('key', (0.6, -0.9, 1.2), 900, 0.8), ('fill', (-1.1, -0.6, 0.5), 300, 1.2), ('rim', (-0.4, 1.0, 0.9), 450, 0.6)):
    ld = bpy.data.lights.new(nm, 'AREA'); ld.energy = en; ld.size = sz
    lo = bpy.data.objects.new(nm, ld); sc.collection.objects.link(lo); rig.append((lo, Vector(loc)))


def frame(objs, d=DIRV, pad=1.18, ratio=1000 / 720):
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    cen = sum(pts, Vector()) / len(pts)
    rad = max((p - cen).length for p in pts)
    cam.location = cen + d * (rad * 6 + 0.5)
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    cd.clip_end = rad * 20 + 5
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    xs = [(inv @ p).x for p in pts]; ys = [(inv @ p).y for p in pts]
    cd.ortho_scale = max(max(xs) - min(xs), (max(ys) - min(ys)) * ratio) * pad
    cam.location += cam.matrix_world.to_3x3() @ Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0))
    for lo, v in rig:                                      # lumini in jurul obiectului, la scara lui
        lo.location = cen + v * (rad * 4 + 0.05)
        lo.rotation_euler = (cen - lo.location).to_track_quat('-Z', 'Y').to_euler()
        lo.data.size = max(0.05, rad * 2.5)
        lo.data.energy = {'key': 45, 'fill': 16, 'rim': 26}[lo.name] * (rad * 4 + 0.05) ** 2 * 2.2


VIEW = {'glisiera_movento': Vector((1.0, -0.55, 0.8)), 'glisiera_bile_450': Vector((1.0, -0.55, 0.6)), 'tip_on': Vector((1.0, -0.6, 0.9)),
        'sina_suspendare': Vector((0.45, -1.0, 0.55)), 'bara_ovala': Vector((0.45, -1.0, 0.6)), 'bara_sincronizare': Vector((0.45, -1.0, 0.6)),
        'banda_dublu': Vector((0.5, -0.8, 1.0)), 'placuta_balama': Vector((1.0, -0.7, 0.6)), 'balama_blum': Vector((1.0, -0.6, 0.9)),
        'balama_70T3650': Vector((1.0, -0.6, 0.9)), 'balama_71B3550': Vector((1.0, -0.6, 0.9)), 'suport_bara': Vector((1.0, -0.6, 0.5)),
        'coltar_40': Vector((1.0, 0.7, 0.8)), 'anti_rasturnare': Vector((1.0, 0.7, 0.8)), 'cleme_movento': Vector((0.8, -0.8, 0.9)),
        'adaptor_tipon': Vector((0.9, -0.8, 1.0)), 'clema_soclu': Vector((0.9, -0.9, 0.8))}

objs = {}
for c in CATALOG:
    mid = c[0]
    if ONLY and mid not in ONLY:
        continue
    objs[mid] = import_model(mid)

SHOW_ROT = {'tipon_usa': (0, math.radians(90), 0), 'adaptor_tipon': (0, math.radians(90), 0)}   # doar pentru imaginea de catalog
for mid, o in objs.items():
    for x in objs.values():
        x.hide_render = x is not o
    o.rotation_euler = SHOW_ROT.get(mid, (0, 0, 0))
    frame([o], VIEW.get(mid, DIRV).normalized())
    sc.render.filepath = os.path.join(PNG, mid + '.png')
    bpy.ops.render.render(write_still=True)
    o.rotation_euler = (0, 0, 0)
    print('RANDAT', mid)


def place(src, loc, rot=None):
    o = src.copy(); sc.collection.objects.link(o); o.hide_render = False
    if rot:
        o.rotation_mode = 'XYZ'; o.rotation_euler = rot
    o.location = Vector(loc) * 0.001
    return o


# ansamblu balama + placuta + suruburi (pozitie inchisa, ca in montaj)
if all(k in objs for k in ('balama_blum', 'placuta_balama', 'surub_3_5x17', 'surub_3_5x15')):
    for x in objs.values():
        x.hide_render = True
    A = [place(objs['balama_blum'], (0, 0, 0)), place(objs['placuta_balama'], (0, 0, 0))]
    A += [place(objs['surub_3_5x17'], (16.0, yy, 3.2)) for yy in (-22.5, 22.5)]
    A += [place(objs['surub_3_5x15'], (3.05, yy, 37.0), (0, math.radians(90), 0)) for yy in (-16.0, 16.0)]
    frame(A, Vector((1.0, -0.6, 0.9)).normalized())
    sc.render.filepath = os.path.join(PNG, 'balama_ansamblu.png')
    bpy.ops.render.render(write_still=True)
    for a in A:
        bpy.data.objects.remove(a, do_unlink=True)
    print('RANDAT balama_ansamblu')

# biblioteca .blend: obiectele asezate pe randuri, vizibile in viewport
if not ONLY:
    x = y = 0.0
    rowh = 0.0
    for mid, o in objs.items():
        o.hide_render = False
        bpy.context.view_layer.update()
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        wdt = max(v.x for v in bb) - min(v.x for v in bb)
        dep = max(v.y for v in bb) - min(v.y for v in bb)
        if x > 0.9:
            x = 0.0; y -= rowh + 0.08; rowh = 0.0
        o.location = (x - (min(v.x for v in bb) - o.location.x), y - (max(v.y for v in bb) - o.location.y), 0)
        t = bpy.data.curves.new('t_' + mid, 'FONT'); t.body = mid; t.size = 0.008
        to = bpy.data.objects.new('ET_' + mid, t); sc.collection.objects.link(to); to.location = (x, y + 0.012, 0)
        x += wdt + 0.05; rowh = max(rowh, dep)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(D, 'feronerie_3d.blend'))
print('FERONERIE_R2_OK', len(objs))
