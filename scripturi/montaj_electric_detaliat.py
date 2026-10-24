from pathlib import Path
import json, math, csv
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
src=src.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'","OUT=ROOT/'output/pdf/Apartament_184_Montaj_electric_R03.pdf'").replace('R01 |','R03 |').replace("(-1,-1),9)","(-1,-1),6)")
src=src.replace("fill=HexColor('#ffe9df'),stroke=RED,lw=1.3","fill=HexColor('#eef0f1'),stroke=GRAY,lw=.5")
exec(src)
c.setTitle('Apartament 184 - Montaj electric detaliat R03')
E=json.loads((ROOT/'tmp/electric_plan.json').read_text(encoding='utf-8'));PS={p['id']:p for p in E['points']};ZTOP=2400
PURPLE=HexColor('#7954a2')
N={'A':(9956,-4330),'B':(9000,-4330),'C':(7500,-4330),'D':(6800,-4330),'E':(4800,-4330),'F':(4000,-4330),'G':(3050,-4330),'H':(3050,-3700),'I':(2500,-3700),'J':(3450,-3700),'K':(150,-3700),'M':(8500,-4330),'N':(8500,-3400),'O':(7350,-3400),'Q':(9600,-3400),'R':(9600,-1900),'U':(9900,-1900),'V':(10400,-1900),'NET':(7900,-5540)}
edges=[('A','B'),('B','M'),('M','C'),('C','D'),('D','E'),('E','F'),('F','G'),('G','H'),('H','I'),('I','K'),('H','J'),('M','N'),('N','O'),('N','Q'),('Q','R'),('R','U'),('U','V'),('M','NET')]
# Every trunk is orthogonal except NET feed; split it into two perpendicular segments.
N['W']=(7900,-4330);edges[-1:]=[('M','W'),('W','NET')];edges[2]=('W','C')
groups=[]
def g(code,ids,room,anchor,mode,wall,datum):
 p=[PS[i] for i in ids.split(',')];axisx=p[0]['x'];axisy=p[0]['y']
 if wall=='X':axisx=round(sum(v['x'] for v in p)/len(p));axisy=round(sum(v['y'] for v in p)/len(p))
 elif wall=='Y':axisx=round(sum(v['x'] for v in p)/len(p));axisy=round(sum(v['y'] for v in p)/len(p))
 groups.append(dict(id=code,points=ids.split(','),room=room,anchor=anchor,x=axisx,y=axisy,zmin=min(v['z'] for v in p),mode=mode,wall=wall,datum=datum))
g('B01','P01','Dormitor','K','verticală la priză','X',-250)
g('B02','P02','Dormitor','K','verticală la priză','X',-250)
g('B03','P03','Dormitor','I','în spatele dulapului, acces sus','Y',150)
g('B04','P04,D03,T03,F03','Dormitor','J','canal tehnic în spatele panoului TV','X',-250)
g('B05','P05','Dormitor','J','verticală în zona machiaj','Y',150)
g('B06','P06,P07,D01,D02,T01,T02,F02','Sufragerie','F','canal tehnic în spatele panoului TV','X',-250)
g('B07','P08','Sufragerie','D','verticală la canapea','X',-250)
g('B08','P09,P10,D04','Sufragerie','F','canal comun sub/lateral birou','X',-250)
g('B09','P11,F01','Sufragerie','E','în spatele dressingului, service interior','Y',3700)
g('B10','P12','Vestibul','G','compartiment tehnic lateral spălătorie','Y',2525)
g('B11','P13','Baie','G','verticală la prize, în afara zonei căzii','Y',150)
g('B12','P14','Bucătărie','Q','corp lateral accesibil frigiderului','X',-250)
g('B13','P15','Bucătărie','Q','verticală la masă','X',-250)
g('B14','P16,F06','Bucătărie','O','în spatele mobilierului superior','X',-250)
g('B15','P17,P18,P19,P22','Bucătărie','O','spate mobilier; corp uscat accesibil','X',-250)
g('B16','P20,P21','Bucătărie','O','corp vecin cuptorului, acces service','X',-250)
g('B17','P23,F04','Hol','W','dulap tehnic ventilat NET, separatoare','Y',7250)
g('B18','F05','Debara','V','sursă LED deasupra rafturilor','Y',9875)
g('B19','F07','Baie','G','racord ventilator; clasă/IP de confirmat','Y',150)
anchors=['I','D','N','B','U','D','F','G'];rooms=['Dormitor','Sufragerie','Bucătărie','Hol','Debara','Sufragerie','Sufragerie','Vestibul']
for i in range(1,9):
 s=PS['S%02d'%i];g('B%02d'%(19+i),s['id'],rooms[i-1],anchors[i-1],'verticală la întrerupător','Y' if i in (1,3,6) else 'X',150 if i==1 else 0)
