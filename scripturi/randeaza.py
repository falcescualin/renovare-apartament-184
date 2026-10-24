"""Ruleaza: blender --background apartament_184_randare.blend --python randeaza.py -- <camere|ALL> <esantioane> <latime> <inaltime> <zi|noapte>
Randeaza camerele cerute in randari/<zi|noapte>/ (PNG, cate un fisier per unghi). Nu salveaza .blend."""
import bpy, sys, os, time

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
cams = argv[0] if argv else "ALL"
samples = int(argv[1]) if len(argv) > 1 else 512
w = int(argv[2]) if len(argv) > 2 else 1920
h = int(argv[3]) if len(argv) > 3 else 1200
mode = argv[4] if len(argv) > 4 else "zi"
OUT = os.path.join(r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\randari", mode)
os.makedirs(OUT, exist_ok=True)

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'
prefs.get_devices()
for d in prefs.devices:
    d.use = (d.type == 'OPTIX')
sc.cycles.device = 'GPU'
sc.cycles.samples = samples
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100

if mode == "noapte":
    sun = bpy.data.objects.get("R_Soare")
    if sun:
        sun.hide_render = True
    bg = next(n for n in sc.world.node_tree.nodes if n.type == 'BACKGROUND')
    bg.inputs["Strength"].default_value = 0.004          # cer de noapte, abia vizibil
    for o in bpy.data.objects:                             # seara: fara lumini de umplere, doar corpurile reale
        if o.type == 'LIGHT' and o.name.startswith("R_Umplere_"):
            o.hide_render = True
    for mn, s in (("R_LED_alb_cald", 10.0), ("R_Plafoniera_LED", 4.0)):
        m = bpy.data.materials.get(mn)
        if m:
            em = next(x for x in m.node_tree.nodes if x.type == 'EMISSION')
            em.inputs["Strength"].default_value = s

names = [o.name for o in bpy.data.collections["CAMERE"].objects] if cams == "ALL" else cams.split(",")
for n in names:
    t = time.time()
    sc.camera = bpy.data.objects[n]
    key = "expunere_noapte" if mode == "noapte" else "expunere"
    if key in sc.camera:
        sc.view_settings.exposure = float(sc.camera[key])
    sc.render.filepath = os.path.join(OUT, n + ".png")
    bpy.ops.render.render(write_still=True)
    print("RANDAT", mode, n, "%.0fs" % (time.time() - t), flush=True)
