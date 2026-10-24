"""Rulează: blender --background apartament_184_randare.blend --python materiale_kronospan_blender.py [-- --nu-salva]
Decorurile Kronospan alese pe 06.10.2026 în locul celor Egger, din imaginile oficiale Kronospan (texturi/kronospan):
- R_Egger_W1000_ST9_alb      → Kronospan 8685 BS Snow White (corpuri);
- R_Egger_U702_ST9_Cashmere  → Kronospan 5981 BS Cashmere (fronturi, noptiere, comoda TV, soclu, măști);
- R_Stejar_natural_H1145     → Kronospan 3025 SN Light Vintage Oak / Sonoma (echivalentul H1145 din tabelele de cant):
  scanarea plăcii întregi 2070 × 2800 mm, la mărime reală, cu fibra pe lungimea fiecărei piese și alt loc din placă
  pentru fiecare piesă (ca la debitarea reală); porii vin din aceeași scanare (relief_3025_pori.png).
Albul și cashmere-ul: culoarea din imaginea oficială, adusă la scara de luminozitate a scenei (ca vechile culori Egger),
relief din fotografia structurii BS (relief_BS.png, ~30 cm pe imagine, repetare în oglindă), luciu satinat.
Numele materialelor rămân (le folosesc și alte scripturi); decorul real e în proprietatea „decor”.
Mașina de spălat vase e incorporabilă: fața ei primește front cashmere."""
import bpy, bmesh, os, sys, random

ROOT = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
K = os.path.join(ROOT, 'texturi', 'kronospan')
SAVE = '--nu-salva' not in sys.argv
UVB, UVF = 'UV_box', 'UV_fibra'
SCAN, SW, SL = os.path.join(K, '3025_2070x2800mm.jpg'), 2.07, 2.80


def srgb_lin(c):
    return tuple(((v / 255 + 0.055) / 1.055) ** 2.4 if v / 255 > 0.04045 else v / 255 / 12.92 for v in c) + (1.0,)


def clear(m):
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (400, 0)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (100, 0)
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return nt, b


def tex(nt, path, noncolor, vec, x, y, ext='REPEAT'):
    n = nt.nodes.new('ShaderNodeTexImage')
    n.image = bpy.data.images.load(path, check_existing=True)
    n.image.colorspace_settings.name = 'Non-Color' if noncolor else 'sRGB'
    n.interpolation = 'Cubic'
    n.extension = ext
    n.location = (x, y)
    nt.links.new(vec, n.inputs['Vector'])
    return n


def uvvec(nt, uv, scale, x=-1100, y=0):
    u = nt.nodes.new('ShaderNodeUVMap'); u.uv_map = uv; u.location = (x, y)
    mp = nt.nodes.new('ShaderNodeMapping'); mp.location = (x + 200, y)
    mp.inputs['Scale'].default_value = scale
    nt.links.new(u.outputs['UV'], mp.inputs['Vector'])
    return mp.outputs['Vector']


def maprange(nt, val, a, b, c, d, x, y):
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.location = (x, y); mr.clamp = True
    mr.inputs['From Min'].default_value, mr.inputs['From Max'].default_value = a, b
    mr.inputs['To Min'].default_value, mr.inputs['To Max'].default_value = c, d
    nt.links.new(val, mr.inputs['Value'])
    return mr.outputs['Result']


