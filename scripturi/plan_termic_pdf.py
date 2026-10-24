from pathlib import Path
import json, math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color, white
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'tmp/termic_model.json').read_text(encoding='utf-8'))
OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'
W,H=1190.551,841.890
for name,file in [('Segoe','segoeui.ttf'),('SegoeB','segoeuib.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
INK=HexColor('#172b3a');MUT=HexColor('#536473');BLUE=HexColor('#277dba');RED=HexColor('#c64937');TEAL=HexColor('#147b73');LIGHT=HexColor('#edf3f5');ORANGE=HexColor('#a96516');GRAY=HexColor('#d5dde1')
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Apartament 184 - Plan termic, sectiuni si cantitati - R01');c.setAuthor('Documentatie de coordonare dupa modelul FreeCAD')
PAGE=0
style=ParagraphStyle('p',fontName='Segoe',fontSize=11,leading=15,textColor=INK,spaceAfter=0)
styles={sz:ParagraphStyle('p'+str(sz),parent=style,fontSize=sz,leading=sz*1.35) for sz in (9,10,11,12,14,18)}
def txt(x,y,text,size=11,color=INK,bold=False):
 c.setFillColor(color);c.setFont('SegoeB' if bold else 'Segoe',size);c.drawString(x,H-y,text)
def para(x,y,width,text,size=11):
 p=Paragraph(text,styles[size]);_,h=p.wrap(width,1000);p.drawOn(c,x,H-y-h);return h

def line(x1,y1,x2,y2,color=INK,lw=1,dash=None):
 c.setStrokeColor(color);c.setLineWidth(lw);c.setDash(dash or []);c.line(x1,H-y1,x2,H-y2);c.setDash([])
def rect(x,y,w,h,fill=None,stroke=INK,lw=1):
 c.setLineWidth(lw);c.setStrokeColor(stroke)
 if fill:c.setFillColor(fill)
 c.rect(x,H-y-h,w,h,stroke=1,fill=bool(fill))
def poly(pts,fill=None,color=INK,lw=1,close=True):
 path=c.beginPath();path.moveTo(pts[0][0],H-pts[0][1])
 for x,y in pts[1:]:path.lineTo(x,H-y)
 if close:path.close()
 c.setLineWidth(lw);c.setStrokeColor(color)
 if fill:c.setFillColor(fill)
 c.drawPath(path,stroke=1,fill=bool(fill))
def circle(x,y,r,color=INK,fill=None):
 c.setStrokeColor(color)
 if fill:c.setFillColor(fill)
 c.circle(x,H-y,r,stroke=1,fill=bool(fill))
def tag(x,y,s,color=TEAL):
 width=pdfmetrics.stringWidth(s,'SegoeB',9)+14;rect(x,y-13,width,19,fill=color,stroke=color);txt(x+7,y,s,9,white,True)
def start(code,title,subtitle,scale='Fără scară'):
 global PAGE
 PAGE+=1;c.setFillColor(TEAL);c.rect(0,H-9,W,9,fill=1,stroke=0)
 txt(42,44,'APARTAMENT 184 / BLOC L14 / BUCUREȘTI',10,MUT,True)
 txt(42,83,title,25,INK,True);txt(42,107,subtitle,11,MUT)
 line(42,124,W-42,124,GRAY)
 line(42,H-57,W-42,H-57,GRAY)
 txt(42,H-35,'R01 | 05.10.2026 | COORDONARE ȘI OFERTARE - NU PLAN DE EXECUȚIE VALIDAT',9,MUT)
 txt(790,H-35,scale,9,MUT);txt(1050,H-35,code+'  /  '+str(PAGE).zfill(2),10,TEAL,True)
 c.bookmarkPage(code);c.addOutlineEntry(code+' - '+title,code)
def end():c.showPage()
def panel(x,y,w,title,body,color=TEAL):
 rect(x,y,w,32,fill=color,stroke=color);txt(x+12,y+22,title,12,white,True)
 h=para(x+12,y+45,w-24,body,11);return y+45+h

def table(x,y,widths,rows,size=10):
 ps=styles[size]
 cells=[[Paragraph(str(cell),ps) for cell in row] for row in rows]
 t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('FONTNAME',(0,0),(-1,0),'SegoeB'),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),.35,GRAY),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f7f9fa')])]))
 _,h=t.wrapOn(c,sum(widths),1200)
 if y+h>H-75:raise ValueError('Table overflow on page '+str(PAGE)+': '+str(y+h))
 t.drawOn(c,x,H-y-h);return y+h