adj={k:[] for k in N}
for a,b in edges:adj[a].append(b);adj[b].append(a)
def path(a,b):
 todo=[(a,[a])];seen=set()
 while todo:
  x,pp=todo.pop(0)
  if x==b:return pp
  if x in seen:continue
  seen.add(x)
  todo.extend((y,pp+[y]) for y in adj[x] if y not in seen)
 raise ValueError((a,b))
def ortho(a,b):return [a,(b[0],a[1]),b] if a[0]!=b[0] and a[1]!=b[1] else [a,b]
TR=[]
for i,(a,b) in enumerate(edges,1):
 route=ortho(N[a],N[b]);TR.append(dict(id='TR%02d'%i,a=a,b=b,route=route,length=round(sum(math.dist(x,y) for x,y in zip(route,route[1:]))/1000,3),circuits=set(),points=[]))
JANCHOR={'J01':'B','J02':'D','J03':'J','J04':'G','J05':'N','J06':'U'}
for box in E['junction_boxes']:
 pp=path('A',JANCHOR[box['id']])
 for a,b in zip(pp,pp[1:]):
  tr=next(t for t in TR if {t['a'],t['b']}=={a,b});tr['circuits'].add(box['circuit']);tr['points'].append(box['id'])
for gr in groups:
 gr['branch']=ortho(N[gr['anchor']],(gr['x'],gr['y']))
 gr['length_plan']=round(sum(math.dist(a,b) for a,b in zip(gr['branch'],gr['branch'][1:]))/1000,3)
 gr['vertical']=round(abs(ZTOP-gr['zmin'])/1000,3)
 gr['circuits']=sorted({PS[p]['circuit'] for p in gr['points']})
 for pid in gr['points']:
  p=PS[pid];pp=path('NET' if p['kind'] in ('D','T') else 'A',gr['anchor'])
  for a,b in zip(pp,pp[1:]):
   tr=next(t for t in TR if {t['a'],t['b']}=={a,b});tr['circuits'].add(p['circuit']);tr['points'].append(pid)
  p['montaj_group']=gr['id'];p['trunks']=[next(t['id'] for t in TR if {t['a'],t['b']}=={a,b}) for a,b in zip(pp,pp[1:])]
  p['local_h']=abs(p['y']-gr['datum']) if gr['wall']=='X' else abs(p['x']-gr['datum'])
J={b['id']:b for b in E['junction_boxes']}
for b in J.values():b['z']=ZTOP
light_anchor={'L01':'J03','L02':'J02','L03':'J05','L04':'J01','L05':'J06','L06':'J05','L07':'J04','L08':'J04'}
def drawroute(P,route,color=RED,width=1.1):
 for a,b in zip(route,route[1:]):line(*P(*a),*P(*b),color,width,[4,2])
def marker(P,p,label=True):
 x,y=P(p['x'],p['y']);col=BLUE if p['kind'] in ('D','T') else TEAL if p['kind'] in ('S','L') else RED
 circle(x,y,3,col,white)
 if label:txt(x+5,y-4,p['id'],8,col,True)
def base():return view(70,255,50)
def roomview(room):
 mapping={'Dormitor':'Dormitor','Sufragerie':'CameraDeZi','Vestibul':'Vestibul','Baie':'Baie','Bucătărie':'Bucatarie','Hol':'Hol','Debara':'Nisa'}
 rr=next(r for r in DATA['rooms'] if r['name']=='Pardoseala_'+mapping[room]);xs=[p[0] for p in rr['polygon']];ys=[p[1] for p in rr['polygon']]
 sc=30 if room=='Sufragerie' else 15 if room in ('Baie','Vestibul','Hol') else 20
 kk=72/25.4/sc
 return view(70-min(xs)*kk,185+max(ys)*kk,sc,clip=(42,150,680,595)),sc
