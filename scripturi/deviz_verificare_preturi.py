"""R02 deviz: aplica preturile verificate online (05.10.2026) pe liniile din tmp/deviz.json (R01 Codex, 103 linii),
cu link si baza de pret pentru fiecare. Liniile fara produs ales raman 'estimat'. Recalculeaza totalurile,
scrie tmp/deviz.json (backup R01 in tmp/deviz_R01_codex.json) si Deviz_materiale_ap184.xlsx cu coloana de link."""
import json, collections, shutil
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'tmp/deviz.json'
BAK = ROOT / 'tmp/deviz_R01_codex.json'
if not BAK.exists():
    shutil.copy(SRC, BAK)
D = json.loads(BAK.read_text(encoding='utf-8'))
ROWS = {r['id']: r for r in D['rows']}
V, E = 'verificat', 'estimat'
DT = '05.10.2026'


def up(i, pmin, pmax, url, basis, st=V, art=None, q=None, um=None, note=None):
    r = ROWS[i]
    r.update(pmin=round(pmin, 2), pmax=round(pmax, 2), url=url, price_basis=basis + ' (' + DT + ')', st=st)
    if art: r['art'] = art
    if q is not None: r['q'] = q
    if um: r['um'] = um
    if note: r['note'] = note


DD = 'https://www.dedeman.ro/ro/'
# ---------------------------------------------------------------- 1. sapa si pardoseli
up('M001', 123.48, 125.55, DD + 'amorsa-pentru-sape-ceresit-r777-interior-10-kg/p/5001054', 'Dedeman 125,55 lei / 10 kg; Presto 123,48 lei',
   art='Amorsă pentru șape Ceresit R777, 10 kg (acoperă 60–90 m²)', q=1,
   note='Amorsă penetrantă sub șapa autonivelantă, pe toată suprafața interioară (51 m²); o găleată ajunge.')
up('M009', 77, 90, DD + 'sapa-autonivelanta-baumit-nivello-50-interior/-exterior-25-kg/p/5018684',
   'Dedeman 90 lei; Hornbach 85 lei; Vasion 77 lei / sac 25 kg',
   art='Șapă autonivelantă Baumit Nivello 50, interior / exterior, pe bază de ciment, 2–50 mm, 25 kg (baie)',
   note='Baie 3,75 m² × 5 mm × 1,5 kg/m²/mm = 28 kg → 2 saci. Ordinea: amorsă R777 → Nivello 50 → hidroizolație CL 51 + bandă CL 152 (M052) → microciment impermeabil.')
up('M003', 129, 149, DD + 'parchet-triplustratificat-14-mm-diana-forest-stejar-carmelian-finisaj-lac-mat/p/4016234',
   'Dedeman 149 lei/m², promoție 129 lei/m²', art='Parchet triplustratificat 14 mm Diana Forest stejar, lac mat (30,2 m² + 8 %)')
up('M004', 112, 112, DD + 'substrat-din-polistiren-extrudat-pentru-parchet-laminat-3-in-1-arbiton-secura-aquastop-2-mm-cu-bariera-de-vapori-rola-13-64-x-1-1-m/p/4014470',
   'Dedeman 112 lei / rolă 15 m² (12,50 lei/m²)', art='Subparchet Arbiton Secura AquaStop 3 în 1, 2 mm, cu barieră de vapori', q=3, um='rolă')
up('M005', 24.89, 46.90, DD + 'plinta-parchet-mdf-set-alb-2440-x-60-x-19-mm/p/4021233', 'Dedeman: SET alb 60 mm 24,89 lei; 90 mm 46,90 lei / 2,44 m',
   art='Plintă MDF SET albă 2440 × 60 (sau 90) × 19 mm', q=18, um='buc')
up('M007', 1267.60, 2535.20, 'https://emex.ro/pardoseala-epoxidica', 'Kit Emex 10 kg + 2 kg întăritor 633,80 lei; 2 kituri la ~1 mm, 4 kituri la 2 mm',
   art='Pardoseală epoxidică autonivelantă Emex gri: bucătărie, debara, balcon (~15 m²)', q=1, um='lot')
up('M008', 74.51, 74.51, DD + 'profil-aluminiu-de-trecere-set-s04-autoadeziv-argintiu-2-7-m/p/4020004', 'Dedeman 74,51 lei / bară 2,7 m',
   art='Profil de trecere aluminiu SET S04 argintiu, 2,7 m (din 2 bare se taie cele 5 praguri)', q=2, um='buc')
# ---------------------------------------------------------------- 2. pereti
up('M011', 39.00, 39.00, DD + 'glet-de-finisaj-knauf-satengips-pe-baza-de-ipsos-interior-20-kg/p/5018715', 'Dedeman 39,00 lei / sac 20 kg',
   art='Glet de finisaj Knauf Satengips 20 kg')
up('M012', 77.98, 77.98, DD + 'amorsa-perete-ceresit-ct-17-interior/-exterior-10-l/p/5003196', 'Dedeman 77,98 lei / 10 L; vopseaua de mai jos are deja 4 L amorsă',
   art='Amorsă Ceresit CT 17, 10 L, pentru glet', q=1)
