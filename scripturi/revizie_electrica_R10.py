from pathlib import Path
import json,math,csv,copy,collections
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing,Line,String,Circle,Rect
R=Path(__file__).resolve().parents[1];O=R/'output/pdf'
for n,f in [('Segoe','segoeui.ttf'),('SegoeB','segoeuib.ttf')]:pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
old=json.loads((O/'Apartament_184_Tuburi_prinderi_R09.json').read_text(encoding='utf-8'))
base=json.loads((O/'Apartament_184_Trasee_complete_R07.json').read_text(encoding='utf-8'))['routes'];by={r['id']:r for r in base}
ts=copy.deepcopy(old['variants']['C']['tubes']);ts=[t for t in ts if t['destination']!='F08A']
end={r['id']:r['endpoint'] for r in base};end.update(P01=[158,-2700,750],P02=[158,-850,750],S09=[157,-850,900],F08B=[510,-700,478])
def simplify(ps):
 out=[]
 for p in ps:
  if not out or p!=out[-1]:out.append(p)
 change=True
 while change:
  change=False
  for i in range(1,len(out)-1):
   a,b,c=out[i-1:i+2]
   u=[b[k]-a[k] for k in range(3)];v=[c[k]-b[k] for k in range(3)]
   cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
   if sum(q*q for q in cross)<.000001:
    out.pop(i);change=True;break
 return [p for i,p in enumerate(out) if i==0 or p!=out[i-1]]
def replace_end(t):
 ps=t['points']
 for side,node in [('start',t['source']),('end',t['destination'])]:
  if node not in ['P01','P02','F08B']:continue
  p=end[node]
  if side=='start':
   oldp=ps[0];ps=[p,[p[0],p[1],-30],[oldp[0],p[1],-30],[oldp[0],oldp[1],-30]]+ps[1:]
  else:
   oldp=ps[-1];ps=ps[:-1]+[[oldp[0],oldp[1],-30],[oldp[0],p[1],-30],[p[0],p[1],-30],p]
 t['points']=simplify(ps)
for t in ts:
 replace_end(t)
 if t['destination'] in ('P21','P22'):
  target=t['destination'];pts=copy.deepcopy(by[target]['points']);pts=[p if i in (0,len(pts)-1) else [p[0],p[1],-30] for i,p in enumerate(pts)]
  pts.insert(1,[*pts[0][:2],-30]);pts.insert(len(pts)-1,[*pts[-1][:2],-30]);t.update(source='TE',points=simplify(pts),circuit='C13' if target=='P21' else 'C14')
 if t['destination']=='F08B':t['points']=[end['P02'],[158,-700,750],[510,-700,750],end['F08B']];t['source']='P02 / sursa 24 V accesibila'
ts.append(dict(id='TB_S09',destination='S09',source='J03',circuit='C01',kind='S',mounting='SAPA',points=[[3550,-3600,2400],[3550,-3600,-30],[3450,-3600,-30],[3450,-850,-30],[157,-850,-30],end['S09']]))
for t in ts:
 k=t['kind'];target=t['destination']
 n=3;sec=2.5 if k=='P' else 1.5;roles='L, N, PE';diam=25 if k=='P' else 20;status='PRESELECTIE'
 if k=='S':
  n=5 if target in ['S01','S09','S03','S08'] else 4
  roles={'S01':'L, naveta A, naveta B, N rezerva, PE','S09':'naveta A, naveta B, retur L01, N rezerva, PE','S03':'L, retur L03, retur F06, N rezerva, PE','S08':'L, retur L08, comanda F07, N rezerva, PE'}.get(target,'L, retur lumina, N rezerva, PE')
 if target=='F07':n=4;roles='L permanent, N, PE, LT comanda';status='4 fire rezervate; dupa model ventilator'
 if k=='D':n=1;sec=None;roles='1 cablu Cat6, 4 perechi / 8 conductoare';diam=25
 if k=='T':n=1;sec=None;roles='1 cablu coaxial';diam=25
 if k=='H':n=1;sec=None;roles='1 HDMI; gabarit conector de verificat';diam=32;status='diametru nevalidat pentru mufa HDMI'
 if k=='V':n=2;sec=1;roles='+24 V, 0 V; separat de 230 V';diam=20;status='sectiune SELV dupa curent si lungime'
 t.update(wire_count=n,section_mm2=sec,wire_roles=roles,diameter_proposed_mm=diam,status=status)
 t['points']=simplify(t['points']);t['length_m']=round(sum(math.dist(a,b) for a,b in zip(t['points'],t['points'][1:]))/1000,3)
 t['bends']=len(t['points'])-2;t['pull_review']=t['bends']>3 or t['length_m']>15
 assert t['points'][-1]==end.get(target,t['points'][-1]),target