def new(code,title,sub,scale='Fără scară'):start(code,title,sub,scale)
def page_table(code,title,widths,rows,sub='Cote în mm; lungimi în m; trasee propuse de verificat pe teren',size=9):
 new(code,title,sub);table(42,155,widths,rows,size);end()
new('M00','Montaj electric / trasee și cote','R03 | detaliere a soluției R02, cu trasee grupate și HDMI înlocuibil')
panel(42,155,525,'BAZA DE TRASARE','Cote exacte ale propunerii CAD. Origine O: colț exterior stânga-sus, X spre dreapta, Y negativ spre jos. Z=0 este pardoseala finită. Tablou deasupra ușii: loc confirmat, axă aproximativă. Toate axele noi sunt propuse; releveul și verificarea pereților preced execuția.')
panel(620,155,525,'REDUCEREA ȘANȚURILOR','Coridoare comune pentru tuburi distincte, distribuție sus și trasee în spatele mobilierului. Noua axă superioară Z2400 înlocuiește Z2300 din R02 pentru această variantă; se verifică înălțimea măștii și corpurile înalte. Masca se dimensionează după tuburi și razele lor, nu automat la 100 mm.')
table(42,385,[95,510,501],[['Planșe','Conținut','Folosire'],['M01-M03','Coridoare, noduri și coborâri grupate','Alegerea traseului comun și identificare'],['M04-M25','Fișe pe încăperi și elevații de perete','Poziții, cote locale, puncte și circuite'],['MD01-MD06','TV/HDMI, doze, comenzi, plafoniere','Montaj detaliat și acces pentru înlocuire'],['MQ01-MQ03','Lista traseelor, puncte de control, surse','Măsurare și ofertare'] ],11)
para(42,640,1106,'R03 este un dosar de montaj pentru coordonare. Dimensionarea circuitelor/protecțiilor din R02 rămâne preliminară; nu se consideră validată prin aceste cote. La bucătărie, lungimea cablurilor aparatelor, accesul lateral și traseele de gaz/apă pot impune ajustarea prizelor. Nu se taie structura pentru a păstra o cotă propusă.',12)
end()
new('M01','Traseu principal / noduri de distribuție','Coridoare superioare comune; fiecare circuit în tubul său','1:50 la imprimare A3, 100%')
P,k=base()
for t in TR:
 drawroute(P,t['route'],RED,1.4);a,b=t['route'][0],t['route'][-1];x,y=P((a[0]+b[0])/2,(a[1]+b[1])/2);txt(x+2,y-7,t['id'],8,RED,True)
for name,xy in N.items():
 x,y=P(*xy);circle(x,y,2,TEAL,TEAL);txt(x+4,y+10,name,8,TEAL,True)
para(750,170,395,'<b>A = TE</b>, deasupra intrării. <b>NET</b> = compartiment rețea propus în hol. Nodurile reprezintă schimbări de direcție/ramificații ale traseului, nu obligatoriu doze electrice.<br/><br/>TR01-TR19: coridoare de montaj. T01-T03 identifică porturile coaxiale TV, ca în R02.<br/><br/>Distribuția de sus se montează la Z2400 ca axă propusă. În zonele mobilierului înalt se ocolește prin compartimente tehnice accesibile, fără a strivi tuburile. Traversările dintre camere se coordonează cu golurile ușilor și structura.<br/><br/>Un coridor poate conține mai multe tuburi, cu identificare proprie. Datele și HDMI rămân separate de 230V. Registrul CSV indică succesiunea coridoarelor pentru fiecare punct; pentru comenzile Sxx aceasta reprezintă accesul circuitului până la zonă, iar conexiunea electrică se face prin doza J a circuitului, conform MD03-MD06.',11)
end()
for n,chunk in enumerate([TR[:10],TR[10:]],2):
 page_table('M%02d'%n,'Registru coridoare / coordonate și utilizare',[65,60,175,175,70,300,261],[['ID','Noduri','Pornire X / Y','Sosire X / Y','L [m]','Circuite / rețele','Montaj']]+[[t['id'],t['a']+'-'+t['b'],' / '.join(map(str,t['route'][0])),' / '.join(map(str,t['route'][-1])),t['length'],', '.join(sorted(t['circuits'])) or 'Rezervă / iluminat local','Tuburi separate, axă Z2400; acces la ramificații'] for t in chunk])
