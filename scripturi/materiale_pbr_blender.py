"""Rulează: blender --background <scena.blend> --python materiale_pbr_blender.py [-- --nu-salva]
Leagă texturile PBR din texturi/ (CC0: Poly Haven, ambientCG) de materialele scenei de randare:
- culoarea rămâne cea din proiect; din textura foto se ia variația (fibra lemnului, pete, țesătura) ca un multiplicator
  fin, iar la travertin, inox și covor culoarea vine direct din textură;
- relieful (hartă normal + deplasare ca bump) și luciul (hartă de rugozitate, mapată pe un interval realist);
- coordonate: hartă UV „UV_box” proiectată pe cub, în metri, ca textura să aibă mărimea reală a materialului;
- cerul și exteriorul din geamuri: HDRI 8K buikslotermeerplein; soarele R_Soare rămâne.
PAL-ul Egger (W1000, U702, H1145) rămâne procedural până vin scanările oficiale Egger."""
import bpy, bmesh, os, glob, json, sys

ROOT = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
TX = os.path.join(ROOT, 'texturi')
SAVE = '--nu-salva' not in sys.argv
UV = 'UV_box'


def ph(aid, size=None):
    d = os.path.join(TX, 'polyhaven', aid)
    info = json.load(open(os.path.join(d, 'info.json'), encoding='utf-8'))
    f = lambda k: next((os.path.join(d, x) for x in info['maps'] if '_%s_' % k in x), None)
    return dict(color=f('diff'), normal=f('nor_gl'), rough=f('rough'), disp=f('disp'), size=size or info['dimensions_mm'][0] / 1000)


def acg(aid, size):
    d = os.path.join(TX, 'ambientcg', aid)
    f = lambda k: next(iter(glob.glob(os.path.join(d, '*_%s.jpg' % k))), None)
    return dict(color=f('Color'), normal=f('NormalGL'), rough=f('Roughness'), disp=f('Displacement'), size=size)


def hexlin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)


# luminanța liniară a texturilor de culoare (p5, p95), măsurată pe imagini: pentru variația de culoare
LUM = {'wood_floor': (0.099, 0.167), 'white_oak_veneer': (0.173, 0.251), 'smooth_concrete_floor': (0.029, 0.072),
       'poly_wool_herringbone': (0.139, 0.235), 'rough_linen': (0.364, 0.426)}