lights=copy.deepcopy(old['existing_lights'])
for l in lights:
 l.update(wire_count=3,section_mm2=1.5,roles='retur comutat, N, PE',length_m=None)
 if l['id']=='L05':l['model_endpoint']=[10199,-1835,2490]
circs=[('C01','Dormitor + sufragerie: plafoniere; LED machiaj',.35),('C02','Hol, bucatarie, debara, balcon + LED',.45),('C03','Baie + vestibul + ventilator',.15),('C04','Prize dormitor, dulap LED, noptiera',1.5),('C05','Prize sufragerie, birou, TV, fier',2.5),('C06','Prize baie',2.0),('C07','Rufe Heinner HWM-HME1014IVA10+++ [M1]',1.65),('C08','Masina vase',2.0),('C09','Cuptor Arctic ARSE11130XD [M2]',2.4),('C10','Masa, hota, aprindere gaz, rezerva bucatarie',.5),('C11','Frigider',.3),('C12','Internet',.15),('C13','Microunde - circuit nou propus',1.5),('C14','Contrablat - circuit nou propus',2.2)]
data={'revision':'R10','date':'2026-10-07','status':'REVIZIE DE COORDONARE; nu este autorizatie de executie','base_links':len(ts),'existing_ceiling_links':len(lights),'floor_height':'DE MASURAT; Z=-30 doar conventie grafica','tubes':ts,'lights':lights,'circuits':circs}
(O/'Apartament_184_Revizie_electrica_R10.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
with (O/'Apartament_184_Tuburi_fire_R10.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Tub','De la','Pana la','Circuit','Diametru exterior PROPUS mm','Numar fire sau cabluri','Sectiune conductor mm2','Roluri','Metri geometrici','Coturi axa','Necesita revizie tragere','Coordonate XYZ mm'])
 for t in ts:w.writerow([t['id'],t['source'],t['destination'],t['circuit'],t['diameter_proposed_mm'],t['wire_count'],t['section_mm2'],t['wire_roles'],t['length_m'],t['bends'],t['pull_review'],json.dumps(t['points'])])
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyR',fontName='Segoe',fontSize=10,leading=14,spaceAfter=7))
styles.add(ParagraphStyle(name='TitleR',fontName='SegoeB',fontSize=22,leading=27,spaceAfter=14,textColor=colors.HexColor('#143e4b')))
styles.add(ParagraphStyle(name='SmallR',fontName='Segoe',fontSize=8,leading=11))
story=[]
def p(s,sty='BodyR'):return Paragraph(s,styles[sty])
def title(s):story.append(p(s,'TitleR'))
def para(s):story.append(p(s))
def table(headers,rows,widths):
 cells=[[p(str(v),'SmallR') for v in row] for row in [headers]+rows];t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e3eef0')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#c6d2d5')),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(t)
