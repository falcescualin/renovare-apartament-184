"""Randari izometrice ale fiecarui panou, cu gaurile reale (boolean) si feronerie 3D explodata deasupra gaurilor (stil IKEA).
Rulare: blender --background --python montaj_panouri_blender.py -- <panouri.json> <folder_iesire> <feronerie_3d.blend>
panouri.json: {"panels":[{"id","box":[x,y,z,dx,dy,dz],"mat","views":[{"name","dir":[x,y,z],"holes":[{pos,n_out,dia,depth,through,hw,kind}]}]}]}"""
import bpy, bmesh, sys, os, json, math
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index('--') + 1:]
DATA = json.load(open(argv[0], encoding='utf-8')); OUT = argv[1]; LIB = argv[2]
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# biblioteca de feronerie
with bpy.data.libraries.load(LIB, link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith('HW_')]
HW = {o.name[3:]: o for o in dst.objects if o}
for o in HW.values():
    o.hide_render = True

COL = {'corp': (0.88, 0.88, 0.85, 1), 'front': (0.78, 0.74, 0.68, 1), 'stj': (0.82, 0.68, 0.48, 1), 'hdf': (0.90, 0.90, 0.86, 1),
       'sertar': (0.93, 0.91, 0.84, 1), 'top': (0.80, 0.77, 0.72, 1), 'blat': (0.82, 0.68, 0.48, 1)}

sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'; sh.show_object_outline = True; sh.object_outline_color = (0.09, 0.17, 0.23)
sh.show_cavity = True; sh.cavity_type = 'BOTH'; sh.cavity_ridge_factor = 0.8; sh.cavity_valley_factor = 1.2
sh.show_shadows = False; sh.show_specular_highlight = False
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = 1.0
RX, RY = 1400, 1000
sc.render.resolution_x, sc.render.resolution_y = RX, RY
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
cd = bpy.data.cameras.new('c'); cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); cd.type = 'ORTHO'; sc.camera = cam


def mat(name, rgba):
    m = bpy.data.materials.get(name)
    if not m:
        m = bpy.data.materials.new(name); m.diffuse_color = rgba
    return m


def cleanup(objs):
    for o in objs:
        me = o.data if o.type == 'MESH' else None
        bpy.data.objects.remove(o, do_unlink=True)
        if me and me.users == 0 and me.name not in {h.data.name for h in HW.values()}:
            bpy.data.meshes.remove(me)


def box_obj(name, box, rgba):
    x, y, z, dx, dy, dz = [v / 1000.0 for v in box]
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=Vector((dx, dy, dz)), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector((x + dx / 2, y + dy / 2, z + dz / 2)), verts=bm.verts)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(mat('pm_' + name, rgba))
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    return o


def cutter(h):
    n = Vector(h['n_out']).normalized()
    depth = (h['depth'] + 4.0) / 1000.0 if h['through'] else (h['depth'] + 1.0) / 1000.0
    r = h['dia'] / 2000.0
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=r, radius2=r, depth=depth)
    # cilindrul e centrat pe origine, axa Z. Il orientam pe -n (in material) cu capul deasupra fetei.
    # centrul: pos + n*(1mm) - n*depth/2 ... pentru through: de la pos + 2mm pana la pos - (T+2mm)
    ofs = (2.0 if h['through'] else 1.0) / 1000.0
    center = Vector([v / 1000.0 for v in h['pos']]) + n * ofs - n * depth / 2
    q = Vector((0, 0, 1)).rotation_difference(n)
    M = Matrix.Translation(center) @ q.to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    return bm


def place_hw(model, pos, n, offset_mm, scale=1.0):
    o = HW[model].copy(); sc.collection.objects.link(o)
    o.hide_render = False
    n = Vector(n).normalized()
    q = Vector((0, 0, 1)).rotation_difference(n)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = q
    o.location = Vector([v / 1000.0 for v in pos]) + n * (offset_mm / 1000.0)
    o.scale = (0.001 * scale,) * 3
    return o


