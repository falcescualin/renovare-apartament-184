"""Noptiera Woodworking: panouri, feronerie STEP locala si gaurire verificabila."""
from pathlib import Path
from collections import Counter
import sys, json, csv, math
import FreeCAD as App, FreeCADGui as Gui, Part
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/woodworking_pilot'
sys.path.insert(0,str(ROOT/'scripturi'))
from montaj_spec_noptiera import noptiera
from feronerie_catalog import INFO
import montaj_holes
spec=noptiera()
doc=App.newDocument('Noptiera_Woodworking_Feronerie')
doc.Label='Noptieră — panouri, feronerie și găurire'
pg=doc.addObject('App::DocumentObjectGroup','Panouri')
hg=doc.addObject('App::DocumentObjectGroup','Feronerie')
tg=doc.addObject('App::DocumentObjectGroup','SculeGaurire'); tg.Label='Scule găurire (ascunse)'
refs={p['cod']:p for p in json.loads((ROOT/'tmp/lista_debitare_R03.json').read_text(encoding='utf-8'))['piese'] if p['cod'].startswith('N-')}
panel_map={}
def prop(obj,name,value):
    if name not in obj.PropertiesList: obj.addProperty('App::PropertyString',name,'Executie')
    setattr(obj,name,str(value))
for p in spec.parts:
    if p['code'] not in refs: continue
    x,y,z,dx,dy,dz=p['box']
    if p['role']=='door': y+=2.5; p['box'][1]=y
    obj=doc.addObject('Part::Box','Panel_'+p['id'].replace('.','_'))
    obj.Label=p['code']+' | '+p['label']+' | '+p['id']
    obj.Length,obj.Width,obj.Height=dx,dy,dz
    obj.Placement.Base=App.Vector(x,y,z)
    r=refs[p['code']]
    for k,v in [('CodPiesa',p['code']),('MaterialComanda',r['mat']),('Precizie','panou finit'),('CanturiR03',json.dumps({k:r[k] for k in ('L1','L2','W1','W2')}))]: prop(obj,k,v)
    obj.ViewObject.ShapeColor=(0.72,0.66,0.57) if r['mat']=='CAS18' else (0.93,0.93,0.91)
    pg.addObject(obj); panel_map[p['id']]=obj
doc.recompute()

# Actual hole positions from the existing construction specification; never group
# mirrored panels by code because their machining can differ.
hole_info=montaj_holes.compute(spec,uniq_by_code=False)
holes=[]
for pid,d in hole_info.items():
    if pid not in panel_map: continue
    for h in d['h3']:
        item=dict(h,panel=pid)
        if item['kind']=='cep8' and item['face']=='muchie': item['depth']=23.0
        holes.append(item)

# Remaining screw fixings: build entry positions from the real attached panels.
for h in spec.hwi:
    pid=h.get('attach')
    if pid not in panel_map: continue
    model=h['model']
    if model not in ('surub_3_5x16','surub_4x30','surub_4x25','surub_3_5x15'): continue
    if h.get('tag')=='rail': continue
    a=panel_map[pid]; bb=a.Shape.BoundBox
    pos=list(h['at']); n=h['az']; axis=max(range(3),key=lambda i:abs(n[i]))
    mins=[bb.XMin,bb.YMin,bb.ZMin]; maxs=[bb.XMax,bb.YMax,bb.ZMax]
    pos[axis]=maxs[axis] if n[axis]>0 else mins[axis]
    t=maxs[axis]-mins[axis]
    dia=5.0 if model=='surub_4x25' else (4.0 if model=='surub_4x30' else 2.5)
    depth=t if model in ('surub_4x25','surub_4x30','surub_3_5x16') else 10.0
    holes.append(dict(panel=pid,kind='fixare_'+model,pos=pos,n_out=n,dia=dia,depth=depth,through=depth==t,step=h['step'],face='prindere',with_=None))
    if model=='surub_4x25':
        target=pid.split('.')[0]+'.fr'
        # No screw emerges through the 18 mm front: pilot depth 6 mm.
        if target in panel_map:
            front=panel_map[target]
            holes.append(dict(panel=target,kind='pilot_front',pos=[pos[0],front.Placement.Base.y,pos[2]],n_out=[0,-1,0],dia=2.5,depth=6.0,through=False,step=8,face='spate',with_=pid))
    if model=='surub_4x30':
        target='sb_jos' if pid=='blat_c' else 'blat1'
        if target in panel_map:
            dest=panel_map[target]
            holes.append(dict(panel=target,kind='pilot_suport',pos=[pos[0],pos[1],dest.Placement.Base.z],n_out=[0,0,-1],dia=2.5,depth=12.0,through=False,step=h['step'],face='jos',with_=pid))

