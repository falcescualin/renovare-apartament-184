"""Rulează: blender --background apartament_184_randare.blend --python texturi_complete_blender.py
Folosește în materialele de randare toate hărțile PBR descărcate în texturi/ care nu erau încă legate (06.10.2026):
- Carpet016 și Travertine009: ocluzie ambientală (AO) înmulțită peste culoare; Travertine009: displacement ca bump fin;
- Metal009: harta Metalness în Metallic și displacement ca bump fin (R_Inox_periat, R_Prag_aluminiu_periat);
- Concrete046 (microciment olive grey): harta Normal GL a lui Concrete046 se adună cu cea din plastered_wall_04;
  rugozitatea din plastered_wall_04 se amestecă cu cea din Concrete046; difuzia din plastered_wall_04 ca variație fină de ton;
- painted_concrete: harta de difuzie ca variație fină de ton peste rășina epoxidică gri;
- wool_boucle: harta de difuzie ca variație fină de ton peste bucle;
- obiectele care mai aveau materiale plate din FreeCAD: profilele și cadrele metalice → R_Inox_periat, picioarele negre → R_Metal_negru,
  rama tabloului → R_Negru_mat.
Idempotent: nu adaugă de două ori aceleași noduri (marchează materialul cu proprietatea „texturi_complete”). Salvează .blend."""
import bpy, os

TX = os.path.join(r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14", "texturi")


def img(path, data=True):
    i = bpy.data.images.load(os.path.join(TX, path), check_existing=True)
    i.colorspace_settings.name = 'Non-Color' if data else 'sRGB'
    return i


def tex(nt, path, vec_from, data=True, loc=(0, 0)):
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = img(path, data); n.location = loc
    nt.links.new(vec_from, n.inputs['Vector'])
    return n


def node(nt, typ, loc=(0, 0), **kw):
    n = nt.nodes.new(typ); n.location = loc
    for k, v in kw.items():
        setattr(n, k, v)
    return n


def bsdf(nt):
    return next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')


def base_src(nt, b):
    l = next((l for l in nt.links if l.to_node == b and l.to_socket.name == 'Base Color'), None)
    return l.from_socket if l else None


def tint(nt, b, path, lo, hi, loc):
    """înmulțește culoarea de bază cu luminanța unei hărți de difuzie, remapată în [lo, hi]"""
    mp = nt.nodes['Mapping'].outputs['Vector']
    t = tex(nt, path, mp, data=False, loc=(loc[0], loc[1]))
    bw = node(nt, 'ShaderNodeRGBToBW', (loc[0] + 250, loc[1]))
    nt.links.new(t.outputs['Color'], bw.inputs['Color'])
    rm = node(nt, 'ShaderNodeMapRange', (loc[0] + 450, loc[1]), clamp=True)
    rm.inputs['From Min'].default_value = 0.0; rm.inputs['From Max'].default_value = 1.0
    rm.inputs['To Min'].default_value = lo; rm.inputs['To Max'].default_value = hi
    nt.links.new(bw.outputs['Val'], rm.inputs['Value'])
    mx = node(nt, 'ShaderNodeMix', (loc[0] + 700, loc[1]), data_type='RGBA', blend_type='MULTIPLY')
    mx.inputs['Factor'].default_value = 1.0
    src = base_src(nt, b)
    if src is not None:
        nt.links.new(src, mx.inputs['A'])
    else:
        mx.inputs['A'].default_value = b.inputs['Base Color'].default_value
    g = node(nt, 'ShaderNodeCombineColor', (loc[0] + 550, loc[1] - 160))
    for s in ('Red', 'Green', 'Blue'):
        nt.links.new(rm.outputs['Result'], g.inputs[s])
    nt.links.new(g.outputs['Color'], mx.inputs['B'])
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])


def ao(nt, b, path, loc):
    mp = nt.nodes['Mapping'].outputs['Vector']
    t = tex(nt, path, mp, data=True, loc=loc)
    mx = node(nt, 'ShaderNodeMix', (loc[0] + 300, loc[1]), data_type='RGBA', blend_type='MULTIPLY')
    mx.inputs['Factor'].default_value = 0.8
    src = base_src(nt, b)
    nt.links.new(src, mx.inputs['A'])
    nt.links.new(t.outputs['Color'], mx.inputs['B'])
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])


def bump_after_normal(nt, b, path, strength, dist, loc):
    """displacement ca bump peste normala existentă: Normal Map → Bump → BSDF"""
    mp = nt.nodes['Mapping'].outputs['Vector']
    t = tex(nt, path, mp, data=True, loc=loc)
    bp = node(nt, 'ShaderNodeBump', (loc[0] + 300, loc[1]))
    bp.inputs['Strength'].default_value = strength; bp.inputs['Distance'].default_value = dist
    nt.links.new(t.outputs['Color'], bp.inputs['Height'])
    l = next((l for l in nt.links if l.to_node == b and l.to_socket.name == 'Normal'), None)
    if l is not None:
        nt.links.new(l.from_socket, bp.inputs['Normal'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])


done = []

def once(name):
    m = bpy.data.materials.get(name)
    if m is None or m.get('texturi_complete'):
        return None
    m['texturi_complete'] = True
    done.append(name)
    return m

m = once('R_Covor_bej')
if m:
    nt = m.node_tree; ao(nt, bsdf(nt), r'ambientcg\Carpet016\Carpet016_4K-JPG_AmbientOcclusion.jpg', (-900, 500))

