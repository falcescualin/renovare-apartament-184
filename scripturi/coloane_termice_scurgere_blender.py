"""Rulează: blender --background apartament_184_randare.blend --python coloane_termice_scurgere_blender.py
Aduce în scena de randare modificările din FreeCAD de la 06.10.2026 (apartament_184.FCStd, spalatorie_vestibul.FCStd):
- racordurile radiatoarelor R1 (dormitor) și R2 (sufragerie) la cele două coloane: multistrat 16 × 2, la cotele 70 / 110 mm, indicative;
- două coloane de agent termic Ø26,9 în colțul dormitor–sufragerie, partea radiatorului (X 3465 / 3525, Y −280, de la pardoseală la tavan);
- coloana de scurgere PP Ø110 din colțul vestibul–sufragerie (X 3450, Y −5450), cu izolație fonică Ø190 și mască de gips-carton 2 × 12,5 mm;
- mobilierul din spălătorie ocolește masca: rafturile coloanei laterale încep la Y −5300, panoul lateral drept la Y −5305, capacul de sus
  are un decupaj în colț, robinetul de rezervă (concept) e mutat cu 250 mm spre ușă.
Se rulează o singură dată pe scena curentă (verifică dacă obiectele există deja). Salvează .blend."""
import bpy, bmesh
from mathutils import Vector

P = 'Spalatorie_vestibul_custom__'


def mat(name, rgb, rough, metal=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    lin = lambda v: ((v / 255 + 0.055) / 1.055) ** 2.4 if v / 255 > 0.04045 else v / 255 / 12.92
    b.inputs['Base Color'].default_value = (lin(rgb[0]), lin(rgb[1]), lin(rgb[2]), 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    return m


def coll():
    for c in bpy.data.collections:
        if 'Spalatorie_vestibul_custom' in c.name or c.name == 'Mobilier':
            return c
    return bpy.context.scene.collection


def new_obj(name, bm, material, col):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    o.data.materials.append(material)
    col.objects.link(o)
    for p in me.polygons:
        p.use_smooth = False
    return o


def box(x0, y0, z0, x1, y1, z1):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector(((x1 + x0) / 2 + v.co.x * (x1 - x0), (y1 + y0) / 2 + v.co.y * (y1 - y0), (z1 + z0) / 2 + v.co.z * (z1 - z0)))
    return bm


def tube(cx, cy, z0, z1, r_out, r_in=None, seg=48):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r_out, radius2=r_out, depth=z1 - z0)
    for v in bm.verts:
        v.co += Vector((cx, cy, (z0 + z1) / 2))
    if r_in:
        bm2 = bmesh.new()
        bmesh.ops.create_cone(bm2, cap_ends=True, segments=seg, radius1=r_in, radius2=r_in, depth=z1 - z0)
        for v in bm2.verts:
            v.co += Vector((cx, cy, (z0 + z1) / 2))
        # inel: două cilindri concentrici, cel interior cu normalele întoarse
        bmesh.ops.reverse_faces(bm2, faces=bm2.faces[:])
        me2 = bpy.data.meshes.new('tmp'); bm2.to_mesh(me2); bm2.free()
        bm.from_mesh(me2); bpy.data.meshes.remove(me2)
    return bm


if bpy.data.objects.get('Coloana_termica_1_dormitor'):
    raise SystemExit('DEJA_APLICAT')

col = coll()
m_otel = mat('R_Teava_otel_vopsita', (232, 230, 217), 0.38, 0.0)
m_pp = mat('R_Teava_PP_gri', (150, 150, 155), 0.45)
m_izol = mat('R_Izolatie_fonica', (62, 62, 66), 0.9)
m_gk = bpy.data.materials.get('R_Vopsea_perete_alb_cald') or mat('R_Vopsea_perete_alb_cald', (232, 230, 217), 0.9)

# 1) coloanele de agent termic din dormitor (mm → m)
mm = 0.001
for i, x in ((1, 3525), (2, 3465)):
    new_obj('Coloana_termica_%d_dormitor' % i, tube(x * mm, -280 * mm, 0, 2.5, 0.01345), m_otel, col)

# 1b) racordurile radiatoarelor la coloane (multistrat 16x2, Ø16): același traseu ca în FreeCAD (Racord_R1_A ... Racord_R2_B)
from mathutils import Quaternion
def polyline_tube(pts, r=0.008, seg=16):
    bm = bmesh.new()
    P = [Vector((x * mm, y * mm, z * mm)) for x, y, z in pts]
    for a, b in zip(P, P[1:]):
        d = b - a
        q = d.to_track_quat('Z', 'Y')
        res = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=d.length)
        for v in res['verts']:
            v.co = q @ v.co + (a + b) / 2
    for p in P[1:-1]:
        res = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=8, radius=r)
        for v in res['verts']:
            v.co += p
    return bm
yc = -371.5
RACORD = {
    'Racord_R1_A': [(3525, -280, 70), (3525, -312, 70), (2030, -312, 70), (2030, yc, 70), (2030, yc, 150)],
    'Racord_R1_B': [(3465, -280, 110), (2930, -280, 110), (2930, yc, 110), (2930, yc, 150)],
    'Racord_R2_A': [(3525, -280, 70), (3925, -280, 70), (3925, yc, 70), (3925, yc, 150)],
    'Racord_R2_B': [(3465, -280, 110), (3465, -312, 110), (5025, -312, 110), (5025, yc, 110), (5025, yc, 150)],
}
for n, pts in RACORD.items():
    new_obj(n, polyline_tube(pts), m_otel, col)

# 2) scurgerea mașinii de spălat: țeavă PP Ø110, izolație Ø190, mască fonică
new_obj('Teava_scurgere_masina_spalat_PP110', tube(3.45, -5.45, 0, 2.5, 0.055), m_pp, col)
new_obj('Izolatie_fonica_teava', tube(3.45, -5.45, 0, 2.5, 0.095, 0.055), m_izol, col)
new_obj('Masca_fonica_colt_A', box(3.305, -5.55, 0, 3.33, -5.305, 2.5), m_gk, col)
new_obj('Masca_fonica_colt_B', box(3.33, -5.33, 0, 3.55, -5.305, 2.5), m_gk, col)

# 3) mobilierul coloanei laterale ocolește masca
def clamp_y(name, ymin):
    o = bpy.data.objects[P + name]
    for v in o.data.vertices:
        if v.co.y < ymin:
            v.co.y = ymin
    o.data.update()


for n in ('Baza_laterala', 'Raft_lateral', 'Raft_lateral001', 'Raft_lateral002', 'Raft_lateral003', 'Raft_lateral004'):
    clamp_y(n, -5.300)
clamp_y('Lateral_dreapta', -5.305)

cap = bpy.data.objects[P + 'Capac_sus']                       # capac L: decupaj în colț (x ≥ 3300, y ≤ −5305)
xs = [v.co.x for v in cap.data.vertices]; ys = [v.co.y for v in cap.data.vertices]; zs = [v.co.z for v in cap.data.vertices]
x0, x1, y0, y1, z0, z1 = min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)
bm = box(x0, -5.305, z0, x1, y1, z1)
bm2 = box(x0, y0, z0, 3.30, -5.305, z1)
me2 = bpy.data.meshes.new('tmp'); bm2.to_mesh(me2); bm2.free(); bm.from_mesh(me2); bpy.data.meshes.remove(me2)
bm.to_mesh(cap.data); bm.free(); cap.data.update()

rb = bpy.data.objects[P + 'Robinet_rezerva_POZITIE_CONCEPT']
rb.location.y += 0.25

print('COLOANE_OK')
bpy.ops.wm.save_mainfile()
