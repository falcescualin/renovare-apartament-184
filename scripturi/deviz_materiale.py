"""Deviz estimativ de MATERIALE (fara manopera) pentru renovarea si mobilarea ap. 184.
Preturi in lei cu TVA, octombrie 2026: 'verificat' = pret gasit online pe 05.10.2026 la produsul ales;
'estimat' = interval de piata pentru produs inca neales. Cantitatile vin din model / planurile R01-R02.
Iese: Deviz_materiale_ap184.xlsx + tmp/deviz.json (pentru raportul PDF)."""
import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
V, E = 'verificat', 'estimat'
# (categorie, articol, cantitate, UM, pret_min, pret_max, status, sursa / nota)
R = []


def add(cat, art, q, um, pmin, pmax, st, note=''):
    R.append(dict(cat=cat, art=art, q=q, um=um, pmin=pmin, pmax=pmax, st=st, note=note))


# ---------------------------------------------------------------- 1. pardoseli si sape
C = '1. Șapă și pardoseli'
add(C, 'Amorsă pentru șapă (Ceresit CN 94 / echivalent), 10 l', 2, 'buc', 110, 160, E, 'pentru ~44 m² interior')
add(C, 'Șapă autonivelantă 25 kg (Ceresit DA / CN 68), ~5 mm medie pe 44 m²', 16, 'sac', 63, 87, V, 'Dedeman 69,90–86,99 lei; Vasion 62,94 lei')
add(C, 'Parchet stejar triplustratificat 13–14 mm, cameră de zi + dormitor (30,2 m² + 8 %)', 33, 'm²', 129, 175, V, 'Dedeman: Diana Forest / Tarkett 129–175 lei/m²')
add(C, 'Folie / subparchet 2 mm cu barieră de vapori', 33, 'm²', 10, 22, E, '')
add(C, 'Plintă (MDF albă de vopsit / stejar) + accesorii', 42, 'ml', 15, 32, E, 'perimetru cameră de zi + dormitor fără goluri')
add(C, 'Microciment: hol, vestibul, baie pardoseală (10,6 m²) + pereți umezi baie (~12 m²)', 23, 'm²', 137, 190, V, 'kit 10 m² 1.368 lei; varianta impermeabilă 1.899 lei (cementart.ro)')
add(C, 'Rășină / vopsea epoxidică gri cu amorsă: bucătărie, debara, balcon (15,1 m²)', 15, 'm²', 45, 110, E, 'variantă simplă: 2 straturi; autonivelantă 2 mm e spre maximul intervalului')
add(C, 'Praguri aluminiu periat 10 mm (U1, U3, U4, U5, U8)', 5, 'buc', 40, 90, E, '')
# ---------------------------------------------------------------- 2. pereti, tavane, finisaje
C = '2. Pereți, tavane, finisaje'
add(C, 'Glet de finisaj (gips) 20 kg, reparații și finisare', 8, 'sac', 45, 70, E, '~180 m² pereți + 49 m² tavane, local')
add(C, 'Amorsă / grund pentru vopsea, 10 l', 3, 'buc', 90, 160, E, '')
add(C, 'Vopsea lavabilă premium albă / alb cald 15 l (2 straturi)', 3, 'buc', 300, 480, E, 'pereți + tavane ≈ 230 m²')
add(C, 'Vopsea lavabilă rezistentă la umiditate (bucătărie, baie fără microciment), 5 l', 1, 'buc', 120, 220, E, '')
add(C, 'Colțare, plasă, bandă, șmirghel, silicon acrilic, folie protecție', 1, 'lot', 400, 800, E, '')
add(C, 'Baghete poliuretan perete TV cameră de zi (~30 ml) + adeziv', 30, 'ml', 18, 40, E, 'se vopsesc în culoarea peretelui')
add(C, 'Panouri riflaje stejar pe pâslă, dormitor (~1,5 × 2,5 m)', 3, 'buc', 330, 600, E, 'panouri acustice 2400–2600 × 600; decupaj modul TV')
# ---------------------------------------------------------------- 3. electrice curenti tari
C = '3. Instalație electrică'
add(C, 'Cablu 3 × 1,5 mm² (iluminat + comenzi)', 110, 'm', 4.5, 7, E, 'plan electric R02, E17: 77 m + 28 m comenzi')
add(C, 'Cablu 3 × 2,5 mm² (prize, circuite dedicate)', 170, 'm', 7, 10, E, 'plan electric R02, E17: ~159 m + rezervă')
add(C, 'Tub flexibil / canal cablu, doze aparat, doze derivație J01–J06', 1, 'lot', 600, 1100, E, '')
add(C, 'Prize Schuko cu ramă (gamă medie Schneider / Legrand)', 35, 'buc', 22, 40, E, 'IE01: 35 mecanisme')
add(C, 'Întrerupătoare (6 simple + 2 duble) cu ramă', 8, 'buc', 30, 60, E, 'IE02')
add(C, 'Tablou ~54 module + separator, SPD, bare N/PE', 1, 'set', 450, 900, E, 'IE05, IE07')
add(C, 'RCBO 1P+N 30 mA tip A (3 × B10 + 9 × B16)', 12, 'buc', 95, 170, E, 'IE06')
add(C, 'AFDD pentru C01 / C04', 2, 'buc', 300, 600, E, 'Ordin 959/2023')
add(C, 'Borne, etichete, cleme, accesorii', 1, 'lot', 200, 400, E, 'IE10')
# ---------------------------------------------------------------- 4. curenti slabi
C = '4. Internet și TV (curenți slabi)'
add(C, 'Cablu Cat6 cupru integral', 52, 'm', 2.5, 5, E, 'ISL01')
add(C, 'Prize RJ45 Cat6 + patch-panel 8 porturi + patch-corduri', 1, 'set', 250, 500, E, 'ISL02, ISL05')
add(C, 'Cablu coaxial 75 Ω + 3 prize TV + distribuitor', 1, 'set', 150, 300, E, 'ISL03')
add(C, 'Switch 8 porturi (ONT / router de la operator)', 1, 'buc', 100, 200, E, 'ISL04')
# ---------------------------------------------------------------- 5. iluminat si LED
C = '5. Iluminat și LED'
add(C, 'Plafoniere LED slim 3000 K (8 încăperi; baie și balcon IP44)', 8, 'buc', 90, 260, E, 'IE03')
add(C, 'Aplice liniare verticale negre, perete TV', 2, 'buc', 150, 400, E, '')
add(C, 'Bandă LED 24 V, 4000 K / alb cald, CRI > 90', 45, 'm', 12, 30, E, 'dulap hol, dressing, debara, bucătărie, comode TV, riflaje, oglindă, noptiere')
add(C, 'Profil aluminiu + difuzor opal', 40, 'm', 20, 40, E, '')
add(C, 'Surse 24 V (30–100 W)', 7, 'buc', 80, 220, E, 'hol, dressing, debara, bucătărie, TV cameră de zi, dormitor, noptiere')
add(C, 'Întrerupătoare de balama / senzori ușă 24 V', 9, 'buc', 25, 60, E, 'dulap hol 4 + dressing 5')
# ---------------------------------------------------------------- 6. sanitare si baie
C = '6. Baie și instalații sanitare'
add(C, 'Cadă Roca Contesa 150 × 70, oțel emailat + kit susținere', 1, 'buc', 856, 1050, V, 'Dedeman 855,93 lei; absulo 842 lei')
add(C, 'Sifon cadă + preaplin (Alcadrain A55KM)', 1, 'buc', 120, 250, E, 'IS03')
add(C, 'Baterie cadă-duș Grohe Eurosmart Cosmopolitan 32831000 + set pară Tempesta', 1, 'set', 650, 1000, E, 'IS04, IS05')
add(C, 'Rezervor încastrat Geberit Duofix Sigma 112 cm + set ancorare', 1, 'set', 1100, 1500, E, 'IS06, Dedeman (prețul exact de verificat)')
add(C, 'Clapetă Geberit Sigma', 1, 'buc', 150, 350, E, 'IS07')
add(C, 'Vas WC suspendat Roca Meridian compact Rimless + capac soft-close', 1, 'set', 800, 1200, E, 'IS08, IS09')
add(C, 'Lavoar + mobilier 60 cm (Roca The Gap)', 1, 'set', 1200, 2100, E, 'IS10')
add(C, 'Baterie lavoar Grohe Eurosmart Cosmopolitan + ventil / sifon', 1, 'set', 400, 650, E, 'IS11, IS12')
add(C, 'Paravan cadă rabatabil ~80 × 140 cm (Radaway)', 1, 'buc', 600, 1300, E, 'IS13')
add(C, 'Robineți colțar, racorduri flexibile, izolare AR / AC', 1, 'lot', 120, 250, E, 'IS14–IS16')
add(C, 'Țevi și fitinguri apă (sistem unic) + izolație', 1, 'lot', 400, 900, E, 'IS17, IS18 — după releveu')
add(C, 'Canalizare PP Ø40 / 50 / 110, coturi, ramificații', 1, 'lot', 200, 450, E, 'IS19–IS21')
add(C, 'Hidroizolație Ceresit CL 51 + bandă CL 152 + colțuri / manșete', 1, 'lot', 400, 750, E, 'IS25–IS27')
add(C, 'Plăci hidrofuge Knauf / Aquapanel + profile pentru măști, nișe, trape', 1, 'lot', 400, 800, E, 'IS23, IS24')
add(C, 'Oglindă baie + accesorii (port-prosop, suport hârtie, cârlige)', 1, 'set', 300, 700, E, '')
# ---------------------------------------------------------------- 7. incalzire
C = '7. Încălzire'
add(C, 'Radiator Purmo Compact 22, 600 × 1000 (dormitor) cu accesorii', 1, 'buc', 450, 580, V, 'Hornbach 455 lei; Brico Depot 450 lei')
add(C, 'Radiator Purmo Compact 22, 600 × 1200 (cameră de zi) cu accesorii', 1, 'buc', 520, 680, E, '')
add(C, 'Portprosop Purmo Santorini ~500 × 800 (baie)', 1, 'buc', 300, 650, E, 'IT03')
add(C, 'Robinet termostatic + cap + detentor (set Danfoss)', 3, 'set', 120, 250, E, 'IT05, IT06')
add(C, 'Țevi, fitinguri, olandeze, aerisitoare', 1, 'lot', 200, 500, E, 'IT07–IT09 — după releveu')
# ---------------------------------------------------------------- 8. mobilier custom - placi si atelier
C = '8. Mobilier la comandă – plăci și atelier'
add(C, 'PAL Egger W1000 ST9 18 mm 2800 × 2070', 16, 'placă', 302, 470, V, '11 plăci din planul de debitare + ~5 pentru corpurile bucătăriei; Mambricolaj 389,95 lei')
add(C, 'PAL Egger U702 ST9 18 mm 2800 × 2070 (fronturi)', 6, 'placă', 380, 560, E, '5 din planul de debitare + 1 rezervă bucătărie')
add(C, 'PAL Egger W1000 ST9 16 mm (cutii de sertar)', 2, 'placă', 280, 420, E, '')
add(C, 'HDF alb 3 mm 2800 × 2070 (spate)', 6, 'placă', 70, 120, E, '4 din planul de debitare + 2 bucătărie')
add(C, 'PAL Egger H1145 ST10 stejar 18 mm (comode, machiaj)', 1, 'placă', 420, 620, E, 'sau rest de la atelier')
add(C, 'Debitare, cant ABS 2 / 0,8 mm, găurire CNC (taxe atelier)', 31, 'placă', 100, 170, E, 'serviciu atelier, nu manoperă de montaj; se confirmă în oferta Debimax / Mambricolaj')
add(C, 'Blat bucătărie Egger H1145 38 mm, 4100 × 600 + cant + decupaje', 1, 'buc', 700, 1100, E, '')
add(C, 'Oglinzi 4 mm cu folie: dulap hol (8 uși, ~4,3 m²) + machiaj 80 × 174', 5.7, 'm²', 150, 260, E, 'sticlărie')
add(C, 'Protecție perete bucătărie (sticlă / panou compact)', 1, 'buc', 300, 800, E, 'materialul nu e ales')
# ---------------------------------------------------------------- 9. feronerie
C = '9. Feronerie Blum și accesorii mobilier'
add(C, 'Dulap hol: balamale CLIP top, plăcuțe, TIP-ON, MOVENTO + TIP-ON BLUMOTION, confirmat, picioare, bare', 1, 'set', 1500, 2100, V, 'balama 70T3550 6,8–8,9 lei; MOVENTO 760H5000S 124–159 lei/pereche')
add(C, 'Dressing: ~30 balamale, 10 TIP-ON, 6 sertare interioare MOVENTO, bare', 1, 'set', 2200, 3200, E, '')
add(C, 'Masă de călcat incorporată în dressing', 1, 'buc', 800, 1600, E, 'tip Ironfix / echivalent')
add(C, 'Bucătărie: balamale, sertare, push / mânere, picioare, coș gunoi, picurător', 1, 'set', 1800, 3000, E, '')
add(C, 'Spălătorie: sertar coșuri + poliță extractibilă MOVENTO, balamale; platformă metalică mașină', 1, 'set', 1000, 1900, E, 'platforma se dimensionează separat')
add(C, 'Noptiere, comode TV, machiaj, dulap WC, debara: glisiere, balamale, suporți rafturi', 1, 'set', 900, 1500, E, '')
# ---------------------------------------------------------------- 10. bucatarie: echipare
C = '10. Bucătărie – echipare'
add(C, 'Chiuvetă compozit 1 cuvă cu picurător', 1, 'buc', 400, 900, E, '')
add(C, 'Baterie bucătărie', 1, 'buc', 250, 600, E, '')
add(C, 'Hotă incorporabilă / grup filtrant 60 cm, ≥ 600 m³/h', 1, 'buc', 500, 1100, E, 'încă neleasă')
add(C, 'Tub plat 150 × 70, coturi, clapetă anti-retur', 1, 'set', 150, 300, E, '')
add(C, 'Masă 80 × 60 + 2 pufuri / scaune', 1, 'set', 500, 1100, E, '')
add(C, 'Rulouri textile filtrante bucătărie', 2, 'buc', 120, 250, E, '')
# ---------------------------------------------------------------- 11. electrocasnice si TV
C = '11. Electrocasnice și TV'
add(C, 'Frigider side-by-side TCL RP503SSE1', 1, 'buc', 2500, 2900, V, 'eMAG 2.499,99 lei (preț întreg 2.899,99)')
add(C, 'Pachet cuptor Arctic ARSE11130XD + plită gaz Arctic', 1, 'buc', 1380, 1500, V, 'eMAG 1.379,99 lei')
add(C, 'Microunde incorporabil Heinner HMW-MDBI28GDBK', 1, 'buc', 716, 800, V, 'eMAG 716,14 lei')
add(C, 'Mașină de spălat vase incorporabilă 60 cm (Arctic DBI542 / Heinner HDW-BI6614AID)', 1, 'buc', 1450, 1700, V, 'eMAG 1.448,89–1.689 lei; modelul nu e ales')
add(C, 'Mașină de spălat rufe Heinner HWM-HME1014IVA10+++', 1, 'buc', 1400, 1710, V, '1.399–1.709 lei (compari.ro, eMAG)')
add(C, 'Televizor TCL 55C6K Pro (cameră de zi)', 1, 'buc', 3000, 3000, V, 'eMAG 2.999,99 lei')
add(C, 'Televizor TCL 55P8L (dormitor)', 1, 'buc', 2500, 2500, V, 'eMAG 2.499,99 lei')
add(C, 'Suport TV Nexio NX-LPA52-446', 2, 'buc', 185, 185, V, 'eMAG 184,98 lei')
# ---------------------------------------------------------------- 12. mobilier gata facut si textile
C = '12. Mobilier și textile'
add(C, 'Canapea extensibilă 220 cm', 1, 'buc', 2500, 4500, E, '')
add(C, 'Pat 160 × 200 cu ladă', 1, 'buc', 1800, 3500, E, '')
add(C, 'Saltea 160 × 200', 1, 'buc', 1200, 2500, E, '')
add(C, 'Birou IKEA TROTTEN reglabil electric, alb, 120 × 70', 1, 'buc', 999, 999, V, 'IKEA 999 lei')
add(C, 'Scaun de birou ergonomic', 1, 'buc', 400, 900, E, '')
add(C, 'Măsuțe de cafea: travertin oval 110 × 65 + stejar Ø60 (comandă)', 1, 'set', 1800, 3500, E, '')
add(C, 'Puf bouclé Ø40 + covor cameră de zi', 1, 'set', 500, 1100, E, '')
add(C, 'Draperii blackout + voal, cameră de zi și dormitor, cu șine de tavan', 1, 'set', 1200, 2500, E, '')
add(C, 'Lenjerie, perne, pătură decorativă (pentru închiriere)', 1, 'set', 400, 900, E, '')
add(C, 'Uscător de rufe pliabil, balcon', 1, 'buc', 150, 300, E, '')
# ---------------------------------------------------------------- 13. diverse
C = '13. Diverse și rezervă'
add(C, 'Consumabile (burghie, discuri, bandă, saci moloz, protecții)', 1, 'lot', 500, 1000, E, '')
add(C, 'Transport materiale și livrări', 1, 'lot', 600, 1200, E, '')