m = once('R_Travertin_bej')
if m:
    nt = m.node_tree; b = bsdf(nt)
    ao(nt, b, r'ambientcg\Travertine009\Travertine009_4K-JPG_AmbientOcclusion.jpg', (-900, 500))
    bump_after_normal(nt, b, r'ambientcg\Travertine009\Travertine009_4K-JPG_Displacement.jpg', 0.25, 0.002, (-900, -700))

for name in ('R_Inox_periat', 'R_Prag_aluminiu_periat'):
    m = once(name)
    if m:
        nt = m.node_tree; b = bsdf(nt)
        t = tex(nt, r'ambientcg\Metal009\Metal009_4K-JPG_Metalness.jpg', nt.nodes['Mapping'].outputs['Vector'], loc=(-900, -500))
        nt.links.new(t.outputs['Color'], b.inputs['Metallic'])
        bump_after_normal(nt, b, r'ambientcg\Metal009\Metal009_4K-JPG_Displacement.jpg', 0.1, 0.0005, (-900, -800))

m = once('R_Microciment_olive_gri')
if m:
    nt = m.node_tree; b = bsdf(nt)
    nm_old = nt.nodes['Normal Map']
    t = tex(nt, r'ambientcg\Concrete046\Concrete046_4K-JPG_NormalGL.jpg', nt.nodes['Mapping'].outputs['Vector'], loc=(-900, -900))
    nm2 = node(nt, 'ShaderNodeNormalMap', (-600, -900)); nm2.inputs['Strength'].default_value = 0.5
    nt.links.new(t.outputs['Color'], nm2.inputs['Color'])
    add = node(nt, 'ShaderNodeVectorMath', (-300, -800), operation='ADD')
    nt.links.new(nm_old.outputs['Normal'], add.inputs[0]); nt.links.new(nm2.outputs['Normal'], add.inputs[1])
    nz = node(nt, 'ShaderNodeVectorMath', (-100, -800), operation='NORMALIZE')
    nt.links.new(add.outputs['Vector'], nz.inputs[0])
    bump = nt.nodes['Bump']
    nt.links.new(nz.outputs['Vector'], bump.inputs['Normal'])
    # rugozitate: amestec Concrete046 + plastered_wall_04
    rr = tex(nt, r'polyhaven\plastered_wall_04\plastered_wall_04_rough_4k.jpg', nt.nodes['Mapping.001'].outputs['Vector'], loc=(-900, -1200))
    rm = nt.nodes['Map Range.001']
    mixr = node(nt, 'ShaderNodeMix', (300, -1000), data_type='FLOAT'); mixr.inputs['Factor'].default_value = 0.4
    nt.links.new(rm.outputs['Result'], mixr.inputs['A'])
    r2 = node(nt, 'ShaderNodeMapRange', (-500, -1200), clamp=True)
    r2.inputs['To Min'].default_value = rm.inputs['To Min'].default_value; r2.inputs['To Max'].default_value = rm.inputs['To Max'].default_value
    nt.links.new(rr.outputs['Color'], r2.inputs['Value'])
    nt.links.new(r2.outputs['Result'], mixr.inputs['B'])
    nt.links.new(mixr.outputs['Result'], b.inputs['Roughness'])
    tint(nt, b, r'polyhaven\plastered_wall_04\plastered_wall_04_diff_4k.jpg', 0.80, 1.08, (-900, 900))

m = once('R_Rasina_epoxidica_gri')
if m:
    nt = m.node_tree; tint(nt, bsdf(nt), r'polyhaven\painted_concrete\painted_concrete_diff_4k.jpg', 0.86, 1.10, (-900, 500))

m = once('R_Boucle_alb')
if m:
    nt = m.node_tree; tint(nt, bsdf(nt), r'polyhaven\wool_boucle\wool_boucle_diff_4k.jpg', 0.88, 1.04, (-900, 500))

# obiecte cu materiale plate din FreeCAD → materiale PBR existente
REMAP = {'FC_464e53_t0': 'R_Inox_periat', 'FC_3c4d52_t0': 'R_Inox_periat', 'FC_b8b9b8_t0': 'R_Inox_periat', 'FC_acb9b8_t0': 'R_Inox_periat',
         'FC_9da2a6_t0': 'R_Inox_periat', 'FC_b3b4b3_t0': 'R_Inox_periat', 'FC_333333_t0': 'R_Metal_negru', 'Dormitor_33_38_36': 'R_Negru_mat'}
n = 0
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    for s in o.material_slots:
        if s.material and s.material.name in REMAP and bpy.data.materials.get(REMAP[s.material.name]):
            s.material = bpy.data.materials[REMAP[s.material.name]]; n += 1
# materialele care folosesc nodul „UV Map” au nevoie de UV: obiectele noi fără UV primesc proiecție cub
for o in bpy.data.objects:
    if o.type == 'MESH' and not o.data.uv_layers and any(s.material and s.material.name in ('R_Inox_periat', 'R_Metal_negru', 'R_Negru_mat') for s in o.material_slots):
        bpy.context.view_layer.objects.active = o
        for ob in bpy.context.selected_objects:
            ob.select_set(False)
        o.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.cube_project(cube_size=0.3); bpy.ops.object.mode_set(mode='OBJECT')
print('TEXTURI_COMPLETE materiale:', done, '| obiecte remapate:', n)
bpy.ops.wm.save_mainfile()
