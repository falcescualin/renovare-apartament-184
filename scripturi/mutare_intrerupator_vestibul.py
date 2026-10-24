import FreeCAD as App,Part
from FreeCAD import Vector
apt=App.getDocument('apartament_184')
sw=apt.getObject('Intrerupator_LED_vestibul')
sw.Shape=Part.makeCompound([Part.makeBox(10,86,86,Vector(3700,-4043,1007)),Part.makeBox(4,50,50,Vector(3710,-4025,1025))])
sw.Label='Intrerupator LED vestibul - in sufragerie, langa intrare, 105 cm'
sw.NotaMontaj='Pe fata din sufragerie a peretelui dintre sufragerie si vestibul, langa intrarea U3, pe portiunea libera spre dormitor. Centru la (3700,-4000,1050) mm; aproximativ 50 mm de marginea golului pe aceasta latura. Lumina LED se aprinde inainte de intrarea in vestibul. Usa U3 si tocul real de confirmat; la 90 grade foaia se afla la y=-4050. Cota dupa pardoseala modelului.'
assert sw.Shape.isValid()
assert sw.Shape.BoundBox.YMin>-4050 and sw.Shape.BoundBox.YMax<-3920
apt.recompute();apt.save()
print('Saved vestibule switch on living-room side, at entry, height 1050 mm.')