WOOD, OAK, CONC, PAINT = ph('wood_floor'), ph('white_oak_veneer'), ph('smooth_concrete_floor', 1.6), ph('painted_concrete', 1.5)
PLAST, BOUC, LIN, HERR = ph('white_plaster_02'), ph('wool_boucle', 0.35), ph('rough_linen', 0.3), ph('poly_wool_herringbone', 0.3)
TRAV, METAL, CARP = acg('Travertine009', 0.9), acg('Metal009', 0.35), acg('Carpet016', 0.6)
# material: sursa, variație de culoare (lo, hi) sau 'tex' (culoarea texturii), culoare de proiect (None = cea existentă),
#           rugozitate (lo, hi), tărie normal, bump din deplasare, metalic
SPEC = {
    'R_Parchet_stejar': dict(t=WOOD, lum='wood_floor', var=(0.72, 1.28), col='#C9A57B', rough=(0.38, 0.6), n=0.7, bump=0.12),
    'R_Stejar_deschis_riflaje': dict(t=OAK, lum='white_oak_veneer', var=(0.82, 1.16), col='#D6B48A', rough=(0.45, 0.65), n=0.5),
    'R_Microciment_alb_cald': dict(t=CONC, lum='smooth_concrete_floor', var=(0.84, 1.08), rough=(0.24, 0.52), n=0.55),
    'R_Rasina_epoxidica_gri': dict(t=dict(PAINT, color=None), rough=(0.12, 0.3), n=0.18),
    'R_Vopsea_perete_alb_cald': dict(t=dict(PLAST, color=None), rough=(0.8, 0.92), n=0.15),
    'R_Tavan_alb': dict(t=dict(PLAST, color=None), rough=(0.82, 0.94), n=0.12),
    'R_Boucle_alb': dict(t=dict(BOUC, color=None), rough=(0.8, 0.97), n=1.6, bump=0.7),
    # H1145 Stejar Bardolino natur: provizoriu cu fibra de stejar descărcată, recolorată, până la scanarea oficială Egger
    'R_Stejar_natural_H1145': dict(t=dict(OAK, size=0.6), lum='white_oak_veneer', var=(0.74, 1.22), col='#B98C5F', rough=(0.42, 0.62), n=0.8),
    # PAL Egger ST9 (mat fin): relief foarte fin, culoarea rămâne cea din proiect
    'R_Egger_W1000_ST9_alb': dict(t=dict(PLAST, color=None, size=0.25), rough=(0.42, 0.55), n=0.06),
    'R_Egger_U702_ST9_Cashmere': dict(t=dict(PLAST, color=None, size=0.25), rough=(0.45, 0.58), n=0.06),
    'R_Draperie_in_bej': dict(t=LIN, lum='rough_linen', var=(0.94, 1.05), rough=(0.78, 0.95), n=0.6),
    'R_Voal_alb': dict(t=LIN, lum='rough_linen', var=(0.96, 1.03), rough=(0.8, 0.95), n=0.35),
    'R_Lenjerie_alb': dict(t=LIN, lum='rough_linen', var=(0.95, 1.04), rough=(0.78, 0.95), n=0.5),
    'R_Textil_pat_alb_cald': dict(t=LIN, lum='rough_linen', var=(0.95, 1.04), rough=(0.78, 0.95), n=0.5),
    'R_Perna_teracota': dict(t=LIN, lum='rough_linen', var=(0.93, 1.06), rough=(0.78, 0.95), n=0.6),
    'R_Textil_canapea_gri_bej': dict(t=HERR, lum='poly_wool_herringbone', var=(0.86, 1.12), rough=(0.82, 0.97), n=0.8),
    'R_Pled_greige': dict(t=HERR, lum='poly_wool_herringbone', var=(0.86, 1.12), rough=(0.82, 0.97), n=0.9),
    'R_Textil_scaune': dict(t=HERR, lum='poly_wool_herringbone', var=(0.88, 1.1), rough=(0.82, 0.97), n=0.8),
    'R_Travertin_bej': dict(t=TRAV, var='tex', rough=(0.22, 0.45), n=0.5),
    'R_Inox_periat': dict(t=METAL, var='tex', rough=(0.18, 0.38), n=0.25, metal=1.0),
    'R_Prag_aluminiu_periat': dict(t=METAL, var='tex', rough=(0.22, 0.4), n=0.25, metal=1.0),
    'R_Covor_bej': dict(t=CARP, var='tex', rough=(0.85, 1.0), n=1.0, bump=0.4),
}


def base_color(m, b):
    inp = b.inputs['Base Color']
    return tuple(inp.default_value) if not inp.is_linked else tuple(m.diffuse_color)


def img(nt, path, noncolor, vec, x, y):
    n = nt.nodes.new('ShaderNodeTexImage')
    n.image = bpy.data.images.load(path, check_existing=True)
    n.image.colorspace_settings.name = 'Non-Color' if noncolor else 'sRGB'
    n.interpolation = 'Cubic' if noncolor else 'Linear'
    n.location = (x, y)
    nt.links.new(vec, n.inputs['Vector'])
    return n


def maprange(nt, val, a, b, c, d, x, y):
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.location = (x, y)
    mr.clamp = True
    mr.inputs['From Min'].default_value, mr.inputs['From Max'].default_value = a, b
    mr.inputs['To Min'].default_value, mr.inputs['To Max'].default_value = c, d
    nt.links.new(val, mr.inputs['Value'])
    return mr.outputs['Result']


