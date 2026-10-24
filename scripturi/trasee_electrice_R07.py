"""Model FreeCAD autonom: trasee R07, vizualizare dedicata balconului."""
import FreeCAD as App, Part, json, math
from pathlib import Path
ROOT=Path('C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
D=json.loads((ROOT/'output/pdf/Apartament_184_Trasee_complete_R07.json').read_text(encoding='utf-8'))
doc=App.newDocument('montaj_electric_R07')
root=doc.addObject('App::Part','Trasee_R07');root.Label='R07 | trasee electrice complete | 06.10.2026'
root.addProperty('App::PropertyString','Observatii');root.Observatii='Geometrie preluata R07. Cote in mm fata de model; trasee propuse, de coordonat la montaj.'
contur=doc.addObject('App::Part','Contur_apartament');root.addObject(contur)
model=json.loads((ROOT/'tmp/termic_model.json').read_text(encoding='utf-8'))
for i,edge in enumerate(model['wall_edges']):
    if len(edge)!=2: continue
    o=doc.addObject('Part::Feature','Contur_'+str(i));o.Shape=Part.makePolygon([App.Vector(x,y,0) for x,y in edge]);contur.addObject(o)
groups={}
def feature(name,label,points,parent,color,width=2):
    o=doc.addObject('Part::Feature',name);o.Label=label;parent.addObject(o)
    o.Shape=Part.makeCompound([Part.makeLine(App.Vector(*a),App.Vector(*b)) for a,b in zip(points,points[1:]) if math.dist(a,b)>.001])
    if App.GuiUp:
        o.ViewObject.LineColor=color;o.ViewObject.LineWidth=width
    return o
for r in D['routes']:
    key=r['circuit'].replace(',','_').replace(' ','_').replace('/','_')
    if key not in groups:
        g=doc.addObject('App::Part','Circuit_'+key);g.Label=r['circuit']+' | trasee si capete';root.addObject(g);groups[key]=g
    color=(.12,.43,.8) if r['source']=='TE' else (.55,.25,.7)
    o=feature('Ruta_'+r['id'],r['id']+' | '+r['desc'],r['points'],groups[key],color)
    for name,val in [('Circuit',r['circuit']),('Sursa',r['source']),('Doza',r.get('junction') or '-'),('Coordonate',json.dumps(r['points'])),('Planse',r.get('sheet','')+' / '+r.get('detail_sheet',''))]:
        o.addProperty('App::PropertyString',name,'Traseu');setattr(o,name,val)
    o.addProperty('App::PropertyLength','LungimeGeometrica','Traseu');o.LungimeGeometrica=sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:]))
    marker=doc.addObject('Part::Feature','Capat_'+r['id']);marker.Label=r['id']+' | destinatie';marker.Shape=Part.makeSphere(24,App.Vector(*r['endpoint']));groups[key].addObject(marker)
    if App.GuiUp:o.Visibility=False;marker.Visibility=False
bal=doc.addObject('App::Part','Balcon_evidentiat');bal.Label='BALCON | TE - J05 - S06 / L06 | afisare initiala';root.addObject(bal)
for rid,col in [('J05',(.45,.45,.45)),('S06',(.95,.55,.05)),('L06',(.05,.65,.38))]:
    r=next(r for r in D['routes'] if r['id']==rid)
    feature('Balcon_'+rid,rid+' | '+r['desc'],r['points'],bal,col,4)
    marker=doc.addObject('Part::Feature','Balcon_reper_'+rid);marker.Label=rid+' | '+str(r['endpoint'])+' mm';marker.Shape=Part.makeSphere(45,App.Vector(*r['endpoint']));bal.addObject(marker)
    if App.GuiUp:marker.ViewObject.ShapeColor=col
bal.addProperty('App::PropertyString','Comanda');bal.Comanda='S06 comanda L06. N si PE la plafoniera; faza comandata distincta. Cele doua rute au portiuni comune, nu se insumeaza ca santuri separate.'
bal.addProperty('App::PropertyString','Pozitii');bal.Pozitii='L06: X5400 Y650 Z2490; S06: X6180 Y-255 Z1050; distributie propusa Z2400 mm.'
# Six physical junction boxes: cover on finished wall face, 40 mm body inside wall.
boxes=doc.addObject('App::Part','Doze_pe_pereti');boxes.Label='DOZE J01-J06 | capac 120x120 | centru Z2400';root.addObject(boxes)
for rid in ['J01','J02','J03','J04','J05','J06']:
    r=next(r for r in D['routes'] if r['id']==rid);x,y,z=r['endpoint']
    if rid in ('J01','J04','J06'):
        base=App.Vector(x-40,y-60,z-60);dims=(40,120,120);coverbase=App.Vector(x-2,y-60,z-60);coverdims=(2,120,120)
    elif rid in ('J02','J03'):
        base=App.Vector(x,y-60,z-60);dims=(40,120,120);coverbase=App.Vector(x,y-60,z-60);coverdims=(2,120,120)
    else:
        base=App.Vector(x-60,y-40,z-60);dims=(120,40,120);coverbase=App.Vector(x-60,y-2,z-60);coverdims=(120,2,120)
    o=doc.addObject('Part::Feature','Doza_'+rid);o.Label=rid+' | incastrata / capac pe fata peretelui';o.Shape=Part.makeBox(*dims,base);boxes.addObject(o)
    cap=doc.addObject('Part::Feature','Capac_'+rid);cap.Label=rid+' | capac accesibil';cap.Shape=Part.makeBox(*coverdims,coverbase);boxes.addObject(cap)
    o.addProperty('App::PropertyString','CentruCapac_mm');o.CentruCapac_mm=str(r['endpoint'])
    o.addProperty('App::PropertyString','NotaMontaj');o.NotaMontaj='Gabarit schematic 120x120x40 mm; modelul comercial si tipul montajului se confirma. Peretele nu este decupat in acest model.'
    if App.GuiUp: o.ViewObject.ShapeColor=(.8,.8,.8);cap.ViewObject.ShapeColor=(.98,.85,.25)

doc.recompute()
bad=[o.Name for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
assert not bad,bad
assert len([o for o in doc.Objects if o.Name.startswith('Ruta_')])==len(D['routes'])
out=ROOT/'montaj_electric_R07.FCStd'
if App.GuiUp:
    import FreeCADGui as Gui
    for g in groups.values():g.Visibility=False
    contur.Visibility=True;bal.Visibility=True;boxes.Visibility=True
    Gui.activeDocument().activeView().viewTop();Gui.activeDocument().activeView().fitAll()
doc.saveAs(str(out))
(ROOT/'tmp/trasee_R07_verificare.json').write_text(json.dumps({'file':str(out),'routes':len(D['routes']),'valid':not bad,'balcon':['J05','S06','L06']},indent=2),encoding='utf-8')
print('R07 SALVAT: '+str(out))
