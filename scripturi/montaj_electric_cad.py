import FreeCAD as App, FreeCADGui as Gui, Part, json
from FreeCAD import Vector
from pathlib import Path
ROOT=Path('C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
data=json.loads((ROOT/'output/pdf/Apartament_184_Montaj_electric_R03.json').read_text(encoding='utf-8'))
doc=App.getDocument('montaj_electric_R03') if 'montaj_electric_R03' in App.listDocuments() else App.newDocument('montaj_electric_R03')
root=doc.getObject('Montaj_R03') or doc.addObject('App::Part','Montaj_R03');root.Label='Montaj electric R03 - cote propuse, validare pe teren'
def group(name):
 o=doc.getObject(name) or doc.addObject('App::Part',name);root.addObject(o);return o
tr=group('Coridoare_TR');br=group('Coborari_B');hd=group('HDMI');ar=group('Contur_apartament')
def make(name,label,pts,color,parent):
 ps=[Vector(*p) for p in pts];clean=[ps[0]]
 for v in ps[1:]:
  if (v-clean[-1]).Length>.01:clean.append(v)
 o=doc.getObject(name) or doc.addObject('Part::Feature',name);o.Label=label;o.Shape=Part.makePolygon(clean) if len(clean)>1 else Part.makeSphere(15,clean[0]);o.ViewObject.LineColor=color;o.ViewObject.ShapeColor=color;o.ViewObject.LineWidth=3;parent.addObject(o);return o
def note(o,key,value):
 if key not in o.PropertiesList:o.addProperty('App::PropertyString',key,'Montaj')
 setattr(o,key,value)
for t in data['trunks']:
 o=make(t['id'],t['id']+' / '+t['a']+'-'+t['b'],[(x,y,2400) for x,y in t['route']],(.8,.2,.15),tr)
 note(o,'Circuite',', '.join(t['circuits']));note(o,'Nota','Coridor comun de montaj, tuburi separate pe circuite; nu reprezinta un singur cablu. Axa propusa Z2400.')
for g in data['drops']:
 pts=[(x,y,2400) for x,y in g['branch']]+[(g['x'],g['y'],g['zmin'])]
 o=make(g['id'],g['id']+' / '+g['room']+' / '+','.join(g['points']),pts,(.15,.45,.75),br)
 for key,value in [('Puncte',','.join(g['points'])),('ModMontaj',g['mode']),('NodOrigine',g['anchor']),('Circuite',','.join(g['circuits']))]:note(o,key,value)
for id,x,y,z1,z2 in [('H01',3700,-2650,350,1350),('H02',3550,-1707,400,1410)]:
 o=make(id,id+' - tub HDMI ascuns si inlocuibil',[(x,y,z1),(x,y,z2)],(.5,.25,.7),hd);note(o,'Nota','Axa propusa in spatele panoului TV. Tub ales dupa mufa si raza cablului; capete accesibile. H02 rezerva.')
geom=json.loads((ROOT/'tmp/termic_model.json').read_text(encoding='utf-8'))
for i,edge in enumerate(geom['wall_edges']):
 if len(edge)==2:make('Perete_'+str(i),'Contur CAD',[(x,y,0) for x,y in edge],(.65,.65,.65),ar)
doc.recompute();doc.saveAs(str(ROOT/'montaj_electric_R03.FCStd'))
apt=App.getDocument('apartament_184');link=apt.getObject('Montaj_electric_R03_link') or apt.addObject('App::Link','Montaj_electric_R03_link');link.setLink(root);link.Label='Montaj electric R03 - trasee si HDMI';link.Visibility=False;apt.recompute();apt.save()
App.setActiveDocument(doc.Name);Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
print(json.dumps({'saved':str(ROOT/'montaj_electric_R03.FCStd'),'trunks':len(data['trunks']),'drops':len(data['drops']),'invalid':[o.Name for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]},ensure_ascii=False))
