"""Rulează: blender --background apartament_184_randare.blend --python baie_dormitor_fix_blender.py [-- --nu-salva]
Corecturi cerute pe 06.10.2026 pentru randări fotorealiste:
BAIE
- microciment OLIVE GREY pe pereții băii, pardoseală, măști, nișe și trapele de acces (material nou
  R_Microciment_olive_gri): variația „norilor” din ambientCG Concrete046 (2,4 m), urmele de gletieră din
  Poly Haven plastered_wall_04 (3,2 m), luciu satinat de microciment sigilat;
- lumina băii 4000 K (neutră), camera B_01 cu obiectiv 16 mm în loc de 14 (fără deformarea marginilor);
DORMITOR
- patul: în locul cutiei provizorii, cadru de stejar cu tăblie (JYSK HALD 160 × 200 cu ladă), saltea, pilotă,
  perne și pled cu forme moi (rotunjiri + subdivizare + ondulații fine ale țesăturii); obiectele vechi doar se ascund;
- voalul: era material cu transmisie (ca sticla) pe o plasă în zigzag cu grosime, care refracta parapetul și
  dădea „lamelele” albe de deasupra caloriferului → țesătură translucidă, fără refracție, cu pliuri netede;
- draperiile blackout din dormitor și sufragerie: pliuri netede (sinusoidale), nu în zigzag;
- camera D_01 mutată mai departe de perete;
GENERAL
- muchii rotunjite de 1 mm (doar la randare) pe plăcile de mobilier: muchiile prind lumina ca în realitate."""
import bpy, bmesh, math, os, sys, random
from mathutils import Vector, Matrix

ROOT = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
TX = os.path.join(ROOT, 'texturi')
SAVE = '--nu-salva' not in sys.argv


def srgb_lin(c):
    return tuple(((v / 255 + 0.055) / 1.055) ** 2.4 if v / 255 > 0.04045 else v / 255 / 12.92 for v in c) + (1.0,)


def tex(nt, path, noncolor, vec, x, y):
    n = nt.nodes.new('ShaderNodeTexImage')
    n.image = bpy.data.images.load(path, check_existing=True)
    n.image.colorspace_settings.name = 'Non-Color' if noncolor else 'sRGB'
    n.interpolation = 'Cubic'; n.location = (x, y)
    nt.links.new(vec, n.inputs['Vector'])
    return n


def maprange(nt, val, a, b, c, d, x, y):
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.location = (x, y); mr.clamp = True
    mr.inputs['From Min'].default_value, mr.inputs['From Max'].default_value = a, b
    mr.inputs['To Min'].default_value, mr.inputs['To Max'].default_value = c, d
    nt.links.new(val, mr.inputs['Value'])
    return mr.outputs['Result']


