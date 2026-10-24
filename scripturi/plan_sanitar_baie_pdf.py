from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
# Reuse the verified A3 drawing system, without executing thermal pages.
src=(ROOT/'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8-sig').split('# T00')[0]
src=src.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'","OUT=ROOT/'output/pdf/Apartament_184_Plan_sanitar_baie_R01.pdf'")
src=src.replace("('TOPPADDING',(0,0),(-1,-1),9)","('TOPPADDING',(0,0),(-1,-1),7)").replace("('BOTTOMPADDING',(0,0),(-1,-1),9)","('BOTTOMPADDING',(0,0),(-1,-1),7)")
exec(compile(src,'drawing_helpers','exec'))
c.setTitle('Apartament 184 - Instalatii sanitare baie - plan, montaj si cantitati cu linkuri')
BA={o['name']:o for o in json.loads((ROOT/'tmp/baie_sanitar_model.json').read_text(encoding='utf-8'))}
GREEN=HexColor('#35845c')
L={
'cadă':('https://www.dedeman.ro/ro/cada-baie-dreptunghiulara-roca-contesa-a236060000-150-x-70-cm/p/3036495','Roca Contesa 150×70 / Dedeman'),
'cadru':('https://catalog.geberit.ro/ro-RO/product/PRO_3933392','Geberit Duofix Sigma 112 cm'),
'WC':('https://www.roca.ro/produse/vas-wc-compact-suspendat-rimless-evacuare-orizontala-346244..0','Roca Meridian compact Rimless'),
'lavoar':('https://www.roca.ro/produse/lavoar-suspendat-60cm-3270M1..0?sku=A3270M1000','Roca The Gap 600×460'),
'baterie_lav':('https://www.grohe.ro/ro_ro/eurosmart-cosmopolitan-baterie-lavoar-monocomand-1-2-m-rimea-s-2337700E.html','Grohe Eurosmart Cosmopolitan'),
'baterie_cadă':('https://www.sanitino.ro/grohe-eurosmart-cosmopolitan-baterie-cada-monocomanda-crom-32831000','Grohe 32831000 / Sanitino'),
'duș':('https://www.dedeman.ro/ro/set-dus-para-furtun-suport-savoniera-bara-grohe-tempesta-28436001-4-functii-1-75-m/p/3017922','Grohe Tempesta / Dedeman'),
'sifon_cadă':('https://www.alcadrain.ro/produse/sifoane-pentru-cada/ovladane/a55km-detail','Alcadrain A55KM'),
'sifon_lav':('https://www.alcadrain.ro/sifon-de-retinere-a-mirosurilor/sifoane-pentru-lavoar','Alcadrain / sifoane lavoar'),
'paravan':('https://configurator.radaway.ro/paravane-de-cada/serie','Radaway / configurator paravane'),
'apă':('https://www.geberit.ro/sisteme-sanitare-tevi/sisteme-de-alimentare-cu-apa/geberit-flowfit/','Geberit FlowFit / sistem apă'),
'canal':('https://www.geberit.ro/sisteme-sanitare-tevi/sisteme-de-drenaj/geberit-silent-pp/','Geberit Silent-PP / canalizare'),
'robinet':('https://www.alcadrain.ro/produse/alte-produse/rohove-ventily','Alcadrain / robineți colțar'),
'trapă':('https://knauf.com/ro-RO/p/produs/trapa-de-vizitare-aquapanel-r-15294_0123','Knauf AQUAPANEL / trapă'),
'hidro':('https://www.ceresit.ro/servicii/aplicatii/placari/solutii-de-hidroizolare-pentru-camere-umede.html','Ceresit / sistem camere umede'),
'bandă':('https://www.ceresit.ro/produse/solutii-pentru-placari/produs.html/ceresit-cl-152/SAP_0201SMC013Q6.html','Ceresit CL 152 / bandă'),
'normativ':('https://legislatie.just.ro/Public/DetaliiDocument/262177','Ordin de aprobare I9-2022')}
def link(key):
 url,label=L[key];return '<link href="'+url+'" color="#277dba">'+label+'</link>'
