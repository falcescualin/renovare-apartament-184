"""Rulează: blender --background apartament_184_randare.blend --python canapea_puma_blender.py   (07.10.2026)
Aduce în scena de randare canapeaua Puma (Dedeman 8119379) din apartament_184.FCStd (OBJ în tmp/canapea_obj, mm → m),
ascunde canapeaua veche (obiectul „Canapea” și pernele C_Perna_sezut_*, C_Perna_spatar_*) și mută cele două perne decorative
pe șezutul noii canapele. Material nou R_Textil_canapea_crem (copie a lui R_Textil_canapea_gri_bej, mai deschisă și caldă). Salvează .blend."""
import bpy, os

OBJ = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\tmp\canapea_obj"
MAT = {'Canapea_lada': 'R_Textil_canapea_crem', 'Canapea_brate': 'R_Textil_canapea_crem', 'Canapea_spatar': 'R_Textil_canapea_crem',
       'Canapea_perne_sezut': 'R_Textil_canapea_crem', 'Canapea_picioare_lemn': 'R_Parchet_stejar',
       'Canapea_picioare_negre': 'R_Metal_negru'}


def crem():
    m = bpy.data.materials.get('R_Textil_canapea_crem')
    if m:
        return m
    m = bpy.data.materials['R_Textil_canapea_gri_bej'].copy(); m.name = 'R_Textil_canapea_crem'
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    l = next((l for l in nt.links if l.to_node == b and l.to_socket.name == 'Base Color'), None)
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.location = (-200, 300)
    mx.inputs['Factor'].default_value = 1.0
    mx.inputs['B'].default_value = (1.28, 1.20, 1.02, 1)
    if l:
        nt.links.new(l.from_socket, mx.inputs['A'])
    else:
        mx.inputs['A'].default_value = b.inputs['Base Color'].default_value
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    return m


def read_obj(path):
    vs, fs = [], []
    for ln in open(path, encoding='utf-8'):
        if ln.startswith('v '):
            _, x, y, z = ln.split()[:4]
            vs.append((float(x) / 1000, float(y) / 1000, float(z) / 1000))
        elif ln.startswith('f '):
            fs.append(tuple(int(t.split('/')[0]) - 1 for t in ln.split()[1:]))
    return vs, fs


old = bpy.data.objects['Canapea']
col = old.users_collection[0]
crem()
done = []
for n, mn in MAT.items():
    vs, fs = read_obj(os.path.join(OBJ, n + '.obj'))
    o = bpy.data.objects.get(n)
    if o is None:
        me = bpy.data.meshes.new(n); o = bpy.data.objects.new(n, me); col.objects.link(o)
    else:
        me = o.data; me.clear_geometry()
    me.from_pydata(vs, [], fs); me.update(); me.validate()
    for p in me.polygons:
        p.use_smooth = False
    me.materials.clear(); me.materials.append(bpy.data.materials[mn])
    o['produs'] = 'Dedeman 8119379 Canapea extensibilă Puma 215 × 76 × 87 cm'
    bpy.context.view_layer.objects.active = o
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=0.4)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    # rotunjire fină la randare, fără a schimba geometria nominală
    if n in ('Canapea_lada', 'Canapea_brate', 'Canapea_perne_sezut', 'Canapea_spatar'):
        bpy.ops.object.shade_smooth()
        if hasattr(o.data, 'set_sharp_from_angle'):
            o.data.set_sharp_from_angle(angle=0.6)
    done.append((n, tuple(round(d * 1000) for d in o.dimensions)))

for nm in ['Canapea'] + [o.name for o in bpy.data.objects if o.name.startswith(('C_Perna_sezut_', 'C_Perna_spatar_'))]:
    o = bpy.data.objects[nm]
    o.hide_render = True; o.hide_viewport = True
    o['inlocuit_07_10'] = 'canapea Puma'

# pernele decorative se așază pe șezutul nou: spătarul e mai la perete cu ~0,21 m, șezutul cu 4 cm mai jos
for nm in ('C_Perna_deco_1', 'C_Perna_deco_2'):
    o = bpy.data.objects[nm]
    if not o.get('mutata_puma'):
        o.location.x += 0.211; o.location.z -= 0.04
        o['mutata_puma'] = True
print('CANAPEA_OK', done)
bpy.ops.wm.save_mainfile()
