import FreeCAD as App,Part,json
from FreeCAD import Vector
apt=App.getDocument('apartament_184');electric=apt.getObject('Electric')
configs=[
 ('Intrerupator_LED_vestibul','Intrerupator LED vestibul - 105 cm',Vector(3540,-4043,1007),Vector(3536,-4025,1025),(10,86,86),(4,50,50),'Interior vestibul, perete spre sufragerie, partea balamalei U3. Centru (3540,-4000,1050) mm. Partea opusa ocupata de spalatorie. Controleaza plafoniera LED vestibul. Tocul real de confirmat.'),
 ('Intrerupator_baie','Intrerupator baie - in vestibul, partea clantei, 105 cm',Vector(2525,-4163,1007),Vector(2535,-4145,1025),(10,86,86),(4,50,50),'In vestibul, pe peretele baii, deasupra golului U2 in plan, pe partea clantei. Centru (2525,-4120,1050) mm, ~80 mm de marginea golului. Accesibil si cu usa baii in sensul propus spre interior. Controleaza lumina generala baie.'),
 ('Intrerupator_dormitor','Intrerupator dormitor - interior, partea clantei, 105 cm',Vector(2472,-3845,1007),Vector(2490,-3835,1025),(86,10,86),(50,4,50),'In dormitor, langa intrarea din vestibul, pe partea clantei U1. Centru (2515,-3845,1050) mm, ~85 mm de marginea golului. Pe peretele spre vestibul, liber de mobilier. Controleaza lumina generala dormitor.')]
for name,label,panel,key,dims,kdims,note in configs:
    o=apt.getObject(name) or apt.addObject('Part::Feature',name)
    o.Shape=Part.makeCompound([Part.makeBox(*dims,panel),Part.makeBox(*kdims,key)])
    o.Label=label;o.ViewObject.ShapeColor=(0.96,0.96,0.94);electric.addObject(o)
    if 'NotaMontaj' not in o.PropertiesList:o.addProperty('App::PropertyString','NotaMontaj')
    o.NotaMontaj=note+' Cota dupa pardoseala modelului; de coordonat cu pardoseala finita si tocurile reale.'
light=apt.getObject('Plafoniera_LED_vestibul') or apt.addObject('Part::Feature','Plafoniera_LED_vestibul')
light.Shape=Part.makeCylinder(120,20,Vector(3037.5,-4480,2480));light.Label='Plafoniera LED vestibul - comanda de la intrare';light.ViewObject.ShapeColor=(1.0,0.96,0.85);electric.addObject(light)
if 'NotaMontaj' not in light.PropertiesList:light.addProperty('App::PropertyString','NotaMontaj')
light.NotaMontaj='Simbol LED slim diametru 240 mm pe tavan. Controleaza Intrerupator_LED_vestibul. Model comercial, putere, temperatura culorii si traseele se stabilesc in planul electric.'
apt.recompute()
assert all(apt.getObject(cfg[0]).Shape.isValid() for cfg in configs)
# Rectangles lie on existing solid wall portions, outside modeled door gaps.
assert apt.Intrerupator_LED_vestibul.Shape.BoundBox.YMin>-4050 and apt.Intrerupator_LED_vestibul.Shape.BoundBox.YMax<-3920
assert apt.Intrerupator_baie.Shape.BoundBox.YMin>-4200 and apt.Intrerupator_baie.Shape.BoundBox.YMax<-3920
assert apt.Intrerupator_dormitor.Shape.BoundBox.XMax<2600
apt.save()
print(json.dumps({'saved':True,'switches':[{'name':cfg[0],'label':cfg[1],'valid':apt.getObject(cfg[0]).Shape.isValid()} for cfg in configs],'height_mm':1050,'vestibule_light':True},ensure_ascii=False))