up('M013', 474.90, 574.90, DD + 'vopsea-superlavabila-interior-savana-superalba-alb-15-l-amorsa-4-l/p/5014502',
   'Dedeman: Savana Superalba 15 L + amorsă 4 L 474,90 lei; Savana Ultra Rezist 574,90 lei', art='Vopsea Savana Superalba 15 L + amorsă 4 L (2 straturi)')
up('M016', 59.99, 59.99, DD + 'brau-decorativ-poliuretan-sp2-modern-alb-200-x-2-1-x-1-cm/p/8054675', 'Dedeman 59,99 lei / bară 2 m',
   art='Brâu poliuretan SP2, 200 × 2,1 × 1 cm, pentru baghetele peretelui TV (profilul final de ales)', q=15, um='buc')
up('M017', 299, 299, DD + 'riflaj-decorativ-tip-panou-acustic-mdf-unic-spot-stejar-2400-x-600-x-21-mm/p/4026476', 'Dedeman 299 lei / panou',
   art='Panou riflaj acustic Unic Spot stejar 2400 × 600 × 21 mm (tavan 2,50 m: completare sus/jos)')
# ---------------------------------------------------------------- 3. electric
up('M018', 4.84, 4.84, DD + 'rola-cablu-electric-cyy-f-3-x-1-5-mmp-100-m-cupru/p/1073159', 'Dedeman 484 lei / rolă 100 m',
   art='Cablu CYY-F 3 × 1,5 mm² (o rolă de 100 m ajunge)', q=86,
   note='Calcul exact pe traseele R04, circuitele C01–C03: 77,8 m (traseul comun numărat o dată) + 1 m la tablou pe circuit + 0,3 m la fiecare punct = 86 m.')
up('M019', 7.25, 7.25, DD + 'rola-cablu-electric-cyy-f-600/-1000-3-x-2-5-mmp-100-m-cupru/p/1073161', 'Dedeman 725 lei / rolă 100 m',
   art='Cablu CYY-F 3 × 2,5 mm² (rolă 100 m + ~37 m la metru)', q=137,
   note='Calcul exact pe traseele R04, circuitele C04–C12: 115,6 m (prizele de pe același circuit legate în serie) + 4,6 m urcări între prize + 1 m la tablou pe circuit + 0,3 m la fiecare priză = 137 m.')
up('M021', 10.39, 14.90, DD + 'priza-schuko-simpla-schneider-electric-asfora-eph2900221-incastrat-rama-inclusa-contact-de-protectie-alb/p/1036843',
   'Dedeman: Asfora simplă 14,90 lei; dublă EPH9900121 20,78 lei (10,39 lei / post)', art='Prize Schuko Schneider Asfora albe cu ramă (simple + duble)')
up('M020', 255, 820, DD + 'copex-hdpe-total-plast-fara-halogen-cu-fir-d-20-mm-rola-50-m/p/1061301',
   'Copex 20 mm: Total Plast 28,99–31,99 lei / rolă 50 m; Legrand 750 N 2,89 lei/m (Dedeman). Doze aparat GW24208 0,75 lei; doze derivație 39-019 9,96 lei',
   art='Tub copex 20 mm (~250 m) + ~45 doze de aparat + 6 doze de derivație J01–J06',
   note='Tub pentru 223 m de cablu 230 V + date (R04); 23 grupuri de prize + 8 întrerupătoare + 7 prize date ≈ 45 doze; la ramele duble, doze duble.')
up('M022', 15.20, 15.20, DD + 'intrerupator-dublu-schneider-electric-asfora-eph0300121-incastrat-rama-inclusa-alb/p/1036844',
   'Dedeman: Asfora simplu EPH0100121 14,24 lei × 6 + dublu EPH0300121 18,08 lei × 2 = 121,60 lei', art='Întrerupătoare Schneider Asfora (6 simple + 2 duble)')
up('M023', 742.92, 837.72, DD + 'tablou-electric-gewiss-gw40051-aparent-54-18-x-3-module/p/1041973',
   'Gewiss GW40051 333 lei (Dedeman) + separator Schneider iSW A9S65240 62,32–79,45 lei + SPD Easy9 EZ9L33620 285–319,16 lei + 2 bare N/PE Gewiss 16,40–32,19 lei + pieptene Easy9 1P+N 29,80–41,73 lei',
   art='Tablou Gewiss GW40051 54 module + separator iSW 2P 40 A + descărcător SPD T2 1P+N + bare N/PE + pieptene')
up('M024', 219, 270.72, 'https://www.vonmag.ro/produse/info/a9dg4616-pret-intrerupator-diferential-rcbo-icv40h-1p-n-b-16a-10ka-30ma-tip-a-schneider',
   'Schneider iCV40H A9DG4616 tip A 219 lei (Vonmag); Acti9 RCBO B16 tip A 10 kA 270,72 lei (Micul Electrician)',
   art='RCBO Schneider Acti9 1P+N 30 mA tip A (2 × B10 + 8 × B16)')