def dim(x1,y1,x2,y2,label,offset=20):
 if abs(y2-y1)<.01:
  yy=y1+offset;line(x1,y1,x1,yy+4,MUT,.4);line(x2,y2,x2,yy+4,MUT,.4);line(x1,yy,x2,yy,MUT,.5)
  for xx in (x1,x2):line(xx-3,yy-3,xx+3,yy+3,MUT,.7)
  c.setFillColor(white);tw=pdfmetrics.stringWidth(label,'Segoe',9);c.rect((x1+x2-tw)/2-3,H-yy-4,tw+6,13,fill=1,stroke=0);txt((x1+x2-tw)/2,yy+3,label,9,MUT)
 else:
  xx=x1+offset;line(x1,y1,xx+4,y1,MUT,.4);line(x2,y2,xx+4,y2,MUT,.4);line(xx,y1,xx,y2,MUT,.5)
  for yy in (y1,y2):line(xx-3,yy-3,xx+3,yy+3,MUT,.7)
  c.saveState();c.translate(xx-4,H-(y1+y2)/2);c.rotate(90);c.setFillColor(MUT);c.setFont('Segoe',9);c.drawCentredString(0,0,label);c.restoreState()

def leader(points,label,color=INK):
 for aa,bb in zip(points,points[1:]):line(*aa,*bb,color,.8)
 circle(*points[0],2,color,color);txt(points[-1][0]+5,points[-1][1]-3,label,10,color,True)

def view(ox,oy,scale=50,clip=None):
 k=72/25.4/scale
 def P(x,y):return ox+x*k,oy-y*k
 if clip:c.saveState();path=c.beginPath();path.rect(clip[0],H-clip[1]-clip[3],clip[2],clip[3]);c.clipPath(path,stroke=0)
 for r in DATA['rooms']:
  poly([P(*p) for p in r['polygon']],fill=HexColor('#fafbfb'),color=GRAY,lw=.35)
 for f in DATA['furniture']:
  b=f['bbox'];p=P(b[0],b[4]);rect(*p,(b[3]-b[0])*k,(b[4]-b[1])*k,fill=HexColor('#eef0f1'),stroke=GRAY,lw=.5)
 for e in DATA['wall_edges']:
  if len(e)==2:line(*P(*e[0]),*P(*e[1]),INK,.8)
 # Window symbols from source CAD.
 for x0,x1,door in [(1680,3280,False),(3750,5200,False),(5250,6100,True),(8230,9630,False)]:
  for yy in (-105,-145):line(*P(x0,yy),*P(x1,yy),BLUE,.7)
 # Current door opening geometry (schematic plan only).
 doors=[((3500,-3882.5),(2600,-3882.5),(3500,-2982.5)),((2487.5,-4200),(2487.5,-4900),(3187.5,-4200)),((3625,-4050),(3625,-4950),(4525,-4050)),((7175,-4850),(7175,-3950),(6275,-4850)),((8800,-3507.5),(8000,-3507.5),(8800,-2707.5)),((9837.5,-2200),(9837.5,-1500),(9137.5,-2200))]
 for h,cl,op in doors:
  line(*P(*h),*P(*op),MUT,.45);aa=math.atan2(cl[1]-h[1],cl[0]-h[0]);bb=math.atan2(op[1]-h[1],op[0]-h[0]);delta=(bb-aa+math.pi)%(2*math.pi)-math.pi;r=math.dist(h,cl)
  pts=[P(h[0]+r*math.cos(aa+delta*i/18),h[1]+r*math.sin(aa+delta*i/18)) for i in range(19)];poly(pts,color=GRAY,lw=.35,close=False)
 for rr in DATA['radiators']:
  b=rr['bbox'];p=P(b[0],b[4]);rect(*p,(b[3]-b[0])*k,(b[4]-b[1])*k,fill=HexColor('#ffe9df'),stroke=RED,lw=1.3)
 if clip:c.restoreState()
 return P,k

def route(P):
 # Indicative envelope only; not site-measured routing or hydraulics.
 for col,off in [(RED,0),(BLUE,35)]:
  for pts in [[(3755+off,-320),(3755+off,-470-off),(3050,-470-off),(3050,-370)],[(3755+off,-320),(3755+off,-470-off),(3835,-470-off),(3835,-370)]]:
   for aa,bb in zip(pts,pts[1:]):line(*P(*aa),*P(*bb),col,1.3,[4,2])
 for xx,col in [(3755,RED),(3790,BLUE)]:circle(*P(xx,-320),3,col,white)