# =====================================================================  BAIE
def microciment_olive():
    m = bpy.data.materials.get('R_Microciment_olive_gri') or bpy.data.materials.new('R_Microciment_olive_gri')
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (500, 0)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (200, 0)
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    uv = nt.nodes.new('ShaderNodeUVMap'); uv.uv_map = 'UV_box'; uv.location = (-1500, 0)
    m1 = nt.nodes.new('ShaderNodeMapping'); m1.location = (-1300, 200); m1.inputs['Scale'].default_value = (1 / 2.4,) * 3
    m2 = nt.nodes.new('ShaderNodeMapping'); m2.location = (-1300, -300); m2.inputs['Scale'].default_value = (1 / 3.2,) * 3
    nt.links.new(uv.outputs['UV'], m1.inputs['Vector']); nt.links.new(uv.outputs['UV'], m2.inputs['Vector'])
    c46 = os.path.join(TX, 'ambientcg', 'Concrete046', 'Concrete046_4K-JPG_')
    col = tex(nt, c46 + 'Color.jpg', False, m1.outputs['Vector'], -1000, 300)
    bw = nt.nodes.new('ShaderNodeRGBToBW'); bw.location = (-700, 300)
    nt.links.new(col.outputs['Color'], bw.inputs['Color'])
    var = maprange(nt, bw.outputs['Val'], 0.528, 0.676, 0.84, 1.12, -500, 300)        # „norii” de gletieră
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.location = (-250, 300)
    mx.inputs['Factor'].default_value = 1.0
    mx.inputs['A'].default_value = srgb_lin((127, 125, 108))                            # olive grey #7F7D6C
    nt.links.new(var, mx.inputs['B'])
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    rg = tex(nt, c46 + 'Roughness.jpg', True, m1.outputs['Vector'], -1000, 0)
    nt.links.new(maprange(nt, rg.outputs['Color'], 0, 1, 0.3, 0.56, -500, 0), b.inputs['Roughness'])
    nm = tex(nt, os.path.join(TX, 'polyhaven', 'plastered_wall_04', 'plastered_wall_04_nor_gl_4k.jpg'), True, m2.outputs['Vector'], -1000, -300)
    nmap = nt.nodes.new('ShaderNodeNormalMap'); nmap.location = (-500, -300); nmap.uv_map = 'UV_box'
    nmap.inputs['Strength'].default_value = 0.35
    nt.links.new(nm.outputs['Color'], nmap.inputs['Color'])
    disp = tex(nt, c46 + 'Displacement.jpg', True, m1.outputs['Vector'], -1000, -600)
    bp = nt.nodes.new('ShaderNodeBump'); bp.location = (-200, -450)
    bp.inputs['Strength'].default_value = 0.08; bp.inputs['Distance'].default_value = 0.002
    nt.links.new(disp.outputs['Color'], bp.inputs['Height'])
    nt.links.new(nmap.outputs['Normal'], bp.inputs['Normal'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    m['decor'] = 'Microciment olive grey (#7F7D6C), sigilat satinat'
    m.diffuse_color = srgb_lin((127, 125, 108))
    return m


MO = microciment_olive()
MC = bpy.data.materials['R_Microciment_alb_cald']
X0, X1, Y0, Y1 = 0.145, 2.455, -5.555, -3.915                     # conturul băii (m)
pw = bpy.data.objects['Pereti']
me = pw.data
if MO.name not in [m.name for m in me.materials if m]:
    me.materials.append(MO)
names = [m.name if m else '' for m in me.materials]
io, ic = names.index(MO.name), names.index(MC.name)
M = pw.matrix_world
nb = 0
for p in me.polygons:
    if p.material_index != ic:
        continue
    vs = [M @ me.vertices[i].co for i in p.vertices]
    if all(X0 - 0.01 <= v.x <= X1 + 0.01 and Y0 - 0.01 <= v.y <= Y1 + 0.01 for v in vs):
        p.material_index = io; nb += 1
print('BAIE pereți olive:', nb, 'fețe')
for n in ('Pardoseala_Baie', 'Baie_custom__Masca_cada_nise', 'Baie_custom__Masca_WC_fata', 'Baie_custom__Masca_WC_lateral_lavoar',
          'Baie_custom__Masca_WC_lateral_stanga', 'Baie_custom__Masca_WC_polita_sus', 'Baie_custom__Panou_cada_acces',
          'Baie_custom__Trapa_acces_laterala'):
    o = bpy.data.objects.get(n)
    if o is not None:
        o.data.materials.clear(); o.data.materials.append(MO)
        if 'UV_box' not in o.data.uv_layers:          # UV în metri, ca la restul pereților
            bm = bmesh.new(); bm.from_mesh(o.data)
            lay = bm.loops.layers.uv.new('UV_box')
            R = o.matrix_world.to_3x3()
            for f in bm.faces:
                nn = R @ f.normal
                ax = max(range(3), key=lambda i: abs(nn[i]))
                for l in f.loops:
                    co = o.matrix_world @ l.vert.co
                    l[lay].uv = ((co.y, co.z), (co.x, co.z), (co.x, co.y))[ax]
            bm.to_mesh(o.data); bm.free()
lb = bpy.data.objects.get('R_Lumina_Baie')
if lb:
    lb.data.color = (1.0, 0.92, 0.84)              # ~4000 K
cam = bpy.data.objects['B_01_baie']
cam.data.lens = 16.0
cam['tinta'] = 0.48            # pereții olive sunt închiși: ținta expunerii automate mai jos, ca obiectele albe să nu se ardă
cam['tinta_noapte'] = 0.38

# =====================================================================  DORMITOR: pat
def hide(name):
    o = bpy.data.objects.get(name)
    if o is not None:
        o.hide_render = True; o.hide_set(True); o['inlocuit'] = '06.10.2026: pat nou modelat (baie_dormitor_fix_blender.py)'


old = bpy.data.objects.get('Pat')
coll = old.users_collection[0] if old else bpy.context.scene.collection
# patul din FreeCAD se poate muta (Codex l-a avansat cu 150 mm pe 06.10): patul nou urmează poziția lui
if old is not None:
    _pts = [old.matrix_world @ Vector(c) for c in old.bound_box]
    DX, DY = min(p.x for p in _pts) - 0.15, min(p.y for p in _pts) - (-2.60)
else:
    DX = DY = 0.0
print('PAT deplasare față de poziția inițială: %.3f / %.3f m' % (DX, DY))
for n in ('Pat', 'D_Perna_1', 'D_Perna_2', 'D_Perna_deco_1', 'D_Pilota', 'D_Pled'):
    hide(n)


def soft_box(name, x0, x1, y0, y1, z0, z1, mat, bevel=0.0, seg=3, subsurf=0, noise=0.0, rot=None, pivot=None):
    o = bpy.data.objects.get(name)
    if o is not None:
        bpy.data.objects.remove(o, do_unlink=True)
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 + (v.co.x + 0.5) * (x1 - x0)
        v.co.y = y0 + (v.co.y + 0.5) * (y1 - y0)
        v.co.z = z0 + (v.co.z + 0.5) * (z1 - z0)
    if rot:
        pv = Vector(pivot)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=pv, matrix=Matrix.Rotation(math.radians(rot[1]), 3, rot[0]))
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    coll.objects.link(o)
    me.materials.append(bpy.data.materials[mat])
    for p in me.polygons:
        p.use_smooth = True
    if bevel:
        bv = o.modifiers.new('Rotunjire', 'BEVEL'); bv.width = bevel; bv.segments = seg; bv.limit_method = 'NONE'
        bv.harden_normals = False
    if subsurf:
        ss = o.modifiers.new('Moale', 'SUBSURF'); ss.levels = subsurf; ss.render_levels = subsurf
    if noise:
        t = bpy.data.textures.get('T_tesatura') or bpy.data.textures.new('T_tesatura', 'CLOUDS')
        t.noise_scale = 0.12; t.noise_depth = 2
        d = o.modifiers.new('Cute', 'DISPLACE'); d.texture = t; d.strength = noise; d.mid_level = 0.5
    o['pat_nou'] = True
    return o


OAK = 'R_Stejar_natural_H1145'          # același stejar Kronospan 3025 ca restul mobilierului din dormitor
LIN = 'R_Lenjerie_alb'


def drape(name, x0, x1, y0, y1, z, drop, mat, sides=('y0', 'y1', 'x1'), thick=0.03, noise=0.01, out=0.035):
    """țesătură pusă peste saltea: un dreptunghi sus + „fuste” care cad pe laturile date (pilotă, pled)"""
    o = bpy.data.objects.get(name)
    if o is not None:
        bpy.data.objects.remove(o, do_unlink=True)
    nx, ny, nz = 40, 30, 8
    bm = bmesh.new()
    top = [[bm.verts.new((x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny, z)) for j in range(ny + 1)] for i in range(nx + 1)]
    for i in range(nx):
        for j in range(ny):
            bm.faces.new((top[i][j], top[i + 1][j], top[i + 1][j + 1], top[i][j + 1]))

    def skirt(edge, outdir):
        rows, prev = [edge], edge
        for k in range(1, nz + 1):
            t = k / nz
            row = [bm.verts.new((v.co.x + outdir[0] * out * t, v.co.y + outdir[1] * out * t, z - drop * t)) for v in edge]
            for a in range(len(edge) - 1):
                bm.faces.new((prev[a], prev[a + 1], row[a + 1], row[a]))
            rows.append(row); prev = row
        return rows

    def corner(ra, ia, rb, ib):
        """închide colțul dintre două fuste care pleacă din același vârf de sus"""
        for k in range(1, nz + 1):
            a0, a1, b0, b1 = ra[k - 1][ia], ra[k][ia], rb[k - 1][ib], rb[k][ib]
            if a0 is b0:
                bm.faces.new((a0, b1, a1))
            else:
                bm.faces.new((a0, b0, b1, a1))
    S = {}
    if 'y0' in sides:
        S['y0'] = skirt([top[i][0] for i in range(nx + 1)], (0, -1))
    if 'y1' in sides:
        S['y1'] = skirt([top[i][ny] for i in range(nx + 1)][::-1], (0, 1))
    if 'x1' in sides:
        S['x1'] = skirt([top[nx][j] for j in range(ny + 1)][::-1], (1, 0))
        if 'y0' in S:
            corner(S['y0'], -1, S['x1'], -1)
        if 'y1' in S:
            corner(S['x1'], 0, S['y1'], 0)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me); coll.objects.link(o)
    me.materials.append(bpy.data.materials[mat])
    so = o.modifiers.new('Grosime', 'SOLIDIFY'); so.thickness = thick; so.offset = 1.0
    t = bpy.data.textures.get('T_tesatura') or bpy.data.textures.new('T_tesatura', 'CLOUDS')
    t.noise_scale = 0.12; t.noise_depth = 2
    d = o.modifiers.new('Cute', 'DISPLACE'); d.texture = t; d.strength = noise; d.mid_level = 0.5
    ss = o.modifiers.new('Moale', 'SUBSURF'); ss.levels = 1; ss.render_levels = 2
    o['pat_nou'] = True
    return o


