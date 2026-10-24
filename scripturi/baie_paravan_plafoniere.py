import FreeCAD as App, Part, json
from FreeCAD import Vector
b=App.getDocument('Baie');a=App.getDocument('apartament_184');root=b.Baie_amenajare
b.openTransaction('Cada intre pereti si paravan')
tub=b.Cada_150x70.Shape.BoundBox
delta=-3920-tub.YMax
for name in ('Cada_150x70','Sifon_cada','Panou_cada_acces'):
 o=b.getObject(name);sh=o.Shape.copy();sh.translate(Vector(0,delta,0));o.Shape=sh
south=b.Cada_150x70.Shape.BoundBox.YMin
depth=south-(-5550)
mask=Part.makeBox(700,depth,2100,Vector(150,-5550,10))
for zz,h in ((800,350),(1250,350),(1700,300)):
 mask=mask.cut(Part.makeBox(580,depth-19,h,Vector(210,-5530,zz)))
b.Masca_cada_nise.Shape=mask
b.Masca_cada_nise.Label='Masca cu 3 nise - umple exact golul de la capatul cazii'
root.NiseCada='Cada 1500 mm de la y=-5420 la -3920, lipita de peretele nordic. Masca cu nise umple integral golul sudic de 130 mm, latime 700 mm. Ansamblu de la perete la perete 1630 mm. Adancime geometrica nise 110 mm, utila finala dupa finisaje. Hidroizolatie si racord etans cada/pereti obligatorii; cote finite de masurat.'
def add(name,label,shape,col):
 o=b.getObject(name) or b.addObject('Part::Feature',name);o.Label=label;o.Shape=shape;o.ViewObject.ShapeColor=col;root.addObject(o);return o
z=b.Cada_150x70.Shape.BoundBox.ZMax
# closed position; hinge on niche mask, folds toward bathtub.
g=add('Paravan_sticla_cada','Paravan cada - sticla securizata 80 x 140 cm',Part.makeBox(8,800,1400,Vector(834,south,z)),(0.72,0.85,0.90));g.ViewObject.Transparency=78
metal=(0.7,0.72,0.74)
add('Profil_paravan_cada','Profil paravan fixat pe masca niselor',Part.makeBox(24,20,1400,Vector(826,south,z)),metal)
for i,zz in enumerate((z+230,z+1120)):
 add('Balama_paravan_'+str(i),'Balama paravan cada',Part.makeBox(28,45,60,Vector(824,south,zz)),metal)
add('Garnitura_paravan_cada','Garnitura inferioara antistropi',Part.makeBox(10,780,10,Vector(833,south+20,z)),(0.85,0.89,0.9))
if 'NotaMontaj' not in g.PropertiesList:g.addProperty('App::PropertyString','NotaMontaj')
g.NotaMontaj='Paravan orientativ 800x1400x8 mm, sticla securizata; zona de dus la capatul cu nise. Fixare profil in suport ranforsat al mastii, nu doar in placa de gips. Garnitura inferioara; rabatare spre interiorul cazii. Dimensiuni si feronerie dupa produs si cada, acces la nise prin rabatare.'
b.recompute();assert all(o.Shape.isValid() for o in (b.Cada_150x70,b.Masca_cada_nise,g));b.commitTransaction();b.save()
a.openTransaction('Plafoniere LED camere')
items=[('Dormitor',1850,-2047.5,400),('CameraDeZi',5400,-2750,500),('Bucatarie',8525,-1860,350),('Baie',1500,-4530,300),('Hol',8550,-4547.5,350),('Nisa',10400,-1860,240),('Balcon',5400,650,300)]
for room,x,y,d in items:
 name='Plafoniera_LED_'+room;o=a.getObject(name) or a.addObject('Part::Feature',name)
 o.Shape=Part.makeCompound([Part.makeCylinder(d/2,8,Vector(x,y,2492)),Part.makeCylinder(d/2-8,12,Vector(x,y,2480))]);o.Label='Plafoniera LED - '+room;o.ViewObject.ShapeColor=(0.98,0.98,0.94);a.Electric.addObject(o)
 if 'NotaMontaj' not in o.PropertiesList:o.addProperty('App::PropertyString','NotaMontaj')
 o.NotaMontaj='Plafoniera LED la tavan 2500 mm, dimensiune orientativa; lumina calda 3000K, CRI>=80. Flux si model de ales dupa incapere. Racord fix la iluminat.'
 if room=='Baie':o.NotaMontaj+=' Corp cu protectie pentru baie (propunere IP44 sau superior); pozitie peste zona libera, nu peste cada; model si zona de confirmat la montaj.'
 if room=='Balcon':o.NotaMontaj+=' Balcon inchis, tavan normal; grad de protectie potrivit eventualului condens.'
a.recompute();assert all(a.getObject('Plafoniera_LED_'+r).Shape.isValid() for r,x,y,d in items);a.commitTransaction();a.save()
print(json.dumps({'tub_north_gap_mm':-3920-b.Cada_150x70.Shape.BoundBox.YMax,'niche_mask_depth_mm':depth,'glass_mm':[800,1400,8],'LED_added':[r for r,x,y,d in items],'vestibule':'existing retained','saved':True}))
