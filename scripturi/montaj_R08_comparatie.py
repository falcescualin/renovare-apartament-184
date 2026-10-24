"""Two explicit installation alternatives, architectural linework and route audit."""
from pathlib import Path
import json, math, copy, csv, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripturi'))
from plan_comun import union_len
DATA=json.loads((ROOT/'tmp/termic_model.json').read_text(encoding='utf-8'))
MOB=json.loads((ROOT/'tmp/mobilier_plan.json').read_text(encoding='utf-8'))['items']
BASE=json.loads((ROOT/'output/pdf/Apartament_184_Trasee_complete_R07.json').read_text(encoding='utf-8'))
CEILING=2490; FLOOR=-30
VARIANTS={}
def clean(points):
 out=[]
 for p in points:
  if not out or math.dist(p,out[-1])>.001:out.append(list(p))
 return out
for variant in ('A','B'):
 result=[]
 for orig in BASE['routes']:
  r=copy.deepcopy(orig)
  if r['kind'] in ('H','V'):
   r['mounting']='LOCAL';r['plane']=None
  else:
   plane=FLOOR if variant=='B' and r['kind'] in ('P','D','T') else CEILING
   r['plane']=plane;r['mounting']='SAPA' if plane==FLOOR else 'TAVAN'
   pts=[r['points'][0], [*r['points'][0][:2],plane]]
   junction=next((j['endpoint'] for j in BASE['routes'] if j['id']==r.get('junction')),None)
   for p in orig['points'][1:-1]:
    pts.append([*p[:2],plane])
    if junction and p==junction:pts.extend([junction,[*p[:2],plane]])
   pts.extend([[*r['endpoint'][:2],plane],r['endpoint']])
   r['points']=clean(pts)
  r['length_m']=sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:]))/1000
  r['verified']=r['points'][-1]==r['endpoint']
  for a,b in zip(r['points'],r['points'][1:]):
   if r['kind'] not in ('H','V') and a[:2]!=b[:2]:assert a[2]==b[2]==r['plane'],(variant,r['id'],a,b)
  assert r['verified'];result.append(r)
 VARIANTS[variant]=result
OUTJSON=ROOT/'output/pdf/Apartament_184_Trasee_comparatie_R08.json'
OUTJSON.write_text(json.dumps({'revision':'R08','date':'2026-10-06','units':'mm','ceiling_plane_proposed':CEILING,'floor_plane_proposed':FLOOR,'status':'doua variante de coordonare; cote verticale de confirmat','variants':VARIANTS},ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'output/pdf/Apartament_184_Registru_trasee_R08.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Varianta','ID','Circuit','Camera','Montaj','Plan_Z_mm','Endpoint_X','Endpoint_Y','Endpoint_Z','Lungime_geometrica_m','Traseu_XYZ_mm'])
 for v,rs in VARIANTS.items():
  for r in rs:w.writerow([v,r['id'],r['circuit'],r['room'],r['mounting'],r['plane'],*r['endpoint'],round(r['length_m'],3),json.dumps(r['points'])])