# T00
start('T00','Instalația termică','Dosar de coordonare: amplasare, secțiuni, racorduri și cantități')
for x,title,value,sub in [(42,'R1 / DORMITOR','≈ 1.100 W','Radiator nou, sub geam'),(410,'R2 / SUFRAGERIE','≈ 1.600 W','Radiator nou, poziție păstrată'),(778,'R3 / BAIE','≈ 450 W','Portprosop, opus lavoarului')]:
 rect(x,150,350,125,fill=LIGHT,stroke=GRAY);txt(x+16,177,title,11,TEAL,True);txt(x+16,218,value,28,INK,True);txt(x+16,249,sub,11,MUT)
para(42,300,525,'<b>Date confirmate</b><br/>Termoficare; etajul 1; bloc izolat exterior; ferestre termopan; locuință încălzită dedesubt; înălțime liberă 2,50 m. Coloana comună sufragerie-dormitor se află în colțul dinspre ferestre și traversează peretele spre dormitor. Bucătăria rămâne fără radiator.',12)
para(620,300,525,'<b>Ce este încă provizoriu</b><br/>Dimensiunile radiatoarelor sunt cele de reprezentare din CAD. Puterea reală, temperaturile tur/retur, presiunea, materialul și diametrul conductelor, tipul mono/bifilar și racordul băii nu sunt măsurate. Cotele coloanei și ale traversării sunt indicative.',12)
rows=[['Planșă','Conținut','Utilizare'],['T01','Plan termic al apartamentului, 1:50','Poziții și identificare'],['T02','Coloană + ramuri R1/R2, detaliu 1:25','Coordonare cu peretele și ferestrele'],['T03','Elevații dormitor și sufragerie, 1:20','Cote radiatoare/parapet'],['T04','Baie și secțiuni de montaj','Portprosop, textile, trecere perete'],['T05','Necesar termic și temperaturi de lucru','Estimare; selecția în wați'],['T06','Scheme de principiu și racordare','Identificarea instalației existente'],['T07','Lista de cantități pentru încălzire','Cerere de ofertă'],['T08','Măsurători, recepție și surse','Închiderea punctelor deschise']]
table(42,465,[85,575,446],rows,10)
end()
# T01
start('T01','Plan termic / poziții păstrate','Cote în mm; originea O = colțul exterior din stânga-sus al planului CAD','1:50 la imprimare A3, 100%')
P,k=view(70,285,50)
route(P)
for text,x,y in [('DORMITOR',1850,-2350),('SUFRAGERIE',5400,-3200),('BUCĂTĂRIE',8600,-2000),('BAIE',1350,-4800),('VESTIBUL',3035,-4650),('HOL',8550,-4380),('DEBARA',10300,-1750),('BALCON ÎNCHIS',5400,650)]:
 px,py=P(x,y);txt(px-30,py,text,9,MUT,True)
