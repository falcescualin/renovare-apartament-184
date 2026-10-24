"""Vestibul: concept laundry cabinet. Dimensions mm, not fabrication drawings.
Washer and structural plinth are schematic pending appliance and structural sizing.
"""
import FreeCAD as App, FreeCADGui as Gui, Part, math, json
from FreeCAD import Vector
ROOT=r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14'
if 'Spalatorie_vestibul' in App.listDocuments():
    raise RuntimeError('Document already exists; edit the existing document instead of rerunning.')
d=App.newDocument('Spalatorie_vestibul')
root=d.addObject('App::Part','Spalatorie');root.Label='Spalatorie vestibul - CONCEPT 100x65 cm'
white=(0.94,0.94,0.91);front=(0.72,0.71,0.67);metal=(0.28,0.31,0.33);basket=(0.68,0.73,0.72)
x=2537.5;y=-5550.;z0=10.;W=1000.;D=650.;H=2460.;T=18.;split=x+700
root.addProperty('App::PropertyString','StatusProiect');root.StatusProiect='CONCEPT. Nu se debiteaza. Heinner HWM-HME1014IVA10+++. Suport portant, prinderi, racorduri si inversare usa baie de confirmat.'
root.addProperty('App::PropertyString','Materiale');root.Materiale='Corp Egger W1000 ST9; fronturi Egger U702 ST9; structura portanta metalica schematica, de dimensionat separat.'
root.addProperty('App::PropertyString','Dimensiuni');root.Dimensiuni='1000 latime x 650 adancime x 2460 inaltime; vestibul 1025 x 1630; fata ocupa 50 mm din lungimea golului U3: raman 850 mm nominal in zona de intrare.'
root.addProperty('App::PropertyString','Instalatii');root.Instalatii='Racorduri din baie de proiectat; robinet, scurgere si priza accesibile in compartimentul lateral. Cota scurgerii conform modelului ales. Nu sunt trasee aprobate.'
root.addProperty('App::PropertyString','SuportMasina');root.SuportMasina='Platforma h=500 mm; aparat 61 kg, sarcini dinamice de dimensionat. Manual Heinner cere asigurare anti-rasturnare pe platforma inalta. Structura si prinderile la masina se dimensioneaza/aleg dupa model. PAL si glisiere fara rol portant pentru masina.'
def group(name,label):
    g=d.addObject('App::DocumentObjectGroup',name);g.Label=label;root.addObject(g);return g
car=group('Carcasa','Carcasa decorativa W1000')
base=group('Suport_portant','Suport metalic independent - schematic')
wash=group('Aparat','Heinner HWM-HME1014IVA10+++ 595x590x845; exterior schematic')
drawer=group('Sertar_rufe','Sertar inferior - 2 cosuri detasabile, concept')
tray=group('Polita_extractibila','Polita pentru cosul de incarcare - cursa 450 mm')
upper=group('Depozitare_sus','Detergenti accesibili + depozitare sezoniera')
side=group('Coloana_laterala','Coloana laterala - racorduri, accesorii')
views=group('Demonstratii','Demonstratii deschise - ascunse implicit')
def obj(g,name,shape,color):
    o=d.addObject('Part::Feature',name);o.Shape=shape;o.ViewObject.ShapeColor=color;g.addObject(o);return o
def box(g,name,xx,yy,zz,w,dep,h,col=white):return obj(g,name,Part.makeBox(w,dep,h,Vector(xx,yy,zz)),col)
def hollow(g,name,xx,yy,zz,w,dep,h,t,col):
    sh=Part.makeBox(w,dep,h,Vector(xx,yy,zz)).cut(Part.makeBox(w-2*t,dep-2*t,h,Vector(xx+t,yy+t,zz+t)))
    return obj(g,name,sh,col)
# Decorative casing, ventilation and appliance clearance are schematic.
box(car,'Lateral_stanga',x,y,z0,T,D,H)
box(car,'Lateral_dreapta',x+W-T,y,z0,T,D,H)
box(car,'Separator_lateral',split,y,z0,T,D,H)
box(car,'Capac_sus',x+T,y,z0+H-T,W-2*T,D,T)
box(car,'Masca_tavan',x,y+D-T,z0+H,W,T,27,front)
# Independent frame on the floor. Tube section is illustrative, not sized.
for xx in (x+40,split-80):
    for yy in (y+35,y+D-80):
        box(base,'Stalp_metalic',xx,yy,z0,40,40,470,metal)
for yy in (y+35,y+D-80):box(base,'Traversa_metalica',x+40,yy,z0+430,620,40,40,metal)
for xx in (x+40,split-80):box(base,'Lonjeron_metalic',xx,y+35,z0+430,40,D-115,40,metal)
box(base,'Platforma_portanta_SCHEMATIC',x+30,y+25,z0+470,640,600,30,metal)
# Washer on the support, front faces north (+Y). 60 mm rear hose reserve.
wx=x+52.5;wy=y+50;wz=z0+500
body_depth=558
box(wash,'Masina_Heinner_carcasa',wx,wy,wz,595,body_depth,845,white)
box(wash,'Panou_comenzi',wx+10,wy+body_depth,wz+735,580,12,85,(0.84,0.85,0.85))
obj(wash,'Buton_program',Part.makeCylinder(25,10,Vector(wx+430,wy+body_depth+12,wz+775),Vector(0,1,0)),metal)
obj(wash,'Hublou_rama',Part.makeCylinder(190,30,Vector(wx+300,wy+body_depth,wz+410),Vector(0,1,0)),(0.25,0.26,0.27))
obj(wash,'Hublou_sticla',Part.makeCylinder(152,32,Vector(wx+300,wy+body_depth,wz+410),Vector(0,1,0)),(0.38,0.51,0.55))
box(wash,'Sertar_detergent_aparat',wx+20,wy+body_depth+13,wz+747,205,4,62,(0.90,0.90,0.88))
# Baskets on a pull-out drawer, mechanically independent from frame.
box(drawer,'Baza_sertar',x+85,y+70,z0+55,530,D-88,18)
box(drawer,'Front_sertar_cosuri',x+21,y+D-T,z0+20,658,T,380,front)
for i in range(2):
    hollow(drawer,'Cos_detasabil_'+str(i+1),x+95+i*265,y+200,z0+80,250,420,315,5,basket)
