"""Ruleaza: blender --background apartament_184_randare.blend --python plan_3d_sus.py -- <esantioane>
Vedere de sus fotorealista a intregului apartament, fara tavan (macheta). Capetele peretilor sunt gri inchis.
Fundal transparent; adnotarile se adauga dupa, cu adnoteaza_plan_3d.py. Salveaza si scena separat (plan_3D.blend)."""
import bpy, bmesh, sys, os, math

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
samples = int(argv[0]) if argv else 256
BASE = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
OUT = os.path.join(BASE, "randari", "plan_3D_sus_baza.png")
CX, CY, ORTHO = 5.575, -2.20, 14.0            # centrul si latimea cadrului (m) -> folosite si la adnotare
W, H = 3200, 2200

sc = bpy.context.scene

# fara tavane, fara exterior, fara lumini interioare, fara plafoniere
for n in ("R_Tavan_apartament", "Balcon_tavan", "R_Sol_exterior"):
    o = bpy.data.objects.get(n)
    if o: o.hide_render = True
for o in bpy.data.objects:
    if o.name.startswith(("R_Bloc_departare", "R_Umplere_", "R_Lumina_")):
        o.hide_render = True
    elif o.type == 'MESH' and any(s.material and s.material.name == "R_Plafoniera_LED" for s in o.material_slots):
        o.hide_render = True
# bucataria fara corpurile de sus, masca si tubulatura hotei: se vad blatul si plita
from mathutils import Vector
for o in bpy.data.collections["Bucatarie_custom"].all_objects:
    if o.type == 'MESH' and min((o.matrix_world @ Vector(c)).z for c in o.bound_box) > 1.30:
        o.hide_render = True

# capetele peretilor (fetele orizontale de sus) primesc material gri inchis
cap = bpy.data.materials.get("R_Capac_perete") or bpy.data.materials.new("R_Capac_perete")
cap.use_nodes = True
p = cap.node_tree.nodes.get("Principled BSDF")
p.inputs["Base Color"].default_value = (0.05, 0.052, 0.056, 1); p.inputs["Roughness"].default_value = 0.85
w = bpy.data.objects.get("Pereti")
if w:
    me = w.data
    if cap.name not in me.materials: me.materials.append(cap)
    ci = list(me.materials).index(me.materials[cap.name])
    bm = bmesh.new(); bm.from_mesh(me)
    zmax = max((w.matrix_world @ v.co).z for v in bm.verts)
    n = 0
    for f in bm.faces:
        if f.normal.z > 0.95 and abs((w.matrix_world @ f.calc_center_median()).z - zmax) < 0.02:
            f.material_index = ci; n += 1
    bm.to_mesh(me); bm.free()
    print("CAPACE", n, "z", round(zmax, 3))

# camera ortografica de sus
cd = bpy.data.cameras.new("CAM_plan_3D"); cam = bpy.data.objects.new("CAM_plan_3D", cd); sc.collection.objects.link(cam)
cd.type = 'ORTHO'; cd.ortho_scale = ORTHO
cam.location = (CX, CY, 20.0); cam.rotation_euler = (0, 0, 0)
cd.clip_start = 1.0; cd.clip_end = 40.0
sc.camera = cam

# cer neutru (fara nuanta albastra) + soare aproape de zenit, umbre scurte spre dreapta-jos
wn = sc.world.node_tree
bg = next(n for n in wn.nodes if n.type == 'BACKGROUND')
for l in list(bg.inputs["Color"].links): wn.links.remove(l)
bg.inputs["Color"].default_value = (0.93, 0.93, 0.92, 1)
bg.inputs["Strength"].default_value = 1.1
sun = bpy.data.objects.get("R_Soare")
sun.hide_render = False
sun.data.energy = 3.0; sun.data.angle = math.radians(8); sun.data.color = (1.0, 0.96, 0.9)
sun.rotation_euler = (math.radians(24), 0, math.radians(135))

sc.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'; prefs.get_devices()
for d in prefs.devices: d.use = (d.type == 'OPTIX')
sc.cycles.device = 'GPU'; sc.cycles.samples = samples
sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
sc.view_settings.exposure = 0.2
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BASE, "plan_3D.blend"), copy=True)
print("PLAN3D", OUT)
