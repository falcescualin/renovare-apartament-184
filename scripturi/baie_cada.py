import FreeCAD as App,FreeCADGui as Gui,Part,json
from FreeCAD import Vector
ROOT=r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14'
a=App.getDocument('apartament_184')
if 'Baie' in App.listDocuments():raise RuntimeError('Baie already open; update existing document.')
d=App.newDocument('Baie');root=d.addObject('App::Part','Baie_amenajare');root.Label='Baie - cada 150, WC incastrat, lavoar pe acelasi perete'
white=(0.96,0.96,0.94);tile=(0.82,0.81,0.76);taupe=(0.72,0.71,0.67);metal=(0.24,0.30,0.32)
def obj(name,label,shape,col=white):
 o=d.addObject('Part::Feature',name);o.Label=label;o.Shape=shape;o.ViewObject.ShapeColor=col;root.addObject(o);return o
def box(name,x,y,z,w,dep,h,col=white):return obj(name,name,Part.makeBox(w,dep,h,Vector(x,y,z)),col)
# tub volume - 1500 long in Y, 700 wide; rim and bowl are schematic.
outer=Part.makeBox(700,1500,550,Vector(150,-5550,10))
inner=Part.makeBox(580,1370,460,Vector(210,-5485,110))
obj('Cada_150x70','Cada 150x70 cm - model orientativ',outer.cut(inner))
obj('Sifon_cada', 'Sifon cada - pozitie orientativa',Part.makeCylinder(25,3,Vector(500,-5420,111)),metal)
box('Panou_cada_acces',820,-5350,80,30,350,350,tile)
# concealed cistern boxing, 650x300x1200, includes frame shown behind opaque facing.
front=Part.makeBox(650,35,1200,Vector(1050,-5285,10))
front=front.cut(Part.makeBox(240,37,155,Vector(1255,-5286,895)))
box('Masca_WC_lateral_stanga',1050,-5550,10,35,300,1200,tile)
sidepanel=Part.makeBox(35,300,1200,Vector(1665,-5550,10))
opening=Part.makeBox(37,250,500,Vector(1664,-5525,570))
obj('Masca_WC_lateral_lavoar','Masca WC - lateral spre lavoar',sidepanel.cut(opening),tile)
obj('Masca_WC_fata','Masca WC - fata cu gol clapeta service',front,tile)
box('Masca_WC_polita_sus',1050,-5550,1210,650,300,25,tile)
hatch=box('Trapa_acces_laterala',1667,-5523,572,35,246,496,tile)
hatch.Label='Trapa demontabila spre lavoar - acces suplimentar ~25x50 cm'
# steel frame and cistern schematic, independent of gypsum skin.
for xx in (1110,1600):box('Cadru_WC_stalp',xx,-5480,10,40,40,1120,metal)
for zz in (150,450,1070):box('Cadru_WC_traversa',1110,-5480,zz,530,40,40,metal)
box('Rezervor_incastrat',1150,-5480,620,450,150,450,(0.78,0.84,0.87))
box('Clapeta_WC_service',1257,-5250,897,236,8,151,(0.70,0.71,0.70))
# suspended bowl, rounded front, cut bowl schematic. Flush rear edge at box front -5250.
bowl=Part.makeBox(360,335,160,Vector(1195,-5585+335,270))
# box from -5250 toward north = +Y
bowl=Part.makeBox(360,335,160,Vector(1195,-5250,270)).fuse(Part.makeCylinder(180,160,Vector(1375,-4915,270)))
cut=Part.makeBox(250,250,150,Vector(1250,-5210,295)).fuse(Part.makeCylinder(125,150,Vector(1375,-4960,295)))
obj('WC_suspendat','WC suspendat - latime 36, proiectie ~52 cm',bowl.cut(cut))
seat=Part.makeBox(370,335,25,Vector(1190,-5250,430)).fuse(Part.makeCylinder(185,25,Vector(1375,-4915,430)))
seatcut=Part.makeBox(250,250,30,Vector(1250,-5210,430)).fuse(Part.makeCylinder(125,30,Vector(1375,-4960,430)))
obj('Colac_WC','Colac WC - model orientativ',seat.cut(seatcut))
# vanity on same wall as WC, offset for lateral hatch access.
box('Corp_lavoar',1800,-5550,400,600,450,430,taupe)
basin=Part.makeBox(600,450,60,Vector(1800,-5550,830)).cut(Part.makeBox(420,290,50,Vector(1890,-5470,850)))
obj('Lavoar_60','Lavoar 60x45 cm pe peretele WC-ului',basin)
obj('Baterie_lavoar','Baterie lavoar - simbol',Part.makeCylinder(18,170,Vector(2100,-5510,890)),metal)
box('Oglinda_lavoar',1800,-5545,1050,600,12,750,(0.65,0.76,0.78))
# removable vanity service back and plumbing reserve notes; actual column not surveyed.
root.addProperty('App::PropertyString','Status');root.Status='CONCEPT. Cada 150x70 cu latime presupusa. WC/lavoar pe peretele sudic, conform peretelui WC anterior. Pozitia exacta coloanei si scurgerilor de confirmat.'
root.addProperty('App::PropertyString','MascaWC');root.MascaWC='650x300x1200 mm + capac 25 mm. Cadru portant dedicat WC, imbracat in sistem pentru umiditate si hidroizolatie. Grosimile si prinderile se stabilesc cu sistemul ales. Trapa laterala 250x500 suplimentara; acces principal rezervor prin clapeta frontala.'
root.addProperty('App::PropertyString','AccesLateral');root.AccesLateral='200 mm intre masca WC si corpul lavoarului. Trapa laterala demontabila, scoasa spre fata; nu usa cu balamale. Pentru interventii mai ample corpul lavoarului poate necesita demontare. Daca aceasta este coloana comuna, se remasoara si se prevad golurile ei reale de acces.'
root.addProperty('App::PropertyString','UsaBaie');root.UsaBaie='Pentru spalatoria din vestibul, usa trebuie sa se deschida in baie. Cu noua pozitie WC si lavoar, gabaritul schematic al foii la 90 grade este liber; arcul, tocul si manerul se confirma pe teren.'
for part in d.Objects:
 if part.TypeId=='Part::Feature' and part.Name.startswith(('Masca_WC','Cadru_WC','Rezervor_incastrat','Clapeta_WC','WC_suspendat','Colac_WC','Trapa_acces_laterala')):
  sh=part.Shape.copy();sh.translate(Vector(-100,0,0));part.Shape=sh