def uni(name, rgb, decor, structura, rough=(0.38, 0.5), bump=0.12):
    """PAL uni: culoare plată (decorul e uniform), relief din fotografia structurii, luciu satinat variabil"""
    m = bpy.data.materials[name]
    nt, b = clear(m)
    b.inputs['Base Color'].default_value = srgb_lin(rgb)
    b.inputs['Specular IOR Level'].default_value = 0.5
    vec = uvvec(nt, UVB, (1 / 0.305,) * 3)
    r = tex(nt, os.path.join(K, 'relief', 'relief_%s.png' % structura), True, vec, -650, -250, 'MIRROR')
    nt.links.new(maprange(nt, r.outputs['Color'], 0, 1, rough[1], rough[0], -350, 0), b.inputs['Roughness'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.location = (-200, -250)
    bp.inputs['Strength'].default_value = bump
    bp.inputs['Distance'].default_value = 0.0004
    nt.links.new(r.outputs['Color'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    m['decor'] = decor
    m.diffuse_color = srgb_lin(rgb)


def stejar(name, decor):
    m = bpy.data.materials[name]
    nt, b = clear(m)
    vec = uvvec(nt, UVF, (1.0, 1.0, 1.0))
    c = tex(nt, SCAN, False, vec, -650, 250)
    # luminozitatea scanării adusă la scara scenei (ca la culorile uni), fără să schimbe nuanța
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.location = (-300, 250)
    mx.inputs['Factor'].default_value = 1.0
    nt.links.new(c.outputs['Color'], mx.inputs['A'])
    mx.inputs['B'].default_value = (0.78, 0.78, 0.78, 1.0)
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    p = tex(nt, os.path.join(K, 'relief', 'relief_3025_pori.png'), True, vec, -650, -150)
    nt.links.new(maprange(nt, p.outputs['Color'], 0, 1, 0.66, 0.46, -350, -50), b.inputs['Roughness'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.location = (-200, -250)
    bp.inputs['Strength'].default_value = 0.35
    bp.inputs['Distance'].default_value = 0.0006
    bp.invert = True                      # porii sunt mai închiși la culoare = adânciți
    nt.links.new(p.outputs['Color'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    m['decor'] = decor


def uv_fibra(o, rnd):
    """UV în coordonatele scanării: pe fiecare față, fibra (V, lungimea plăcii de 2,80 m) merge pe latura cea mai lungă
    a piesei din planul feței; fiecare piesă primește alt loc din placă."""
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    lay = bm.loops.layers.uv.get(UVF) or bm.loops.layers.uv.new(UVF)
    M = o.matrix_world
    R = M.to_3x3()
    pts = [M @ v.co for v in me.vertices]
    lo = [min(p[i] for p in pts) for i in range(3)]
    ext = [max(p[i] for p in pts) - lo[i] for i in range(3)]
    ou, ov = rnd.uniform(0.02, 0.6), rnd.uniform(0.02, 0.6)
    for f in bm.faces:
        n = R @ f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        a, b = [i for i in range(3) if i != ax]
        g, t = (a, b) if ext[a] >= ext[b] else (b, a)        # g = axa fibrei
        for l in f.loops:
            co = M @ l.vert.co
            u = ou + (co[t] - lo[t]) / SW
            v = ov + (co[g] - lo[g]) / SL
            l[lay].uv = (u % 1.0 if u > 1 else u, v % 1.0 if v > 1 else v)
    bm.to_mesh(me); bm.free()


# ---------------------------------------------------------------- 1. albul și cashmere-ul
# culoarea din imaginea oficială × raportul folosit și la Egger (randare / imagine oficială): alb 0,93, cashmere 0,86
uni('R_Egger_W1000_ST9_alb', (237, 237, 236), 'Kronospan 8685 BS Snow White', 'BS', rough=(0.36, 0.48))
uni('R_Egger_U702_ST9_Cashmere', (175, 169, 160), 'Kronospan 5981 BS Cashmere', 'BS', rough=(0.4, 0.52))
# ---------------------------------------------------------------- 2. stejarul
stejar('R_Stejar_natural_H1145', 'Kronospan 3025 SN Light Vintage Oak (Sonoma)')
rnd = random.Random(3025)
n = 0
for o in bpy.data.objects:
    if o.type == 'MESH' and any(m and m.name == 'R_Stejar_natural_H1145' for m in o.data.materials):
        if o.data.users > 1:
            o.data = o.data.copy()
        uv_fibra(o, rnd); n += 1
print('STEJAR obiecte:', n)
# ---------------------------------------------------------------- 3. mașina de vase incorporabilă: front cashmere
mv = bpy.data.objects.get('Bucatarie_custom__M2_masina_vase')
if mv is not None:
    me = mv.data
    cas = bpy.data.materials['R_Egger_U702_ST9_Cashmere']
    if cas.name not in [m.name for m in me.materials if m]:
        me.materials.append(cas)
    ci = [m.name if m else '' for m in me.materials].index(cas.name)
    R = mv.matrix_world.to_3x3()
    xs = [(mv.matrix_world @ v.co).x for v in me.vertices]
    for p in me.polygons:
        nn = R @ p.normal
        if nn.x > 0.9 and abs((mv.matrix_world @ p.center).x - max(xs)) < 1e-4:
            p.material_index = ci
    print('MASINA_VASE: front cashmere')
print('KRONOSPAN_OK')
if SAVE:
    bpy.ops.wm.save_mainfile()
