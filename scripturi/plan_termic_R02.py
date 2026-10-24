"""Plan termic R02: aceleași planșe ca R01 (plan_termic_pdf.py, nemodificat), refăcute cu ultimele decizii:
- produsele alese în devizul R03, cu preț și link (T07): Purmo Compact 22 600×1000 / 600×1200, Purmo Santorini 500×714,
  kit Danfoss, racorduri multistrat 16×2;
- R3 la mărimea standard 500 × 714 (500 × 800 nu există în gamă), T01 / T04;
- mobilierul actual pe planuri; calendarul: radiatoarele înainte de pornirea căldurii.
Rulează cu Python-ul care are reportlab. Iese: output/pdf/Apartament_184_Plan_termic_R02.pdf"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_comun import *

pre, rest = (ROOT / 'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')
SRC = patch_prefix(pre) + '# T00' + rest


def rep(a, b, n=1):
    global SRC
    assert SRC.count(a) == n, (SRC.count(a), a[:90])
    SRC = SRC.replace(a, b)


rep('Apartament_184_Plan_termic_R01.pdf', 'Apartament_184_Plan_termic_R02.pdf')
rep("'R01 | 05.10.2026 |", "'R02 | 05.10.2026 |")
rep("c.setTitle('Apartament 184 - Plan termic, sectiuni si cantitati - R01')", "c.setTitle('Apartament 184 - Plan termic, sectiuni si cantitati - R02')")

# ---- T00
rep("start('T00','Instalația termică','Dosar de coordonare: amplasare, secțiuni, racorduri și cantități')",
    "start('T00','Instalația termică','R02: produsele alese cu preț (T07), portprosopul R3 la 500 × 714, mobilierul actual pe planuri, montaj înainte de pornirea căldurii')")
rep("'Radiator nou, sub geam'", "'Purmo Compact 22, 600 × 1000, sub geam'")
rep("'Radiator nou, poziție păstrată'", "'Purmo Compact 22, 600 × 1200, poziție păstrată'")
rep("'Portprosop, opus lavoarului'", "'Purmo Santorini 500 × 714, opus lavoarului'")
rep("Bucătăria rămâne fără radiator.',12)",
    "Bucătăria rămâne fără radiator. <b>Calendar:</b> radiatoarele se montează pe 13–15.10, înainte de pornirea căldurii; golirea coloanei se programează din timp cu asociația.',12)")
rep('Dimensiunile radiatoarelor sunt cele de reprezentare din CAD.',
    'Produsele sunt alese (T07), dar puterea lor se verifică la temperatura reală a agentului termic.')

# ---- T01: gabarite reale
rep("gabarit 1.000×600×100.", "Purmo C22 1.000 × 600.")
rep("gabarit 1.200×600×100.", "Purmo C22 1.200 × 600.")
rep("gabarit ≈500×800.", "Santorini 500 × 714 (modelul 3D are 500 × 800).")

# ---- T04: portprosopul la 714
rep("for xx in (1020,1480):line(*p(xx,500),*p(xx,1300),RED,6)", "for xx in (1020,1480):line(*p(xx,500),*p(xx,1214),RED,6)")
rep("for zz in range(550,1300,80):line(*p(1020,zz),*p(1480,zz),RED,2.5)", "for zz in range(550,1214,80):line(*p(1020,zz),*p(1480,zz),RED,2.5)")
rep("dim(*p(1600,500),*p(1600,1300),'800',20)", "dim(*p(1600,500),*p(1600,1214),'714',20)")
rep("dim(*p(1000,500),*p(1500,500),'≈500',25)", "dim(*p(1000,500),*p(1500,500),'500',25)")
rep("'Ax X=1.250 mm, centrat pe lavoar. Putere țintă preliminară ≈450 W la temperatura de lucru și cameră la 24°C. Gabaritul actual nu dovedește această putere.'",
    "'Ax X=1.250 mm, centrat pe lavoar. Purmo Santorini 500 × 714 (deviz R03). Putere țintă ≈450 W la 24°C: se verifică în fișă la temperatura reală a agentului termic.'")

# ---- T07: produse, prețuri, magazine
rep("start('T07','Lista de cantități / instalația termică','Cantități pentru cerere de ofertă; fără lucrări electrice sau finisaje generale')",
    "start('T07','Lista de cantități / instalația termică','Produsele alese în devizul R03, la cea mai bună ofertă găsită pe 05.10.2026; prețuri cu TVA, manopera separat')")
T07 = r'''
MAP={'IT01':'M057','IT02':'M058','IT03':'M059','IT05':'M060','IT08':'M061'}
INC={'IT04':'incluse la R1/R2 (pachet cu accesorii); la R3 după kit','IT06':'inclus în kitul Danfoss (IT05)','IT07':'incluse în pachetul radiatoarelor','IT09':'inclus la IT08: 8 racorduri 16 × 2'}
new=[['Cod','Articol / lucrare','UM','Cant.','Preț lei','Unde / statut']];tot=0
for r in rows[1:]:
 code=r[0]
 if code in MAP:
  d=DVR[MAP[code]];tot+=d['tmin'];new.append([code,'<b>'+esc(d['art'])+'</b>',r[2],qty(d).split(' ')[0] if code!='IT08' else '1 lot',lei(d['tmin']),dvlink(d)+'<br/>'+r[4]])
 elif code in INC:new.append([code,r[1],r[2],r[3],'inclus',INC[code]])
 elif code>='IT11':new.append([code,r[1],r[2],r[3],'manoperă','în afara devizului de materiale; '+r[4]])
 else:new.append([code,r[1],r[2],r[3],'-',r[4]])
new.append(['','<b>Total materiale încălzire</b>','','','<b>'+lei(tot)+'</b>','R1 + R2 + R3 + 3 kituri Danfoss + racorduri multistrat'])
y=tbl(42,148,[50,420,50,60,70,456],new,9,4,total=True)
para(42,y+14,1106,'<b>Cumpărare:</b> radiatoarele și kiturile în săptămâna 12.10 (etapa E1), ca montajul să fie gata înainte de pornirea căldurii. Robinetele și racordurile se confirmă după identificarea instalației (mono/bifilar). IT05/IT06 sunt același kit și nu se cumpără dublu. Fitingurile pentru R3 depind de racordul băii, încă nemăsurat.',10)
'''
rep("y=table(42,150,[60,390,55,100,501],rows,10)\n", T07.lstrip('\n'))
rep("para(42,y+14,1106,'<b>* Cantitate de buget, condiționată.</b>", "if 0:para(42,y+14,1106,'<b>* Cantitate de buget, condiționată.</b>")

SRC = SRC.replace('c.save()', "\n# ---- NOTE 06.10.2026: coloane noi, radiatorul din baie, PPR, scurgerea mașinii de spălat\nstart('T10','Note de verificat: coloane, radiatorul din baie, PPR, scurgerea mașinii de spălat','Adăugat pe 06.10.2026 la cererea beneficiarului; nimic de aici nu e măsurat pe teren')\ny=148+para(42,148,540,'<b>1. Radiatorul din baie (R3): sursa agentului termic e necunoscută</b><br/>'\n 'Nu se știe de unde vine agentul termic la portprosopul din baie. Planul nu presupune nicio legătură cu coloanele din colțul dormitorului. Se verifică înainte de comandă:<br/>'\n '• dacă există o țeavă de tur și retur în zona băii (pe sub pardoseală, în perete sau spre vestibul), cu poze și cote;<br/>'\n '• dacă portprosopul era legat la apa caldă menajeră sau la încălzire (diferă temperatura și regimul de funcționare);<br/>'\n '• ce spun asociația și furnizorul de termoficare despre ramificații și modificări la coloană;<br/>'\n '• dacă se poate alimenta din cele două coloane din colțul dormitorului, cu traseu prin zid sau prin pardoseală (șanțuri noi în pereții structurali nu se fac).<br/>'\n 'Până se lămurește, R3 rămâne în dosar fără racord desenat, iar portprosopul se poate înlocui cu varianta electrică, dacă sursa nu se găsește.',10)\ny=y+16+para(42,y+16,540,'<b>2. Baia: schimbăm totul pe PPR?</b> (decizie de luat după punctul 1)<br/>'\n 'Planul sanitar prevede deja apă rece și caldă în PPR 20 PN20 și canalizare PP. De hotărât:<br/>'\n '• dacă se înlocuiesc toate conductele vechi din baie cu PPR, inclusiv cele din pereți, înainte de microciment și hidroizolație (după ele nu mai are rost să se deschidă);<br/>'\n '• pentru <b>încălzire</b>, PPR PN20 simplu are limită de temperatură; la tur de termoficare se folosește PPR armat (cu aluminiu sau fibră) sau multistrat. Se confirmă cu instalatorul și cu fișa produsului, după temperaturile reale;<br/>'\n '• racordurile la coloane se fac cu robineți de închidere accesibili, ca să nu se oprească blocul.',10)\ny2=148+para(620,148,528,'<b>3. Două coloane de agent termic în colțul dormitorului (modelate)</b><br/>'\n 'În colțul dormitor–sufragerie, pe partea radiatorului, sunt două țevi verticale Ø26,9 mm, de la pardoseală la tavan: axe X 3465 și X 3525, Y −280, în spatele draperiei. '\n 'Diametrul, materialul, sensul (tur / retur), axele și legătura cu C1 din planul R01 (simbol la X≈3755, în sufragerie) sunt de măsurat. '\n 'Draperia și șina sunt acum cu 175 mm în cameră, ca să acopere radiatorul și coloanele; blatul mesei de machiaj a fost scurtat de la 800 la 630 mm.',10)\ny2=y2+16+para(620,y2+16,528,'<b>4. Scurgerea mașinii de spălat: coloană mare la colțul vestibul–sufragerie</b><br/>'\n 'Coloana de canalizare Ø110 trece prin colț (model: axa X 3450, Y −5450, de măsurat) și se izolează fonic: vată minerală 40 mm + membrană fonică (Ø190), închisă într-o mască de gips-carton 2 × 12,5 mm (≈ 22 × 22 cm). '\n 'Mobilierul din spălătorie ține cont de ea: rafturile coloanei laterale au 38 cm adâncime în loc de 62, panoul și capacul de sus ocolesc masca, iar robinetul de rezervă s-a mutat cu 25 cm spre ușă. '\n 'Masca are trapă de acces la mufe și la curățitor. Izolația fonică nu înlocuiește etanșarea trecerii prin planșeu.',10)\nend()\n" + 'c.save()', 1) if SRC.count('c.save()') == 1 else SRC
assert '# ---- NOTE 06.10.2026: coloan' in SRC
exec(compile(SRC, 'plan_termic_pdf+R02', 'exec'))