def bathroom(ox=75,oy=210,scale=10):
 k=72/25.4/scale
 def P(x,y):return ox+(x-150)*k,oy+(-3920-y)*k
 rect(ox-15*k,oy-15*k,2330*k,1660*k,fill=HexColor('#f7f9fa'),stroke=INK,lw=1.4)
 # Main fixture envelopes, current CAD only.
 for name,col in [('Cada_150x70',HexColor('#edf6fa')),('Masca_cada_nise',HexColor('#e5e0d7')),('Corp_lavoar',HexColor('#e5e0d7')),('Masca_WC_polita_sus',HexColor('#e5e0d7')),('WC_suspendat',white),('Calorifer_prosop',HexColor('#ffe9df'))]:
  bb=BA[name]['bbox'];p=P(bb[0],bb[4]);rect(*p,(bb[3]-bb[0])*k,(bb[4]-bb[1])*k,fill=col,stroke=MUT,lw=.7)
 # tub inner bowl
 rect(*P(210,-3990),580*k,1360*k,fill=white,stroke=BLUE,lw=.6)
 # paravan at long edge, existing closed position.
 b=BA['Paravan_sticla_cada']['bbox'];line(*P(b[0],b[1]),*P(b[0],b[4]),BLUE,2)
 # Outward door leaf; old wall aperture stays.
 rect(*P(2450,-4200),75*k,700*k,fill=white,stroke=white)
 hv=(2487.5,-4200);op=(3187.5,-4200)
 line(*P(*hv),*P(*op),MUT,.6)
 pts=[P(hv[0]+700*math.cos(-math.pi/2+math.pi/2*i/24),hv[1]+700*math.sin(-math.pi/2+math.pi/2*i/24)) for i in range(25)]
 poly(pts,color=GRAY,lw=.6,close=False)
 return P,k

def water(P):
 for col,dy in [(BLUE,0),(RED,45)]:
  pts=[(2320,-5500+dy),(500,-5500+dy),(300,-5500+dy),(300,-5200)]
  for a,b in zip(pts,pts[1:]):line(*P(*a),*P(*b),col,1.6,[5,2])
  for pt in [(1250,-5500+dy),(500,-5500+dy)]:circle(*P(*pt),3,col,white)
  line(*P(1250,-5500+dy),*P(1250,-5310+dy),col,1.6,[5,2])
 line(*P(2320,-5500),*P(2075,-5500),BLUE,1.6,[5,2]);line(*P(2075,-5500),*P(2075,-5330),BLUE,1.6,[5,2])

def drains(P):
 paths=[([(500,-5290),(500,-5400),(2320,-5400),(2320,-5500)],'Ø50 / cadă'), ([(1250,-5350),(1250,-5460),(2320,-5460),(2320,-5500)],'Ø40→50 / lavoar'), ([(2075,-5260),(2075,-5500),(2320,-5500)],'Ø90/110 / WC')]
 for pts,lab in paths:
  for aa,bb in zip(pts,pts[1:]):line(*P(*aa),*P(*bb),GREEN,2.1,[5,2])
  circle(*P(*pts[0]),4,GREEN,white)
 circle(*P(2320,-5500),7,TEAL,white)
 return paths
# S00
start('S00','Instalații sanitare / baie','Plan de coordonare, detalii de montaj și cantități cu linkuri')
for x,title,val,body in [(42,'BAIE','2.300 × 1.630 mm','Înălțime liberă 2.500 mm'),(410,'OBIECTE','Cadă / lavoar / WC','Lavoarul este central; WC la dreapta'),(778,'COLOANĂ','În zona WC-ului','Capătul peretelui spre vestibul')]:
 rect(x,150,350,130,fill=LIGHT,stroke=GRAY);txt(x+16,180,title,11,TEAL,True);txt(x+16,220,val,21,INK,True);txt(x+16,252,body,11,MUT)
