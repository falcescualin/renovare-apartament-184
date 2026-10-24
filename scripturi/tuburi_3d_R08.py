"""FreeCAD 3D comparison: conduits, proposed fixings, architectural context."""
import FreeCAD as App, Part, json, math
from pathlib import Path
ROOT=Path('C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
D=json.loads((ROOT/'output/pdf/Apartament_184_Tuburi_prinderi_R08.json').read_text(encoding='utf-8'))
M=json.loads((ROOT/'tmp/termic_model.json').read_text(encoding='utf-8'))
F=json.loads((ROOT/'tmp/mobilier_plan.json').read_text(encoding='utf-8'))['items']
doc=App.newDocument('montaj_electric_R08_3D')
root=doc.addObject('App::Part','Comparatie_R08');root.Label='R08 | A tavan / B mixt | cote verticale propuse'
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
 g=doc.addObject('App::Part','Varianta_'+v);g.Label=v+' | '+('TOATE PE TAVAN' if v=='A' else 'ILUMINAT TAVAN / PRIZE SI DATE SAPA');root.addObject(g);variants[v]=g
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
 markers=[]
 for s in d['fixings']:
  x,y,z=s['xyz'];markers.append(Part.makeBox(30,16,8,App.Vector(x-15,y-8,z-4)))
 ob=doc.addObject('Part::Feature',v+'_Prinderi_propuse');ob.Label=v+' | '+str(len(markers))+' repere clema, pas propus max 500 mm';ob.Shape=Part.makeCompound(markers);g.addObject(ob)
 ob.addProperty('App::PropertyString','Nota');ob.Nota='Reperele sunt pe axa tubului, nu coordonate de gaurire. Suportul, ancorele, pasul si grosimea sapei se confirma. CSV contine fiecare reper.'
 g.addProperty('App::PropertyString','Cote');g.Cote='Axa tavan +2490 mm / axa in sapa -30 mm: ipoteze de lucru, de masurat.'
 g.addProperty('App::PropertyString','Tuburi');g.Tuburi='63 legaturi fizice. Total geometric '+str(d['total_tube_m'])+' m, fara rezerve.'
doc.recompute()
assert all(o.Shape.isValid() for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull())
doc.saveAs(str(ROOT/'montaj_electric_R08_3D.FCStd'))
print('R08 3D saved, 2 alternatives, 63 conduits each, proposed fixing markers included')
