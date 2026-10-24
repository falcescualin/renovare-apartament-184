"""Plan sanitar baie R02: aceleași planșe ca R01 (plan_sanitar_baie_pdf.py, nemodificat), refăcute cu ultimele decizii:
- S07: produsele alese în devizul R03, cu prețul celei mai bune oferte și link la magazin;
- S08: lista exactă de țevi PPR / PP, fitinguri, robineți, hidroizolație (CL 51 + CL 152), amorsă R777 și șapă Nivello 50,
  plus racordul mașinii de spălat din vestibul (acum inclus);
- S09: ordinea amorsă → șapă → hidroizolație → microciment.
Rulează cu Python-ul care are reportlab. Iese: output/pdf/Apartament_184_Plan_sanitar_baie_R02.pdf"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_comun import *

SRC = (ROOT / 'scripturi/plan_sanitar_baie_pdf.py').read_text(encoding='utf-8-sig')


def rep(a, b, n=1):
    global SRC
    assert SRC.count(a) == n, (SRC.count(a), a[:90])
    SRC = SRC.replace(a, b)


def section(start, stop, new):
    global SRC
    i, j = SRC.index(start), SRC.index(stop)
    SRC = SRC[:i] + new.lstrip('\n') + SRC[j:]


rep('Apartament_184_Plan_sanitar_baie_R01.pdf', 'Apartament_184_Plan_sanitar_baie_R02.pdf')
rep("exec(compile(src,'drawing_helpers','exec'))", "src=patch_prefix(src).replace('R01 |','R02 |');exec(compile(src,'drawing_helpers','exec'))")
rep("c.setTitle('Apartament 184 - Instalatii sanitare baie - plan, montaj si cantitati cu linkuri')",
    "c.setTitle('Apartament 184 - Instalatii sanitare baie - R02 - plan, montaj, cantitati si preturi')")

# linkurile duc acum la produsele alese în deviz (cea mai bună ofertă)
NEW_L = {k: (DVR[i]['url'], lab) for k, i, lab in [
    ('cadă', 'M040', 'Roca Contesa 150×70 / absulo'), ('cadru', 'M043', 'Geberit Duofix Sigma 111.300.00.5 / eSanitare'),
    ('WC', 'M045', 'Roca Meridian Rimless compact / Instalplus'), ('lavoar', 'M046', 'Roca Gap New 60 cu mască / Dedeman'),
    ('baterie_lav', 'M047', 'Grohe Eurosmart 33265002 / Sanitino'), ('baterie_cadă', 'M042', 'Grohe 32831000 / Sanitino'),
    ('sifon_cadă', 'M041', 'Alcadrain A55KM / euro-instal'), ('paravan', 'M048', 'Mediterraneo 80×140 / Neakaisa'),
    ('apă', 'M050', 'PPR 20 PN20 / Dedeman'), ('canal', 'M051', 'PP Ø50 / Dedeman'), ('robinet', 'M049', 'Ferro colțar 1/2×3/8 / Dedeman'),
    ('hidro', 'M052', 'Ceresit CL 51 / Leroy Merlin'), ('clapetă', 'M044', 'Geberit Sigma01 / Neakaisa'),
    ('nivello', 'M009', 'Baumit Nivello 50 / Dedeman'), ('r777', 'M001', 'Ceresit R777 / Dedeman'), ('rigips', 'M053', 'Rigips RBI / Dedeman'),
    ('microciment', 'M006', 'Microciment pardoseală / Cementart')]}
rep('def link(key):', 'L.update(NEW_L)\ndef link(key):')

# ---- S00
rep("start('S00','Instalații sanitare / baie','Plan de coordonare, detalii de montaj și cantități cu linkuri')",
    "start('S00','Instalații sanitare / baie','R02: produsele alese cu preț (S07), lista exactă de țevi, fitinguri și hidroizolație (S08), racordul mașinii de spălat, ordinea șapă → hidroizolație → microciment (S09)')")
rep("['S07','Cantități obiecte / echipamente cu linkuri'],['S08','Cantități instalație / hidroizolație cu linkuri']",
    "['S07','Obiecte sanitare alese, cu preț și link la magazin'],['S08','Țevi, fitinguri, robineți, șapă și hidroizolație: cantități exacte, prețuri']")

# ---- S02: mașina de spălat e inclusă acum
rep("Mașina de spălat este în vestibul: alimentarea și evacuarea ei nu fac parte din acest dosar al băii.",
    "Mașina de spălat din vestibul (corpul SP, lângă peretele băii) se racordează din aceeași zonă: robinet pe AR și scurgere Ø40 cu sifon cu clapetă; cantitățile sunt în S08.")

# ---- S07: obiectele alese, cu preț
rep("start('S07','Cantități / obiecte și echipamente','Linkurile albastre sunt clicabile; variante de selecție, nu comenzi ferme')",
    "start('S07','Obiecte sanitare alese / preț și magazin','Devizul R03: cea mai bună ofertă găsită pe 05.10.2026, prețuri cu TVA; linkurile duc la magazin')")
S07 = r'''
MAP={'IS01':'M040','IS02':'M055','IS03':'M041','IS04':'M042','IS05':'M042','IS06':'M043','IS07':'M044','IS08':'M045','IS09':'M045','IS10':'M046','IS11':'M047','IS12':'M047','IS13':'M048'}
seen=set();new=[['Cod','Articol ales','Cant.','Preț lei','Unde','Verificare înainte de comandă']];tot=0
for r in rows[1:]:
 i=MAP[r[0]]
 if i in seen:new.append([r[0],esc(r[1])+' <font color="#536473">(inclus în rândul de mai sus)</font>',r[2],'inclus','',r[4]])
 else:
  seen.add(i);tot+=DVR[i]['tmin'];new.append([r[0],'<b>'+esc(DVR[i]['art'])+'</b>',r[2],lei(DVR[i]['tmin']),dvlink(DVR[i]),r[4]])
new.append(['','<b>Total obiecte sanitare</b>','','<b>'+lei(tot)+'</b>','',''])
y=tbl(42,148,[48,290,52,58,300,358],new,9,4,total=True)
para(42,y+12,1106,'Culorile și dimensiunile se confirmă la comandă. Variantă mai ieftină pentru lavoar: set Roca The Gap 60 A855997806 (German Quality, 2.199,94 lei). Corpurile de mobilier și măștile se detaliază separat.',10);end()
'''
rep("table(42,150,[55,270,70,290,421],rows,10)\npara(42,725,1106,'Prețurile/stocul și selecția finală nu sunt fixate. Produsele sunt exemple pentru ofertare; culorile și dimensiunile se confirmă. Corpurile de mobilier și măștile necesită detaliere separată, nu o comandă directă din catalog.',10);end()\n",
    S07.lstrip('\n'))

# ---- S08: lista exactă de instalație, șapă și hidroizolație
S08 = r'''
# S08
start('S08','Țevi, fitinguri, șapă și hidroizolație / cantități exacte','Lungimi din modelul băii + 20 % rezervă; prețurile celei mai bune oferte (deviz R03, M001, M009, M049–M053, M056)')
f2=lambda v:lei2(v)
rows=[['Cod','Articol','Cant.','Preț unitar','Total lei','Unde / bază de cantitate'],
['','<b>APĂ RECE / CALDĂ (M049, M050)</b>','','','',''],
['IS14','Robinet colțar Ferro 1/2 × 3/8, alamă cromată','2 buc','17,30','34,60',link('robinet')+': lavoar AR + AC'],
['IS15','Robinet AR rezervor','inclus','-','-','inclus în stelajul Geberit; nu se comandă dublu'],
['IS16','Robineți de izolare AR / AC pentru baie','2 buc','~25','50,00','estimat; la coloană, cu acces'],
['IS17','Robinet pentru mașina de spălat (vestibul)','1 buc','~20','20,00','estimat; pe AR, lângă corpul SP'],
['IS18','Țeavă PPR 20 PN20, bare de 4 m','5 bare = 20 m','9,75','48,75',link('apă')+': ~10 m AR + ~6 m AC + 20 %'],
['IS19','Coturi și teuri PPR 20','20 buc','0,76','15,20','Dedeman; o piesă la fiecare schimbare de direcție'],
['IS20','Coturi PPR 20 cu filet 1/2 (ieșiri)','7 buc','7,96','55,72','Dedeman; lavoar ×2, cadă ×2, rezervor, mașină, rezervă'],
['IS21','Izolație țeavă 22 mm, bare','8 buc','4,71','37,68','Dedeman; AC complet, AR în măști'],
['','<b>CANALIZARE PP (M051, M056)</b>','','','',''],
['IS22','Țeavă PP Ø50, 1 m','5 buc','14,16','70,80',link('canal')+': lavoar → coloană 1,7 m, cadă → coloană 2,3 m'],
['IS23','Țeavă PP Ø40','3 m','~7','21,00','estimat; mașina de spălat ~2–3 m'],
['IS24','Țeavă / racord PP Ø110 pentru WC','1 m','~20','20,00','estimat; WC → coloană'],
['IS25','Cot PP Ø50 87°','6 buc','3,11','18,66','Dedeman'],
['IS26','Coturi 45°, ramificații, reducții, mufe','1 lot','-','52,00','estimat; după racordul la coloană'],
['IS27','Sifon cu clapetă + racord scurgere mașină de spălat','1 buc','~40','40,00','estimat (M056)'],
['','<b>ȘAPĂ ȘI HIDROIZOLAȚIE (M001, M009, M052, M053)</b>','','','',''],
['IS28','Amorsă Ceresit R777, 10 kg','1 buc','123,48','123,48',link('r777')+': pentru toată pardoseala apartamentului'],
['IS29','Șapă Baumit Nivello 50, 25 kg','2 saci','77,00','154,00',link('nivello')+': 3,75 m² × 5 mm × 1,5 kg/m²/mm = 28 kg'],
['IS30','Hidroizolație Ceresit CL 51, 15 kg','1 găleată','325,00','325,00',link('hidro')+': pardoseală + ridicări; al doilea set dacă se tratează toți pereții'],
['IS31','Bandă Ceresit CL 152, 10 m','1 rolă','105,90','105,90',link('bandă')+': perimetru 7,86 m + colțuri nișe (Dedeman)'],
['IS32','Plăci Rigips RBI + profile, trape WC și cadă','1 lot','-','399,96',link('rigips')+': măști WC, nișe, trapă 250 × 500, acces sifon']]
tot=sum(DVR[i]['tmin'] for i in ('M049','M050','M051','M052','M053','M056'))+DVR['M001']['tmin']+DVR['M009']['tmin']
rows.append(['','<b>Total instalație, șapă și hidroizolație baie</b>','','','<b>'+lei(tot)+'</b>','microcimentul (M006, M010) e în devizul de finisaje'])
y=tbl(42,148,[46,330,92,72,72,494],rows,9,3,total=True)
para(42,y+10,1106,'Prețurile sunt cele observate pe 05.10.2026; „~” înseamnă estimat. Cotele exacte ale racordurilor se iau la releveu; dacă diferă mult de model, se refac lungimile, nu fitingurile.',10);end()
'''
section('# S08', '# S09', S08)

# ---- S09: ordinea pardoselii băii și mașina de spălat
rep("['6 / Hidroizolare','Suport, benzi, manșete și timp de uscare conform fișelor; control înaintea placării.']",
    "['6 / Șapă și hidroizolare','Amorsă R777 → șapă Nivello 50 (≈5 mm) → CL 51 în două straturi, cu bandă CL 152 la colțuri, rosturi și străpungeri → microciment impermeabil pe pardoseală și pereți. Timpi de uscare conform fișelor; control înaintea finisajului.']")
rep("Instalația mașinii de spălat din vestibul este în afara acestui dosar.",
    "Racordul mașinii de spălat din vestibul (robinet AR, scurgere Ø40 cu sifon cu clapetă) e inclus acum în S08.")

SRC = SRC.replace('c.save()', "\n# ---- NOTE 06.10.2026: coloane noi, radiatorul din baie, PPR, scurgerea mașinii de spălat\nstart('S10','Note de verificat: coloane, radiatorul din baie, PPR, scurgerea mașinii de spălat','Adăugat pe 06.10.2026 la cererea beneficiarului; nimic de aici nu e măsurat pe teren')\ny=148+para(42,148,540,'<b>1. Radiatorul din baie (R3): sursa agentului termic e necunoscută</b><br/>'\n 'Nu se știe de unde vine agentul termic la portprosopul din baie. Planul nu presupune nicio legătură cu coloanele din colțul dormitorului. Se verifică înainte de comandă:<br/>'\n '• dacă există o țeavă de tur și retur în zona băii (pe sub pardoseală, în perete sau spre vestibul), cu poze și cote;<br/>'\n '• dacă portprosopul era legat la apa caldă menajeră sau la încălzire (diferă temperatura și regimul de funcționare);<br/>'\n '• ce spun asociația și furnizorul de termoficare despre ramificații și modificări la coloană;<br/>'\n '• dacă se poate alimenta din cele două coloane din colțul dormitorului, cu traseu prin zid sau prin pardoseală (șanțuri noi în pereții structurali nu se fac).<br/>'\n 'Până se lămurește, R3 rămâne în dosar fără racord desenat, iar portprosopul se poate înlocui cu varianta electrică, dacă sursa nu se găsește.',10)\ny=y+16+para(42,y+16,540,'<b>2. Baia: schimbăm totul pe PPR?</b> (decizie de luat după punctul 1)<br/>'\n 'Planul sanitar prevede deja apă rece și caldă în PPR 20 PN20 și canalizare PP. De hotărât:<br/>'\n '• dacă se înlocuiesc toate conductele vechi din baie cu PPR, inclusiv cele din pereți, înainte de microciment și hidroizolație (după ele nu mai are rost să se deschidă);<br/>'\n '• pentru <b>încălzire</b>, PPR PN20 simplu are limită de temperatură; la tur de termoficare se folosește PPR armat (cu aluminiu sau fibră) sau multistrat. Se confirmă cu instalatorul și cu fișa produsului, după temperaturile reale;<br/>'\n '• racordurile la coloane se fac cu robineți de închidere accesibili, ca să nu se oprească blocul.',10)\ny2=148+para(620,148,528,'<b>3. Două coloane de agent termic în colțul dormitorului (modelate)</b><br/>'\n 'În colțul dormitor–sufragerie, pe partea radiatorului, sunt două țevi verticale Ø26,9 mm, de la pardoseală la tavan: axe X 3465 și X 3525, Y −280, în spatele draperiei. '\n 'Diametrul, materialul, sensul (tur / retur), axele și legătura cu C1 din planul R01 (simbol la X≈3755, în sufragerie) sunt de măsurat. '\n 'Draperia și șina sunt acum cu 175 mm în cameră, ca să acopere radiatorul și coloanele; blatul mesei de machiaj a fost scurtat de la 800 la 630 mm.',10)\ny2=y2+16+para(620,y2+16,528,'<b>4. Scurgerea mașinii de spălat: coloană mare la colțul vestibul–sufragerie</b><br/>'\n 'Coloana de canalizare Ø110 trece prin colț (model: axa X 3450, Y −5450, de măsurat) și se izolează fonic: vată minerală 40 mm + membrană fonică (Ø190), închisă într-o mască de gips-carton 2 × 12,5 mm (≈ 22 × 22 cm). '\n 'Mobilierul din spălătorie ține cont de ea: rafturile coloanei laterale au 38 cm adâncime în loc de 62, panoul și capacul de sus ocolesc masca, iar robinetul de rezervă s-a mutat cu 25 cm spre ușă. '\n 'Masca are trapă de acces la mufe și la curățitor. Izolația fonică nu înlocuiește etanșarea trecerii prin planșeu.',10)\nend()\n" + 'c.save()', 1) if SRC.count('c.save()') == 1 else SRC
assert '# ---- NOTE 06.10.2026: coloan' in SRC
exec(compile(SRC, 'plan_sanitar_baie_pdf+R02', 'exec'))
