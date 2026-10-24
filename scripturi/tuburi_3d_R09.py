"""FreeCAD 3D comparison: conduits, proposed fixings, architectural context."""
import FreeCAD as App, Part, json, math
from pathlib import Path
ROOT=Path('C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
D=json.loads((ROOT/'output/pdf/Apartament_184_Tuburi_prinderi_R09.json').read_text(encoding='utf-8'))
M=json.loads((ROOT/'tmp/termic_model.json').read_text(encoding='utf-8'))
F=json.loads((ROOT/'tmp/mobilier_plan.json').read_text(encoding='utf-8'))['items']
doc=App.newDocument('montaj_electric_R09_3D')
root=doc.addObject('App::Part','Comparatie_R09');root.Label='R09 | distributie prin sapa | plafoniere existente | DE COORDONAT'
context=doc.addObject('App::Part','Arhitectura');context.Label='PERETI | contur real; vedere cu pereti taiati la 700 mm';root.addObject(context)
walls=[]
for e in M['wall_edges']:
 if len(e)==2:
  walls.append(Part.makeLine(App.Vector(*e[0],0),App.Vector(*e[1],0)).extrude(App.Vector(0,0,700)))
o=doc.addObject('Part::Feature','Pereti_sectionati');o.Label='Pereti / contur existent, taiat pentru vizibilitate';o.Shape=Part.makeCompound(walls);context.addObject(o)
furn=[]
for f in F:
 for q in f.get('polys') or [f['poly']]:
  furn.append(Part.makePolygon([App.Vector(x,y,0) for x,y in q+q[:1]]))
o=doc.addObject('Part::Feature','Mobilier_punctat');o.Label='Mobilier / contur punctat de referinta';o.Shape=Part.makeCompound(furn);context.addObject(o)
variants={}
for v,d in D['variants'].items():
 g=doc.addObject('App::Part','Varianta_'+v);g.Label=v+' | '+'DISTRIBUTIE PARDOSEALA / URCARI LA APARATAJ';root.addObject(g);variants[v]=g
 for t in d['tubes']:
  shapes=[]
  for a,b in zip(t['points'],t['points'][1:]):
   av=App.Vector(*a);bv=App.Vector(*b);direction=bv-av
   shapes.append(Part.makeCylinder(t['diameter_proposed_mm']/2,direction.Length,av,direction))
  ob=doc.addObject('Part::Feature',v+'_'+t['id']);ob.Label=t['id']+' | '+t['source']+' > '+t['destination']+' | '+t['circuit'];ob.Shape=Part.makeCompound(shapes);g.addObject(ob)
  for name,value in [('DeLa',t['source']),('PanaLa',t['destination']),('Circuit',t['circuit']),('Montaj',t['mounting']),('CoordonateAxaJSON',json.dumps(t['points']))]:
   ob.addProperty('App::PropertyString',name,'Montaj');setattr(ob,name,value)
  ob.addProperty('App::PropertyInteger','DiametruPropus_mm','Montaj');ob.DiametruPropus_mm=t['diameter_proposed_mm']
  ob.addProperty('App::PropertyString','Statut','Montaj');ob.Statut='Gabarit de comparatie. Axele suprapuse reprezinta tuburi distincte; vezi registrul SG pentru numar. Coturile au nevoie de raza reala a tubului.'
 g.addProperty('App::PropertyString','Cote');g.Cote='Cota grafica axa -30 mm provizorie. Grosime pardoseala DE MASURAT. Nu se taie placa.'
 g.addProperty('App::PropertyString','Statut');g.Statut='Dozele existente din model raman sus si accesibile. Pozarea separata a tuburilor, traversarile si prinderile necesita coordonare dupa masuratori.'
lightgroup=doc.addObject('App::Part','Iluminat_existent');root.addObject(lightgroup)
lightgroup.Label='Puncte de lumina de pastrat | pozitiile modelului de verificat'
for l in D['existing_lights']:
 ob=doc.addObject('Part::Feature','Existent_'+l['id']);lightgroup.addObject(ob)
 ob.Shape=Part.makeSphere(45,App.Vector(*l['model_endpoint']))
 ob.Label=l['id']+' | EXISTENT, tub de verificat | fara traseu nou prescris'
 ob.addProperty('App::PropertyString','Statut');ob.Statut=l['status']

doc.recompute()
assert all(o.Shape.isValid() for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull())
doc.saveAs(str(ROOT/'montaj_electric_R09_3D.FCStd'))
print('R09 floor proposal saved; existing ceiling connections intentionally unprescribed')
