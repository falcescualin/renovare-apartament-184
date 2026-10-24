"""Randari pas cu pas pentru instructiunile de montaj (stil IKEA), cu feronerie 3D reala (tmp/feronerie_R2/obj).
Rulare (fundal, nu modifica nimic):
  blender --background --python montaj_blender.py -- <spec.json> <folder_iesire> [<fisier.blend cu piese reale>]
spec.json: parts [{id, box [x,y,z,dx,dy,dz] mm | obj | model+place+mirror, mat, step, role, follow}],
           steps [{n, view, parts, explode {id: [dx,dy,dz]}, solo [ids], detail {...}, frame}],
           hwi [{step, model, at, az, ax, mirror, attach, explode, dash}]
Iese: pas_<n>.png (explodat: piese noi turcoaz, feronerie noua portocalie, linii punctate), pas_<n>_ok.png (montat),
      pas_<n>d.png (detaliu), final_<vedere>.png (culori reale), ancore.json (pozitia pe imagine a pieselor noi)."""
import bpy, sys, os, json, math
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

argv = sys.argv[sys.argv.index('--') + 1:]
SPEC = json.load(open(argv[0], encoding='utf-8'))
OUT = argv[1]
BLEND = argv[2] if len(argv) > 2 else None
HWDIR = r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\tmp\feronerie_R2\obj'
os.makedirs(OUT, exist_ok=True)

COL = {'corp': (0.93, 0.93, 0.91, 1), 'front': (0.74, 0.71, 0.67, 1), 'stj': (0.80, 0.66, 0.46, 1), 'hdf': (0.88, 0.88, 0.84, 1),
       'sertar': (0.90, 0.88, 0.80, 1), 'hw': (0.55, 0.57, 0.60, 1), 'top': (0.74, 0.71, 0.67, 1), 'oglinda': (0.80, 0.86, 0.90, 1),
       'led': (1.0, 0.92, 0.55, 1), 'blat': (0.80, 0.66, 0.46, 1), 'metal': (0.55, 0.57, 0.60, 1), 'perete': (0.86, 0.87, 0.88, 1)}
NOU = (0.18, 0.58, 0.54, 1)
ORG = (0.95, 0.50, 0.12, 1)
HW_OLD = (0.42, 0.44, 0.47, 1)
DASH = (0.08, 0.30, 0.45, 1)

if BLEND:
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    for o in bpy.data.objects:
        o.hide_render = True
else:
    bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
PART = {p['id']: p for p in SPEC['parts']}

# ------------------------------------------------------------------ feronerie: un mesh pe model (mm), culoarea dominanta
SRC = {}


def hw_mesh(mid):
    if mid in SRC:
        return SRC[mid]
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=os.path.join(HWDIR, mid + '.obj'), forward_axis='Y', up_axis='Z')
    new = [o for o in bpy.data.objects if o not in before]
    areas = {}
    for o in new:
        for poly in o.data.polygons:
            m = o.material_slots[poly.material_index].material if o.material_slots else None
            if m:
                areas[m.name.split('.')[0]] = areas.get(m.name.split('.')[0], 0) + poly.area
    dom = max(areas, key=areas.get) if areas else 'zinc'
    col = None
    for o in new:
        for s in o.material_slots:
            if s.material and s.material.name.split('.')[0] == dom:
                col = tuple(s.material.diffuse_color)
    bpy.ops.object.select_all(action='DESELECT')
    for o in new:
        o.select_set(True)
    bpy.context.view_layer.objects.active = new[0]
    if len(new) > 1:
        bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active
    me = o.data
    me.materials.clear()
    zs = [v.co.z for v in me.vertices]
    SRC[mid] = (me, col or (0.6, 0.6, 0.6, 1), max(zs) - min(zs))
    bpy.data.objects.remove(o, do_unlink=True)
    return SRC[mid]


def frame_matrix(at, az, ax, mirror):
    az = Vector(az).normalized(); ax = Vector(ax).normalized()
    ay = az.cross(ax)
    R = Matrix(((ax.x, ay.x, az.x, 0), (ax.y, ay.y, az.y, 0), (ax.z, ay.z, az.z, 0), (0, 0, 0, 1)))
    Sx = Matrix.Diagonal(Vector((-0.001 if mirror else 0.001, 0.001, 0.001, 1.0)))
    return Matrix.Translation(Vector(at) / 1000.0) @ R @ Sx


