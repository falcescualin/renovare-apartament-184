import FreeCAD as App, Part, json
from pathlib import Path
V=App.Vector
R=Path(r'C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
a=App.getDocument('apartament_184')
bk=R/'_arhiva/2026-10-06_corp_spate_pat';bk.mkdir(parents=True,exist_ok=True)
a.saveCopy(str(bk/'apartament_inainte.FCStd'))
bed=a.Pat
delta=300-bed.Shape.BoundBox.XMin
bed.Placement.Base.x+=delta
for n in ['Noptiera_nord','Noptiera_sud']:a.getObject(n).Visibility=False
d=App.newDocument('corp_spate_pat')
root=d.addObject('App::Part','Corp_spate_pat');root.Label='Corp ingust spate pat | 130 x 1600 x 1120 mm'
def obj(name,s,color,parent=root):
 o=d.addObject('Part::Feature',name);o.Shape=s;o.ViewObject.ShapeColor=color;o.ViewObject.LineColor=(.28,.26,.22);parent.addObject(o);return o
wood=(.64,.48,.32);ivory=(.91,.88,.82);dark=(.13,.15,.14)
# Local coordinate X is depth from wall, Y is width along the headboard.
obj('Blat_stejar',Part.makeBox(130,1600,20,V(0,0,1100)),wood)
obj('Laterala_1',Part.makeBox(112,18,1100,V(0,0,0)),ivory)
obj('Laterala_2',Part.makeBox(112,18,1100,V(0,1582,0)),ivory)
obj('Reazem_central',Part.makeBox(112,18,1100,V(0,791,0)),ivory)
obj('Panou_spate',Part.makeBox(8,1564,1100,V(0,18,0)),ivory)
obj('Bordura_spate',Part.makeBox(8,1600,20,V(0,0,1120)),wood)
root.addProperty('App::PropertyString','Nota');root.Nota='Blat la 1120 mm, peste tablia existenta de 1100 mm. Carte asezata vertical sau pe muchie. Fixare de perete de dimensionat.'
# A framed geometric artwork constructed as native CAD faces, not a raster render.
art=d.addObject('App::Part','Tablou_modern');art.Label='Tablou abstract | 1100 x 700 mm | centrat deasupra patului'
obj('Rama_tablou',Part.makeBox(28,1100,700,V(0,250,1450)),dark,art)
obj('Fundal_tablou',Part.makeBox(2,1070,670,V(28,265,1465)),(.92,.88,.79),art)
obj('Soare_ocru',Part.makeCylinder(155,1,V(31,970,1890),V(1,0,0)),(.72,.42,.19),art)
obj('Forma_verde',Part.makeBox(1,260,390,V(32,480,1510)),(.29,.38,.32),art)
obj('Forma_bej',Part.makeCylinder(130,1,V(33,610,1900),V(1,0,0)),(.64,.62,.50),art)
obj('Linie_neagra',Part.makeBox(1,570,12,V(34,600,1620)),dark,art)
obj('Accent_teracota',Part.makeBox(1,210,85,V(35,995,1490)),(.65,.32,.22),art)
d.recompute();d.saveAs(str(R/'corp_spate_pat.FCStd'))
for n,target,label in [('Corp_spate_pat_custom',root,'Corp subtire in spatele patului'),('Tablou_pat_custom',art,'Tablou abstract modern deasupra patului')]:
 l=a.addObject('App::Link',n);l.setLink(target);l.Label=label;l.Placement=App.Placement(V(150,-2600,0),App.Rotation());a.Mobilier.addObject(l)
a.recompute()
assert a.Pat.Shape.common(a.Corp_spate_pat_custom.Shape).Volume<.01
assert a.Pat.Shape.common(a.Perete_TV_dormitor_custom.Shape).Volume<.01
report={'bed_shift_toward_TV_mm':150,'console_depth_mm':130,'console_width_mm':1600,'console_top_mm':1120,'bed_to_TV_furniture_minimum_mm':round(a.Pat.Shape.distToShape(a.Perete_TV_dormitor_custom.Shape)[0],1),'bed_wardrobe_clearance_mm':623,'nightstands_hidden':True,'art_mm':[1100,700],'note':'Distanta minima CAD, nu latimea uniforma a culoarului. Prizele existente nu au fost mutate.'}
a.save();(R/'output/Corp_spate_pat_verificare.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
# Isolated bedroom view, copied for presentation only.
v=App.newDocument('Dormitor_corp_pat_vedere')
for n,col in [('Pat',(.78,.78,.72)),('Corp_spate_pat_custom',wood),('Tablou_pat_custom',ivory),('Dulap_dormitor_custom',ivory),('Perete_TV_dormitor_custom',ivory)]:
 src=a.getObject(n)
 if n in ['Corp_spate_pat_custom','Tablou_pat_custom']:continue
 o=v.addObject('Part::Feature',n);o.Shape=src.Shape.copy();o.ViewObject.ShapeColor=col
for src in d.Objects:
 if src.TypeId!='Part::Feature':continue
 o=v.addObject('Part::Feature',src.Name);s=src.Shape.copy();s.translate(V(150,-2600,0));o.Shape=s;o.ViewObject.ShapeColor=src.ViewObject.ShapeColor
floor=v.addObject('Part::Feature','Podea');floor.Shape=Part.makeBox(3400,3595,10,V(150,-3845,-10));floor.ViewObject.ShapeColor=(.75,.65,.5)
wall=v.addObject('Part::Feature','Perete_tablou');wall.Shape=Part.makeBox(20,3595,2500,V(130,-3845,0));wall.ViewObject.ShapeColor=(.92,.91,.88)
v.recompute();App.setActiveDocument(v.Name)
z=V(1.8,1.4,1.1);x=V(0,0,1).cross(z)
Gui.activeDocument().activeView().setCameraType('Orthographic');Gui.activeDocument().activeView().getCameraNode().orientation.setValue(*App.Rotation(x,V(0,0,1),z,'ZXY').Q)
Gui.activeDocument().activeView().fitAll();Gui.updateGui()
Gui.activeDocument().activeView().saveImage(str(R/'output/Dormitor_corp_pat_tablou.png'),1600,1200,'White')
v.saveAs(str(R/'output/Dormitor_corp_pat_vedere.FCStd'))
print(json.dumps(report))
