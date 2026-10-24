"""Ruleaza cu: blender --background apartament_184.blend --python verificare_blender.py
Randari rapide (Workbench) de verificare: vedere de sus ortografica + perspectiva. Nu salveaza .blend."""
import bpy, os, json
from mathutils import Vector

OUT = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\blender_export\verificare"
os.makedirs(OUT, exist_ok=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'
sc.display.shading.color_type = 'MATERIAL'
sc.display.shading.show_shadows = True
sc.render.resolution_x, sc.render.resolution_y = 1600, 1000

pts = [o.matrix_world @ Vector(c) for o in sc.objects
       if o.type == 'MESH' and not o.hide_render for c in o.bound_box]
mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
ctr = (mn + mx) / 2

cam_data = bpy.data.cameras.new("CAM_verificare")
cam = bpy.data.objects.new("CAM_verificare", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam

cam_data.type = 'ORTHO'
cam_data.ortho_scale = max(mx.x - mn.x, mx.y - mn.y) * 1.08
cam.location = (ctr.x, ctr.y, mx.z + 10)
cam.rotation_euler = (0, 0, 0)
sc.render.filepath = os.path.join(OUT, "verificare_sus.png")
bpy.ops.render.render(write_still=True)

cam_data.type = 'PERSP'
cam_data.lens = 24
cam.location = (ctr.x + 8, ctr.y - 9, 11)
cam.rotation_euler = (ctr - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.render.filepath = os.path.join(OUT, "verificare_perspectiva.png")
bpy.ops.render.render(write_still=True)

print("VERIF", json.dumps({"bbox_m": [round(v, 3) for v in (mx - mn)], "min": [round(v, 3) for v in mn]}))