for label,x,y in [('R1',2480,-680),('R2',4475,-680),('R3',1250,-4300)]:tag(*P(x,y),label,RED)
leader([P(3770,-320),P(4150,400),P(6800,400)],'C1 - coloană existentă',TEAL)
leader([P(3600,-470),P(2900,850),P(1550,850)],'Trecere existentă spre dormitor',TEAL)
for aa,bb,lab in [((150,-5550),(2450,-5550),'2.300 / baie'),((3700,-5550),(7100,-5550),'3.400 / sufragerie')]:dim(*P(*aa),*P(*bb),lab,25)
dim(*P(150,-250),*P(3550,-250),'3.400 / dormitor',-45)
dim(*P(3700,-250),*P(7100,-250),'3.400 / sufragerie',-45)
# Origin and scale bar
op=P(0,0);circle(*op,3,INK);txt(op[0]-18,op[1]-8,'O',10,INK,True)
for i in range(4):rect(70+i*500*k,725,500*k,7,fill=INK if i%2==0 else white,stroke=INK,lw=.5)
txt(70,746,'0',9,MUT);txt(70+1000*k,746,'1 m',9,MUT);txt(70+2000*k,746,'2 m',9,MUT)
xx=780
panel(xx,150,368,'LEGENDA','<font color="#c64937"><b>R1 / R2</b></font> Radiatoare panou noi.<br/><font color="#c64937"><b>R3</b></font> Portprosop baie.<br/><font color="#147b73"><b>C1</b></font> Coloană existentă, poziție de colț confirmată; axe de măsurat.<br/><font color="#c64937"><b>Roșu întrerupt</b></font> Tur, traseu indicativ.<br/><font color="#277dba"><b>Albastru întrerupt</b></font> Retur, traseu indicativ.<br/>Mobilierul gri este suport de coordonare, nu instalație.')
rows=[['Reper','Poziție / cotă în model'],['R1','Ax X=2.480; Y CAD≈-372; bază Z=150; gabarit 1.000×600×100.'],['R2','Ax X=4.475; Y CAD≈-372; bază Z=150; gabarit 1.200×600×100.'],['R3','Ax X=1.250; perete Y=-3.920; bază Z=500; gabarit ≈500×800.'],['C1','Colț sufragerie-dormitor, lângă ferestre. Simbol la X≈3.755, Y≈-320; NU cotă de montaj.']]
table(xx,440,[58,310],rows,10)
para(xx,692,368,'<b>Baia:</b> racordul și coloana de alimentare sunt neidentificate; nu se presupune legarea ei la C1.<br/><b>Bucătărie, hol, vestibul, debara și balcon:</b> fără emițător nou în acest plan.',10)
end()
# T02
start('T02','Coloana C1 și traversarea spre dormitor','Detaliu de coordonare; conductele desenate nu sunt trasee măsurate','Detaliu 1:25 / schemă fără scară')
P,k=view(80,260,25,clip=(42,145,850,400));route(P)
leader([P(3755,-320),P(3950,550),P(5000,550)],'C1 - cote și număr conducte de verificat',TEAL)
leader([P(3600,-470),P(2800,780),P(2100,780)],'Se reutilizează traversarea existentă',TEAL)
for label,x,y in [('R1',2480,-720),('R2',4475,-720)]:tag(*P(x,y),label,RED)
# dimension to radiator center, from room's finished left wall
for aa,bb,lab in [((150,-900),(2480,-900),'2.330 până la ax R1'),((3700,-900),(4475,-900),'775 până la ax R2')]:dim(*P(*aa),*P(*bb),lab,18)
para(925,158,223,'<b>Confirmat de beneficiar</b><br/>C1 este în colțul comun dinspre ferestre. Conductele traversează peretele spre dormitor.<br/><br/><b>De măsurat</b><br/>Axa coloanei față de pereții finisați; numărul și diametrul țevilor; cotele ramurilor; sensul curgerii; distanța între racorduri; golul existent.',11)
rows=[['Reper','Cerință de coordonare','Ce NU se fixează încă'],['C1 / coloană','Păstrare poziție și continuitate; acces la racorduri și eventuale repartitoare.','Nu se aleg robinete de coloană și nu se modifică diametrul.'],['Traversare P1','Trecerea existentă spre dormitor este păstrată. Se verifică manșonul și starea peretelui.','Nu se proiectează găuri sau șanțuri noi în peretele de 150 mm.'],['Ramuri R1/R2','Înlocuire locală doar cât este necesar pentru racordul modelului ales. Tur/retur trebuie identificate pe teren.','Nu se impune racord inferior de 50 mm sau diametru DN presupus.'],['Ramură R3 / baie','Sursă de agent termic, traseu și sens de curgere de identificat separat.','Nu este desenată o legătură fictivă prin baie/vestibul.']]
table(42,550,[165,545,396],rows,10)
end()
# T03
start('T03','Elevații / radiatoare sub ferestre','Vedere din cameră către ferestre; geometrie preluată din CAD','1:20 la imprimare A3, 100%')
def elevation(x,y,left,right,window,rad,name):
 s=72/25.4/20
 def E(xx,zz):return x+(xx-left)*s,y+(2500-zz)*s
 x0,y0=E(left,2500);rect(x0,y0,(right-left)*s,2500*s,fill=HexColor('#fafafa'),stroke=INK)
 wx0,wx1=window
 p=E(wx0,2400);rect(*p,(wx1-wx0)*s,1500*s,fill=HexColor('#eef6fb'),stroke=BLUE)
 rx0,rx1=rad;p=E(rx0,750);rect(*p,(rx1-rx0)*s,600*s,fill=HexColor('#ffe9df'),stroke=RED,lw=1.3)
 for xx in range(rx0+30,rx1-20,60):line(*E(xx,180),*E(xx,720),RED,.4)
 txt(x,y-17,name,13,TEAL,True)
 dim(*E(rx0,150),*E(rx1,150),str(rx1-rx0),30)
 dim(*E(left+60,0),*E(left+60,150),'150',-24)
 dim(*E(right-60,150),*E(right-60,750),'600',30)
 dim(*E(right-180,750),*E(right-180,900),'150',42)
 dim(*E(wx0,2400),*E(wx1,2400),str(wx1-wx0),-20)
 txt(x+25,y+2500*s+62,'±0,00 = pardoseală finită; parapet model +900',10,MUT)
 return E