def page():story.append(PageBreak())
title('Instalatia electrica / revizie R10')
para('Apartament 184, Bloc L14 | 7 octombrie 2026 | Distributie predominant prin sapa')
para('<b>Ce putem numara acum:</b> 55 legaturi de baza intre punctele proiectului, plus 8 legaturi spre plafoniere existente, nemasurate. Cele 55 NU sunt numarul final de bucati de copex: traseele cu multe curbe necesita reasezare sau doze de tragere accesibile. Nu ingropam doze de conexiuni obisnuite sub sapa.')
counts=collections.Counter(t['kind'] for t in ts)
table(['Categoria','Legaturi','Continut propus'],[['Prize',counts['P'],'23 tuburi: 3 conductoare / tub, Cu 2,5 mm²'],['Alimentari doze J',counts['J'],'6 tuburi: L + N + PE, Cu 1,5 mm²'],['Comenzi',counts['S'],'9 tuburi: 4 sau 5 conductoare, Cu 1,5 mm²'],['LED / ventilator',counts['F'],'7 tuburi: 3 fire; ventilator 4 fire prevazute'],['Date / TV',counts['D']+counts['T'],'4 Cat6 + 3 coaxiale; cate un cablu in tub separat'],['HDMI',counts['H'],'2 tuburi locale; diametrul dupa mufa'],['LED noptiera pastrata',counts['V'],'1 tub local SELV; 2 fire, dupa sursa'],['Plafoniere existente',8,'3 fire / legatura; tuburile si lungimile de verificat']],[150,65,535])
para('<b>Corectii:</b> P01/P02 apropiate de pat; F08A eliminat; F08B mutat cu noptiera; S09 cap-scara adaugat. C13 pentru microunde si C14 pentru contrablat sunt propuneri noi, pentru a reduce incarcarea vechiului C10.')
para('<b>Limita esentiala:</b> puterile marcate [M1] si [M2] sunt verificate in documentatia producatorilor; celelalte sunt ipoteze de sarcina, nu date nominale confirmate. Nu exista masuratori ale coloanei, PE, buclei de defect sau inaltimii sapei.')
page();title('Circuite si calcul preliminar de putere')
table(['Circuit','Utilizare','Putere ipoteza kW','Conductoare plecare'],[[c,n,str(w),'3 x 1,5 mm²' if int(c[1:])<=3 else '3 x 2,5 mm²'] for c,n,w in circs],[55,430,95,170])
total=sum(w for _,_,w in circs)
para(f'<b>Suma ipotezelor de sarcina: {total:.2f} kW</b>, echivalent {total*1000/230:.1f} A la 230 V si cos φ=1 daca functioneaza simultan. Nu se dimensioneaza generalul prin simpla insumare a sigurantelor circuitelor.')
page();title('Putere simultana si limitele calculului')
para('Scenariu solicitant explicit: cuptor 2,4 + rufe 1,65 + vase 2,0 + fierbator 2,2 + consum de fond 0,6 = <b>8,85 kW / 38,5 A</b> la 230 V, cos φ=1. Microundele ar adauga inca 1,5 kW. Scenariul este o estimare de utilizare, nu un coeficient normativ de simultaneitate.')
para('Echivalente monofazate: 25 A = 5,75 kVA; 32 A = 7,36 kVA; 40 A = 9,20 kVA; 50 A = 11,50 kVA. <b>Nu prescriem montarea unui general de 50 A:</b> puterea aprobata, sectiunea coloanei, schema de alimentare si protectia din amonte trebuie verificate. Daca bransamentul este limitat, solutia poate fi gestionarea sarcinilor.')
para('B10 pentru iluminat si B16 pentru prize raman numai preselectii. Definitivarea cere curenti admisibili cu factori de grupare/izolatie, cadere de tensiune, curent de scurtcircuit, timpi de deconectare si coordonare. Protectii diferentiale 30 mA, tip si AFDD/SPD conform situatiei si normativului, de verificat de proiectant autorizat.')
para('Scenariul anterior plus microunde 1,5 kW = 10,35 kW / 45,0 A. Un calcul al cererii nu arata daca exista alimentare mono/trifazata. La 3 faze se verifica fiecare faza si dezechilibrul; nu se divide arbitrar consumul la trei.')
para('<b>Date verificate:</b> [M1] manual Heinner: 1.650 W; [M2] fisa Arctic: 2.400 W. Puterea de iesire de 900 W a microundelor nu este puterea absorbita din priza. Pentru C13 am pastrat ipoteza de 1.500 W pana la verificarea completa a regimului combinat.')
page();title('Cate fire incap in copex?')
para('Propunere: conductoare individuale Cu, tip H07V-U sau echivalent adecvat. Pentru sertizari/conexiuni se respecta tipul conductorului si bornele alese. L, N si PE ale unui circuit sunt pozate impreuna; in aceasta propunere nu amestecam circuite de putere in acelasi tub.')
para('I7, tabelul 5.7, foloseste aria conductorului <b>cu izolatie</b> si aria interioara a tubului: Si ≥ 3 × suma ariilor conductoarelor. Pentru fire identice, criteriul geometric este Di ≥ de × √(3n). Criteriul nu inlocuieste verificarea termica sau conditiile de tragere.')
table(['Legatura','Fire prevazute','Tub propus','Verificare de facut'],[['Priza / aparat','3 x 2,5: L,N,PE','Ø25','Diametrul real al firelor, grupare si curenti'],['Doza iluminat / lampa','3 x 1,5','Ø20','Tabel 5.7 si tuburile existente la lampi'],['Intrerupator simplu','4 x 1,5: L,retur,N rezerva,PE','Ø20','N ramane izolat daca aparatul nu-l foloseste'],['Comanda dubla','5 x 1,5: L,2 retururi,N,PE','Ø20','Borne, doza si curbe'],['Fiecare cap-scara','5 x 1,5','Ø20','Rolurile difera la intrare fata de pat'],['Ventilator cu temporizare','4 x 1,5: L,N,PE,LT','Ø20','PE se termina izolat daca echipamentul clasa II nu are borna']],[140,245,90,275])
para('Exemplu dimensional, nu capacitate universala: la un tub cu interior 14 mm si fire cu diametrul exterior 3,3 mm, 5 fire ocupa circa 27,8% din aria tubului, sub 1/3. FFKuS-EM-F Ø20 are interior nominal 14 mm, iar Ø25 are 19 mm conform producatorului. Produsul cumparat poate avea alte valori.')
para('Pentru Cat6/coax se numara cabluri, nu firele interne ale cablului. HDMI se verifica inclusiv cu mufa si raza de curbura; Ø32 este numai o rezerva grafica, nu o garantie de trecere.')
arch=json.loads((R/'tmp/termic_model.json').read_text(encoding='utf-8'))
furniture=json.loads((R/'tmp/mobilier_plan_R03.json').read_text(encoding='utf-8'))['items']
for kind,titlemap in [('J','Pozitia dozelor si plecarile din tablou'),('P','Prize / trasee de baza prin pardoseala'),('S','Comenzi si alimentari iluminat prin pardoseala'),('D','Date, coaxial si HDMI')]:
 page();title(titlemap)
 dr=Drawing(750,420);scale=.059;labelboxes=[]
 def xy(p):return 35+p[0]*scale,350+p[1]*scale
 for f in furniture:
  for poly in f.get('polys') or [f['poly']]:
   for a,b in zip(poly,poly[1:]+poly[:1]):dr.add(Line(*xy(a),*xy(b),strokeColor=colors.HexColor('#cbd0d2'),strokeWidth=.4,strokeDashArray=[2,2]))
 for e in arch['wall_edges']:
  if len(e)==2:
   q,z=xy(e[0]),xy(e[1]);dr.add(Line(*q,*z,strokeColor=colors.HexColor('#32383b'),strokeWidth=1.2))
 for t in ts:
  if not (t['kind']==kind or kind=='S' and t['kind']=='F' or kind=='D' and t['kind'] in ['T','H']):continue
  col=colors.HexColor('#1579a1') if kind!='D' else colors.HexColor('#7546a0')
  for aa,bb in zip(t['points'],t['points'][1:]):
   q,z=xy(aa),xy(bb);dr.add(Line(*q,*z,strokeColor=col,strokeWidth=.8))
  x,y=xy(t['points'][-1]);dr.add(Circle(x,y,2.5,fillColor=colors.white,strokeColor=col))
  lx=x+6;ly=y+3;wid=pdfmetrics.stringWidth(t['destination'],'SegoeB',8)+4
  while any(not(lx+wid<a or lx>b or ly+9<c or ly>d) for a,b,c,d in labelboxes):ly+=11
  labelboxes.append((lx,lx+wid,ly-2,ly+9))
  if abs(ly-y)>8:dr.add(Line(x,y,lx,ly+3,strokeColor=col,strokeWidth=.35))
  dr.add(Rect(lx-1,ly-1,wid,10,fillColor=colors.white,strokeColor=None))
  dr.add(String(lx,ly,t['destination'],fontName='SegoeB',fontSize=8,fillColor=col))
 for node,co in [('TE',[9956,-4330]),('NET',[7900,-5540])]:
  x,y=xy(co);dr.add(Rect(x-3,y-3,6,6,fillColor=colors.orange));dr.add(String(x+5,y+5,node,fontName='SegoeB',fontSize=8))
 story.append(dr)
 para('Pereti: negru continuu. Mobilier: gri punctat, fundal R03. Trasee: colorat. Plan de coordonare, fara scara de executie. Liniile coincidente reprezinta tuburi distincte; intersectiile nu sunt doze. Cota sub pardoseala este provizorie.')
 if kind=='J':
  page();title('Doze / coordonate de referinta in model')
  table(['Doza','Circuit','X / Y / Z mm','Loc'],[[j,by[j]['circuit'],' / '.join(map(str,end[j])),by[j]['room']] for j in ['J01','J02','J03','J04','J05','J06']],[60,65,250,375])