def dashes(pos, n, a_mm, b_mm):
    """linie intrerupta intre pos+n*a si pos+n*b (mm), cilindri subtiri"""
    out = []
    n = Vector(n).normalized()
    t = a_mm
    while t < b_mm:
        t2 = min(t + 3.0, b_mm)
        p0 = Vector(pos) + n * t; p1 = Vector(pos) + n * t2
        mid = (p0 + p1) / 2 / 1000.0
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.00035, radius2=0.00035, depth=(t2 - t) / 1000.0)
        q = Vector((0, 0, 1)).rotation_difference(n)
        bmesh.ops.transform(bm, matrix=Matrix.Translation(mid) @ q.to_matrix().to_4x4(), verts=bm.verts)
        me = bpy.data.meshes.new('d'); bm.to_mesh(me); bm.free(); me.materials.append(mat('dash', (0.1, 0.4, 0.6, 1)))
        o = bpy.data.objects.new('d', me); sc.collection.objects.link(o); out.append(o)
        t += 6.0
    return out


results = {}
for P in DATA['panels']:
    results[P['id']] = []
    rgba = COL.get(P['mat'], COL['corp'])
    for vi, V in enumerate(P['views']):
        base = box_obj('P_' + P['id'], P['box'], rgba)
        created = [base]
        holes = V['holes']
        if holes:
            bm = bmesh.new()
            for h in holes:
                c = cutter(h)
                tmp = bpy.data.meshes.new('t'); c.to_mesh(tmp); c.free(); bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
            cm = bpy.data.meshes.new('cut'); bm.to_mesh(cm); bm.free()
            cut = bpy.data.objects.new('cut', cm); sc.collection.objects.link(cut)
            mod = base.modifiers.new('b', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = cut; mod.solver = 'EXACT'
            bpy.context.view_layer.objects.active = base
            bpy.ops.object.modifier_apply(modifier='b')
            bpy.data.objects.remove(cut, do_unlink=True)
            # gaurile: umbrire interioara inchisa (materialul panoului ramane; cavity arata gaurile)
        hw_objs = []
        for h in holes:                                   # discuri negre = gauri vizibile pe imagine
            nn = Vector(h['n_out']).normalized()
            rr = h['dia'] / 2000.0
            bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=rr, radius2=rr, depth=0.0006)
            qq = Vector((0, 0, 1)).rotation_difference(nn)
            bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector([v / 1000.0 for v in h['pos']]) + nn * 0.00025) @ qq.to_matrix().to_4x4(), verts=bm.verts)
            me = bpy.data.meshes.new('hd'); bm.to_mesh(me); bm.free(); me.materials.append(mat('hole_dark', (0.03, 0.05, 0.07, 1)))
            ob = bpy.data.objects.new('hd', me); sc.collection.objects.link(ob); hw_objs.append(ob)
        for h in holes:
            if h.get('hw') and h['hw'] in HW and h['kind'] != 'pilot5':
                off = 55.0 if h['hw'] in ('confirmat',) else 42.0
                hw_objs.append(place_hw(h['hw'], h['pos'], h['n_out'], off, 1.7))
                hw_objs += dashes(h['pos'], h['n_out'], 2.0, off - 6.0)
        created += hw_objs
        sc.view_layers[0].update()
        d = Vector(V['dir']).normalized()
        pts = []
        for o in [base] + [x for x in hw_objs if x.name.startswith('HW_')]:
            pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
        cen = sum(pts, Vector()) / len(pts)
        cam.location = cen + d * 5
        cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
        bpy.context.view_layer.update()
        inv = cam.matrix_world.inverted()
        xs = [(inv @ p).x for p in pts]; ys = [(inv @ p).y for p in pts]
        cd.ortho_scale = max(max(xs) - min(xs), (max(ys) - min(ys)) * RX / RY) * 1.18
        cam.location += cam.matrix_world.to_3x3() @ Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0))
        fn = os.path.join(OUT, 'pan_%s_%d.png' % (P['id'], vi))
        sc.render.filepath = fn
        bpy.ops.render.render(write_still=True)
        results[P['id']].append(os.path.basename(fn))
        cleanup(created)
json.dump(results, open(os.path.join(OUT, 'panouri_imagini.json'), 'w'), indent=1)
print('PANOURI_OK', sum(len(v) for v in results.values()))
