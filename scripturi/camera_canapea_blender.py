"""Rulează: blender --background apartament_184_randare.blend --python camera_canapea_blender.py   (07.10.2026)
Adaugă camera CZ_05_canapea (privește spre canapeaua Puma de lângă peretele din est) în colecția CAMERE. Idempotent. Salvează .blend."""
import bpy
from mathutils import Vector
if 'CZ_05_canapea' not in bpy.data.objects:
    src = bpy.data.objects['CZ_01_ansamblu_perete_TV']
    cam = src.copy(); cam.data = src.data.copy(); cam.name = 'CZ_05_canapea'; cam.data.name = 'CZ_05_canapea'
    cam.data.lens = 22
    bpy.data.collections['CAMERE'].objects.link(cam)
    cam.location = Vector((4.15, -1.75, 1.35))
    d = Vector((7.1, -3.0, 0.62)) - cam.location
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    for k in ('tinta', 'tinta_noapte'):
        if k in src: cam[k] = src[k]
print('CAMERA_OK')
bpy.ops.wm.save_mainfile()