for j in ['J01','J02','J03','J04','J05','J06']:
 page();title(j+' / '+by[j]['room']+' / '+by[j]['circuit'])
 para('Coordonate centru in model, mm: '+str(end[j])+'. Z fata de pardoseala finita. Doza aparent accesibila la +2400 mm; gabaritul se alege dupa borne, fire si intrari. Accesul fata de mobilier/tavan se confirma.')
 linked=[t for t in ts if t['source']==j or t['destination']==j]
 rows=[[t['id'],t['source']+' → '+t['destination'],t['circuit'],str(t['wire_count'])+' x '+str(t['section_mm2']),t['wire_roles']] for t in linked]
 rows += [['EX_'+l['id'],j+' → '+l['id'],by[j]['circuit'],'3 x 1.5','Retur comutat, N, PE; tub existent de verificat'] for l in lights if l['source']==j]
 table(['Tub','Legatura','Circuit','Fire mm²','Roluri'],rows,[80,120,60,80,410])
 para(f'<b>La aceasta doza:</b> {len(linked)} legaturi noi de baza + {sum(l["source"]==j for l in lights)} legaturi catre plafoniere existente. Fiecare legatura este un tub distinct; intrarile finale cresc daca apar doze suplimentare de tragere.')
 if j=='J03':para('<b>Cap-scara:</b> L din alimentare merge la comunul S01. Navetele A/B ale S01 se continua in J03 spre navetele S09. Comunul S09 revine prin J03 ca faza comutata la L01. N si PE merg direct la L01; N de rezerva la comenzi ramane izolat. F03 are alimentare permanenta separata de returul L01, dar pe acelasi C01.')
 elif j=='J04':para('S07 comanda L07. S08 are doua retururi separate: L08 si comanda ventilatorului F07. Pentru ventilator este prevazuta si faza permanenta; folosirea LT depinde de model. Nu se amesteca nulul C03 cu nulul C06 al prizelor din baie.')
 elif j=='J05':para('S03: faza comuna si doua retururi distincte, unul pentru L03, unul pentru F06. S06: retur separat pentru L06 balcon. N si PE se distribuie la consumatorii aceluiasi C02. Racordul real catre plafoniera balconului trebuie identificat.')
 elif j=='J06':para('S05 comanda impreuna L05 si F05 in aceasta propunere. Daca se doreste control separat al LED-ului, sunt necesare comanda dubla si un retur suplimentar.')
 else:para('Se separa bornele L permanent, N, PE si fiecare retur de comanda. N si PE nu sunt punti intre circuite. Alimentarile LED permanente au comanda locala/senzor, dupa mobilier; faza comutata merge numai la corpul comandat.')
 diagram=Drawing(750,155);cx=365;cy=115
 diagram.add(Line(70,cy,cx,cy,strokeColor=colors.HexColor('#1579a1'),strokeWidth=1.5))
 diagram.add(String(50,cy+12,'TE / '+by[j]['circuit'],fontName='SegoeB',fontSize=10))
 diagram.add(String(135,cy+6,'1 tub / L + N + PE',fontName='Segoe',fontSize=9))
 diagram.add(Rect(cx-22,cy-13,44,26,fillColor=colors.HexColor('#e3eef0'),strokeColor=colors.HexColor('#1579a1')))
 diagram.add(String(cx-12,cy-4,j,fontName='SegoeB',fontSize=11))
 branches=[(t['destination'],str(t['wire_count'])+' fire') for t in linked if t['source']==j]+[(l['id'],'3 fire / existent') for l in lights if l['source']==j]
 for ii,(name,desc) in enumerate(branches):
  x=65+620*(ii+.5)/len(branches)
  diagram.add(Line(cx,cy-14,x,45,strokeColor=colors.HexColor('#1579a1'),strokeWidth=1))
  diagram.add(String(x-15,29,name,fontName='SegoeB',fontSize=10));diagram.add(String(x-35,14,desc,fontName='Segoe',fontSize=8))
 story.append(diagram)