# Separate sliding shelf above baskets, below platform. Closed by default.
box(tray,'Polita_cos_incarcare',x+85,y+50,z0+400,530,D-50,18)
box(tray,'Front_polita',x+80,y+D-T,z0+410,540,T,30,front)
# Upper wall-supported cupboard, leave 60 mm above washer.
uz=z0+1410
box(upper,'Baza_corp_superior',x+T,y,uz,664,D,T)
box(upper,'Spate_corp_superior',x+T,y,uz+T,664,8,H-1410-T)
for zz in (uz+380,z0+1900,z0+2220):box(upper,'Polita_superioara',x+T,y+8,zz,664,D-26,T)
# Everyday supplies niche remains open, 380 mm high, removable drip tray.
box(upper,'Tava_detergenti',x+45,y+280,uz+T,610,280,10,(0.65,0.67,0.65))
for i,(rad,height,col) in enumerate(((48,260,(0.71,0.82,0.87)),(45,245,(0.87,0.81,0.72)),(40,220,(0.74,0.78,0.67)))):
    obj(upper,'Recipient_demo_'+str(i+1),Part.makeCylinder(rad,height,Vector(x+140+i*180,y+450,uz+28)),col)
for i in range(2):box(upper,'Usa_depozitare_sus_'+str(i+1),x+21+i*331,y+D-T,z0+1810,328,T,647,front)
# narrow adjacent service cabinet - accessible ports shown schematically.
box(side,'Baza_laterala',split+T,y,z0+80,264,D-18,T)
for zz in (z0+780,z0+1150,z0+1540,z0+1900,z0+2220):box(side,'Raft_lateral',split+T,y+8,zz,264,D-26,T)
box(side,'Usa_tehnica_laterala',split+T+3,y+D-T,z0+90,258,T,660,front)
box(side,'Usa_accesorii_laterala',split+T+3,y+D-T,z0+800,258,T,1657,front)
obj(side,'Robinet_rezerva_POZITIE_CONCEPT',Part.makeCylinder(22,45,Vector(split+125,y+100,z0+600),Vector(0,1,0)),(0.3,0.55,0.85))
box(side,'Priza_rezerva_POZITIE_CONCEPT',split+180,y+15,z0+620,70,20,70,white)
# Invisible demonstration duplicates: pullout 450, baskets 400, washer door swung left.
for g,dist in ((tray,450),(drawer,400)):
    shapes=[]
    for o in g.Group:
        sh=o.Shape.copy();sh.translate(Vector(0,dist,0));shapes.append(sh)
    o=obj(views,g.Name+'_deschis',Part.makeCompound(shapes),(0.63,0.74,0.74));o.ViewObject.Visibility=False
old_door=box(views,'Usa_baie_existenta_90grade',2487.5,-4917.5,10,700,35,2100,(0.75,0.55,0.35));old_door.ViewObject.Visibility=False
root.addProperty('App::PropertyString','UsaBaie');root.UsaBaie='NECESAR: deschidere in baie. Sensul existent in vestibul intersecteaza corpul de 650 mm. Propunere pe golul existent; de confirmat pe teren.'
box(views,'Rezerva_utilizare_front_60cm',x+T,y+D,10,664,600,10,(0.45,0.7,0.85)).ViewObject.Visibility=False
# Mark dimensions and uncertainties in document properties.
for g in (drawer,tray):
    g.addProperty('App::PropertyString','Feronerie');g.Feronerie='Blum MOVENTO, lungime si sarcina de ales dupa cote reale; polita cu blocare la deschidere. Nu sustine masina.'
d.recompute()
for o in d.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid():raise RuntimeError('Invalid shape: '+o.Name)
d.saveAs(ROOT+r'\spalatorie_vestibul.FCStd')
# Link into the apartment, retaining the old washer hidden for reference.
a=App.getDocument('apartament_184')
link=a.getObject('Spalatorie_vestibul_custom') or a.addObject('App::Link','Spalatorie_vestibul_custom');link.setLink(root)
link.Label='Spalatorie vestibul (CONCEPT -> spalatorie_vestibul.FCStd)'
a.getObject('Mobilier').addObject(link)
a.getObject('Masina_spalat').ViewObject.Visibility=False
# Validation: closed concept stays within vestibule floor footprint and no wall solid collision.
print('Footprint:',root.Shape.BoundBox)
print('Overlap with apartment walls mm3:',root.Shape.common(a.Pereti.Shape).Volume)
print('Clear depth in front mm:',1630-D)
print('Old bathroom door collision mm3:',old_door.Shape.common(root.Shape).Volume)
print('Washer lateral gaps mm:',wx-(x+T),split-(wx+595))
print('Distance from bathroom 90-degree leaf to cabinet front mm:',-4917.5-(y+D))
a.recompute();a.save()
App.setActiveDocument(d.Name);Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
print('Saved concept and linked apartment. Existing bathroom washer hidden, not deleted.')



