"""Floor-first coordination proposal; existing ceiling paths remain unmeasured."""
from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[1]
old=json.loads((ROOT/'output/pdf/Apartament_184_Tuburi_prinderi_R08.json').read_text(encoding='utf-8'))
tubes=[]; lights=[]
for t in old['variants']['B']['tubes']:
 if t['kind']=='L':
  lights.append(dict(id=t['destination'],source=t['source'],model_endpoint=t['points'][-1],status='Punct existent de pastrat; pozitie si tub existent de verificat pe teren. Traseu nou neprescris.'))
  continue
 pts=[]
 for i,p in enumerate(t['points']):
  p=list(p)
  if 0<i<len(t['points'])-1 and t['kind'] not in ('H','V') and p[2]==2490:p[2]=-30
  if not pts or p!=pts[-1]:pts.append(p)
 t['points']=pts
 if t['kind'] not in ('H','V'):t['mounting']='SAPA'
 t['length_m']=round(sum(math.dist(a,b) for a,b in zip(pts,pts[1:]))/1000,3)
 tubes.append(t)
out=dict(revision='R09',status='PROPUNERE DE COORDONARE, NU PLAN VALIDAT DE EXECUTIE',floor_Z_model_mm=-30,floor_height_status='DE MASURAT; -30 este doar cota grafica preluata din comparatie, nu cota de montaj',existing_lights=lights,variants={'C':dict(tubes=tubes,fixings=[],spans=[],total_tube_m=round(sum(t['length_m'] for t in tubes),3))})
(ROOT/'output/pdf/Apartament_184_Tuburi_prinderi_R09.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
s=(ROOT/'scripturi/tuburi_3d_R08.py').read_text(encoding='utf-8').replace('R08','R09')
s=s.replace("root.Label='R09 | A tavan / B mixt | cote verticale propuse'","root.Label='R09 | distributie prin sapa | plafoniere existente | DE COORDONAT'")
s=s.replace("('TOATE PE TAVAN' if v=='A' else 'ILUMINAT TAVAN / PRIZE SI DATE SAPA')","'DISTRIBUTIE PARDOSEALA / URCARI LA APARATAJ'")
start=s.index(' markers=[]');end=s.index('\ndoc.recompute()',start)
s=s[:start]+''' g.addProperty('App::PropertyString','Cote');g.Cote='Cota grafica axa -30 mm provizorie. Grosime pardoseala DE MASURAT. Nu se taie placa.'
 g.addProperty('App::PropertyString','Statut');g.Statut='Dozele existente din model raman sus si accesibile. Pozarea separata a tuburilor, traversarile si prinderile necesita coordonare dupa masuratori.'
lightgroup=doc.addObject('App::Part','Iluminat_existent');root.addObject(lightgroup)
lightgroup.Label='Puncte de lumina de pastrat | pozitiile modelului de verificat'
for l in D['existing_lights']:
 ob=doc.addObject('Part::Feature','Existent_'+l['id']);lightgroup.addObject(ob)
 ob.Shape=Part.makeSphere(45,App.Vector(*l['model_endpoint']))
 ob.Label=l['id']+' | EXISTENT, tub de verificat | fara traseu nou prescris'
 ob.addProperty('App::PropertyString','Statut');ob.Statut=l['status']
''' + s[end:]
s=s.replace("print('R09 3D saved, 2 alternatives, 63 conduits each, proposed fixing markers included')","print('R09 floor proposal saved; existing ceiling connections intentionally unprescribed')")
(ROOT/'scripturi/tuburi_3d_R09.py').write_text(s,encoding='utf-8')
print('R09:',len(tubes),'proposed tubes;',len(lights),'existing light points awaiting field verification')