def new_obj(name, me):
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    return o


# ------------------------------------------------------------------ piese
obj, base_mw = {}, {}
for p in SPEC['parts']:
    if 'obj' in p:
        o = bpy.data.objects.get(p['obj'])
        if o is None:
            print('LIPSA', p['obj']); continue
    elif p.get('poly'):
        pts = [(x / 1000.0, y / 1000.0) for x, y in p['poly']]
        ar = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
        if ar < 0:
            pts = pts[::-1]
        n_ = len(pts); z0_ = p['box'][2] / 1000.0; z1_ = z0_ + p['box'][5] / 1000.0
        vs = [(x, y, z0_) for x, y in pts] + [(x, y, z1_) for x, y in pts]
        fs = [tuple(range(n_))[::-1], tuple(range(n_, 2 * n_))] + [(i, (i + 1) % n_, n_ + (i + 1) % n_, n_ + i) for i in range(n_)]
        me = bpy.data.meshes.new(p['id']); me.from_pydata(vs, [], fs); me.update()
        o = new_obj(p['id'], me)
    elif p.get('model'):
        me, col, _ = hw_mesh(p['model'])
        o = new_obj(p['id'], me)
        o.matrix_world = frame_matrix(p['place'], (0, 0, 1), (1, 0, 0), p.get('mirror', False))
    else:
        x, y, z, dx, dy, dz = [v / 1000.0 for v in p['box']]
        vs = [(x, y, z), (x + dx, y, z), (x + dx, y + dy, z), (x, y + dy, z), (x, y, z + dz), (x + dx, y, z + dz), (x + dx, y + dy, z + dz), (x, y + dy, z + dz)]
        fs = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (0, 4, 7, 3)]
        me = bpy.data.meshes.new(p['id']); me.from_pydata(vs, [], fs); me.update()
        o = new_obj(p['id'], me)
    obj[p['id']] = o
    base_mw[p['id']] = o.matrix_world.copy()

HW = []
for i, h in enumerate(SPEC.get('hwi', [])):
    me, col, length = hw_mesh(h['model'])
    o = new_obj('HWI_%03d_%s' % (i, h['model']), me)
    mw = frame_matrix(h['at'], h['az'], h['ax'], h.get('mirror', False))
    o.matrix_world = mw
    HW.append(dict(h=h, o=o, mw=mw, col=col, L=length))

for o in sc.objects:
    if o.type == 'MESH':
        o.hide_render = o.name not in {v.name for v in obj.values()} and not o.name.startswith('HWI_')

# ------------------------------------------------------------------ Workbench, lumina de studio, contur
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.light = 'STUDIO'; sh.color_type = 'OBJECT'
sh.show_object_outline = True; sh.object_outline_color = (0.09, 0.17, 0.23)
sh.show_cavity = True; sh.cavity_type = 'BOTH'; sh.cavity_ridge_factor = 1.0; sh.cavity_valley_factor = 1.0
sh.show_shadows = False; sh.show_specular_highlight = True
sc.render.film_transparent = True
sc.display_settings.display_device = 'sRGB'; sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = 1.1
RX, RY = SPEC.get('resolution', [1800, 1300])
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = RX, RY, 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'

cd = bpy.data.cameras.new('CAM_montaj'); cam = bpy.data.objects.new('CAM_montaj', cd); sc.collection.objects.link(cam)
cd.type = 'ORTHO'; sc.camera = cam; cd.clip_end = 200
DIRS = {'fata': Vector((0.55, 1.0, 0.55)), 'spate': Vector((-0.55, -1.0, 0.45)), 'sus': Vector((0.35, 1.0, 1.2)),
        'jos': Vector((0.55, 1.0, -0.6)), 'stanga': Vector((-1.0, 0.45, 0.35)), 'dreapta': Vector((1.0, 0.55, 0.45)), 'plan': Vector((0.0, 0.05, 1.0))}
DIRS.update({k: Vector(v) for k, v in SPEC.get('views', {}).items()})


def corners(objs):
    bpy.context.view_layer.update()
    pts = []
    for o in objs:
        pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    return pts


