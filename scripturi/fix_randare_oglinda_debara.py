"""Ruleaza: blender --background apartament_184_randare.blend --python fix_randare_oglinda_debara.py
Oglinda de machiaj primeste materialul de oglinda (era emisiva), LED-ul din spatele ei e mai slab,
debaraua primeste mai multa lumina si expunere mai mare. Salveaza .blend."""
import bpy
o = bpy.data.objects["Perete_TV_dormitor_custom__Machiaj_oglinda_LED"]
o.data.materials.clear(); o.data.materials.append(bpy.data.materials["R_Oglinda"])
led = bpy.data.materials["R_LED_alb_cald"]
soft = bpy.data.materials.get("R_LED_oglinda") or led.copy(); soft.name = "R_LED_oglinda"
next(n for n in soft.node_tree.nodes if n.type == 'EMISSION').inputs["Strength"].default_value = 2.5
for n in ("Perete_TV_dormitor_custom__Machiaj_LED_spate_oglinda", "Perete_TV_dormitor_custom__LED_vertical_margine_riflaje"):
    b = bpy.data.objects[n]; b.data.materials.clear(); b.data.materials.append(soft)
bpy.data.objects["R_Lumina_Nisa"].data.energy = 40.0
c = bpy.data.objects["DB_01_debara"]; c["expunere"] = 1.5; c["expunere_noapte"] = 0.4
bpy.ops.wm.save_mainfile()
print("FIX_OK")
