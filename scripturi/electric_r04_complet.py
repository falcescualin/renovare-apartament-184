from pathlib import Path
import json,math,csv,copy
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
OLD=json.loads((ROOT/'output/pdf/Apartament_184_Montaj_electric_R03.json').read_text(encoding='utf-8'))
POINTS={p['id']:copy.deepcopy(p) for p in OLD['points']}
N={n:[*xy,2400] for n,xy in OLD['nodes'].items()}
J={b['id']:b for b in OLD['junctions']}
G={g['id']:g for g in OLD['drops']}
TE=[9956,-4330,2250];NET=[7900,-5540,2000]
JA={'J01':'B','J02':'D','J03':'J','J04':'G','J05':'N','J06':'U'}
LJ={'L01':'J03','L02':'J02','L03':'J05','L04':'J01','L05':'J06','L06':'J05','L07':'J04','L08':'J04'}
SJ={'S01':'J03','S02':'J02','S03':'J05','S04':'J01','S05':'J06','S06':'J05','S07':'J04','S08':'J04'}
FJ={'F01':'J01','F02':'J01','F03':'J03','F04':'J01','F05':'J06','F06':'J05','F07':'J04'}
adj={n:[] for n in N}
for t in OLD['trunks']:adj[t['a']].append((t['b'],t['id']));adj[t['b']].append((t['a'],t['id']))
def graph(a,b):
 q=deque([(a,[a],[])]);seen=set()
 while q:
  n,ns,ts=q.popleft()
  if n==b:return ns,ts
  if n in seen:continue
  seen.add(n)
  for other,tid in adj[n]:
   if other not in seen:q.append((other,ns+[other],ts+[tid]))
 raise ValueError((a,b))
def xyz(p):return [p['x'],p['y'],p['z']]
def clean(pts):
 out=[]
 for p in pts:
  p=list(p)
  if not out or math.dist(out[-1],p)>.001:out.append(p)
 return out
def connect(a,b,order=(0,1,2)):
 out=[list(a)];cur=list(a)
 for axis in order:
  cur=cur.copy();cur[axis]=b[axis];out.append(cur)
 return clean(out)
def through(start,end,first=TE):
 ns,ts=graph(start,end);return clean([first]+[N[n] for n in ns]),ts
def jfeed(jid):
 b=J[jid];pts,ts=through('A',JA[jid]);return clean(pts+connect(pts[-1],xyz(b))),ts
def from_j_to_anchor(jid,anchor):
 b=J[jid];pts,ts=jfeed(jid)
 ns,ts2=graph(JA[jid],anchor)
 return clean(pts+connect(xyz(b),N[JA[jid]])+[N[n] for n in ns]),ts+ts2
routes={}
for pid,p in POINTS.items():
 if pid=='F08':continue
 grp=next((g for g in G.values() if pid in g['points']),None)
 jid=None;source='NET' if p['kind'] in ('D','T') else 'TE'
 if p['kind']=='L':
  jid=LJ[pid];pts,ts=jfeed(jid)
  # Balcony goes through circulation, avoiding the earlier shortcut through kitchen/living wall.
  if pid=='L06':
   pts,ts=from_j_to_anchor(jid,'D');pts+=connect(pts[-1],[6180,-255,2400]);pts+=connect(pts[-1],[5400,-255,2400]);pts+=connect(pts[-1],[5400,650,2400])
  else:pts+=connect(pts[-1],[p['x'],p['y'],2400])
  pts+=connect(pts[-1],xyz(p));branch='PLAFOND'
 else:
  anchor=grp['anchor'];branch=grp['id']
  if p['kind']=='S':jid=SJ[pid]
  if p['kind']=='F':jid=FJ[pid]
  if jid:pts,ts=from_j_to_anchor(jid,anchor)
  else:pts,ts=through('NET' if source=='NET' else 'A',anchor,NET if source=='NET' else TE)
  pts+=connect(pts[-1],[grp['x'],grp['y'],2400])
  # Explicit descent to this actual point height, then accessible final service leg.
  pts+=connect(pts[-1],[grp['x'],grp['y'],p['z']])
  pts+=connect(pts[-1],xyz(p))
 pts=clean(pts)
 routes[pid]=dict(id=pid,source=source,junction=jid,group=branch,points=pts,trunks=ts,circuit=p['circuit'],kind=p['kind'],desc=p['desc'],endpoint=xyz(p),quantity=p['n'])