soft_box('Pat_HALD_soclu_umbra', 0.20, 2.10, -2.57, -1.03, 0.0, 0.025, 'R_Negru_mat')
soft_box('Pat_HALD_cadru', 0.19, 2.15, -2.60, -1.00, 0.025, 0.32, OAK, bevel=0.004, seg=2)
soft_box('Pat_HALD_tablie', 0.15, 0.19, -2.62, -0.98, 0.025, 1.05, OAK, bevel=0.004, seg=2)
soft_box('Pat_saltea', 0.20, 2.13, -2.58, -1.02, 0.32, 0.52, LIN, bevel=0.03, seg=4)
drape('Pat_pilota', 0.74, 2.13, -2.58, -1.02, 0.585, 0.25, LIN, thick=0.06, noise=0.012)
soft_box('Pat_pilota_rasfrant', 0.66, 0.90, -2.62, -0.98, 0.585, 0.635, LIN, bevel=0.022, seg=4, subsurf=2, noise=0.006)
# perne sprijinite de tăblie (65 × 45, groase 14), înclinate 15° spre tăblie
soft_box('Pat_perna_1', 0.31, 0.45, -1.73, -1.07, 0.52, 0.97, LIN, bevel=0.04, seg=4, subsurf=2, noise=0.005, rot=('Y', -15), pivot=(0.45, -1.4, 0.52))
soft_box('Pat_perna_2', 0.31, 0.45, -2.53, -1.87, 0.52, 0.97, LIN, bevel=0.04, seg=4, subsurf=2, noise=0.005, rot=('Y', -15), pivot=(0.45, -2.2, 0.52))
soft_box('Pat_perna_deco', 0.47, 0.59, -2.03, -1.57, 0.52, 0.84, 'R_Pled_greige', bevel=0.035, seg=4, subsurf=2, noise=0.004, rot=('Y', -12), pivot=(0.59, -1.8, 0.52))
drape('Pat_pled', 1.68, 2.06, -2.59, -1.01, 0.655, 0.2, 'R_Pled_greige', sides=('y0', 'y1'), thick=0.016, noise=0.005, out=0.13)
for o in bpy.data.objects:
    if o.get('pat_nou'):
        o.location = (DX, DY, 0.0)