page_no=4
room_order=['Dormitor','Sufragerie','Vestibul','Baie','Bucătărie','Hol','Debara']
for room in room_order:
 gg=[q for q in groups if q['room']==room]
 sc=30 if room=='Sufragerie' else 15 if room in ('Baie','Vestibul','Hol') else 20
 new('M%02d'%page_no,room+' / trasee locale și coborâri','Linie punctată = coridor superior; cerc = axă comună a coborârii','1:'+str(sc)+' la imprimare A3, 100%');page_no+=1
 (P,k),sc=roomview(room)
 c.saveState();cp=c.beginPath();cp.rect(42,H-150-595,680,595);c.clipPath(cp,stroke=0)
 for t in TR:drawroute(P,t['route'],RED,.65)
 for gr in gg:
  drawroute(P,gr['branch'],BLUE,1.3);x,y=P(gr['x'],gr['y']);circle(x,y,4,BLUE,white);txt(x+6,y-5,gr['id'],9,BLUE,True)
 c.restoreState()
 para(745,155,400,'<b>'+room+'</b><br/>Fiecare Bxx grupează un traseu fizic. Punctele alimentate pot avea circuite diferite în tuburi distincte; conductoarele nu se reunesc electric. Racordurile scurte din mobilier sunt accesibile și înlocuibile.<br/><br/>Cotele axei Bxx reprezintă propunerea unui canal comun; aparatajul se montează la cotele proprii din registrul următor. Abaterile dintre canal și porturi se rezolvă în spatele panoului sau în corpul tehnic, fără diagonale tăiate în perete.',11)
 table(745,405,[60,190,150],[['Axă','Puncte','Z minim']]+[[q['id'],', '.join(q['points']),q['zmin']] for q in gg],9)
 end()
 # Split registers to ensure full readable detail.
 selected=[(gr,PS[pid]) for gr in gg for pid in gr['points']]
 for index in range(0,len(selected),14):
  page_table('M%02d'%page_no,room+' / fișă de trasare '+str(index//14+1),[55,55,250,120,120,70,125,80,231],[['Punct','Axă','Funcțiune','X','Y','Z','Cotă locală','Circuit','Reper cotă locală']]+[[p['id'],gr['id'],p['desc'],p['x'],p['y'],p['z'],p['local_h'] if not p['id'].startswith('S') else 'după X/Y',p['circuit'],('de la peretele cu geam Y=-250' if gr['wall']=='X' and gr['datum']==-250 else 'de la X='+str(gr['datum']) if gr['wall']=='Y' else 'axa CAD; verificare toc')] for gr,p in selected[index:index+14]],'Z = centru aparat; pozițiile CAD sunt propuneri, nu măsurători ale instalației existente');page_no+=1
 # Wall elevations for each physical plane, schematic horizontal positions but heights to scale.
 new('M%02d'%page_no,room+' / elevație de montaj','Înălțimi la scară 1:15; pozițiile orizontale sunt desfășurate comparativ','Vertical 1:15; orizontal schematic');page_no+=1
 sy=72/25.4/15;yfloor=685;top=yfloor-2500*sy
 line(55,yfloor,1135,yfloor,INK,1.3);line(55,top,1135,top,GRAY,1)
 line(55,yfloor-ZTOP*sy,1135,yfloor-ZTOP*sy,BLUE,.8,[4,2]);txt(65,top-14,'TAVAN 2500 / AXĂ TRASEU 2400 mm',10,MUT,True)
 for i,gr in enumerate(gg):
  xx=90+i*(1000/max(1,len(gg)-1));txt(xx-15,top-35,gr['id'],11,TEAL,True);line(xx,yfloor-ZTOP*sy,xx,yfloor-gr['zmin']*sy,BLUE,1.5,[4,2])
  byheight={}
  for pid in gr['points']:byheight.setdefault(PS[pid]['z'],[]).append(pid)
  lasty=-1000
  for j,(zz,ids) in enumerate(sorted(byheight.items(),reverse=True)):
   yy=yfloor-zz*sy;circle(xx,yy,3,RED,white);ly=max(yy,lasty+12);lasty=ly
   # Labels alternate sides for dense groups.
   dx=-95 if i==len(gg)-1 else 7
   if ly!=yy:line(xx,yy,xx+dx,ly,GRAY,.5)
   txt(xx+dx,ly-3,','.join(ids)+' / '+str(zz),8,RED)
 para(55,725,1080,'Bxx = traseu comun; fiecare circuit în tub separat. Înălțimea canalului ascuns în mobilier se adaptează pentru acces și razele cablurilor. Porțiunile deasupra axei 2400 (de exemplu sursa dressingului) sunt urcări locale. Etichetele indică ID și Z în mm.',10);end()
new('MD01','HDMI / două trasee locale înlocuibile','Sufragerie și dormitor; tub separat de alimentarea 230V, ascuns în panoul TV')
for x,title,upper,lower,axis in [(42,'H01 / SUFRAGERIE',1350,350,'X3700 / Y≈-2650'),(610,'H02 / DORMITOR',1410,400,'X3550 / Y≈-1707')]:
 rect(x+20,160,480,150,LIGHT,GRAY);txt(x+40,186,title,14,TEAL,True);rect(x+80,220,310,48,white,BLUE);txt(x+95,248,'Ieșire cu perie în spatele TV / Z'+str(upper),11)
 rect(x+80,500,310,48,white,BLUE);txt(x+95,528,'Ieșire în comodă / Z'+str(lower),11)
 line(x+235,268,x+235,500,BLUE,4);txt(x+255,375,'TUB HDMI',11,BLUE,True);txt(x+255,395,'Ø32-40 orientativ',10,MUT);txt(x+255,415,'mufa trebuie să treacă',10,MUT)
 para(x+25,585,490,'<b>'+axis+'</b><br/>Axă propusă, ajustată în interiorul panoului după suportul TV. Cablu direct, fără cuplă ascunsă. Capete accesibile și rezervă pentru scoaterea ecranului. Raza curbelor după cablul ales; probă de tragere cu mufa reală înainte de închidere.',11)
para(42,715,1106,'Alegeți cablu potrivit instalării fixe și performanțelor aparatelor; pentru 4K/120Hz, Ultra High Speed certificat. Test video/audio și eARC înainte de închiderea măștii. Nu se înglobează cablul direct în tencuială. H02 este o rezervă propusă până la alegerea aparatelor din dormitor.',10);end()
new('MD02','Doze și secțiune / acces și separare','Secțiune convențională; dimensiunile carcasei după tuburi, umplere și raza de îndoire')
for x,t,col in [(70,'230V / tub Cxx',RED),(400,'DATE / Cat6 + coax',BLUE),(730,'HDMI / tub dedicat',PURPLE)]:
 rect(x,200,285,160,LIGHT,GRAY);txt(x+18,230,t,13,col,True)
 for dx in [60,125,190]:circle(x+dx,285,18,col,white)
 txt(x+18,338,'Acces prin capac demontabil',10,MUT)
table(42,400,[160,370,576],[['Element','Montaj propus','Control înainte de închidere'],['Doze P / S','Adânci, după aparataj și număr conductoare','Spațiu borne; ramă compatibilă; N rezervat unde necesar; PE continuu'],['Doze J01-J06','Z2400; accesibile; circuite identificate','J02 numai C01; alte circuite trec în tub separat, fără îmbinare aici'],['Module TV / birou','Carcase separate sau separatoare certificate','Nicio trecere necompartimentată între borne 230V și date'],['Sursă LED','Compartiment tehnic uscat, ventilat','Acces la driver, distanțe față de textile, cablu 24V dimensionat'],['Coborâre în perete','Verticală; lățime după tuburi și suport','În beton: soluție verificată sau mască aparentă; nu se presupune șanț permis'] ],11)
para(42,715,1106,'F08 / noptiere: două alimentări LED locale din P01 și P02, prin surse adecvate accesibile; nu se creează o coborâre suplimentară la mijlocul patului. Benzile, driverul și secțiunea cablului 24V se aleg după lungime și putere.',10)
end()
new('MD03','Comenzi / legături funcționale','Circuite și funcții; conexiunile finale după aparataj și manualele receptorilor')
table(42,155,[80,155,200,270,401],[['Comandă','Circuit','Receptori','Conexiune funcțională','Control'],['S01','C01 + AFDD','L01','L → întrerupător → retur L01','N și PE direct la corp; nu se întrerupe PE'],['S02','C01 + AFDD','L02','L → întrerupător → retur L02','F02 este C02 și are comandă locală separată'],['S03 dublu','C02','L03 + F06','L comun; două retururi distincte','N și PE până la lampă/driver, după clasă'],['S04','C02','L04','Comandă simplă','N/PE rezervate corespunzător în doză'],['S05','C02','L05; LED rafturi','L05 de la tastă; F05 cu senzor local','Alimentarea senzorului după model'],['S06','C02','L06','Comandă din sufragerie','Etanșare la trecerea spre balcon'],['S07','C03','L07','Comandă din sufragerie spre vestibul','Poziție păstrată la intrarea în vestibul'],['S08 dublu','C03','L08 + F07','Lumină și ventilator separat','Pentru temporizare: L permanent, LT, N; PE după clasa aparatului'] ],10)
para(42,635,1106,'Conductorul verde-galben se folosește exclusiv pentru protecție; neutrul se identifică albastru. Numărul firelor de comandă se stabilește după funcțiile de mai sus, fără reutilizarea PE ca retur. Nu se unesc neutralii circuitelor din avalul RCBO-urilor. Dozele surselor LED alimentate din circuite diferite se identifică distinct.',11)
end()
page_table('MD04','Plafoniere / puncte și ramuri finale',[70,180,180,85,110,481],[['Punct','X / Y','Origine ramură','Z corp','Circuit','Traseu final / comandă']]+[[pid,str(PS[pid]['x'])+' / '+str(PS[pid]['y']),jid,PS[pid]['z'],PS[pid]['circuit'],'Din '+jid+' în tub propriu, pe tavan/mască; cotă și structură verificate. Comandă S'+pid[1:]] for pid,jid in light_anchor.items()],'Corpul la intrados ≈2500; traseu propus Z2400 și urcare locală la corp')
new('MD05','Iluminat / ramuri pe tavan și doze','Trasee ortogonale propuse; racorduri la corpurile LED','1:50 la imprimare A3, 100%')
P,k=base()
for pid,jid in light_anchor.items():
 b=J[jid];p=PS[pid];drawroute(P,ortho((b['x'],b['y']),(p['x'],p['y'])),TEAL,1);marker(P,p)
for jid,b in J.items():
 x,y=P(b['x'],b['y']);rect(x-3,y-3,6,6,ORANGE,ORANGE);txt(x+5,y+11,jid,8,ORANGE,True)
para(750,170,395,'Ramurile J → L sunt pe plafon/în masca propusă, la Z2400, cu urcare locală la Z corp. Cablul final include N, PE și faza comandată. La aparatele clasa II PE se termină izolat, nu se folosește ca retur.<br/><br/>Pentru balcon, J05 → L06 este un traseu propus pe tavan, cu traversare verificată spre sufragerie și apoi balcon; lungimea și găurile se stabilesc după structura reală. Dacă traversarea nu este permisă, ramura se conduce pe coridoarele prin hol/sufragerie.<br/><br/>Planul de cablare se finalizează după alegerea măștilor și verificarea pereților; poziția plafonierelor este preluată din CAD.',11);end()
page_table('MD06','Doze J / alimentare și comenzi',[70,90,150,75,90,195,436],[['Doză','Nod','X / Y','Z','Circuit','Comenzi','Funcție']]+[[jid,JANCHOR[jid],str(b['x'])+' / '+str(b['y']),2400,b['circuit'],{'J01':'S04','J02':'S02','J03':'S01','J04':'S07,S08','J05':'S03,S06','J06':'S05'}[jid],'Alimentare din nodul indicat, apoi ramuri către comenzi și lămpi; separare de alte circuite.'] for jid,b in J.items()],'Doze accesibile; traseele de comandă au coborâre la S și retur separat identificat')
for i in range(0,len(groups),14):
 page_table('MQ'+str(i//14+1).zfill(2),'Cantități / coridoare de coborâre',[55,120,150,50,70,75,130,456],[['Axă','X / Y','Puncte','Nod','L sus m','L vert. m','Circuite','Tip de montaj']]+[[gr['id'],str(gr['x'])+' / '+str(gr['y']),','.join(gr['points']),gr['anchor'],gr['length_plan'],gr['vertical'],','.join(gr['circuits']),gr['mode']] for gr in groups[i:i+14]],'L sus = ramură de la nod la axa B; L vert. = până la cel mai jos punct; nu metri de șanț obligatoriu')
new('MQ03','Ordinea montajului / validarea pe teren','Cotele din model devin cote de execuție după releveu și aprobarea soluției constructive')
table(42,155,[70,340,696],[['Etapă','Operație','Rezultat cerut'],['1','Releveu și identificare','TE, branșament/PE, structură pereți, trasee existente, gaz/apă, înălțimi finite'],['2','Trasare la scară reală','Marcaje P/S/J, Bxx, panouri TV, mobilier și tocuri; cote verificate din aceeași origine'],['3','Probă de traseu','Simulare cu tuburi reale în mască; raze, grad umplere, capac service și extracție cabluri'],['4','Montaj tuburi / doze','Fixări adecvate suportului; segregare 230V/date; identificare la ambele capete'],['5','Cablare / test intermediar','Continuitate, izolație, PE; test LAN și HDMI înainte de finisaj; fotografii cu ruleta'],['6','Închidere / echipare','Capace și acces păstrate; fără surse LED sau borne zidite; prize accesibile lângă aparate'],['7','Recepție','Teste instalație și diferențiale, identificare circuite, raport și plan conform executat'] ],11)
para(42,615,525,'<b>Economia reală se măsoară pe șantier</b><br/>Coridoarele comune și panourile TV reduc traseele separate. Lungimile listate sunt de traseu, nu cantități de șanț: tuburile paralele, ramurile suprapuse și segmentele în mobilier se separă la deviz. Nu se atribuie procent de economie fără soluția de perete și oferta executantului.',11)
para(620,615,525,'<b>Referințe</b><br/><link href="https://legislatie.just.ro/public/DetaliiDocument/271142" color="#277dba">I7 / modificări Ordin 959/2023</link><br/><link href="https://www.legrand.ro/sites/g/files/ocwmcr861/files/2024-06/brosura_sisteme_perimetrale_legrand_-_dlp_si_dlp-s_ud2022next.pdf" color="#277dba">Legrand / sisteme compartimentate</link><br/><link href="https://www.hdmi.org/resource/cables" color="#277dba">HDMI / categorii și certificare</link><br/>R02 păstrează calculul preliminar al circuitelor și lista aparatajului; R03 înlocuiește geometria traseelor propuse.',11)
end();c.save()
for t in TR:t['circuits']=sorted(t['circuits']);t['points']=sorted(set(t['points']))
out={'revision':'R03','z_traseu':ZTOP,'nodes':N,'trunks':TR,'drops':groups,'points':list(PS.values()),'junctions':list(J.values())}
(ROOT/'output/pdf/Apartament_184_Montaj_electric_R03.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'output/pdf/Apartament_184_Trasare_R03.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Punct','Functie','X_mm','Y_mm','Z_mm','Circuit','Coborare','Coridoare'])
 for p in PS.values():w.writerow([p['id'],p['desc'],p['x'],p['y'],p['z'],p['circuit'],p.get('montaj_group','local/tavan'),','.join(p.get('trunks',[]))])
print('PDF',OUT,'pages',PAGE,'trunks',len(TR),'drops',len(groups))
