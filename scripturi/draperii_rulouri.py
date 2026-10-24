import FreeCAD as App,Part,math,json
from FreeCAD import Vector
a=App.getDocument('apartament_184');a.openTransaction('Draperii blackout si rulouri')
g=a.getObject('Protectie_solara') or a.addObject('App::Part','Protectie_solara');g.Label='Draperii blackout si rulouri bucatarie'
def add(name,label,shape,col):
 o=a.getObject(name) or a.addObject('Part::Feature',name);o.Shape=shape;o.Label=label;o.ViewObject.ShapeColor=col;g.addObject(o);assert shape.isValid();return o
def fabric(x,w):
 pts=[Vector(x+w*i/60,-305+18*math.sin(i/60*math.pi*12),60) for i in range(61)]
 outline=pts+[Vector(p.x,p.y+3,p.z) for p in reversed(pts)]+[pts[0]]
 return Part.Face(Part.Wire(Part.makePolygon(outline).Edges)).extrude(Vector(0,0,2390))
for room,x,width,panels in [('Dormitor',1450,2050,[(1450,230),(3280,220)]),('Sufragerie',3700,2900,[(3700,350),(6150,450)])]:
 rail=add('Sina_draperie_'+room,'Sina tavan draperii blackout - '+room,Part.makeBox(width,28,20,Vector(x,-318,2465)),(0.94,0.94,0.92))
 for i,(px,pw) in enumerate(panels):
  o=add('Draperie_blackout_'+room+'_'+str(i+1),'Draperie blackout '+room+' - panou '+str(i+1)+' strans',fabric(px,pw),(0.64,0.62,0.58))
  if 'NotaMontaj' not in o.PropertiesList:o.addProperty('App::PropertyString','NotaMontaj')
  o.NotaMontaj='Tesatura blackout opaca, doua panouri mobile pe sina de tavan, reprezentate stranse. La inchidere acopera intreaga deschidere cu suprapunere centrala si intoarceri laterale; latime material dupa factor de incretire si masuratori. Tiv la aproximativ 5 cm de pardoseala finita. Culoare taupe cald orientativa.'
 if room=='Sufragerie':
  o.NotaMontaj+=' Sina comuna pentru fereastra si usa balconului; panourile parcate in afara golului usii, acces liber la balcon.'
# Kitchen: two frame-mounted roller units, half lowered in the model.
for i,x in enumerate((8230,8930)):
 add('Rulou_bucatarie_caseta_'+str(i+1),'Rulou bucatarie - caseta '+str(i+1),Part.makeBox(700,42,55,Vector(x,-205,2345)),(0.91,0.91,0.88))
 o=add('Rulou_bucatarie_material_'+str(i+1),'Rulou bucatarie - material lavabil, partial coborat',Part.makeBox(680,2,680,Vector(x+10,-188,1665)),(0.79,0.78,0.72))
 add('Rulou_bucatarie_bara_'+str(i+1),'Rulou bucatarie - bara inferioara',Part.makeBox(680,12,15,Vector(x+10,-194,1650)),(0.91,0.91,0.88))
 if 'NotaMontaj' not in o.PropertiesList:o.addProperty('App::PropertyString','NotaMontaj')
 o.NotaMontaj='Doua rulouri textile lavabile, filtrante pentru intimitate, montaj propus individual pe canaturile ferestrei; nu blackout (nesolicitat pentru bucatarie). Impartire in 2 x 700 mm orientativa, de confirmat cu tamplaria reala. Cursa completa pana la parapet z900; montaj si comanda astfel incat geamul sa poata fi deschis. Material potrivit bucatariei, fara textile deasupra plitei.'
a.recompute();a.commitTransaction();a.save()
print(json.dumps({'blackout_rooms':['Dormitor','Sufragerie'],'balcony_door_gap_x':[5250,6100],'kitchen_rollers':2,'saved':True}))