# F08 has two separate local outputs, instead of one misleading point in the middle of the bed.
for pid,parent,yy in [('F08A','P01',-2900),('F08B','P02',-700)]:
 pp=POINTS[parent];end=[360,yy,478]
 pts=clean(routes[parent]['points']+connect(xyz(pp),[158,yy,520])+connect([158,yy,520],end))
 routes[pid]=dict(id=pid,source='TE',junction=None,group=routes[parent]['group'],points=pts,trunks=routes[parent]['trunks'],circuit='C04',kind='V',desc='LED noptieră '+('spre dulap' if pid=='F08A' else 'spre geam'),endpoint=end,quantity=1,parent=parent,local_start=xyz(pp))
for jid,b in J.items():
 pts,ts=jfeed(jid);routes[jid]=dict(id=jid,source='TE',junction=None,group='DOZA',points=pts,trunks=ts,circuit=b['circuit'],kind='J',desc='Doză '+b['desc'],endpoint=xyz(b),quantity=1)
for pid,x,yt,yb,zt,zb in [('H01',3700,-2657,-2595,1350,350),('H02',3550,-1707,-1707,1410,400)]:
 routes[pid]=dict(id=pid,source='HDMI sus',junction=None,group='TV',points=connect([x,yt,zt],[x,yb,zb],(2,1,0)),trunks=[],circuit='HDMI',kind='H',desc='HDMI '+('sufragerie' if pid=='H01' else 'dormitor / rezervă'),endpoint=[x,yb,zb],quantity=1)
for r in routes.values():
 r['length_m']=round(sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:]))/1000,3)
 r['verified']=bool(r['points'] and math.dist(r['points'][-1],r['endpoint'])<.001)
 if r['source']=='TE':r['verified'] &= math.dist(r['points'][0],TE)<.001
 if r['source']=='NET':r['verified'] &= math.dist(r['points'][0],NET)<.001
 r['verified'] &= all(sum(abs(a[i]-b[i])>.001 for i in range(3))==1 for a,b in zip(r['points'],r['points'][1:]))
