import FreeCAD as App,Part,json
from FreeCAD import Vector
a=App.getDocument('apartament_184');a.openTransaction('Radiatoare noi in pozitiile existente')
g=a.getObject('Incalzire') or a.addObject('App::Part','Incalzire');g.Label='Incalzire - radiatoare noi, pozitii pastrate'
for room,cx,width in [('Dormitor',2480,1000),('Sufragerie',4475,1200)]:
 x=cx-width/2;y=-420;z=150;h=600
 parts=[Part.makeBox(width,28,h,Vector(x,y,z)),Part.makeBox(width,28,h,Vector(x,y+72,z)),Part.makeBox(width,100,12,Vector(x,y,z+h-12))]
 for xx in range(int(x+20),int(x+width-15),25):parts.append(Part.makeBox(8,44,h-30,Vector(xx,y+28,z+15)))
 # slight raised vertical ribs on the front panel.
 for xx in range(int(x+18),int(x+width-12),40):parts.append(Part.makeBox(12,3,h-24,Vector(xx,y-3,z+12)))
 o=a.getObject('Radiator_nou_'+room) or a.addObject('Part::Feature','Radiator_nou_'+room);o.Shape=Part.makeCompound(parts);o.Label='Radiator panou nou - '+room+' - pozitie existenta';o.ViewObject.ShapeColor=(0.95,0.95,0.93);g.addObject(o)
 if 'NotaMontaj' not in o.PropertiesList:o.addProperty('App::PropertyString','NotaMontaj')
 o.NotaMontaj='Reprezentare orientativa radiator panou tip22, '+str(width)+'x600x100 mm. Pozitie pastrata sub geam; sufragerie in zona indicata a biroului. Nu reprezinta dimensionare termica sau produs ales. Puterea, dimensiunile, presiunea admisa si racordurile se confirma pentru termoficare; traseele existente nu sunt modificate. Centrul ferestrei folosit ca reper in lipsa cotelor racordurilor actuale.'
 assert o.Shape.isValid()
a.recompute();a.commitTransaction();a.save();print(json.dumps({'saved':True,'radiators':['Dormitor','Sufragerie'],'positions':'under existing windows; exact pipe offsets unmeasured','furniture_changed':False}))
