import FreeCAD as App,Part,math,json
from FreeCAD import Vector
a=App.getDocument('apartament_184');a.openTransaction('Usi si eliminare birou')
for name in ('Birou','Scaun_birou'):
 if a.getObject(name):a.removeObject(name)
a.Prize_birou_4.Label='Dormitor - 4 prize generale sub fereastra, 65 cm'
g=a.getObject('Propuneri_usi') or a.addObject('App::DocumentObjectGroup','Propuneri_usi');g.Label='Usi - foi deschise si arcuri de deschidere'
old=a.getObject('Usa_baie_sens_propus')
if old:old.ViewObject.Visibility=False
hx=(9762.26+9917.26)/2;cx=(9994.37+10149.37)/2
dx=cx-hx;dy=900
items=[('U1','Dormitor', (3500,-3882.5),(2600,-3882.5),(3500,-2982.5)),('U2','Baie spre vestibul',(2487.5,-4200),(2487.5,-4900),(3187.5,-4200)),('U3','Vestibul spre sufragerie',(3625,-4050),(3625,-4950),(4525,-4050)),('U4','Hol spre sufragerie',(7175,-4850),(7175,-3950),(6275,-4850)),('U5','Bucatarie spre frigider',(8800,-3507.5),(8000,-3507.5),(8800,-2707.5)),('U6','Debara spre bucatarie',(9837.5,-2200),(9837.5,-1500),(9137.5,-2200)),('U7','Intrare apartament',(hx,-4780),(cx,-3880),(hx-dy,-4780+dx)),('U8','Balcon',(5250,-125),(6100,-125),(5250,725))]
leaves=[]
for code,label,h,c,o in items:
 hv=Vector(*h,10);cv=Vector(*c,10);ov=Vector(*o,10);v=ov-hv;n=Vector(-v.y,v.x,0);n.normalize();n.multiply(17.5)
 poly=Part.makePolygon([hv+n,ov+n,ov-n,hv-n,hv+n]);shape=Part.Face(Part.Wire(poly.Edges)).extrude(Vector(0,0,2100))
 leaf=a.getObject('Usa_'+code) or a.addObject('Part::Feature','Usa_'+code);leaf.Shape=shape;leaf.Label=code+' - '+label+' - deschisa 90 grade';leaf.ViewObject.ShapeColor=(0.82,0.78,0.70);leaf.ViewObject.Transparency=55;g.addObject(leaf);leaves.append(leaf)
 if 'NotaDeschidere' not in leaf.PropertiesList:leaf.addProperty('App::PropertyString','NotaDeschidere')
 leaf.NotaDeschidere='Foaie schematica de 35 mm, inaltime 2100 mm; latimea reprezinta golul nominal, dimensiunea efectiva se reduce dupa toc. Balama si sens conform modelului; arc 90 grade. Cote finite si feronerie de confirmat.'
 aa=math.atan2(cv.y-hv.y,cv.x-hv.x);bb=math.atan2(v.y,v.x);sweep=(bb-aa+math.pi)%(2*math.pi)-math.pi;r=(cv-hv).Length
 pts=[Vector(h[0]+r*math.cos(aa+sweep*i/36),h[1]+r*math.sin(aa+sweep*i/36),25) for i in range(37)]
 arc=a.getObject('Arc_'+code) or a.addObject('Part::Feature','Arc_'+code);arc.Shape=Part.makePolygon(pts);arc.Label=code+' - arc deschidere';arc.ViewObject.LineColor=(0.18,0.45,0.63);arc.ViewObject.LineWidth=2.5;g.addObject(arc)
 closed=a.getObject('Pozitie_inchisa_'+code) or a.addObject('Part::Feature','Pozitie_inchisa_'+code);closed.Shape=Part.makeLine(Vector(*h,25),Vector(*c,25));closed.Label=code+' - pozitie inchisa';closed.ViewObject.LineColor=(0.45,0.45,0.45);closed.ViewObject.DrawStyle='Dashed';g.addObject(closed)
 assert leaf.Shape.isValid()
a.recompute()
checks={}
for leaf in leaves:
 checks[leaf.Name]=[name for name in ('Pat','Noptiere','Dulap_dormitor','Canapea','Comoda_TV','Masa','Scaune_masa','Set_balcon') if a.getObject(name) and leaf.Shape.common(a.getObject(name).Shape).Volume>1]
a.commitTransaction();a.save()
print(json.dumps({'doors':8,'removed':['Birou','Scaun_birou'],'open_leaf_collisions_main_furniture':checks,'saved':True}))
