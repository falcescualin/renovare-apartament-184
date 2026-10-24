"""Instructiuni de montaj pas cu pas (stil IKEA) pentru dulapul din hol, in stilul planselor A3 ale proiectului.
R02: fiecare piesa are eticheta (folie) legata de placa din planul de debitare; fiecare pas are pagina de imbinari
R03: pagina de cumparaturi cu preturi (M04b, deviz R03), senzori de usa IR pentru LED, trimiteri la planurile R02/R03
(unde intra confirmatele, cepii, pinii, placutele Blum) si tabel cu feroneria.
Ruleaza (Python cu reportlab): dulap_hol_montaj_pdf.py   | imagini: dulap_hol_pasi_blender.py | placi: optimizare_debitare.py
Iese: output/pdf/Apartament_184_Dulap_hol_montaj_R03.pdf"""
from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripturi'))
from plan_comun import patch_prefix, DVR
prefix = (ROOT / 'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
prefix = prefix.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'", "OUT=ROOT/'output/pdf/Apartament_184_Dulap_hol_montaj_R03.pdf'")
prefix = prefix.replace("'R01 | 05.10.2026 | COORDONARE ȘI OFERTARE - NU PLAN DE EXECUȚIE VALIDAT'", "'R03 | 05.10.2026 | DULAP HOL – INSTRUCȚIUNI DE MONTAJ | COTE ÎN MM'")
exec(patch_prefix(prefix))
c.setTitle('Apartament 184 - Dulap hol - instructiuni de montaj - R03')
data_src = (ROOT / 'scripturi/excel_debitare.py').read_text(encoding='utf-8').split('THIN = Side')[0]
D = {}
exec(data_src, D)
P, G = D['P'], D['G']
IMG = ROOT / 'tmp/dulap_hol_pasi'
ANC = json.loads((IMG / 'ancore.json').read_text())
LAY = json.loads((ROOT / 'tmp/debitare_layout.json').read_text(encoding='utf-8'))['A']
PALE = HexColor('#e7f3f1'); WARN = HexColor('#fbeee9'); HWC = HexColor('#c27a2c')
SC = {'W1000 18 mm': 'W18', 'U702 18 mm': 'U18', 'W1000 16 mm': 'W16', 'HDF 3 mm': 'HDF'}
PCS = {p[0]: p for p in P}

# ---------------------------------------------------------------- etichete (folii): piesa -> placa din planul de debitare
SHEET = {}
for m, r in LAY.items():
    for i, sh in enumerate(r['sheets'], 1):
        for p in sh:
            for t in (p['inst'].split('+') if '+' in p['inst'] else [p['inst']]):
                t = t if t.startswith('C09') else t
                SHEET[t if '.' in t or t[:3] != 'C09' else t] = '%s-%d' % (SC[m], i)
for a, b in (('C09.1', 'C09.1+2'), ('C09.2', 'C09.1+2'), ('C09.3', 'C09.3+4'), ('C09.4', 'C09.3+4')):
    for m, r in LAY.items():
        for i, sh in enumerate(r['sheets'], 1):
            if any(p['inst'] == b for p in sh):
                SHEET[a] = '%s-%d' % (SC[m], i)
STEP_OF = {'C03': '1', 'C01': '2', 'C02': '2', 'C05': '3', 'C06': '3', 'C07': '4', 'C08': '4', 'C04': '5', 'H01': '6', 'H02': '6', 'C09': '7',
           'C10': '8', 'F05': '8', 'S01': '9a', 'S02': '9a', 'S03': '9a', 'S04': '9a', 'S05': '9a', 'F03': '9', 'F04': '9', 'F01': '11', 'F02': '12', 'F06': '13'}
INST = []
for p in P:
    for i in range(p[6]):
        INST.append(('%s.%d' % (p[0], i + 1)) if p[6] > 1 else p[0])


def tags(code):
    return [t for t in INST if t.split('.')[0] == code]


def where(t):
    return SHEET.get(t, '?')


OBJTAG = {'Baza': 'C03', 'Lateral_stanga': 'C01', 'Lateral_oblic': 'C02', 'Despartitor_central': 'C05', 'Despartitor_3': 'C06',
          'Polita_sertare_A': 'C07.1', 'Polita_sus_A': 'C07.2', 'Polita_sertare_B': 'C08.1', 'Polita_sus_B': 'C08.2', 'Blat_sus': 'C04',
          'Spate_HDF': 'H01 + H02', 'Soclu': 'C10', 'Plinta_colt': 'F05', 'Front_sertar_A': 'F03', 'Front_sertar_B': 'F04', 'Masca_tavan': 'F06',
          'Sertar_pantofi_A': 'sertar 1', 'Sertar_pantofi_B': 'sertar 2'}
for i in range(1, 5):
    OBJTAG['Raft_colt_%d' % i] = 'C09.%d' % i
    OBJTAG['Usa_oglinda_%d' % i] = 'F01.%d' % i
    OBJTAG['Usa_sus_oglinda_%d' % i] = 'F02.%d' % i
HWTAG = {'Picior': 'F', 'Bara_haine': 'U', 'LED_profil': 'X', 'Senzor_usa': 'X', 'Sursa_LED': 'X'}

# ---------------------------------------------------------------- feronerie cu litere
HW = {
    'A': ('Confirmat 7 × 50 (ericson)', '50', '44 folosite + 6 rezervă'),
    'B': ('Capac confirmat alb', '50', ''),
    'C': ('Cep lemn Ø8 × 35', '4', ''),
    'D': ('Colțar metalic 40 × 40', '10', ''),
    'E': ('Colțar anti-răsturnare + diblu 8 × 60 + șurub 5 × 60', '3', 'obligatoriu'),
    'F': ('Picior reglabil soclu 80–100 mm', '10', ''),
    'G': ('Clemă soclu', '5', ''),
    'H': ('Pin raft Ø5', '16', ''),
    'I': ('Șurub PAL 4 × 16', '250', '234 folosite + rezervă'),
    'J': ('Șurub PAL 4 × 30', '20', ''),
    'K': ('Șurub PAL 4 × 40', '12', ''),
    'L': ('Șurub 3,5 × 16 sau capse', '80', 'spate HDF'),
    'M': ('Blum 70T3550 balama CLIP top, aplicată, fără arc', '6', 'ușile F01.1 / F02.1'),
    'N': ('Blum 70T3650 balama CLIP top, semiaplicată, fără arc*', '18', 'celelalte uși'),
    'O': ('Blum 173L6100 plăcuță 0 mm, cruce', '24', ''),
    'P': ('Blum 956.1004 TIP-ON uși + adaptor drept*', '8', ''),
    'Q': ('Blum 760H5000S glisieră MOVENTO, NL 500', '2 perechi', ''),
    'R': ('Blum TIP-ON BLUMOTION pentru MOVENTO*', '2 seturi', ''),
    'S': ('Blum sincronizare TIP-ON BLUMOTION*', '2', 'tăiată 750 / 760 mm'),
    'T': ('Blum cleme cuplare front MOVENTO*', '2 perechi', ''),
    'U': ('Bară ovală aluminiu 30 × 15 + 4 suporți', '1015 + 1025 mm', ''),
    'V': ('Oglindă 4 mm cu folie: 1695 × 515 / 373 × 515', '4 + 4', 'de la sticlărie'),
    'W': ('Silicon neutru pentru oglinzi', '2 tuburi', ''),
    'X': ('LED: profil 1 m ×2, bandă 24 V 4000 K 2 m, senzor de ușă IR 24 V ×4, sursă 24 V', '1 set', 'senzorii lângă balamaua de sus a ușilor mari'),
}


def img(name, x, y, w, h):
    c.drawImage(str(IMG / name), x, H - y - h, w, h, mask='auto', preserveAspectRatio=True, anchor='c')


def pill(x, y, s, col=TEAL, size=10):
    w = pdfmetrics.stringWidth(s, 'SegoeB', size) + 12
    c.setFillColor(col); c.setStrokeColor(white); c.setLineWidth(1.2)
    c.roundRect(x - w / 2, H - y - size * .7, w, size * 1.6, size * .8, stroke=1, fill=1)
    c.setFillColor(white); c.setFont('SegoeB', size); c.drawCentredString(x, H - y - size * .3 + 1, s)


def hwdot(x, y, s, size=10):
    c.setFillColor(HWC); c.setStrokeColor(white); c.setLineWidth(1.2); c.circle(x, H - y, size * .9, stroke=1, fill=1)
    c.setFillColor(white); c.setFont('SegoeB', size); c.drawCentredString(x, H - y - size * .35, s)


def callouts(step, box=(52, 150, 620, 580), iw=1800, ih=1500):
    bx, by, bw, bh = box
    s = min(bw / iw, bh / ih); dw, dh = iw * s, ih * s; ox, oy = bx + (bw - dw) / 2, by + (bh - dh) / 2
    done = set()
    for k, (u, v) in ANC.get(step, {}).items():
        X, Y = ox + u * dw, oy + (1 - v) * dh
        if k in OBJTAG:
            if OBJTAG[k] in done:
                continue
            done.add(OBJTAG[k]); pill(X, Y, OBJTAG[k])
        else:
            h = next((v2 for k2, v2 in HWTAG.items() if k.startswith(k2)), None)
            if h and h not in done:
                done.add(h); hwdot(X, Y, h)


# ---------------------------------------------------------------- desen fata de panou cu gauri
SYM = {'A': ('Confirmat Ø7 (ericson)', RED), 'A2': ('Confirmat Ø7, montat din partea cealaltă', HexColor('#7a3fa0')), 'C': ('Cep Ø8', BLUE),
       'H': ('Pin raft Ø5', INK), 'O': ('Plăcuță balama Blum, 2 găuri Ø5', TEAL), 'D': ('Colțar 40 × 40', HWC), 'F': ('Picior reglabil', MUT),
       'L': ('Șurub HDF', MUT), 'E': ('Colțar anti-răsturnare', RED), 'Q': ('Glisieră MOVENTO', BLUE)}


def mark(x, y, kind):
    col = SYM[kind][1]
    if kind in ('A', 'A2'):
        circle(x, y, 3.6, col, white); line(x - 2.5, y, x + 2.5, y, col, .8); line(x, y - 2.5, x, y + 2.5, col, .8)
    elif kind == 'C':
        poly([(x, y - 4), (x + 4, y), (x, y + 4), (x - 4, y)], fill=col, color=col)
    elif kind == 'H':
        circle(x, y, 2, col, col)
    elif kind == 'O':
        circle(x, y, 2.2, col, col)
    elif kind == 'D':
        poly([(x - 4, y + 4), (x - 4, y - 4), (x + 4, y - 4)], color=col, lw=1.6, close=False)
    elif kind in ('F', 'E'):
        rect(x - 3.5, y - 3.5, 7, 7, fill=col, stroke=col)
    elif kind == 'L':
        circle(x, y, 1.1, col, col)


def face(x0, y0, k, W, Hh, holes, title, sub='', dims=True):
    """fata unui panou: X = de la muchia din fata (stanga desenului), Y = de la muchia de jos (in sus)"""
    rect(x0, y0, W * k, Hh * k, fill=HexColor('#f4f6f7'), stroke=INK, lw=.7)
    line(x0, y0, x0, y0 + Hh * k, TEAL, 2.2)                 # muchia din fata (cu cant)
    txt(x0, y0 - 18, title, 10, INK, True)
    if sub:
        txt(x0, y0 - 6, sub, 8, MUT)
    for X, Y, kind in holes:
        mark(x0 + X * k, y0 + (Hh - Y) * k, kind)
    if dims:
        dim(x0, y0 + Hh * k, x0 + W * k, y0 + Hh * k, str(W), 14)
        dim(x0 + W * k, y0, x0 + W * k, y0 + Hh * k, str(Hh), 12)
    return x0 + W * k


def gh(piece, typ, facec=None, cond=None, kind='A'):
    out = []
    for g in G:
        if g[0] == piece and typ in g[2] and (facec is None or facec in g[1]):
            X, Y = g[5], g[6]
            if not isinstance(X, (int, float)) or not isinstance(Y, (int, float)):
                continue
            if cond is None or cond(X, Y):
                out.append((X, Y, kind))
    return out


def legend(x, y, kinds):
    for kd in kinds:
        mark(x + 4, y - 3, kd); txt(x + 14, y, SYM[kd][0], 9, MUT); y += 15
    return y


def trapez_plan(x0, y0, k, holes, title, sub=''):
    """baza/blat vazute de sus: fata jos, capatul C01 in stanga, capatul oblic in dreapta (2417 fata / 2267 spate)"""
    pts = [(x0, y0), (x0 + 2267 * k, y0), (x0 + 2417 * k, y0 + 580 * k), (x0, y0 + 580 * k)]
    poly(pts, fill=HexColor('#f4f6f7'), color=INK, lw=.7)
    line(x0, y0 + 580 * k, x0 + 2417 * k, y0 + 580 * k, TEAL, 2.2)
    txt(x0, y0 - 18, title, 10, INK, True)
    if sub:
        txt(x0, y0 - 6, sub, 8, MUT)
    txt(x0 + 4, y0 + 580 * k + 26, 'C01', 9, TEAL, True); txt(x0 + 2417 * k - 40, y0 + 580 * k + 26, 'oblic C02', 9, TEAL, True)
    for X, Y, kind in holes:        # X de la capatul C01, Y de la fata
        mark(x0 + X * k, y0 + (580 - Y) * k, kind)
    dim(x0, y0 + 580 * k, x0 + 2417 * k, y0 + 580 * k, '2417 față / 2267 spate', 30)


# ---------------------------------------------------------------- M00 coperta
start('M00', 'Dulap hol – instrucțiuni de montaj', 'R03: piese etichetate după planul de debitare R02 | îmbinări și feronerie Blum la fiecare pas | cumpărături cu prețuri (M04b)')
for i, (t, v, s) in enumerate([('PIESE', '%d piese' % len(INST), 'fiecare cu folie: cod + placa din planul de debitare'),
                               ('UȘI', '8 uși oglindă', '4 jos + 4 sus, push-to-open TIP-ON'),
                               ('ECHIPĂ', '2 persoane', 'aproximativ 1,5 zile, montaj în picioare')]):
    x = 42 + i * 182
    rect(x, 150, 172, 100, fill=LIGHT, stroke=GRAY, lw=.6)
    txt(x + 14, 175, t, 10, TEAL, True); txt(x + 14, 210, v, 20, INK, True); para(x + 14, 222, 150, s, 9)
y = 280
y = panel(42, y, 530, 'Cum se citesc instrucțiunile',
          'Fiecare pas are două pagini. Prima: imaginea dulapului văzut din hol, cu <b>piesele noi colorate turcoaz și etichetate</b> '
          '(eticheta turcoaz = piesa, cercul portocaliu = feronerie), ce îți trebuie și acțiunile numerotate. '
          'A doua: <b>îmbinările</b> – desenul fețelor de panou cu fiecare gaură (ericsoane, cepi, pini, plăcuțe Blum) și tabelul cu feroneria pasului.') + 16
y = panel(42, y, 530, 'Etichete (folii)',
          'Fiecare piesă primește la debitare o folie cu eticheta ei (paginile M05–M06): <b>C07.1 · placa W18-3 · pasul 4</b>. '
          'Placa (W18-3 = W1000 18 mm, placa 3) e cea din Planul de debitare R02, așa că știi exact din ce placă vine fiecare piesă.') + 16
y = panel(42, y, 530, 'Orientare',
          'Desenele 3D arată dulapul din hol: <b>C01 (capătul dinspre camera de zi) apare în dreapta imaginilor</b>, C02 (oblic) în stânga. '
          'Ușile se numerotează de la C01: F01.1 / F02.1 lângă C01, F01.4 / F02.4 lângă colț.')
img('pas_final.png', 600, 130, 560, 640)
end()

# ---------------------------------------------------------------- M01 inainte sa incepi
start('M01', 'Înainte să începi', 'Verificări pe șantier, unelte și reguli de siguranță')
y = panel(42, 150, 540, 'Verificări obligatorii',
          '1. Înălțimea finită a tavanului în hol trebuie să fie <b>≥ 2480 mm</b> pe toată lungimea dulapului (corp 2460 mm + mască ajustabilă).<br/>'
          '2. Pardoseala (microciment) este gata și curată; picioarele reglabile preiau 0–20 mm denivelare.<br/>'
          '3. Doza de 230 V pentru sursa LED e montată în perete la <b>2400 mm</b>, în dreptul modulului dinspre C01.<br/>'
          '4. Peretele din spate este verificat pentru diblu 8 × 60 (colțarele anti-răsturnare).<br/>'
          '5. Fiecare piesă are folia lipită și se potrivește cu lista M02–M03.') + 16
y = panel(42, y, 540, 'De ce se montează în picioare, departe de perete',
          'Holul are ~1,8 m lățime: dulapul nu se poate asambla culcat și ridica. Se montează în picioare, '
          'cu spatele la <b>~60 cm de perete</b>, ca spatele HDF să poată fi prins din spate (pasul 6). Apoi se împinge la perete pe cartoane. '
          'Lateralele (2380 × 580) se pot ridica: diagonala lor e 2450 mm, sub tavan.') + 16
y = panel(42, y, 540, 'De coordonat cu electricul',
          'Planul electric R03: punctul NET (X 7900, Z 2000) cade <b>în spatele dulapului, în modulul dinspre C01</b>. Ușile cu oglindă atenuează Wi-Fi: '
          'ONT-ul poate sta în dulap, cu acces, dar routerul rămâne afară. Se decide până la electricul brut (13–21.10); dacă rămâne în spate, se decupează H01 și se lasă acces și aerisire.', RED)
yy = panel(610, 150, 538, 'Unelte',
           'Autofiletantă cu bit PZ2 · cheie hexagonală 4 mm pentru confirmat · burghiu în trepte pentru confirmat (Ø5 / Ø7) · burghiu Ø8 · '
           'burghiu beton Ø8 · nivelă 1 m și 2 m · ruletă · șablon de găurire confirmat · 2 scări · 2 cleme · ciocan de cauciuc · pistol de silicon · cartoane.') + 16
yy = panel(610, yy, 538, 'Ce e un confirmat (ericson)',
           'Șurub de mobilă 7 × 50 cu cap hexagonal: trece prin gaura Ø7 din panoul lateral și se înșurubează în gaura Ø5 × 45 din cantul piesei care vine perpendicular. '
           'Toate găurile sunt date de atelier, în afară de cele din cantul oblic (C03 / C04), pe care le dai tu cu șablonul. Strânge ferm, fără să rupi PAL-ul.') + 16
table(610, yy, [90, 448], [['Simbol', 'Înseamnă'], ['eticheta turcoaz', 'piesă (cod + număr), ex. C07.1'], ['cerc portocaliu', 'feronerie / accesoriu, literele A–X de la M04'],
                           ['W18-3', 'placa din planul de debitare: W1000 18 mm, placa 3'], ['*', 'cod Blum de confirmat la dealer înainte de comandă']], 10)
end()


# ---------------------------------------------------------------- M02–M03 lista pieselor (cu placa)
def piece_rows(codes):
    rows = [['Cod', 'Denumire', 'L × l × gros.', 'Buc.', 'Material', 'Cant L1 / L2 / l1 / l2', 'Etichete → placă', 'Pas']]
    for k in codes:
        p = PCS[k]
        tg = tags(k)
        pl = sorted({where(t) for t in tg})
        rows.append([p[0], p[1], '%d × %d × %d' % (p[4], p[5], p[3]), str(p[6]), p[2].replace('Egger ', '').replace(' Premium White', '').replace(' Cashmere Grey', ''),
                     ' / '.join(p[7:11]), '%s → <b>%s</b>' % (', '.join(tg), ', '.join(pl)), STEP_OF[k]])
    return rows


WID = [40, 175, 105, 36, 90, 130, 460, 70]
start('M02', 'Lista pieselor – corp și fronturi', 'Dimensiuni finite cu cant inclus | fiecare etichetă arată placa din planul de debitare')
table(42, 145, WID, piece_rows([k for k in PCS if k[0] in 'CF']), 9)
end()
start('M03', 'Lista pieselor – sertare și spate', 'Sertare din W1000 16 mm, spate HDF alb 3 mm')
y = table(42, 145, WID, piece_rows([k for k in PCS if k[0] in 'SH']), 9) + 24
y0 = y
panel(42, y, 540, 'Forme speciale',
      '<b>C03 / C04</b> (bază, blat): trapez, față 2417 mm, spate 2267 mm.<br/>'
      '<b>C09</b>: se taie în perechi (C09.1+2, C09.3+4) dintr-un dreptunghi 577 × 525, apoi oblic: față 337, spate 188.<br/>'
      '<b>F06</b> (mască): latura de sus se ajustează pe tavan la montaj (pasul 13).')
panel(610, y0, 538, 'Plăcile', 'W18-1…3 = Egger W1000 ST9 18 mm · U18-1…2 = Egger U702 ST9 18 mm · W16-1 = W1000 16 mm · HDF-1…2 = HDF alb 3 mm. '
      'Hărțile de tăiere sunt în Apartament_184_Plan_debitare_R02.pdf, cu aceleași etichete.')
end()

# ---------------------------------------------------------------- M04 feronerie
start('M04', 'Feronerie și accesorii', 'Literele A–X apar în fiecare pas | * = cod Blum de confirmat la dealer')
items = list(HW.items())
for col_i, chunk in enumerate((items[:12], items[12:])):
    rows = [['', 'Denumire', 'Total', 'Notă']] + [[k, v[0], v[1], v[2]] for k, v in chunk]
    table(42 + col_i * 562, 145, [34, 330, 78, 102], rows, 9)
end()
# ---------------------------------------------------------------- M04b cumparaturi (deviz R03)
start('M04b', 'Cumpărături – feronerie, oglinzi și LED', 'Cantitățile de la M04 la cel mai mic preț găsit pe 05.10.2026 (deviz R03); prețuri cu TVA; * = cod de confirmat la dealer')
U71 = DVR['M071']['url']
BUY = [('A', 'Confirmat 7 × 50', 50, 0.0995, 'cel mai mic preț găsit', ''), ('B', 'Capac confirmat alb', 50, 0.0524, 'cel mai mic preț găsit', ''),
       ('C', 'Cep lemn Ø8 × 35', 4, 0.05, 'cel mai mic preț găsit', ''), ('D', 'Colțar metalic 40 × 40', 10, 1.0, 'estimat', ''),
       ('E', 'Colțar anti-răsturnare + diblu 8 × 60 + șurub', 3, 5.0, 'estimat', ''), ('F', 'Picior reglabil soclu H100', 10, 1.25, 'cel mai mic preț găsit', ''),
       ('G', 'Clemă soclu', 5, 2.0, 'estimat', ''), ('H', 'Pin raft Ø5', 16, 0.10, 'estimat', ''),
       ('I–L', 'Șuruburi PAL 4 × 16, 4 × 30, 4 × 40, 3,5 × 16 (cutii de 100)', 4, 8.0, 'estimat', ''),
       ('M', 'Blum 70T3550 CLIP top aplicată, fără arc', 6, 6.77, 'Feromob', U71), ('N', 'Blum 70T3650 CLIP top semiaplicată, fără arc*', 18, 7.50, 'cel mai mic preț găsit', ''),
       ('O', 'Blum 173L6100 plăcuță cruce 0 mm', 24, 0.85, 'AccesoriiPentruMobilier', ''), ('P', 'Blum TIP-ON 956.1004 + adaptor drept*', 8, 22.86, 'Darel 18,86 lei + adaptor ~4 lei', ''),
       ('Q', 'Blum MOVENTO 760H5000S, NL 500 (pereche)', 2, 124.25, 'Triton', ''), ('R', 'Blum TIP-ON BLUMOTION S1 pentru MOVENTO*', 2, 85.83, 'cel mai mic preț găsit', ''),
       ('S', 'Blum bară de sincronizare*', 2, 17.24, 'cel mai mic preț găsit', ''), ('T', 'Blum cleme de cuplare MOVENTO* (pereche)', 2, 6.0, 'estimat', ''),
       ('U', 'Bară ovală 1 m + 2 suporți', 2, 6.11 + 2 * 0.76, 'cel mai mic preț găsit', ''),
       ('V', 'Oglindă 4 mm cu folie de siguranță, ~4,3 m² (8 uși)', 4.3, 202.99, 'geamurioglinzi.ro', DVR['M069']['url']),
       ('W', 'Silicon neutru pentru oglinzi', 2, 25.0, 'estimat', ''),
       ('X', 'Profil LED aplicat 2 m cu difuzor opal (tăiat 2 × 1 m)', 1, 41.0, 'smartego.ro', DVR['M037']['url']),
       ('X', 'Bandă LED COB 24 V CRI90, rolă 5 m (folosești 2 m)', 1, 85.0, 'DVB Design', DVR['M036']['url']),
       ('X', 'Senzor de ușă IR 5–24 V DC 5 A, autoadeziv', 4, 45.50, '24led', DVR['M039']['url']),
       ('X', 'Sursă Mean Well LPV-60-24, 24 V 60 W', 1, 79.0, 'led-box', DVR['M038']['url'])]
rows = [['', 'Articol', 'Cant.', 'Preț unitar', 'Total lei', 'Unde']]
for k, art, q, pu, st, url in BUY:
    rows.append(['<b>%s</b>' % k, esc(art), ('%g' % q).replace('.', ','), lei2(pu), lei2(q * pu),
                 ('<link href="%s" color="#277dba"><u>%s</u></link>' % (_html.escape(url), esc(st))) if url else esc(st)])
fer = sum(q * pu for k, _, q, pu, _, _ in BUY if k not in ('V', 'W', 'X'))
tot = sum(q * pu for _, _, q, pu, _, _ in BUY)
rows.append(['', '<b>Total dulap hol: feronerie, oglinzi și LED</b>', '', '', '<b>' + lei(tot) + '</b>', 'feroneria A–U: %s lei (deviz M071)' % lei2(fer)])
y = tbl(42, 145, [40, 430, 60, 80, 80, 416], rows, 9, 3, total=True) + 14
para(42, y, 540, '<b>Senzorul de ușă</b><br/>Blum nu are întrerupător de balama în gamă, iar în magazinele din România am găsit senzori de ușă IR, care se lipesc pe corp. '
     'Funcția e aceeași: LED-ul se aprinde când se deschide ușa. Senzorul nu apasă pe ușă, deci nu încurcă deschiderea TIP-ON. '
     'Verifică în fișa lui că două ieșiri se pot lega în paralel; altfel, alternativa e un senzor pentru uși duble (LED Solution, ~52 lei), câte unul pe modul.', 10)
para(620, y, 528, '<b>Ce mai trebuie</b><br/>Plăcile, debitarea, cantul și găurirea sunt în planul de debitare R02 (lot comun cu celelalte corpuri). '
     'Oglinzile se comandă la sticlărie pe dimensiunile de la V (1695 × 515 ×4, 373 × 515 ×4), cu folie de siguranță pe spate. '
     'Cablul de 230 V până la doza de deasupra dulapului e în planul electric R03 (F04).', 10)
end()

# ---------------------------------------------------------------- M05–M06 folii
LW, LH = 262, 98
lab = list(INST)
for pg in range(0, len(lab), 24):
    start('M%02d' % (5 + pg // 24), 'Folii de etichetare (%d / %d)' % (pg // 24 + 1, -(-len(lab) // 24)),
          'Se printează pe hârtie autocolantă și se lipesc pe fața nevăzută a piesei, imediat după debitare | linia groasă = muchie cu cant 2 mm, subțire = 0,8 mm')
    for j, t in enumerate(lab[pg:pg + 24]):
        x0, y0 = 42 + (j % 4) * (LW + 12), 140 + (j // 4) * (LH + 8)
        p = PCS[t.split('.')[0]]
        rect(x0, y0, LW, LH, fill=white, stroke=GRAY, lw=.6)
        rect(x0, y0, 8, LH, fill=TEAL, stroke=TEAL)
        txt(x0 + 16, y0 + 26, t, 20, INK, True)
        txt(x0 + 16, y0 + 44, p[1][:34], 9, MUT)
        txt(x0 + 16, y0 + 60, '%d × %d × %d mm' % (p[4], p[5], p[3]), 10, INK, True)
        txt(x0 + 16, y0 + 76, p[2].replace('Egger ', ''), 8, MUT)
        txt(x0 + 16, y0 + 90, 'placa %s · pasul %s' % (where(t), STEP_OF[p[0]]), 9, TEAL, True)
        # mini schita cant: L1 jos (fata), L2 sus, l1 stanga, l2 dreapta
        bx, by, bw, bh = x0 + LW - 80, y0 + 18, 64, 40
        rect(bx, by, bw, bh, fill=LIGHT, stroke=GRAY, lw=.4)
        for val, (a, b2, cc, d2) in zip(p[7:11], ((bx, by + bh, bx + bw, by + bh), (bx, by, bx + bw, by), (bx, by, bx, by + bh), (bx + bw, by, bx + bw, by + bh))):
            if val != '-':
                line(a, b2, cc, d2, INK, 2.6 if val.startswith('2') else 1.2)
        txt(bx, by + bh + 12, 'L1 = jos', 7, MUT)
    end()

# ---------------------------------------------------------------- pasi
K15 = 72 / 25.4 / 15
K10 = 72 / 25.4 / 10


def det_none():
    pass


def det_01():
    legs = [(x, y, 'F') for x in (45, 585, 1135, 1685, 2205) for y in (120, 490)]
    trapez_plan(60, 200, K15, legs, 'C03 – baza văzută de dedesubt', 'fața în jos, capătul C01 în stânga')
    trapez_plan(60, 420, K15, [(x, y, 'C') for x in (1026, 2071) for y in (100, 480)], 'C03 – baza văzută de sus (pentru pasul 3)', 'găurile Ø8 × 12 pentru cepi')
    legend(60, 640, ['F', 'C'])


def det_02():
    x = face(70, 190, K15, 580, 2380, gh('C01', 'Confirmat (față)', cond=lambda X, Y: Y < 100), 'C01 – fața interioară', 'X de la față, Y de la jos')
    x = face(x + 90, 190, K15, 599, 2380, gh('C02', 'Confirmat (față)', cond=lambda X, Y: Y < 100), 'C02 – fața interioară')
    txt(x + 70, 200, 'Găuri folosite acum:', 10, INK, True)
    para(x + 70, 210, 230, 'C01: Ø7 la 9 mm de jos, la 50 / 290 / 530 mm de față.<br/>C02: Ø7 la 9 mm de jos, la 50 / 300 / 549 mm.<br/><br/>'
         'În bază (C03): Ø5 × 45 în cantul drept la 50 / 290 / 530 mm (atelier) și în cantul oblic la 50 / 300 / 549 mm (tu, cu șablonul).', 10)
    legend(x + 70, 420, ['A'])


def det_03():
    holes = [(x, y, 'C') for x in (1026, 2071) for y in (100, 480)] + [(1026 - 30, 550, 'D'), (2071 + 30, 550, 'D')]
    trapez_plan(60, 200, K15, holes, 'C03 – baza văzută de sus', 'C05 la 1026 mm, C06 la 2071 mm de capătul C01 (axe)')
    face(60, 420, K15 * 1.4, 577, 18, [], 'C05 / C06 – cantul de jos', 'Ø8 × 25 la 100 și 480 mm de față', dims=False)
    for X in (100, 480):
        mark(60 + X * K15 * 1.4, 420 + 9 * K15 * 1.4, 'C')
    legend(60, 480, ['C', 'D'])


def det_04():
    cond = lambda X, Y: 200 < Y < 2100
    x = face(70, 190, K15, 580, 2380, gh('C01', 'Confirmat poliță', cond=cond), 'C01 – interior', 'spre C07')
    x = face(x + 70, 190, K15, 577, 2344, gh('C05', 'Confirmat poliță stânga') + gh('C05', 'Confirmat poliță dreapta', kind='A2'), 'C05 – ambele fețe')
    x = face(x + 70, 190, K15, 577, 2344, gh('C06', 'Confirmat poliță dreapta'), 'C06 – fața spre C08')
    para(70, 665, 660, '<b>C07</b> (modulul dinspre C01): muchia de jos a polițelor la 360 și 2080 mm de pardoseală. '
         'Confirmatele C01 → C07 la 289 / 2009 mm de jos ale lui C01.<br/><br/>'
         '<b>C05</b> e găurit străpuns pe ambele seturi: <font color="#c64937">roșu</font> (73 / 527 mm) se înșurubează <b>din modulul dinspre colț</b> în C07; '
         '<font color="#7a3fa0">mov</font> (123 / 477 mm) se înșurubează <b>din modulul dinspre C01</b> în C08. Decalajul le ferește să se lovească.', 10)
    legend(x + 40, 200, ['A', 'A2'])


def det_05():
    x = face(70, 190, K15, 580, 2380, gh('C01', 'Confirmat (față)', cond=lambda X, Y: Y > 2000), 'C01 – interior')
    x = face(x + 90, 190, K15, 599, 2380, gh('C02', 'Confirmat (față)', cond=lambda X, Y: Y > 2000), 'C02 – interior')
    trapez_plan(x + 70, 230, K15 * .7, [(1026 - 30, 50, 'D'), (1026 - 30, 530, 'D'), (2071 + 30, 50, 'D'), (2071 + 30, 530, 'D')],
                'C04 – blatul văzut de jos', 'colțare lângă C05 și C06')
    legend(x + 70, 420, ['A', 'D'])


def det_06():
    k = 72 / 25.4 / 20
    x0, y0 = 70, 190
    Wb, Hb = 2417, 2362
    rect(x0, y0, Wb * k, Hb * k, fill=HexColor('#f1efe9'), stroke=INK)
    txt(x0, y0 - 18, 'Vedere din spate (C01 în DREAPTA)', 10, INK, True)
    split = Wb - 1044
    line(x0 + split * k, y0, x0 + split * k, y0 + Hb * k, RED, 1.2, [4, 2])
    txt(x0 + split * k / 2 - 14, y0 + 20, 'H02', 12, INK, True); txt(x0 + (split + 522) * k - 14, y0 + 20, 'H01', 12, INK, True)
    for X in [i * 150 for i in range(0, 17)] + [Wb]:
        for Y in (8, Hb - 8):
            mark(x0 + min(X, Wb - 8) * k, y0 + Y * k, 'L')
    for Y in [i * 150 for i in range(0, 16)]:
        for X in (8, Wb - 8, Wb - 1035, Wb - 2071 + 9):
            mark(x0 + X * k, y0 + (Hb - Y) * k, 'L')
    for X in (Wb - 100, Wb - 1035, 120):
        mark(x0 + X * k, y0 + 10, 'E')
    dim(x0, y0 + Hb * k, x0 + Wb * k, y0 + Hb * k, '2417', 14)
    legend(x0 + Wb * k + 40, 220, ['L', 'E'])
    para(x0 + Wb * k + 40, 260, 300, 'Îmbinarea H01 / H02 cade pe despărțitorul central C05 (linia roșie). Șuruburi la 150 mm pe contur, pe C05 și pe C06. '
         'Colțarele anti-răsturnare E: sus, sub blat, la C01, la C05 și la capătul oblic.', 10)


def det_07():
    x = face(70, 190, K15, 599, 2380, gh('C02', 'Pin raft', kind='H'), 'C02 – interior')
    x = face(x + 90, 190, K15, 577, 2344, gh('C06', 'Pin raft', kind='H'), 'C06 – fața spre colț')
    para(x + 60, 190, 260, 'Pini Ø5 × 10: în C02 la 60 / 540 mm de față, în C06 la 60 / 517 mm. '
         'Înălțimi: C02 413 / 813 / 1213 / 1613 mm de la muchia de jos a lui C02; C06 395 / 795 / 1195 / 1595 mm. Toate rafturile ajung la aceeași cotă (500 / 900 / 1300 / 1700 mm de la pardoseală).', 10)
    legend(x + 60, 330, ['H'])


def det_09():
    k = K15
    x = 70
    for nm, W, Hh, yb in (('C01 – interior', 580, 2380, 18), ('C05 – fața spre modulul C01', 577, 2344, 0), ('C05 – fața spre colț', 577, 2344, 0), ('C06 – fața spre C08', 577, 2344, 0)):
        face(x, 190, k, W, Hh, [], nm, dims=False)
        rect(x + 3 * k, 190 + (Hh - yb - 30) * k, 500 * k, 30 * k, fill=BLUE, stroke=BLUE)
        x += W * k + 50
    para(70, 680, 640, 'Glisierele Q stau direct pe bază (la 18 mm de muchia de jos a lui C01, la 0 mm pe C05 / C06), retrase 3 mm de la față, cu 3 șuruburi I prin găurile lor. '
         'Folosește șablonul Blum pentru glisiere. În spatele cutiei, cârligul glisierei intră în gaura Ø6 din S02 / S03.', 10)
    legend(70, 660, ['Q'])


def det_11(upper=False):
    cond = (lambda X, Y: Y > 1950) if upper else (lambda X, Y: Y < 1950)
    x = 70
    for nm, piece, typ, fc, W, Hh in (('C01 – ușa F0x.1', 'C01', 'Plăcuță', None, 580, 2380), ('C05 – ușa .2 (modul C01)', 'C05', 'Plăcuță', 'stânga', 577, 2344),
                                     ('C05 – ușa .3 (decalată)', 'C05', 'Plăcuță', 'dreapta', 577, 2344), ('C06 – ușa .4', 'C06', 'Plăcuță', None, 577, 2344)):
        x = face(x, 190, K15, W, Hh, gh(piece, typ, fc, cond, 'O'), nm.replace('F0x', 'F02' if upper else 'F01'), dims=False) + 45
    para(70, 680, 640, 'Plăcuțele O pe linia de 37 mm de la față, câte 2 găuri Ø5 × 11 la ± 16 mm. Pe C05 cele două rânduri sunt decalate (ușa 2 / ușa 3), '
         'ca plăcuțele să nu se suprapună. Cotele exacte sunt în foaia „Găurire” din Excel și pe pagina P11a.' + ('' if upper else ' Senzorul de ușă X se lipește pe corp, lângă balamaua de sus a fiecărei uși mari.'), 10)
    legend(70, 660, ['O'])


STEPS = [
    ('01', 'Baza pe picioare', ['C03'], 'PZ2, nivelă, ruletă',
     ['Așază baza C03 cu fața de jos în sus, pe un carton. Capătul oblic e spre ușa de intrare.',
      'Înșurubează cele 10 picioare F (4 șuruburi I fiecare) în pozițiile din desen.',
      'Întoarce baza pe picioare, la ~60 cm de perete. Reglează picioarele la 80 mm și pune-o la nivel pe lung și pe lat.'],
     'Nivelul bazei decide cum se închid ușile. Verifică de două ori.',
     [('F', 'Picior reglabil soclu 80–100 mm', 10, 'sub C03: rândul din față la 120 mm de muchie, cel din spate la 490 mm; pe lungime la 45 / 585 / 1135 / 1685 / 2205 mm de capătul C01'),
      ('I', 'Șurub PAL 4 × 16', 40, '4 la fiecare picior')], det_01),
    ('02', 'Lateralele', ['C01', 'C02'], 'cheie hex 4 mm, șablon confirmat, burghiu în trepte Ø5/Ø7',
     ['Ridicați C01 în picioare (2 persoane) la capătul drept al bazei, cu muchia cu cant de 2 mm în față.',
      'Prinde-l cu 3 confirmat A prin găurile Ø7 de jos, în cantul bazei.',
      'Dă cele 3 găuri Ø5 × 45 din cantul oblic al bazei cu șablonul și prinde C02 cu 3 confirmat A.',
      'Ține lateralele vertical cu o șipcă prinsă provizoriu între ele, sus, până la pasul 5.'],
     'Lateralele nu stau singure: nu le lăsa nesusținute.',
     [('A', 'Confirmat 7 × 50 (ericson)', 6, '3 prin C01 + 3 prin C02, în găurile Ø7 de la 9 mm de jos, în cantul bazei (Ø5 × 45)'),
      ('—', 'Șablon de găurire confirmat', 1, 'găurile din cantul oblic al bazei: 50 / 300 / 549 mm de la față')], det_02),
    ('03', 'Despărțitoarele', ['C05', 'C06'], 'ciocan de cauciuc, aracet, nivelă',
     ['Pune aracet în cele 4 găuri Ø8 din bază și bate cepii C.',
      'Așază C05 pe cepii de la 1026 mm de capătul C01 și C06 pe cei de la 2071 mm.',
      'Prinde fiecare despărțitor de bază, în spate, cu un colțar D.',
      'Verifică vertical cu nivela și susține-le provizoriu sus.'],
     'C05 și C06 au aceeași formă, dar sunt găurite diferit: verifică folia.',
     [('C', 'Cep lemn Ø8 × 35', 4, 'Ø8 × 12 în bază și Ø8 × 25 în cantul de jos al C05 / C06, la 100 și 480 mm de față'),
      ('D', 'Colțar metalic 40 × 40', 2, 'jos, în spate, unul la C05 și unul la C06'), ('I', 'Șurub PAL 4 × 16', 8, '4 la fiecare colțar')], det_03),
    ('04', 'Polițele fixe', ['C07', 'C08'], 'cheie hex 4 mm, nivelă',
     ['Polițele de jos (C07.1, C08.1) au muchia de jos la 360 mm de pardoseală; cele de sus (C07.2, C08.2) la 2080 mm.',
      'C07: prin C01 și prin C05 (din modulul dinspre colț), câte 2 confirmat A la fiecare capăt.',
      'C08: prin C05 (din modulul dinspre C01) și prin C06 (din colț), câte 2 confirmat A.',
      'Muchia din față a polițelor e retrasă 20 mm față de laterale.'],
     'Polițele rigidizează corpul: după ele scoate susținerile provizorii.',
     [('A', 'Confirmat 7 × 50 (ericson)', 16, 'C01 → C07: 4 · C05 → C07: 4 · C05 → C08: 4 · C06 → C08: 4 (vezi desenul pentru cote)')], det_04),
    ('05', 'Blatul de sus', ['C04'], '2 scări, cheie hex 4 mm, șablon confirmat',
     ['Sub tavan rămân ~20 mm: doi oameni pe scări împing blatul din față, orizontal, peste despărțitoare, până în spate.',
      'Prinde C01 de blat cu 3 confirmat A, prin găurile de sus.',
      'Dă găurile din cantul oblic al blatului cu șablonul (50 / 300 / 549 mm) și prinde C02 cu 3 confirmat A.',
      'Prinde C05 și C06 de blat cu câte 2 colțare D (față și spate).'],
     'Nu împinge corpul cât lucrezi pe scări.',
     [('A', 'Confirmat 7 × 50 (ericson)', 6, 'C01 → C04: 3 la 2371 mm de jos (50 / 290 / 530) · C02 → C04: 3 (50 / 300 / 549)'),
      ('D', 'Colțar metalic 40 × 40', 4, 'sub blat, lângă C05 și C06, la 50 mm de față și de spate'), ('I', 'Șurub PAL 4 × 16', 16, '4 la fiecare colțar')], det_05),
    ('06', 'Diagonale, spate HDF, la perete', ['H01', 'H02'], 'ruletă, autofiletantă, bormașină cu Ø8 beton',
     ['Măsoară diagonalele pe față la ambele module: diferență maximă 2 mm.',
      'Decupează în H01 golul pentru doza de 230 V (2400 mm) și, dacă e cazul, pentru router.',
      'Din spate, prinde H01 și H02 cu șuruburi L la 150 mm pe contur, pe C05 și pe C06.',
      'Împingeți dulapul la perete pe cartoane, scoateți cartoanele, refaceți nivelul.',
      'Montează 3 colțare E sub blat, prinse în perete cu diblu 8 × 60.'],
     'Colțarele anti-răsturnare sunt obligatorii înainte de uși și de încărcare.',
     [('L', 'Șurub 3,5 × 16 sau capse', 80, 'la 150 mm pe contur, pe C05 și C06'),
      ('E', 'Colțar anti-răsturnare + diblu 8 × 60 + șurub 5 × 60', 3, 'sub C04, lângă spate: la C01, la C05, la capătul oblic'),
      ('I', 'Șurub PAL 4 × 16', 6, '2 la fiecare colțar E, în blat')], det_06),
    ('07', 'Rafturile din colț', ['C09'], '—',
     ['Introdu pinii H în C02 și C06 (câte 4 pe raft).',
      'Așază rafturile trapez C09.1 – C09.4 cu latura de 337 mm în față, de jos în sus.'], '',
     [('H', 'Pin raft Ø5', 16, 'C02: la 60 / 540 mm de față · C06: la 60 / 517 mm (înălțimi în desen)')], det_07),
    ('08', 'Soclul și plinta din colț', ['C10', 'F05'], 'adeziv de montaj, distanțier 10 mm',
     ['Prinde clemele G pe cele 5 picioare din rândul din față.',
      'Apasă soclul C10 pe cleme, cu muchia cu cant de 0,8 mm în jos. Soclul rămâne retras ~40 mm.',
      'Lipește plinta F05 pe cantul bazei, sub raftul de colț, aliniată cu fronturile, la 10 mm de pardoseală.'], '',
     [('G', 'Clemă soclu', 5, 'pe picioarele din rândul din față'), ('—', 'Adeziv de montaj', 1, 'plinta F05 pe cantul bazei C03')], det_none),
]
STEPS2 = [
    ('09', 'Sertarele: glisiere și fronturi', ['F03', 'F04'], 'PZ2, șablon Blum pentru glisiere, ferăstrău pentru metal',
     ['Asamblează întâi cutiile de sertar (pagina 9a).',
      'Montează glisierele Q pe bază, pe C01 / C05 (sertarul 1) și C05 / C06 (sertarul 2).',
      'Clipsează TIP-ON BLUMOTION R și bara de sincronizare S (750 / 760 mm).',
      'Agață cutiile: cârligul din spate în gaura din S02 / S03, în față clemele T.',
      'Prinde F03 / F04 din interior cu câte 4 șuruburi J: 10 mm deasupra pardoselii, rost 3 mm sub uși.'],
     'Codurile marcate * se confirmă la dealer: lungimea sincronizării depinde de setul ales.',
     [('Q', 'Blum 760H5000S MOVENTO BLUMOTION S, NL 500, 40 kg', '2 perechi', 'pe bază, pe C01 / C05 și C05 / C06, retrase 3 mm, 3 șuruburi I fiecare'),
      ('R', 'Blum TIP-ON BLUMOTION pentru MOVENTO*', '2 seturi', 'clipsat pe glisieră, în spate'),
      ('S', 'Blum bară de sincronizare*', 2, 'între unitățile TIP-ON: 750 mm (sertar 1), 760 mm (sertar 2)'),
      ('T', 'Blum cleme de cuplare MOVENTO*', '2 perechi', 'sub fața interioară a cutiei, stânga / dreapta, 2 șuruburi I'),
      ('I', 'Șurub PAL 4 × 16', 20, '12 la glisiere + 8 la cleme'), ('J', 'Șurub PAL 4 × 30', 8, '4 prin S02 / S03 în fiecare front')], det_09),
    ('10', 'Bare, LED și senzori', [], 'PZ2, electrician pentru 230 V',
     ['Montează barele U la 1950 mm de pardoseală: 1015 mm la C07, 1025 mm la C08.',
      'Prinde profilele LED sub C07.2 / C08.2, la 20 mm de muchia din față.',
      'Sursa de 24 V în compartimentul de sus dinspre C01; racordul la 230 V îl face electricianul.',
      'Trage câte un cablu de la fiecare profil LED în jos, pe C01 / C05 / C06, până în dreptul balamalei de sus a ușilor mari (~1600 mm). Senzorii de ușă se montează la pasul 11.'],
     'Sursa rămâne accesibilă: nu o acoperi cu cutii.',
     [('U', 'Bară ovală aluminiu 30 × 15', 2, 'la 1950 mm de pardoseală, la ~290 mm de față, 2 suporți cu 2 șuruburi I'),
      ('X', 'Profil LED aplicat 1 m + difuzor', 2, 'sub C07.2 / C08.2, la 20 mm de față, cleme cu șuruburi I'),
      ('X', 'Cablu 2 × 0,5 mm² pentru senzorii de ușă', '~6 m', 'pe muchia interioară a C01, C05, C06, prins cu cleme, până lângă balamaua de sus'),
      ('X', 'Sursă 24 V 30–60 W', 1, 'pe C07.2, în compartimentul de sus dinspre C01'), ('I', 'Șurub PAL 4 × 16', 16, '')], det_none),
    ('11', 'Ușile de jos', ['F01'], 'PZ2',
     ['Prinde plăcuțele O pe C01, C05 (ambele fețe) și C06, în găurile Ø5 de pe linia de 37 mm.',
      'Prinde balamalele în locașurile Ø35 ale ușilor: M pe F01.1, N pe F01.2 – F01.4.',
      'Agață ușile pe plăcuțe (clic).',
      'Montează câte un TIP-ON P în corp, sus, pe partea opusă balamalelor.',
      'Lângă balamaua de sus a fiecărei uși mari lipește senzorul de ușă X pe corp (C01, C05 sau C06), cu fața spre ușă: LED-ul se aprinde când se deschide ușa. Senzorii celor două uși ale unui modul se leagă în paralel.'],
     'Ușile se montează fără oglindă; oglinzile se lipesc la pasul 14. Push fără soft-close: balamalele sunt fără arc, ca TIP-ON să poată deschide ușa.',
     [('O', 'Blum 173L6100 plăcuță cruce, 0 mm', 16, 'pe linia de 37 mm: C01 4, C05 stânga 4, C05 dreapta 4 (decalate), C06 4; 2 șuruburi I'),
      ('M', 'Blum 70T3550 CLIP top aplicată, fără arc', 4, 'F01.1 (lângă C01): locaș Ø35 × 13 la 21,5 mm de muchie, 2 șuruburi I'),
      ('N', 'Blum 70T3650 CLIP top semiaplicată, fără arc*', 12, 'F01.2 – F01.4 (despărțitoare comune), 2 șuruburi I'),
      ('P', 'Blum TIP-ON 956.1004 + adaptor drept*', 4, 'în corp, sus, opus balamalelor, 2 șuruburi I'),
      ('X', 'Senzor de ușă IR 24 V, autoadeziv, 30 × 14 × 6 mm', 4, 'pe corp, lângă balamaua de sus a F01.1 – F01.4; câte 2 în paralel pe modul, la LED-ul modulului'),
      ('I', 'Șurub PAL 4 × 16', 72, '')],
     lambda: det_11(False)),
    ('12', 'Ușile de sus', ['F02'], 'PZ2',
     ['Plăcuțele O la cotele din desen (2 pe ușă).',
      'Balamale: M pe F02.1, N pe F02.2 – F02.4.',
      'Rostul dintre ușa de jos și cea de sus: 3 mm.'], '',
     [('O', 'Blum 173L6100 plăcuță cruce, 0 mm', 8, 'pe linia de 37 mm, 2 pe fiecare ușă'),
      ('M', 'Blum 70T3550 CLIP top aplicată, fără arc', 2, 'F02.1'), ('N', 'Blum 70T3650 CLIP top semiaplicată, fără arc*', 6, 'F02.2 – F02.4'),
      ('P', 'Blum TIP-ON 956.1004 + adaptor drept*', 4, 'în corp, opus balamalelor'), ('I', 'Șurub PAL 4 × 16', 40, '')], lambda: det_11(True)),
    ('13', 'Masca de tavan', ['F06'], 'ruletă, fierăstrău circular / rindea',
     ['Măsoară distanța dintre blat și tavan în 3 puncte.',
      'Taie latura de sus (L2) a măștii la cota cea mai mică, minus 2 mm.',
      'Prinde masca de blat cu 4 colțare D, aliniată cu fața ușilor.'],
     'Lasă rostul de 2 mm: tavanul nu e niciodată perfect drept.',
     [('D', 'Colțar metalic 40 × 40', 4, 'în spatele măștii, pe blatul C04, la ~300 mm de capete și la treimi'), ('I', 'Șurub PAL 4 × 16', 16, '')], det_none),
]


def step_page(code, title, codes, tools, actions, warn, hwrows, det, image):
    # pagina A: imagine + necesar + actiuni
    start('P' + code, 'Pasul %s – %s' % (code.lstrip('0'), title), 'Piesele noi sunt turcoaz, cu eticheta lor | cercurile portocalii = feronerie | vedere din hol')
    rect(42, 140, 640, 600, fill=HexColor('#f6f8f9'), stroke=GRAY, lw=.5)
    img(image, 52, 150, 620, 580)
    callouts(code)
    circle(85, 185, 26, TEAL, TEAL); c.setFillColor(white); c.setFont('SegoeB', 26); c.drawCentredString(85, H - 194, code.lstrip('0'))
    x, w = 706, 442
    lines = []
    for k in codes:
        p = PCS[k]
        tg = tags(k)
        lines.append('<b>%s</b> %s, %d × %d — placa <b>%s</b>' % (', '.join(tg), p[1], p[4], p[5], ', '.join(sorted({where(t) for t in tg}))))
    lines += ['<font color="#c27a2c"><b>%s</b></font> %s — %s' % (r[0], r[1].replace('*', ''), r[2]) for r in hwrows if r[0] != '—']
    y = panel(x, 140, w, 'Necesar', '<br/>'.join(lines) or '—') + 10
    y += para(x, y, w, '<b>Unelte:</b> ' + tools, 10) + 14
    for i, a in enumerate(actions, 1):
        circle(x + 9, y + 8, 9, TEAL, white); txt(x + 6, y + 12, str(i), 10, TEAL, True)
        y += para(x + 26, y, w - 26, a, 11) + 10
    if warn:
        h = para(x + 12, y + 12, w - 24, '<b>Atenție:</b> ' + warn, 10)
        rect(x, y, w, h + 24, fill=WARN, stroke=RED, lw=.6); para(x + 12, y + 12, w - 24, '<b>Atenție:</b> ' + warn, 10)
        y += h + 24
    if y > H - 70:
        raise ValueError('Pasul %s depaseste pagina: %d' % (code, y))
    end()
    # pagina B: imbinari si feronerie
    start('P%sb' % code, 'Pasul %s – îmbinări și feronerie' % code.lstrip('0'), 'Unde intră fiecare ericson, cep, pin și piesă Blum | X de la muchia din față (linia turcoaz), Y de la muchia de jos a piesei',
          '1:15 la imprimare A3, 100%' if det is not det_none else 'Fără scară')
    rows = [['', 'Element / cod', 'Buc.', 'Unde și cum']] + [[('<font color="#c27a2c"><b>%s</b></font>' % r[0]), r[1], str(r[2]), r[3]] for r in hwrows]
    if det is det_none:
        table(42, 150, [36, 330, 70, 670], rows, 10)
    else:
        det()
        table(756, 150, [28, 140, 46, 178], rows, 9)
    end()


for s in STEPS:
    step_page(*s, image='pas_%s.png' % s[0])

# ---------------------------------------------------------------- 9a cutia de sertar
start('P09a', 'Pasul 9a – Cutia de sertar (×2)', 'Asamblare pe masă, înainte de pasul 9 | cote în mm', '1:5 la imprimare A3, 100%')
k = 72 / 25.4 / 5
ox, oy = 80, 190
Lc, Wd, t = 490, 1007, 16
rect(ox, oy, Wd * k, t * k, fill=PALE, stroke=TEAL); rect(ox, oy + (Lc - t) * k, Wd * k, t * k, fill=PALE, stroke=TEAL)
rect(ox, oy, t * k, Lc * k, fill=LIGHT, stroke=INK); rect(ox + (Wd - t) * k, oy, t * k, Lc * k, fill=LIGHT, stroke=INK)
for X in (0, Wd - t):
    for Y in (8, Lc - 8):
        mark(ox + (X + t / 2) * k, oy + Y * k, 'A')
txt(ox, oy - 12, 'Vedere de sus (fără fund)', 11, INK, True)
dim(ox, oy + Lc * k, ox + Wd * k, oy + Lc * k, '1007 lățime exterioară (975 + 2 × 16)', 22)
dim(ox + Wd * k, oy, ox + Wd * k, oy + Lc * k, '490', 18)
pill(ox + 60, oy + Lc * k / 2, 'S01.1 / S01.3', TEAL, 9); pill(ox + Wd * k - 60, oy + Lc * k / 2, 'S01.2 / S01.4', TEAL, 9)
pill(ox + Wd * k / 2, oy + 5, 'S02.2 / S03.2 spate', TEAL, 9); pill(ox + Wd * k / 2, oy + (Lc - 8) * k, 'S02.1 / S03.1 față interioară', TEAL, 9)
txt(ox + Wd * k / 2 - 60, oy + Lc * k / 2 + 30, 'fund S04 / S05: 975 × 490', 10, MUT)
sx, sy = 80, 560
rect(sx, sy, Lc * k, 200 * k, fill=LIGHT, stroke=INK)
rect(sx, sy + (200 - 29) * k, Lc * k, 16 * k, fill=PALE, stroke=TEAL)
for xx in (8, 482):
    for yy in (69, 160):
        mark(sx + xx * k, sy + (200 - yy) * k, 'A')
txt(sx, sy - 12, 'Lateral S01 (490 × 200), interior', 11, INK, True)
dim(sx + Lc * k, sy, sx + Lc * k, sy + 200 * k, '200', 18)
dim(sx, sy + 200 * k, sx + Lc * k, sy + 200 * k, '490', 22)
leader([(sx + 482 * k, sy + (200 - 160) * k), (sx + Lc * k + 40, sy + 10)], 'confirmat Ø7 la 8 mm de capete, la 69 și 160 mm de jos', RED)
leader([(sx + 300 * k, sy + (200 - 21) * k), (sx + Lc * k + 40, sy + 200 * k - 10)], 'fund retras 13 mm de la muchia de jos (MOVENTO)', TEAL)
x, w = 706, 442
lines = ['<b>%s</b> — placa <b>%s</b>' % (', '.join(tags(cd)), ', '.join(sorted({where(t2) for t2 in tags(cd)}))) for cd in ('S01', 'S02', 'S03', 'S04', 'S05')]
y = panel(x, 140, w, 'Necesar pentru 2 sertare', '<br/>'.join(lines)) + 10
y = table(x, y, [28, 150, 40, 224], [['', 'Element', 'Buc.', 'Unde'],
                                      ['<font color="#c27a2c"><b>A</b></font>', 'Confirmat 7 × 50', '16', 'prin S01 (Ø7) în cantul S02 / S03 (Ø5 × 45), 4 la fiecare colț de cutie'],
                                      ['<font color="#c27a2c"><b>K</b></font>', 'Șurub PAL 4 × 40', '12', '3 prin fiecare lateral în cantul fundului'],
                                      ['<font color="#c27a2c"><b>J</b></font>', 'Șurub PAL 4 × 30', '8', '2 prin fund în S02 și 2 în S03, la fiecare cutie']], 9) + 12
for i, a in enumerate(['Prinde S02 (față interioară) și S03 / S02 spate între lateralele S01 cu confirmat A.',
                       'Introdu fundul între laterale, cu fața de jos la 13 mm deasupra muchiei de jos a lateralelor.',
                       'Prinde fundul cu șuruburi K prin laterale și J în față și spate.',
                       'Verifică diagonalele cutiei (diferență max. 1 mm).'], 1):
    circle(x + 9, y + 8, 9, TEAL, white); txt(x + 6, y + 12, str(i), 10, TEAL, True)
    y += para(x + 26, y, w - 26, a, 11) + 8
end()

for s in STEPS2:
    step_page(*s, image='pas_%s.png' % s[0])
    if s[0] == '11':
        start('P11a', 'Detaliu – balamalele ușilor', 'Locașuri Ø35 × 13 la 21,5 mm de muchie (date la atelier) | cote de la muchia de jos a ușii', '1:10 la imprimare A3, 100%')
        kd = 72 / 25.4 / 10
        doors = [('F01.1, F01.2, F01.4', 1699, D['LOWER_A']), ('F01.3 (decalată)', 1699, D['LOWER_B']),
                 ('F02.1, F02.2, F02.4', 377, D['UPPER_A']), ('F02.3', 377, D['UPPER_B'])]
        for i, (name, hgt, lst) in enumerate(doors):
            x0 = 90 + i * 270; y0 = 160 + (1699 - hgt) * kd
            rect(x0, y0, 519 * kd, hgt * kd, fill=HexColor('#e4e9ec'), stroke=INK)
            txt(x0, y0 - 10, name, 11, INK, True)
            for yy in lst:
                cy = y0 + (hgt - yy) * kd
                circle(x0 + 21.5 * kd, cy, 35 * kd / 2, TEAL, white)
                txt(x0 + 21.5 * kd + 10, cy + 3, '%g' % yy, 9, TEAL, True)
            dim(x0, y0 + hgt * kd, x0 + 519 * kd, y0 + hgt * kd, '519', 18)
            dim(x0 + 519 * kd, y0, x0 + 519 * kd, y0 + hgt * kd, str(hgt), 16)
        para(42, 700, 1100, 'Spatele ușii, cu balamalele pe stânga; la ușile cu balamale pe dreapta cotele sunt în oglindă. '
             'F01.1 / F02.1 primesc balamale aplicate M (70T3550), celelalte semiaplicate N (70T3650). Ușa 3 e decalată ca plăcuțele ei să nu se întâlnească în C05 cu cele ale ușii 2.', 11)
        end()

# ---------------------------------------------------------------- pasul 14
start('P14', 'Pasul 14 – Reglaje, oglinzi și verificări finale', 'Ultimul pas: rosturi egale, oglinzi lipite, capace')
img('pas_final.png', 52, 150, 620, 580)
x, w = 706, 442
y = table(x, 140, [28, 150, 50, 214], [['', 'Element', 'Buc.', 'Unde'],
                                      ['<font color="#c27a2c"><b>V</b></font>', 'Oglindă 4 mm cu folie', '4 + 4', '1695 × 515 pe F01, 373 × 515 pe F02, retrase 2 mm pe contur'],
                                      ['<font color="#c27a2c"><b>W</b></font>', 'Silicon neutru', '2 tuburi', 'benzi verticale la ~100 mm, nu puncte'],
                                      ['<font color="#c27a2c"><b>B</b></font>', 'Capac confirmat alb', '44', 'pe toate capetele de confirmat vizibile']], 9) + 14
for i, a in enumerate(['Reglează ușile din cele 3 șuruburi ale balamalei CLIP top (lateral ±2 mm, înălțime ±2 mm, adâncime +3 / −2 mm) până ai rost de 3 mm peste tot.',
                       'Dă jos câte o ușă (clic), așaz-o pe orizontală și lipește oglinda cu silicon neutru W. Lasă 24 de ore.',
                       'Remontează ușile și refă reglajul: oglinda adaugă ~5 kg pe ușa mare.',
                       'Pune capacele B pe confirmatele vizibile.'], 1):
    circle(x + 9, y + 8, 9, TEAL, white); txt(x + 6, y + 12, str(i), 10, TEAL, True)
    y += para(x + 26, y, w - 26, a, 11) + 10
y += 6
table(x, y, [32, 410], [['', 'Verificare finală'], ['□', 'Colțarele anti-răsturnare sunt prinse în perete'], ['□', 'Ușile se deschid cu TIP-ON și nu ating masca'],
                         ['□', 'Sertarele se închid singure, sincronizat'], ['□', 'LED-ul se aprinde la fiecare ușă'], ['□', 'Rosturi de 3 mm, oglinzi fără tensiune']], 10)
end()
c.save()
print('PDF', OUT, PAGE, 'pagini')