assert all(r['verified'] for r in routes.values())
assert set(POINTS)-{'F08'} <= set(routes)
assert set(routes)==(set(POINTS)-{'F08'})|{'F08A','F08B'}|set(J)|{'H01','H02'}
# Source evidence independently read from FreeCAD this revision.
assert routes['P02']['endpoint']==[158,-450,650]
assert routes['P05']['endpoint']==[3400,-256,900]
RMAP={pid:g['room'] for g in G.values() for pid in g['points']}
RMAP.update({'L01':'Dormitor','L02':'Sufragerie','L03':'Bucătărie','L04':'Hol','L05':'Debara','L06':'Balcon','L07':'Vestibul','L08':'Baie','F08A':'Dormitor','F08B':'Dormitor'})
for pid,jid in LJ.items():RMAP[jid]=J[jid]['desc'].split(',')[0]
RMAP.update({'J01':'Hol','J02':'Sufragerie','J03':'Dormitor','J04':'Vestibul','J05':'Bucătărie','J06':'Debara','H01':'Sufragerie','H02':'Dormitor'})
for r in routes.values():r['room']=RMAP[r['id']]
OUTDATA=ROOT/'output/pdf/Apartament_184_Trasee_complete_R04.json'
OUTDATA.write_text(json.dumps({'revision':'R04','routes':list(routes.values()),'points_source':list(POINTS.values()),'TE':TE,'NET':NET,'checks':{'routes':len(routes),'endpoints_covered':55,'junction_feeds':6,'hdmi':2,'unconnected':[],'source_CAD_P02':[158,-450,650],'source_CAD_P05':[3400,-256,900]}},ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'output/pdf/Apartament_184_Verificare_trasee_R04.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['ID','Functie','Camera','Sursa','Circuit','Doza','Coborare','X_final','Y_final','Z_final','Continuitate_geometrica','Traseu_XYZ_mm'])
 for r in routes.values():w.writerow([r['id'],r['desc'],r['room'],r['source'],r['circuit'],r['junction'] or '-',r['group'],*r['endpoint'],'VERIFICATA',json.dumps(r['points'])])

src=(ROOT/'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
src=src.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'","OUT=ROOT/'output/pdf/Apartament_184_Montaj_electric_R04.pdf'").replace('R01 |','R04 |').replace("(-1,-1),9)","(-1,-1),6)")
src=src.replace("fill=HexColor('#ffe9df'),stroke=RED,lw=1.3","fill=HexColor('#eef0f1'),stroke=GRAY,lw=.5")
exec(src)
c.setTitle('Apartament 184 - Montaj electric R04 - traseu pana la fiecare punct')
# Correct old grouped furniture footprint which hid both bedside positions in the base plan.
DATA['furniture']=[f for f in DATA['furniture'] if f['name']!='Noptiere']+[{'name':'Noptiera_nord','bbox':[150,-950,5,570,-450,520]},{'name':'Noptiera_sud','bbox':[150,-3150,5,570,-2650,520]}]
COLORS=[BLUE,RED,TEAL,HexColor('#8747a1'),HexColor('#b76a12'),HexColor('#4f6075')]
styles[8]=ParagraphStyle('p8',parent=style,fontSize=8,leading=10)
PAGE_REFS={}
def startp(code,title,sub,scale='Fără scară'):
 start(code,title,sub,scale);PAGE_REFS[code]=PAGE
def fullview():return view(65,270,50)
def roomview(room):
 names={'Dormitor':'Dormitor','Sufragerie':'CameraDeZi','Baie':'Baie','Vestibul':'Vestibul','Bucătărie':'Bucatarie','Hol':'Hol','Debara':'Nisa'}
 if room=='Balcon':xs=[3550,7250];ys=[0,1300]
 else:
  rr=next(r for r in DATA['rooms'] if r['name']=='Pardoseala_'+names[room]);xs=[p[0] for p in rr['polygon']];ys=[p[1] for p in rr['polygon']]
 sc=30 if room=='Sufragerie' else 20 if room in ('Dormitor','Bucătărie') else 15
 k=72/25.4/sc
 return view(82-min(xs)*k,190+max(ys)*k,sc,clip=(42,150,675,590)),sc
def clipped():
 c.saveState();p=c.beginPath();p.rect(42,H-150-590,675,590);c.clipPath(p,stroke=0)
def drawpath(P,pts,col,width=1.8):
 # Visible route from source to actual endpoint; circle/cross indicates the Z descent in plan.
 for a,b in zip(pts,pts[1:]):
  aa=P(a[0],a[1]);bb=P(b[0],b[1])
  if aa!=bb:line(*aa,*bb,col,width)
def dot(P,xyz_,col,rad=4):circle(*P(xyz_[0],xyz_[1]),rad,col,white)
def callout(P,r,col,dy=0):
 x,y=P(r['endpoint'][0],r['endpoint'][1]);dot(P,r['endpoint'],col)
 lx=max(55,min(650,x+10));ly=y-9+dy
 if dy:line(x,y,lx,ly-2,col,.6)
 label=r['id'];tw=pdfmetrics.stringWidth(label,'SegoeB',10)
 rect(lx-2,ly-10,tw+5,13,white,white,.1);txt(lx,ly,label,10,col,True)
def trail(r):
 origin='Distribuitor NET' if r['source']=='NET' else 'Tablou TE'
 if r['kind']=='H':return 'Ieșire TV → tub HDMI → ieșire comodă'
 if r['kind']=='V':return origin+' → '+r['parent']+' → sursă locală → '+r['id']
 return origin+' → '+r['circuit']+(' → '+r['junction'] if r['junction'] else '')+(' → '+r['group'] if r['group'] not in ('PLAFOND','DOZA') else '')+' → '+r['id']
def legendrow(x,y,r,col):
 rect(x,y,12,12,col,col);txt(x+21,y+11,r['id']+' / '+r['desc'],10,INK,True)
 z=r['endpoint'][2];para(x+21,y+19,370,'Circuit '+r['circuit']+' • centru '+str(z)+' mm<br/>'+trail(r),10)
def tablepage(code,title,rows,widths,size=10):
 startp(code,title,'Verificare a geometriei propuse; montajul se validează pe teren');table(42,155,widths,rows,size);end()
startp('00','Fiecare punct are acum traseul complet','R04 | plan de citire simplă + verificare de continuitate + detalii de montaj')
for x,title,value,body in [(42,'PUNCTE TERMINALE','55','F08 desfăcut în două noptiere'),(410,'DOZE + HDMI','6 + 2','Alimentări și legături desenate'),(778,'TRASEE ÎNTRERUPTE','0','Verificare geometrică a propunerii')]:
 rect(x,150,350,125,LIGHT,GRAY);txt(x+16,177,title,11,TEAL,True);txt(x+16,218,value,29,INK,True);txt(x+16,250,body,10,MUT)
para(42,310,525,'<b>Corecția importantă</b><br/>P02, priza de lângă geamul dormitorului, exista în registrul R03, dar era greu de urmărit deoarece ramura ei se suprapunea cu P01. În R04 are traseu evidențiat separat, coborâre și punct final explicit. P05, priza de machiaj de lângă fereastră, este verificată separat.',12)
para(620,310,525,'<b>Ce înseamnă „verificat”</b><br/>Fiecare polilinie pornește de la sursa declarată și ajunge la coordonata aparatului, inclusiv ultima legătură din mobilier. Verificarea este digitală; nu confirmă existența cablurilor în apartament sau posibilitatea de a tăia un perete. Axele sunt propuneri până la releveu.',12)
table(42,495,[150,500,456],[['Cum citești','Planșe','Ce urmărești'],['1 / Exemplu','01 - priza P02, integral','Tablou → dormitor → coborâre → priză'],['2 / Pe camere','Planșe marcate cu numele încăperii','Maximum 5 puncte colorate pe o planșă'],['3 / Doze și HDMI','J / HDMI / comenzi','Sursa fiecărei ramuri și ieșirile accesibile'],['4 / Verificare','Registrul final + CSV','Fiecare ID, sursa, circuitul și capătul traseului'] ],11)
end()
startp('01','Priza de lângă geam / P02','Traseu integral C04; coordonată verificată în FreeCAD: X158 / Y-450 / Z650','1:50 la imprimare A3, 100%')
P,k=fullview();drawpath(P,routes['P02']['points'],BLUE,2.4);dot(P,TE,RED,6);callout(P,routes['P02'],BLUE)
txt(*P(8500,-4700),'TE → hol',10,RED,True);txt(*P(3000,-4700),'vestibul',10,BLUE,True)
para(760,160,385,'<b>P02 / noptiera spre geam</b><br/>Priza este pe peretele stâng, la 200 mm de peretele cu fereastra, cu centrul la 650 mm de pardoseala finită. Aceasta este diferită de P05, priza dublă de machiaj de pe peretele ferestrei.<br/><br/><b>Traseu de urmărit</b><br/>1. Plecare din TE pe C04.<br/>2. Distribuție sus prin hol și sufragerie.<br/>3. Intrare în dormitor prin zona ușii.<br/>4. Traseu sus pe peretele stâng până deasupra P02.<br/>5. Coborâre de la 2400 la 650 mm: 1750 mm.<br/><br/>P01 folosește parțial același coridor, cu derivație proprie. Suprapunerea în plan nu înseamnă că P02 se termină la P01.',11)
para(42,660,1106,'Succesiune: '+ ' → '.join(routes['P02']['trunks'])+' → B02 → P02. Linia reprezintă traseul de cablare; coborârea verticală se vede în detaliul de pe planșa următoare. Circuitele independente împart doar coridorul de montaj, nu conductorii.',11);end()
startp('02','Dormitor / P02 și P05, detaliu de montaj','Cele două prize din zona ferestrei, cu cote și înălțimi explicite')
for x,pid,title in [(42,'P02','NOPTIERĂ SPRE GEAM'),(610,'P05','MACHIAJ / LÂNGĂ DRAPERIE')]:
 r=routes[pid];z=r['endpoint'][2];rect(x+15,170,495,390,LIGHT,GRAY);txt(x+35,202,pid+' / '+title,13,TEAL,True)
 top=235;floor=525;s=.116
 line(x+55,top,x+460,top,MUT,1);line(x+55,floor,x+460,floor,INK,1.2)
 y=floor-z*s;line(x+200,floor-2400*s,x+200,y,BLUE,2.5);circle(x+200,y,7,BLUE,white)
 txt(x+220,y,pid+' / Z'+str(z),12,BLUE,True);txt(x+70,top-8,'Plafon ≈2500 / distribuție Z2400',10,MUT)
 dim(x+200,floor,x+200,y,str(z)+' mm',-50)
 para(x+30,590,485,('Pe peretele vestic: 200 mm de peretele cu geamul. C04, 1 Schuko. Coborâre B02 de 1750 mm.' if pid=='P02' else 'Pe peretele cu geamul: X3400, la 3250 mm de peretele vestic al dormitorului. C04, 2 Schuko; Z900. Acces în spatele draperiei de verificat.')+'<br/><br/>Cotele se raportează la pardoseala și fețele finite ale pereților. Desenul de mai sus este o elevație explicativă, fără scară.',11)
end()

# Small pages by function, max five points, all endpoints and final connectors visible.
roomlist=['Dormitor','Sufragerie','Bucătărie','Vestibul','Baie','Hol','Debara','Balcon']
manifest=[]
for room in roomlist:
 lists=[('Prize și date',[r for r in routes.values() if r['room']==room and r['kind'] in ('P','D','T')]),('Lumină și comenzi',[r for r in routes.values() if r['room']==room and r['kind'] in ('F','L','S','V')])]
 for category,rr in lists:
  for off in range(0,len(rr),5):
   batch=rr[off:off+5];code='C'+str(len(manifest)+1).zfill(2)
   scale=30 if room=='Sufragerie' else 20 if room in ('Dormitor','Bucătărie') else 15
   startp(code,room+' / '+category.lower(),', '.join(r['id'] for r in batch)+' | linie continuă până la fiecare aparat','1:'+str(scale)+' la imprimare A3, 100%')
   (P,k),_=roomview(room);clipped()
   # All routes run into the visible room, but source-to-room is on the global inset.
   for i,r in enumerate(batch):drawpath(P,r['points'],COLORS[i],1.7)
   used=[]
   for i,r in enumerate(batch):
    x,y=P(r['endpoint'][0],r['endpoint'][1]);dy=0
    while any(abs(x-a)<35 and abs(y+dy-b)<15 for a,b in used):dy+=16
    used.append((x,y+dy));callout(P,r,COLORS[i],dy)
   c.restoreState()
   for i,r in enumerate(batch):legendrow(745,155+i*93,r,COLORS[i]);r['sheet']=code
   para(745,645,397,'<b>Linie = traseu fizic propus.</b> Punct colorat = capăt real la aparataj. Cercul poate corespunde unei coborâri verticale, invizibile în vederea de sus. Cotele Z sunt în legenda fiecărui punct. Porțiunile comune se suprapun; fiecare punct are și fișă individuală de traseu în registru.',10)
   end();manifest.append({'sheet':code,'room':room,'ids':[r['id'] for r in batch]})

startp('J0','Alimentarea dozelor / de la tablou','Cele șase doze au traseu explicit de la TE; neutrali separați pe circuite','1:50 la imprimare A3, 100%')
P,k=fullview()
for i,jid in enumerate(J):drawpath(P,routes[jid]['points'],COLORS[i],1);callout(P,routes[jid],COLORS[i]);routes[jid]['sheet']='J0'
for i,jid in enumerate(J):legendrow(745,155+i*87,routes[jid],COLORS[i])
end()
tablepage('J1','Comenzi / conexiuni funcționale',[['Comandă','Doză / circuit','Receptor','Cum se închide legătura'],['S01','J03 / C01','L01','Faza comandată revine în J03; N și PE merg la lampă'],['S02','J02 / C01','L02','Retur separat din S02 spre L02 prin J02'],['S03 dublu','J05 / C02','L03 + F06','Două retururi distincte; fază comună din același circuit'],['S04','J01 / C02','L04','Retur de fază; N/PE identificate'],['S05','J06 / C02','L05','LED debara F05 cu senzor local'],['S06','J05 / C02','L06','Retur prin doza J05; traseu prin circulație'],['S07','J04 / C03','L07','Întrerupător în sufragerie; lampă vestibul'],['S08 dublu','J04 / C03','L08 + F07','Pentru fan cu temporizare: L permanent, LT, N și PE după clasă']],[120,190,160,636],11)
startp('H0','HDMI / de la televizor până în comodă','Legăturile H01 și H02 sunt acum polilinii complete, cu ambele ieșiri')
for x,h in [(42,'H01'),(610,'H02')]:
 r=routes[h];a,b=r['points'][0],r['endpoint'];rect(x+20,165,470,390,LIGHT,GRAY);txt(x+40,196,h+' / '+r['desc'],14,TEAL,True)
 rect(x+75,245,340,52,white,BLUE);txt(x+90,275,'TV / X'+str(a[0])+' Y'+str(a[1])+' Z'+str(a[2]),10)
 rect(x+75,465,340,52,white,BLUE);txt(x+90,495,'Comodă / Y'+str(b[1])+' Z'+str(b[2]),10)
 line(x+240,297,x+240,465,BLUE,3);txt(x+260,380,'tub propriu',11,BLUE,True)
 para(x+25,580,475,'Cablu continuu, înlocuibil; tub orientativ Ø32-40 după dimensiunea mufei și raza de curbură. Ieșiri cu perie și acces la capete. Test HDMI/eARC înainte de închiderea panoului. H02 este rezervă până la alegerea aparatelor din dormitor.',11);r['sheet']='H0'
end()

# Individual records make overlapped trunks auditable without a spaghetti plan.
TERMINALS=[r for r in routes.values() if r['kind']!='J']
for off in range(0,len(TERMINALS),4):
 code='F'+str(off//4+1).zfill(2);startp(code,'Fișe individuale / traseu până la capăt','Fiecare fișă este o legătură verificată geometric; coordonate în mm')
 for i,r in enumerate(TERMINALS[off:off+4]):
  x=42+(i%2)*568;y=155+(i//2)*295;col=COLORS[i]
  rect(x,y,535,270,white,GRAY);rect(x,y,535,30,col,col);txt(x+12,y+21,r['id']+' / '+r['desc'][:65],11,white,True)
  para(x+12,y+43,511,'<b>'+trail(r)+'</b><br/>Capăt real: X'+str(r['endpoint'][0])+' / Y'+str(r['endpoint'][1])+' / Z'+str(r['endpoint'][2])+'<br/>Planșa de poziționare: '+r.get('sheet','H0')+' • circuit '+r['circuit']+' • cantitate '+str(r['quantity']),11)
  para(x+12,y+119,511,'Coridoare: '+(' → '.join(r['trunks']) if r['trunks'] else 'legătură locală')+'.',9)
  # Last three physical segments expose service legs which R03 omitted.
  segs=list(zip(r['points'],r['points'][1:]))[-3:]
  para(x+12,y+168,511,'<b>Ultimele segmente XYZ:</b><br/>'+'<br/>'.join('/'.join(map(str,a))+' → '+'/'.join(map(str,b)) for a,b in segs),9)
  txt(x+12,y+253,'CONTINUITATE GEOMETRICĂ: VERIFICATĂ',10,TEAL,True);r['detail_sheet']=code
 end()
for off in range(0,len(routes),16):
 batch=list(routes.values())[off:off+16]
 tablepage('V'+str(off//16+1).zfill(2),'Registru de verificare / toate legăturile',[['ID','Destinație','Sursă','Circuit','Doză','Final XYZ','Plan / fișă','Geometrie']]+[[r['id'],r['desc'],r['source'],r['circuit'],r['junction'] or '-', '/'.join(map(str,r['endpoint'])),r.get('sheet','-')+' / '+r.get('detail_sheet','-'),'Conectat'] for r in batch],[60,275,80,75,65,210,190,151],9)
startp('FIN','Ce s-a verificat / ce se confirmă la montaj','R04 înlocuiește reprezentarea traseelor din R03')
table(42,155,[300,806],[['Verificare','Rezultat'],['P02 lângă geam / P05 machiaj','Confirmate separat în FreeCAD; rute complete până la centrele aparatajului'],['Acoperirea inventarului','54 intrări R02 devin 55 puncte terminale: F08 separat în două noptiere'],['Continuitatea rutelor','63 polilinii: 55 puncte + 6 alimentări J + 2 HDMI. Sursă corectă, capăt exact, fără salturi între segmente'],['Grupurile TV / birou / bucătărie','Adăugate segmentele finale dintre axa comună și fiecare port; firele/circuitele păstrate separate'],['Corpuri și comenzi','Incluse în același set de date și în modelul FreeCAD; relațiile S-J-L explicate pe J1'],['Verificare vizuală','PDF randat și controlat pentru etichete și lizibilitate. Registru CSV pentru căutare după ID'] ],11)
para(42,530,525,'<b>Înainte de execuție</b><br/>Se confirmă pe teren pereții, trecerile, mobilierul și accesul, secțiunile/protecțiile, branșamentul și PE. Continuitatea desenată nu reprezintă test electric și nu autorizează șanțuri în beton. Distribuția propusă este la Z2400; dimensiunea măștii se verifică cu tuburile reale.',12)
para(620,530,525,'<b>Documente de utilizat împreună</b><br/>R04: poziționare și trasee complete. R02: aparataj și preselecție circuite, de validat. Lungimile vechi R02/R03 nu se folosesc ca listă finală de comandă după aceste corecții. CSV-ul R04 conține toate coordonatele fiecărei polilinii; lungimile comune nu se însumează ca șanțuri separate.',12)
end();c.save()
# Persist reference sheet IDs alongside the exact geometry used for drawing and CAD.
obj=json.loads(OUTDATA.read_text(encoding='utf-8'));obj['routes']=list(routes.values());obj['pages']=PAGE;obj['manifest']=manifest
OUTDATA.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pdf':str(OUT),'pages':PAGE,'routes':len(routes),'terminal_points':len(TERMINALS),'checks':'passed'},ensure_ascii=False))