up('M025', 994.30, 1099, 'https://www.vonmag.ro/produse/info/a9tde3616-pret-acti9-afdd-intreruptor-automat-diferential-detectie-arc-electric-icv40n-rcbo-1p-n-curba-b-16a-6ka-30ma-tip',
   'Schneider Acti9 iCV40N VigiARC A9TDE3616 (AFDD + RCBO într-un aparat): Celon 994,30 lei – Vonmag 1.099 lei. Alternativ AFDD separat ABB S-ARC1 594,50 lei + RCBO',
   art='AFDD + RCBO Schneider Acti9 iCV40N VigiARC A9TDE3616, 1P+N B16 30 mA (C01, C04)')
up('M026', 157.50, 230, DD + 'conector-wago-221-413-compact-3-fire-0-02-4-mmp-set-50-bucati/p/1062639',
   'Wago 221-413 set 50 buc: Mathaus 86,50 – Dedeman 95 lei; set 57 etichete tablou 20,99 lei (eMAG); coliere / cleme estimate 50–115 lei',
   art='Conectori Wago 221-413 (50 buc) + etichete tablou + coliere')
up('M028', 516.99, 662.99, 'https://www.a2t.ro/stocuri-limitate/cablu-utp-cat6-cupru-0-53-mm-rezistent-la-flacara-dahua-pfm920i-6un-c-v2-1.html',
   'Rolă 305 m cupru: Dahua 516,99 lei (a2t); Safer 662,99 lei. Varianta la metru, ~52 m, iese mai ieftin dacă există',
   art='Cablu UTP Cat6 cupru integral, rolă 305 m', q=1, um='rolă')
up('M029', 197 + 99.09 + 40, 213.2 + 181.60 + 80, DD + 'priza-internet-schneider-electric-asfora-eph4700121-rj45-cat-6-incastrat-rama-inclusa-alb/p/1086580',
   '4 × RJ45 Asfora 49,25 lei (Dedeman) + patch-panel 8 porturi Cat6 99,09–181,60 lei (eMAG) + patch-corduri estimate',
   art='4 prize RJ45 Cat6 Schneider Asfora + patch-panel 8 porturi + patch-corduri')
up('M030', 21 + 71.34 + 30, 62.6 + 82.08 + 60, DD + 'priza-tv-de-capat-asfora-eph3200121-rama-inclusa-alb/p/1036847',
   'RG6 Dedeman 1,05–3,13 lei/m × 20 m (traseu R04 14,7 m + rezerve) + 3 prize TV Asfora 23,78–27,36 lei + distribuitor estimat',
   art='Cablu coaxial RG6 20 m + 3 prize TV Asfora + distribuitor')
up('M031', 132.81, 160.97, 'https://www.emag.ro/switch-tp-link-8-x-10-100-1000mbps-tl-sg108/pd/EKFVNBBBM/', 'eMAG 132,81–160,97 lei',
   art='Switch TP-Link TL-SG108, 8 porturi gigabit')
# ---------------------------------------------------------------- 5. iluminat
up('M034', 128, 155, DD + 'plafoniera-led-memo-05-935-24-w-lumina-calda/-neutra/-rece-rotunda-negru-modern/p/1064357',
   'Dedeman: Memo 05-935 24 W 128 lei; Memo 05-945 24 W 3000 K 155 lei; baie / balcon: model IP44 de ales', art='Plafoniere LED 24 W (Memo 05-935 / 05-945)')
up('M035', 129.99, 450, 'https://eiluminat.ro/products/aplica-led-liniara-80cm-neagra-echivalent-400w', 'eiluminat 80 cm 129,99 lei; Chass 60 cm 450 lei (glim.ro)',
   art='Aplice LED liniare negre 60–80 cm')
up('M036', 85, 162, 'https://dvbdesign.ro/produs/banda-led-cob-8w-m-320led-m-cri90-24v-rola-5m/', 'COB 8 W/m CRI90 24 V 85 lei (DVB Design); Premium COB 162 lei (top-led)',
   art='Bandă LED COB 24 V CRI90, rolă 5 m (45 m)', q=9, um='rolă')
up('M037', 41, 88.90, 'https://smartego.ro/profile-aluminiu/3523-profil-din-aluminiu-pentru-banda-led-cu-difuzor-opac-2-m.html',
   'Profil aplicat 2 m cu difuzor: 41–88,90 lei', art='Profil aluminiu aplicat 2 m cu difuzor opal (40 m)', q=20, um='buc')
up('M038', 79, 175, 'https://led-box.ro/products/lpv-60-24-mean-well-sursa-alimentare-led-60w-24v-2-5a', 'Mean Well LPV-60-24 79 lei; HLG-60H-24A 175 lei (led-box)',
   art='Surse Mean Well 24 V 60 W')
up('M039', 45.50, 57.99, 'https://www.24led.ro/accesorii-banda-led/intrerupator-de-dulap-5-24v-dc-5a-usa.html', 'Întrerupător ușă dulap 5–24 V 45,50 lei (24led); senzor IR 57,99 lei',
   art='Întrerupătoare de ușă / balama 12–24 V (dulap hol 4, dressing 5)')