E1=elevation(74,210,150,3550,(1680,3280),(1980,2980),'A-A / Dormitor - R1')
E2=elevation(640,210,3700,7100,(3750,5200),(3875,5075),'B-B / Sufragerie - R2')
para(74,690,490,'<b>R1:</b> axul radiatorului este centrat pe fereastra de 1.600 mm. Dimensiunea 1.000×600 este orientativă; lungimea finală depinde de puterea la temperatura reală și de racordurile existente.',11)
para(640,690,490,'<b>R2:</b> axul radiatorului este centrat pe fereastra de 1.450 mm. Mobilierul din dreptul radiatorului trebuie să lase libere intrarea aerului jos și ieșirea lui sus. Usa balconului este în afara acestei elevații parțiale.',11)
end()
# T04
start('T04','Baie și secțiuni de montaj','R3 opus lavoarului; relație radiator-perete-textile; trecere existentă','Baie 1:10 / secțiune 1:5 / P1 fără scară')
# bathroom elevation cropped width 1000 around radiator.
x0=70;y0=180;s=72/25.4/10
rect(x0,y0,1000*s,1500*s,fill=HexColor('#fafafa'),stroke=GRAY)
# display 0..1500 height
p=lambda xx,zz:(x0+(xx-750)*s,y0+(1500-zz)*s)
for xx in (1020,1480):line(*p(xx,500),*p(xx,1300),RED,6)
for zz in range(550,1300,80):line(*p(1020,zz),*p(1480,zz),RED,2.5)
txt(x0,y0-15,'C-C / R3 portprosop baie',12,TEAL,True)
dim(*p(1000,500),*p(1500,500),'≈500',25)
dim(*p(1600,500),*p(1600,1300),'800',20)
dim(*p(850,0),*p(850,500),'500',-22)
para(70,650,300,'Ax X=1.250 mm, centrat pe lavoar. Putere țintă preliminară ≈450 W la temperatura de lucru și cameră la 24°C. Gabaritul actual nu dovedește această putere.',10)
# section side, vertical extent 1050, width 400 at1:5
txt(455,190,'D-D / radiator sub fereastră',12,TEAL,True)
sx=455;sy=205;sc=72/25.4/5
S=lambda xx,zz:(sx+xx*sc,sy+(1000-zz)*sc)
# wall behind window / parapet
rect(*S(-70,1000),70*sc,1000*sc,fill=GRAY,stroke=MUT)
line(*S(-70,0),*S(360,0),INK,1.2)
line(*S(-70,900),*S(15,900),INK,2)
rect(*S(70,750),103*sc,600*sc,fill=HexColor('#ffe9df'),stroke=RED,lw=1.4)
line(*S(55,980),*S(55,60),ORANGE,1.5,[4,2])
leader([S(55,820),(615,310),(650,310)],'Textil în CAD',ORANGE)
leader([S(120,450),(690,430),(710,430)],'R1/R2',RED)
dim(*S(200,150),*S(200,750),'600',22)
dim(*S(245,750),*S(245,900),'150',22)
dim(*S(0,150),*S(70,150),'70',16)
dim(*S(275,0),*S(275,150),'150',15)
# penetration concept right
xx=835;yy=195
rect(xx+110,yy+60,70,250,fill=GRAY,stroke=MUT)
line(xx+20,yy+150,xx+280,yy+150,RED,4)
line(xx+20,yy+220,xx+280,yy+220,BLUE,4)
rect(xx+100,yy+141,90,18,fill=None,stroke=ORANGE)
rect(xx+100,yy+211,90,18,fill=None,stroke=ORANGE)
txt(xx,yy-15,'P1 / traversare existentă',12,TEAL,True)
leader([(xx+150,yy+143),(xx+240,yy+90),(xx+245,yy+60)],'Manșon',ORANGE)
para(xx,yy+335,285,'<b>Detaliu de principiu</b><br/>Se verifică manșonul existent, dilatarea țevilor și etanșarea compatibilă cu peretele. Nu se înglobează îmbinări demontabile în perete. Golurile și diametrele nu se deduc din desen.<br/><br/>Nu se taie și nu se șanțuiește peretele structural pentru adaptarea traseului.',11)
end()
# T05
start('T05','Necesar termic / selecție preliminară','Estimare de buget, nu calcul al pierderilor de căldură conform EN 12831')
para(42,148,1106,'<b>Metodă:</b> Q≈V×k, cu V=A×2,50 m. Estimarea discutată folosește aproximativ 35-36 W/m³ pentru camerele uscate; baia este tratată separat la ≈450 W pentru confort de 24°C. Coeficienții sunt ipoteze de buget, nu valori măsurate. U-urile pereților/ferestrelor, orientarea, infiltrațiile și temperatura exterioară de calcul nu sunt cunoscute.',11)
rows=[['Încăpere','Arie CAD / volum','Țintă aer','Q estimat','Emițător / situație'],['Dormitor','12,223 m² / 30,56 m³','20°C','≈1.100 W','R1; poziție sub geam'],['Sufragerie','18,020 m² / 45,05 m³','20°C','≈1.600 W','R2; poziție păstrată'],['Baie','3,749 m² / 9,37 m³','24°C','≈450 W','R3; produs de dimensionat'],['Bucătărie','8,211 m² / 20,53 m³','20°C, dacă se dorește','≈720 W','Fără radiator, conform cererii'],['Hol + vestibul + debara','8,890 m² / 22,22 m³','20°C, dacă se dorește','≈780 W','Fără emițător direct'],['Balcon închis','4,810 m²','Neîncălzit','Nealocat','Spațiu tampon; ușă închisă']]
y=table(42,225,[155,215,160,120,456],rows,10)
para(42,y+16,1106,'<b>Total orientativ al spațiilor interioare la temperaturile din tabel: ≈4.650 W.</b> R1+R2+R3 au ținte însumate de ≈3.150 W. Diferența de ≈1.500 W pentru spațiile fără radiator NU este alocată radiatoarelor existente. Transferul de căldură prin uși nu garantează 20°C în bucătărie și hol; selecția finală trebuie să rezolve această situație fără a presupune un radiator în bucătărie.',11)
rows=[['Regim apă / aer','Factor radiator, n≈1,3','R1: putere nominală ΔT50 necesară','R2: putere nominală ΔT50 necesară','R3 la 24°C: nominal ΔT50'],['75/65°C / 20°C','1,000','≈1.100 W','≈1.600 W','≈500 W'],['60/50°C / 20°C','≈0,629','≈1.750 W','≈2.550 W','≈840 W'],['55/45°C / 20°C','≈0,515','≈2.140 W','≈3.110 W','≈1.060 W']]
y2=table(42,y+101,[175,180,260,260,231],rows,10)
para(42,y2+12,1106,'<b>Corecție:</b> P=P50×(ΔT/50)<super>n</super>, ΔT=(tur+retur)/2 - temperatura camerei. Pentru R3 factorul se calculează separat cu aer la 24°C. Exponentul real n se ia din fișa modelului. Puterile în tabel sunt cerințe de selecție, nu puteri confirmate ale corpurilor desenate. Bază tehnică: sursele S1/S2, pagina T08.',10)
end()
# T06
start('T06','Scheme de principiu / racordare','Mai întâi se identifică instalația existentă; schema nu schimbă coloana comună')
# two-pipe principle diagram
rect(42,150,650,320,fill=HexColor('#fafbfb'),stroke=GRAY)
txt(60,177,'A / Instalație bifilară - numai dacă se confirmă',13,TEAL,True)
for x,color,label in [(105,RED,'TUR'),(160,BLUE,'RETUR')]:line(x,210,x,430,color,3);txt(x-16,450,label,10,color,True)
for yy,rr in [(235,'R1'),(355,'R2')]:
 rect(385,yy-15,135,60,fill=HexColor('#ffe9df'),stroke=RED);txt(437,yy+20,rr,12,RED,True)
 line(105,yy,385,yy,RED,2);line(160,yy+35,385,yy+35,BLUE,2)
 poly([(265,yy-7),(265,yy+7),(278,yy),(265,yy-7)],color=RED,fill=white)
 circle(320,yy+35,5,BLUE,white)
 txt(244,yy-15,'Vt',9,RED);txt(309,yy+57,'Vr',9,BLUE)
