import FreeCAD as App, FreeCADGui as Gui, Part,json
from pathlib import Path
R=Path('C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
data=json.loads((R/'output/pdf/Apartament_184_Trasee_complete_R04.json').read_text(encoding='utf-8'))
doc=App.newDocument('montaj_electric_R04')
root=doc.addObject('App::Part','Montaj_R04');root.Label='R04 - trasee complete, cote propuse'
arch=doc.addObject('App::Part','Contur');root.addObject(arch)
for i,edge in enumerate(json.loads((R/'tmp/termic_model.json').read_text(encoding='utf-8'))['wall_edges']):
 if len(edge)!=2:continue
 obj=doc.addObject('Part::Feature','Perete_'+str(i));obj.Shape=Part.makePolygon([App.Vector(x,y,0) for x,y in edge]);obj.ViewObject.LineColor=(.65,.65,.65);arch.addObject(obj)
groups={}
for r in data['routes']:
 key=r['circuit'].replace(',','_').replace(' ','_').replace('/','_')
 if key not in groups:
  g=doc.addObject('App::Part','Circuit_'+key);g.Label=r['circuit']+' - afisati pentru inspectie';root.addObject(g);groups[key]=g
 obj=doc.addObject('Part::Feature','Ruta_'+r['id']);obj.Label=r['id']+' / '+r['desc'];groups[key].addObject(obj)
 # Compound segments preserve intentional retraced routes to local junctions.
 pts=[App.Vector(*p) for p in r['points']]
 obj.Shape=Part.makeCompound([Part.makeLine(a,b) for a,b in zip(pts,pts[1:])])
 obj.ViewObject.LineColor=(.12,.42,.77);obj.ViewObject.LineWidth=3
 for name,value in [('Sursa',r['source']),('Circuit',r['circuit']),('CapAtXYZ',str(r['endpoint'])),('Plansa',r.get('sheet','')+' / '+r.get('detail_sheet','')),('Geometrie','Continuitate verificata; montaj de validat pe teren'),('Coordonate',json.dumps(r['points']))]:
  obj.addProperty('App::PropertyString',name,'Montaj');setattr(obj,name,value)
 obj.Visibility=False
 marker=doc.addObject('Part::Feature','Capat_'+r['id']);marker.Label='Capat real '+r['id'];marker.Shape=Part.makeSphere(23,pts[-1]);groups[key].addObject(marker);marker.ViewObject.ShapeColor=(.12,.42,.77);marker.Visibility=False
# Show one auditable route on opening; others can be enabled individually.
doc.getObject('Ruta_P02').Visibility=True;doc.getObject('Capat_P02').Visibility=True
doc.recompute()
invalid=[o.Name for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
assert not invalid,invalid
doc.saveAs(str(R/'montaj_electric_R04.FCStd'))
if 'apartament_184' in App.listDocuments():
 apt=App.getDocument('apartament_184');link=apt.getObject('Montaj_electric_R04_link') or apt.addObject('App::Link','Montaj_electric_R04_link');link.setLink(root);link.Label='R04 - traseu complet la fiecare punct';link.Visibility=False;apt.recompute();apt.save()
App.setActiveDocument(doc.Name);Gui.activeDocument().activeView().viewTop();Gui.activeDocument().activeView().fitAll()
print(json.dumps({'saved':str(R/'montaj_electric_R04.FCStd'),'routes':len(data['routes']),'invalid':invalid}))