# ---------------------------------------------------------------- 6. baie
up('M041', 90, 158, 'https://euro-instal.ro/sifon-cada-cu-ventil-automat-si-preaplin-alcadrain-a55km-cromat', 'euro-instal 90 lei; Foglia 158 lei')
up('M042', 454.51 + 261.70, 549 + 320, 'https://www.sanitino.ro/grohe-eurosmart-cosmopolitan-baterie-cada-monocomanda-crom-32831000',
   'Grohe 32831000 454,51 lei (Sanitino) – 549 lei; set Tempesta Cosmopolitan 100 cu bară 261,70 lei (Badabum) – ~320 lei')
up('M043', 1229.99, 1363, 'https://www.esanitare.ro/ceramica-si-mobilier/obiecte-sanitare/rezervoare-si-cadre/rezervor-wc-geberit-duofix-111-300-00-5-incastrat-compatibil-placute-sigma-ajustabil-112-cm-otel-111-300-00-5.html',
   'Geberit Duofix Sigma 111.300.00.5: eSanitare 1.229,99 lei; Bagno 1.363 lei; set ancorare separat dacă nu e inclus', art='Rezervor încastrat Geberit Duofix Sigma 111.300.00.5, 112 cm')
up('M044', 234, 234, DD + 'clapeta-actionare-rezervor-wc-incastrat-geberit-sigma-01-115770115-alb-24-6-x-16-4-cm/p/3015805', 'Dedeman 234 lei',
   art='Clapetă Geberit Sigma01 115.770.11.5, albă')
up('M045', 990, 1281.77, 'https://www.instalplus.ro/vas-wc-suspendat-roca-meridian-rimless-compact', 'Instalplus 990 lei (set cu capac); compari.ro de la 1.281,77 lei')
up('M046', 2083, 2378.27, DD + 'masca-baie-lavoar-roca-gap-new-60-a851476806-cu-sertare-alb-suspendat-60-5-x-46-0-x-53-7-cm/p/3044509',
   'Dedeman 2.378,27 lei; MobMob de la 2.083 lei', art='Mască + lavoar Roca Gap New 60 A851476806, cu sertare, suspendat')
up('M047', 295 + 60, 349 + 120, DD + 'baterie-baie-pentru-lavoar-grohe-eurosmart-33265002/p/3025943',
   'Grohe Eurosmart 33265002 295 lei; cu ventil 349 lei (Dedeman); sifon lavoar estimat 60–120 lei', art='Baterie lavoar Grohe Eurosmart 33265002 + ventil / sifon')
up('M048', 572, 805, 'https://www.neakaisa.ro/paravan-de-cada-mediterraneo-standard-80x140-cm-sticla-securizata.html',
   'Neakaisa: Mediterraneo Standard 80 × 140 572 lei; Super 2 805 lei', art='Paravan cadă Mediterraneo 80 × 140, sticlă securizată')
up('M052', 355 + 105.90, 2 * 355 + 2 * 105.90, DD + 'hidroizolatie-flexibila-impermeabila-ceresit-cl-51-15-kg/p/5015895',
   'Dedeman: CL 51 15 kg 355 lei; bandă CL 152 10 m 105,90 lei; 1–2 seturi după suprafața reală', art='Hidroizolație Ceresit CL 51 15 kg + bandă CL 152 10 m')
up('M053', 4 * 62.49 + 150, 4 * 69.70 + 250, DD + 'placa-gips-carton-tip-h-protectie-umiditate-rigips-rbi-12-5-x-1200-x-2600-mm/p/5006977',
   '4 plăci Rigips RBI 12,5 × 1200 × 2600: 62,49–69,70 lei (Dedeman); profile și trape estimate 150–250 lei', st=E,
   art='Plăci Rigips RBI hidrofuge + profile pentru măști, nișe, trape')
# ---------------------------------------------------------------- 7. incalzire
up('M057', 450, 455, 'https://www.hornbach.ro/shop/Radiator-otel-Purmo-Compact-22-600x1000-mm-incl-accesorii-montaj/5617110/produs.html',
   'Hornbach 455 lei; Brico Depot 450 lei')
up('M058', 549, 558.23, 'https://www.hornbach.ro/p/radiator-otel-purmo-compact-22-600x1200-mm-incl-accesorii-montaj/5775048/', 'Hornbach 549–558,23 lei')
up('M059', 322, 410, 'https://www.instaldepot.ro/calorifer-baie-714-500-purmo-santorini-alb-drept-p1690',
   'Purmo Santorini 500 × 714: 322 lei (Instaldepot) – 410 lei; 500 × 800 nu e mărime standard', art='Portprosop Purmo Santorini 500 × 714 (baie)')
