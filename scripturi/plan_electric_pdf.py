from pathlib import Path
import json, math, csv
ROOT=Path(__file__).resolve().parents[1]
prefix=(ROOT/'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
prefix=prefix.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'","OUT=ROOT/'output/pdf/Apartament_184_Plan_electric_R02.pdf'")
prefix=prefix.replace('R01 |','R02 |')
prefix=prefix.replace("(-1,-1),9)","(-1,-1),6)")
prefix=prefix.replace("fill=HexColor('#ffe9df'),stroke=RED,lw=1.3","fill=HexColor('#eef0f1'),stroke=GRAY,lw=.5")
exec(prefix)
c.setTitle('Apartament 184 - Instalatii electrice curenti tari si slabi - R02')
EM=json.loads((ROOT/'tmp/electric_model.json').read_text(encoding='utf-8'))
BASE={o['name']:o for o in EM if o['doc']=='apartament_184'}
PURPLE=HexColor('#7754a1')
points=[]
def add(code,name,desc,n,circuit,kind='P',coords=None,status='CAD',note=''):
 if coords is None:
  b=BASE[name]['bbox'];coords=[round((b[i]+b[i+3])/2) for i in range(3)]
 p=dict(id=code,name=name,desc=desc,n=n,circuit=circuit,kind=kind,x=coords[0],y=coords[1],z=coords[2],status=status,note=note)
 points.append(p);return p
spec=[
('P01','Priza_noptiera_stanga','Noptieră spre dulap',1,'C04'),('P02','Priza_noptiera_dreapta','Noptieră spre fereastră',1,'C04'),
('P03','Priza_dulap_dormitor','Dulap dormitor / sursă LED',1,'C04'),
('P04',None,'TV dormitor / ascuns',1,'C04','P',[3540,-1893,1410]),
('P05','Priza_machiaj_dubla','Machiaj / perete fereastră',2,'C04'),
('P06',None,'TV sufragerie / sus',1,'C05','P',[3700,-2843,1350]),
('P07',None,'Comodă TV / aparat, rezervă, soundbar',3,'C05','P',[3700,-2843,350]),
('P08','Priza_canapea_dubla','Lângă canapea',2,'C05'),
('P09','Priza_birou_dubla','Birou / existent CAD, acces lateral',2,'C05'),
('P10',None,'Birou / nou 2 Schuko + RJ45',2,'C05','P',[3700,-870,600],'PROPUS'),
('P11','Priza_fier_calcat_dressing_M3','Fier de călcat / dressing M3',1,'C05'),
('P12','Priza_masina_spalat_vestibul','Mașină de rufe / acces lateral',1,'C07'),
('P13','Prize_baie_uscator_ras','Baie / uscător și aparat de ras',2,'C06'),
('P14','Priza_frigider','Frigider / necesită acces lateral',1,'C11'),
('P15','Priza_masa_dubla','Bucătărie / masă',2,'C10'),
('P16','Priza_hota','Hotă / compartiment accesibil',1,'C10'),
('P17',None,'MSV / priză dedicată în corp vecin',1,'C08','P',[7250,-2550,250],'REVIZUIT'),
('P18',None,'Plită GAZ / aprindere electrică',1,'C10','P',[7250,-2480,250],'REVIZUIT'),
('P19','Priza_sub_chiuveta','Rezervă sub chiuvetă / zonă uscată',1,'C10'),
('P20',None,'Cuptor / priză dedicată, acces corp vecin',1,'C09','P',[7250,-550,750],'REVIZUIT'),
('P21',None,'Microunde / alimentare separată de cuptor',1,'C10','P',[7250,-450,750],'REVIZUIT'),
('P22','Priza_contrablat_dubla','Contrablat / mici electrocasnice',2,'C10'),
('P23',None,'Hol / ONT + router + switch + rezervă',4,'C12','P',[7900,-5540,2000],'PROPUS'),
('F01','Doza_LED_dressing','Alimentare LED dressing',1,'C02','F'),
('F02',None,'LED mobilier TV sufragerie',1,'C02','F',[3700,-1500,400],'PROPUS'),
('F03',None,'LED TV + oglindă machiaj dormitor',1,'C01','F',[3550,-1250,400],'PROPUS'),
('F04',None,'LED dulap hol / sursă accesibilă',1,'C02','F',[8000,-5500,2150],'PROPUS'),
('F05',None,'LED debara / sursă sus',1,'C02','F',[10400,-285,2400],'PROPUS'),
('F06',None,'LED bucătărie sub corpuri / sursă',1,'C02','F',[7250,-2200,2250],'PROPUS'),
('F07','Alimentare_ventilator_baie','Ventilator existent / L, N, PE, LT după model',1,'C03','F'),
('F08',None,'LED noptiere / 24V din P01/P02',2,'C04','F',[150,-1800,500],'PROPUS')]
for a in spec:add(*a)
lights=[('L01','Plafoniera_LED_Dormitor','Dormitor','C01'),('L02','Plafoniera_LED_CameraDeZi','Sufragerie','C01'),('L03','Plafoniera_LED_Bucatarie','Bucătărie','C02'),('L04','Plafoniera_LED_Hol','Hol','C02'),('L05','Plafoniera_LED_Nisa','Debara / nișă','C02'),('L06','Plafoniera_LED_Balcon','Balcon închis','C02'),('L07','Plafoniera_LED_vestibul','Vestibul','C03'),('L08','Plafoniera_LED_Baie','Baie','C03')]
for code,name,desc,ci in lights:add(code,name,'Plafonieră '+desc,1,ci,'L')
switches=[('S01','Intrerupator_dormitor','Dormitor / plafonieră','C01'),('S02','Intrerupator_camera_de_zi','Sufragerie / plafonieră','C01'),('S03','Intrerupator_bucatarie','Bucătărie / plafonieră + LED','C02'),('S04','Intrerupator_hol','Hol / plafonieră','C02'),('S05','Intrerupator_debara','Debara / plafonieră + LED','C02'),('S06','Intrerupator_balcon','Balcon / plafonieră','C02'),('S07','Intrerupator_LED_vestibul','Vestibul / din sufragerie','C03'),('S08','Intrerupator_baie','Baie / lumină + ventilator','C03')]
for code,name,desc,ci in switches:add(code,name,desc,2 if code in ('S03','S08') else 1,ci,'S')
data_points=[('D01','RJ45 TV sufragerie sus',[3700,-2781,1350]),('D02','RJ45 comodă sufragerie',[3700,-2719,350]),('D03','RJ45 TV dormitor',[3550,-1831,1410]),('D04','RJ45 sub birou sufragerie',[3700,-790,600])]
for code,desc,co in data_points:add(code,None,desc,1,'LAN','D',co,'CAD' if code!='D04' else 'PROPUS')
for code,desc,co in [('T01','Coax TV sufragerie sus',[3700,-2719,1350]),('T02','Coax comodă sufragerie',[3700,-2657,350]),('T03','Coax TV dormitor',[3550,-1769,1410])]:add(code,None,desc,1,'TV','T',co)
TE=(9956,-4330);NET=(7900,-5540)
# Ceiling corridor spine, branching through circulation/door areas. Corridors are schematic;
# structural crossing and mounting method must be measured before issuing execution drawings.
SPINE=[TE,(9000,-4250),(7500,-4250),(6800,-4250),(4800,-4250),(4000,-4400),(3050,-4400)]
def stem(p):
 x,y=p['x'],p['y']
 if x<2500 and y>-3920:return SPINE+[(3050,-3800),(2500,-3600),(x,-3600),(x,y)]
 if x<2500:return SPINE+[(2480,-4400),(x,-4400),(x,y)]
 if x<3700 and y>-3920:return SPINE+[(3050,-3800),(3450,-3600),(3450,y),(x,y)]
 if x<3700:return SPINE+[(x,-4400),(x,y)]
 if x<=7100:return SPINE[:5]+[(x,-4250),(x,y)]
 if x<9800 and y>-3500:return SPINE[:3]+[(8500,-4250),(8500,-3500),(x,-3400),(x,y)]
 if x>=9800 and y>-3500:return SPINE[:3]+[(8500,-3500),(9000,-2500),(9900,-2000),(x,y)]
 return SPINE[:2]+[(x,-4250),(x,y)]
def lanroute(p):return [NET,(7900,-4250)]+stem(p)[2:]
for p in points:
 p['route']=lanroute(p) if p['kind'] in ('D','T') else stem(p)
 if p['kind'] in ('D','T'):
  plan=sum(math.dist(a,b) for a,b in zip(p['route'],p['route'][1:]))/1000
  p['route_m']=round(plan+abs(2300-p['z'])/1000+0.3+2,1)
BOXES=[('J01',9000,-4250,'Hol','C02'),('J02',6800,-4250,'Sufragerie, acces lângă intrare','C01'),('J03',3450,-3600,'Dormitor, deasupra intrării','C01'),('J04',3050,-4400,'Vestibul, acces din circulație','C03'),('J05',8500,-3400,'Bucătărie, deasupra intrării','C02'),('J06',9900,-2000,'Debara, acces lângă ușă','C02')]
def union_length(paths):
 groups={}
 for pts in paths:
  for a,b in zip(pts,pts[1:]):
   dx,dy=b[0]-a[0],b[1]-a[1];dist=math.hypot(dx,dy)
   if dist<.1:continue
   ux,uy=dx/dist,dy/dist
   if ux<-.000001 or (abs(ux)<.000001 and uy<0):ux,uy=-ux,-uy
   key=(round(ux,6),round(uy,6),round(-uy*a[0]+ux*a[1],3))
   groups.setdefault(key,[]).append(sorted([ux*a[0]+uy*a[1],ux*b[0]+uy*b[1]]))
 total=0
 for intervals in groups.values():
  merged=[]
  for lo,hi in sorted(intervals):
   if merged and lo<=merged[-1][1]+.01:merged[-1][1]=max(hi,merged[-1][1])
   else:merged.append([lo,hi])
  total+=sum(hi-lo for lo,hi in merged)
 return total/1000
route_quantities=[]
for ci in ['C'+str(i).zfill(2) for i in range(1,13)]:
 pts=[p for p in points if p['circuit']==ci and p['kind']!='S' and p['id']!='F08']
 branches=union_length([p['route'] for p in pts]);drops=sum(abs(2300-p['z'])/1000+.3 for p in pts)
 # Z of TE is provisional; 1m covers its departure/service reserve.
 length=round(branches+drops+1,1)
 commands=[p for p in points if p['circuit']==ci and p['kind']=='S']
 # Each command receives a dedicated proposed branch from the closest conceptual J box.
 command_m=0
 for s in commands:
  j=min(BOXES,key=lambda j:math.dist((j[1],j[2]),(s['x'],s['y'])))
  command_m+=math.dist((j[1],j[2]),(s['x'],s['y']))/1000+abs(2300-s['z'])/1000+.6
 route_quantities.append({'id':ci,'distribution_m':length,'budget_m':math.ceil(length*1.15),'command_m':round(command_m,1),'budget_command_m':math.ceil(command_m*1.15)})
circuits=[
('C01','L01,L02,F03','Iluminat dormitor + sufragerie','3×1,5','B10+AFDD',0.35),
('C02','L03-L06,F01,F02,F04-F06','Iluminat hol, bucătărie, debara, balcon + LED','3×1,5','B10',0.45),
('C03','L07,L08,F07','Iluminat vestibul + baie + ventilator','3×1,5; comandă 4/5 fire','B10',0.15),
('C04','P01-P05,F08','Prize dormitor + LED noptiere','3×2,5','B16+AFDD',1.5),
('C05','P06-P11','Prize sufragerie, TV, birou, fier','3×2,5','B16',2.5),
('C06','P13','Prize baie / dedicat','3×2,5','B16',2.0),
('C07','P12','Mașină de spălat rufe / dedicat','3×2,5','B16',2.2),
('C08','P17','Mașină de spălat vase / dedicat','3×2,5','B16',2.0),
('C09','P20','Cuptor / dedicat','3×2,5','B16*',3.0),
('C10','P15,P16,P18,P19,P21,P22','Prize bucătărie + hotă + aprindere gaz','3×2,5','B16',2.5),
('C11','P14','Frigider / dedicat','3×2,5','B16',0.3),
('C12','P23','Echipamente internet / dedicat','3×2,5','B16',0.15)]
LINKS={'I7':'https://legislatie.just.ro/Public/DetaliiDocument/286763','ghid':'https://www.se.com/ro/ro/work/products/product-launch/electrical-installation-guide/','manual':'https://www.se.com/ro/ro/download/document/Manual_inst_electrice2024/','canal':'https://www.legrand.ro/sites/g/files/ocwmcr861/files/2024-06/brosura_sisteme_perimetrale_legrand_-_dlp_si_dlp-s_ud2022next.pdf','aparataj':'https://www.se.com/ro/ro/work/products/residential-and-small-business/','rcbo':'https://www.se.com/rs/sr/product/A9D56616/acti9-idpn-n-vigi-rcbo-1p%2Bn-16a-b-kriva-6000a-30ma-tip-a/','patch':'https://www.legrand.ro/ro/catalog/produse/patch-cord-rj-45-cat-6-sfutp-ecranat-pvc-5-m-albastru-051755'}
LINKS['ordin']='https://legislatie.just.ro/public/DetaliiDocument/271142'
LINKS['afdd']='https://www.eaton.com/content/dam/eaton/markets/residential/fire-safety/documents/romanian/eaton-gama-de-produse-afdd-ro.pdf'
def lk(key,label=None):return '<link href="'+LINKS[key]+'" color="#277dba"><u>'+(label or key)+'</u></link>'
def sheet(code,title,sub,scale='Fără scară'):start(code,title,sub,scale)
def route_draw(P,pts,color,lw=1):
 for a,b in zip(pts,pts[1:]):line(*P(*a),*P(*b),color,lw,[3,2])
LABELS=[]
def symbol(P,p,label=True):
 x,y=P(p['x'],p['y']);kind=p['kind'];col={'P':RED,'F':ORANGE,'L':TEAL,'S':TEAL,'D':BLUE,'T':PURPLE}[kind]
 if kind=='L':circle(x,y,6,col,white);line(x-4,y-4,x+4,y+4,col);line(x-4,y+4,x+4,y-4,col)
 elif kind=='S':circle(x,y,3,col,white);line(x,y,x+5,y-7,col)
 elif kind in ('D','T'):rect(x-4,y-4,8,8,white,col)
 else:circle(x,y,4,col,white);line(x-2,y-2,x-2,y+2,col);line(x+2,y-2,x+2,y+2,col)
 if label:
  lx,ly=x+7,y-5
  while any(abs(lx-a)<25 and abs(ly-b)<10 for a,b in LABELS):ly+=11
  LABELS.append((lx,ly))
  if abs(ly-y+5)>1:line(x+3,y,lx-2,ly-2,col,.4)
  txt(lx,ly,p['id'],8,col,True)
def plan(selected,ox=60,oy=265,scale=50,routes=False):
 LABELS.clear()
 P,k=view(ox,oy,scale)
 for name,x,y in [('DORMITOR',1200,-1500),('CAMERA DE ZI',4700,-1900),('BUCĂTĂRIE',8050,-1200),('BAIE',850,-4650),('VESTIBUL',2730,-5150),('HOL',8400,-5100),('DEBARA',10000,-950),('BALCON',4300,650)]:txt(*P(x,y),name,8,MUT,True)
 for p in selected:
  if routes:route_draw(P,p['route'],BLUE if p['kind']=='D' else PURPLE if p['kind']=='T' else ORANGE if p['kind'] in ('L','S','F') else RED,.55)
  symbol(P,p)
 x,y=P(*TE);rect(x-6,y-6,12,12,RED,RED);txt(x+9,y+2,'TE',9,RED,True)
 return P,k
def register(rows,title,code):
 sheet(code,title,'Coordonate globale CAD în mm; Z = centru față de pardoseala finită')
 table(42,155,[55,315,75,75,70,80,85,351],[['ID / nr.','Funcțiune','X','Y','Z','Circuit','Statut','Montaj / observații']]+rows,9)
 end()
def row(p):
 note=p['note'] or ('Separare fizică 230V/date; acces service' if p['kind'] in ('D','T') or 'TV' in p['desc'] else 'Coordonare cu mobilierul și finisajele')
 return [p['id']+' / '+str(p['n']),p['desc'],p['x'],p['y'],p['z'],p['circuit'],p['status'],note]

sheet('E00','Instalația electrică / dosar de coordonare','Curenți tari + curenți slabi | poziții, trasee, doze, tablou, rețea și cantități')
for x,title,val,sub in [(42,'ALIMENTARE','12 circuite','Separare iluminat / prize / aparate'),(410,'REȚEA','4 RJ45 + 3 TV','Legături individuale la distribuție'),(778,'ILUMINAT','8 plafoniere','LED mobilier și ventilator incluse')]:
 rect(x,150,350,112,LIGHT,GRAY);txt(x+15,177,title,11,TEAL,True);txt(x+15,213,val,25,INK,True);txt(x+15,240,sub,10,MUT)
para(42,290,525,'<b>Baza planului</b><br/>Modelul FreeCAD salvat, amenajarea curentă și cerințele beneficiarului. Tabloul și intrarea internetului sunt deasupra ușii apartamentului. Coordonatele TE sunt aproximative; nișa se măsoară. Routerul este propus în hol. Originea CAD este colțul exterior stânga-sus; X spre dreapta, Y negativ spre jos, Z față de pardoseala finită.',12)
para(620,290,525,'<b>Nivelul documentației</b><br/>Plan de coordonare și ofertare. Trasee propuse pe tavan/în mască accesibilă, fără șanțuri presupuse în beton. Protecțiile și secțiunile sunt preselecții: se validează după branșament, puteri reale, mod de pozare, lungimi, scurtcircuit și măsurători PE.',12)
table(42,450,[70,440,596],[['Planșe','Conținut','Scop'],['E01-E04','Poziții prize, iluminat, trasee 230V, curenți slabi','Planuri A3 1:50 și topologia rețelei'],['E05-E07','Registre aparataj și cote de montaj','Identificare unică, cantități, stare CAD/propunere'],['E08-E09','Circuite și schemă de principiu tablou','12 plecări propuse, protecții și verificări'],['E10-E13','TV/birou, doze, hol/router, baie și LED','Detalii acces, separare și montaj'],['E14-E17','Cantități, cabluri, verificări și surse','Ofertare, rezervă, recepție'],['E18','Secțiune verticală și cote locale de poziționare','Montaj și coordonare cu pereții / mobilierul'] ],10)
end()

sheet('E01','Curenți tari / poziții prize și alimentări','Fiecare grup este identificat în E05-E06; circuitele sunt în E08','1:50 la imprimare A3, 100%')
P,k=plan([p for p in points if p['kind'] in ('P','F')])
para(750,180,395,'<b>Roșu:</b> prize 230V P01-P23.<br/><b>Ocru:</b> racorduri fixe / surse LED F01-F08.<br/><b>TE:</b> tabloul existent deasupra intrării. Poziția aproximativă X≈9956, Y≈-4330; axa reală se măsoară.<br/><br/>P10 este grupul cerut sub birou: 2 Schuko + RJ45. P09 rămâne priza laterală deja modelată. Nu reapare priza eliminată de sub geamul dormitorului.<br/><br/>Prizele cuptorului și MSV au circuite proprii, chiar dacă simbolurile vechi erau grupate în aceeași ramă. Plita din CAD este pe gaz; se alimentează doar aprinderea. O viitoare plită electrică necesită dimensionare nouă.',11)
para(750,490,395,'<b>Acces în mobilier</b><br/>Nu se lasă prize direct în spatele aparatului unde împiedică retragerea sau sunt inaccesibile. Se rezervă compartiment lateral uscat, accesibil, coordonat cu tâmplarul. P14, P17, P20 și P21 au cotele inițiale CAD; montajul exact se ajustează după electrocasnice.<br/><br/>P23: patru prize pentru ONT, router, switch și rezervă, pe circuit C12. Modulul de date este separat fizic de 230V.',11)
end()

sheet('E02','Iluminat / comenzi și alimentări LED','Plafoniere LED; întrerupătoare păstrate în pozițiile stabilite','1:50 la imprimare A3, 100%')
P,k=plan([p for p in points if p['kind'] in ('L','S')])
for s,l in [('S01','L01'),('S02','L02'),('S03','L03'),('S04','L04'),('S05','L05'),('S06','L06'),('S07','L07'),('S08','L08')]:
 a=next(p for p in points if p['id']==s);b=next(p for p in points if p['id']==l);route_draw(P,[(a['x'],a['y']),(b['x'],b['y'])],TEAL,.7)
para(750,175,395,'Liniile verzi indică <b>relația comandă-lampă</b>, nu traseul fizic al cablului.<br/><br/>S07 este în sufragerie, la intrarea în vestibul. S08 este în vestibul, pentru lumină baie și ventilator. S03 este dublu: plafonieră bucătărie + LED contrablat.<br/><br/>S05 comandă plafoniera debaralei; LED rafturi prin senzor de ușă sau comandă separată, după accesoriul ales. Dressing: 5 senzori de uși, alimentare permanentă a sursei 24V.<br/><br/>S01/S02 pot deveni duble dacă se dorește LED mobilier de la intrare; în această variantă LED-urile decorative au comandă locală accesibilă. Nu se folosește un întrerupător în același grup pentru circuite diferite.',11)
para(750,530,395,'<b>Preselecție lumină</b><br/>3000K pentru camere/hol; bucătărie și baie 3000-4000K după finisaje. Fluxul și puterea se aleg prin verificarea iluminării reale; diametrele CAD nu reprezintă fișe comerciale. Alimentare N și PE până la corp; PE se termină izolat la corpurile clasa II. În dozele comenzilor se rezervă N pentru accesorii viitoare.',11)
end()

sheet('E03','Curenți tari / coridoare și coborâri propuse','Reprezentare schematică în plan; cote de traseu și detalii în E11','1:50 la imprimare A3, 100%')
P,k=plan([],routes=False)
for pts in [SPINE,SPINE+[(3050,-3800),(2500,-3600),(300,-3600),(300,-450)],SPINE+[(2480,-4400),(1650,-4400),(1650,-5550)],SPINE[:5]+[(4000,-4250),(4000,-600)],SPINE[:3]+[(8500,-3500),(7350,-3400),(7350,-550)],SPINE[:3]+[(8500,-3500),(9000,-2500),(9900,-2000),(10400,-285)]]:route_draw(P,pts,RED,1.6)
for id,x,y,desc,ci in BOXES:
 xx,yy=P(x,y);rect(xx-4,yy-4,8,8,ORANGE,ORANGE);txt(xx+7,yy-5,id,9,ORANGE,True)
for p in [p for p in points if p['kind']=='P']:symbol(P,p)
para(750,170,395,'<b>Traseul de principiu</b><br/>TE → hol → sufragerie → vestibul → dormitor/baie; ramuri distincte spre bucătărie/debara. Coridoarele roșii sunt axele de coordonare ale tuburilor, nu un singur cablu comun tuturor circuitelor.<br/><br/>Distribuție în tuburi separate, pe intrados în mască/canal tehnic accesibil; cota propusă Z≈2300 mm, de coordonat cu golurile, draperiile și mobilierul până aproape de tavan. Coborâri verticale la aparataj.<br/><br/>J01-J06 sunt doze accesibile pentru iluminat/LED. Circuitele aparatelor dedicate pleacă individual din TE la receptor. Prizele generale se distribuie în doze adânci ale aparatajului, cu continuitatea PE verificabilă.',11)
para(750,545,395,'<b>Perete portant / planșeu</b><br/>Planul nu autorizează șanțuri sau găuri în structură. Traversările prin goluri/zone permise și tipul măștii se verifică la măsurători. Nu se îngroapă îmbinări fără acces; se fotografiază traseele înainte de închidere. Nu se combină circuite diferite fără compartimentare și identificare.',11)
end()

sheet('E04','Curenți slabi / LAN, coaxial și router','Legături în stea, cabluri individuale, fără legare în serie','1:50 la imprimare A3, 100%')
P,k=plan([p for p in points if p['kind'] in ('D','T')],routes=True)
xx,yy=P(*NET);rect(xx-6,yy-6,12,12,BLUE,BLUE);txt(xx+9,yy+3,'NET / R',9,BLUE,True)
route_draw(P,[TE,(9000,-4250),(7900,-4250),NET],BLUE,1.5)
para(750,160,395,'<b>Distribuție propusă NET</b><br/>Hol, peretele dinspre dressing, compartiment ventilat accesibil la X≈7900, Y≈-5540, Z≈2000 mm. ONT/patch-panel/coax într-un compartiment tehnic; router Wi-Fi pe suport deschis sau cu front nemetalic și ventilație. Dimensiunea finală după echipamente; orientativ spațiu 450×350×150 mm pentru partea pasivă, router separat dacă nu încape.<br/><br/>Intrarea operatorului: deasupra U7. Tub separat până la NET; fibră fără curbări strânse și îmbinări improvizate.<br/><br/><font color="#277dba">D01-D04:</font> câte un Cat6 cupru integral la patch-panel. <font color="#7754a1">T01-T03:</font> câte un coax 75Ω la distribuția TV. Biroul are date, fără coax cerut.',11)
para(750,545,395,'Router → switch doar dacă porturile LAN sunt insuficiente → patch-panel → prize. Pentru 4 prize, switch de 8 porturi oferă rezervă; patch-panel de 8 porturi, cu 4 populate. Distribuitor coax cu 3 ieșiri active / 4 cu una terminată, numai dacă semnalul operatorului permite. IPTV poate folosi Cat6; nu se presupune că fibra oferă automat semnal coax.<br/><br/>HDMI este local între TV și comodă, în tub propriu accesibil; nu merge până la router.',10)
end()

for code,title,sel in [('E05','Registru prize / camere și baie',[p for p in points if p['kind']=='P' and int(p['id'][1:])<=13]),('E06','Registru prize / bucătărie și rețea',[p for p in points if p['kind']=='P' and int(p['id'][1:])>13]+[p for p in points if p['kind']=='F' and p['id']!='F08'])]:
 register([row(p) for p in sel],title,code)
sheet('E07','Registru iluminat / comenzi / date','Cote de montaj la centrul aparatajului; corpuri de tavan la intrados ≈2500 mm')
table(42,150,[55,275,175,65,80,456],[['ID','Funcțiune','X / Y [mm]','Z','Circuit','Observație']]+[[p['id'],p['desc'],str(p['x'])+' / '+str(p['y']),p['z'],p['circuit'],'Comandă la 1050 mm, ajustată față de toc' if p['kind']=='S' else 'Corp LED / montaj pe tavan' if p['kind']=='L' else 'Cat6 / 75Ω în tub separat; fără îmbinare ascunsă'] for p in points if p['kind'] in ('L','S','D','T')],9)
end()

sheet('E08','Circuite / preselecție protecții și conductoare','Cupru; PE continuu; fiecare circuit propus cu RCBO 1P+N, 30mA, tip A')
table(42,150,[55,155,320,175,75,80,226],[['Circuit','Puncte','Destinație','Cu [mm²] propus','Curba/In','P estim. kW','Validare']]+[[ci,ids,desc,sec,prot,pow,'Iz, ΔU, Ik, mod pozare și manual receptor'] for ci,ids,desc,sec,prot,pow in circuits],9)
para(42,615,1106,'<b>Preselecțiile nu înlocuiesc calculul:</b> Ib ≤ In ≤ Iz, scădere de tensiune, curent de scurtcircuit/putere de rupere și timp de deconectare. B10/1,5 mm² și B16/2,5 mm² sunt soluții inițiale, nu dimensionări garantate pentru orice pozare. *Cuptorul: puterea nominală și racordarea se verifică din manual; dacă depășește capacitatea circuitului propus, se redimensionează. Mașina cu invertor poate cere tip F/B în loc de A, după producător.',11)
para(42,700,1106,'Puterile sunt ipoteze de buget, nu valori de pe etichete. Total instalat estimativ: '+str(round(sum(ci[5] for ci in circuits),2))+' kW; nu este puterea simultană admisă. Puterea aprobată și siguranța branșamentului sunt necunoscute; se întocmește bilanț cu simultaneitate și se evită depășirea lor. Nu se mărește siguranța generală fără verificarea coloanei.',10)
end()

sheet('E09','Tablou electric / schemă de principiu','Schema finală depinde de tipul rețelei existente și de puterea aprobată')
for x,title,body in [(42,'BRANȘAMENT / CONTOR','Număr faze, secțiune coloană, protecție amonte, putere contractată și schemă TN/TT: de verificat.'),(410,'SECȚIONARE + SUPRATENSIUNE','Separator general dimensionat; SPD după evaluare și protecția existentă a clădirii, cu coordonare amonte.'),(778,'DISTRIBUȚIE / 12 RCBO','Plecări 1P+N cu 30mA; neutrul propriu fiecărui circuit și bară PE continuă. Tip/curbă după receptor.')]:panel(x,155,350,title,body)
line(360,220,400,220,RED,2);line(728,220,768,220,RED,2)
line(65,355,1120,355,RED,2)
line(50,355,50,525,RED,1);line(50,525,1120,525,RED,2)
txt(65,339,'Plecare L/N către fiecare RCBO; barele N/PE se detaliază după schema reală',10,MUT)
for i,ci in enumerate(circuits):
 col=i%6;rowi=i//6;x=65+col*180;y=400+rowi*145
 line(x+65,355 if rowi==0 else 525,x+65,y,RED,.7);rect(x,y,145,105,LIGHT,GRAY);txt(x+12,y+24,ci[0],14,TEAL,True);txt(x+12,y+46,ci[4]+' / 30mA',10,INK,True);para(x+12,y+56,121,ci[2],9)
para(42,700,1106,'<b>Carcasă orientativă:</b> 54 module, de verificat după RCBO/SPD și cele 2 AFDD prevăzute pentru C01 și C04 (circuite dormitor). Se păstrează ≈20% rezervă. AFDD la originea circuitului, combinat sau asociat compatibil cu protecțiile. '+lk('ordin','Ordin 959/2023, pct. 4.2.2.10-12')+'. Nu se leagă N la PE în avalul diferențialelor; nu se inventează PE din nulul prizei. Separarea PEN se proiectează numai în punctul permis. Tabloul rămâne accesibil.',10)
end()

sheet('E10','Detalii multimedia / TV și birou','Doze separate sau carcasă certificată cu separatoare; acces pentru mentenanță')
for x,title,top,bottom in [(42,'SUFRAGERIE',1350,350),(610,'DORMITOR',1410,400)]:
 rect(x+25,175,435,180,LIGHT,GRAY);txt(x+45,198,title+' / ECRAN',12,TEAL,True)
 for j,t in enumerate(['230V','RJ45','COAX','HDMI']):rect(x+90+j*72,255,65,45,white,RED if j==0 else BLUE);txt(x+96+j*72,281,t,10)
 txt(x+45,330,'Centru grup ascuns Z='+str(top)+' mm',10,MUT)
 lower=[('3×230V',x+50,90),('RJ45',x+150,90),('COAX',x+250,90),('HDMI',x+350,90)] if x==42 else [('LED 230V',x+70,100),('HDMI',x+290,100)]
 for j,(t,bx,bw) in enumerate(lower):rect(bx,440,bw,55,white,RED if j==0 else BLUE);txt(bx+7,470,t,10)
 end_x=x+395 if x==42 else x+340
 for a,b in zip([(x+338.5,300),(x+338.5,395),(end_x,395)],[(x+338.5,395),(end_x,395),(end_x,440)]):line(*a,*b,BLUE,1.5,[4,2])
 txt(x+40,520,'Jos Z='+str(bottom)+' mm; acces din mobilier',10,MUT)
para(42,560,520,'<b>Sufragerie:</b> sus 1 Schuko + RJ45 + coax + perie HDMI; jos 3 Schuko (aparat, rezervă, soundbar) + RJ45 + coax + perie HDMI. Două cabluri Cat6 și două coax individuale. Cablu HDMI direct, fără adaptor mascat. Tub de trecere orientativ Ø32-40 mm după mufa HDMI, curbe largi și fir de tragere.',11)
para(610,560,535,'<b>Dormitor:</b> sus 1 Schuko + RJ45 Cat6 + coax + perie HDMI. Alimentarea LED-ului comodei/oglinzii este racord separat F03, propus la Z400; nu se adaugă tacit al doilea modul multimedia jos.<br/><b>Birou:</b> P10 + D04 sub blat, Z600; 2 Schuko și RJ45 în compartimente separate. Lăsăm cablu flexibil suficient pentru biroul reglabil, până la cursa maximă, fără tensionare.',11)
para(42,715,1106,'Dimensiunile desenate sunt de principiu, nu șablon de găurire. Poziția exactă a modulelor se confruntă cu VESA, suportul TV, conectorii aparatelor și grosimea panoului decorativ. Nu se ascund prize în spatele unei plăci care nu se poate demonta.',10)
end()

sheet('E11','Doze / secțiune de traseu / separare','Propunere de montaj cu mască demontabilă; fără intervenții presupuse în structură')
table(42,155,[65,210,190,100,541],[['ID','Poziție','X / Y [mm]','Z [mm]','Funcție / acces']]+[[id,desc,str(x)+' / '+str(y),2300,'Doză iluminat '+ci+'; capac accesibil. Nu reprezintă îmbinare pentru toate circuitele.'] for id,x,y,desc,ci in BOXES],10)
rect(70,470,520,150,LIGHT,GRAY);txt(85,493,'SECȚIUNE DE PRINCIPIU / MASCĂ',12,TEAL,True)
rect(95,525,180,55,white,RED);txt(108,558,'230V / tuburi circuit',11,RED)
rect(350,525,180,55,white,BLUE);txt(365,558,'LAN + coax / tuburi',11,BLUE)
line(305,520,305,595,INK,2);txt(95,605,'Separator fizic / sistem certificat / capac service',10,MUT)
para(635,460,505,'<b>Distanța/separarea</b><br/>Nu se adoptă o distanță universală pentru toate cablurile. Se alege după sistemul de pozare, ecranare, compatibilitate electromagnetică și prescripțiile producătorului. Canal compartimentat certificat sau tuburi independente; încrucișări pe cât posibil la 90°. 24V LED în compartiment distinct de 230V.<br/><br/><b>Doze aparataj</b><br/>Adâncime orientativă ≥60 mm unde spațiul permite; ramă și număr de module după seria aleasă. Doze separate pentru date și 230V sau separatoare aprobate. Nu se amestecă firele în aceeași doză simplă. Îmbinări numai în doze accesibile, cu borne certificate.',11)
para(42,685,1106,'Z≈2300 mm este o cotă propusă a coridorului, nu înălțimea unui tavan nou. Se verifică spațiul deasupra ușilor, corpurile înalte, șinele draperiilor și conducta hotei. Dacă nu există loc, se revizuiește traseul înainte de execuție. Diametre tuburi orientative: 20 mm pentru prize, 16-20 pentru lumină, 20-25 pentru fiecare Cat6/coax, după umplere și posibilitatea de retragere.',10)
end()

sheet('E12','Intrare / router / rack de apartament','Tablou și intrare operator deasupra U7; distribuție NET propusă în hol')
panel(42,155,350,'1 / DEASUPRA INTRĂRII','TE existent și intrare operator, în carcase distincte. Coordonata desenată este orientativă. Se măsoară spațiul față de tavan și accesul la protecții.')
panel(410,155,350,'2 / TUB OPERATOR → NET','Fibră/coax în tub separat, rezervă de tragere și raze după operator. Nu se desfășoară fibra în tabloul de 230V; nu se mută terminația fără operator.')
panel(778,155,350,'3 / COMPARTIMENT HOL','P23 cu 4 Schuko, patch-panel 8 porturi/4 populate, ONT, distribuție coax și switch 8 porturi opțional. Acces din front, ventilație permanentă.')
for i,(name,body) in enumerate([('ONT','Conversie fibră / intrare ISP'),('ROUTER','WAN din ONT; Wi-Fi în zona holului'),('SWITCH','8 porturi, dacă routerul nu ajunge'),('PATCH-PANEL','D01,D02,D03,D04 / etichete identice')]):
 x=65+i*275;rect(x,390,230,90,LIGHT,BLUE);txt(x+12,416,name,13,BLUE,True);para(x+12,433,206,body,10)
 if i<3:line(x+230,435,x+270,435,BLUE,2)
para(42,535,525,'<b>Wi-Fi</b><br/>Holul este o propunere accesibilă, dar acoperirea prin pereții dintre camere se verifică după instalare. Nu se închide routerul într-un dulap metalic. Dacă dormitorul nu are semnal suficient, se poate instala un punct de acces pe D03 sau se adaugă traseu dedicat; nu este inclus ca echipament obligatoriu.',12)
para(620,535,525,'<b>Conectică și service</b><br/>P23: ONT, router, switch, rezervă; fără prelungitor permanent improvizat. Patch-corduri scurte până la patch-panel. 0,5-1 m rezervă ordonată la distribuție și ≈0,3 m în doza de date, respectând raza cablului. Coax: splitter numai după nivelul de semnal măsurat; porturile libere se termină 75Ω.',12)
end()

sheet('E13','Baie / zone și LED mobilier','Protecția la apă se verifică pentru echipamentul și poziția reale; paravanul nu elimină automat zonele')
LABELS.clear()
k=72/25.4/15
def P(x,y):return 70+(x-150)*k,180+(-3920-y)*k
rect(70,180,2300*k,1630*k,HexColor('#fafbfb'),INK)
# Local bathroom drawing overlays, constrained to viewport.
c.saveState();pa=c.beginPath();pa.rect(42,H-155-420,555,420);c.clipPath(pa,stroke=0)
poly([P(150,-3920),P(850,-3920),P(850,-5420),P(150,-5420)],fill=HexColor('#dceef7'),color=BLUE)
poly([P(850,-3920),P(1450,-3920),P(1450,-5420),P(850,-5420)],fill=HexColor('#fff0df'),color=ORANGE)
for id in ['P13','F07','L08']:symbol(P,next(p for p in points if p['id']==id))
c.restoreState()
txt(83,204,'CADĂ / proiecție zonă 1',10,BLUE,True)
txt(*P(880,-4100),'Zonă 2',10,ORANGE,True)
dim(*P(850,-5450),*P(1450,-5450),'600',28)
dim(*P(850,-5550),*P(1572.5,-5550),'≈722,5 până la marginea prizei',60)
para(42,605,550,'Cadă X150…850; P13 centru X1650. Marginea prizei CAD este X1572,5: distanță nominală față de cada ≈722,5 mm, peste extensia laterală orientativă de 600 mm a zonei 2. Finisajele, poziția jetului și dimensiunea aparatului se verifică; nu se bazează protecția doar pe capacul IP44.',10)
para(650,160,495,'<b>Baie / C06 și C03</b><br/>P13: 2 Schuko cu PE, RCBO 30mA, în afara zonelor în care prizele obișnuite sunt interzise. IP44 sau mai mare după expunere și montaj; capacul deschis poate modifica gradul IP. Întrerupător S08 în vestibul.<br/><br/>Ventilator existent deasupra căzii, Z≈2350: se măsoară cota exactă și se verifică zona reală inclusiv înălțimea dușului. Se selectează aparat permis acolo, de regulă cu protecție la stropire corespunzătoare; dacă nu corespunde, nu se energizează în poziția actuală. Pentru temporizare se duc L permanent, LT comandat, N și PE după clasa aparatului; PE nefolosit se izolează, nu se elimină.<br/><br/>Legături echipotențiale și PE conform situației instalației; se verifică necesitatea și continuitatea, fără a lega arbitrar orice piesă metalică.',11)
para(650,505,495,'<b>LED mobilier / 24V</b><br/>Surse accesibile, ventilate și separate de textile. Putere sursă ≥ suma W/m × lungime, plus rezerva recomandată de producător (uzual 20-25%). Driver compatibil cu banda/controlerul, profil aluminiu cu difuzor, protecție fiecare ramură și cablu dimensionat la curent și scădere de tensiune.<br/><br/>Dressing: 5 benzi ≈3,17 m total și 5 senzori; debara ≈8,6 m după piesele CAD; celelalte benzi se măsoară pe mobilierul final. F08: cele două noptiere se alimentează din P01/P02 cu surse adecvate, fără fire 230V expuse în nișă.',11)
end()

sheet('E14','Lista de cantități / aparataj și echipamente','Cantități ale variantei propuse; linkuri de referință, fără prețuri sau comenzi')
ns=sum(p['n'] for p in points if p['kind']=='P')
table(42,150,[70,370,130,310,226],[['Cod','Articol','Cantitate','Observație','Referință']]+[
['IE01','Prize Schuko 16A cu PE',str(ns)+' mecanisme','Include P23×4 și P10×2; baia×2 cu protecție adecvată',lk('aparataj','Gama / selecție')],
['IE02','Întrerupătoare', '8 poziții','6 simple + 2 duble (S03,S08); opțiunile decorative pot schimba numărul tastelor',lk('aparataj','Gama / selecție')],
['IE03','Plafoniere LED','8 buc','Modele/flux/IP de selectat; cele din CAD sunt gabarite',lk('aparataj','Catalog iluminat/comandă')],
['IE04','Doze derivație accesibile','6 buc','J01-J06; dimensionare după număr fire și borne',lk('canal','Sisteme compartimentate')],
['IE05','Tablou electric','1 ans.','54 module orientativ, spațiu real de măsurat',lk('ghid','Ghid proiectare')],
['IE06','RCBO circuite terminale','12 buc','3×B10 + 9×B16 ca preselecție; tip A/30mA, tip final după receptori',lk('rcbo','Exemplu B16 tip A')],
['IE07','Separator general, SPD, bare N/PE + AFDD','1 set + 2 AFDD','AFDD pe C01/C04; pot fi integrate cu RCBO, fără dublare inutilă',lk('afdd','AFDD / catalog Eaton')],
['IE08','Sursă LED / comandă','De dimensionat','Dressing, debara, hol, TV, oglindă, bucătărie, noptiere; nu dublăm sursele incluse',lk('aparataj','Selecție')],
['IE09','Doze aparataj, rame, separatoare','După gama aleasă','23 grupuri P + 8 S + racorduri F + date; nu echivalăm grupul cu o singură doză standard',lk('canal','Separare / carcase')],
['IE10','Borne, etichete, cleme, accesorii','1 lot','După secțiuni și număr conductoare; etichete circuit la ambele capete',lk('ghid','Ghid')],
['IE11','Tuburi și cabluri Cu 230V','Estimare E17','1,5 / 2,5 mm² preselecție; lungimi finale după traseul aprobat',lk('manual','Dimensionare')],
['IE12','Ventilator baie','1 existent','Reutilizare doar după verificarea zonei/IP/clasei și manualului',lk('I7','I7 actualizat')]],9)
end()

sheet('E15','Curenți slabi / cabluri și necesar','Lungimile sunt estimări geometrice ale traseelor propuse, nu cantități măsurate în șantier')
lan=[p for p in points if p['kind']=='D'];coax=[p for p in points if p['kind']=='T']
table(42,150,[75,395,160,220,256],[['ID','Legătură individuală','Traseu estimat m','Cu 10% rezervă m','Observație']]+[[p['id'],p['desc'],p['route_m'],round(p['route_m']*1.1,1),'Include coborâre la punct și ≈2 m rezervă/service'] for p in lan+coax],10)
table(42,435,[70,450,130,456],[['Cod','Material / echipament','Cantitate','Detaliu']]+[
['ISL01','Cablu Cat6 cupru integral / fără CCA',str(math.ceil(sum(p['route_m'] for p in lan)*1.1))+' m estim.','4 legături; U/UTP sau ecranat ales ca sistem coerent, după separare'],
['ISL02','RJ45 Cat6 + patch-panel 8 porturi','4 + 1 buc','4 porturi populate; testare permanent-link Cat6'],
['ISL03','Coaxial 75Ω + mufe terminale',str(math.ceil(sum(p['route_m'] for p in coax)*1.1))+' m + 3 prize','Distribuitor 3/4 ieșiri condiționat de semnal/operator'],
['ISL04','ONT/router + switch 8 porturi','1 / 1 / opțional','ONT/router după operator, Wi-Fi verificat pe teren'],
['ISL05','Patch-corduri date','4-5 buc','4 spre patch-panel; uplink dacă switch separat; '+lk('patch','Exemplu Cat6')],
['ISL06','HDMI + tub de service local','1 traseu living','Dormitor: rezervă locală numai după aparatele alese'],
['ISL07','Tub operator, suport router, distribuție','1 set','Lungimi/diametre după traseul final; '+lk('canal','Sisteme separate')]],9)
end()

sheet('E16','Montaj / recepție / puncte de închis','Checklist pentru transformarea dosarului de coordonare în proiect de execuție')
panel(42,155,525,'ÎNAINTE DE EXECUȚIE','1. Măsurăm TE și intrarea ISP; identificăm mono/trifazat, puterea aprobată, coloana, schema de legare la pământ și PE.<br/>2. Confirmăm puterile și manualele cuptorului, MSV, mașinii de rufe, ventilatorului și LED-urilor.<br/>3. Alegem sistemul de pozare, verificăm structura și spațiul real pentru trasee; calculăm secțiuni, ΔU, Ik și protecții.<br/>4. Coordonăm dozele cu tocurile, TV/VESA, mobilierul, draperiile, biroul reglabil și accesul la electrocasnice.')
panel(620,155,525,'LA RECEPȚIE','Verificare continuitate PE/echipotențializare, izolație, polaritate, impedanță buclă, timpi/curent declanșare diferențiale, legare la pământ după sistem și probă funcțională. Rezultatele se consemnează.<br/><br/>Cat6: test permanent-link, identificare D01-D04, conectare corectă și certificare după categoria sistemului. Coax: nivel/calitate semnal la fiecare priză. Fotografii trasee și plan conform executat, etichete în TE, doze și patch-panel.')
para(42,495,525,'<b>Surse consultate / acces 05.10.2026</b><br/>'+lk('I7','I7-2011, text consolidat / Portal Legislativ')+'<br/>'+lk('ordin','Ordin 959/2023 / actualizare I7')+'<br/>'+lk('ghid','Schneider Electric / ghid proiectare')+'<br/>'+lk('manual','Schneider Electric / manual 2024')+'<br/>'+lk('canal','Legrand / canalizare compartimentată')+'<br/>'+lk('rcbo','Schneider / exemplu RCBO B16 30mA tip A')+'<br/>'+lk('patch','Legrand / exemplu patch-cord Cat6'),11)
para(620,495,525,'<b>Ce rămâne de validat</b><br/>Nu avem măsurători electrice, puterea aprobată, fișele tuturor aparatelor sau releveul traseelor existente. Schema nu afirmă că apartamentul are deja PE funcțional sau că tabloul actual are loc pentru toate protecțiile.<br/><br/>Pozițiile marcate PROPUS/REVIZUIT completează CAD-ul și nu sunt confundate cu instalația existentă. Documentația se definitivează de proiectant/electrician autorizat pe baza verificărilor înainte de execuție.',11)
end()
sheet('E17','Estimare cabluri 230V / pe circuite','Calcul geometric al variantei propuse; rezervă 15%; nu listă definitivă de comandă')
table(42,150,[70,160,160,185,175,356],[['Circuit','Distribuție estim. m','Buget +15% m','Comenzi estim. m','Comenzi +15% m','Tip / observație']]+[[r['id'],r['distribution_m'],r['budget_m'],r['command_m'],r['budget_command_m'],'3×1,5 mm² + comenzi 4/5×1,5 după funcție' if i<3 else '3×2,5 mm²; borne în doze aparataj'] for i,r in enumerate(route_quantities)],10)
para(42,595,1106,'<b>Metoda:</b> segmentele comune de distribuție sunt numărate o singură dată în interiorul fiecărui circuit; între circuite cablurile rămân individuale. Se adaugă coborârile Z2300 → Z aparat, ≈0,3 m rezervă la punct și 1 m la plecarea TE. Comenzile sunt estimate separat de la doza apropiată, cu 0,6 m rezervă totală; traseul real comandă-lampă se finalizează după montaj. F08 este 24V local și nu se adaugă încă o alimentare din TE.',11)
para(42,685,1106,'<b>Nu se însumează direct pentru tuburi:</b> diametrul, gradul de umplere și numărul tuburilor depind de circuitele paralele și de sistemul ales. Lungimea traseului plafonului nu reprezintă metri de conductor individual: valorile sunt metri de cablu multiconductor echivalent. Pentru conductori în tub se întocmește lista pe culori/secțiuni după schema finală. Alimentările cu mai multe fire (ventilator, comenzi duble) se completează după aparat.',10)
end()
sheet('E18','Secțiune de montaj / cote locale','Secțiune verticală convențională; aparatajul este dispus comparativ, nu pe un singur perete','Secțiune 1:15 la imprimare A3, 100%')
ss=72/25.4/15;floor_y=685
def Z(z):return floor_y-z*ss
rect(70,Z(2500),20,2500*ss,HexColor('#e6e9eb'),GRAY)
line(70,floor_y,555,floor_y,INK,1.5);line(70,Z(2500),555,Z(2500),INK,1.5)
txt(95,Z(2500)-12,'INTRADOS TAVAN / Z≈2500',10,MUT,True)
txt(95,floor_y+20,'PARDOSEALĂ FINITĂ / ±0,00',10,MUT,True)
for z,label in [(300,'Canapea / P08'),(600,'Birou sub blat / P10 + D04'),(650,'Noptiere / P01-P02'),(1050,'Întrerupătoare / S'),(1350,'TV sufragerie / P06'),(1410,'TV dormitor / P04'),(2250,'Dulap dormitor / P03'),(2300,'Traseu / doze J - propus')]:
 yy=Z(z);line(90,yy,150,yy,GRAY,.5)
 rect(120,yy-5,10,10,white,TEAL if z==1050 else RED)
 # Close mounting levels use distinct columns to retain their true vertical position.
 x=300 if z in (600,1350,2250) else 150
 line(130,yy,x,yy,MUT,.5);txt(x+5,yy+3,str(z)+' mm / '+label,9,MUT)
para(625,155,520,'<b>Cote locale din model / verificare cu ruleta</b><br/>Dormitor: P01 la ≈2900 mm de peretele cu fereastra, P02 la ≈200 mm, pe peretele stâng. P03 la ≈2000 mm de peretele stâng, pe peretele dulapului, Z2250. Grupul TV este centrat pe pat; porturile se distribuie în interiorul proiecției ecranului.<br/><br/>Sufragerie: P10 grup sub birou la ≈620 mm de peretele cu fereastra, Z600; RJ45 este în carcasa separată imediat alăturată. P09 lateral rămâne la Z850. P08 este pe peretele canapelei, la ≈1300 mm de peretele cu fereastra, Z300.<br/><br/>Baie: P13 centru la ≈1500 mm de peretele stâng, Z1100; verificare zonă în E13. Mașina de rufe: P12 centru la ≈925 mm de peretele stâng al vestibulului, Z650, acces lateral și separat de racordurile de apă.',11)
para(625,510,520,'<b>Regula de montaj</b><br/>Toate înălțimile sunt față de pardoseala finită, nu față de placa brută. Pozițiile din registre se cotează pe axa grupului sau pe portul identificat, după caz. Se marchează pe pereți înaintea tuburilor și se confruntă cu tocurile și mobilierul.<br/><br/>În această secțiune sunt comparate niveluri de pe pereți diferiți; nu se execută toate aparatele pe aceeași verticală. Traseul la Z2300 se adaptează fără reducerea nejustificată a accesului sau perforarea structurii.',11)
end()
c.save()
model={'revision':'R02','date':'2026-10-05','units':'mm','status':'coordonare_ofertare','TE':{'x':TE[0],'y':TE[1],'z':2250,'note':'deasupra usii intrare, confirmat; coordonate aproximative'},'NET':{'x':NET[0],'y':NET[1],'z':2000,'status':'proposed'},'points':points,'junction_boxes':[dict(id=id,x=x,y=y,z=2300,desc=desc,circuit=ci) for id,x,y,desc,ci in BOXES],'circuits':[dict(id=ci,points=ids,desc=desc,section=sec,protection=prot,power_assumed_kw=pow) for ci,ids,desc,sec,prot,pow in circuits],'cable_estimates':route_quantities}
(ROOT/'tmp/electric_plan.json').write_text(json.dumps(model,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'output/pdf/Apartament_184_Registru_electric_R02.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f,delimiter=';');wr.writerow(['ID','Functie','Cantitate','X_mm','Y_mm','Z_mm','Circuit','Statut'])
 for p in points:wr.writerow([p['id'],p['desc'],p['n'],p['x'],p['y'],p['z'],p['circuit'],p['status']])
print(str(OUT));print('Pages:',PAGE,'Schuko:',ns,'LAN_m:',sum(p['route_m'] for p in lan))