OPT = [('Uși interioare noi (U1–U8) cu toc și feronerie', 8, 'buc', 600, 1300, 'nu e decis dacă se schimbă'),
       ('Soundbar cameră de zi', 1, 'buc', 500, 1500, 'TCL 55C6K Pro are deja Onkyo 2.1'),
       ('Aer condiționat (o unitate 12000 BTU)', 1, 'buc', 1800, 3000, 'întrebare deschisă')]

for r in R:
    r['tmin'] = round(r['q'] * r['pmin'], 2)
    r['tmax'] = round(r['q'] * r['pmax'], 2)
cats = []
for r in R:
    if r['cat'] not in cats:
        cats.append(r['cat'])
summary = [dict(cat=c, tmin=sum(r['tmin'] for r in R if r['cat'] == c), tmax=sum(r['tmax'] for r in R if r['cat'] == c),
                n=sum(1 for r in R if r['cat'] == c), ver=sum(1 for r in R if r['cat'] == c and r['st'] == V)) for c in cats]
tot_min, tot_max = sum(s['tmin'] for s in summary), sum(s['tmax'] for s in summary)
REZ = 0.07
out = dict(rows=R, summary=summary, tot_min=tot_min, tot_max=tot_max, rez=REZ, opt=OPT,
           ver_sum=sum(r['tmin'] for r in R if r['st'] == V))