para(730,159,418,'<b>Vt:</b> robinet de reglaj/termostatic, numai compatibil cu tipul instalației și debitul disponibil.<br/><b>Vr:</b> robinet retur/detentor pentru reglaj și service.<br/><b>Aerisire:</b> accesibilă pe fiecare radiator.<br/><br/>R3 nu este legat în schemă la C1: sursa băii este necunoscută.<br/><br/>Schema de racord lateral sau inferior și poziția turului se aleg după fișa radiatorului și racordurile măsurate.',11)
# singlepipe bypass conceptual
rect(42,500,650,230,fill=HexColor('#fafbfb'),stroke=GRAY)
txt(60,527,'B / Instalație monotubulară - se păstrează circulația',13,TEAL,True)
line(105,565,105,695,RED,3);line(105,585,265,585,RED,2);line(105,660,265,660,BLUE,2);rect(265,570,145,105,fill=HexColor('#ffe9df'),stroke=RED);txt(315,626,'R',15,RED,True)
leader([(105,622),(160,622),(185,700)],'Bypass / continuitate existentă',ORANGE)
para(440,563,226,'Dacă este sistem monotubular, robinetul și bypass-ul se aleg pentru acest sistem. Nu se întrerupe circulația coloanei prin închiderea radiatorului.',10)
para(730,500,418,'<b>Date hidraulice de consemnat</b><br/>Regim mono/bifilar, presiune de lucru, temperaturi tur/retur în condiții de iarnă, diametre, material, sens curgere și stare racorduri.<br/><br/><b>Nu sunt incluse</b><br/>Pompă proprie, distribuitor de încălzire în pardoseală, modificarea coloanei, radiator în bucătărie sau pe balcon.<br/><br/>Schema de echilibrare și reglaj se completează după măsurători și modelul ales.',11)
end()
# T07
start('T07','Lista de cantități / instalația termică','Cantități pentru cerere de ofertă; fără lucrări electrice sau finisaje generale')
rows=[['Cod','Articol / lucrare','UM','Cant.','Statut / condiție'],['IT01','Radiator R1 dormitor; reprezentare panou 1.000×600×100','buc','1','Confirmat ca poziție; produs și putere finale de ales.'],['IT02','Radiator R2 sufragerie; reprezentare panou 1.200×600×100','buc','1','Confirmat ca poziție; produs și putere finale de ales.'],['IT03','Portprosop R3 baie; reprezentare ≈500×800','buc','1','Poziție confirmată; racord și putere la 24°C neconfirmate.'],['IT04','Set console și fixări pentru fiecare corp','set','3','După suportul real și kitul fabricantului; ancorele nu se aleg din desen.'],['IT05','Robinet reglaj/termostatic + cap, compatibil instalației','set','3*','Provizoriu; tipul monotubular poate cere alt ansamblu.'],['IT06','Robinet retur/detentor sau ansamblu echivalent','buc','3*','Provizoriu; configurație după identificarea instalației.'],['IT07','Aerisitor + dopuri/reducții conforme fiecărui corp','set','3','Numai ce nu este inclus în pachetul radiatorului.'],['IT08','Conducte pentru adaptare locală tur/retur R1/R2/R3','m','De măsurat','Material, DN și lungime pe fiecare ramură după releveu.'],['IT09','Coturi, racorduri olandeze, mufe și adaptoare','buc','De măsurat','Listă după racordurile și diametrele reale; fără cantitate fictivă.'],['IT10','Manșon / refacere etanșare la traversarea existentă P1','set','1*','Se verifică starea; nu înseamnă o gaură nouă în perete.'],['IT11','Demontare radiatoare fontă dormitor și sufragerie','buc','2','Inclus evacuare; radiatorul vechi al băii nu este inventariat.'],['IT12','Montare, racordare și aerisire radiatoare noi','buc','3','R3 numai după confirmarea alimentării.'],['IT13','Coordonare golire/umplere instalație și intervenție comună','lot','1','Condițiile cu administratorul/operatorul se stabilesc înainte.'],['IT14','Verificare etanșeitate, reglaj și proces-verbal','lot','1','Protocol conform instalației și componentelor; fără presiune de probă presupusă.'],['IT15','Refaceri locale finisaje și curățare după lucrări','lot','1*','Cantitate și suprafață de măsurat după desfaceri.']]
links_termice={
 'IT01':('https://www.purmo.com/docs/purmo-catalog-radiatoare-panou-ro.pdf','Catalog Purmo Compact'),
 'IT02':('https://www.purmo.com/docs/purmo-catalog-radiatoare-panou-ro.pdf','Catalog Purmo Compact'),
 'IT03':('https://www.purmo.com/ro-ro/produse/14407/santorini/','Purmo Santorini'),
 'IT04':('https://www.purmo.com/docs/purmo-catalog-radiatoare-panou-ro.pdf','Console / accesorii'),
 'IT05':('https://assets.danfoss.com/documents/latest/208753/AB370141588735ro-RO0101.pdf','Set Danfoss / fișă'),
 'IT06':('https://assets.danfoss.com/documents/latest/208753/AB370141588735ro-RO0101.pdf','Retur inclus în set'),
 'IT07':('https://www.purmo.com/docs/purmo-catalog-radiatoare-panou-ro.pdf','Accesorii radiator'),
 'IT08':('https://www.geberit.ro/sisteme-sanitare-tevi/sisteme-de-alimentare-cu-apa/geberit-mapress/geberit-mapress-otel-carbon/','Exemplu sistem de țevi'),
 'IT09':('https://www.geberit.ro/sisteme-sanitare-tevi/sisteme-de-alimentare-cu-apa/geberit-mapress/geberit-mapress-otel-carbon/','Fitinguri de sistem'),
 'IT10':('https://www.geberit.ro/_assets/local-media/geberit-mapress-manual-tehnic-2022.pdf','Detalii de montaj')}