hole_errors=[]; cut_shapes={}; hole_counts=Counter()
for pid,a in panel_map.items():
    hh=[h for h in holes if h['panel']==pid]
    if not hh: continue
    tools=[]
    bb=a.Shape.BoundBox
    for h in hh:
        n=App.Vector(*h['n_out']); pos=App.Vector(*h['pos'])
        direction=-n
        cutter=Part.makeCylinder(h['dia']/2,h['depth']+0.04,pos+n*0.02,direction)
        vol=a.Shape.common(cutter).Volume
        if vol<0.01: hole_errors.append(dict(panel=pid,kind=h['kind'],error='gaura nu intersecteaza panoul'))
        axis=max(range(3),key=lambda i:abs(h['n_out'][i]))
        lo=[bb.XMin,bb.YMin,bb.ZMin][axis]; hi=[bb.XMax,bb.YMax,bb.ZMax][axis]
        endpoint=h['pos'][axis]-h['n_out'][axis]*h['depth']
        if not h['through'] and not lo+0.01<endpoint<hi-0.01:
            hole_errors.append(dict(panel=pid,kind=h['kind'],error='gaura oarba iese din panou',end=endpoint))
        tools.append(cutter); hole_counts[h['kind']]+=1
    tool_obj=doc.addObject('Part::Feature','Tool_'+pid.replace('.','_')); tool_obj.Shape=Part.makeCompound(tools); tg.addObject(tool_obj)
    cut=doc.addObject('Part::Cut','Gaurit_'+pid.replace('.','_')); cut.Base=a; cut.Tool=tool_obj
    cut.Label=a.Label+' — găurit'; cut.ViewObject.ShapeColor=a.ViewObject.ShapeColor
    pg.addObject(cut); cut_shapes[pid]=cut
    prop(cut,'CodPiesa',a.CodPiesa); prop(cut,'PanouSursa',a.Name)
doc.recompute()
for pid,cut in cut_shapes.items():
    panel_map[pid].Visibility=False; cut.Tool.Visibility=False
    if not cut.Shape.isValid() or cut.Shape.Volume<=0: hole_errors.append(dict(panel=pid,error='solid gaurit invalid'))
tg.Visibility=False

cache={}; hwrows=[]
def hwshape(model):
    if model not in cache:
        shape=Part.Shape(); shape.read(str(ROOT/'tmp/feronerie_R2/step'/(model+'.step')))
        if not shape.isValid(): raise ValueError('STEP invalid: '+model)
        cache[model]=shape
    return cache[model].copy()
