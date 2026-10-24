import FreeCAD as App, Part, json
from pathlib import Path
R=Path(r'C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
a=App.getDocument('apartament_184');d=App.getDocument('dulap_dormitor')
offset=App.Vector(150,-3845,0)
obstacles={n:a.getObject(n).Shape for n in ['Pat','Noptiera_sud','Noptiera_nord']}
results=[]
for i in range(4):
 leaf=d.getObject('Usa_'+str(i+1)).Shape.copy()
 handle=d.getObject('Maner_usa_'+str(i+1)).Shape.copy()
 leaf=Part.makeCompound([leaf,handle]);leaf.translate(offset)
 pivot=App.Vector(150+i*550+(18 if i%2==0 else 532),-3254,0)
 sign=1 if i%2==0 else -1
 hit=None;hits=[]
 for deg in range(0,156):
  s=leaf.copy();s.rotate(pivot,App.Vector(0,0,1),sign*deg)
  coll=[n for n,o in obstacles.items() if s.common(o).Volume>0.5]
  if coll:
   if hit is None:hit={'angle_deg':deg,'objects':coll}
   hits.append(deg)
 results.append({'door':i+1,'first_collision':hit,'colliding_angles_deg':hits,'assumed_hinge_axis':list(pivot)})
draw=[]
for i in [0,3]:
 for j in range(4):
  s=Part.makeCompound([d.getObject('Sertar_'+str(i)+'_'+str(j)).Shape,d.getObject('Front_sertar_'+str(i)+'_'+str(j)).Shape,d.getObject('Maner_'+str(i)+'_'+str(j)).Shape]);s.translate(offset)
  first=None
  for dist in range(0,451,5):
   q=s.copy();q.translate(App.Vector(0,dist,0))
   coll=[n for n,o in obstacles.items() if q.common(o).Volume>.5]
   if coll:first={'extension_mm':dist,'objects':coll};break
  draw.append({'bay':i,'drawer':j,'first_collision':first})
(R/'output/Analiza_deschidere_dulap_dormitor.json').write_text(json.dumps({'doors':results,'drawers':draw,'status':'Verificare geometrie CAD; axe balamale propuse; nu simuleaza cinematica feroneriei reale'},indent=2),encoding='utf-8')
print(json.dumps({'doors':[{k:v for k,v in o.items() if k!='colliding_angles_deg'} for o in results],'drawers':draw}))
# Separate read-only study document; furniture is not changed.
study=App.newDocument('Analiza_usi_dormitor')
for name,color in [('Pat',(.75,.76,.78)),('Noptiera_sud',(.95,.55,.18))]:
 o=study.addObject('Part::Feature',name);o.Shape=obstacles[name];o.ViewObject.ShapeColor=color;o.ViewObject.Transparency=35
o=study.addObject('Part::Feature','Dulap_contur');o.Shape=Part.makeBox(2200,600,2360,offset);o.ViewObject.ShapeColor=(.7,.75,.8);o.ViewObject.Transparency=88
for i in range(4):
 base=d.getObject('Usa_'+str(i+1)).Shape.copy();base.translate(offset)
 pv=App.Vector(*results[i]['assumed_hinge_axis']);sign=1 if i%2==0 else -1
 deg=results[i]['first_collision']['angle_deg'] if results[i]['first_collision'] else 90
 base.rotate(pv,App.Vector(0,0,1),sign*deg)
 ob=study.addObject('Part::Feature','Usa_'+str(i+1));ob.Label='Usa '+str(i+1)+' | '+str(deg)+' grade'+(' | COLIZIUNE' if results[i]['first_collision'] else '')
 ob.Shape=base;ob.ViewObject.ShapeColor=(.9,.15,.15) if results[i]['first_collision'] else (.2,.65,.35)
study.recompute();Gui.activeDocument().activeView().viewTop();Gui.activeDocument().activeView().fitAll();Gui.updateGui()
study.saveAs(str(R/'output/Analiza_usi_dormitor.FCStd'))
Gui.activeDocument().activeView().saveImage(str(R/'output/Analiza_usi_dormitor.png'),1400,1100,'White')
