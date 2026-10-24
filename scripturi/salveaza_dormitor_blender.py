import bpy,json,shutil
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(r'C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
B=R/'blender_export_dormitor_actual'
records=json.loads((B/'furniture_manifest.json').read_text(encoding='utf-8'))['parts']
shutil.copy2(bpy.data.filepath,R/'_arhiva/2026-10-06_salvare_finala/blender_sesiune_salvata.blend')
before_names=set(bpy.data.objects.keys())
log=[]
for rec in records:
 pid=rec['part_id'][:63];old=bpy.data.objects.get(pid)
 bpy.ops.object.select_all(action='DESELECT')
 prior=set(bpy.data.objects)
 bpy.ops.wm.obj_import(filepath=str(B/rec['mesh_file']),forward_axis='Y',up_axis='Z')
 new=[o for o in set(bpy.data.objects)-prior if o.type=='MESH'];assert len(new)==1
 o=new[0]
 for vert in o.data.vertices:vert.co*=.001
 if old:
  mats=list(old.data.materials);old.data=o.data;old.matrix_world=Matrix.Identity(4)
  old.data.materials.clear()
  for mat in mats:old.data.materials.append(mat)
  bpy.data.objects.remove(o,do_unlink=True);o=old
 else:
  o.name=pid
  col=bpy.data.collections.get(rec['assembly'])
  if not col:
   col=bpy.data.collections.new(rec['assembly']);bpy.context.scene.collection.children.link(col)
  for c in list(o.users_collection):c.objects.unlink(o)
  col.objects.link(o)
  rgb=rec['color_rgb'];name='Dormitor_'+('_'.join(str(round(c*255)) for c in rgb))
  mat=bpy.data.materials.get(name) or bpy.data.materials.new(name);mat.diffuse_color=(*rgb,1);mat.use_nodes=True
  bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*rgb,1);bs.inputs['Roughness'].default_value=.5
  if 'LED_vertical_' in pid:
   bs.inputs['Emission Color'].default_value=(1,.72,.35,1);bs.inputs['Emission Strength'].default_value=2
  o.data.materials.clear();o.data.materials.append(mat)
 for key in ['part_id','source_document','source_object','label','assembly']:o[key]=rec.get(key,'')
 o.hide_render=False;o.hide_set(False);log.append(pid)
for o in bpy.data.objects:
 if o.name=='Dulap_dormitor' or o.name.startswith('Noptiera_sud__'):
  o.hide_render=True;o.hide_set(True)
 if o.name in ['D_Perna_1','D_Perna_2','D_Perna_deco_1','D_Pilota','D_Pled'] and not o.get('pat_deplasat_150mm'):
  o.location.x+=.15;o['pat_deplasat_150mm']=True
bpy.context.view_layer.update()
errors=[]
for rec in records:
 o=bpy.data.objects[rec['part_id'][:63]]
 pts=[o.matrix_world@Vector(c) for c in o.bound_box]
 lo=[min(p[i] for p in pts)*1000 for i in range(3)];hi=[max(p[i] for p in pts)*1000 for i in range(3)]
 delta=max(abs(lo[i]-rec['bbox_min_mm'][i]) for i in range(3))
 delta=max(delta,max(abs(hi[i]-rec['bbox_min_mm'][i]-rec['bbox_mm'][i]) for i in range(3)))
 if delta>1:errors.append([o.name,delta])
assert not errors,errors
bpy.ops.wm.save_mainfile()
(R/'output/Salvare_sincronizare_Blender.json').write_text(json.dumps({'synced_parts':len(log),'geometry_errors':errors,'blend':bpy.data.filepath,'hidden':['Dulap_dormitor','Noptiera_sud'], 'bed_textiles_moved_mm':150},indent=2),encoding='utf-8')
print('SYNC_SAVED_OK',len(log),'parts, bbox error <=1 mm')
