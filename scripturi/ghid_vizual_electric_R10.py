from pathlib import Path
import json, math, csv, collections
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color, white
R=Path(__file__).resolve().parents[1];O=R/'output/pdf'
D=json.loads((O/'Apartament_184_Revizie_electrica_R10.json').read_text(encoding='utf-8'));T=D['tubes']
A=json.loads((R/'tmp/termic_model.json').read_text(encoding='utf-8'))
F=json.loads((R/'tmp/mobilier_plan_R03.json').read_text(encoding='utf-8'))['items']
for n,f in [('S','segoeui.ttf'),('B','segoeuib.ttf')]:pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
W,H=1190,842;C=canvas.Canvas(str(O/'Apartament_184_Ghid_vizual_electric_R10.pdf'),pagesize=(W,H))
C.setTitle('Apartament 184 | Electric R10 | Ghid vizual si pasi de montaj - coordonare')
ink='#173B49';blue='#14749C';orange='#BA541F';green='#197363';purple='#7548A0';muted='#637780';pale='#EEF3F4';red='#AA3F36'
pg=0
def txt(x,y,s,size=11,col=ink,bold=False):
 C.setFont('B' if bold else 'S',size);C.setFillColor(HexColor(col));C.drawString(x,y,str(s))
def wrap(x,y,s,width,size=11,col=ink,leading=None,bold=False):
 leading=leading or size*1.4;line=''
 for word in s.split():
  test=(line+' '+word).strip()
  if pdfmetrics.stringWidth(test,'B' if bold else 'S',size)>width:
   txt(x,y,line,size,col,bold);y-=leading;line=word
  else:line=test
 if line:txt(x,y,line,size,col,bold);y-=leading
 return y
def box(x,y,w,h,fill=pale,stroke=None):
 C.setFillColor(HexColor(fill));C.setStrokeColor(HexColor(stroke or fill));C.roundRect(x,y,w,h,8,fill=1,stroke=bool(stroke))
def line(x1,y1,x2,y2,col=blue,width=1.5,dash=None):
 C.setStrokeColor(HexColor(col));C.setLineWidth(width);C.setDash(dash or []);C.line(x1,y1,x2,y2);C.setDash([])
def arrow(x1,y1,x2,y2,col=blue):
 line(x1,y1,x2,y2,col,2);a=math.atan2(y2-y1,x2-x1)
 for d in [-.45,.45]:line(x2,y2,x2-8*math.cos(a+d),y2-8*math.sin(a+d),col,2)
def start(title,sub):
 global pg
 if pg:C.showPage()
 pg+=1;box(0,0,W,H,'#FAFBF9');txt(36,798,'APARTAMENT 184 / ELECTRIC R10',10,muted,True);txt(36,760,title,25,ink,True);txt(36,731,sub,11,muted)
 line(36,711,1154,711,'#D2DDE0',1)
 txt(36,21,'07.10.2026 | REVIZIE DE COORDONARE - TRASEE SI COTE DE VALIDAT INAINTE DE EXECUTIE',9,muted)
 txt(1100,21,f'{pg:02d}',10,muted,True)
def step(x,y,n,title,desc,w=310,h=106):
 box(x,y-h,w,h);box(x+12,y-38,27,27,blue);txt(x+19,y-30,n,12,'#FFFFFF',True)
 txt(x+50,y-28,title,12,ink,True);wrap(x+14,y-55,desc,w-28,10.5)
def note(s,y=64,col=orange):
 box(36,y-12,1118,40,'#FFF0E4');wrap(49,y+12,s,1090,10,col)