def insert_hw(model,at,az=(0,0,1),ax=(1,0,0),mirror=False,attach='',letter='',optional=False):
    z=App.Vector(*az); z.normalize(); x=App.Vector(*ax); x.normalize(); y=z.cross(x)
    mx=App.Matrix()
    sx=-1 if mirror else 1
    mx.A11,mx.A21,mx.A31=x.x*sx,x.y*sx,x.z*sx
    mx.A12,mx.A22,mx.A32=y.x,y.y,y.z
    mx.A13,mx.A23,mx.A33=z.x,z.y,z.z
    mx.A14,mx.A24,mx.A34=at
    shape=hwshape(model)
    if mirror:
        shape=shape.transformGeometry(mx)
    else:
        shape.transformShape(mx,False)
    obj=doc.addObject('Part::Feature','HW_'+model.split('@')[0])
    obj.Shape=shape
    base=model.split('@')[0]; info=INFO[base]
    name=('TIP-ON BLUMOTION L1 T60L7340 — gabarit simplificat' if base=='tip_on' else info[2])
    obj.Label=(letter+' | ' if letter else '')+name
    for k,v in [('ModelCatalog',model),('Precizie',info[6]),('Sursa',info[5]),('PanouPrindere',attach),('Optional',optional)]: prop(obj,k,v)
    if base=='tip_on': prop(obj,'AlegereUnitate','L1, NL350, masa totala sertar <=20kg; de verificat la incarcare')
    obj.ViewObject.ShapeColor=(0.53,0.54,0.55) if info[6]=='gabarit' else (0.8,0.81,0.83)
    hg.addObject(obj)
    if optional: obj.Visibility=False
    hwrows.append(dict(obiect=obj.Name,model=model,denumire=name,panou=attach,precizie=info[6],optional=optional))
    return obj
for p in spec.parts:
    if p['code']=='SL': insert_hw(p['model'],p['place'],mirror=p.get('mirror',False),attach=p.get('follow') or '',letter='F')
for h in spec.hwi:
    if h['model']=='banda_dublu': continue # assembly aid, not permanent hardware
    optional=h['step']==11
    insert_hw(h['model'],h['at'],h['az'],h['ax'],h.get('mirror',False),h.get('attach') or '',h['letter'],optional)

# Permanent hardware list counted from the actual inserted instances.
counts=Counter((h['model'],h['denumire'],h['precizie'],h['optional']) for h in hwrows)
with (OUT/'Feronerie_noptiera.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['Model','Denumire','Bucati','Precizie','Optional'])
    for (m,n,p,o),qty in sorted(counts.items()): w.writerow([m,n,qty,p,o])
with (OUT/'Gaurire_noptiera.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['Panou','Tip','X_mm','Y_mm','Z_mm','Nx','Ny','Nz','Diametru_mm','Adancime_mm','Trecere'])
    for h in holes: w.writerow([h['panel'],h['kind'],*h['pos'],*h['n_out'],h['dia'],h['depth'],h['through']])
report=dict(panouri=len(panel_map),instante_feronerie=len(hwrows),gauri=len(holes),tipuri_gauri=dict(hole_counts),erori_gaurire=hole_errors,corectii_pilot=['TIP-ON L1 T60L7340 in loc de S1 pentru NL350 (masa totala <=20kg).','Joc frontal TIP-ON 2.5mm, fronturile mutate spre fata.','Gauri cep: 12+23mm pentru cep35.'],limite=['Geometria mecanismelor Blum este gabarit simplificat local, nu STEP oficial.','Nu este validare cinematica sau verificare completa a coliziunilor mecanismelor.','Fronturi pilot496mm; comanda R03 are497mm si ramane nemodificata.','Gaurire pilot surub2.5mm necesita adaptare la PAL si surubul real.','Feroneria de perete este optionala, ascunsa; gaurirea peretelui nu este inclusa.'])
(OUT/'Verificare_feronerie.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
doc.recompute()
Gui.activeDocument().activeView().viewRear(); Gui.activeDocument().activeView().fitAll()
path=OUT/'Noptiera_Woodworking_Feronerie.FCStd'
doc.saveAs(str(path))
Gui.activeDocument().activeView().saveImage(str(OUT/'Noptiera_cu_feronerie.png'),1200,1000,'White')
# Inspection view shows hardware inside the cabinet without obscuring it.
for pid,a in panel_map.items():
    visible=cut_shapes.get(pid,a)
    visible.ViewObject.Transparency=80
Gui.activeDocument().activeView().viewAxonometric(); Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(OUT/'Noptiera_feronerie_inspectie.png'),1200,1000,'White')
for pid,a in panel_map.items(): cut_shapes.get(pid,a).ViewObject.Transparency=0
print(json.dumps(report,ensure_ascii=False,indent=2))
