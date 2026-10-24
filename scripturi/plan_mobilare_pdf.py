"""Plan de mobilare R02, în stilul planșelor A3 existente, refăcut din modelul 3D actual:
- M01 plan general cotat: încăperi, suprafețe, cote, uși;
- M02 plan de mobilare: toate piesele cu cod și legendă (la comandă / cumpărat / existent / încălzire);
- M03–M07 pe încăperi: piesele cu dimensiuni, produsul ales, prețul celei mai bune oferte și link (deviz R03);
- M08 pardoseli și praguri; M09 plan 3D; M10–M11 randări.
Date: tmp/mobilier_plan.json (extrage_mobilier_plan.py), tmp/termic_model.json (pereți, încăperi), tmp/deviz.json (R03).
Rulează cu Python-ul care are reportlab. Iese: output/pdf/Apartament_184_Plan_mobilare_R02.pdf"""
import sys, math
from pathlib import Path
from urllib.parse import urlparse
sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_comun import *

pre = (ROOT / 'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
for a, b in [('Apartament_184_Plan_termic_R01.pdf', 'Apartament_184_Plan_mobilare_R02.pdf'),
             ("'R01 | 05.10.2026 | COORDONARE ȘI OFERTARE - NU PLAN DE EXECUȚIE VALIDAT'",
              "'R02 | 05.10.2026 | PLAN DE MOBILARE - COTE DIN MODELUL 3D, DE VERIFICAT PE TEREN'")]:
    assert a in pre, a
    pre = pre.replace(a, b)
exec(patch_prefix(pre))
c.setTitle('Apartament 184 - Plan de mobilare - R02')
styles[8] = ParagraphStyle('p8', parent=style, fontSize=8, leading=10.2)
MI = {m['code']: m for m in MOB}
ROOMP = {r['name']: r['polygon'] for r in DATA['rooms']}


def area(p):
    return abs(sum(p[i][0] * p[i - 1][1] - p[i - 1][0] * p[i][1] for i in range(len(p)))) / 2e6


def ro(v, d=2):
    return ('%.*f' % (d, v)).replace('.', ',')


# încăperi: nume, poligon, poziția etichetei (mm), pardoseală
ROOMS = [('DORMITOR', 'Pardoseala_Dormitor', (1250, -2950), 'parchet'), ('CAMERĂ DE ZI', 'Pardoseala_CameraDeZi', (5550, -1550), 'parchet'),
         ('BUCĂTĂRIE', 'Pardoseala_Bucatarie', (8450, -1700), 'epoxid'), ('BAIE', 'Pardoseala_Baie', (1300, -4450), 'microciment'),
         ('VESTIBUL', 'Pardoseala_Vestibul', (3040, -4300), 'microciment'), ('HOL', 'Pardoseala_Hol', (8350, -4250), 'microciment'),
         ('DEBARA', 'Pardoseala_Nisa', (10250, -1830), 'epoxid'), ('BALCON ÎNCHIS', 'Balcon_placa', (5400, 330), 'epoxid')]
CUSTOM = {'DH', 'DR', 'MC', 'BJ', 'BS', 'DB', 'SP', 'CTV', 'CTD', 'N1', 'N2', 'MJ', 'DW', 'NS'}
EXIST, HEAT = {'DD'}, {'R1', 'R2', 'RP'}
CAT = lambda code: 'custom' if code in CUSTOM else 'exist' if code in EXIST else 'heat' if code in HEAT else 'buy'
COL = {'custom': (HexColor('#dcefec'), TEAL), 'buy': (HexColor('#f6ecda'), HexColor('#a8742c')),
       'exist': (HexColor('#e6e8ea'), MUT), 'heat': (HexColor('#ffe3d8'), RED)}
CATN = {'custom': 'la comandă', 'buy': 'cumpărat', 'exist': 'existent', 'heat': 'încălzire'}
# etichete mutate lângă piesă (mm), cu linie de legătură până la piesă
LAB = {'BS': ((7545, -620), None), 'BJ': ((7557, -2450), None), 'TV1': ((4430, -2300), (3754, -2300)), 'CTV': ((3900, -3560), None),
       'CTD': ((2760, -2250), (3300, -2250)), 'TV2': ((2760, -1650), (3458, -1650)), 'RF': ((2760, -1950), (3535, -1950)),
       'DW': ((2075, -5455), None), 'WC': ((2060, -4930), None), 'MM': ((5400, -3360), None), 'MT': ((5100, -2480), None),
       'MC': ((5400, -4380), None), 'PV': ((1020, -4850), (838, -4850)), 'NS': ((500, -5485), None), 'RP': ((1250, -4160), (1250, -3955)),
       'R1': ((2480, -700), (2480, -372)), 'R2': ((5350, -700), (4475, -372)), 'DB': ((10420, -430), None)}

# produsul ales pentru fiecare piesă: text, rânduri din deviz, adaos (suport TV), preț parțial, inclus în altă piesă
PROD = {
    'PT': dict(t='Cadru JYSK HALD 160 × 200 stejar, cu ladă + saltea IKEA VALEVÅG', ids=['M093', 'M094']),
    'N1': dict(t='La comandă: corp U702 greige, 2 sertare push, blat „plutitor”, LED sub blat din priza P01', lot=True),
    'N2': dict(t='Ca N1, în oglindă; LED din priza P02', lot=True),
    'DD': dict(t='Dulapul existent 220 × 60 se păstrează, rotit pe peretele de lângă ușă'),
    'CTD': dict(t='La comandă: stejar H1145, 2 sertare, suspendată la 30–58 cm, LED dedesubt', lot=True),
    'TV2': dict(t='TCL 55P8L pe suport Nexio NX-LPA52-446, centrat pe pat', ids=['M090'], add=DVR['M091']['tmin'] / 2),
    'RF': dict(t='Riflaje stejar pe 150 cm, podea–tavan, decupaj la modulul TV, LED vertical', ids=['M017']),
    'MJ': dict(t='La comandă: blat suspendat 80 × 40 cu 2 sertare; oglindă 80 × 174 cu bandă LED pe ambele laterale (oglinda în M069)', lot=True),
    'PF': dict(t='Puf rotund bouclé ~40 cm', price=253.41, link='M098'),
    'R1': dict(t='Radiator Purmo Compact 22, 600 × 1000', ids=['M057']),
    'CN': dict(t='Canapea extensibilă cu ladă JYSK ILDVED (alternativă IKEA FRIHETEN)', ids=['M092']),
    'CTV': dict(t='La comandă: 240 × 40, suspendată la 20 cm, 3 fronturi U702, blat stejar H1145, LED', lot=True),
    'TV1': dict(t='TCL 55C6K Pro pe suport Nexio NX-LPA52-446', ids=['M089'], add=DVR['M091']['tmin'] / 2),
    'MT': dict(t='Măsuță travertin oval 110 × 65 + măsuța de stejar Ø60 (comandă)', ids=['M097']),
    'MM': dict(t='Măsuță stejar Ø60, sus la 25 cm', inc='MT'),
    'BR': dict(t='Birou IKEA TROTTEN reglabil electric, alb, 120 × 70', ids=['M095']),
    'SB': dict(t='Scaun de birou IKEA FLINTAN', ids=['M096']),
    'DR': dict(t='La comandă: 5 module, fronturi U702 push, sertare MOVENTO, LED + masă de călcat Häfele Ironfix în M3', ids=['M072', 'M073'], lot=True),
    'MC': dict(t='Planșeta mesei de călcat deschisă: ocupă ~1 m în cameră', inc='DR'),
    'R2': dict(t='Radiator Purmo Compact 22, 600 × 1200', ids=['M058']),
    'BJ': dict(t='La comandă: 322 cm, corp W1000, fronturi U702 TIP-ON, blat stejar H1145 38 mm; feronerie Blum', ids=['M074', 'M068'], lot=True),
    'BS': dict(t='Corpuri sus 100 cm, hotă incorporabilă, picurător, mască până la tavan', inc='BJ'),
    'FR': dict(t='Frigider TCL RP503SSE1 side-by-side', ids=['M084']),
    'MS': dict(t='Masă IKEA NÄSINGE 80 × 60 + 2 pufuri', ids=['M081']),
    'SC1': dict(t='Puf / scaun', inc='MS'), 'SC2': dict(t='Puf / scaun', inc='MS'),
    'DB': dict(t='Rafturi W1000 pe 4 niveluri (70 / 110 / 150 / 190 cm), LED sub fiecare raft', lot=True),
    'CD': dict(t='Cadă Roca Contesa 150 × 70 + sifon Alcadrain A55KM + kit de susținere', ids=['M040', 'M041', 'M055']),
    'NS': dict(t='Mască de rigips hidrofug cu 3 nișe, finisată cu microciment', lot=True),
    'PV': dict(t='Paravan cadă Mediterraneo 80 × 140, sticlă securizată', ids=['M048']),
    'LV': dict(t='Lavoar Roca Gap New 60 cu mască și sertare + baterie Grohe Eurosmart', ids=['M046', 'M047']),
    'WC': dict(t='Vas Roca Meridian Rimless compact + rezervor Geberit Duofix + clapetă Sigma01', ids=['M045', 'M043', 'M044']),
    'DW': dict(t='La comandă: 650 × 250 × 800, W1000 / U702, 2 uși', lot=True),
    'RP': dict(t='Portprosop Purmo Santorini 500 × 714', ids=['M059']),
    'SP': dict(t='La comandă: corp 1000 × 650 până la tavan, platformă, coșuri, poliță extractibilă + mașina Heinner 10 kg', ids=['M075', 'M088'], lot=True),
    'DH': dict(t='La comandă: W1000 / U702, 8 uși cu oglindă, TIP-ON, sertar pantofi, LED pornit de senzori de ușă', ids=['M071'], lot=True),
    'US': dict(t='Uscător de rufe Leifheit Pegasus 200, 20 m', ids=['M101'])}
ORDER = [('Dormitor', ['PT', 'N1', 'N2', 'DD', 'CTD', 'TV2', 'RF', 'MJ', 'PF', 'R1']),
         ('Cameră de zi', ['CN', 'CTV', 'TV1', 'MT', 'MM', 'BR', 'SB', 'DR', 'MC', 'R2']),
         ('Bucătărie', ['BJ', 'BS', 'FR', 'MS', 'SC1', 'SC2']), ('Debara', ['DB']),
         ('Baie', ['CD', 'NS', 'PV', 'LV', 'WC', 'DW', 'RP']), ('Vestibul', ['SP']), ('Hol', ['DH']), ('Balcon', ['US'])]
assert sorted(sum((l for _, l in ORDER), [])) == sorted(MI), set(MI) ^ set(sum((l for _, l in ORDER), []))


def dom(i):
    u = DVR[i]['url']
    return urlparse(u).netloc.replace('www.', '') if u else 'estimat'


def price(code):
    p = PROD[code]
    if 'price' in p:
        return p['price']
    if not p.get('ids'):
        return None
    return sum(DVR[i]['tmin'] for i in p['ids']) + p.get('add', 0)


def dims(m):
    b = m['bbox']
    s = '%d × %d' % (round(b[3] - b[0]), round(b[4] - b[1]))
    if m['kind'] in ('sus', 'perete') and b[2] > 60:
        return s + '<br/>la %d–%d' % (b[2], b[5])
    return s + '<br/>h %d' % b[5]


# ---------------------------------------------------------------- desen
def draw_items(P, codes=None, size=8, labels=True):
    sel = [m for m in MOB if codes is None or m['code'] in codes]
    for m in sorted(sel, key=lambda m: m['kind'] == 'sus'):
        fill, stroke = COL[CAT(m['code'])]
        for q in m.get('polys') or [m['poly']]:
            pts = [P(*v) for v in q]
            if m['kind'] == 'sus':
                c.setDash([3, 2]); poly(pts, color=stroke, lw=.8); c.setDash([])
            else:
                poly(pts, fill=fill, color=stroke, lw=.8)
    if labels:
        for m in sel:
            label(P, m, size)


def label(P, m, size=8):
    b = m['bbox']
    (lx, ly), anchor = LAB.get(m['code'], (((b[0] + b[3]) / 2, (b[1] + b[4]) / 2), None))
    x, y = P(lx, ly)
    w = pdfmetrics.stringWidth(m['code'], 'SegoeB', size)
    col = COL[CAT(m['code'])][1]
    if anchor:
        ax, ay = P(*anchor)
        line(x + (w / 2 + 2 if ax > x else -w / 2 - 2 if ax < x else 0), y, ax, ay, col, .5)
        circle(ax, ay, 1.4, col, col)
    c.setFillColor(white); c.rect(x - w / 2 - 2, H - y - size * .45, w + 4, size + 1, stroke=0, fill=1)
    txt(x - w / 2, y + size * .35, m['code'], size, col, True)


def room_labels(P, size=9, dims_=True, pos=None, region=None):
    """numele încăperii, suprafața și (opțional) dimensiunile; încăperile înguste pe trei rânduri"""
    for name, key, xy, _ in ROOMS:
        x, y = (pos or {}).get(name, xy)
        if region and not (region[0] < x < region[1] and region[2] < y < region[3]):
            continue
        p = ROOMP[key]
        xs, ys = [q[0] for q in p], [q[1] for q in p]
        px, py = P(x, y)
        w = pdfmetrics.stringWidth(name, 'SegoeB', size)
        txt(px - w / 2, py, name, size, INK, True)
        lines = [ro(area(p)) + ' m²']
        if dims_:
            lines.append('%s × %s m' % (ro((max(xs) - min(xs)) / 1000), ro((max(ys) - min(ys)) / 1000)))
        if name == 'DEBARA':
            lines = lines[:1]
        elif name != 'VESTIBUL':
            lines = ['   '.join(lines)]
        for i, s in enumerate(lines):
            w2 = pdfmetrics.stringWidth(s, 'Segoe', size - 1.5)
            txt(px - w2 / 2, py + (size + 2) * (i + 1), s, size - 1.5, MUT)


def fit_scale(region, box, scales=(15, 20, 25, 30, 40, 50)):
    x0, x1, y0, y1 = region
    for s in scales:
        k = 72 / 25.4 / s
        if (x1 - x0) * k <= box[2] and (y1 - y0) * k <= box[3]:
            return s
    return scales[-1]


def fit_view(region, box):
    """vederea în plan a unei zone (mm) într-un chenar al paginii, la cea mai mare scară standard care încape"""
    x0, x1, y0, y1 = region
    bx, by, bw, bh = box
    s = fit_scale(region, box)
    k = 72 / 25.4 / s
    ox = bx + (bw - (x1 - x0) * k) / 2 - x0 * k
    oy = by + (bh - (y1 - y0) * k) / 2 + y1 * k
    P, k = view(ox, oy, s, clip=(bx, by, bw, bh))
    return P, k, s


def clip_box(box):
    c.saveState(); pa = c.beginPath(); pa.rect(box[0], H - box[1] - box[3], box[2], box[3]); c.clipPath(pa, stroke=0)


def legend_strip(x, y):
    for i, (k, n) in enumerate(CATN.items()):
        fill, stroke = COL[k]
        rect(x + i * 128, y - 9, 16, 10, fill=fill, stroke=stroke, lw=.8); txt(x + i * 128 + 22, y, n, 9, MUT)
    c.setDash([3, 2]); rect(x + 4 * 128, y - 9, 16, 10, stroke=MUT, lw=.8); c.setDash([])
    txt(x + 4 * 128 + 22, y, 'suspendat (deasupra)', 9, MUT)


DOORS = {'U1': (3050, -3882), 'U2': (2330, -4380), 'U3': (3625, -4500), 'U4': (7175, -4400), 'U5': (8400, -3507),
         'U6': (9837, -1850), 'U7': (9700, -4330), 'U8': (5675, -125)}


def door_labels(P, size=8):
    for d, (x, y) in DOORS.items():
        px, py = P(x, y)
        w = pdfmetrics.stringWidth(d, 'SegoeB', size)
        c.setFillColor(white); c.rect(px - w / 2 - 2, H - py - size * .45, w + 4, size + 1, stroke=0, fill=1)
        txt(px - w / 2, py + size * .35, d, size, BLUE, True)


# ---------------------------------------------------------------- M00 copertă
n = {k: sum(1 for m in MOB if CAT(m['code']) == k) for k in CATN}
SUM = {s['cat'][:2].strip('. '): s['tmin'] for s in DV['summary']}
mob_tot = SUM['8'] + SUM['9'] + SUM['12']
start('M00', 'Plan de mobilare', 'R02: refăcut din modelul 3D actual, cu produsele alese, prețurile celor mai bune oferte (deviz R03), pardoseli, praguri și randări')
for x, title, val, sub in [(42, 'SUPRAFAȚĂ', ro(sum(area(ROOMP[k]) for _, k, _, _ in ROOMS[:-1]), 1) + ' m²', 'pardoseli interioare din model · balcon închis ' + ro(area(ROOMP['Balcon_placa'])) + ' m²'),
                           (410, 'MOBILIER', '%d de piese' % len(MOB), '%d la comandă · %d cumpărate · %d existentă · %d radiatoare' % (n['custom'], n['buy'], n['exist'], n['heat'])),
                           (778, 'BUGET MOBILIER', lei(mob_tot) + ' lei', 'plăci și atelier %s · feronerie %s · gata făcut %s' % (lei(SUM['8']), lei(SUM['9']), lei(SUM['12'])))]:
    rect(x, 150, 350, 125, fill=LIGHT, stroke=GRAY); txt(x + 16, 177, title, 11, TEAL, True); txt(x + 16, 218, val, 28, INK, True); txt(x + 16, 249, sub, 9.5, MUT)
para(42, 300, 525, '<b>Ce conține</b><br/>Planul general cotat, planul de mobilare cu toate piesele și câte o planșă pe încăperi. Pe fiecare planșă de încăpere sunt piesele cu dimensiunile din model, produsul ales, prețul celei mai bune oferte găsite pe 05.10.2026 și linkul. Urmează pardoselile cu pragurile și randările.', 12)
para(620, 300, 525, '<b>De unde vin cotele</b><br/>Conturul fiecărei piese e luat din scena 3D (apartament_184_randare.blend), care vine din modelul FreeCAD. Corpurile la comandă au planuri de debitare separate. Înainte de comandă se remăsoară pereții după tencuială și glet.', 12)
rows = [['Planșă', 'Conținut'], ['M01', 'Plan general cotat: încăperi, suprafețe, dimensiuni, uși U1–U8'], ['M02', 'Plan de mobilare cu toate piesele și legenda'],
        ['M03–M07', 'Pe încăperi: dormitor, cameră de zi, bucătărie și debara, baie și vestibul, hol și balcon (produse, prețuri, linkuri)'],
        ['M08', 'Pardoseli și praguri'], ['M09', 'Plan 3D al apartamentului'], ['M10–M11', 'Randări de zi pe încăperi']]
table(42, 470, [110, 996], rows, 10)
end()

# ---------------------------------------------------------------- M01 plan general cotat
start('M01', 'Plan general cotat', 'Cote interioare finite din model, în mm; suprafețele pardoselilor; uși U1–U8', '1:50 la imprimare A3, 100%')
_m, MOB = MOB, []                        # fără mobilier pe planul cotat
P, k = view(75, 255, 50)
MOB = _m
room_labels(P, 10, pos={'DEBARA': (10380, -700), 'VESTIBUL': (3040, -4250)})
door_labels(P)
for (a, b), lab in [((150, 2450), '2.300'), ((2525, 3550), '1.025'), ((3700, 7100), '3.400'), ((7250, 9563.7), '2.314')]:
    dim(*P(a, -5550), *P(b, -5550), lab, 26)
dim(*P(150, -5550), *P(9563.7, -5550), '9.414 / interior, de la dormitor la hol', 52)
for (a, b), lab in [((-250, -3845), '3.595'), ((-3920, -5550), '1.630')]:
    dim(*P(150, a), *P(150, b), lab, -40)
dim(*P(3550, 1300), *P(7250, 1300), '3.700 / balcon', -16)
dim(*P(7250, 0), *P(7250, 1300), '1.300', 20)
rows = [['Încăpere', 'Suprafață', 'Dimensiuni', 'Pardoseală']]
FIN = {'parchet': 'parchet stejar', 'microciment': 'microciment alb cald', 'epoxid': 'rășină epoxidică gri'}
for name, key, _, fin in ROOMS:
    p = ROOMP[key]; xs, ys = [q[0] for q in p], [q[1] for q in p]
    rows.append([name.capitalize(), ro(area(p)) + ' m²', ro((max(xs) - min(xs)) / 1000) + ' × ' + ro((max(ys) - min(ys)) / 1000) + ' m', FIN[fin]])
rows.append(['<b>Interior</b>', '<b>' + ro(sum(area(ROOMP[k]) for _, k, _, _ in ROOMS[:-1])) + ' m²</b>', 'fără balcon', ''])
y = tbl(770, 150, [118, 72, 92, 96], rows, 9, 4, total=True)
para(770, y + 14, 378, '<b>Uși</b><br/>U1 dormitor · U2 baie · U3 vestibul ↔ cameră de zi · U4 cameră de zi ↔ hol · U5 bucătărie · U6 debara · U7 intrare · U8 balcon.<br/><br/>Hol și debara au un perete oblic: dimensiunile din tabel sunt cele maxime. Pereții de 15 / 25 cm sunt structurali.', 10)
end()

# ---------------------------------------------------------------- M02 plan de mobilare
start('M02', 'Plan de mobilare', 'Toate piesele din modelul 3D, cu cod; produsele și prețurile sunt pe planșele M03–M07', '1:50 la imprimare A3, 100%')
P, k = view(70, 265, 50)
draw_items(P, size=7.5)
for name, key, (x, y), _ in ROOMS:
    px, py = P(x, y); w = pdfmetrics.stringWidth(name, 'SegoeB', 8)
    if name not in ('DEBARA',):
        txt(px - w / 2, py + 14, name, 8, MUT, True)
legend_strip(70, 620)
rows = [['Cod', 'Piesă', 'Tip']]
for room, codes in ORDER:
    rows.append(['', '<b>' + room.upper() + '</b>', ''])
    for code in codes:
        rows.append(['<b>' + code + '</b>', esc(MI[code]['name']), CATN[CAT(code)]])
tbl(745, 148, [40, 255, 108], rows, 8, 1.2)
end()


# ---------------------------------------------------------------- M03–M07 pe încăperi
def room_table(codes, extras):
    rows = [['Cod', 'Piesă și produs ales', 'Dimensiuni mm', 'Preț lei', 'Unde']]
    tot = 0
    for code in codes:
        p, m = PROD[code], MI[code]
        pr = price(code)
        if pr:
            tot += pr
        link_id = p.get('link') or (p['ids'][0] if p.get('ids') else None)
        where_ = dvlink(DVR[link_id], dom(link_id)) if link_id else ('atelier' if p.get('lot') else '-')
        if p.get('lot') and link_id:
            where_ += '<br/><font color="#536473">plăci: atelier</font>'
        pt = lei(pr) if pr else ('inclus la ' + p['inc'] if p.get('inc') else 'lot plăci' if p.get('lot') else 'existent' if code in EXIST else '-')
        rows.append(['<b>' + code + '</b>', '<b>' + esc(m['name']) + '</b><br/>' + esc(p['t']), dims(m), pt, where_])
    for i, art, pr in extras:
        r = DVR[i]
        pr = r['tmin'] if pr is None else pr
        tot += pr
        rows.append(['-', esc(art or r['art']), qty(r), lei(pr), dvlink(r, dom(i)) if r['url'] else 'estimat'])
    rows.append(['', '<b>Total cumpărături (fără plăci)</b>', '', '<b>' + lei(tot) + '</b>', ''])
    return rows


PAGES = [
    ('M03', 'Dormitor', 'Parchet stejar · pat centrat pe TV · dulapul existent rotit lângă ușă', [(0, 3700, -4000, 150)], ['PT', 'N1', 'N2', 'DD', 'CTD', 'TV2', 'RF', 'MJ', 'PF', 'R1'],
     [('M100', 'Lenjerie, perne, pătură decorativă', None)]),
    ('M04', 'Cameră de zi', 'Parchet stejar · perete TV cu comodă suspendată · dressing pe peretele dinspre baie · birou la fereastră', [(3550, 7250, -5650, 150)],
     ['CN', 'CTV', 'TV1', 'MT', 'MM', 'BR', 'SB', 'DR', 'MC', 'R2'],
     [('M098', 'Covor IKEA MORUM 160 × 230 (puful e la dormitor)', 239.0), ('M016', None, None), ('M035', 'Aplice LED liniare negre pe peretele TV', None),
      ('M099', 'Draperii opace MAJGULL + voal, șine VIDGA (cameră de zi + dormitor)', None)]),
    ('M05', 'Bucătărie și debara', 'Rășină epoxidică · bucătărie liniară 322 cm cu coloană · frigider side-by-side lângă ușă · rafturi în debara', [(7100, 11050, -3600, 150)],
     ['BJ', 'BS', 'FR', 'MS', 'SC1', 'SC2', 'DB'],
     [('M085', 'Cuptor Arctic ARSE11130XD + plită pe gaz Arctic', None), ('M086', 'Microunde incorporabil Heinner HMW-MDBI28GDBK', None), ('M087', 'Mașină de spălat vase incorporabilă 60 cm', None),
      ('M077', 'Chiuvetă compozit cu picurător 76 × 44', None), ('M078', 'Baterie Grohe Eurosmart 30463000', None), ('M079', 'Hotă incorporabilă Heinner, 630 m³/h', None),
      ('M080', 'Tub plat 150 × 70 + clapetă anti-retur', None), ('M083', 'Racord gaz plită (firmă autorizată)', None), ('M070', 'Protecție perete între blat și corpuri', None),
      ('M082', 'Rulouri zi-noapte pe fereastră', None)]),
    ('M06', 'Baie și vestibul', 'Microciment · cadă 150 × 70 cu nișe · lavoar central · WC suspendat · spălătoria în vestibul', [(0, 3700, -5650, -3800)],
     ['CD', 'NS', 'PV', 'LV', 'WC', 'DW', 'RP', 'SP'],
     [('M042', 'Baterie cadă-duș Grohe 32831000 + set pară Tempesta', None), ('M054', 'Oglindă baie + accesorii', None)]),
    ('M07', 'Hol și balcon', 'Microciment în hol · dulap cu uși oglindă pe peretele de jos · balcon închis doar pentru uscat rufe', [(7100, 10250, -5650, -3350), (3450, 7350, -150, 1400)],
     ['DH', 'US'], [('M069', 'Oglinzi 4 mm cu folie: ușile dulapului (~4,3 m²) + oglinda de machiaj', None)])]
for code, title, sub, regions, codes, extras in PAGES:
    boxes = [(42, 150, 598, 595)] if len(regions) == 1 else [(42, 150, 598, 330), (42, 500, 598, 245)]
    scales = sorted(set(fit_scale(r, b) for r, b in zip(regions, boxes)))
    start(code, title, sub, ' / '.join('1:%d' % s for s in scales) + ' la imprimare A3, 100%')
    for region, box in zip(regions, boxes):
        P, k, s = fit_view(region, box)
        clip_box(box)
        draw_items(P, codes, size=9)
        room_labels(P, 10, dims_=False, region=region)
        door_labels(P, 9)
        c.restoreState()
    txt(42, H - 75, 'Colorate: piesele încăperii (legenda pe M02). Gri pe fundal: piesele din încăperile vecine.', 9, MUT)
    tbl(660, 148, [30, 232, 82, 50, 94], room_table(codes, extras), 8, 3, total=True)
    end()

# ---------------------------------------------------------------- M08 pardoseli și praguri
start('M08', 'Pardoseli și praguri', 'Pragurile din aluminiu periat de 10 mm se pun numai unde se schimbă materialul', '1:50 la imprimare A3, 100%')
_m, MOB = MOB, []
P, k = view(70, 265, 50)
MOB = _m
FC = {'parchet': HexColor('#e8cfa6'), 'microciment': HexColor('#ebe6dc'), 'epoxid': HexColor('#c3c9ce')}
c.saveState(); c.setFillAlpha(.85)
for name, key, _, fin in ROOMS:
    poly([P(*q) for q in ROOMP[key]], fill=FC[fin], color=FC[fin], lw=.1)
c.restoreState()
for e in DATA['wall_edges']:
    if len(e) == 2:
        line(*P(*e[0]), *P(*e[1]), INK, .8)
room_labels(P, 9, dims_=False)
TH = [('U1', 'dormitor / vestibul', (2600, -3882.5), (3500, -3882.5), 'parchet / microciment'), ('U3', 'vestibul / cameră de zi', (3625, -4050), (3625, -4950), 'microciment / parchet'),
      ('U4', 'cameră de zi / hol', (7175, -3950), (7175, -4850), 'parchet / microciment'), ('U5', 'hol / bucătărie', (8000, -3507.5), (8800, -3507.5), 'microciment / epoxid'),
      ('U8', 'cameră de zi / balcon', (5250, -125), (6100, -125), 'parchet / epoxid')]
for u, _, a, b, _ in TH:
    line(*P(*a), *P(*b), HexColor('#7b8794'), 4.5)
    px, py = P((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    txt(px + 6, py - 6, u + ' · ' + str(round(math.dist(a, b))), 8, INK, True)
x0 = 70
for fin, lab in [('parchet', 'parchet stejar'), ('microciment', 'microciment alb cald'), ('epoxid', 'rășină epoxidică gri')]:
    rect(x0, 611, 16, 10, fill=FC[fin], stroke=GRAY, lw=.5); txt(x0 + 22, 620, lab, 9, MUT); x0 += 150
line(x0, 616, x0 + 22, 616, HexColor('#7b8794'), 4.5); txt(x0 + 28, 620, 'prag aluminiu periat 10 mm', 9, MUT)
A = {fin: sum(area(ROOMP[k]) for _, k, _, f in ROOMS if f == fin) for fin in FC}
rows = [['Finisaj', 'Încăperi', 'Arie', 'Material (deviz R03)', 'Preț lei'],
        ['Parchet stejar 14 mm', 'dormitor, cameră de zi', ro(A['parchet']) + ' m²', dvlink(DVR['M003'], 'Diana Forest, lac mat, 33 m²') + '<br/>' + dvlink(DVR['M004'], 'subparchet Arbiton 3 role') + '<br/>' + dvlink(DVR['M005'], 'plintă MDF albă, 18 buc'),
         lei(DVR['M003']['tmin'] + DVR['M004']['tmin'] + DVR['M005']['tmin'])],
        ['Microciment alb cald', 'hol, vestibul, baie', ro(A['microciment']) + ' m²', dvlink(DVR['M006'], '2 kituri pardoseală impermeabilă') + '<br/>' + dvlink(DVR['M010'], 'pereții umezi ai băii: 2 kituri'), lei(DVR['M006']['tmin'] + DVR['M010']['tmin'])],
        ['Rășină epoxidică gri', 'bucătărie, debara, balcon', ro(A['epoxid']) + ' m²', dvlink(DVR['M007'], 'Emex, autonivelantă, ~17 m² cu pierderi'), lei(DVR['M007']['tmin'])],
        ['Șapă și amorsă', 'tot interiorul', '', dvlink(DVR['M002'], 'Ceresit CN 68, 15 saci (fără baie)') + '<br/>' + dvlink(DVR['M009'], 'Baumit Nivello 50, 2 saci (baie)') + '<br/>' + dvlink(DVR['M001'], 'amorsă Ceresit R777'),
         lei(DVR['M002']['tmin'] + DVR['M009']['tmin'] + DVR['M001']['tmin'])],
        ['Praguri', '5 uși', '4,35 m', dvlink(DVR['M008'], 'profil SET S04 aluminiu, 2 bare × 2,7 m'), lei(DVR['M008']['tmin'])]]
tot = sum(DVR[i]['tmin'] for i in ('M001', 'M002', 'M003', 'M004', 'M005', 'M006', 'M007', 'M008', 'M009', 'M010'))
rows.append(['<b>Total pardoseli</b>', '', '', 'cu pereții de microciment ai băii', '<b>' + lei(tot) + '</b>'])
y = tbl(705, 148, [92, 88, 50, 170, 43], rows, 8, 3, total=True)
rows = [['Prag', 'Între', 'Lungime', 'Materiale']] + [[u, w, str(round(math.dist(a, b))) + ' mm', f] for u, w, a, b, f in TH]
rows.append(['<b>Total</b>', '', '<b>%s mm</b>' % '{:,}'.format(round(sum(math.dist(a, b) for _, _, a, b, _ in TH))).replace(',', '.'), 'din 2 bare de 2,7 m'])
y = tbl(705, y + 14, [40, 150, 66, 187], rows, 8, 3, total=True)
para(705, y + 10, 443, 'Fără prag: U2 baie / vestibul și U6 bucătărie / debara (același material), U7 intrarea. Ordinea: șapă → microciment și epoxid → parchet la final. Lungimea exactă a fiecărui prag se ia pe golul ușii, după tocuri.', 9)
end()

# ---------------------------------------------------------------- M09 plan 3D
start('M09', 'Plan 3D al apartamentului', 'Vedere de sus fără tavan, pereți la 2,50 m; corpurile de sus ale bucătăriei sunt ascunse ca să se vadă blatul')
img = ROOT / 'randari/web/Plan_3D_apartament_184.jpg'
c.drawImage(str(img), 42, 75, 1106, 620, preserveAspectRatio=True, anchor='c')
end()

# ---------------------------------------------------------------- M10–M11 randări
REND = [('CZ_01_ansamblu_perete_TV', 'Cameră de zi / ansamblu și perete TV'), ('CZ_02_perete_TV_frontal', 'Cameră de zi / perete TV'), ('CZ_03_dressing_masute', 'Cameră de zi / dressing și măsuțe'),
        ('CZ_04_birou_fereastra', 'Cameră de zi / birou la fereastră'), ('D_01_pat_noptiere', 'Dormitor / pat și noptiere'), ('D_02_perete_TV_riflaje', 'Dormitor / perete TV cu riflaje'),
        ('D_03_zona_machiaj', 'Dormitor / zona de machiaj'), ('K_01_bucatarie_din_usa', 'Bucătărie / din ușă'), ('K_02_spre_frigider', 'Bucătărie / spre frigider'),
        ('DB_01_debara', 'Debara'), ('B_01_baie', 'Baie'), ('V_01_spalatorie_vestibul', 'Vestibul / spălătorie'), ('H_01_dulap_hol', 'Hol / dulap cu oglinzi'),
        ('H_02_intrare', 'Hol / intrare'), ('BL_01_balcon', 'Balcon închis')]
for pg, chunk in enumerate((REND[:9], REND[9:])):
    start('M%d' % (10 + pg), 'Randări de zi' + (' (2)' if pg else ''), 'Cycles, lumină de zi; variantele de seară sunt în randari/noapte')
    for i, (f, cap) in enumerate(chunk):
        col, row_ = i % 3, i // 3
        w_, h_ = 290, 181
        x = 142 + col * (w_ + 18); y = 148 + row_ * (h_ + 22)
        c.drawImage(str(ROOT / 'randari/web/zi' / (f + '.jpg')), x, H - y - h_, w_, h_)
        txt(x, y + h_ + 14, cap, 9.5, INK, True)
    end()

c.save()
print('PDF', OUT, PAGE, 'pagini')