def plan(ts,x=48,y=170,w=720,h=520):
 scale=min(w/11400,h/7200);ox=x;oy=y+5600*scale
 def xy(p):return ox+p[0]*scale,oy+p[1]*scale
 for f in F:
  for poly in f.get('polys') or [f['poly']]:
   for a,b in zip(poly,poly[1:]+poly[:1]):line(*xy(a),*xy(b),'#C8CECE',.6,[2,3])
 for e in A['wall_edges']:
  if len(e)==2:line(*xy(e[0]),*xy(e[1]),'#47575E',1.4)
 for label,p in [('DORMITOR',[1400,-1600]),('SUFRAGERIE',[4600,-2000]),('BUCATARIE',[7950,-1800]),('BAIE',[700,-4850]),('VESTIBUL',[2650,-4950]),('HOL',[8250,-4700]),('DEBARA',[10000,-2300]),('BALCON',[4850,750])]:
  xx,yy=xy(p);txt(xx,yy,label,8,'#839297')
 used=set();labels=[]
 for t in ts:
  col=purple if t['kind'] in ['D','T','H','V'] else blue
  for a,b in zip(t['points'],t['points'][1:]):line(*xy(a),*xy(b),col,1.9)
  for node,p in [(t['source'],t['points'][0]),(t['destination'],t['points'][-1])]:
   if node in used:continue
   used.add(node);xx,yy=xy(p);C.setFillColor(HexColor(col));C.circle(xx,yy,3,stroke=0,fill=1)
   lx=xx+6;ly=yy+5;name=node if len(node)<10 else 'sursa';ww=pdfmetrics.stringWidth(name,'B',9)+3
   while any(not(lx+ww<a or lx>b or ly+10<c or ly>d) for a,b,c,d in labels):ly+=12
   labels.append((lx,lx+ww,ly-2,ly+10))
   if abs(ly-yy)>10:line(xx,yy,lx,ly,col,.5)
   C.setFillColor(HexColor('#FAFBF9'));C.rect(lx-1,ly-1,ww,11,stroke=0,fill=1);txt(lx,ly,name,9,col,True)
 return xy
def conductor(x,y,n,sec):
 C.setStrokeColor(HexColor(ink));C.setLineWidth(2);C.circle(x,y,33,stroke=1,fill=0)
 cols=[orange,blue,green,'#34373B',purple]
 for i in range(n):
  a=2*math.pi*i/n;xx=x+17*math.cos(a);yy=y+17*math.sin(a);C.setFillColor(HexColor(cols[i%len(cols)]));C.circle(xx,yy,6,stroke=0,fill=1)
 txt(x+48,y+7,f'{n} conductoare',13,ink,True);txt(x+48,y-14,str(sec)+' mm² fiecare',11,muted)

start('Cum folosim acest dosar','Schemele arata legaturile propuse. Registrul tehnic pastreaza toate coordonatele si listele de conductoare.')
stages=[('01','Verificam baza','Cota pardoselii, tabloul existent, traseele plafonierelor si puterile aparatelor.'),('02','Marcam punctele','TE, NET, J01-J06, P01-P23, S01-S09. Fiecare cod apare si in model.'),('03','Asezam tuburile','Un circuit de putere per tub; datele separat. Intai rezolvam curbele si culoarele.'),('04','Tragem si identificam','Firele sunt etichetate la ambele capete, dupa tub si circuit. Conexiuni accesibile.'),('05','Legam si verificam','Electricianul face conexiunile si masuratorile. Acoperirea traseelor urmeaza verificarii.')]
for i,(n,title,desc) in enumerate(stages):
 x=36+i*225;step(x,675,n,title,desc,215,175)
 if i<4:arrow(x+217,587,x+225,587)
for i,(big,title,desc) in enumerate([('55','legaturi noi de baza','Numar de legaturi, nu lungime de rola si nu total final dupa dozele de tragere.'),('6','doze de derivatie','J01-J06 pe pereti. Prizele au propriile doze de aparataj.'),('8','legaturi de plafon','Pozitii existente pastrate; tuburi, conductoare si lungimi de verificat.'),('14','circuite propuse','Inclusiv doua circuite noi separate: microunde si prize contrablat.')]):
 x=36+i*281;box(x,276,267,175);txt(x+18,395,big,36,blue,True);txt(x+18,365,title,14,ink,True);wrap(x+18,338,desc,232,11)
wrap(48,216,'Ce nu confundam: numarul de fire din tub, numarul tuburilor care intra intr-o doza si numarul modulelor de priza sunt trei lucruri diferite.',1050,17,ink,24,True)
note('44 legaturi au axe cu prea multe schimbari de directie pentru a fi declarate gata de montaj. R10 este un dosar de coordonare, nu aviz de executie.')

start('Pasul 1 / alimentare si tablou','Putere calculata pentru consumatori; capacitatea bransamentului existent se confirma separat.')
box(40,550,235,125,ink);txt(58,638,'ALIMENTARE EXISTENTA',13,'#FFFFFF',True);wrap(58,612,'Mono / trifazat, putere aprobata, protectie din amonte si PE: de verificat.',195,11,'#FFFFFF')
arrow(275,610,350,610);box(350,550,210,125);txt(370,632,'TE / TABLOU',18,ink,True);wrap(370,602,'Protectie generala si distributie, alese dupa verificarea coloanei.',170,11)
box(635,550,515,125,'#E4F0E9');txt(654,638,'8,85 kW / circa 38,5 A',24,green,True);wrap(654,605,'Cuptor 2,40 + rufe 1,65 + vase 2,00 + fierbator 2,20 + fond 0,60. La 230 V si cos φ = 1.',470,12)
for i,(ci,label,power) in enumerate(D['circuits']):
 row=i//7;col=i%7;x=40+col*159;y=316-row*164
 box(x,y,149,144);txt(x+12,y+116,ci,17,blue,True);wrap(x+12,y+89,label,125,10,leading=13);txt(x+12,y+17,f'{power:.2f} kW',11,ink,True)