CEN = Vector((0, 0, 0))


def aim(view, pts, pad=1.12):
    if not pts:
        return
    d = DIRS[view].normalized()
    cen = sum(pts, Vector()) / len(pts)
    cam.location = cen + d * 30
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    xs = [(inv @ p).x for p in pts]; ys = [(inv @ p).y for p in pts]
    w = max(xs) - min(xs); h = max(ys) - min(ys)
    cd.ortho_scale = max(w, h * RX / RY) * pad
    cam.location += cam.matrix_world.to_3x3() @ Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0))
    bpy.context.view_layer.update()


DASHES = []


def dash_line(p0, p1, r=0.00045, seg=0.004, gap=0.003):
    import bmesh
    v = p1 - p0; L = v.length
    if L < 1e-5:
        return
    d = v.normalized(); q = Vector((0, 0, 1)).rotation_difference(d)
    bm = bmesh.new(); t = 0.0
    while t < L:
        t2 = min(t + seg, L)
        mid = p0 + d * ((t + t2) / 2)
        g = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=r, radius2=r, depth=t2 - t)
        bmesh.ops.transform(bm, matrix=Matrix.Translation(mid) @ q.to_matrix().to_4x4(), verts=g['verts'])
        t = t2 + gap
    me = bpy.data.meshes.new('dash'); bm.to_mesh(me); bm.free()
    o = new_obj('DASH', me); o.color = DASH; DASHES.append(o)


def clear_dashes():
    for o in DASHES:
        me = o.data; bpy.data.objects.remove(o, do_unlink=True); bpy.data.meshes.remove(me)
    DASHES.clear()


def part_offset(pid, ex):
    p = PART[pid]
    v = ex.get(pid) or (ex.get(p.get('follow')) if p.get('follow') else None)
    return Vector(v) / 1000.0 if v else Vector((0, 0, 0))


def apply_state(n, shown, new, ex, exploded, final=False, detail=False, only=None):
    """pozitioneaza si coloreaza piesele si feroneria pentru pasul n"""
    for pid, o in obj.items():
        vis = pid in shown
        o.hide_render = not vis; o.hide_viewport = not vis
        off = part_offset(pid, ex) if exploded else Vector((0, 0, 0))
        o.matrix_world = Matrix.Translation(off) @ base_mw[pid]
        m = PART[pid]['mat']
        if final:
            o.color = COL.get(m, COL['corp'])
        elif PART[pid].get('role') == 'context':
            o.color = COL['perete']
        else:
            o.color = (ORG if m in ('hw', 'led', 'metal') else NOU) if pid in new else COL.get(m, COL['corp'])
    clear_dashes()
    out = []
    for e in HW:
        h = e['h']; o = e['o']
        vis = h['step'] <= n and (h.get('attach') is None or h['attach'] in shown or PART.get(h['attach'], {}).get('role') == 'context')
        if detail and h.get('attach') is None and h['step'] < n:
            vis = False
        if detail and h.get('attach') is not None and h['attach'] not in shown:
            vis = False
        if only and h['step'] == n and h.get('letter') not in only:
            vis = False
        if n == 0:
            vis = True
        o.hide_render = not vis; o.hide_viewport = not vis
        if not vis:
            continue
        isnew = h['step'] == n and not final
        off = part_offset(h['attach'], ex) if (exploded and h.get('attach') in PART) else Vector((0, 0, 0))
        if isnew and exploded:
            off = off + Vector(h['az']).normalized() * (h['explode'] / 1000.0)
        o.matrix_world = Matrix.Translation(off) @ e['mw']
        o.color = e['col'] if final else (ORG if isnew else HW_OLD)
        if isnew:
            out.append(o)
            if exploded and h.get('dash', True) and abs(h['explode']) > 1:
                at = Vector(h['at']) / 1000.0
                az = Vector(h['az']).normalized()
                tip = at + off - az * (e['L'] / 1000.0)
                dash_line(tip, at - az * (e['L'] / 1000.0) * 0.9)
    return out