def upgrade(m, s):
    nt = m.node_tree
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    t = s['t']
    col0 = hexlin(s['col']) if s.get('col') else base_color(m, b)
    for name in ('Base Color', 'Roughness', 'Normal'):
        for l in list(b.inputs[name].links):
            nt.links.remove(l)
    # curăță nodurile procedurale vechi care nu mai ajung la ieșire
    keep = {out.name, b.name}
    changed = True
    while changed:
        changed = False
        for n in list(nt.nodes):
            if n.name in keep:
                continue
            if not any(l.from_node == n for l in nt.links):
                nt.nodes.remove(n)
                changed = True
    tc = nt.nodes.new('ShaderNodeUVMap'); tc.uv_map = UV; tc.location = (-1500, 0)
    mp = nt.nodes.new('ShaderNodeMapping'); mp.location = (-1300, 0)
    mp.inputs['Scale'].default_value = (1 / t['size'],) * 3
    nt.links.new(tc.outputs['UV'], mp.inputs['Vector'])
    vec = mp.outputs['Vector']
    if t.get('color') and s.get('var'):
        ci = img(nt, t['color'], False, vec, -1000, 300)
        if s['var'] == 'tex':
            nt.links.new(ci.outputs['Color'], b.inputs['Base Color'])
        else:
            bw = nt.nodes.new('ShaderNodeRGBToBW'); bw.location = (-700, 300)
            nt.links.new(ci.outputs['Color'], bw.inputs['Color'])
            lo, hi = LUM[s['lum']]
            v = maprange(nt, bw.outputs['Val'], lo, hi, s['var'][0], s['var'][1], -500, 300)
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.location = (-250, 300)
            mx.inputs['Factor'].default_value = 1.0
            mx.inputs['A'].default_value = col0
            nt.links.new(v, mx.inputs['B'])
            nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    else:
        b.inputs['Base Color'].default_value = col0
    if t.get('rough'):
        ri = img(nt, t['rough'], True, vec, -1000, 0)
        nt.links.new(maprange(nt, ri.outputs['Color'], 0, 1, s['rough'][0], s['rough'][1], -500, 0), b.inputs['Roughness'])
    if t.get('normal'):
        ni = img(nt, t['normal'], True, vec, -1000, -300)
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.location = (-500, -300); nm.uv_map = UV
        nm.inputs['Strength'].default_value = s.get('n', 1.0)
        nt.links.new(ni.outputs['Color'], nm.inputs['Color'])
        norm = nm.outputs['Normal']
        if s.get('bump') and t.get('disp'):
            di = img(nt, t['disp'], True, vec, -1000, -600)
            bp = nt.nodes.new('ShaderNodeBump'); bp.location = (-250, -450)
            bp.inputs['Strength'].default_value = s['bump']
            bp.inputs['Distance'].default_value = 0.002
            nt.links.new(di.outputs['Color'], bp.inputs['Height'])
            nt.links.new(norm, bp.inputs['Normal'])
            norm = bp.outputs['Normal']
        nt.links.new(norm, b.inputs['Normal'])
    if 'metal' in s:
        b.inputs['Metallic'].default_value = s['metal']
    m['pbr'] = os.path.basename(os.path.dirname(t.get('normal') or t.get('color')))


def box_uv(o):
    """UV pe cub, în metri (coordonate globale): fiecare față primește axele perpendiculare pe normala ei"""
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    lay = bm.loops.layers.uv.get(UV) or bm.loops.layers.uv.new(UV)
    shared = me.users > 1
    M = o.matrix_world
    R = M.to_3x3()
    for f in bm.faces:
        n = (R @ f.normal) if not shared else f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for l in f.loops:
            co = (M @ l.vert.co) if not shared else l.vert.co * o.scale[0]
            u, v = ((co.y, co.z), (co.x, co.z), (co.x, co.y))[ax]
            l[lay].uv = (u, v)
    bm.to_mesh(me); bm.free()
    uvl = me.uv_layers[UV]
    me.uv_layers.active = uvl
    uvl.active_render = True