note('Suma sarcinilor de calcul: 17,65 kW. Numai rufele si cuptorul au aici puteri verificate in fisele producatorilor. Nu rezulta automat un general de 40 A sau 50 A.')

start('Pasul 2 / cum urca traseul din pardoseala','Sectiune de principiu, fara scara. Nu se taie placa structurala pentru a face loc tuburilor.')
box(80,160,610,92,'#D7DFE1');txt(96,192,'PLACA DE BETON EXISTENTA',14,ink,True)
box(80,252,610,110,'#EEE0C9');txt(96,326,'STRAT DE POZARE / SAPA - DE DIMENSIONAT',12,orange,True)
box(80,362,610,17,'#AC906A');txt(96,391,'PARDOSEALA FINITA = Z 0',12,ink,True)
box(620,252,70,355,'#D7DFE1');txt(535,631,'PERETE',12,ink,True)
line(135,289,651,289,blue,6);line(651,289,651,509,blue,6);box(632,503,38,48,'#FFFFFF',blue)
txt(240,270,'Copex continuu pana la doza',13,blue,True);arrow(510,539,627,528);txt(270,544,'Doza de aparataj accesibila',13,ink,True)
for i in range(3):C.setFillColor(HexColor([orange,blue,green][i]));C.circle(165+i*43,290,10,fill=1,stroke=0)
wrap(96,451,'Cota Z = -30 mm din model este doar o conventie grafica. Nu stabileste grosimea sapei si nu descrie nivelul real al placii.',450,13)
step(806,675,'1','Masoara pragul','Stabileste diferenta placa - pardoseala finita, inclusiv finisaj si adeziv.',340)
step(806,554,'2','Alege sistemul de pardoseala','Acoperirea deasupra tuburilor rezulta din solutia si fisa sapei, nu doar din diametrul copexului.',340)
step(806,433,'3','Rezolva intersectiile','Tuburile desenate pe aceeasi axa se aseaza fizic alaturat. Se verifica separat latimea si grosimea.',340)
step(806,312,'4','Pastreaza accesul','Nu ascunde conexiuni in sapa. Dozele de derivatie/tragere trebuie sa ramana accesibile.',340)
note('Nu este prevazut tavan fals. Legaturile existente spre plafoniere se verifica si se reutilizeaza numai daca sunt corespunzatoare.')

start('Pasul 3 / gasim dozele J01-J06','Alimentarile pleaca din TE de deasupra intrarii. Pe plan, o intersectie de linii nu inseamna conexiune.')
plan([t for t in T if t['kind']=='J'])
for i,j in enumerate(['J01','J02','J03','J04','J05','J06']):
 t=next(t for t in T if t['destination']==j);x,y,z=t['points'][-1]
 box(806,610-i*76,340,67);txt(820,652-i*76,f'{j} / {t["circuit"]} / 1 tub de alimentare',12,ink,True);txt(820,630-i*76,f'X {x}   Y {y}   Z +{z} mm',10,muted)
note('Toate J sunt propuse la +2400 mm. Accesul fata de mobilier si tavan se verifica. X/Y sunt coordonate CAD, nu cote fata de colturi masurate.')