up('M060', 89.99, 103, DD + 'kit-robinet-calorifer-termostatat-robinet-calorifer-retur-cap-termostat-danfoss-ra-fn-ras-c2-rlv-s-alama-1/2/p/2026041',
   'Dedeman: kit Danfoss tur + retur + cap 89,99–103 lei', art='Kit Danfoss: robinet termostatat + retur + cap termostat')
# ---------------------------------------------------------------- 8. placi si atelier
up('M063', 366.42, 470.38, 'https://www.mam-bricolaj.ro/cumpara/pal-melaminat-gri-casmir-u702-st9-2800x2070x18mm-617',
   'Mambricolaj 409,95 lei; Regency 366,42 lei; Mathaus 470,38 lei')
up('M064', 302, 470, 'https://www.mam-bricolaj.ro/cumpara/pal-melaminat-alb-premium-w1000-st9-2800x2070x18mm-7329',
   'Varianta de 16 mm nu apare online; reper prețul W1000 18 mm 302–470 lei. De cerut la Debimax / Mambricolaj', st=E)
up('M065', 126.65, 149, 'https://www.hornbach.ro/conf/placa-hdf-kronospan-2800x2070x3-mm-alb/7615423/', 'Hornbach Kronospan alb 149 lei; Mathaus 126,65 lei',
   art='HDF Kronospan alb 3 mm 2800 × 2070')
up('M066', 295.05, 499, 'https://www.metalcom-shop.ro/placi-decorative/pal-melaminat-egger-stejar-bardolino-natur-h1145-st10-2800x2070x18-mm.html',
   'H1145 ST10 18 mm: 295,05–499 lei la furnizori online')
up('M067', 100, 170, 'https://www.mam-bricolaj.ro/cumpara/debitare-pal-mdf-3555',
   'Tarife: debitare 1,79 lei/ml (Mambricolaj); aplicare cant ABS 2 mm 3,25–7,16 lei/ml + cant. Pe placă ~22 ml tăiere + ~18 ml cant', st=E)
up('M068', 595.29, 797.87, 'https://www.mam-bricolaj.ro/cumpara/blat-bucatarie-stejar-bardolino-natur-h1145-st10-4100x600x38mm-5887',
   'Mambricolaj 659,95 lei; Regency 595,29 lei; Decorum 797,87 lei; cant și decupaje la atelier', art='Blat bucătărie Egger H1145 ST10 4100 × 600 × 38 mm')
up('M069', 202.99, 286, 'https://geamurioglinzi.ro/oglinda-4-mm', 'Oglindă clară 4 mm 202,99–286 lei/m² la furnizori online; folia de siguranță de confirmat în ofertă')
# ---------------------------------------------------------------- 9. feronerie
up('M071', 1280, 1930, 'https://www.feroshop.ro/balamale-mobilier/balama-clip-top-110-usa-aplicata-fara-arc-70t3550-tlmb-v50-ni',
   'Calculat din prețuri verificate: 70T3550 6,77–8,85 lei; 173L6100 0,85–1,00 lei; TIP-ON 956.1004 18,86–26,78 lei; MOVENTO 760H5000S 124–159 lei/pereche; restul estimat',
   st=E)
up('M073', 729.99, 1019, 'https://www.feroshop.ro/feronerie/feronerie-functionala/organizare/dressing/ironfix-sertar-masa-de-calcat-56860710-40384.html',
   'Häfele Ironfix 568.60.710: Feroshop 729,99 lei – 1.019 lei', art='Masă de călcat în sertar Häfele Ironfix 568.60.710')
# ---------------------------------------------------------------- 10. bucatarie
up('M077', 559, 799, DD + 'chiuveta-bucatarie-compozit-granit-casa-blanca-sand-bej-dreptunghiulara-cuva-stanga/-dreapta-76-x-44-cm-adancime-cuva-18-cm/p/3050804',
   'Dedeman: Casa Blanca 76 × 44 559 lei; Paxton Tina 799 lei', art='Chiuvetă compozit 1 cuvă cu picurător 76 × 44')
up('M078', 446.38, 519, 'https://baterii-bucatarie.compari.ro/grohe/30463000-p681805632/', 'Grohe Eurosmart 30463000: 446,38–519 lei',
   art='Baterie bucătărie Grohe Eurosmart 30463000')
up('M079', 396.99, 1446.23, 'https://www.emag.ro/search/hota+60cm', 'eMAG: Heinner HTCH-MD600GBK 630 m³/h 396,99 lei; Electrolux LFP616X 600 m³/h 1.446,23 lei; tipul (incorporabilă) de verificat',
   st=E)
up('M080', 150, 260, DD + 'conector-cu-clapeta-antiretur-vents-3131-pvc-d-150-mm/p/2013908',
   'Conector cu clapetă Vents D150 16,54 lei (Dedeman); cot 150 32,60 lei; tub plat 150 × 70 și adaptoare estimate', st=E)
up('M081', 499 + 300, 499 + 600, 'https://www.ikea.com/ro/ro/p/naesinge-masa-alb-60587535/', 'IKEA NÄSINGE 80 × 60 499 lei; 2 pufuri estimate 150–300 lei',
   st=E, art='Masă IKEA NÄSINGE 80 × 60 + 2 pufuri')
