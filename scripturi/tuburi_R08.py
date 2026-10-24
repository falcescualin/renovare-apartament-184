"""Explicit conduit connections and proposed fixing stations for both alternatives."""
from pathlib import Path
import json, math, csv
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'output/pdf/Apartament_184_Trasee_comparatie_R08.json').read_text(encoding='utf-8'))
def clean(pts):
 out=[]
 for p in pts:
  if not out or math.dist(p,out[-1])>.001:out.append(p)
 return out
def between(a,b):
 ap,bp=a['points'],b['points'];n=0
 while n<min(len(ap),len(bp)) and ap[n]==bp[n]:n+=1
 assert n
 return clean(list(reversed(ap[n-1:]))+bp[n:])
allv={}
for v,rs in D['variants'].items():
 by={r['id']:r for r in rs};tubes=[];previous={}
 for r in rs:
  pts=r['points'];source=r['source'];diam=20
  if r['kind']=='P':
   prev=previous.get(r['circuit'])
   if prev:pts=between(prev,r);source=prev['id']
   previous[r['circuit']]=r
  elif r.get('junction'):
   src=by[r['junction']]['endpoint'];indices=[i for i,p in enumerate(pts) if p==src];assert indices
   pts=pts[indices[-1]:];source=r['junction']
  elif r['kind']=='V':
   pts=pts[pts.index(r['local_start']):];source=r['parent']
  elif r['kind']=='H':diam=32
  elif r['kind']=='J':diam=25
  length=sum(math.dist(a,b) for a,b in zip(pts,pts[1:]))
  tubes.append(dict(id='TB_'+r['id'],destination=r['id'],source=source,circuit=r['circuit'],kind=r['kind'],mounting=r['mounting'],diameter_proposed_mm=diam,points=pts,length_m=round(length/1000,3)))
 # Atomic horizontal/vertical spans: number of independently drawn tubes on each centreline.
 groups={}
 for t in tubes:
  for a,b in zip(t['points'],t['points'][1:]):
   nz=[i for i in range(3) if abs(a[i]-b[i])>.001];assert len(nz)==1,(t['id'],a,b)
   axis=nz[0];key=(axis,)+tuple(a[i] for i in range(3) if i!=axis)
   groups.setdefault(key,[]).append((min(a[axis],b[axis]),max(a[axis],b[axis]),t['id']))
 spans=[]
 for key,entries in groups.items():
  breaks=sorted({x for a,b,_ in entries for x in (a,b)})
  for a,b in zip(breaks,breaks[1:]):
   ids=sorted({tid for lo,hi,tid in entries if lo<(a+b)/2<hi})
   if not ids:continue
   fixed=list(key[1:]);pa=[];pb=[];j=0
   for i in range(3):
    if i==key[0]:pa.append(a);pb.append(b)
    else:pa.append(fixed[j]);pb.append(fixed[j]);j+=1
   spans.append({'id':f'SG{len(spans)+1:03}','a':pa,'b':pb,'count':len(ids),'tube_ids':ids,'length_m':round((b-a)/1000,3)})
 stations=[]
 for t in tubes:
  seq=0
  for a,b in zip(t['points'],t['points'][1:]):
   length=math.dist(a,b)
   # 500 mm proposal; individual product/support may require adjustment.
   offsets=[length/2] if length<=200 else [100+i*(length-200)/max(1,math.ceil((length-200)/500)) for i in range(max(1,math.ceil((length-200)/500))+1)]
   for s in offsets:
    seq+=1;p=[round(a[i]+(b[i]-a[i])*s/length,2) for i in range(3)]
    stations.append({'id':t['id']+f'_FX{seq:03}','tube_id':t['id'],'xyz':p,'support':'TAVAN' if a[2]==b[2]==2490 else 'SUPORT_PODEA' if a[2]==b[2]==-30 else 'PERETE_LOCAL','status':'propunere 500 mm / coordonate axa tub, suport real de confirmat'})
 allv[v]={'tubes':tubes,'spans':spans,'fixings':stations,'total_tube_m':round(sum(t['length_m'] for t in tubes),3)}
OUT=ROOT/'output/pdf/Apartament_184_Tuburi_prinderi_R08.json'
OUT.write_text(json.dumps({'revision':'R08','variants':allv,'fixing_pitch_proposed_mm':500,'diameters_status':'preselectie; dimensionare dupa cablu/numar conductoare/radii de curbura','ceiling_Z_proposed':2490,'screed_Z_proposed':-30},ensure_ascii=False,indent=2),encoding='utf-8')
for suffix,fields,rows in [
 ('Tuburi',['Varianta','Tub','De_la','Pana_la','Circuit','Montaj','Diametru_PROPUS_mm','Metri_geometrici','Traseu_XYZ_mm'],[[v,t['id'],t['source'],t['destination'],t['circuit'],t['mounting'],t['diameter_proposed_mm'],t['length_m'],json.dumps(t['points'])] for v,d in allv.items() for t in d['tubes']]),
 ('Prinderi',['Varianta','Prindere','Tub','X_mm','Y_mm','Z_AXA_TUB_mm','Suport','Statut'],[[v,s['id'],s['tube_id'],*s['xyz'],s['support'],s['status']] for v,d in allv.items() for s in d['fixings']]),
 ('Segmente',['Varianta','Segment','A_XYZ_mm','B_XYZ_mm','Numar_copexuri','Tuburi','Metri'],[[v,s['id'],json.dumps(s['a']),json.dumps(s['b']),s['count'],', '.join(s['tube_ids']),s['length_m']] for v,d in allv.items() for s in d['spans']])]:
 with (ROOT/f'output/pdf/Apartament_184_{suffix}_R08.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f,delimiter=';');w.writerow(fields);w.writerows(rows)
print(json.dumps({v:{'tubes':len(d['tubes']),'fixings':len(d['fixings']),'spans':len(d['spans']),'tube_m':d['total_tube_m']} for v,d in allv.items()}))
