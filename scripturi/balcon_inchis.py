import FreeCAD as App,Part,json
from FreeCAD import Vector
apart=App.getDocument('apartament_184')
group=apart.getObject('Balcon_inchis') or apart.addObject('App::DocumentObjectGroup','Balcon_inchis')
group.Label='Balcon existent - termopan si tavan'
framecolor=(0.94,0.94,0.91);glasscolor=(0.62,0.80,0.88)
def feature(name,label,shape,color,transparency=0):
    o=apart.getObject(name) or apart.addObject('Part::Feature',name)
    o.Label=label;o.Shape=shape;o.ViewObject.ShapeColor=color;o.ViewObject.Transparency=transparency;group.addObject(o)
    return o
# Assumed enclosure: front and both side returns, above existing 1 m parapet.
# Approximate profiles/glazing and panel subdivisions are a visual survey representation.
low=1000;high=2500;h=high-low;p=70;dep=70
frontbars=[];frontglass=[]
for z in (low,high-p):frontbars.append(Part.makeBox(3560,dep,p,Vector(3620,1215,z)))
for i in range(5):
    xx=3620+i*(3560-p)/4
    frontbars.append(Part.makeBox(p,dep,h-2*p,Vector(xx,1215,low+p)))
for i in range(4):
    left=3620+i*(3560-p)/4+p
    width=(3560-p)/4-p
    frontglass.append(Part.makeBox(width,24,h-2*p,Vector(left,1238,low+p)))
feature('Balcon_rama_front','Termopan balcon - rama frontala, compartimentare orientativa',Part.makeCompound(frontbars),framecolor)
feature('Balcon_geam_front','Termopan balcon - 4 panouri frontale orientative',Part.makeCompound(frontglass),glasscolor,75)
for suffix,xx in (('stanga',3565),('dreapta',7165)):
    bars=[];glazing=[]
    for zz in (low,high-p):bars.append(Part.makeBox(dep,1250,p,Vector(xx,0,zz)))
    for yy in (0,590,1180):bars.append(Part.makeBox(dep,p,h-2*p,Vector(xx,yy,low+p)))
    for yy in (70,660):glazing.append(Part.makeBox(24,520,h-2*p,Vector(xx+23,yy,low+p)))
    feature('Balcon_rama_'+suffix,'Termopan balcon - retur '+suffix,Part.makeCompound(bars),framecolor)
    feature('Balcon_geam_'+suffix,'Termopan balcon - vitraj lateral '+suffix,Part.makeCompound(glazing),glasscolor,75)
ceiling=feature('Balcon_tavan','Tavan existent balcon - intrados la 250 cm, grosime schematica',Part.makeBox(3700,1300,150,Vector(3550,0,2500)),(0.90,0.89,0.86))
for o in group.Group:
    if 'NotaReleveu' not in o.PropertiesList:o.addProperty('App::PropertyString','NotaReleveu')
    o.NotaReleveu='Balcon confirmat de beneficiar ca existent inchis cu termopan si cu tavan. Inaltimea intradosului 2500 mm, grosimea placii 150 mm, profilul, geamul, cele 3 fete vitrate si compartimentarea sunt orientative; se corecteaza dupa fotografii/masuratori. Nu este propunere de inchidere noua.'
label=apart.getObject('Text006')
if label and 'Text' in label.PropertiesList:label.Text=['BALCON INCHIS','4,81 m²']
apart.recompute()
print(json.dumps({'frames_valid':all(o.Shape.isValid() for o in group.Group),'enclosure_z':[low,high],'ceiling_lower_z':ceiling.Shape.BoundBox.ZMin,'new_objects':[o.Name for o in group.Group]},ensure_ascii=False))
apart.save()