for j in ['J01','J02','J03','J04','J05','J06']:
 feed=next(t for t in T if t['destination']==j);outs=[t for t in T if t['source']==j];lights=[l for l in D['lights'] if l['source']==j]
 start(f'Pasul 4 / {j} - intrari si iesiri',f'Circuit {feed["circuit"]} | {1+len(outs)} legaturi noi de baza + {len(lights)} spre plafoniere existente')
 box(45,485,150,105,ink);txt(65,550,'TE',24,'#FFFFFF',True);txt(65,520,feed['circuit'],15,'#FFFFFF');arrow(195,538,300,538)
 txt(204,566,'1 tub',13,blue,True);txt(204,548,'3 x 1,5',10,blue)
 box(300,455,190,165,'#DCEBEF',blue);txt(355,561,j,34,blue,True);txt(326,526,'L / N / PE',17,ink,True);txt(322,493,'borne accesibile',12,muted)
 branches=[(t['destination'],t['wire_count'],t['wire_roles'],False) for t in outs]+[(l['id'],3,'retur comutat, N, PE',True) for l in lights]
 for i,(dest,n,roles,ex) in enumerate(branches):
  yy=657-i*88;arrow(490,538,584,yy-23,green if ex else blue);box(584,yy-62,548,73,'#E5EFE8' if ex else pale)
  txt(598,yy-12,dest,18,green if ex else blue,True);txt(672,yy-10,('EXISTENT / ' if ex else '1 COPEX / ')+str(n)+' FIRE',12,ink,True);wrap(672,yy-30,roles,437,10)
 conductor(128,356,3,1.5)
 steps=[('1','Identifica alimentarea',feed['id']+' vine din TE. Eticheta circuitului ramane pe ambele capete.'),('2','Separa bornele','L permanent, N, PE si fiecare retur au conexiuni distincte. Nu uni retururile intre ele.'),('3','Verifica iesirile','Numara tuburile de pe schema; pentru legaturile intre borne foloseste schema de cap-scara si registrul bornelor.')]
 for i,(n,title,desc) in enumerate(steps):step(45+i*371,233,n,title,desc,353,125)
 note('Pozitionarea fizica a traseelor si accesul dozei se valideaza inainte de tragere. Firele nefolosite se termina izolat; PE nu devine conductor de comanda.')

start('Cap-scara dormitor / ce leaga cele doua comenzi','S01 la intrare + S09 langa pat. Ambele comenzi apartin aceluiasi circuit C01.')
for x,label in [(60,'S01 / INTRARE'),(870,'S09 / PAT')]:box(x,393,250,190);txt(x+18,551,label,17,ink,True)
box(410,337,350,295,'#E5EFF2');txt(438,603,'J03 / legaturi accesibile',19,ink,True)
rows=[('L permanent','L -> comun S01',orange,False),('Naveta A','S01 A -> S09 A','#33383E',True),('Naveta B','S01 B -> S09 B',purple,True),('Retur L01','Comun S09 -> plafoniera',orange,True)]
for i,(a,b,col,full) in enumerate(rows):
 yy=546-i*54;line(294 if i!=3 else 584,yy,886 if i!=0 else 560,yy,col,2.5);txt(432,yy+8,a,11,col,True)
txt(75,509,'COMUN: L',13,orange,True);txt(75,459,'A / B: navete',13,ink,True);txt(884,507,'A / B: navete',13,ink,True);txt(884,411,'COMUN: retur L01',12,orange,True)
box(443,228,288,74);txt(462,274,'L01 / plafoniera',16,ink,True);txt(462,249,'retur comutat + N + PE',12,ink)
arrow(584,384,584,303,orange)
conductor(128,286,5,1.5);conductor(909,286,5,1.5)
txt(71,226,'TB_S01 / 1 tub Ø20 propus',12,blue,True);txt(851,226,'TB_S09 / 1 tub Ø20 propus',12,blue,True)
step(43,187,'1','Intrare','L, A, B, N rezerva, PE.',353,91);step(414,187,'2','Langa pat','A, B, retur L01, N rezerva, PE.',353,91);step(785,187,'3','Plafoniera','N si PE ajung direct, fara a fi comutate.',353,91)
note('Schema functionala. Culorile desenului identifica retele; marcarea fizica a firelor respecta codurile N/PE si schema electricianului. Sursa LED F03 ramane separata de returul L01.')

groups=[(['C04'],'Dormitor / prize si dulap'),(['C05'],'Sufragerie / TV, birou, canapea'),(['C06','C07'],'Baie si masina de spalat'),(['C08','C09'],'Bucatarie / vase si cuptor'),(['C10','C11'],'Bucatarie / consumatori generali si frigider'),(['C13','C14'],'Bucatarie / microunde si contrablat'),(['C12'],'Internet / alimentare 230 V')]
for cis,title in groups:
 ts=[t for t in T if t['kind']=='P' and t['circuit'] in cis]
 start('Pasul 5 / '+title,' / '.join(cis)+' | 3 conductoare Cu 2,5 mm² in fiecare tub de prize; Ø25 propus, de verificat la dimensionare.')
 plan(ts)
 txt(808,677,'ORDINEA LEGATURILOR',13,ink,True)
 for i,t in enumerate(ts):
  yy=639-i*76;box(804,yy-52,345,65);txt(818,yy-7,t['source']+'  ->  '+t['destination'],14,blue,True)
  txt(818,yy-28,t['circuit']+' / '+t['id']+' / 1 copex / 3 fire',10,ink)
 conductor(105,120,3,2.5)
 wrap(350,132,'Doza intermediara: 1 tub intra + 1 tub iese = 6 capete de fire. Priza finala: 1 tub = 3 capete. Grupul de prize poate avea mai multe module Schuko.',790,12)
 note('Axele sunt mostenite si corectate punctual, nu culoare fizice finalizate. Verifica dozele de tragere, razele si caderile de tensiune din anexa. Baia necesita verificarea zonelor de protectie.')