up('M082', 89.90, 113, DD + 'storuri/c/713', 'Dedeman: stor Gardinia Mini Zebra zi-noapte 72,5 × 150: 89,90–113 lei', art='Rulouri zi-noapte Gardinia 72,5 × 150')
# ---------------------------------------------------------------- 11. electrocasnice (pret observat pe eMAG la produsul ales)
EM = 'https://www.emag.ro/'
up('M084', 2499.99, 2899.99, EM + 'side-by-side-tcl-503-l-total-no-frost-compresor-inverter-touch-control-digital-display-dozator-de-apa-aat-technology-iluminat-led-sertar-crisper-multi-air-flow-clasa-e-h-176-cm-gri-quartz-rp503sse1/pd/DZMHTFYBM/',
   'eMAG 2.499,99 lei (preț întreg 2.899,99 lei)')
up('M085', 1379.99, 1500, EM + 'pachet-cuptor-incorporabil-arctic-71-l-electric-6-functii-curatare-cu-abur-grill-timer-clasa-a-plita-incorporabila-gaz-4-arzatoare-aprindere-electrica-wok-60-cm-inox-arse11130xd/pd/D6T897YBM/',
   'eMAG 1.379,99 lei')
up('M086', 716.14, 800, EM + 'cuptor-cu-microunde-incorporabil-heinner-28l-control-digital-900w-putere-grill-1000w-afisaj-led-sticla-neagra-hmw-mdbi28gdbk/pd/DSLRY13BM/',
   'eMAG 716,14 lei')
up('M087', 1448.89, 1689, EM + 'masina-de-spalat-vase-incorporabila-heinner-14-seturi-6-programe-clasa-d-program-rapid-30-program-hygiene-60-cm-hdw-bi6614aid/pd/DK1NKRMBM/',
   'eMAG: Heinner HDW-BI6614AID 1.448,89 lei; Arctic DBI542 1.481,09 lei; Arctic DIN1643 1.689 lei')
up('M088', 1399, 1709.20, EM + 'masina-de-spalat-rufe-heinner-10-kg-1400-rpm-clasa-a-10-motor-inverter-display-digital-program-allergy-steam-alb-hwm-hme1014iva10/pd/DNQK543BM/',
   'eMAG 1.709,20 lei; BricoMix 1.499 lei; compari.ro de la 1.399 lei')
up('M089', 2999.99, 2999.99, EM + 'televizor-tcl-qd-miniled-139-cm-smart-google-tv-4k-ultra-hd-144hz-clasa-e-model-2026-55c6k-pro/pd/DF7JQ32BM/', 'eMAG 2.999,99 lei')
up('M090', 2499.99, 2499.99, EM + 'televizor-tcl-qd-miniled-139-cm-smart-google-tv-4k-ultra-hd-144hz-clasa-f-model-2026-55p8l/pd/D81CPY2BM/', 'eMAG 2.499,99 lei')
up('M091', 184.98, 184.98, EM + 'suport-tv-de-perete-cu-brat-nexio-full-motion-reglabil-32-55-inch-81cm-139cm-capacitate-sustinere-40kg-negru-nx-lpa52-446/pd/DCNGNJYBM/',
   'eMAG 184,98 lei')
# ---------------------------------------------------------------- 12. mobilier si textile
IK = 'https://www.ikea.com/ro/ro/p/'
up('M092', 1999, 2799, IK + 'friheten-canapea-extensibila-3-locuri-faringe-gri-60551225/', 'IKEA FRIHETEN 3 locuri 1.999 lei (Faringe gri) – 2.799 lei (Bomstad); lățime ~230 cm de verificat',
   art='Canapea extensibilă IKEA FRIHETEN 3 locuri')
up('M093', 1699, 2999, IK + 'idanaes-pat-tapitat-cu-depozitare-naggen-bej-30588094/', 'IKEA: GLADSTAD 160 × 200 cu 4 cutii 1.699 lei; IDANÄS cu depozitare 2.999 lei',
   art='Pat tapițat 160 × 200 cu depozitare (IKEA GLADSTAD / IDANÄS)')
up('M094', 999, 1299, IK + 'valevag-saltea-cu-arcuri-impachetate-ferma-bleu-40450680/', 'IKEA: VALEVÅG 999 lei (promoție, 1.299 lei întreg); ÅBYGDA 1.299 lei',
   art='Saltea IKEA VALEVÅG 160 × 200')
up('M096', 399, 699, IK + 'flintan-scaun-rotativ-cu-brate-negru-s89424468/', 'IKEA: FLINTAN cu brațe 399 lei; MARKUS 699 lei', art='Scaun de birou IKEA FLINTAN / MARKUS')
up('M097', 1800, 3500, 'https://www.somproduct.ro/products/masa-de-cafea-din-travertin-si-metal-traverso-bej-alb-o40xh45-cm',
   'Produs la comandă; repere retail travertin 441–1.040 lei pentru măsuțe mai mici', st=E)
