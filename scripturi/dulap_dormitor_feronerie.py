import FreeCAD as App, Part, csv
from pathlib import Path
V=App.Vector
R=Path(r'C:/Users/Falcescu Alin/Desktop/Apartament_184_Bloc_L14')
d=App.getDocument('dulap_dormitor');a=App.getDocument('apartament_184')
bk=R/'_arhiva/2026-10-06_dulap_dormitor/feronerie';bk.mkdir(parents=True,exist_ok=True)
d.saveCopy(str(bk/'dulap_inainte.FCStd'));a.saveCopy(str(bk/'apartament_inainte.FCStd'))
g=d.getObject('Feronerie') or d.addObject('App::Part','Feronerie');d.Dulap_dormitor.addObject(g)
g.Label='Feronerie | gabarite orientative, nu cote de gaurire'
metal=(.63,.66,.69);warm=(1.,.83,.40)
def feat(name,label,s,parent=g,color=metal):
 o=d.getObject(name) or d.addObject('Part::Feature',name);o.Label=label;o.Shape=s;parent.addObject(o);o.ViewObject.ShapeColor=color;o.ViewObject.LineColor=(.28,.30,.32);return o
def box(name,label,x,y,z,w,dep,h,parent=g,color=metal):return feat(name,label,Part.makeBox(w,dep,h,V(x,y,z)),parent,color)
bay=527.5
# 5 hinges per door: provisional allocation, hinge quantity subject to door weight.
for i in range(4):
 x=18+i*(bay+18);hingeleft=i%2==0;side=x if hingeleft else x+bay
 for j,z in enumerate([200,650,1130,1650,2220]):
  xx=side if hingeleft else side-12
  box(f'Balama_placuta_{i}_{j}','Placuta balama | cota propusa',xx,512,z-18,12,48,36)
  xx=side if hingeleft else side-48
  box(f'Balama_brat_{i}_{j}','Balama amortizata fara intruziune | gabarit',xx,542,z-8,48,36,16)
  cx=i*550+(25 if hingeleft else 525)
  feat(f'Balama_cupa_{i}_{j}','Cupa balama 35 mm | reprezentare, nu gaurire',Part.makeCylinder(17.5,11,V(cx,582,z),V(0,1,0)),d.Fronturi)
 # Per-door sensor and cable route in the upper technical zone.
 box('Senzor_usa_'+str(i),'Senzor deschidere usa | circuit LED 24 V',x+bay-40,550,2080,24,15,12,d.LED,(.15,.16,.18))
 if i in (0,3):
  for j,z in enumerate([115,320,505,690]):
   for side,sx in [('S',x+2),('D',x+bay-15)]:
    box(f'Glisiera_sertar_{i}_{j}_{side}','Glisiera laterala 450 mm | extractie totala, amortizare | model de ales',sx,60,z+30,13,450,35)
  # Shelf pin layout: 5 adjustable shelves, 4 supports per shelf.
  for j,z in enumerate([810,1080,1350,1620,1890]):
   for k,(sx,sy) in enumerate([(x,75),(x,475),(x+bay-8,75),(x+bay-8,475)]):
    feat(f'Suport_raft_{i}_{j}_{k}','Suport raft 5 mm | orientativ',Part.makeCylinder(2.5,8,V(sx,sy,z-2.5),V(1,0,0)))
 else:
  d.getObject('Bara_umerase_'+str(i)).Label='Bara camasi | axa 1940 mm | deasupra pantalonilor'
  for k,sx in enumerate([x,x+bay-10]):
   feat(f'Rozeta_bara_{i}_{k}','Suport capat bara camasi',Part.makeCylinder(20,10,V(sx,302,1940),V(1,0,0)))
  for k,sx in enumerate([x+25,x+bay-37]):
   box(f'Amortizor_pantaloni_{i}_{k}','Glisiera suport pantaloni | amortizor schematic',sx,70,980,12,85,12)
# Retain existing two outer LED strips, add one strip in each hanging compartment.
for i in (1,2):
 x=18+i*(bay+18)+8
 box('LED_vertical_'+str(i),'Banda LED 24 V in profil | camasi si pantaloni',x,555,270,12,8,1750,d.LED,warm)
# Aluminum channels behind all four diffusers.
for i,z,length in [(0,820,1200),(1,270,1750),(2,270,1750),(3,820,1200)]:
 x=18+i*(bay+18)+8
 box('Profil_aluminiu_'+str(i),'Profil aluminiu LED + dispersor opal',x-2,551,z,16,4,length,d.LED)
 d.getObject('LED_vertical_'+str(i)).ViewObject.ShapeColor=warm
 d.getObject('LED_vertical_'+str(i)).ViewObject.LineColor=warm
 # Individual 24 V riser; not a mains wiring execution diagram.
 feat('Cablu_LED_'+str(i),'Traseu schematic 24 V | ramura senzor',Part.makeCylinder(2,2340-(z+length),V(x+6,549,z+length),V(0,0,1)),d.LED,(.2,.2,.2))
 box('Canal_LED_'+str(i),'Canal cablu 24 V | zona superioara',x+4,535,2320,bay-22,10,10,d.LED,(.8,.8,.8))
