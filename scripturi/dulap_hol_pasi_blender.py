"""Ruleaza: blender --background apartament_184_randare.blend --python dulap_hol_pasi_blender.py
Imagini pas cu pas (stil instructiuni de montaj) pentru dulapul din hol: piesele noi din fiecare pas sunt colorate.
Iese in tmp/dulap_hol_pasi/pas_XX.png. Nu salveaza .blend."""
import bpy, os, math
from mathutils import Vector

BASE = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14"
OUT = os.path.join(BASE, "tmp", "dulap_hol_pasi")
os.makedirs(OUT, exist_ok=True)
PRE = "Dulap_hol_custom__"
col = bpy.data.collections["Dulap_hol_custom"]
parts = {o.name[len(PRE):]: o for o in col.all_objects if o.type == 'MESH'}

sc = bpy.context.scene
for o in sc.objects:
    o.hide_render = o.name[len(PRE):] not in parts or not o.name.startswith(PRE)

def grp(*names):
    out = []
    for n in names:
        out += [k for k in parts if k == n or (n.endswith("*") and k.startswith(n[:-1]))]
    return out

STEPS = [
    ("01", grp("Baza", "Picior_*"), "baza"),
    ("02", grp("Lateral_stanga", "Lateral_oblic"), "fata"),
    ("03", grp("Despartitor_central", "Despartitor_3"), "fata"),
    ("04", grp("Polita_*"), "fata"),
    ("05", grp("Blat_sus"), "fata"),
    ("06", grp("Spate_HDF"), "spate"),
    ("07", grp("Raft_colt_*"), "fata"),
    ("08", grp("Soclu", "Plinta_colt"), "jos"),
    ("09", grp("Sertar_pantofi_*", "Front_sertar_*"), "fata"),
    ("10", grp("Bara_haine_*", "LED_profil_*", "Senzor_usa_*", "Sursa_LED_24V"), "sus"),
    ("11", grp("Usa_oglinda_*"), "fata"),
    ("12", grp("Usa_sus_oglinda_*"), "fata"),
    ("13", grp("Masca_tavan"), "fata"),
    ("final", [], "fata"),
]

ALB, NOU, GRI = (0.93, 0.93, 0.91, 1), (0.33, 0.72, 0.67, 1), (0.25, 0.25, 0.25, 1)
U702, OGL = (0.74, 0.71, 0.67, 1), (0.80, 0.86, 0.90, 1)

def base_color(k):
    if k.startswith(("Picior", "Senzor")): return GRI
    if k.startswith(("Usa_",)): return OGL
    if k.startswith(("Front_", "Plinta", "Masca")): return U702
    return ALB

# Workbench: lumina de studio, contur, fundal transparent
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.light = 'STUDIO'; sh.color_type = 'OBJECT'
sh.show_object_outline = True; sh.object_outline_color = (0.09, 0.17, 0.23)
sh.show_cavity = True; sh.cavity_type = 'BOTH'; sh.cavity_ridge_factor = 1.0; sh.cavity_valley_factor = 1.0
sh.show_shadows = False; sh.show_specular_highlight = False
sc.render.film_transparent = True
sc.display_settings.display_device = 'sRGB'; sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = 0
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1800, 1500, 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'

C = Vector((8.48, -5.26, 1.25))                     # centrul dulapului (m)
cd = bpy.data.cameras.new("CAM_pasi"); cam = bpy.data.objects.new("CAM_pasi", cd); sc.collection.objects.link(cam)
cd.type = 'ORTHO'; cd.ortho_scale = 3.25; sc.camera = cam
DIRS = {"fata": Vector((0.55, 1.0, 0.55)), "spate": Vector((0.55, -1.0, 0.45)), "jos": Vector((0.55, 1.0, 0.4)), "sus": Vector((0.35, 1.0, 0.2)), "baza": Vector((0.55, 1.0, 0.55))}
# (centru, scara) pentru fiecare vedere
FRAME = {"fata": (Vector((8.48, -5.26, 1.25)), 4.1), "spate": (Vector((8.48, -5.26, 1.25)), 4.1),
         "jos": (Vector((8.48, -5.10, 0.35)), 3.0), "sus": (Vector((8.48, -5.26, 1.85)), 3.0),
         "baza": (Vector((8.48, -5.26, 0.10)), 3.0)}

def aim(view):
    d = DIRS[view].normalized()
    c0, sc_ = FRAME[view]
    cam.location = c0 + d * 12
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    cd.ortho_scale = sc_

from bpy_extras.object_utils import world_to_camera_view
import json
ANC = {}
shown = []
for code, new, view in STEPS:
    shown += new
    for k, o in parts.items():
        o.hide_render = k not in shown and code != "final"
        o.color = NOU if k in new else base_color(k)
    aim(view)
    bpy.context.view_layer.update()
    ANC[code] = {}
    for k in (new or list(parts)):
        o = parts[k]
        bb = [o.matrix_world @ Vector(cc) for cc in o.bound_box]
        ctr = sum(bb, Vector()) / 8
        uv = world_to_camera_view(sc, cam, ctr)
        ANC[code][k] = [round(uv.x, 4), round(uv.y, 4)]
    sc.render.filepath = os.path.join(OUT, "pas_%s.png" % code)
    bpy.ops.render.render(write_still=True)
    print("PAS", code, len(new))
json.dump(ANC, open(os.path.join(OUT, 'ancore.json'), 'w'), indent=1)