up('M098', 249 + 253.41, 449 + 429.99, IK + 'aerende-covor-fir-lung-gri-00576436/', 'IKEA covor 160 × 230: ÄRENDE 249 lei – LOHALS 449 lei; puf rotund 253,41–429,99 lei (eMAG)',
   art='Covor 160 × 230 IKEA + puf rotund ~40 cm')
up('M099', 2 * 249 + 2 * 145 + 200, 2 * 249 + 2 * 145 + 400, IK + 'majgull-draperii-opace-2buc-rjns-gri-80417815/',
   'IKEA MAJGULL opace 2 buc 145 × 300 249 lei × 2; VIDGA set 2 șine tavan 145 lei × 2; voal estimat 200–400 lei', st=E,
   art='Draperii opace IKEA MAJGULL + voal, cu șine VIDGA de tavan (cameră de zi + dormitor)')
up('M101', 235.25, 309.26, 'https://www.emag.ro/uscatoare-rufe1/brand/leifheit/c', 'eMAG: Leifheit Pegasus 200 235,25 lei; Pegasus 200 Deluxe 309,26 lei',
   art='Uscător de rufe Leifheit Pegasus 200, 20 m')

# ---------------------------------------------------------------- recalcul
for r in D['rows']:
    r['tmin'] = round(r['q'] * r['pmin'], 2)
    r['tmax'] = round(r['q'] * r['pmax'], 2)
cats = list(dict.fromkeys(r['cat'] for r in D['rows']))
D['summary'] = [dict(cat=c, tmin=round(sum(r['tmin'] for r in D['rows'] if r['cat'] == c), 2), tmax=round(sum(r['tmax'] for r in D['rows'] if r['cat'] == c), 2),
                     n=sum(1 for r in D['rows'] if r['cat'] == c), ver=sum(1 for r in D['rows'] if r['cat'] == c and r['st'] == V)) for c in cats]
D['old_total'] = [json.loads(BAK.read_text(encoding='utf-8'))[k] for k in ('tot_min', 'tot_max')]
D['tot_min'] = round(sum(s['tmin'] for s in D['summary']), 2)
D['tot_max'] = round(sum(s['tmax'] for s in D['summary']), 2)
D['ver_sum'] = round(sum(r['tmin'] for r in D['rows'] if r['st'] == V), 2)
D['revision'] = 'R02'
note = ('R02: %d din %d linii au preț observat online pe 05.10.2026, cu link la produs; %d au link de reper, dar includ părți estimate; '
        'restul (%d) sunt provizioane fără produs ales (loturi de instalații, consumabile, transport, mobilier la comandă).')
nv = sum(r['st'] == V for r in D['rows']); nl = sum(r['st'] == E and bool(r['url']) for r in D['rows'])
D['notes'] = [n for n in D['notes'] if not n.startswith('R02:')] + [note % (nv, len(D['rows']), nl, len(D['rows']) - nv - nl)]
SRC.write_text(json.dumps(D, ensure_ascii=False, indent=2), encoding='utf-8')

# ---------------------------------------------------------------- Excel
THIN = Side(style='thin', color='C8CCD2'); BR = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD = PatternFill('solid', fgColor='147B73'); VER = PatternFill('solid', fgColor='E7F3F1')
wb = Workbook(); ws = wb.active; ws.title = 'Rezumat'
ws.append(['Deviz materiale R02 – Apartament 184, Bloc L14 (fără manoperă)']); ws['A1'].font = Font(bold=True, size=14, color='147B73')
ws.append(['Lei cu TVA, prețuri observate pe 05.10.2026. „verificat” = preț la produsul ales, cu link; „estimat” = buget de confirmat.']); ws.append([])
ws.append(['Categorie', 'Minim (lei)', 'Maxim (lei)', 'Mediu (lei)', 'Linii', 'Verificate'])
for ci in range(1, 7):
    c = ws.cell(row=4, column=ci); c.font = Font(bold=True, color='FFFFFF'); c.fill = HEAD
first = 5
for s in D['summary']:
    ws.append([s['cat'], s['tmin'], s['tmax'], None, s['n'], s['ver']])
last = ws.max_row
for rr in range(first, last + 1):
    ws.cell(row=rr, column=4, value='=(B%d+C%d)/2' % (rr, rr))
ws.append(['Subtotal', '=SUM(B%d:B%d)' % (first, last), '=SUM(C%d:C%d)' % (first, last), '=SUM(D%d:D%d)' % (first, last)])
sub = ws.max_row
ws.append(['Rezervă neprevăzute', '=B%d*$F$%d' % (sub, sub + 1), '=C%d*$F$%d' % (sub, sub + 1), '=D%d*$F$%d' % (sub, sub + 1), 'procent:', D['rez']])
ws.append(['TOTAL MATERIALE', '=B%d+B%d' % (sub, sub + 1), '=C%d+C%d' % (sub, sub + 1), '=D%d+D%d' % (sub, sub + 1)])
for rr in range(sub, sub + 3):
    ws.cell(row=rr, column=1).font = Font(bold=True)