d.recompute()
assert all(o.Shape.isValid() for o in d.Objects if o.TypeId=='Part::Feature')
# Check only boxes of fixture envelopes vs door sweep; the bathroom leaf rotates into upper half, y>=-4900.
print('WC envelope:',d.WC_suspendat.Shape.BoundBox)
print('Vanity envelope:',d.Corp_lavoar.Shape.BoundBox)
print('Door clearance: WC max X',d.Colac_WC.Shape.BoundBox.XMax,'< leaf minimum X 1787.5; vanity max Y',d.Lavoar_60.Shape.BoundBox.YMax,'< leaf min Y -4917.5')
d.saveAs(ROOT+r'\baie.FCStd')
for oldname in ('Dus','Perete_sticla_dus','Lavoar','WC'):
 a.getObject(oldname).ViewObject.Visibility=False
link=a.getObject('Baie_custom') or a.addObject('App::Link','Baie_custom');link.setLink(root);link.Label='Baie (concept -> baie.FCStd)';a.Mobilier.addObject(link)
# Proposed inward swing, shown as a transparent schematic leaf.
g=a.getObject('Propuneri_usi') or a.addObject('App::DocumentObjectGroup','Propuneri_usi')
leaf=a.getObject('Usa_baie_sens_propus') or a.addObject('Part::Feature','Usa_baie_sens_propus')
leaf.Shape=Part.makeBox(700,35,2100,Vector(1787.5,-4917.5,10));leaf.Label='Usa baie - propunere deschidere in baie';leaf.ViewObject.ShapeColor=(0.72,0.58,0.40);leaf.ViewObject.Transparency=70;g.addObject(leaf)
a.recompute();a.save()
App.setActiveDocument(d.Name);Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
print(json.dumps({'saved':True,'new_file':'baie.FCStd','bathtub_mm':[1500,700],'boxing_mm':[650,300,1200],'side_hatch_mm':[250,500],'vanity_mm':[600,450],'fixture_shapes_valid':True}))