# =====================================================================  DRAPERII / VOAL
def voal_material():
    m = bpy.data.materials['R_Voal_alb']
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (600, 0)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (0, 200)
    b.inputs['Base Color'].default_value = srgb_lin((246, 244, 238)); b.inputs['Roughness'].default_value = 0.9
    tr = nt.nodes.new('ShaderNodeBsdfTranslucent'); tr.location = (0, -100)
    tr.inputs['Color'].default_value = srgb_lin((250, 248, 242))
    tp = nt.nodes.new('ShaderNodeBsdfTransparent'); tp.location = (200, -250)
    m1 = nt.nodes.new('ShaderNodeMixShader'); m1.location = (250, 50); m1.inputs['Fac'].default_value = 0.55
    m2 = nt.nodes.new('ShaderNodeMixShader'); m2.location = (420, 0); m2.inputs['Fac'].default_value = 0.2
    nt.links.new(b.outputs['BSDF'], m1.inputs[1]); nt.links.new(tr.outputs['BSDF'], m1.inputs[2])
    nt.links.new(m1.outputs['Shader'], m2.inputs[1]); nt.links.new(tp.outputs['BSDF'], m2.inputs[2])
    nt.links.new(m2.outputs['Shader'], out.inputs['Surface'])
    m['nota'] = 'voal translucid fără refracție (06.10.2026)'


