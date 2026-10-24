import FreeCAD as App, FreeCADGui as Gui, Part, math, json
from FreeCAD import Vector
src=App.getDocument('apartament_184')
d=App.newDocument('Sufragerie_variante')
wood=(0.72,0.60,0.43); fabric=(0.48,0.60,0.60); grey=(0.83,0.82,0.78)
def add(g,name,shape,color,shift):
    o=d.addObject('Part::Feature',name); o.Shape=shape.copy(); o.Placement.Base=Vector(shift,0,0); o.ViewObject.ShapeColor=color; g.addObject(o); return o
def box(g,name,x,y,z,w,l,h,color,shift):
    return add(g,name,Part.makeBox(w,l,h,Vector(x,y,z)),color,shift)
def chair(g,name,x,y,shift):
    box(g,name+'_sezut',x,y,430,400,400,55,fabric,shift)
    for dx in (25,345):
        for dy in (25,345): box(g,name+'_picior',x+dx,y+dy,10,30,30,420,wood,shift)
    box(g,name+'_spatar',x,y,485,400,35,340,fabric,shift)
clip=Part.makeBox(3700,5700,1150,Vector(3550,-5700,0))
dressing=App.getDocument('Dressing')
closed=Part.makeCompound([o.Shape for o in dressing.Objects if o.TypeId=='PartDesign::Feature' and o.Name!='Masa_calcat_planseta_desfacuta' and hasattr(o,'Shape') and not o.Shape.isNull()])
if closed.isNull():
    closed=Part.makeCompound([o.Shape for o in dressing.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and o.Name not in ('Dressing','Masa_calcat_planseta_desfacuta') and not o.TypeId.startswith(('App::','PartDesign::Plane','PartDesign::Line'))])
for idx,label in enumerate(('A - masa dreptunghiulara 120x75','B - masa rotunda diametru 90')):
    shift=idx*4300
    g=d.addObject('App::DocumentObjectGroup','Varianta_'+str(idx+1)); g.Label=label
    add(g,'Pereti',src.Pereti.Shape.common(clip),grey,shift)
    add(g,'Pardoseala',src.Pardoseala_CameraDeZi.Shape,(0.91,0.87,0.78),shift)
    add(g,'Dressing_inchis',closed,(0.72,0.71,0.67),shift)
    for n in ('Canapea','Comoda_TV','TV'):
        sh=src.getObject(n).Shape.copy(); sh.translate(Vector(0,100,0))
        add(g,n,sh,fabric if n=='Canapea' else (wood if n=='Comoda_TV' else (0.12,0.12,0.12)),shift)
    box(g,'Masuta_80x45',4900,-3100,370,450,800,30,wood,shift)
    for x in (4925,5295):
        for y in (-3075,-2355): box(g,'Picior_masuta',x,y,10,30,30,360,wood,shift)
    if idx==0:
        box(g,'Masa_120x75',3950,-1550,720,750,1200,30,wood,shift)
        for x in (3980,4640):
            for y in (-1520,-410): box(g,'Picior_masa',x,y,10,30,30,710,wood,shift)
        chair(g,'Scaun_1',4750,-850,shift); chair(g,'Scaun_2',4750,-1450,shift)
    else:
        add(g,'Masa_rotunda_90',Part.makeCylinder(450,30,Vector(4450,-1250,720)),wood,shift)
        add(g,'Picior_central',Part.makeCylinder(100,710,Vector(4450,-1250,10)),wood,shift)
        add(g,'Baza_masa',Part.makeCylinder(260,30,Vector(4450,-1250,10)),wood,shift)
        chair(g,'Scaun_1',4250,-750,shift); chair(g,'Scaun_2',4250,-2150,shift)
    # Door leaves at 90 degrees, based on the existing plan. Transparent for study.
    for n,x,y,w,l in [('Usa_hol_deschisa',6275,-4850,900,35),('Usa_vestibul_deschisa',3625,-4067,900,35),('Usa_balcon_deschisa',5232,-975,35,850)]:
        o=box(g,n,x,y,10,w,l,2100,(0.60,0.40,0.25),shift); o.ViewObject.Transparency=65
    # Sofa opening envelope is illustrative; actual mechanism needs a chosen product.
    o=box(g,'Rezerva_canapea_extinsa_ORIENTATIV',4900,-3800,15,2200,2200,15,(0.55,0.75,0.9),shift);o.ViewObject.Visibility=False
    g.addProperty('App::PropertyString','Observatii');g.Observatii='Studiu schematic, mm. Dressing pastrat. Usi conform planului vechi: de confirmat pe teren. Canapeaua extinsa depinde de produs. Masa si scaune mobile.'
d.recompute()
d.saveAs(r'C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\sufragerie_variante.FCStd')
Gui.activeDocument().activeView().viewTop();Gui.activeDocument().activeView().fitAll()
print('Saved two study variants. Original documents unchanged. Dressing closed bbox:',closed.BoundBox)

