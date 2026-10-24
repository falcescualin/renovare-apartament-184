import FreeCAD as App, FreeCADGui as Gui, Part, json
from FreeCAD import Vector
ROOT=r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14'
apt=App.getDocument('apartament_184')
if 'Conexiuni_TV' in App.listDocuments():
    raise RuntimeError('Component already open; edit existing component.')
doc=App.newDocument('Conexiuni_TV')
root=doc.addObject('App::Part','Conexiuni_TV');root.Label='Conexiuni TV complete - doua grupuri'
white=(0.93,0.93,0.91);black=(0.12,0.14,0.16);metal=(0.62,0.64,0.65)
def feature(parent,name,shape,color):
    o=doc.addObject('Part::Feature',name);o.Shape=shape;o.ViewObject.ShapeColor=color;parent.addObject(o);return o
counts={}
for prefix,label,z,ports in [('Sus','In spatele televizorului',1350,['230V','RJ45','Coaxial','Trecere_HDMI']),('Jos','In compartimentul tehnic al comodei',350,['230V','230V','230V','RJ45','Coaxial','Trecere_HDMI'])]:
    group=doc.addObject('App::Part','Grup_'+prefix);group.Label=label;root.addObject(group)
    count=len(ports);width=count*62+12;start=-2750-width/2
    feature(group,prefix+'_Rama',Part.makeBox(12,width,86,Vector(3700,start,z-43)),white)
    for i,typ in enumerate(ports):
        yy=start+37+i*62
        face=feature(group,prefix+'_'+typ+'_'+str(i+1),Part.makeBox(2,58,78,Vector(3712,yy-29,z-39)),(0.86,0.87,0.85))
        face.Label=prefix+' / '+typ+(' - alimentare soundbar' if prefix=='Jos' and i==2 else '')
        if typ=='230V':
            feature(group,prefix+'_Cuva_priza_'+str(i),Part.makeCylinder(21,2,Vector(3714,yy,z),Vector(1,0,0)),(0.72,0.73,0.72))
            for off in (-9,9):feature(group,prefix+'_Contact_'+str(i)+'_'+str(off),Part.makeCylinder(3,2,Vector(3716,yy+off,z),Vector(1,0,0)),black)
        elif typ=='RJ45':
            feature(group,prefix+'_RJ45_port',Part.makeBox(3,17,14,Vector(3714,yy-8.5,z-7)),black)
            feature(group,prefix+'_RJ45_clapeta',Part.makeBox(3,8,4,Vector(3714,yy-4,z-11)),black)
        elif typ=='Coaxial':
            feature(group,prefix+'_Coaxial_mufa',Part.makeCylinder(8,6,Vector(3714,yy,z),Vector(1,0,0)),metal)
            feature(group,prefix+'_Coaxial_contact',Part.makeCylinder(2,7,Vector(3714,yy,z),Vector(1,0,0)),black)
        else:
            feature(group,prefix+'_Trecere_cabluri_HDMI',Part.makeBox(3,24,24,Vector(3714,yy-12,z-12)),black)
            face.Label=prefix+' / trecere cabluri HDMI cu perie - fara adaptor HDMI'
    for name,val in [('Prize230V',ports.count('230V')),('RJ45',1),('Coaxial',1),('TrecereHDMI',1)]:
        group.addProperty('App::PropertyInteger',name,'Conexiuni');setattr(group,name,val)
    counts[prefix]={key:getattr(group,key) for key in ('Prize230V','RJ45','Coaxial','TrecereHDMI')}
root.addProperty('App::PropertyString','NotaMontaj');root.NotaMontaj='Sus: 230V, RJ45, coaxial, trecere HDMI. Jos: 3 prize (aparat, rezerva, soundbar), RJ45, coaxial, trecere HDMI. Alimentarea soundbarului se afla in comoda. Prizele sunt simboluri distincte; carcasa cu separatoare si traseele se aleg in planul electric. In spatele TV si in mobilier, accesibile pentru service.'
root.addProperty('App::PropertyString','Trasee');root.Trasee='HDMI direct intre aparate prin treceri accesibile; rezerva de cablu pentru scoaterea TV. Canal ascuns de coordonat cu masca demontabila, fara sant presupus in peretele structural. Datele se cableaza individual spre distributie, separat de alimentare.'
doc.recompute()
assert counts['Sus']=={'Prize230V':1,'RJ45':1,'Coaxial':1,'TrecereHDMI':1}
assert counts['Jos']=={'Prize230V':3,'RJ45':1,'Coaxial':1,'TrecereHDMI':1}
assert all(o.Shape.isValid() for o in doc.Objects if o.TypeId=='Part::Feature')
doc.saveAs(ROOT+r'\conexiuni_TV.FCStd')
# Hide superseded standalone symbols, including the visible soundbar socket.
for name in ('Priza_TV','Priza_soundbar','Modul_multimedia_comoda_TV'):
    old=apt.getObject(name)
    if old:
        old.ViewObject.Visibility=False;old.Label=old.Label+' [inlocuit de componenta Conexiuni_TV]'
link=apt.getObject('Conexiuni_TV_custom') or apt.addObject('App::Link','Conexiuni_TV_custom');link.setLink(root);link.Label='Conexiuni TV (link -> conexiuni_TV.FCStd)'
apt.getObject('Electric').addObject(link)
# TV was a schematic solid flush to wall. Reserve a real rear mounting gap.
tv=apt.getObject('TV');delta=3760-tv.Shape.BoundBox.XMin
if delta>0:
    tvshape=tv.Shape.copy();tvshape.translate(Vector(delta,0,0));tv.Shape=tvshape
if 'NotaMontaj' not in tv.PropertiesList:tv.addProperty('App::PropertyString','NotaMontaj')
tv.NotaMontaj='Rezerva schematica de 60 mm intre perete si spatele TV, pentru suport si conexiuni; de confirmat cu suportul real. Grupul superior este integral in proiectia ecranului.'
# Cut a rear service pocket for the lower group. Keep facade/top visually intact.
console=apt.getObject('Comoda_TV');pocket=Part.makeBox(121,440,260,Vector(3699,-2970,215))
console.Shape=console.Shape.cut(pocket)
if 'NotaMultimedia' not in console.PropertiesList:console.addProperty('App::PropertyString','NotaMultimedia')
console.NotaMultimedia='Decupaj tehnic schematic in spate 440x260 mm, adancime 120 mm, acces de prevazut din interior prin capac demontabil. Grupul inferior si alimentarea soundbarului sunt ascunse in comoda; mobilierul detaliat ramane de proiectat.'
apt.recompute();apt.save()
print(json.dumps({'grupuri':counts,'ports_valid':True,'TV_rear_gap_mm':tv.Shape.BoundBox.XMin-3700,'lower_module_in_service_pocket':True,'hidden_old_symbols':[n for n in ('Priza_TV','Priza_soundbar','Modul_multimedia_comoda_TV') if not apt.getObject(n).ViewObject.Visibility]},ensure_ascii=False))
App.setActiveDocument(doc.Name);Gui.activeDocument().activeView().viewRight();Gui.activeDocument().activeView().fitAll()