for row in rows[1:]:
 if row[0] in links_termice:
  url,label=links_termice[row[0]]
  row[1]+=' <link href="'+url+'" color="#277dba">'+label+'</link>.'
y=table(42,150,[60,390,55,100,501],rows,10)
para(42,y+14,1106,'<b>* Cantitate de buget, condiționată.</b> Nu se comandă robinete, țevi și fitinguri înainte de identificarea instalației. Prețurile și mărcile nu sunt fixate. Linkurile albastre sunt exemple de selecție, nu produse aprobate; IT05/IT06 pot fi același kit și nu se comandă dublu. Compatibilitatea țevilor cu circuitul se verifică. Oferta separă materialele și manopera.',10)
end()
# T08
start('T08','Măsurători, recepție și trasabilitate','Pașii necesari pentru transformarea dosarului în documentație de execuție')
rows=[['De verificat înainte de comandă','Rezultat de completat pe teren'],['Coloana C1 și P1','Axe X/Y/Z, număr conducte, diametre, material, stare, sens de curgere și fotografii.'],['R1 și R2','Dimensiuni fontă existente, interaxe și cote racorduri, parapet finit, distanțe la textile și mobilier.'],['R3 baie','Sursa agentului termic, traseul existent, racorduri și necesar pentru 24°C; fișa portprosopului.'],['Necesar termic final','U pereți/geamuri, expuneri, temperatură exterioară locală, ventilație, camere vecine și spații fără radiator.'],['Regim termoficare','Temperaturi și presiuni reale, tip mono/bifilar, acces la izolare/golire, repartitoare existente dacă sunt.'],['Alegerea produsului','Putere la regimul real, presiune/temperatură admise, conexiuni, greutate, console și compatibilitate cu agentul termic.'],['Recepție','Etanșeitate fără pierderi, aerisire, reglaj, încălzire uniformă, acces service, proces-verbal și fotografii finale.']]
y=table(42,150,[300,806],rows,11)
para(42,y+18,535,'<b>Coordonare cu amenajarea</b><br/>Radiatoarele rămân în pozițiile convenite. Draperiile blackout nu trebuie să închidă radiatorul într-un volum fără circulație de aer. Blatul/biroul din sufragerie nu trebuie să blocheze ieșirea aerului cald. Aceste două detalii se verifică cu corpurile efectiv alese, fără mutarea automată a mobilierului.',11)
para(620,y+18,528,'<b>Sursa geometriei</b><br/>Modelul FreeCAD deschis la data 05.10.2026: apartament_184.FCStd și baie.FCStd. Ariile, gabaritele și pozițiile R1/R2/R3 sunt extrase din CAD. Poziția de colț a C1 și traversarea spre dormitor sunt confirmate verbal de beneficiar; coordonatele exacte sunt nemăsurate.',11)
sy=y+145
txt(42,sy,'SURSE TEHNICE / CONSULTATE 05.10.2026',11,TEAL,True)
para(42,sy+15,1106,'<b>S1. Purmo - Buyers guide:</b> selecție după pierderi termice și regim real, poziție sub geam, distanțe de montaj. <link href="https://www.purmo.com/en/inspiration/buyers-guide.htm" color="#277dba">Ghid oficial Purmo</link>.<br/><b>S2. Global Radiatori - VOX:</b> puteri EN 442 și exponentul de corecție, exemplu pentru elemenți. <link href="https://www.globalradiatori.it/uploads/blog/00228_17743514200.pdf" color="#277dba">Fișă oficială VOX</link>.<br/><b>S3. Stelrad - Radiator positioning:</b> efectul mobilierului și perdelelor asupra distribuției căldurii. <link href="https://www.stelrad.com/news-events/blog/how-to-position-your-radiator-to-get-the-most-efficient-heating/" color="#277dba">Ghid oficial Stelrad</link>.',10)
para(42,sy+100,1106,'<b>Statut:</b> dosar de coordonare și ofertare. Nu conține calcul hidraulic validat, releveu al țevilor sau calcul complet EN 12831. Nu se prezintă drept proiect semnat/verificat. Documentația finală și intervențiile asupra instalației comune se stabilesc cu specialistul responsabil și administratorul, după situația reală.',10)
end()
c.save()
print(str(OUT));print('Pages:',PAGE)