(ROOT / 'tmp/deviz.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')

# ---------------------------------------------------------------- Excel
THIN = Side(style='thin', color='C8CCD2'); BR = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD = PatternFill('solid', fgColor='147B73'); ZEB = PatternFill('solid', fgColor='F2F5F8'); VER = PatternFill('solid', fgColor='E7F3F1')
wb = Workbook(); ws = wb.active; ws.title = 'Rezumat'
ws.append(['Deviz materiale – Apartament 184, Bloc L14 (fără manoperă)']); ws['A1'].font = Font(bold=True, size=14, color='147B73')
ws.append(['Prețuri cu TVA, lei, 05.10.2026. „verificat” = preț găsit online la produsul ales; „estimat” = interval de piață.']); ws.append([])
ws.append(['Categorie', 'Minim (lei)', 'Maxim (lei)', 'Mediu (lei)', 'Linii', 'Din care verificate'])
for cidx in range(1, 7):
    c = ws.cell(row=4, column=cidx); c.font = Font(bold=True, color='FFFFFF'); c.fill = HEAD; c.border = BR
for s in summary:
    ws.append([s['cat'], round(s['tmin']), round(s['tmax']), round((s['tmin'] + s['tmax']) / 2), s['n'], s['ver']])
ws.append(['Subtotal', round(tot_min), round(tot_max), round((tot_min + tot_max) / 2)])
ws.append(['Rezervă neprevăzute %d %%' % (REZ * 100), round(tot_min * REZ), round(tot_max * REZ), round((tot_min + tot_max) / 2 * REZ)])
ws.append(['TOTAL MATERIALE', round(tot_min * (1 + REZ)), round(tot_max * (1 + REZ)), round((tot_min + tot_max) / 2 * (1 + REZ))])
for rr in range(ws.max_row - 2, ws.max_row + 1):
    for cidx in range(1, 5):
        ws.cell(row=rr, column=cidx).font = Font(bold=True)