ANC = {}
shown = []
for st in SPEC['steps']:
    n = st['n']; key = str(n)
    ex = st.get('explode', {}) or {}
    solo = st.get('solo')
    if solo:
        cur_shown, new = list(solo), list(solo)
    else:
        new = [i for i in st['parts'] if i in obj]
        shown += [i for i in new if PART[i].get('role') != 'context']
        cur_shown = shown + [i for i in obj if PART[i].get('role') == 'context' and PART[i]['step'] <= n]
    # 1) vederea explodata (imaginea principala)
    hw_new = apply_state(n if not solo else -1, set(cur_shown), set(new), ex, True)
    vis_objs = [obj[i] for i in cur_shown] + [e['o'] for e in HW if not e['o'].hide_render] + DASHES
    focus = vis_objs if st.get('frame', 'all') == 'all' else ([obj[i] for i in new] + hw_new + DASHES or vis_objs)
    aim(st.get('view', 'fata'), corners(focus))
    ANC[key] = {}
    grp = {}
    for e in HW:
        if e['h']['step'] == n and not e['o'].hide_render and e['h'].get('letter'):
            bb = [e['o'].matrix_world @ Vector(c) for c in e['o'].bound_box]
            grp.setdefault(e['h']['letter'], []).append(sum(bb, Vector()) / 8)
    for L, pts in grp.items():
        uv = [world_to_camera_view(sc, cam, p) for p in pts]
        # eticheta langa piesa cea mai din exterior a grupului (feroneria explodata e in afara pieselor)
        best = max(uv, key=lambda u: (u.x - 0.5) ** 2 + (u.y - 0.5) ** 2)
        ANC[key]['hw:' + L] = [round(best.x, 4), round(best.y, 4)]
    for pid in new:
        o = obj[pid]
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        uv = world_to_camera_view(sc, cam, sum(bb, Vector()) / 8)
        ANC[key][pid] = [round(uv.x, 4), round(uv.y, 4)]
    sc.render.filepath = os.path.join(OUT, 'pas_%s.png' % key)
    bpy.ops.render.render(write_still=True)
    # 2) detaliu (explodat, alta vedere / piese ascunse)
    det = st.get('detail')
    if det:
        hide = set(det.get('hide', []))
        vis = list(det['only']) if det.get('only') else [k for k in cur_shown if k not in hide]
        apply_state(n if not solo else -1, set(vis), set(new), ex, True, detail=True, only=det.get('hw'))
        hwn = [e['o'] for e in HW if not e['o'].hide_render and (e['h']['step'] == n)]
        if det.get('only'):
            objs = [obj[k] for k in det['only']] + [e['o'] for e in HW if not e['o'].hide_render]
        elif det.get('frame') == 'hw':                                  # incadrare doar pe feroneria noua (+ piesele din 'with')
            objs = hwn + DASHES + [obj[k] for k in det.get('with', [])]
        else:
            objs = [obj[k] for k in (new if det.get('frame', 'new') == 'new' else vis) if k not in hide and PART[k].get('role') != 'context'] + hwn + DASHES
        aim(det.get('view', 'fata'), corners(objs or [obj[k] for k in vis]), pad=1.08)
        sc.render.filepath = os.path.join(OUT, 'pas_%sd.png' % key)
        bpy.ops.render.render(write_still=True)
    # 3) rezultatul pasului (montat)
    apply_state(n if not solo else -1, set(cur_shown), set(new), {}, False)
    vis_objs = [obj[i] for i in cur_shown if PART[i].get('role') != 'context'] + [e['o'] for e in HW if not e['o'].hide_render]
    aim(st.get('view', 'fata'), corners(vis_objs or [obj[i] for i in cur_shown]))
    sc.render.filepath = os.path.join(OUT, 'pas_%s_ok.png' % key)
    bpy.ops.render.render(write_still=True)

# final: toate piesele (fara context), culori reale
allp = [k for k in obj if PART[k].get('role') != 'context']
for view in SPEC.get('final_views', ['fata']):
    apply_state(999, set(allp), set(), {}, False, final=True)
    aim(view, corners([obj[k] for k in allp]))
    sc.render.filepath = os.path.join(OUT, 'final_%s.png' % view)
    bpy.ops.render.render(write_still=True)
json.dump(ANC, open(os.path.join(OUT, 'ancore.json'), 'w'), indent=1)
print('MONTAJ_OK', len(SPEC['steps']), 'feronerie', len(HW))
