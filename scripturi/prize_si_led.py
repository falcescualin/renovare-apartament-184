import FreeCAD as App, Part, json
from FreeCAD import Vector
apart=App.getDocument('apartament_184')
electric=apart.getObject('Electric')
white=(0.96,0.96,0.94);dark=(0.20,0.23,0.25)
def socket(name,label,axis,face,center,height,count,note):
    length=86+(count-1)*69
    shapes=[]
    if axis=='X':
        # face = inner wall X coordinate; depth extends into room
        x0=face if face<5000 else face-12
        shapes.append(Part.makeBox(12,length,86,Vector(x0,center-length/2,height-43)))
        for i in range(count):
            c=center-length/2+43+i*69
            cyl=Part.makeCylinder(22,2,Vector(x0+12 if face<5000 else x0,c,height),Vector(1 if face<5000 else -1,0,0))
            shapes.append(cyl)
    else:
        # all Y sockets here are on south wall facing +Y or north wall facing -Y
        y0=face if face<-5000 else face-12
        shapes.append(Part.makeBox(length,12,86,Vector(center-length/2,y0,height-43)))
        for i in range(count):
            c=center-length/2+43+i*69
            shapes.append(Part.makeCylinder(22,2,Vector(c,y0+12 if face<-5000 else y0,height),Vector(0,1 if face<-5000 else -1,0)))
    o=apart.getObject(name) or apart.addObject('Part::Feature',name)
    o.Label=label;o.Shape=Part.makeCompound(shapes);o.ViewObject.ShapeColor=white
    electric.addObject(o)
    for prop,typ,val in [('NotaMontaj','App::PropertyString',note),('NumarPrize','App::PropertyInteger',count),('CotaCentru','App::PropertyLength',height)]:
        if prop not in o.PropertiesList:o.addProperty(typ,prop,'Electrice')
        setattr(o,prop,val)
    return o
socket('Priza_masina_spalat_vestibul','Priza masina de spalat - acces lateral, 65 cm','Y',-5550,3450,650,1,'Heinner HWM-HME1014IVA10+++. Priza cu impamantare, acces prin usa tehnica laterala; se coordoneaza separat de robinet. Circuit dedicat de stabilit in planul electric. Pozitie concept, traseul nu este proiectat.')
socket('Priza_TV','Priza TV - in spatele ecranului, 135 cm','X',3700,-2750,1350,1,'Pentru televizorul de pe peretele spre dormitor. Aparat schematic la perete: distanta suportului si pozitia efectiva se coordoneaza pentru a nu acoperi conectorii. Nu se presupune ingropare in peretele structural.')
socket('Priza_soundbar','Priza soundbar - sub TV, 90 cm','X',3700,-2750,900,1,'Priza separata pentru eventual soundbar; la 90 cm, sub televizor si deasupra comodei. Cablul HDMI/eARC se coordoneaza cu aparatele si suportul TV. Pozitie concept.')
socket('Prize_birou_4','Birou - 4 prize sub blat, 65 cm','Y',-250,2300,650,4,'Biroul din dormitor, sub fereastra. Patru prize pentru calculator, monitor, lampa si incarcator; centru la 65 cm, sub blatul de 75 cm si sub parapetul ferestrei. Accesul si rezerva pentru cabluri se coordoneaza cu biroul.')
socket('Priza_canapea_dubla','Canapea - priza dubla langa capat, 30 cm','X',7100,-1550,300,2,'Langa capatul canapelei dinspre balcon, la ~15 cm dincolo de canapeaua actuala. Pentru lampa si incarcator; se ajusteaza daca se schimba canapeaua.')
# Remove duplicate provisional power symbol from laundry linked model.
laundry=App.getDocument('Spalatorie_vestibul')
old=laundry.getObject('Priza_rezerva_POZITIE_CONCEPT')
if old:
    old.ViewObject.Visibility=False;old.Label='Rezerva priza - inlocuita de Priza_masina_spalat_vestibul din apartament'
laundry.recompute();laundry.save()
# Existing dressing already has 5 strips and power supply. Add conceptual door sensors.
dressing=App.getDocument('Dressing')
assembly=dressing.getObject('Dressing')
for idx,xx in enumerate((3750,4448,5146,5716,6414),1):
    sensor=dressing.getObject('Senzor_LED_usa_M'+str(idx)) or dressing.addObject('PartDesign::Feature','Senzor_LED_usa_M'+str(idx))
    sensor.Shape=Part.makeBox(12,20,10,Vector(xx,-4995,2060));sensor.ViewObject.ShapeColor=dark
    sensor.Label='Senzor usa LED - modul '+str(idx)
    assembly.addObject(sensor)
    led=dressing.getObject('LED_M'+str(idx));led.Label='LED 24V 4000K - modul '+str(idx);led.ViewObject.ShapeColor=(1.0,0.94,0.76)
    if 'Comanda' not in led.PropertiesList:led.addProperty('App::PropertyString','Comanda')
    led.Comanda='Senzor de usa al modulului; aprindere la deschidere. Banda 24V, putere si sursa de dimensionat dupa banda aleasa.'
source=dressing.getObject('Sursa_LED_24V')
if 'NotaAlimentare' not in source.PropertiesList:source.addProperty('App::PropertyString','NotaAlimentare')
source.NotaAlimentare='Alimentare 230V din Doza_LED_dressing aflata in modelul apartamentului; distribuitor 24V pentru cele cinci module. Sursa accesibila in M3. Putere si cablare de dimensionat.'
dressing.recompute();dressing.save()
led_feed=apart.getObject('Doza_LED_dressing')
led_feed.Label='Alimentare 230V LED dressing - 5 module, senzori usi'
if 'NotaMontaj' not in led_feed.PropertiesList:led_feed.addProperty('App::PropertyString','NotaMontaj')
led_feed.NotaMontaj='Alimentare existenta pentru sursa LED 24V din modulul M3. Acces de service prin compartimentul superior; sa nu fie mascata definitiv. Cota model 2440 mm; de coordonat cu masca si tavanul finisat.'
apart.recompute();apart.save()
print(json.dumps({'new_sockets':{name:apart.getObject(name).NumarPrize for name in ('Priza_masina_spalat_vestibul','Priza_TV','Priza_soundbar','Prize_birou_4','Priza_canapea_dubla')},'dressing_strips':5,'door_sensors':5,'saved':['apartament_184','Dressing','Spalatorie_vestibul']},ensure_ascii=False))
