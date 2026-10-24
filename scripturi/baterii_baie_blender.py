"""Rulează: blender --background apartament_184_randare.blend --python baterii_baie_blender.py   (07.10.2026)
Aduce în scena de randare piesele din baie.FCStd create de baterii_baie_freecad.py (OBJ în tmp/baterii_obj, mm → m):
Coloana_dus_* (coloana de duș 9710N) și Baterie_lavoar (9707N, înlocuiește simbolul cilindric). Material nou R_Gun_grey_satin,
copie a lui R_Inox_periat cu culoarea înmulțită cu un gri-grafit. Idempotent: reia geometria dacă obiectele există. Salvează .blend."""
import bpy, os

OBJ = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\tmp\baterii_obj"
NAMES = ['Coloana_dus_baterie', 'Coloana_dus_teava', 'Coloana_dus_palarie', 'Coloana_dus_suport_para',
         'Coloana_dus_para', 'Coloana_dus_furtun', 'Baterie_lavoar']
PRE = 'Baie_custom__'


def gun_grey():
    m = bpy.data.materials.get('R_Gun_grey_satin')
    if m:
        return m
    src = bpy.data.materials['R_Inox_periat']
    m = src.copy(); m.name = 'R_Gun_grey_satin'
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    l = next((l for l in nt.links if l.to_node == b and l.to_socket.name == 'Base Color'), None)
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.location = (-200, 300)
    mx.inputs['Factor'].default_value = 1.0
    mx.inputs['B'].default_value = (0.30, 0.31, 0.34, 1)
    if l:
        nt.links.new(l.from_socket, mx.inputs['A'])
    else:
        mx.inputs['A'].default_value = b.inputs['Base Color'].default_value
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = max(b.inputs['Roughness'].default_value, 0.32) if not any(
        k.to_socket.name == 'Roughness' for k in nt.links) else b.inputs['Roughness'].default_value
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


old = bpy.data.objects.get(PRE + 'Baterie_lavoar')
col = old.users_collection[0] if old else bpy.context.scene.collection
m_gg = gun_grey()
done = []
for n in NAMES:
    vs, fs = read_obj(os.path.join(OBJ, n + '.obj'))
    o = bpy.data.objects.get(PRE + n)
    if o is None:
        me = bpy.data.meshes.new(PRE + n)
        o = bpy.data.objects.new(PRE + n, me)
        col.objects.link(o)
    else:
        me = o.data
        me.clear_geometry()
    me.from_pydata(vs, [], fs)
    me.update(); me.validate()
    for p in me.polygons:
        p.use_smooth = False
    me.materials.clear(); me.materials.append(m_gg)
    o.matrix_world.identity()
    o['produs'] = 'Alessandro Design ' + ('9707N' if n == 'Baterie_lavoar' else '9710N')
    bpy.context.view_layer.objects.active = o
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=0.3)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    done.append((n, len(vs), tuple(round(d * 1000) for d in o.dimensions)))
print('BATERII_OK', done)
bpy.ops.wm.save_mainfile()
