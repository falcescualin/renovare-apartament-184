"""Rulează: blender --background apartament_184_randare.blend --python randeaza_R04.py -- <camere|ALL> <eșantioane> <lățime> <înălțime> <zi|noapte> [dir_ieșire]
Ca randeaza.py, plus EXPUNERE AUTOMATĂ pe fiecare unghi (06.10.2026): înainte de randarea finală se face o
randare rapidă (400 × 250, 16 eșantioane, cu denoising), se măsoară mediana luminozității afișate și se
corectează expunerea până când mediana ajunge la țintă (zi 0,58, seară 0,42; cameră cu „tinta” proprie), în maximum 6 pași, ±2,5 EV
față de valoarea salvată pe cameră. Valoarea găsită se scrie pe cameră („expunere_auto” / „expunere_auto_noapte”).
Nu salvează .blend."""
import bpy, sys, os, time, math

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
cams = argv[0] if argv else "ALL"
samples = int(argv[1]) if len(argv) > 1 else 384
w = int(argv[2]) if len(argv) > 2 else 1920
h = int(argv[3]) if len(argv) > 3 else 1200
mode = argv[4] if len(argv) > 4 else "zi"
OUT = argv[5] if len(argv) > 5 else os.path.join(r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\randari", mode)
TARGET = 0.58 if mode == "zi" else 0.42
TMP = os.path.join(os.environ.get("TEMP", OUT), "ap184_expunere.png")
os.makedirs(OUT, exist_ok=True)

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'
prefs.get_devices()
for d in prefs.devices:
    d.use = (d.type == 'OPTIX')
sc.cycles.device = 'GPU'
sc.cycles.use_denoising = True

if mode == "noapte":
    sun = bpy.data.objects.get("R_Soare")
    if sun:
        sun.hide_render = True
    bg = next(n for n in sc.world.node_tree.nodes if n.type == 'BACKGROUND')
    bg.inputs["Strength"].default_value = 0.004
    for o in bpy.data.objects:
        if o.type == 'LIGHT' and o.name.startswith("R_Umplere_"):
            o.hide_render = True
    for mn, s in (("R_LED_alb_cald", 10.0), ("R_Plafoniera_LED", 4.0)):
        m = bpy.data.materials.get(mn)
        if m:
            em = next(x for x in m.node_tree.nodes if x.type == 'EMISSION')
            em.inputs["Strength"].default_value = s


def median_lum(path):
    im = bpy.data.images.load(path, check_existing=False)
    px = im.pixels[:]
    lum = sorted(0.2126 * px[i] + 0.7152 * px[i + 1] + 0.0722 * px[i + 2] for i in range(0, len(px), 4 * 3))
    bpy.data.images.remove(im)
    return lum[len(lum) // 2]


def auto_exposure(cam, base):
    target = float(cam.get('tinta_noapte' if mode == 'noapte' else 'tinta', TARGET))     # țintă proprie pe cameră (ex. baia, cu pereți închiși)
    sc.cycles.samples = 16
    sc.render.resolution_x, sc.render.resolution_y = 400, 250
    sc.render.filepath = TMP
    ev = base
    for _ in range(6):
        sc.view_settings.exposure = ev
        bpy.ops.render.render(write_still=True)
        med = max(median_lum(TMP), 0.02)
        if abs(med - target) < 0.025:
            break
        ev += max(-1.5, min(1.5, 2.4 * math.log2(target / med)))      # AgX comprimă luminile: pas mai mare
        ev = max(base - 2.5, min(base + 2.5, ev))
    return round(ev, 2), round(med, 3)


names = [o.name for o in bpy.data.collections["CAMERE"].objects] if cams == "ALL" else cams.split(",")
key = "expunere_noapte" if mode == "noapte" else "expunere"
for n in names:
    t = time.time()
    sc.camera = bpy.data.objects[n]
    base = float(sc.camera.get(key, sc.view_settings.exposure))
    ev, med = auto_exposure(sc.camera, base)
    sc.camera[key.replace("expunere", "expunere_auto")] = ev
    sc.view_settings.exposure = ev
    sc.cycles.samples = samples
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    sc.render.filepath = os.path.join(OUT, n + ".png")
    bpy.ops.render.render(write_still=True)
    print("RANDAT", mode, n, "expunere %.2f (salvată %.2f, mediană probă %.2f)" % (ev, base, med), "%.0fs" % (time.time() - t), flush=True)