para(42,304,530,'<b>Configurație păstrată</b><br/>Cadă 150×70 cm, între peretele dinspre dormitor și masca cu nișe de 13 cm. Paravan rabatabil 80×140 cm. Lavoar 60 cm pe peretele coloanei, central. WC suspendat cu rezervor încastrat, mască de 65×30 cm și acces lateral spre lavoar. Ușa se deschide spre vestibul.',12)
para(620,304,525,'<b>Date necesare înainte de execuție</b><br/>Coloana este confirmată în zona WC-ului; axa și cota racordurilor nu sunt măsurate. Se verifică sursa apei calde, presiunea, diametrele existente, cota de intrare în canalizare și grosimea disponibilă a pardoselii. Nu se intervine în pereții structurali pe baza acestei planșe.',12)
rows=[['Planșă','Conținut'],['S01','Amplasare cotată și repere obiecte sanitare, 1:10'],['S02','Apă rece / caldă - trasee propuse și cote de montaj'],['S03','Canalizare - ramuri propuse și profil cu pantă'],['S04','Elevația peretelui WC-lavoar și repere de racord'],['S05','WC suspendat - stelaș, mască și acces de service'],['S06','Cadă, paravan, nișe și etanșări'],['S07','Cantități obiecte / echipamente cu linkuri'],['S08','Cantități instalație / hidroizolație cu linkuri'],['S09','Ordine montaj, verificări, documente și surse']]
table(42,448,[95,1011],rows,10);end()
# S01
start('S01','Plan baie / amplasare și dimensiuni','Cote în mm, după modelul CAD; axe conducte și coloane de măsurat','1:10 la imprimare A3, 100%')
P,k=bathroom()
for label,x,y in [('C / CADĂ',400,-4650),('L / LAVOAR',1100,-5200),('W / WC',2000,-5070),('R3',1130,-4110),('NIȘE',330,-5460)]:txt(*P(x,y),label,10,TEAL,True)
# column reference in confirmed area, footprint schematic.
circle(*P(2320,-5500),7,TEAL,white)
leader([P(2320,-5500),P(2450,-5550),(770,720)],'CS - zona coloanei',TEAL)
dim(*P(150,-3920),*P(2450,-3920),'2.300',-38)
dim(*P(150,-3920),*P(150,-5550),'1.630',-32)
dim(*P(150,-5420),*P(850,-5420),'700',14)
dim(*P(950,-5100),*P(1550,-5100),'600',15)
dim(*P(1750,-5250),*P(2400,-5250),'650',15)
leader([P(834,-5000),(775,405),(805,405)],'Paravan',BLUE)
para(845,160,303,'<b>CS:</b> coloana de canalizare și racordurile de apă sunt în zona WC-ului, spre vestibul, conform beneficiarului. Simbolul indică zona, nu coordonata reală.<br/><br/><b>Cadă:</b> Y=-5.420...-3.920; X=150...850.<br/><b>Lavoar:</b> X=950...1.550; corp adâncime 450.<br/><b>Mască WC:</b> X=1.750...2.400; adâncime 300.<br/><br/><b>Acces:</b> trapa laterală este demontabilă, nu cu balamale, în golul de 200 mm dintre lavoar și mască.<br/><br/>Masca cu nișe umple exact cei 130 mm dintre cadă și peretele coloanei.',11)
para(75,723,670,'Origine de cote: coordonate CAD ale apartamentului; ±0,00 = pardoseală finită. Cotele sunt de amenajare. Toate racordurile se verifică după produsele finale.',10);end()
# S02
start('S02','Alimentare cu apă rece și caldă','Trasee propuse în măști tehnice, fără șanțuri presupuse în pereții structurali','1:10 / repere de montaj orientative')
P,k=bathroom(75,185,10);water(P)
for label,x,y in [('Cadă / AR+AC',220,-5110),('Lavoar / AR+AC',1050,-5220),('WC / numai AR',1840,-5150)]:txt(*P(x,y),label,10,TEAL,True)
circle(*P(2320,-5500),7,TEAL,white)
rows=[['Punct','Racord / cotă orientativă'],['L / lavoar','AR+AC cu robineți colțar, în corp la ≈550 mm; evacuare ≈500-550 mm, după sifon și sertare.'],['C / cadă','Baterie aparentă pe peretele lung, în zona paravanului; ax ≈950 mm. Interaxul bateriei se ia din fișă.'],['W / WC','Numai AR, la racordul rezervorului ales; nu se fixează o cotă universală.'],['AR / AC','Albastru: apă rece. Roșu: apă caldă. Trasee întrerupte = propunere.']]
table(845,150,[55,248],rows,10)
para(845,520,303,'<b>Principiu propus</b><br/>Ramuri din zona coloanei spre obiecte. Se asigură izolare locală și acces la robinete; apa caldă și rece se izolează adecvat. Materialul și diametrele se aleg după debit/presiune și sistemul existent.<br/><br/>Nu se înglobează îmbinări demontabile. Țevile nu se presupun montate în cei ≈20 mm rămași în spatele nișelor: se coordonează măști separate / trasee joase accesibile.',10)
para(75,697,690,'Mașina de spălat este în vestibul: alimentarea și evacuarea ei nu fac parte din acest dosar al băii. Portprosopul R3 aparține instalației termice, nu alimentării cu apă menajeră.',10);end()
# S03
start('S03','Canalizare / trasee și profil','Trasee gravitaționale propuse; cota racordului CS este necunoscută','Plan 1:15 / profil schematic fără scară')
P,k=bathroom(75,185,15);drains(P)
txt(*P(550,-5270),'Sifon cadă',10,GREEN,True)
txt(*P(970,-5260),'Lavoar',10,GREEN,True)
txt(*P(1800,-5110),'WC',10,GREEN,True)
para(585,160,563,'<b>Ramuri de verificat</b><br/>Cadă: evacuare sifon spre ramură Ø50 orientativ. Lavoar: sifon Ø32/40, ramură Ø40/50 orientativ. WC: racord Ø90/110 conform stelașului. Acestea sunt diametre de coordonare, nu dimensionare finală.<br/><br/>Coloana comună și aerisirea ei se păstrează. Acces pentru curățare, racordurile în sensul curgerii și tipul ramificațiilor se stabilesc cu sistemul ales. Nu se propune WC conectat la conducta lavoarului.',11)
# conceptual profile lower half
x=90;y=610
line(x,715,x+665,715,INK,1)
line(x,600,x+600,625,GREEN,5)
line(x,625,x+600,650,GREEN,1)
rect(x-15,575,30,50,fill=LIGHT,stroke=MUT)
line(x+600,555,x+600,700,TEAL,8)
txt(x,558,'Sifon cadă / cotă de ieșire de măsurat',11,TEAL,True)
txt(x+470,545,'CS / racord existent',11,TEAL,True)
dim(x,660,x+600,660,'Exemplu: L = 2.000 mm',20)
leader([(x+310,613),(x+310,580),(x+345,580)],'i = 2% → Δh = 40 mm',GREEN)
para(830,490,318,'<b>Condiție de fezabilitate</b><br/>Exemplul de 2% este o ipoteză de verificare, nu o pantă prescrisă pentru toate ramurile. Δh=i×L. Pe 2 m rezultă 40 mm diferență de nivel, la care se adaugă gabaritul țevii, mufelor și spațiul de montaj.<br/><br/>Se măsoară cota sifonului și a racordului coloanei. Dacă nu încape, se revizuiește soluția locală; nu se taie planșeul pentru a crea panta.',11)
end()
# S04
start('S04','Elevație / peretele lavoar-WC','Vedere din cameră; cote finite raportate la pardoseală','1:10 la imprimare A3, 100%')
s=72/25.4/10;E=lambda x,z:(85+(x-150)*s,150+(2200-z)*s)
rect(*E(150,2200),2300*s,2200*s,fill=HexColor('#fafafa'),stroke=GRAY)
for name,col in [('Masca_cada_nise',HexColor('#e5e0d7')),('Corp_lavoar',HexColor('#e5e0d7')),('Lavoar_60',white),('Oglinda_lavoar',HexColor('#e5f1f6')),('Masca_WC_fata',HexColor('#e5e0d7')),('Clapeta_WC_service',white),('Dulap_WC_usa',HexColor('#e5e0d7')),('Dulap_WC_usa001',HexColor('#e5e0d7'))]:
 b=BA[name]['bbox'];rect(*E(b[0],b[5]),(b[3]-b[0])*s,(b[5]-b[2])*s,fill=col,stroke=MUT,lw=.7)
