import bpy,shutil,json
from pathlib import Path
R=Path(r'C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
B=R/'_arhiva/2026-10-06_corectie_material_oglinda';B.mkdir(parents=True,exist_ok=True)
shutil.copy2(bpy.data.filepath,B/'inainte.blend')
mirror=bpy.data.objects['Perete_TV_dormitor_custom__Machiaj_oglinda_LED']
ref=bpy.data.objects['Dulap_hol_custom__Usa_oglinda_1']
mirror.data.materials.clear()
for m in ref.data.materials:mirror.data.materials.append(m)
for p in mirror.data.polygons:p.material_index=0
back=bpy.data.objects['Perete_TV_dormitor_custom__Machiaj_LED_spate_oglinda']
back.hide_render=True;back.hide_viewport=True;back.hide_set(True)
mirror.hide_render=False;mirror.hide_viewport=False;mirror.hide_set(False)
assert mirror.data.materials[0]==ref.data.materials[0]
bpy.ops.wm.save_mainfile()
(R/'output/Corectie_oglinda_dormitor.json').write_text(json.dumps({'material':mirror.data.materials[0].name,'same_as_hall':True,'back_panel_hidden':back.hide_render,'cameras':[o.name for o in bpy.data.objects if o.type=='CAMERA']},indent=2))
print('MIRROR_FIXED_SAVED')
