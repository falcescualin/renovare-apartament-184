import FreeCAD as App, FreeCADGui as Gui, Part, json
from FreeCAD import Vector
from pathlib import Path
ROOT=Path('C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
data=json.loads((ROOT/'tmp/electric_plan.json').read_text(encoding='utf-8'))
doc=App.getDocument('instalatie_electrica') if 'instalatie_electrica' in App.listDocuments() else App.newDocument('instalatie_electrica')
root=doc.getObject('Instalatie_electrica') or doc.addObject('App::Part','Instalatie_electrica')
root.Label='Instalatie electrica R02 - coordonare, NU executie validata'
def group(name,label):
 g=doc.getObject(name) or doc.addObject('App::Part',name);g.Label=label;root.addObject(g);return g
power=group('Curenti_tari','Curenti tari - puncte si racorduri')
weak=group('Curenti_slabi','Curenti slabi - Cat6 si coaxial')
routes=group('Trasee_230V','Trasee 230V propuse - tavan Z2300')
routes_data=group('Trasee_date','Trasee date/coax - schematic, tub separat')
boxes=group('Doze_distributie','Doze J01-J06 - accesibile')
equip=group('Distributie','Tablou / router - gabarite orientative')
colors={'P':(0.78,.24,.19),'F':(.68,.4,.13),'L':(.12,.52,.45),'S':(.12,.52,.45),'D':(.16,.45,.74),'T':(.47,.28,.65)}
def feat(name,label,shape,col,parent):
 o=doc.getObject(name) or doc.addObject('Part::Feature',name);o.Label=label;o.Shape=shape;o.ViewObject.ShapeColor=col;o.ViewObject.LineColor=col;parent.addObject(o);return o
def prop(o,name,typ,val):
 if name not in o.PropertiesList:o.addProperty(typ,name,'Plan electric')
 setattr(o,name,val)
for p in data['points']:
 parent=weak if p['kind'] in ('D','T') else power
 o=feat(p['id'],p['id']+' - '+p['desc'],Part.makeSphere(22,Vector(p['x'],p['y'],p['z'])),colors[p['kind']],parent)
 for name,typ,val in [('Circuit','App::PropertyString',p['circuit']),('Statut','App::PropertyString',p['status']),('NumarMecanisme','App::PropertyInteger',p['n']),('CotaCentru','App::PropertyLength',p['z']),('Nota','App::PropertyString','Marcaj de coordonare; nu gabarit al aparatului. Vezi PDF R02.')]:prop(o,name,typ,val)
 if p['kind'] in ('S',) or p['id']=='F08':continue
 z=2320 if p['kind'] in ('D','T') else 2300
 # 20mm offset is a drawing distinction, not a prescribed physical separation.
 pts=[Vector(x,y,z) for x,y in p['route']]+[Vector(p['x'],p['y'],p['z'])]
 clean=[pts[0]]
 for pt in pts[1:]:
  if (pt-clean[-1]).Length>.01:clean.append(pt)
 o=feat('Traseu_'+p['id'],'Traseu '+p['id']+' / '+p['circuit'],Part.makePolygon(clean),colors[p['kind']],routes_data if p['kind'] in ('D','T') else routes)
 o.ViewObject.LineWidth=2;prop(o,'Nota','App::PropertyString','Traseu propus de coordonare, nu cablu dimensionat. Separarea reala se stabileste dupa sistem. Fara santuri presupuse in structura.')
for b in data['junction_boxes']:
 o=feat(b['id'],b['id']+' - '+b['desc'],Part.makeBox(100,60,50,Vector(b['x']-50,b['y']-30,b['z']-25)),(.8,.5,.18),boxes)
 prop(o,'Circuit','App::PropertyString',b['circuit']);prop(o,'Nota','App::PropertyString','Doza accesibila, gabarit orientativ de ales dupa fire/borne.')
t=data['TE'];o=feat('Tablou_TE','TE - deasupra intrarii, coordonate aproximative',Part.makeBox(360,120,220,Vector(t['x']-180,t['y']-60,2160)),(.78,.24,.19),equip)
prop(o,'Nota','App::PropertyString','Loc confirmat de beneficiar; carcasa/54 module si axa se masoara. C01/C04 cu AFDD; vezi PDF.')
n=data['NET'];o=feat('NET','NET - compartiment ventilat hol, PROPUS',Part.makeBox(450,150,350,Vector(n['x']-225,n['y'],1850)),(.16,.45,.74),equip)
o.ViewObject.Transparency=60;prop(o,'Nota','App::PropertyString','Coordonare cu dulap hol; acces frontal, fara carcasa metalica pentru router Wi-Fi. 4 Schuko C12. Gabarit orientativ.')
for ci in data['circuits']:
 o=doc.getObject('Circuit_'+ci['id']) or doc.addObject('App::FeaturePython','Circuit_'+ci['id']);o.Label=ci['id']+' - '+ci['desc'];root.addObject(o)
 for name,typ,val in [('ProtectiePropusa','App::PropertyString',ci['protection']+' / RCBO 30mA; de validat'),('SectiunePropusa','App::PropertyString',ci['section']),('Puncte','App::PropertyString',ci['points'])]:prop(o,name,typ,val)
routes.Visibility=False;routes_data.Visibility=False
doc.recompute();doc.saveAs(str(ROOT/'instalatie_electrica_R02.FCStd'))
apt=App.getDocument('apartament_184')
link=apt.getObject('Instalatie_electrica_plan') or apt.addObject('App::Link','Instalatie_electrica_plan');link.setLink(root);link.Label='Plan electric R02 (link -> instalatie_electrica_R02.FCStd)';link.Visibility=False
# Concrete requested desk group: 2 Schuko and 1 RJ45, with physically distinct housings.
g=apt.getObject('Modul_birou_Cat6') or apt.addObject('App::Part','Modul_birou_Cat6');g.Label='Birou sufragerie - 2 Schuko + RJ45 sub blat, Z600';apt.Electric.addObject(g)
for idx,typ in enumerate(('Schuko_1','Schuko_2','RJ45_Cat6')):
 y=-985+idx*80
 o=apt.getObject('Birou_'+typ) or apt.addObject('Part::Feature','Birou_'+typ)
 o.Shape=Part.makeBox(14,70,80,Vector(3700,y,560));o.ViewObject.ShapeColor=(.93,.93,.91);g.addObject(o)
 port=apt.getObject('Birou_port_'+typ) or apt.addObject('Part::Feature','Birou_port_'+typ)
 port.Shape=Part.makeCylinder(21,3,Vector(3714,y+35,600),Vector(1,0,0)) if idx<2 else Part.makeBox(3,17,14,Vector(3714,y+26.5,593))
 port.ViewObject.ShapeColor=(.15,.17,.19);g.addObject(port)
prop(g,'NotaMontaj','App::PropertyString','P10 + D04: doze separate 230V/date sau separatoare certificate; sub birou reglabil, cablu flexibil cu rezerva de cursa. P09 lateral pastrat. Pozitie propusa, de coordonat cu cadrul biroului.')
apt.recompute();apt.save();App.setActiveDocument(apt.Name)
print(json.dumps({'saved':str(ROOT/'instalatie_electrica_R02.FCStd'),'points':len(data['points']),'desk_module':'2 Schuko + 1 RJ45','plan_link_hidden':True},ensure_ascii=False))
