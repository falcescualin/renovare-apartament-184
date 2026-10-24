import FreeCAD as App, Part, json
from FreeCAD import Vector
a=App.getDocument('apartament_184');a.openTransaction('Amenajare dormitor')
w=a.Dulap_dormitor;sh=w.Shape.copy();sh.rotate(Vector(0,0,0),Vector(0,0,1),-90);bb=sh.BoundBox;sh.translate(Vector(150-bb.XMin,-3845-bb.YMin,0));w.Shape=sh
for name in ('Pat','Noptiere'):
 o=a.getObject(name);s=o.Shape.copy();s.translate(Vector(0,250,0));o.Shape=s
center=(a.Pat.Shape.BoundBox.YMin+a.Pat.Shape.BoundBox.YMax)/2
white=(0.94,0.94,0.92);black=(0.12,0.13,0.14)
def feat(name,label,shape,color=white,group=None):
 o=a.getObject(name) or a.addObject('Part::Feature',name);o.Label=label;o.Shape=shape;o.ViewObject.ShapeColor=color;(group or a.Electric).addObject(o);return o
# TV on east wall facing bed; reserve 60mm for bracket and hidden modules.
tv=feat('TV_dormitor','Televizor dormitor - centrat pe pat',Part.makeBox(40,1000,580,Vector(3450,center-500,1120)),black,a.Mobilier)
module=a.getObject('Modul_TV_dormitor') or a.addObject('App::Part','Modul_TV_dormitor');module.Label='Modul ascuns TV dormitor - Schuko, RJ45 Cat6, coaxial, HDMI';a.Electric.addObject(module)
z=1410;start=center-130
feat('TV_dormitor_rama','Rama modul TV dormitor',Part.makeBox(12,260,86,Vector(3538,start,z-43)),white,module)
for i,kind in enumerate(('Schuko','RJ45_Cat6','Coaxial','Trecere_HDMI')):
 yy=start+37+i*62
 feat('TV_dormitor_'+kind,kind,Part.makeBox(2,58,78,Vector(3536,yy-29,z-39)),white,module)
 if kind=='Schuko':
  feat('TV_dormitor_cuva','Cuva Schuko',Part.makeCylinder(21,2,Vector(3536,yy,z),Vector(-1,0,0)),(0.7,0.7,0.7),module)
  for j,off in enumerate((-9,9)):feat('TV_dormitor_contact_'+str(j),'Contact Schuko',Part.makeCylinder(3,2,Vector(3534,yy+off,z),Vector(-1,0,0)),black,module)
 elif kind=='RJ45_Cat6':feat('TV_dormitor_port_RJ45','Mufa RJ45 - cablare Cat6',Part.makeBox(3,17,14,Vector(3533,yy-8.5,z-7)),black,module)
 elif kind=='Coaxial':feat('TV_dormitor_port_coax','Mufa coaxiala',Part.makeCylinder(8,6,Vector(3536,yy,z),Vector(-1,0,0)),(0.65,0.65,0.65),module)
 else:feat('TV_dormitor_port_HDMI','Trecere cablu HDMI cu perie',Part.makeBox(3,24,24,Vector(3533,yy-12,z-12)),black,module)
if 'NotaMontaj' not in module.PropertiesList:module.addProperty('App::PropertyString','NotaMontaj')
module.NotaMontaj='1 Schuko 230V, 1 RJ45 cablat Cat6, 1 coaxial TV, 1 trecere HDMI. Modul integral ascuns in proiectia televizorului, rezerva suport 60 mm, acces dupa scoaterea ecranului. Date si 230V in compartimente/trasee separate; nu se presupun santuri in perete structural.'
def socket(name,label,axis,x,y,z):
 parts=[]
 if axis=='X':
  parts.append(Part.makeBox(12,86,86,Vector(x,y-43,z-43)))
  parts.append(Part.makeCylinder(21,2,Vector(x+12,y,z),Vector(1,0,0)))
  for off in (-9,9):parts.append(Part.makeCylinder(3,2,Vector(x+14,y+off,z),Vector(1,0,0)))
 else:
  parts.append(Part.makeBox(86,12,86,Vector(x-43,y,z-43)))
  parts.append(Part.makeCylinder(21,2,Vector(x,y+12,z),Vector(0,1,0)))
  for off in (-9,9):parts.append(Part.makeCylinder(3,2,Vector(x+off,y+14,z),Vector(0,1,0)))
 return feat(name,label,Part.makeCompound(parts))
# lateral to each nightstand, at 650mm for access above furniture.
socket('Priza_noptiera_stanga','Schuko noptiera stanga - 65 cm','X',150,-3150,650)
socket('Priza_noptiera_dreapta','Schuko noptiera dreapta - 65 cm','X',150,-450,650)
socket('Priza_dulap_dormitor','Schuko dulap dormitor - compartiment tehnic superior','Y',2150,-3845,2250)
if 'NotaPriza' not in w.PropertiesList:w.addProperty('App::PropertyString','NotaPriza')
w.NotaPriza='Priza Schuko la 2250 mm, in compartiment tehnic accesibil al dulapului; decupaj/loc sursa de prevazut in mobilier. Dulap rotit pe peretele din stanga intrarii, x150..2350, y-3845..-3245. Fronturile spre camera.'
a.recompute()
assert abs(center-(tv.Shape.BoundBox.YMin+tv.Shape.BoundBox.YMax)/2)<0.01
assert w.Shape.common(a.Pat.Shape).Volume<0.01
assert w.Shape.common(a.Noptiere.Shape).Volume<0.01
assert all(o.Shape.isValid() for o in (w,a.Pat,a.Noptiere,tv))
a.commitTransaction();a.save()
print(json.dumps({'bed_TV_axis_y':center,'wardrobe_bbox':str(w.Shape.BoundBox),'wardrobe_nightstand_gap_mm':a.Noptiere.Shape.BoundBox.YMin-w.Shape.BoundBox.YMax,'TV_hidden_ports':4,'new_Schuko_total':4,'saved':True}))