# Terminal nets, each J contains only its assigned lighting circuit.
switch_nets={'S01':['L','A','B','N','PE'],'S09':['A','B','R_L01','N','PE'],'S02':['L','R_L02','N','PE'],'S03':['L','R_L03','R_F06','N','PE'],'S04':['L','R_L04','N','PE'],'S05':['L','R_L05_F05','N','PE'],'S06':['L','R_L06','N','PE'],'S07':['L','R_L07','N','PE'],'S08':['L','R_L08','R_F07','N','PE']}
netrows=[]
for j in ['J01','J02','J03','J04','J05','J06']:
 nets=collections.defaultdict(list)
 for t in ts:
  if t['destination']==j:
   for net in ['L','N','PE']:nets[net].append(t['id']+':'+net)
  if t['source']!=j:continue
  dest=t['destination'];k=t['kind']
  if k=='S':nn=switch_nets[dest]
  elif dest=='F07':nn=['L','N','PE','R_F07']
  else:nn=[{'F05':'R_L05_F05','F06':'R_F06'}.get(dest,'L'),'N','PE']
  for net in nn:nets[net].append(t['id']+':'+net)
 for l in lights:
  if l['source']!=j:continue
  for net in [('R_L05_F05' if l['id']=='L05' else 'R_'+l['id']),'N','PE']:nets[net].append('EX_'+l['id']+':'+net)
 netrows += [[j,by[j]['circuit'],net,len(ends),'; '.join(ends)] for net,ends in nets.items()]