for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
    for c in row:
        c.border = BR
        if c.column in (2, 3, 4):
            c.number_format = '#,##0'
for col, w in zip('ABCDEF', (52, 14, 14, 14, 8, 18)):
    ws.column_dimensions[col].width = w
ws2 = wb.create_sheet('Deviz detaliat')
hdr = ['Categorie', 'Articol', 'Cant.', 'UM', 'Preț unitar min', 'Preț unitar max', 'Total min', 'Total max', 'Status', 'Sursă / notă']
ws2.append(hdr)
for cidx in range(1, len(hdr) + 1):
    c = ws2.cell(row=1, column=cidx); c.font = Font(bold=True, color='FFFFFF'); c.fill = HEAD; c.border = BR; c.alignment = Alignment(wrap_text=True, vertical='center')
for i, r in enumerate(R, start=2):
    ws2.append([r['cat'], r['art'], r['q'], r['um'], r['pmin'], r['pmax'], '=C%d*E%d' % (i, i), '=C%d*F%d' % (i, i), r['st'], r['note']])
    for cidx in range(1, len(hdr) + 1):
        c = ws2.cell(row=i, column=cidx); c.border = BR; c.alignment = Alignment(wrap_text=True, vertical='top')
        if cidx in (5, 6, 7, 8):
            c.number_format = '#,##0.00'
        if r['st'] == V:
            c.fill = VER