for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
    for c in row:
        c.border = BR
        if c.column in (2, 3, 4):
            c.number_format = '#,##0'
ws.cell(row=sub + 1, column=6).number_format = '0%'
for col, w in zip('ABCDEF', (52, 14, 14, 14, 9, 11)):
    ws.column_dimensions[col].width = w
ws2 = wb.create_sheet('Deviz detaliat')
hdr = ['ID', 'Categorie', 'Articol', 'Cant.', 'UM', 'Preț min', 'Preț max', 'Total min', 'Total max', 'Status', 'Sursa prețului', 'Link', 'Bază cantitate / notă']
H0 = 5                                   # randul de antet; deasupra sunt totalurile selectiei
n = H0 + len(D['rows'])
PANEL = PatternFill('solid', fgColor='E7F3F1')
ws2['A1'] = 'TOTAL SELECȚIE – se recalculează după filtrele din antet (Categorie, Status etc.)'
ws2['A1'].font = Font(bold=True, size=12, color='147B73')
for rr, lab, f in ((2, 'Fără rezervă', '=SUBTOTAL(109,{c}%d:{c}%d)' % (H0 + 1, n)), (3, 'Cu rezervă %d %%' % (D['rez'] * 100), '={c}2*%s' % (1 + D['rez']))):
    ws2.cell(row=rr, column=3, value=lab).font = Font(bold=True)
    for col in 'HI':
        c = ws2['%s%d' % (col, rr)]; c.value = f.format(c=col); c.number_format = '#,##0'; c.font = Font(bold=True, size=12); c.fill = PANEL; c.border = BR
    ws2['J%d' % rr] = '=(H%d+I%d)/2' % (rr, rr); ws2['J%d' % rr].number_format = '#,##0'; ws2['J%d' % rr].font = Font(bold=True); ws2['J%d' % rr].fill = PANEL
ws2['H1'], ws2['I1'], ws2['J1'] = 'Minim', 'Maxim', 'Mediu'
for col in 'HIJ':
    ws2['%s1' % col].font = Font(bold=True, color='147B73')
ws2['C4'] = 'Linii afișate:'; ws2['D4'] = '=SUBTOTAL(103,A%d:A%d)' % (H0 + 1, n); ws2['C4'].font = Font(bold=True)
for ci, h in enumerate(hdr, start=1):
    c = ws2.cell(row=H0, column=ci, value=h); c.font = Font(bold=True, color='FFFFFF'); c.fill = HEAD; c.alignment = Alignment(wrap_text=True)
for i, r in enumerate(D['rows'], start=H0 + 1):
    for ci, v in enumerate([r['id'], r['cat'], r['art'], r['q'], r['um'], r['pmin'], r['pmax'], '=D%d*F%d' % (i, i), '=D%d*G%d' % (i, i), r['st'],
                            r.get('price_basis', ''), r['url'] or '', r['note']], start=1):
        ws2.cell(row=i, column=ci, value=v)
    if r['url']:
        ws2.cell(row=i, column=12).hyperlink = r['url']; ws2.cell(row=i, column=12).value = 'deschide'; ws2.cell(row=i, column=12).font = Font(color='277DBA', underline='single')
    for ci in range(1, len(hdr) + 1):
        c = ws2.cell(row=i, column=ci); c.border = BR; c.alignment = Alignment(wrap_text=True, vertical='top')
        if ci in (6, 7, 8, 9):
            c.number_format = '#,##0.00'
        if r['st'] == V:
            c.fill = VER
ws2.auto_filter.ref = 'A%d:M%d' % (H0, n)
for col, w in zip('ABCDEFGHIJKLM', (7, 22, 52, 7, 7, 10, 10, 12, 12, 10, 50, 10, 50)):
    ws2.column_dimensions[col].width = w
ws2.freeze_panes = 'D%d' % (H0 + 1)
ws3 = wb.create_sheet('Opționale')
ws3.append(['Articol', 'Cant.', 'UM', 'Preț min', 'Preț max', 'Notă'])
for o in D['opt']:
    ws3.append(list(o))
try:
    wb.save(ROOT / 'Deviz_materiale_ap184_R02.xlsx')
except PermissionError:                     # fisierul e deschis in Excel: salveaza o copie cu ora in nume
    import datetime
    alt = ROOT / ('Deviz_materiale_ap184_R02_%s.xlsx' % datetime.datetime.now().strftime('%H%M'))
    wb.save(alt); print('Excel deschis: salvat ca', alt.name)
st = collections.Counter(r['st'] for r in D['rows'])
print('R02', dict(st), 'cu link:', sum(bool(r['url']) for r in D['rows']))
print('subtotal %.0f – %.0f | cu rezerva %.0f – %.0f | R01 %.0f – %.0f' % (D['tot_min'], D['tot_max'], D['tot_min'] * (1 + D['rez']), D['tot_max'] * (1 + D['rez']), *D['old_total']))
for s in D['summary']:
    print('%-45s %9.0f %9.0f  %d/%d' % (s['cat'], s['tmin'], s['tmax'], s['ver'], s['n']))