with (O/'Apartament_184_Borne_doze_R10.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Doza','Circuit','Retea electrica','Capete conductoare','Legaturi']);w.writerows(netrows)
for i in range(0,6,2):
 page();title('Legaturi in doze / '+str(i//2+1))
 for j in ['J01','J02','J03','J04','J05','J06'][i:i+2]:
  para('<b>'+j+' - '+by[j]['circuit']+'</b>')
  table(['Borna / retea','Capete','Conductoare conectate intre ele'],[[n,c,e] for jj,ci,n,c,e in netrows if jj==j],[100,60,590])
 para('L = faza permanenta; N = neutru; PE = protectie; R = retur comutat; A/B = navete. Fiecare rand este o retea distincta, nu neaparat o singura piesa de borna. Capacitatea bornelor se alege dupa numarul capetelor, sectiune si tip conductor. PE verde/galben si N albastru nu se folosesc ca faza/navete.')
page();title('Prize / cum pleaca fiecare circuit')
for ci,name,_ in circs:
 if int(ci[1:])<4:continue
 subset=[t for t in ts if t['circuit']==ci and t['kind']=='P']
 para('<b>'+ci+' - '+name+'</b><br/>'+'; '.join(t['source']+' → '+t['destination'] for t in subset))
para('La o priza intermediara: un tub intra si unul iese; in fiecare sunt L, N, PE ale aceluiasi circuit. Asta inseamna 6 capete de conductoare in doza, nu 6 fire intr-un singur tub. Se folosesc borne compatibile si doze suficient de adanci; continuitatea PE se pastreaza. Priza finala are un tub de alimentare.')
para('Punctele Pxx reprezinta grupuri de aparataj; de exemplu P23 are patru Schuko, dar o alimentare C12. Numarul dozelor modulare depinde de rama aleasa, nu coincide cu numarul Pxx.')
page();title('Tablou / repartizare si verificare de lungime')
para('C01 pleaca separat spre J02 si J03; C02 spre J01, J05 si J06; C03 spre J04. Plecarile aceluiasi circuit se reunesc in tablou pe distributie compatibila. Nu se introduc mai multe fire in borna unui aparat decat admite producatorul. Fiecare circuit isi pastreaza propriul N dupa protectia diferentiala.')
vr=[]
for ci,name,power in circs:
 subs=[t for t in ts if t['kind']=='P' and t['circuit']==ci];dist={'TE':0.0}
 for _ in range(len(subs)+1):
  for t in subs:
   if t['source'] in dist:dist[t['destination']]=dist[t['source']]+t['length_m']
 if subs:
  assert all(t['destination'] in dist for t in subs),ci
  far=max((t['destination'] for t in subs),key=lambda n:dist[n]);ll=dist[far];drop=2*.0225*ll*16/2.5
  vr.append([ci,far,f'{ll:.2f}',f'{drop:.2f} V / {100*drop/230:.2f}%'])
table(['Circuit','Punct indepartat','Lungime de la TE, m','Test 16 A la capat, numai ramura'],vr,[75,135,175,365])
para('Test orientativ: ΔU = 2ρLI/S, cu ρ = 0,0225 Ω·mm²/m, Cu 2,5 mm², I = 16 A, 230 V. Presupune intreaga sarcina in priza cea mai indepartata; nu reproduce distributia reala a consumului. Nu include coloana din amonte. Traseele lungi necesita scurtare, impartire sau redimensionare dupa calcul complet; B16 + 2,5 mm² nu este o validare automata.')
points=[t for t in ts if t['kind'] in ['P','S']]
for st in range(0,len(points),16):
 page();title('Pozitii aparataj / '+str(st//16+1))
 table(['Punct','Circuit','X mm','Y mm','Z mm','Tuburi 230 V in doza'],[[t['destination'],t['circuit'],*t['points'][-1],sum(u['kind'] in ['P','S'] and t['destination'] in (u['source'],u['destination']) for u in ts)] for t in points[st:st+16]],[65,70,115,115,115,270])
 para('Coordonate globale ale centrelor din model, nu cote trasate pe santier. Z se masoara de la pardoseala finita. Originea X/Y este cea a modelului CAD; pentru executie se cer cote fata de colturi fixe masurate. P05 langa fereastra alimenteaza zona mesei de machiaj; pozitia si accesul se verifica fata de radiator/draperie. Aparatajul de baie ramane de verificat fata de zonele cazii.')
for start in range(0,len(ts),11):
 page();title('Registru tuburi si fire / '+str(start//11+1))
 table(['Tub','De la → la','Circuit','Ø propus','Fire / continut','m axa','Curbe'],[[t['id'],t['source']+' → '+t['destination'],t['circuit'],t['diameter_proposed_mm'],str(t['wire_count'])+(' x '+str(t['section_mm2'])+' mm²' if t['section_mm2'] else ' cablu')+'<br/>'+t['wire_roles'],t['length_m'],str(t['bends'])+(' *' if t['pull_review'] else '')] for t in ts[start:start+11]],[75,130,50,55,260,70,60])
 para('* Traseu care necesita revizia conditiilor de tragere. Lungimea este geometrica, fara rezerve, fara corectia razelor de curbura si fara ramurile existente din tavan.')
page();title('Cantitati preliminare si puncte de inchis')
tot=collections.defaultdict(float);wire=collections.defaultdict(float)
for t in ts:
 tot[t['diameter_proposed_mm']]+=t['length_m']
 if t['section_mm2']:wire[t['section_mm2']]+=t['wire_count']*t['length_m']
table(['Copex propus','Lungime axa, fara rezerve'],[[str(k)+' mm',f'{v:.2f} m'] for k,v in sorted(tot.items())],[250,500])
table(['Conductoare individuale','Metri-conductor, fara rezerve / plafoniere'],[[str(k)+' mm²',f'{v:.2f} m'] for k,v in sorted(wire.items())],[250,500])
para('Metri-conductor = numarul firelor × lungimea tubului, nu metri de cablu multiconductor. Lungimile ramurilor de lumina existente, rezervele de conexiune, intrarea ISP, alimentarea tabloului si eventualele doze suplimentare NU sunt incluse.')
para(f'<b>{sum(t["pull_review"] for t in ts)} din {len(ts)} legaturi necesita revizia tragerii</b> dupa numarul de coturi/lungime. I7 trateaza distantele intre dozele de tragere si traseele cu curbe; nu pot fi declarate gata de executie axele vechi cu multe schimbari de directie. Dozele suplimentare vor fi accesibile pe pereti, cu separarea circuitelor, dupa alegerea traseelor fizice.')
para('<b>De rezolvat in teren:</b> grosimea reala a pardoselii (devizul vechi de 5 mm autonivelanta nu acopera copexurile); culoare fizice distincte pentru tuburi; traversari si raze; acces la J01-J06; trasee plafoniere si ventilator; puteri de pe etichete; alimentare existenta mono/trifazata, putere aprobata, PE si verificari electrice. Nu se mareste generalul doar pe baza scenariului de putere.')
para('<b>Surse:</b><br/><link href="https://heinner.ro/electrocasnice/wp-content/uploads/sites/5/2025/12/manual_de_utilizare_HWM-HME1014IVA10____68aed84fbbb54.pdf">[M1] Manual Heinner HWM-HME1014IVA10+++</link>, date tehnice, 1.650 W.<br/><link href="https://www.arctic.ro/media/products/fise/ARSE11130XD.pdf">[M2] Fisa Arctic ARSE11130XD</link>, putere cuptor 2.400 W.<br/><link href="https://legislatie.just.ro/Public/DetaliiDocument/286763">I7 pe Portalul Legislativ</link> - 5.2.12.1.5-1.7, tabel 5.7; 5.2.12.3, doze si tragere.<br/><link href="https://www.fraenkische.com/de-DE/product/ffkus-em-f-grau">FRÄNKISCHE FFKuS-EM-F</link> - domeniu de utilizare si diametre interioare. Consultate la 07.10.2026.')
def footer(c,doc):
 c.setFont('Segoe',8);c.setFillColor(colors.HexColor('#587078'));c.drawString(35,20,'R10 | COORDONARE - COTE SI DIMENSIONARI DE VALIDAT | 07.10.2026');c.drawRightString(806,20,str(doc.page))
out=O/'Apartament_184_Revizie_montaj_electric_R10.pdf'
SimpleDocTemplate(str(out),pagesize=(842,595),leftMargin=35,rightMargin=35,topMargin=30,bottomMargin=40).build(story,onFirstPage=footer,onLaterPages=footer)
print(json.dumps({'pdf':str(out),'links':len(ts),'tube_m':dict(tot),'wire_m':dict(wire),'pull_review':sum(t['pull_review'] for t in ts),'power_assumptions_kw':total}))