# Reuse typography/table helpers, while replacing the architectural background entirely.
prefix=(ROOT/'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
prefix=prefix.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'","OUT=ROOT/'output/pdf/Apartament_184_Montaj_comparatie_R08.pdf'")
prefix=prefix.replace('R01 | 05.10.2026','R08 | 06.10.2026')
exec(compile(prefix,'drawing_helpers','exec'))
c.setTitle('Apartament 184 | Montaj electric R08 | Tavan vs sapa')
GRAY=HexColor('#a4a9ae');INK=HexColor('#161c23');TAV=HexColor('#c83e35');SAP=HexColor('#286baa');DAT=HexColor('#7544a7')
def architectural(P,k):
 # Architectural context: every non-wall component is dashed, without coloured fills.
 for f in MOB:
  for q in f.get('polys') or [f['poly']]:
   c.setDash([2,2]);poly([P(*p) for p in q],color=GRAY,lw=.45);c.setDash([])
 for e in DATA['wall_edges']:
  if len(e)==2:line(*P(*e[0]),*P(*e[1]),INK,1.65)
 for x0,x1 in [(1680,3280),(3750,5200),(5250,6100),(8230,9630)]:
  for y in (-105,-145):line(*P(x0,y),*P(x1,y),GRAY,.45,[2,2])
 doors=[((3500,-3882.5),(2600,-3882.5),(3500,-2982.5)),((2487.5,-4200),(2487.5,-4900),(3187.5,-4200)),((3625,-4050),(3625,-4950),(4525,-4050)),((7175,-4850),(7175,-3950),(6275,-4850)),((8800,-3507.5),(8000,-3507.5),(8800,-2707.5)),((9837.5,-2200),(9837.5,-1500),(9137.5,-2200))]
 for h,cl,op in doors:
  line(*P(*h),*P(*op),GRAY,.45,[2,2]);aa=math.atan2(cl[1]-h[1],cl[0]-h[0]);bb=math.atan2(op[1]-h[1],op[0]-h[0]);delta=(bb-aa+math.pi)%(2*math.pi)-math.pi;rad=math.dist(h,cl)
  c.setDash([2,2]);poly([P(h[0]+rad*math.cos(aa+delta*i/24),h[1]+rad*math.sin(aa+delta*i/24)) for i in range(25)],color=GRAY,lw=.45,close=False);c.setDash([])
 # Additional enclosed balcony outline, from floor geometry.
 balcony=next(r for r in DATA['rooms'] if r['name']=='Balcon_placa')
 poly([P(*p) for p in balcony['polygon']],color=INK,lw=.9)

def legend(x=855,y=158):
 rows=[('Perete existent',INK,None,1.65),('Mobilier / usi / ferestre',GRAY,[2,2],.5),('230 V / tavan',TAV,None,1.3),('230 V / sapa',SAP,[7,2],1.3),('Date Cat6 / coax',DAT,[5,2,1,2],1.2)]
 for text,col,dash,lw in rows:
  line(x,y,x+35,y,col,lw,dash);txt(x+45,y+3,text,9,INK);y+=21
 para(x,y+14,280,'<b>Simboluri</b><br/>P = priza; D = RJ45; T = coax; L = plafoniera; S = intrerupator; F = alimentare LED/fan; J = doza de derivatie; H = tub HDMI.<br/><br/>Patrat: doza / priza.<br/>Cerc: corp / alimentare.<br/>Triunghi: urcare sau coborare verticala.<br/><br/><b>Cote Z</b><br/>Fata de pardoseala finita, Z=0. Tavan tehnic propus: +2490 mm. Axa tubului in sapa: -30 mm, ipoteza de comparatie; nu reprezinta grosimea sapei disponibile.',10)

def drawroutes(P,rs):
 tubular=json.loads((ROOT/'output/pdf/Apartament_184_Tuburi_prinderi_R08.json').read_text(encoding='utf-8')) if (ROOT/'output/pdf/Apartament_184_Tuburi_prinderi_R08.json').exists() else None
 for r in rs:
  col=DAT if r['kind'] in ('D','T') else SAP if r['mounting']=='SAPA' else TAV
  dash=[5,2,1,2] if r['kind'] in ('D','T') else [7,2] if r['mounting']=='SAPA' else None
  points=r['points']
  if tubular:
   variant='B' if any(rr['mounting']=='SAPA' for rr in rs) else 'A'
   points=next(t['points'] for t in tubular['variants'][variant]['tubes'] if t['destination']==r['id'])
  for a,b in zip(points,points[1:]):
   if a[:2]!=b[:2]:line(*P(*a[:2]),*P(*b[:2]),col,1.1,dash)
  x,y=P(*r['endpoint'][:2])
  if r['kind'] in ('P','D','T','J','S'):rect(x-3,y-3,6,6,white,col,.8)
  else:circle(x,y,3,col,white)
  if r['plane'] is not None and r['endpoint'][2]!=r['plane']:
   poly([(x-4,y+7),(x+4,y+7),(x,y+1)],color=col,lw=.7)

def labels(P,rs,clipbounds):
 used=[];xmin,ymin,xmax,ymax=clipbounds
 for r in sorted(rs,key=lambda r:(r['endpoint'][1],r['endpoint'][0],r['id'])):
  x,y=P(*r['endpoint'][:2]);text=r['id'];tw=pdfmetrics.stringWidth(text,'SegoeB',8)+6
  opts=[(x+9,y-9),(x+9,y+17),(x-tw-9,y-9),(x-tw-9,y+17)]
  opts += [(x+10,y+dy) for dy in (-27,35,-43,51,-59,67)]
  for lx,ly in opts:
   bb=(lx-2,ly-9,lx+tw,ly+3)
   if bb[0]<xmin or bb[2]>xmax or bb[1]<ymin or bb[3]>ymax:continue
   if not any(bb[0]<a[2] and bb[2]>a[0] and bb[1]<a[3] and bb[3]>a[1] for a in used):break
  used.append(bb);line(x,y,lx,ly-3,MUT,.4);rect(bb[0],bb[1],bb[2]-bb[0],12,white,white,.1);txt(lx,ly,text,8,INK,True)

def plan(code,title,variant,rs,region=None,scale=40):
 start(code,title,'Varianta '+variant+' | pereti continui; toate elementele de context in linii punctate','1:'+str(scale)+' la A3, 100%')
 k=72/25.4/scale
 if region is None:ox,oy=45,245
 else:
  xs,ys=region;ox=65-min(xs)*k;oy=165+max(ys)*k
 P=lambda x,y:(ox+x*k,oy-y*k)
 c.saveState();clip=c.beginPath();clip.rect(42,H-730,805,590);c.clipPath(clip,stroke=0)
 architectural(P,k);drawroutes(P,rs);labels(P,rs,(45,143,842,724));c.restoreState()
 legend();para(855,550,278,'<b>Montaj si identificare</b><br/>Legaturile suprapuse in plan sunt in tuburi distincte dupa circuit si tipul cablului. Inaltimile fiecarui capat apar in registru. J01-J06 raman pe perete la +2400 mm, cu acces la capac.<br/><br/>Traseele verticale sunt exclusiv la doze/aparataj. H01/H02 sunt tuburi locale pentru HDMI, independente de reteaua Cat6.<br/><br/>Variante comparative; traseele si cotele verticale se coordoneaza cu sapa, tavanul si structura reale.',10)
 end()

start('00','Montaj electric / doua variante clare','R08 | comparatie trasee pe tavan vs prize si date prin sapa')
panel(42,158,530,'A / Toate traseele pe tavan','Iluminat, prize si date distribuite sus; coborari verticale la aparataj. Cat6 si coaxial in tuburi separate. Fara trasee orizontale intermediare pe pereti.')
panel(620,158,530,'B / Iluminat sus; prize si date prin sapa','Iluminatul si dozele J raman pe tavan / pereti. Prizele P01-P23 si datele D/T pleaca prin sapa, cu urcari verticale. Trasee locale H/V pastrate separat.')
rows=[['Criteriu','A / tavan','B / mixt']]
rows += [['Pereti','Coborari mai lungi la prize joase','Urcari mai scurte la prize joase'],['Pardoseala','Nu necesita tuburi in sapa','Necesita loc pentru tuburi si acoperire, confirmat'],['Tavan','Necesita solutie de fixare si mascare','Necesita solutie de fixare si mascare pentru iluminat'],['Doze de derivatie','Pe perete, capace accesibile','Pe perete; fara imbinari ingropate in sapa'],['Decizie','Dupa verificarea tavanului','Dupa verificarea grosimii sapei']]
table(42,320,[185,460,460],rows,10)
para(42,620,1100,'<b>Ce este exact si ce este propus</b><br/>X/Y si pozitiile aparatelor provin din modelul R07. Pereții au contururile din model, cu golurile existente. R08 descrie doua distributii distincte, nu o varianta aleasa pentru executie. +2490 mm si -30 mm sunt cote de lucru pentru comparatie. Grosimea sapei, stratul de acoperire, tuburile si solutia de tavan se confirma la releveu. Lungimile geometrice nu sunt o comanda finala de cablu.',11)
end()
for v,rs in VARIANTS.items():
 plan(v+'01','Plan general / iluminat si doze',v,[r for r in rs if r['kind'] in ('L','S','F','J')])
 plan(v+'02','Plan general / prize 230 V',v,[r for r in rs if r['kind']=='P'])
 plan(v+'03','Plan general / curenti slabi si HDMI',v,[r for r in rs if r['kind'] in ('D','T','H')])
 for room,name in [('Dormitor','Pardoseala_Dormitor'),('Sufragerie','Pardoseala_CameraDeZi'),('Bucătărie','Pardoseala_Bucatarie'),('Vestibul','Pardoseala_Vestibul')]:
  polyroom=next(r['polygon'] for r in DATA['rooms'] if r['name']==name)
  xs=[p[0] for p in polyroom];ys=[p[1] for p in polyroom]
  selected=[r for r in rs if r['room']==room]
  if room=='Vestibul':selected += [r for r in rs if r['room']=='Baie'];xs=[150,3550];ys=[-5550,-3920]
  plan(v+'D'+str(len(xs))+room[:2],room+' / pozitii si distributie',v,selected,(xs,ys),30 if room=='Sufragerie' else 25)

start('SEC','Sectiuni / tavan, perete si sapa','Schematic; cotele de lucru nu reprezinta un releveu al straturilor')
for v,x in [('A',65),('B',635)]:
 txt(x,165,'Varianta '+v+' / priza joasa',16,INK,True)
 # Diagram exaggerated for legibility; no fake dimension scale.
 rect(x+25,205,410,24,HexColor('#eeeeee'),INK,1.2);txt(x+95,198,'Tavan / intrados de confirmat',10,MUT)
 rect(x+390,229,35,340,HexColor('#eeeeee'),INK,1.2)
 line(x+25,570,x+425,570,INK,1.4);txt(x+25,588,'Pardoseala finita / Z=0',10,INK)
 rect(x+25,594,410,45,None,GRAY,.7);txt(x+25,659,'Sapa si planseu: grosimi de confirmat',10,MUT)
 if v=='A':
  line(x+55,243,x+382,243,TAV,3);line(x+382,243,x+382,520,TAV,3);txt(x+55,268,'Axa tavan propusa +2490 mm',10,TAV)
 else:
  line(x+55,610,x+382,610,SAP,3,[7,2]);line(x+382,610,x+382,520,SAP,3);txt(x+55,693,'Axa tub -30 mm / ipoteza, nu strat masurat',10,SAP)
 rect(x+370,506,20,25,white,INK,1);txt(x+110,521,'Priza: cota din registru',10,INK)
para(65,720,1065,'Dozele J sunt accesibile pe perete. Ramura de la tavan coboara local la centru +2400 mm. Nu exista doze de imbinare propuse in sapa. Tubul HDMI permite inlocuirea cablului; iesirile raman accesibile. Diametrele si separarea fizica se stabilesc dupa cabluri si capacitatea tuburilor.',10)
end()

start('CMP','Comparatie / lungimi geometrice','Reuniune de segmente pe circuit; fara rezerve si fara a presupune schema finala de cablare')
rows=[['Circuit / retea','A: geometrie m','B: geometrie m','Diferenta B - A m']]
for ci in [f'C{i:02}' for i in range(1,13)]+['Cat6','Coax']:
 vals=[]
 for v in ('A','B'):
  rs=[r for r in VARIANTS[v] if (r['kind']=='D' if ci=='Cat6' else r['kind']=='T' if ci=='Coax' else r['circuit']==ci and r['kind']!='V')]
  vals.append(sum(r['length_m'] for r in rs) if ci in ('Cat6','Coax') else union_len([r['points'] for r in rs]))
 rows.append([ci,*[f'{x:.2f}' for x in vals],f'{vals[1]-vals[0]:+.2f}'])
table(42,155,[275,275,275,280],rows,9)
para(42,710,1100,'Acest tabel compara coridoarele geometrice, nu pretul final sau metri de cablu de cumparat. La 230 V schema de legare intre prize, retururile comenzilor si rezervele schimba cantitatea. La date, fiecare legatura este independenta in stea. Bugetul nu se modifica inainte de alegerea variantei.',10);end()

for off in range(0,len(BASE['routes']),18):
 batch=BASE['routes'][off:off+18]
 start('REG'+str(off),'Registru / pozitii exacte si modul de montaj','Coordonate globale CAD, mm; cote Z fata de pardoseala finita')
 rows=[['ID','Destinatie / camera','Circuit','X / Y / Z mm','A','B']]
 for r in batch:
  ar=next(a for a in VARIANTS['A'] if a['id']==r['id']);br=next(a for a in VARIANTS['B'] if a['id']==r['id'])
  rows.append([r['id'],r['desc']+' / '+r['room'],r['circuit'],' / '.join(str(x) for x in r['endpoint']),ar['mounting'],br['mounting']])
 table(42,155,[65,420,95,230,140,155],rows,9);end()
TFILE=ROOT/'output/pdf/Apartament_184_Tuburi_prinderi_R08.json'
if TFILE.exists():
 TD=json.loads(TFILE.read_text(encoding='utf-8'))
 start('TB00','Copexuri / legaturi si prinderi','Identificare fizica a tuburilor; preselectie diametre, pas si cote de confirmat')
 rows=[['Varianta','Legaturi de tub','Lungime geometrica','Repere de prindere propuse']]
 for v,d in TD['variants'].items():rows.append([v,63,str(d['total_tube_m'])+' m',len(d['fixings'])])
 table(42,155,[170,230,325,380],rows,11)
 para(42,320,530,'<b>Cum se numara</b><br/>Un ID TB este o legatura de tub intre doua puncte accesibile. La prizele aceluiasi circuit, tuburile leaga prizele succesiv; nu exista doze de imbinare in sapa. Datele sunt in stea, cate un tub pentru fiecare RJ45/coax. La iluminat, ramurile pleaca din doza J atribuita. Numarul de tuburi pe un segment SG este lista de ID-uri distincte care il traverseaza.',11)
 para(620,320,530,'<b>Fixarea propusa</b><br/>Pas de lucru maximum 500 mm pe fiecare portiune dreapta, reper la 100 mm de fiecare capat de segment. Pe segmente scurte, reper la mijloc. Coordonatele CSV sunt ale axei tubului, nu puncte de gaurire: clema si suportul real determina ancora. Clemele sunt reprezentate schematic in 3D; radiusurile coturilor se definitiveaza dupa tub.',11)
 para(42,540,1105,'<b>Dimensionare</b><br/>Diametrele 20 / 25 / 32 mm sunt gabarite de comparatie, nu selectie finala. Se verifica diametrul interior, cablurile, conductoarele de comanda, raza de curbura si tragerea cablului. Nu se comanda toate tuburile doar pe baza diametrului desenat.<br/><br/><b>Tavan fals?</b><br/>Pentru trasee ascunse sus este necesara o solutie de mascare: tavan fals sau masca tehnica pe traseu. Canalul aparent evita coborarea intregului tavan. Varianta A are pana la 21 de tuburi pe un segment comun; varianta B are pana la 9 sus si 14 jos. Latimea mastii si grosimea straturilor nu pot fi stabilite din axele suprapuse.',11)
 end()
 for v,d in TD['variants'].items():
  for off in range(0,len(d['tubes']),16):
   start(v+'TB'+str(off),'Tuburi '+v+' / de unde pana unde','Metri geometrici fara rezerve; diametre propuse, verificare dupa cabluri si comanda')
   rows=[['Tub','Plecare > destinatie','Circuit','Montaj','Diam. propus','Metri','Prinderi propuse']]
   for t in d['tubes'][off:off+16]:rows.append([t['id'],t['source']+' > '+t['destination'],t['circuit'],t['mounting'],str(t['diameter_proposed_mm'])+' mm',str(t['length_m']),sum(s['tube_id']==t['id'] for s in d['fixings'])])
   table(42,155,[125,235,100,160,145,145,195],rows,9);end()
  for off in range(0,len(d['spans']),10):
   start(v+'SG'+str(off),'Segmente '+v+' / cate copexuri trec','Coordonate A > B in mm; fiecare ID TB reprezinta un tub distinct pe segment')
   rows=[['Segment','A XYZ > B XYZ','Copexuri','Tuburi distincte','Metri']]
   for s in d['spans'][off:off+10]:rows.append([s['id'],' / '.join(map(str,s['a']))+'<br/>'+' / '.join(map(str,s['b'])),s['count'],', '.join(s['tube_ids']),s['length_m']])
   table(42,155,[100,260,85,550,110],rows,9);end()
 start('FX','Prinderi / localizare si registre complete','Repere pe fiecare tub, cu suport TAVAN / SUPORT_PODEA / PERETE_LOCAL')
 para(42,155,1100,'Registrul complet al celor peste 1.300 de repere pe varianta este in <b>Apartament_184_Prinderi_R08.csv</b>. Fiecare reper are ID, tub, X/Y/Z si suport. Reperele sunt marcate in modelul 3D; cotele -30 si +2490 mm sunt ipoteze de comparatie.<br/><br/>Inainte de turnare se verifica suportul si stratificatia, se fixeaza tuburile compatibile cu montajul, se protejeaza iesirile si se documenteaza traseele. Clemele pentru tavan se aleg impreuna cu fixarile adecvate suportului; nu se transfera automat o solutie de fixare intre tavan si pardoseala.<br/><br/>Pentru a obtine cote de montaj definitive sunt necesare: inaltimea libera reala, grosimea si straturile pardoselii noi, solutia de tavan/masca, produsele de tub si clema, schema finala de cablare a comenzilor.',12)
 para(42,465,1100,'<b>Surse tehnice consultate la 06.10.2026</b><br/><link href="https://legislatie.just.ro/Public/DetaliiDocument/286763" color="#277dba">Normativ I7, Portal Legislativ</link> — selectie tuburi dupa modul de montaj si conductoare.<br/><link href="https://www.obo.ro/produse/instala-ie-industriala/produse-speciale/cleme-pentru-cabluri-si-tevi-din-seria-quick/" color="#277dba">OBO — cleme Quick pentru tuburi</link> — exemplu de sistem de fixare, nu produs selectat pentru toate suporturile.<br/><br/>Cote, pas de prindere si diametre in acest dosar: propuneri ale proiectului, nu valori certificate prin sursele de mai sus.',11)
 end()
for v in ('A','B'):
 pic=ROOT/('tmp/varianta_'+v+'_R08_3D.png')
 if pic.exists():
  start(v+'3D','Vedere 3D / varianta '+v,'Pereti taiati pentru vizibilitate; tuburile comune au axe suprapuse, vezi numarul in registrul SG')
  c.drawImage(str(pic),42,H-710,width=1105,height=535,preserveAspectRatio=True,anchor='c',mask='auto')
  para(42,730,1100,'Rosu: distributie pe tavan. Albastru: distributie prin sapa. Mov: date / legaturi locale. Galben: repere de prindere propuse. Cotele verticale si diametrele sunt de confirmat; modelul 3D nu reprezinta tuburi deja montate.',10)
  end()
c.save()
print(json.dumps({'pdf':str(OUT),'pages':PAGE,'variants':2,'routes_each':63,'horizontal_routes_only_on_selected_plane':True},ensure_ascii=False))