box('Distribuitor_LED','Distribuitor 24 V | 4 iesiri comandate separat',1840,155,2100,90,35,20,d.LED,(.2,.2,.2))
d.Sursa_LED.Label='Rezerva sursa LED 24 V / 60 W | accesibila, ventilata | de ales'
# Anti-tip brackets represented above the back; anchors depend on actual wall substrate.
for i,x in enumerate([80,750,1400,2080]):
 s=Part.makeBox(35,35,3,V(x,0,2300)).fuse(Part.makeBox(35,3,35,V(x,0,2300)))
 feat('Antirasturnare_'+str(i),'Coltar antirasturnare | ancora dupa suportul peretelui',s)
d.Dulap_dormitor.addProperty('App::PropertyString','Iluminat','Proiect') if 'Iluminat' not in d.Dulap_dormitor.PropertiesList else None
d.Dulap_dormitor.Iluminat='4 benzi: 2 x 1.20 m + 2 x 1.75 m = 5.90 m; ipoteza 24 V, 7.2 W/m => 42.48 W; sursa propusa 60 W. 4 senzori. Produse de confirmat.'
d.recompute()
assert all(o.Shape.isValid() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull())
d.Fronturi.Visibility=True;d.save();a.recompute();a.save()
rows=[
 ['Balamale amortizate fara intruziune pentru sertare interioare',20,'buc','5/usa, provizoriu; numar si suprapunere dupa masa frontului','https://www.blum.com/aa/en/products/hingesystems/clip-top-blumotion/downloads-videos/'],
 ['Placuta montaj balama',20,'buc','Inaltime si compatibilitate dupa balama',''],
 ['Glisiere laterale sertar 450 mm, extractie totala, amortizare',8,'perechi','Joc lateral disponibil 16 mm; produs si capacitate de confirmat',''],
 ['Suport extractibil pantaloni cu 8 brate',2,'set','Include glisiere; fara dublare in cantitati',''],
 ['Bara camasi diametru 24 mm, lungime 507.5 mm',2,'buc','Doua in TOTAL; lungime de taiere dupa rozete',''],
 ['Rozete suport bara camasi',4,'buc','Compatibile cu bara aleasa',''],
 ['Suporti raft',40,'buc','10 rafturi reglabile x 4; rafturi fixe cu imbinari separate',''],
 ['Coltare antirasturnare',4,'set','Suruburi si ancore de ales dupa peretele real',''],
 ['Manere usi / sertare',12,'buc','4 usi + 8 sertare; deja modelate',''],
 ['Banda LED 24 V, ipoteza 7.2 W/m, 3000 K, CRI>=90',5.9,'m','Lungime utila; taiere conform pasului produsului',''],
 ['Profil aluminiu cu dispersor opal',5.9,'m','4 tronsoane: 1200,1750,1750,1200 mm',''],
 ['Capace profil',8,'buc','2 pentru fiecare tronson',''],
 ['Senzor usa pentru 24 V',4,'buc','Cate unul pe compartiment; compatibilitate cu sursa/banda de verificat',''],
 ['Sursa LED 24 V, propunere 60 W',1,'buc','42.48 W nominal calculat; ventilatie si derating dupa produs',''],
 ['Distribuitor 24 V pentru 4 ramuri',1,'buc','Dimensionat dupa sarcina; conexiuni accesibile',''],
 ['Cablare 24 V si conectori',1,'lot','Lungimi si sectiuni dupa traseu real si cadere de tensiune',''],
 ['Suruburi imbinare carcasa si fixari feronerie',1,'lot','Cantitati dupa detaliul de atelier; nu este o lista completa de debitare','']]
with (R/'output/Dulap_dormitor_feronerie_LED.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Articol','Cantitate','Unitate','Observatii','Referinta']);w.writerows(rows)
App.setActiveDocument(d.Name);d.Fronturi.Visibility=False
z=V(350,1000,450);x=V(0,0,1).cross(z)
Gui.activeDocument().activeView().getCameraNode().orientation.setValue(*App.Rotation(x,V(0,0,1),z,'ZXY').Q)
Gui.activeDocument().activeView().fitAll();Gui.updateGui()
Gui.activeDocument().activeView().saveImage(str(R/'output/Dulap_dormitor_LED_feronerie.png'),1600,1400,'White')
d.Fronturi.Visibility=True;d.save();a.recompute();a.save()
print('Saved: four LED strips (5.9 m), 20 schematic hinges, 8 drawer runner pairs, 2 shirt rails total, hardware CSV.')
