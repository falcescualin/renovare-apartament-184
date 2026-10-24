import FreeCAD as App,Part,json
from FreeCAD import Vector
b=App.getDocument('Baie');a=App.getDocument('apartament_184');root=b.Baie_amenajare
if b.getObject('Masca_cada_nise'):raise RuntimeError('Already created; edit existing features.')
for name in ('Cada_150x70','Sifon_cada','Panou_cada_acces'):
 o=b.getObject(name);sh=o.Shape.copy();sh.translate(Vector(0,100,0));o.Shape=sh
def add(name,label,shape,col=(0.82,0.81,0.76)):
 o=b.addObject('Part::Feature',name);o.Label=label;o.Shape=shape;o.ViewObject.ShapeColor=col;root.addObject(o);return o
def box(name,x,y,z,w,d,h,col=(0.94,0.94,0.91)):return add(name,name,Part.makeBox(w,d,h,Vector(x,y,z)),col)
mask=Part.makeBox(700,100,2100,Vector(150,-5550,10))
for zz,h in ((800,350),(1250,350),(1700,300)):
 mask=mask.cut(Part.makeBox(580,81,h,Vector(210,-5530,zz)))
add('Masca_cada_nise','Masca capat cada - 3 nise, adancime utila ~8 cm',mask)
# show a few small bottles, avoid implying large bottles fit the shallow niches.
for i in range(3):add('Recipient_nisa_'+str(i),'Recipient igiena - simbol',Part.makeCylinder(22,180,Vector(330+i*160,-5490,805)),(0.64,0.75,0.77))
# over-WC cupboard, preserve cistern access below and fan clearance above.
x=1750;y=-5550;z=1350;w=650;dep=250;h=800;t=18
box('Dulap_WC_lateral_stanga',x,y,z,t,dep,h);box('Dulap_WC_lateral_dreapta',x+w-t,y,z,t,dep,h)
box('Dulap_WC_spate',x+t,y,z,w-2*t,8,h)
for zz in (z,z+390,z+h-t):box('Dulap_WC_polita',x+t,y+8,zz,w-2*t,dep-8,t)
for i in range(2):box('Dulap_WC_usa',x+2+i*325,y+dep-t,z+2,321,t,h-4,(0.72,0.71,0.67))
root.addProperty('App::PropertyString','NiseCada');root.NiseCada='Cada deplasata 100 mm spre peretele dormitorului, dreapta privit din intrare. Masca capat 700x100x2100; 3 nise, utile ~80 mm in model, mai putin dupa hidroizolatie/finisaj. Sistem umiditate si hidroizolatie, nu gipscarton obisnuit. Cada ramane la 30 mm de peretele dormitorului: finisajele si dimensiunea reala de verificat.'
root.addProperty('App::PropertyString','DulapDeasupraWC');root.DulapDeasupraWC='650x250x800 mm, de la 1350 la 2150 mm. Accesul la clapeta rezervorului si trapa laterala ramane liber. Spatiu pentru ventilator mai sus; pozitia reala a gurii de ventilatie de confirmat.'
# Covered outlets on solid rear wall, right of mirror; >600mm from bathtub projection.
e=a.Electric
s=a.getObject('Prize_baie_uscator_ras') or a.addObject('Part::Feature','Prize_baie_uscator_ras')
shapes=[Part.makeBox(155,12,86,Vector(1572.5,-5550,1057))]
for xx in (1615.5,1684.5):shapes.append(Part.makeBox(60,5,68,Vector(xx-30,-5538,1066)))
s.Shape=Part.makeCompound(shapes);s.Label='Baie - 2 prize cu capac pentru uscator si ras, 110 cm';s.ViewObject.ShapeColor=(0.96,0.96,0.94);e.addObject(s)
for prop,val in [('NotaMontaj','Doua prize cu capac, contact de protectie, protectie la stropi IP44 sau superioara conform produsului si conditiilor de montaj. Pozitie concept la x=1650, y=-5550, z=1100; minimum nominal 722.5 mm intre marginea grupului si gabaritul cazii x=850. Zona, distanta fata de lavoar/jet, protectie diferentiala 30mA si circuite de confirmat de electrician. Nu se considera impermeabile; capacul si IP in utilizare depind de produs.'),('Utilizare','Uscator de par si aparat de ras - 2 prize normale, nu priza speciala de ras cu transformator')]:
 if prop not in s.PropertiesList:s.addProperty('App::PropertyString',prop)
 setattr(s,prop,val)
# provisional fan location, to be corrected using user's reply.
f=a.getObject('Ventilator_baie') or a.addObject('Part::Feature','Ventilator_baie')
f.Shape=Part.makeCompound([Part.makeBox(180,35,180,Vector(2110,-5550,2260)),Part.makeCylinder(65,5,Vector(2200,-5515,2350),Vector(0,1,0))]);f.Label='Ventilator baie existent - pozitie provizorie';f.ViewObject.ShapeColor=(0.95,0.95,0.93);e.addObject(f)
feed=a.getObject('Alimentare_ventilator_baie') or a.addObject('Part::Feature','Alimentare_ventilator_baie')
feed.Shape=Part.makeBox(50,12,50,Vector(2320,-5550,2325));feed.Label='Racord electric ventilator baie - 235 cm, provizoriu';feed.ViewObject.ShapeColor=(0.7,0.8,0.9);e.addObject(feed)
for o in (f,feed):
 if 'NotaMontaj' not in o.PropertiesList:o.addProperty('App::PropertyString','NotaMontaj')
 o.NotaMontaj='Ventilator existent: pozitia reala a gurii in asteptarea raspunsului beneficiarului. Simbol provizoriu deasupra dulapului WC, pe peretele WC/lavoar, centru2350mm. Racord fix, nu priza. Comanda independenta de la a doua tasta a intrerupatorului baii; temporizare/umiditate si alimentarea permanenta se coordoneaza cu modelul ales. Gura de ventilatie ramane accesibila si libera.'
sw=a.Intrerupator_baie
sw.Shape=Part.makeCompound([Part.makeBox(10,86,86,Vector(2525,-4163,1007)),Part.makeBox(4,24,50,Vector(2535,-4145,1025)),Part.makeBox(4,24,50,Vector(2535,-4117,1025))]);sw.Label='Intrerupator baie dublu - lumina / ventilator, 105 cm'
sw.NotaMontaj=sw.NotaMontaj+' Doua taste: lumina generala si ventilator. Temporizarea se alege dupa ventilator.'
b.recompute();b.save();a.recompute();a.save()
assert all(o.Shape.isValid() for o in (b.Masca_cada_nise,s,f,feed))
print(json.dumps({'saved':True,'tub_shift_mm':100,'tub_to_bedroom_wall_mm':30,'niche_depth_mm':80,'over_WC_storage_mm':[650,250,800],'bath_sockets':2,'switch_keys':2,'fan_location':'provisional pending user reply'},ensure_ascii=False))