n = len(R) + 1
ws2.append(['', 'TOTAL (fără rezervă)', '', '', '', '', '=SUM(G2:G%d)' % n, '=SUM(H2:H%d)' % n])
for cidx in (2, 7, 8):
    ws2.cell(row=n + 1, column=cidx).font = Font(bold=True); ws2.cell(row=n + 1, column=cidx).number_format = '#,##0'
for col, w in zip('ABCDEFGHIJ', (30, 62, 8, 7, 12, 12, 12, 12, 10, 60)):
    ws2.column_dimensions[col].width = w
ws2.freeze_panes = 'C2'
ws3 = wb.create_sheet('Opționale (în afara totalului)')
ws3.append(['Articol', 'Cant.', 'UM', 'Preț min', 'Preț max', 'Notă'])
for o in OPT:
    ws3.append(list(o))
for col, w in zip('ABCDEF', (52, 8, 7, 12, 12, 40)):
    ws3.column_dimensions[col].width = w
fn = ROOT / 'Deviz_materiale_ap184.xlsx'
wb.save(fn)
print('XLSX', fn)
print('SUBTOTAL %.0f – %.0f | cu rezerva %.0f – %.0f' % (tot_min, tot_max, tot_min * (1 + REZ), tot_max * (1 + REZ)))
for s in summary:
    print('%-45s %9.0f %9.0f' % (s['cat'], s['tmin'], s['tmax']))
