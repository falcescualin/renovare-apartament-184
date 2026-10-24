"""Specificatie de montaj R04: dressing (camera de zi, 5 module). Coordonate: x = gx - 3710, y = gy + 5550 (spate y = 0, fata y = 580), z de la pardoseala.
Piese din R03 (DR-xx); pozitii din FreeCAD dressing (inventar 07.10.2026)."""
from montaj_specs import Spec, drawer
import montaj_hw, montaj_lib as L
from montaj_comun import B, caps, finish
from montaj_spec_dulapuri import VIEWS, bracket_under_top, clothes_rail


def dressing():
    S = Spec('dressing', 'Dressing', 'Dressing pe peretele de sud, cameră de zi',
             'Camera de zi, pe peretele de sud, între colțul de vest și dulapul de pe hol', (3380, 598, 2497),
             'Dulap de 3380 × 580 × 2380 mm în 5 module, pe 12 picioare (soclu retras): bare de haine, rafturi pe pini, 6 sertare interioare Blum MOVENTO, '
             'masă de călcat rabatabilă și coș de rufe în modulul din mijloc, 10 uși cashmere fără mâner (TIP-ON).')
    S.views = dict(VIEWS)
    Z0, Z1, W = 80.0, 2460.0, 3380.0
    D = [(698, 716), (1396, 1414), (1966, 1984), (2664, 2682)]
    M = [(18, 698), (716, 1396), (1414, 1966), (1984, 2664), (2682, 3362)]
    B(S, 'lat1', 'DR-01', 'Lateral (dreapta)', 0, 18, 0, 580, Z0, Z1, 2)
    B(S, 'lat2', 'DR-01', 'Lateral (stânga)', W - 18, W, 0, 580, Z0, Z1, 2)
    B(S, 'bz_v', 'DR-02', 'Bază, bucata dreapta', 18, 1405, 3, 580, Z0, Z0 + 18, 2)
    B(S, 'bz_e', 'DR-03', 'Bază, bucata stânga', 1405, 3362, 3, 580, Z0, Z0 + 18, 2)
    B(S, 'bl_v', 'DR-04', 'Blat sus, bucata dreapta', 18, 1405, 3, 580, Z1 - 18, Z1, 2)
    B(S, 'bl_e', 'DR-05', 'Blat sus, bucata stânga', 1405, 3362, 3, 580, Z1 - 18, Z1, 2)
    for i, (a, b) in enumerate(D, 1):
        B(S, 'd%d' % i, 'DR-06', 'Despărțitor %d' % i, a, b, 3, 580, Z0 + 18, Z1 - 18, 1)
    for i, (a, b) in enumerate(M, 1):
        B(S, 'ps%d' % i, 'DR-08' if i == 3 else 'DR-07', 'Poliță fixă sus M%d' % i, a, b, 3, 560, 2080, 2098, 3)
    hd = [('h1', 'DR-12', 18, 707), ('h2', 'DR-13', 707, 1975), ('h3', 'DR-13b', 1975, 3362)]
    for pid, code, a, b in hd:
        B(S, pid, code, 'Spate HDF ' + code, a, b, 0, 3, Z0 + 2, Z1 - 2, 4)
    B(S, 'perete', 'PERETE', 'Peretele de sud', -80, W + 80, -63, 0, 0, 2500, 6, mat='perete', role='context')
    B(S, 'soc1', 'DR-11', 'Soclu, bucata 1', 18, 1690, 522, 540, 0, 80, 6)
    B(S, 'soc2', 'DR-11', 'Soclu, bucata 2', 1690, 3362, 522, 540, 0, 80, 6)
    shelves = [(2, z) for z in (600, 900, 1200, 1500, 1800)] + [(4, z) for z in (950, 1300, 1650)] + [(5, 300)] + [(3, 1100), (3, 1500)]
    for k, (m, z) in enumerate(shelves):
        a, b = M[m - 1]
        B(S, 'r%d' % k, 'DR-10' if m == 3 else 'DR-09', 'Raft mobil M%d' % m, a + 1, b - 1, 3, 560, z, z + 18, 8, role='shelf')
    # sertare interioare MOVENTO NL 500, fara front separat (fata interioara de 18 mm e frontul)
    for tag, m, zp in (('a1', 2, 99), ('a2', 2, 299), ('b1', 4, 99), ('b2', 4, 299), ('b3', 4, 499), ('b4', 4, 699)):
        a, b = M[m - 1]
        drawer(S, tag, 'DR-SI', a, 580, zp, b - a, 500, 150, 9, 1, 9, None, None, None, step_tob=None,
               side_r='d1' if m == 2 else 'd3', side_l='d2' if m == 2 else 'd4')
    B(S, 'calcat', 'HAF', 'Masă de călcat rabatabilă Häfele Ironfix (produs)', 1427, 1953, 30, 550, 840, 890, 10, mat='metal', role='hw')
    B(S, 'cos', 'COS', 'Coș de rufe extractibil (produs)', 1434, 1946, 40, 540, 110, 600, 10, mat='metal', role='hw')
    for i, (a, b) in enumerate(M, 1):
        B(S, 'led%d' % i, 'LED', 'Profil LED sub polița de sus M%d' % i, a + 10, b - 10, 513, 530, 2072, 2080, 7, mat='led', role='hw')
    X = [(2, 706), (708, 1404), (1406, 1974), (1976, 2672), (2674, 3378)]
    cj = {1: 'DR-U704', 2: 'DR-U695', 3: 'DR-U567', 4: 'DR-U695', 5: 'DR-U704'}
    cs = {1: 'DR-S704', 2: 'DR-S695', 3: 'DR-S567', 4: 'DR-S695', 5: 'DR-S704'}
    for i, (a, b) in enumerate(X, 1):
        B(S, 'uj%d' % i, cj[i], 'Ușă jos M%d' % i, a, b, 580, 598, 10, 2078, 11, role='door')
        B(S, 'us%d' % i, cs[i], 'Ușă sus M%d' % i, a, b, 580, 598, 2082, 2459, 11, role='door')
    B(S, 'm1', 'DR-14', 'Mască tavan (dreapta)', 0, 1405, 580, 598, Z1, 2497, 13)
    B(S, 'm2', 'DR-15', 'Mască tavan (stânga)', 1405, W, 580, 598, Z1, 2497, 13)
    # balamale: M1 pe lateral, M2 pe D1, M3 pe D2, M4 pe D3, M5 pe celalalt lateral -> fiecare placa are placute pe o singura fata
    sides = {1: ('lat1', '70T3550'), 2: ('d1', '70T3650'), 3: ('d2', '70T3650'), 4: ('d3', '70T3650'), 5: ('lat2', '70T3550')}
    for i in range(1, 6):
        sd, tip = sides[i]
        L.hinges(S, 11, 'uj%d' % i, sd, tip)
        L.hinges(S, 11, 'us%d' % i, sd, tip)
    for i, (a, b) in enumerate(X, 1):
        ox = b - 40 if i < 5 else a + 40
        L.tipon(S, 12, 'uj%d' % i, 'ps%d' % i, ox)
        L.tipon(S, 12, 'us%d' % i, 'bl_v' if ox < 1405 else 'bl_e', ox)
    for pid, code, a, b in hd:
        L.back_screws(S, 4, pid)
    xs = (60, 707, 1405, 1975, 2673, 3320)
    L.legs(S, 5, 'bz_v', [(x, y) for x in xs[:3] for y in (60, 460)], h=80)
    L.legs(S, 5, 'bz_e', [(x, y) for x in xs[3:] for y in (60, 460)], h=80)
    for x in xs:
        S.hw_at(6, 'clema_soclu', (x, 460, 20.0), az=(0, 0, 1), ax=(1, 0, 0), explode=0, letter='CS', dash=False)
    for x in (400.0, 1700.0, 3000.0):
        bracket_under_top(S, 6, x, 0.0, Z1 - 18)
    clothes_rail(S, 7, 18, 698, 290, 1980, 'M1s')
    clothes_rail(S, 7, 18, 698, 290, 980, 'M1j')
    clothes_rail(S, 7, 2682, 3362, 290, 1980, 'M5')
    left_of = {1: 'lat1', 2: 'd1', 3: 'd2', 4: 'd3', 5: 'd4'}
    right_of = {1: 'd1', 2: 'd2', 3: 'd3', 4: 'd4', 5: 'lat2'}
    for k, (m, z) in enumerate(shelves):
        L.shelf_pins(S, 8, 'r%d' % k, left_of[m], right_of[m])
    for x in (300.0, 1000.0, 1800.0, 2600.0, 3200.0):
        S.hw_at(13, 'coltar_40', (x, 580.0, Z1), az=(0, 0, 1), ax=(-1, 0, 0), explode=40, letter='L', dash=False)
    montaj_hw.auto(S)
    caps(S, 14, ('lat1', 'lat2', 'd1', 'd2', 'd3', 'd4', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5'))
    S.final_views = ['fata']
    S.gbox = (3710, -5550, 7090, -4952)
    S.time = '≈ 2–3 zile'
    S.people = '2, și 4 la ridicarea corpului'
    S.wall = dict(kind='antirasturnare', unit_h=2380, note='3 colțare sub blatul corpului. Dressingul de 3,4 m se prinde și de dulapul de pe hol, cu 3 șuruburi de îmbinare prin laterale.')
    S.pre = ['Pardoseala e finită; peretele de sud e vopsit.', 'Înălțimea sub tavan e măsurată în 3 puncte (proiect ~2500 mm).',
             'Alimentarea LED 24 V și senzorii de ușă au cablul adus sus, în modulul 3.']
    RA = {}
    for g in ('a1', 'a2', 'b1', 'b2', 'b3', 'b4'):
        RA[g + '.rl'] = [40, 0, 0]
        RA[g + '.rr'] = [-40, 0, 0]
    S.step(1, 'Glisierele sertarelor interioare pe despărțitori (pe podea)', 'culcat',
           ['Sertarele interioare sunt în modulul 2 (2 bucăți) și în modulul 4 (4 bucăți); glisierele vin pe despărțitorii 1 și 2 (modulul 2), 3 și 4 (modulul 4).',
            'Prinde glisierele MOVENTO NL 500 cu câte 3 șuruburi Blum 3,5 × 15 la 37 / 261 / 293 mm de muchia din față, la cotele din „Desene de găurire”.'],
           extra={'explode': RA})
    S.step(2, 'Corpul culcat pe spate: baze, blaturi, laterale, despărțitori', 'culcat',
           ['Corpul are 3380 mm: lucrați pe podea, cu el culcat pe spate, în fața peretelui, și lăsați loc pentru ridicare.',
            'Baza și blatul sunt din 2 bucăți, cu îmbinarea sub și deasupra despărțitorului 2: despărțitorul se prinde cu confirmate în ambele bucăți.',
            'Bate cepurile și prinde bazele și blaturile de laterale și despărțitori cu confirmate. Măsoară diagonalele fiecărui modul.'],
           extra={'explode': {'bz_v': [0, 0, -140], 'bz_e': [0, 0, -140], 'bl_v': [0, 0, 140], 'bl_e': [0, 0, 140], 'lat1': [-140, 0, 0], 'lat2': [140, 0, 0]}})
    S.step(3, 'Polițele fixe de sus', 'culcat', ['Prinde polițele fixe DR-07 (modulele 1, 2, 4, 5) și DR-08 (modulul 3) la 2080 mm, cu confirmate și cepuri.'],
           extra={'explode': {k: [0, 160, 0] for k in ('ps1', 'ps2', 'ps3', 'ps4', 'ps5')}})
    S.step(4, 'Spatele HDF din 3 bucăți', 'spate',
           ['Spatele intră între laterale (încastrat 3 mm) și se prinde pe muchiile bazei, blatului și despărțitorilor, cu îmbinări pe despărțitorii 1 și 3.',
            'Prinde-l cu șuruburi 3,5 × 16 la ~150 mm; taie 3 decupaje de 45 × 20 mm sub blat pentru colțarele de perete.'],
           extra={'explode': {k: [0, -120, 0] for k in ('h1', 'h2', 'h3')}})
    S.step(5, 'Plăcile picioarelor și ridicarea', 'fata_sus',
           ['Prinde sub baze cele 12 plăci de picior (4 × 16).',
            'Ridicați corpul în 4 persoane, fără tuburile picioarelor (diagonala 2450 mm sub tavanul de ~2500 mm), apoi introduceți picioarele săltând pe rând câte o latură.'],
           warn=['Corpul de 3,4 m se îndoaie dacă e ridicat de la un capăt: ridicați-l uniform, cu câte o persoană la fiecare despărțitor.'], extra={'explode': {}})
    S.step(6, 'Nivelare, colțare de perete și soclu', 'fata', ['Nivelează din picioare; prinde 3 colțare sub blat, în perete.',
                                                             'Prinde clemele pe picioarele din față și apasă cele două bucăți de soclu DR-11 (retras 40 mm).'],
           extra={'explode': {'soc1': [0, 150, 0], 'soc2': [0, 150, 0]}})
    S.step(7, 'Barele de haine și LED-urile', 'fata', ['Modulul 1: 2 bare (la 980 și 1980 mm); modulul 5: 1 bară la 1980 mm. Profilele LED sub polițele de sus.'],
           extra={'explode': {}})
    S.step(8, 'Rafturile pe pini', 'fata', ['Modulul 2: 5 rafturi; modulul 3: 2; modulul 4: 3; modulul 5: 1 (jos, la 300 mm). Fiecare raft pe 4 pini Ø5.'],
           extra={'explode': {('r%d' % k): [0, 0, 100] for k in range(len(shelves))}})
    S.step(9, 'Sertarele interioare', 'fata',
           ['Asamblează cele 6 cutii (laterale DR-SI.L, față și spate DR-SI.FS de 18 mm, fund DR-SI.F retras 13 mm); fața de 18 mm e frontul sertarului interior.',
            'Găurile Ø6 × 10 pentru cârlig, clemele sub fund, apoi împinge cutiile pe glisiere.'],
           extra={'explode': {k: [0, 450, 0] for k in [p['id'] for p in S.parts if p['id'][:3] in ('a1.', 'a2.', 'b1.', 'b2.', 'b3.', 'b4.') and p['code'] != 'SL']}})
    S.step(10, 'Masa de călcat și coșul de rufe (modulul 3)', 'fata',
           ['Montează masa de călcat Häfele Ironfix 568.60.710 și coșul de rufe după fișele producătorilor, pe despărțitorii 2 și 3.'],
           extra={'explode': {'calcat': [0, 300, 0], 'cos': [0, 300, 0]}})
    S.step(11, 'Ușile: plăcuțe și balamale', 'fata_sus',
           ['Ușile de jos (2068 mm) au 5 balamale, cele de sus 2. Ușile M1 și M5 sunt aplicate pe laterale (70T3550); M2, M3 și M4 se prind pe despărțitorii 1, 2 și 3 (semiaplicate, 70T3650).',
            'Astfel fiecare despărțitor are plăcuțe pe o singură față: șuruburile de 15 mm nu se întâlnesc în placa de 18.'],
           extra={'explode': {k: [0, 280, 0] for k in [p['id'] for p in S.parts if p['id'][:2] in ('uj', 'us')]},
                  'detail': {'view': 'spate_usa', 'only': ['uj2'], 'hw': ['BA', 'D17'], 'text': 'Ușa de jos M2, din spate: 5 balamale semiaplicate 70T3650, fiecare cu 2 șuruburi 3,5 × 17.'}})
    S.step(12, 'TIP-ON și reglajul ușilor', 'jos_fata',
           ['Câte un TIP-ON pe ușă: sub polița de sus (ușile de jos) și sub blat (ușile de sus), lângă marginea de deschidere.',
            'Reglează rosturile: 2 mm între uși, 3 mm între ușa de jos și cea de sus.'],
           extra={'explode': {k: [0, 280, 0] for k in [p['id'] for p in S.parts if p['id'][:2] in ('uj', 'us')]}})
    S.step(13, 'Masca de tavan', 'fata_sus', ['Taie cele două măști (DR-14, DR-15) la înălțimea reală până la tavan și prinde-le pe blat cu colțare; îmbinarea vine în dreptul rostului M2/M3.'],
           extra={'explode': {'m1': [0, 0, 120], 'm2': [0, 0, 120]}})
    S.step(14, 'Capacele de confirmat', 'fata', ['Pune capacele pe confirmatele vizibile din interiorul modulelor.'], extra={'explode': {}})
    return finish(S, notes=['Stânga/dreapta = privit din față. Balamale: M1 și M5 aplicate (14 × 70T3550), M2–M4 semiaplicate (21 × 70T3650); devizul R04 are 6 + 29.',
                            'Sertare interioare Blum MOVENTO 760H5000S (NL 500): SKW = 680 − 42 = 638, SKL = 490.'],
                  extra=[('K', 'Profile LED 24 V + senzori de ușă', '1 set', 'sub polițele de sus', '7'),
                         ('HA', 'Masă de călcat Häfele Ironfix 568.60.710 + coș de rufe extractibil', '1 + 1', 'modulul 3, după fișa producătorului', '10')])