def curtain(o, fold=0.11, sheer=False):
    """refă plasa unei draperii ca pliuri sinusoidale netede, în același contur"""
    M = o.matrix_world
    pts = [M @ Vector(c) for c in o.bound_box]
    lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
    along = 0 if (hi.x - lo.x) >= (hi.y - lo.y) else 1
    dep = 1 - along
    W = hi[along] - lo[along]
    amp = max((hi[dep] - lo[dep]) / 2 - 0.002, 0.008)
    cen = (hi[dep] + lo[dep]) / 2
    ncol = max(60, int(W / fold * 16))
    nrow = 36
    rnd = random.Random(o.name)
    ph = [rnd.uniform(-0.25, 0.25) for _ in range(4)]
    bm = bmesh.new()
    grid = []
    for r in range(nrow):
        z = lo.z + (hi.z - lo.z) * r / (nrow - 1)
        tz = r / (nrow - 1)
        row = []
        for c in range(ncol):
            s = lo[along] + W * c / (ncol - 1)
            k = 2 * math.pi * (s - lo[along]) / fold
            a = amp * (0.82 + 0.18 * math.sin(k * 0.13 + ph[0])) * (0.92 + 0.08 * tz)
            d = cen + a * math.sin(k + ph[1] + 0.35 * math.sin(tz * 3.1 + ph[2]))
            co = Vector((0, 0, z)); co[along] = s; co[dep] = d
            row.append(bm.verts.new(M.inverted() @ co))
        grid.append(row)
    for r in range(nrow - 1):
        for c in range(ncol - 1):
            f = bm.faces.new((grid[r][c], grid[r][c + 1], grid[r + 1][c + 1], grid[r + 1][c]))
            f.smooth = True
    me = o.data
    old = me.copy(); old.name = me.name + '_zigzag_vechi'; old.use_fake_user = True
    bm.to_mesh(me); bm.free()
    for mod in list(o.modifiers):
        o.modifiers.remove(mod)
    if not sheer:
        so = o.modifiers.new('Grosime', 'SOLIDIFY'); so.thickness = 0.002
    ss = o.modifiers.new('Moale', 'SUBSURF'); ss.levels = 1; ss.render_levels = 1


voal_material()
nc = 0
for o in list(bpy.data.objects):
    if o.type == 'MESH' and (o.name.startswith('D_Voal_') or o.name.startswith('Draperie_blackout_')):
        curtain(o, sheer=o.name.startswith('D_Voal_')); nc += 1
print('DRAPERII refăcute:', nc)

# =====================================================================  CAMERA D_01
cam = bpy.data.objects['D_01_pat_noptiere']
cam.location = (3.0, -2.85, 1.45)
tgt = Vector((0.45 + DX, -1.62 + DY, 0.62))
cam.rotation_euler = (tgt - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 17.0
# unghi nou: dulapul de dormitor, corpul din spatele patului și tabloul (piesele noi de pe 06.10)
c4 = bpy.data.objects.get('D_04_dulap_tablou')
if c4 is None:
    c4 = bpy.data.objects.new('D_04_dulap_tablou', cam.data.copy())
    bpy.data.collections['CAMERE'].objects.link(c4)
c4.location = (3.05, -0.75, 1.5)
c4.rotation_euler = (Vector((1.0, -3.3, 1.05)) - c4.location).to_track_quat('-Z', 'Y').to_euler()
c4.data.lens = 17.0
c4['expunere'] = 0.5
c4['expunere_noapte'] = -0.1

# =====================================================================  MUCHII ROTUNJITE la mobilier (doar randare)
FURN = {'R_Egger_W1000_ST9_alb', 'R_Egger_U702_ST9_Cashmere', 'R_Stejar_natural_H1145'}
nbv = 0
for o in bpy.data.objects:
    if o.type != 'MESH' or o.hide_render or o.get('pat_nou'):
        continue
    if not any(m and m.name in FURN for m in o.data.materials):
        continue
    d = o.dimensions
    if min(d) < 0.008 or len(o.data.vertices) > 64 or any(m.type == 'BEVEL' for m in o.modifiers):
        continue
    bv = o.modifiers.new('Muchie_1mm', 'BEVEL'); bv.width = 0.001; bv.segments = 2; bv.limit_method = 'ANGLE'
    bv.angle_limit = math.radians(40); bv.harden_normals = True
    nbv += 1
print('MUCHII rotunjite pe', nbv, 'piese')
print('BAIE_DORMITOR_OK')
if SAVE:
    bpy.ops.wm.save_mainfile()