# 0. microciment pe pereții băii și pe măștile din baie (în proiect: kit microciment pereți, M010),
#    în loc de vopseaua albă: fețele peretelui aflate în întregime în conturul băii
MC = bpy.data.materials['R_Microciment_alb_cald']
X0, X1, Y0, Y1 = 0.145, 2.455, -5.555, -3.915
pw = bpy.data.objects.get('Pereti')
if pw is not None:
    me = pw.data
    if MC.name not in [m.name for m in me.materials if m]:
        me.materials.append(MC)
    idx = [m.name if m else '' for m in me.materials].index(MC.name)
    M = pw.matrix_world
    nb = 0
    for p in me.polygons:
        vs = [M @ me.vertices[i].co for i in p.vertices]
        if abs((M.to_3x3() @ p.normal).z) < 0.2 and all(X0 <= v.x <= X1 and Y0 <= v.y <= Y1 for v in vs):
            p.material_index = idx; nb += 1
    print('PERETI_BAIE microciment:', nb, 'fețe')
for n in ('Baie_custom__Masca_cada_nise', 'Baie_custom__Masca_WC_fata', 'Baie_custom__Masca_WC_lateral_lavoar',
          'Baie_custom__Masca_WC_lateral_stanga', 'Baie_custom__Masca_WC_polita_sus'):
    o = bpy.data.objects.get(n)
    if o is not None:
        o.data.materials.clear(); o.data.materials.append(MC)
# 1. UV pe obiectele care folosesc materialele noi
done, objs = set(), 0
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    if any(m and m.name in SPEC for m in o.data.materials) and o.data.name not in done:
        box_uv(o); done.add(o.data.name); objs += 1
# 2. materialele
for name, s in SPEC.items():
    m = bpy.data.materials.get(name)
    if m is None:
        print('LIPSA', name); continue
    upgrade(m, s)
# 3. cerul: HDRI 8K
sc = bpy.context.scene
w = sc.world
nt = w.node_tree
bg = next(n for n in nt.nodes if n.type == 'BACKGROUND')
for n in list(nt.nodes):
    if n.type in ('TEX_SKY', 'TEX_ENVIRONMENT', 'MAPPING', 'TEX_COORD'):
        nt.nodes.remove(n)
env = nt.nodes.new('ShaderNodeTexEnvironment'); env.location = (-400, 0)
env.image = bpy.data.images.load(os.path.join(TX, 'hdri', 'buikslotermeerplein_8k.hdr'), check_existing=True)
tco = nt.nodes.new('ShaderNodeTexCoord'); tco.location = (-800, 0)
mpw = nt.nodes.new('ShaderNodeMapping'); mpw.location = (-600, 0)
mpw.inputs['Rotation'].default_value = (0, 0, float(os.environ.get('HDRI_ROT', '0')) * 3.14159265 / 180)
nt.links.new(tco.outputs['Generated'], mpw.inputs['Vector'])
nt.links.new(mpw.outputs['Vector'], env.inputs['Vector'])
nt.links.new(env.outputs['Color'], bg.inputs['Color'])
bg.inputs['Strength'].default_value = float(os.environ.get('HDRI_STR', '1.0'))
# 4. expunere: baia era arsă (microcimentul are acum variație și se vede abia cu expunere corectă)
for cam, ev in {'B_01_baie': 0.7}.items():
    c = bpy.data.objects.get(cam)
    if c is not None:
        c['expunere'] = ev
print('PBR_OK obiecte cu UV:', objs, '| materiale:', len(SPEC), '| HDRI tărie', bg.inputs['Strength'].default_value)
if SAVE:
    bpy.ops.wm.save_mainfile()