for z,h in [(800,350),(1250,350),(1700,300)]:rect(*E(210,z+h),580*s,h*s,fill=white,stroke=INK,lw=.6)
# WC front silhouette, height from CAD.
rect(*E(1895,455),360*s,185*s,fill=white,stroke=MUT)
# vanity water/drain service zone, not exact drilling template
for xx,col in [(1210,RED),(1290,BLUE)]:circle(*E(xx,550),4,col,white)
circle(*E(1250,510),5,GREEN,white)
leader([E(1250,510),(770,610),(810,610)],'Racorduri lavoar',GREEN)
dim(*E(950,400),*E(1550,400),'600',20)
dim(*E(1750,1210),*E(2400,1210),'650',-15)
dim(*E(1550,1030),*E(1750,1030),'200 / acces',-20)
para(850,160,298,'<b>Cote CAD</b><br/>Lavoar: margine superioară ≈890 mm.<br/>Mobilier lavoar: 400...830 mm.<br/>Șezut WC: ≈455 mm.<br/>Mască WC: ≈1.235 mm inclusiv capac.<br/>Dulap WC: 1.350...2.150 mm.<br/><br/><b>Repere propuse pentru instalații</b><br/>Robineți lavoar ≈550 mm; evacuare ≈510 mm. Pozițiile se confirmă cu sertarele, sifonul și lavoarul final.<br/><br/>Cota vasului se reglează după pardoseala finită și modelul ales. Clapeta rezervorului rămâne accesibilă.',11)
# drawing extends to2200*0.283=624 =>804, footer conflict! shift height starts at 2100 croppedfloor? fix scale below in QA if needed
end()
# S05
start('S05','WC suspendat / mască și acces','Stelaș portant dedicat; placa de închidere nu susține vasul','Secțiuni schematice fără scară')
# Side section
rect(80,180,80,470,fill=GRAY,stroke=MUT)
rect(190,245,160,260,fill=HexColor('#edf6fa'),stroke=BLUE)
for xx in (185,355):line(xx,215,xx,650,TEAL,7)
line(175,650,380,650,TEAL,7)
rect(390,185,25,475,fill=HexColor('#e5e0d7'),stroke=MUT)
poly([(415,450),(595,450),(625,510),(600,550),(415,550)],fill=white,color=MUT)
line(415,480,350,480,GREEN,5);line(350,480,350,615,GREEN,5)
line(80,660,665,660,INK,1.5)
leader([(265,265),(285,180),(430,180)],'Rezervor încastrat',BLUE)
leader([(185,580),(125,710),(170,710)],'Fixări în suport portant',TEAL)
leader([(403,290),(525,270),(555,270)],'Clapetă / service',TEAL)
para(720,155,428,'<b>Variantă de selecție</b><br/>'+link('cadru')+'; cadru de 500 mm lățime și 1.120 mm înălțime, conform fișei. Se verifică adâncimea completă cu racordul Ø90/110 în masca de 300 mm.<br/><br/>Fixarea se face în suportul admis de fabricant. Nu se substituie cadrul portant prin rigips și nu se omit ancorele/șinele necesare.',11)
para(720,360,428,'<b>Acces lateral suplimentar</b><br/>Trapa de aproximativ 250×500 mm este pe partea dinspre lavoar. În golul de 200 mm se folosește un panou complet demontabil. Accesul principal la mecanismul rezervorului este prin clapeta frontală.<br/><br/>Poziția coloanei comune poate impune un gol mai mare de intervenție. Trapa nu garantează acces la toate racordurile până la releveu.',11)
para(720,582,428,'<b>Ordine de montaj</b><br/>Stelaș + fixări → alimentare AR → evacuare → probe → închidere umedă/hidroizolare → placare → ceramică și clapetă. Grosimea finisajelor se introduce înaintea reglării cotelor.',11);end()
# S06
start('S06','Cadă / paravan / nișe și etanșări','Ansamblu 1.500 + 130 = 1.630 mm; sifon accesibil','Detalii schematice fără scară')
# schematic long section bath and niche
rect(85,205,60,370,fill=GRAY,stroke=MUT)
rect(160,230,520,350,fill=HexColor('#edf6fa'),stroke=BLUE)
poly([(180,255),(650,255),(620,490),(215,490)],fill=white,color=BLUE)
rect(685,180,65,400,fill=HexColor('#e5e0d7'),stroke=MUT)
for yy in (240,330,420):rect(690,yy,50,50,fill=white,stroke=MUT)
line(85,590,765,590,INK,1.2)
line(210,525,570,525,GREEN,4)
rect(200,495,40,45,fill=LIGHT,stroke=GREEN)
leader([(220,520),(185,640),(220,640)],'Sifon cu preaplin / acces',GREEN)
dim(160,590,680,590,'1.500 / cadă',45)
dim(685,590,750,590,'130',45)
para(825,155,323,'<b>Montaj cadă</b><br/>Kit de susținere și fixare conform produsului, sifon cu preaplin și panou demontabil pentru service. Se probează scurgerea înainte de închidere. Dimensiunea reală a căzii și grosimea placării se verifică înainte de executarea măștii.',11)
para(825,350,323,'<b>Nișe</b><br/>Masca umple golul de 130 mm; adâncimea geometrică a nișei este ≈110 mm, redusă de finisaje. Suport pentru umiditate, hidroizolație continuă, colțuri/bandă și etanșări la străpungeri. Nu este gips-carton obișnuit și nu se taie peretele structural.',11)
para(825,575,323,'<b>Paravan</b><br/>80×140 cm, rabatabil spre cadă. Profilul se fixează în ranforsarea măștii; nu doar în placă. Se verifică accesul la nișe, cursa sticlei și racordul etanș la cadă. '+link('paravan')+'.',10)
para(85,700,660,'<b>Hidroizolația:</b> racord cadă-perete cu soluție compatibilă sistemului, nu doar silicon decorativ. Rosturile, colțurile și trecerile de țevi se etanșează înaintea placării. '+link('hidro')+'.',11);end()
# S07
start('S07','Cantități / obiecte și echipamente','Linkurile albastre sunt clicabile; variante de selecție, nu comenzi ferme')
rows=[['Cod','Articol','Cant.','Link produs / fișă','Verificare înainte de comandă'],['IS01','Cadă 150×70 cm','1 buc',link('cadă'),'Roca Contesa A236060000: exemplu 150×70; înălțimea și susținerea finală după fișă.'],['IS02','Kit susținere / fixare cadă','1 set',link('cadă'),'Kit compatibil cu cada, nu console universale presupuse.'],['IS03','Sifon cadă + preaplin','1 set',link('sifon_cadă'),'Gaură de evacuare, lungime preaplin și acces pentru curățare.'],['IS04','Baterie aparentă cadă-duș','1 buc',link('baterie_cadă'),'Interax, AR/AC, presiune și suport; fără baterie încastrată în nișa de 13 cm.'],['IS05','Set pară + furtun + suport/bară','1 set',link('duș'),'Verifică ce include pachetul bateriei; evită dublarea furtunului/perei.'],['IS06','Stelaș WC + rezervor','1 set',link('cadru'),'Sigma 111.300.00.6 ca variantă; kit ancorare, racord și accesorii după pachet.'],['IS07','Clapetă compatibilă Sigma','1 buc',link('cadru'),'Clapeta poate fi separată de stelaș; se comandă seria compatibilă.'],['IS08','Vas WC suspendat compact','1 buc',link('WC'),'Exemplu 360×480 mm, mai scurt decât gabaritul CAD ≈520 mm; racord/fixare compatibile.'],['IS09','Capac soft-close compatibil','1 buc',link('WC'),'Codul compatibil se ia din pagina vasului; dacă este inclus, nu se dublează.'],['IS10','Lavoar ≈60 cm + mobilier','1 set',link('lavoar'),'Exemplul The Gap are 600×460, CAD 600×450: diferență 10 mm; se coordonează mobilierul.'],['IS11','Baterie lavoar','1 buc',link('baterie_lav'),'Lungimea pipei și prinderea; ventilul poate fi inclus.'],['IS12','Ventil + sifon lavoar','1 set',link('sifon_lav'),'După evacuare/preaplin și sertare; nu se dublează ventilul inclus în baterie.'],['IS13','Paravan rabatabil ≈80×140 cm','1 set',link('paravan'),'Dimensiune și sticlă după serie; configuratorul nu reprezintă un cod de produs ales.']]
table(42,150,[55,270,70,290,421],rows,10)
para(42,725,1106,'Prețurile/stocul și selecția finală nu sunt fixate. Produsele sunt exemple pentru ofertare; culorile și dimensiunile se confirmă. Corpurile de mobilier și măștile necesită detaliere separată, nu o comandă directă din catalog.',10);end()
# S08
start('S08','Cantități / apă, canalizare și etanșări','Accesorii de montaj; cantitățile conductelor depind de măsurarea racordurilor')
rows=[['Cod','Articol','UM / cant.','Link / sistem','Bază de cantitate'],['IS14','Robineți colțar lavoar','buc / 2',link('robinet'),'AR+AC; dimensiuni după furtunurile bateriei.'],['IS15','Robinet AR rezervor','buc / 1*',link('cadru'),'De regulă inclus în stelaș; nu se comandă dublu.'],['IS16','Izolare locală AR/AC baie','set / 1*',link('robinet'),'2 robinete dacă nu există; poziție accesibilă, fără schimbarea coloanei comune.'],['IS17','Țevi/fitinguri apă rece/caldă','m / de măsurat',link('apă'),'Un singur sistem certificat pentru apă potabilă; diametre și lungimi după debit/releveu.'],['IS18','Izolație conducte AR/AC','m / de măsurat',link('apă'),'După lungimea reală, condens/dilatare și fișa sistemului.'],['IS19','Ramuri evacuare lavoar/cadă','m / de măsurat',link('canal'),'Ø40/50 orientativ; lungime, pantă și cotă finale de calculat.'],['IS20','Racord WC Ø90/110','set / 1*',link('cadru'),'Verifică racordul inclus în kitul WC; piesă de tranziție după coloana existentă.'],['IS21','Coturi, ramificații, mufe, curățare','buc / de măsurat',link('canal'),'După fiecare schimbare de direcție, cote și acces; fără listă fictivă de fitinguri.'],['IS22','Fixări și protecție fonică WC','set / 1*',link('cadru'),'Conform pachetului; se listează doar ce lipsește.'],['IS23','Trapă laterală WC demontabilă','buc / 1',link('trapă'),'≈250×500 mm în concept; sistem și gol după accesul real la coloane.'],['IS24','Acces sifon cadă','buc / 1',link('trapă'),'Panou demontabil compatibil masca; dimensiune după sifon și cursa mâinii.'],['IS25','Hidroizolație pardoseală baie','m² / 3,749',link('hidro'),'Arie CAD; ridicări pe pereți și pierderi se adaugă separat.'],['IS26','Hidroizolație nișe / pereți umezi','m² / de măsurat',link('hidro'),'După fețele finale, toate colțurile și străpungerile; consum în kg după fișă.'],['IS27','Bandă, colțuri și manșete','m/buc / de măsurat',link('bandă'),'Perimetru geometric baie 7,86 m înainte de goluri; rosturi nișe și tubulaturi suplimentare.']]
table(42,150,[55,275,125,260,391],rows,9)
para(42,726,1106,'* Cantitate condiționată: se verifică accesoriile incluse. Pentru lucrări: 1 lot demontări sanitare, 1 lot montaj și probe, 1 lot refaceri locale; valoarea după releveu. Nu se include un sifon nou de pardoseală sau o pompă de evacuare necerută.',10);end()
# S09
start('S09','Montaj, probe și surse','Dosar de coordonare/ofertare; verificări înaintea închiderii măștilor')
rows=[['Etapă','Verificare / document de predat'],['1 / Releveu','Poziție CS, apă AR/AC, contoare/robinete, diametre, cota evacuării, grosime pardoseală și fotografii.'],['2 / Produse','Fișe pentru cadă, sifon, stelaș, ceramică, lavoar, baterii și paravan; accesorii incluse și compatibilitate.'],['3 / Trasee','Se confirmă debitele, diametrele, pantele și nivelurile. Coloanele comune și aerisirile se păstrează.'],['4 / Montaj brut','Stelaș portant, conducte și fixări; acces la robinete, sifoane și curățare; fără îmbinări demontabile inaccesibile.'],['5 / Probe înainte de închidere','Apă: etanșeitate conform sistemului. Canalizare: evacuare/etanșeitate cu obiectele simulate; fără contrapante. Se consemnează rezultatele.'],['6 / Hidroizolare','Suport, benzi, manșete și timp de uscare conform fișelor; control înaintea placării.'],['7 / Finalizare','Reglare cote WC/lavoar, test preaplin/sifoane, clapetă, paravan și acces service; fotografii și proces-verbal.']]
y=table(42,150,[225,881],rows,11)
para(42,y+20,535,'<b>Repere tehnice</b><br/>'+link('normativ')+'. Documentația finală trebuie să respecte reglementările aplicabile și fișele produselor. Diametrele și panta din acest dosar sunt propuneri de coordonare, nu calcul hidraulic validat.<br/><br/><b>Geometrie:</b> baie.FCStd, extras la 05.10.2026. CS confirmată de beneficiar în zona WC spre vestibul; axe și cote nemăsurate.',11)
para(620,y+20,528,'<b>Linkuri și alegerea produselor</b><br/>Linkurile din S07/S08 duc la pagini oficiale, fișe sau comercianți identificați. Au fost consultate la 05.10.2026. Nu sunt aprobări de comandă.<br/><br/>Ventilatorul și prizele băii rămân în model, dar nu sunt dimensionate aici. Portprosopul este documentat în planul termic. Instalația mașinii de spălat din vestibul este în afara acestui dosar.',11)
end();c.save();print(str(OUT));print('Pages:',PAGE)