start('Pasul 6 / curenti slabi si HDMI','Retea in stea din NET. Cat6, coaxial, HDMI si 24 V sunt separate de traseele de 230 V.')
plan([t for t in T if t['kind'] in ['D','T','H']])
for i,(big,title,desc) in enumerate([('4','Tuburi Cat6','Cate 1 cablu de 4 perechi. Cele 8 fire interne nu inseamna 8 cabluri.'),('3','Tuburi coaxiale','NET -> T01, T02, T03. Distributia/splitterul depinde de semnalul operatorului.'),('2','Tuburi locale HDMI','Legatura mobila -> televizor. Ø32 este doar propus; trecerea mufei trebuie probata.')]):
 yy=660-i*154;box(802,yy-127,344,136);txt(818,yy-36,big,30,purple,True);txt(866,yy-28,title,15,ink,True);wrap(819,yy-64,desc,309,11)
note('Cablul operatorului pana la NET nu este cuantificat: punctul de intrare si tehnologia trebuie confirmate. Tuburile de rezerva suplimentare nu sunt incluse in cele 55 legaturi.')

start('Pasul 7 / inainte de acoperirea traseelor','Ordine de lucru pentru coordonarea echipelor; conexiunile si verificarile electrice sunt facute de electrician.')
check=[('1','Plan marcat in apartament','Se marcheaza fiecare punct si se compara cu usile, mobilierul, cada, radiatorul si draperiile.'),('2','Trasee fizice rezolvate','Se elimina ocolurile, se aleg dozele accesibile de tragere si se verifica trecerile. Cele 44 semnalate in registru cer revizie.'),('3','Tuburi asezate si fixate','Sistem de fixare compatibil cu placa si sapa, conform producatorului. Nu prescriem gauri in placa fara verificarea structurii si instalatiilor existente.'),('4','Tragere si identificare','Se verifica trecerea pe fiecare tub; se eticheteaza tubul, circuitul si conductoarele la ambele capete.'),('5','Masuratori si documentare','Continuitate PE, izolatie si celelalte verificari prescrise pentru instalatie. Se fotografiaza traseele cu cote si se actualizeaza planul.'),('6','Acoperire dupa verificare','Se inchid doar traseele acceptate. Schema finala a tabloului si rezultatele probelor raman in dosarul apartamentului.')]
for i,(n,t,d) in enumerate(check):step(40+(i%3)*374,680-(i//3)*260,n,t,d,354,223)
note('Pasi de coordonare, nu instructiuni de lucru sub tensiune. Inaintea executiei raman necesare validarea dimensionarii si verificarile instalatiei existente.')

start('Citire rapida / fisiere si valori de referinta','Ghid vizual + anexa tehnica + model editabil. Toate au acelasi indicativ R10.')
for i,(title,desc) in enumerate([('GHIDUL VIZUAL','Acest document: ordine de lucru, planuri filtrate pe circuite si scheme de doze.'),('ANEXA TEHNICA','Revizie_montaj_electric_R10.pdf: coordonate, registrul celor 55 de legaturi, fire, borne si calcule.'),('MODELUL FREECAD','montaj_electric_R10_revizie.FCStd: selecteaza un circuit, apoi tubul. Proprietatile arata sursa, destinatia si continutul.'),('REGISTRE CSV','Tuburi_fire_R10.csv si Borne_doze_R10.csv: liste editabile, cate o legatura sau retea de borne pe rand.')]):
 box(42,563-i*117,1107,99);txt(62,627-i*117,title,17,blue,True);wrap(62,599-i*117,desc,1050,12)
wrap(50,152,'Surse pentru puteri: manualul Heinner HWM-HME1014IVA10+++ (1.650 W) si fisa Arctic ARSE11130XD (2.400 W). Celelalte sarcini sunt ipoteze. Normativ I7 si fisa tubului FRÄNKISCHE: linkuri in anexa.',1070,11)
note('R10 nu inlocuieste releveul si proiectul verificat. Registrele cuantifica axele de coordonare, nu cantitati finale de comanda.')
C.save();print('Visual pages:',pg)
