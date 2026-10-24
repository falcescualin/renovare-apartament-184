import FreeCAD as App, Part, json, shutil
from pathlib import Path
V=App.Vector
ROOT=Path(r'C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
backup=ROOT/'_arhiva/2026-10-06_dulap_dormitor';backup.mkdir(parents=True,exist_ok=True)
apt=App.getDocument('apartament_184')
if not (backup/'apartament_184_inainte.FCStd').exists():shutil.copy2(ROOT/'apartament_184.FCStd',backup/'apartament_184_inainte.FCStd')
apt.saveCopy(str(backup/'apartament_184_sesiune_inainte.FCStd'))
doc=App.newDocument('dulap_dormitor')
root=doc.addObject('App::Part','Dulap_dormitor');root.Label='Dulap dormitor | 2 persoane | 2200 x 600 x 2360 mm'
groups={}
for name,label in [('Carcasa','Carcasa PAL 18 mm'),('Persoana_A','Persoana A | sertare, tricouri, umerase, pantaloni'),('Persoana_B','Persoana B | sertare, tricouri, umerase, pantaloni'),('Fronturi','4 usi | ascunde grupul pentru interior'),('LED','LED si compartiment tehnic')]:
 g=doc.addObject('App::Part',name);g.Label=label;root.addObject(g);groups[name]=g
white=(.91,.90,.85);wood=(.64,.43,.25);dark=(.16,.18,.19);metal=(.65,.68,.7)
def shape(name,label,s,g='Carcasa',color=white):
 o=doc.addObject('Part::Feature',name);o.Label=label;o.Shape=s;groups[g].addObject(o);o.ViewObject.ShapeColor=color;o.ViewObject.LineColor=(.25,.26,.25);return o
def box(name,x,y,z,w,d,h,g='Carcasa',color=white,label=None):
 return shape(name,label or name,Part.makeBox(w,d,h,V(x,y,z)),g,color)
W=2200;D=600;H=2360;t=18;bay=(W-5*t)/4
box('Soclu',0,20,0,W,540,80,color=dark)
box('Baza',0,0,80,W,578,t);box('Capac',0,0,H-t,W,578,t)
for i,x in enumerate([0]+[18+i*(bay+18)+bay for i in range(4)]):box('Panou_'+str(i),x,0,98,t,578,H-t-98)
# Back leaves clearance to wall socket, with an accessible opening in the upper compartment.
back=Part.makeBox(W,8,H-98,V(0,18,98))
back=back.cut(Part.makeBox(260,20,225,V(1840,10,2135)))
shape('Spate','Spate 8 mm | decupaj acces priza sus dreapta',back)
for i in range(4):
 x=18+i*(bay+18);person='Persoana_A' if i<2 else 'Persoana_B'
 box('Raft_sus_'+str(i),x,26,2050,bay,535,18,person,label='Depozitare sezoniera | cota 2050 mm')
 if i in (0,3):
  for j,(z,h,usage) in enumerate([(115,180,'Pijamale / accesorii'),(320,160,'Sosete'),(505,160,'Lenjerie'),(690,95,'Ceasuri / bijuterii')]):
   dx=x+16;dw=bay-32;yy=56;dd=480
   tray=Part.makeBox(dw,dd,h,V(dx,yy,z)).cut(Part.makeBox(dw-24,dd-24,h,V(dx+12,yy+12,z+12)))
   shape('Sertar_'+str(i)+'_'+str(j),usage+' | sertar extractibil, feronerie de dimensionat',tray,person,wood)
   box('Front_sertar_'+str(i)+'_'+str(j),x+3,540,z-2,bay-6,18,h+8,person,white,usage)
   box('Maner_'+str(i)+'_'+str(j),x+bay/2-60,558,z+h-28,120,12,8,person,dark)
   if j in (1,2,3):
    for k in range(1,4 if j==3 else 3):
     xx=dx+12+k*(dw-24)/(4 if j==3 else 3)
     box('Separator_'+str(i)+'_'+str(j)+'_'+str(k),xx,yy+12,z+12,6,dd-24,h-20,person,wood)
    if j==3:box('Separator_ceasuri_'+str(i),dx+12,yy+dd/2,z+12,dw-24,6,h-20,person,wood)
  for j,z in enumerate([810,1080,1350,1620,1890]):
   box('Raft_tricouri_'+str(i)+'_'+str(j),x,26,z,bay,515,18,person,label='Raft reglabil tricouri | '+str(z)+' mm')
 else:
  shape('Bara_umerase_'+str(i),'Bara umerase | axa 1940 mm',Part.makeCylinder(12,bay-20,V(x+10,302,1940),V(1,0,0)),person,metal)
  box('Raft_jos_'+str(i),x,26,240,bay,520,18,person,label='Raft inferior pentru cutii')
  # Pull-out pants rack, schematic hardware envelope, 8 supports per person.
  for xx in (x+25,x+bay-37):box('Glisiera_pantaloni_'+str(i)+'_'+str(int(xx)),xx,62,960,12,460,18,person,metal)
  box('Traversa_pantaloni_'+str(i),x+25,65,966,bay-50,18,18,person,dark)
  for j in range(8):
   xx=x+55+j*(bay-110)/7
   shape('Suport_pantaloni_'+str(i)+'_'+str(j),'Pantaloni | suport '+str(j+1)+' din 8',Part.makeCylinder(5,425,V(xx,83,975),V(0,1,0)),person,metal)
for i in range(4):
 x=i*550+2
 box('Usa_'+str(i+1),x,582,82,546,18,2276,'Fronturi',white,label='Usa '+str(i+1)+' | 546 mm | sens si balamale de validat')
 box('Maner_usa_'+str(i+1),x+(510 if i%2==0 else 22),600,980,10,22,240,'Fronturi',dark)
# Short handles protrude beyond the original 600 mm cabinet carcass.
for i in (0,3):
 x=18+i*(bay+18)+8
 box('LED_vertical_'+str(i),x,555,820,12,8,1200,'LED',(1.,.86,.5),label='Profil LED cu difuzor | senzor deschidere usa')
box('Sursa_LED',1860,45,2100,160,90,35,'LED',dark,label='Spatiu sursa LED | acces prin usa si decupaj spate')
for name,value in [('Dimensiuni','2200 x 600 x 2360 mm; manere +22 mm'),('Organizare','2 persoane; fiecare: 4 sertare, 5 rafturi, bara umerase, 8 suporturi pantaloni, depozitare sus'),('Statut','Concept mobilier. Feroneria, jocurile sertarelor, balamalele si fixarea anti-rasturnare se dimensioneaza la atelier; nu este debitare de productie.')]:
 root.addProperty('App::PropertyString',name,'Proiect');setattr(root,name,value)
doc.recompute()
assert all(o.Shape.isValid() for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull())
groups['Fronturi'].Visibility=True
doc.saveAs(str(ROOT/'dulap_dormitor.FCStd'))
old=apt.getObject('Dulap_dormitor')
if old:
 old.Visibility=False
 old.Label='Dulap dormitor anterior | inlocuit de componenta externa'
link=apt.getObject('Dulap_dormitor_custom') or apt.addObject('App::Link','Dulap_dormitor_custom')
link.setLink(root);link.Label='Dulap dormitor | componenta externa | 2 persoane'
link.Placement=App.Placement(V(150,-3845,0),App.Rotation())
apt.Mobilier.addObject(link)
apt.recompute();apt.save()
App.setActiveDocument(doc.Name)
groups['Fronturi'].Visibility=False
Gui.activeDocument().activeView().setCameraType('Orthographic')
# Look from the open front (+Y); Z is vertical.
Gui.activeDocument().activeView().setCameraOrientation(App.Rotation(V(-1,0,0),V(0,0,1),V(0,1,0),'ZXY').Q)
Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(ROOT/'output/Dulap_dormitor_interior.png'),1600,1400,'White')
groups['Fronturi'].Visibility=True
doc.save()
print(json.dumps({'file':str(ROOT/'dulap_dormitor.FCStd'),'objects':len(doc.Objects),'link':link.Name,'dimensions_mm':[2200,600,2360],'drawer_count':8,'pants_supports':16}))
