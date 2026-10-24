"""Specificatii de montaj R04 pentru dulapurile inalte: dulap hol, dressing, spalatorie (dulapul din dormitor e separat).
Coordonate locale: mm, fata = +y, sus = +z, pardoseala la z = 0. x mic = dreapta privit din fata.
Dimensiunile pieselor sunt din planul de debitare R03; pozitiile din modelele FreeCAD (inventar 07.10.2026)."""
import math
from montaj_specs import Spec, drawer
import montaj_hw, montaj_lib as L
from montaj_comun import B, caps, finish, R03

VIEWS = {'spate_usa': [0.45, -1.0, 0.4], 'dedesubt': [-0.45, 0.7, -1.0], 'jos_fata': [0.4, 1.0, -0.55], 'culcat': [0.35, 0.6, 1.0],
         'fata_sus': [0.3, 1.0, 0.35]}


def poly_part(S, pid, code, label, pts, z0, h, step, mat=None, role='panel'):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    B(S, pid, code, label, min(xs), max(xs), min(ys), max(ys), z0, z0 + h, step, mat=mat, role=role)
    S.parts[-1]['poly'] = [list(p) for p in pts]
    return S.parts[-1]


def bracket_under_top(S, step, x, y_back, z_top_under, letter='L'):
    """colțar anti-rasturnare sub blatul corpului, cu aripa in jos prin decupajul din spatele HDF, prins in perete"""
    at = (x, y_back, z_top_under)
    S.hw_at(step, 'coltar_40', at, az=(0, 0, -1), ax=(-1, 0, 0), explode=50, letter=letter, dash=False)
    for yy in (14.0, 30.0):
        S.hw_at(step, 'surub_4x16', (x - 10, y_back + yy, z_top_under - 2.0), az=(0, 0, -1), explode=80, letter='I')
    S.hw_at(step, 'diblu_6x40', (x - 10, y_back, z_top_under - 30.0), az=(0, 1, 0), explode=70, letter='T')
    S.hw_at(step, 'surub_4x40', (x - 10, y_back + 2.0, z_top_under - 30.0), az=(0, 1, 0), explode=120, letter='U')


def clothes_rail(S, step, x0, x1, y, z, tag):
    L_ = x1 - x0 - 6
    S.hw_at(step, 'suport_bara', (x0, y, z), az=(0, 0, 1), ax=(1, 0, 0), explode=40, letter='SB', dash=False, tag=tag)
    S.hw_at(step, 'suport_bara', (x1, y, z), az=(0, 0, 1), ax=(-1, 0, 0), explode=40, letter='SB', dash=False, tag=tag)
    for x, sx in ((x0, 1), (x1, -1)):
        for k in range(3):
            a = math.radians(90 + 120 * k)
            S.hw_at(step, 'surub_4x16', (x + sx * 3.0, y + 21.5 * math.cos(a), z + 21.5 * math.sin(a)), az=(sx, 0, 0), explode=40, letter='I', tag=tag)
    S.hw_at(step, 'bara_ovala@%d' % round(L_), (x0 + 3, y, z), az=(0, 0, 1), ax=(1, 0, 0), explode=-120, letter='BO', dash=False, tag=tag)


# ================================================================== DULAP HOL
def dulap_hol():
    S = Spec('dulap_hol', 'Dulap hol', 'Dulap pe hol cu uși oglindă',
             'Hol, pe peretele de sud, între ușa de intrare și colțul oblic', (2453, 598, 2497),
             'Dulap de 2453 × 580 × 2380 mm pe 10 picioare (soclu retras de 80 mm), cu latura dreaptă oblică (14,5°): două module cu bară de haine și '
             'câte un sertar Blum MOVENTO jos, un colț cu 4 rafturi, 8 uși cashmere cu oglindă lipită, fără mâner (TIP-ON).')
    S.views = dict(VIEWS)
    Z0, Z1 = 80.0, 2460.0
    # --- corp
    B(S, 'lat', 'DH-C01', 'Lateral drept (în R03: „stânga”)', 0, 18, 0, 580, Z0, Z1, 2)
    obl = [(2285.0, 0.0), (2435.0, 580.0), (2452.4, 575.5), (2302.4, -4.5)]
    poly_part(S, 'obl', 'DH-C02', 'Lateral oblic 14,5° (în R03: „dreapta”)', obl, Z0, Z1 - Z0, 2, role='oblic')
    trap = [(18.0, 0.0), (2285.0, 0.0), (2435.0, 580.0), (18.0, 580.0)]
    poly_part(S, 'baza', 'DH-C03', 'Bază (trapez)', trap, Z0, 18, 2)
    poly_part(S, 'blat', 'DH-C04', 'Blat sus (trapez)', trap, Z1 - 18, 18, 2)
    B(S, 'div_c', 'DH-C05', 'Despărțitor central', 1035, 1053, 0, 577, Z0 + 18, Z1 - 18, 1)
    B(S, 'div_k', 'DH-C06', 'Despărțitor colț', 2080, 2098, 0, 577, Z0 + 18, Z1 - 18, 1)
    for i, z in enumerate((360.0, 2080.0)):
        B(S, 'pA%d' % i, 'DH-C07', 'Poliță fixă modul A (dreapta)', 18, 1035, 0, 557, z, z + 18, 3)
        B(S, 'pB%d' % i, 'DH-C08', 'Poliță fixă modul B (mijloc)', 1053, 2080, 0, 557, z, z + 18, 3)
    B(S, 'h1', 'DH-H01', 'Spate HDF (modul A)', 0, 1044, -3, 0, Z0 + 2, Z1 - 2, 4)
    B(S, 'h2', 'DH-H02', 'Spate HDF (modul B + colț)', 1044, 2300, -3, 0, Z0 + 2, Z1 - 2, 4)
    B(S, 'perete', 'PERETE', 'Peretele de sud', -80, 2600, -63, -3, 0, 2500, 6, mat='perete', role='context')
    B(S, 'soclu', 'DH-C10', 'Soclu retras', 18, 2414, 520, 538, 0, 80, 6)
    for i, z in enumerate((500.0, 900.0, 1300.0, 1700.0)):
        poly_part(S, 'rk%d' % i, 'DH-C09', 'Raft colț (trapez)', [(2098.0, 0.0), (2286.0, 0.0), (2435.0, 577.0), (2098.0, 577.0)], z, 18, 8, role='shelf')
    # sertare MOVENTO NL 500 (deviz: 760H5000S + TIP-ON BLUMOTION)
    gA = drawer(S, 'sA', 'DH-S', 18, 580, Z0 + 19, 1017, 500, 200, 10, 1, 11, (2, 580, 10, 1041, 18, 366), 'DH-F03', 'Front sertar modul A', step_tob=9,
                fs_t=16.0, side_r='lat', side_l='div_c', codes=dict(L='DH-S01', FS='DH-S02', F='DH-S04'), offs_l=(69, 133, 229))
    gB = drawer(S, 'sB', 'DH-S', 1053, 580, Z0 + 19, 1027, 500, 200, 10, 1, 11, (1046, 580, 10, 1042, 18, 366), 'DH-F04', 'Front sertar modul B', step_tob=9,
                fs_t=16.0, side_r='div_c', side_l='div_k', codes=dict(L='DH-S01', FS='DH-S03', F='DH-S05'))
    # usi: 4 jos (1699) + 4 sus (377); usa 1 aplicata pe lateral, celelalte semiaplicate pe despartitori
    X = [(2, 521), (524, 1043), (1046, 1565), (1568, 2087)]
    for i, (a, b) in enumerate(X, 1):
        B(S, 'uj%d' % i, 'DH-F01', 'Ușă jos %d (suport oglindă)' % i, a, b, 580, 598, 380, 2079, 12, role='door')
        B(S, 'us%d' % i, 'DH-F02', 'Ușă sus %d' % i, a, b, 580, 598, 2082, 2459, 12, role='door')
    B(S, 'plinta', 'DH-F05', 'Plintă colț', 2090, 2453, 580, 598, 10, 98, 15)
    B(S, 'masca', 'DH-F06', 'Mască tavan (se ajustează pe tavan)', 0, 2453, 580, 598, 2460, 2497, 15)
    for i, (a, b) in enumerate(X, 1):
        B(S, 'og%d' % i, 'OGL', 'Oglindă 4 mm (lipită)', a + 3, b - 3, 598, 602, 383, 2076, 14, mat='oglinda', role='door')
    for k, (a, b) in enumerate(((28, 1025), (1063, 2070))):
        B(S, 'led%d' % k, 'LED', 'Profil LED sub polița de sus', a, b, 515, 532, 2072, 2080, 7, mat='led', role='hw')
    # --- feronerie pozitionata
    sides = {1: 'lat', 2: 'div_c', 3: 'div_c', 4: 'div_k'}
    for i in range(1, 5):
        tip = '70T3550' if i == 1 else '70T3650'
        L.hinges(S, 12, 'uj%d' % i, sides[i], tip)
        L.hinges(S, 12, 'us%d' % i, sides[i], tip)
    open_x = {1: 481, 2: 564, 3: 1525, 4: 1608}
    for i in range(1, 5):
        L.tipon(S, 13, 'uj%d' % i, 'pA1' if i <= 2 else 'pB1', open_x[i])
        L.tipon(S, 13, 'us%d' % i, 'blat', open_x[i])
    L.back_screws(S, 4, 'h1')
    L.back_screws(S, 4, 'h2')
    legs = [(60, 60), (60, 460), (600, 60), (600, 460), (1150, 60), (1150, 460), (1700, 60), (1700, 460), (2220, 60), (2220, 460)]
    L.legs(S, 5, 'baza', legs, h=80)
    for x in (60, 600, 1150, 1700, 2220):
        S.hw_at(6, 'clema_soclu', (x, 460, 20.0), az=(0, 0, 1), ax=(1, 0, 0), explode=0, letter='CS', dash=False)
    for x in (300.0, 1250.0, 2000.0):
        bracket_under_top(S, 6, x, -3.0, Z1 - 18)
    clothes_rail(S, 7, 18, 1035, 290, 1950, 'A')
    clothes_rail(S, 7, 1053, 2080, 290, 1950, 'B')
    for k in range(4):
        L.shelf_pins(S, 8, 'rk%d' % k, 'div_k', 'obl_pin') if False else None
    # rafturile de colt: pini in despartitorul de colt si in lateralul oblic (gaurile pe oblic se dau dupa sablon)
    for k, z in enumerate((500.0, 900.0, 1300.0, 1700.0)):
        for yy in (37.0, 520.0):
            S.hw_at(8, 'pin_raft', (2098.0, yy, z - 4.2), az=(1, 0, 0), ax=(0, -1, 0), attach='div_k', explode=30, letter='PR')
            L.hole(next(p for p in S.parts if p['id'] == 'div_k'), 'pin5', (2098.0, yy, z - 4.2), (1, 0, 0), 5.0, 12.0, 'pin raft colț')
            xo = 2285.0 + 150.0 * yy / 580.0
            S.hw_at(8, 'pin_raft', (xo, yy, z - 4.2), az=(-0.968, 0.25, 0), explode=30, letter='PR')
    # confirmatele lateralului oblic (imbinare inclinata, date manual): 3 jos, 3 sus
    n = (0.9682, -0.2504, 0.0)
    for zc, step in ((Z0 + 9, 2), (Z1 - 9, 2)):
        for t in (60.0, 300.0, 540.0):
            px, py = 2285.0 + 150.0 * t / 580.0, t
            S.hw_at(step, 'confirmat', (px + n[0] * 18, py + n[1] * 18, zc), az=n, attach='obl', explode=45, letter='A')
    S.skip_joints += [('obl', 'baza'), ('obl', 'blat')]
    # masca de tavan: 4 colțare pe blat
    for x in (300.0, 900.0, 1500.0, 2100.0):
        S.hw_at(15, 'coltar_40', (x, 580.0, Z1), az=(0, 0, 1), ax=(-1, 0, 0), explode=40, letter='L', dash=False)
    montaj_hw.auto(S)
    caps(S, 16, ('lat', 'div_c', 'div_k', 'pA0', 'pA1', 'pB0', 'pB1'))
    S.final_views = ['fata']
    S.gbox = (7250, -5550, 9703, -4952)
    S.front_detail = True
    S.front_step = 11
    S.time = '≈ 2 zile (2 persoane)'
    S.people = '2 (plăcile de 2380 mm și ridicarea corpului)'
    S.wall = dict(kind='antirasturnare', unit_h=2380, note='3 colțare sub blatul corpului, prin decupaje în spatele HDF. Dulapul înalt nu se lasă niciodată neprins de perete.')
    S.pre = ['Pardoseala holului e finită; peretele de sud e vopsit.', 'Senzorii de ușă și sursa LED 24 V au alimentarea adusă în colțul de sus.',
             'Înălțimea reală sub tavan e măsurată în 3 puncte (proiect: ~2500 mm).']
    RA = {'sA.rl': [40, 0, 0], 'sA.rr': [-40, 0, 0], 'sB.rl': [40, 0, 0], 'sB.rr': [-40, 0, 0]}
    S.step(1, 'Glisierele pe lateral și pe despărțitori (pe podea)', 'culcat',
           ['Pune lateralul DH-C01 și despărțitorii DH-C05 și DH-C06 pe covor, cu fața pe care vin glisierele în sus.',
            'Trasează axa șuruburilor la %g mm de muchia de jos a plăcilor (cu +1 mm pentru montajul înainte de asamblare).' % (gA['screw_z'] - Z0 - 18 + 18),
            'Prinde glisierele MOVENTO NL 500 cu câte 3 șuruburi Blum 3,5 × 15 la 37 / 261 / 293 mm de muchia din față.',
            'Despărțitorul central primește glisiere pe ambele fețe: pe fața modulului A la 69 / 133 / 229 mm, ca șuruburile să nu se întâlnească.'],
           extra={'explode': dict(RA)})
    S.step(2, 'Corpul culcat pe spate: bază, blat, lateral, despărțitori, lateral oblic', 'culcat',
           ['Lucrați în doi, pe covor, cu corpul culcat pe spate în fața peretelui (nu în mijlocul holului).',
            'Bate cepurile, apoi prinde baza și blatul (trapeze) de lateralul DH-C01 și de despărțitori, cu confirmate.',
            'Lateralul oblic DH-C02 se prinde la urmă: 3 confirmate jos și 3 sus, perpendicular pe el, la 60, 300 și 540 mm de muchia din spate.',
            'Măsoară diagonalele modulelor A și B; diferență sub 3 mm.'],
           warn=['Baza și blatul au capătul tăiat oblic: verifică pe placă latura din spate (2267 mm) înainte de găurire.'],
           extra={'explode': {'baza': [0, 0, -150], 'blat': [0, 0, 150], 'obl': [150, 0, 0], 'lat': [-150, 0, 0]}})
    S.step(3, 'Polițele fixe', 'culcat', ['Prinde polițele DH-C07 (modulul A) și DH-C08 (modulul B) la 360 mm (deasupra sertarului) și la 2080 mm, cu confirmate și cepuri.'],
           extra={'explode': {k: [0, 160, 0] for k in ('pA0', 'pA1', 'pB0', 'pB1')}})
    S.step(4, 'Spatele HDF din două bucăți', 'spate',
           ['Spatele vine din 2 bucăți (DH-H01 și DH-H02), cu îmbinarea pe muchia din spate a despărțitorului central.',
            'Verifică diagonalele, apoi prinde HDF-ul cu șuruburi 3,5 × 16 la ~150 mm în bază, blat, lateral și despărțitori.',
            'Taie 3 decupaje de 45 × 20 mm sub blat (la 300, 1250 și 2000 mm) pentru colțarele de perete.'],
           extra={'explode': {'h1': [0, -120, 0], 'h2': [0, -120, 0]}})
    S.step(5, 'Plăcile picioarelor și ridicarea corpului', 'fata_sus',
           ['Cât corpul e culcat, prinde sub bază cele 10 plăci de picior, fiecare cu 4 șuruburi 4 × 16.',
            'Ridică dulapul FĂRĂ tuburile picioarelor: diagonala corpului e 2450 mm; cu picioarele (2527 mm) nu încape sub tavan (~2500 mm).',
            'După ridicare, săltă pe rând câte o latură cu o pârghie și introdu picioarele în plăci.'],
           warn=['Verifică înainte înălțimea reală sub tavan; dacă e sub 2460 mm, corpul trebuie asamblat în picioare, pe loc.'],
           extra={'explode': {}})
    S.step(6, 'Poziționare, nivelare, colțare de perete și soclu', 'fata',
           ['Împinge corpul la perete și nivelează-l din picioare (în față și în lateral).',
            'Prinde cele 3 colțare sub blat: în blat cu 2 șuruburi 4 × 16, în perete cu diblu Ø6 × 40 și șurub 4 × 40.',
            'Prinde clemele de soclu pe picioarele din față și apasă soclul retras DH-C10 în cleme.'],
           extra={'explode': {'soclu': [0, 150, 0]}})
    S.step(7, 'Barele de haine și LED-urile', 'fata', ['Prinde suporții barelor la 1950 mm, câte 3 șuruburi 4 × 16, și pune barele ovale tăiate la lungime.',
                                                        'Lipește profilele LED sub polițele de sus, la 50 mm de muchia din față.'], extra={'explode': {}})
    S.step(8, 'Rafturile de colț pe pini', 'fata', ['Pune câte 4 pini în rândurile de găuri din despărțitorul de colț și din lateralul oblic și așază rafturile DH-C09 (trapez).'],
           extra={'explode': {k: [0, 0, 120] for k in ('rk0', 'rk1', 'rk2', 'rk3')}})
    S.step(9, 'TIP-ON BLUMOTION și barele de sincronizare', 'fata',
           ['Clipsează unitățile TIP-ON BLUMOTION pe glisiere.', 'Taie barele de sincronizare la %d mm (modulul A) și %d mm (modulul B).' % (gA['rod'], gB['rod'])],
           extra={'explode': {}})
    S.step(10, 'Cutiile de sertar și clemele', 'fata',
           ['Asamblează cutiile din PAL 16 (laterale DH-S01, față/spate DH-S02 și DH-S03, funduri DH-S04 și DH-S05), fundul retras 13 mm.',
            'Găurile Ø6 × 10 pentru cârlig în spatele lateralelor; clemele sub fund; împinge cutiile pe glisiere.'],
           extra={'explode': {k: [0, 450, 0] for k in [p['id'] for p in S.parts if p['id'][:3] in ('sA.', 'sB.') and p['code'] != 'SL' and not p['id'].endswith('.fr')]}})
    S.step(11, 'Fronturile de sertar', 'fata', ['Fixează fronturile DH-F03 și DH-F04 după paginile de detaliu.'],
           extra={'explode': {'sA.fr': [0, 120, 0], 'sB.fr': [0, 120, 0]}})
    S.step(12, 'Ușile: plăcuțe și balamale', 'fata_sus',
           ['Ușile jos au 4 balamale, cele de sus 2. Ușa 1 (lângă lateral) are balamale aplicate 70T3550; ușile 2–4 se întâlnesc pe despărțitori și au balamale semiaplicate 70T3650.',
            'Cupele Ø35 × 13 se fac la atelier (lotul M104); prinde balamalele cu 3,5 × 17 și plăcuțele cu 3,5 × 15 la 37 mm de muchia din față.',
            'Agață ușile de jos înainte de cele de sus; lasă 3 mm între ușa de jos și cea de sus.'],
           extra={'explode': {k: [0, 280, 0] for k in [p['id'] for p in S.parts if p['id'][:2] in ('uj', 'us')]},
                  'detail': {'view': 'spate_usa', 'only': ['uj2'], 'hw': ['BA', 'D17'],
                             'text': 'Ușa de jos 2, din spate: 4 balamale semiaplicate 70T3650, fiecare cu 2 șuruburi 3,5 × 17.'}})
    S.step(13, 'TIP-ON pe uși și reglajul', 'jos_fata', ['Prinde adaptoarele TIP-ON sub polițele de sus (ușile de jos) și sub blat (ușile de sus), în dreptul marginii de deschidere.',
                                                        'Pune plăcile metalice pe uși și reglează rosturile: 3 mm între uși, ușile drepte și în același plan.'],
           extra={'explode': {k: [0, 280, 0] for k in [p['id'] for p in S.parts if p['id'][:2] in ('uj', 'us')]}})
    S.step(14, 'Oglinzile pe ușile de jos', 'fata', ['După reglaj, dă ușile jos pe rând, curăță fața cu alcool izopropilic și lipește oglinzile de 4 mm cu adeziv pentru oglinzi (MS polimer, în benzi verticale).',
                                                     'Ține oglinda cu bandă adezivă 24 de ore, cu ușa culcată, apoi agaț-o la loc.'],
           warn=['Nu folosi silicon acetic: pătează spatele oglinzii.'], extra={'explode': {k: [0, 120, 0] for k in ('og1', 'og2', 'og3', 'og4')}})
    S.step(15, 'Masca de tavan, plinta de colț și capacele', 'fata_sus',
           ['Taie masca DH-F06 la înălțimea reală dintre corp și tavan (proiect: 37 mm din 60) și prinde-o cu 4 colțare pe blat.',
            'Lipește plinta de colț DH-F05 pe picioarele din colț; pune capacele de confirmat.'],
           extra={'explode': {'masca': [0, 0, 120], 'plinta': [0, 100, 0]}})
    return finish(S, notes=['Stânga/dreapta = privit din față. În R03, DH-C01 e numit „lateral stânga” și DH-C02 „lateral oblic (dreapta)”: denumirile din R03 sunt privite dinspre spate.',
                            'Cote Blum MOVENTO 760H5000S (NL 500): SKW = LW − 42 (975 / 985); SKL = 490; bare de sincronizare %d / %d mm.' % (gA['rod'], gB['rod'])],
                  extra=[('OG', 'Oglindă 4 mm (4 bucăți) + adeziv pentru oglinzi', '4', 'pe ușile de jos', '14'), ('K', 'Profile LED 24 V + senzori de ușă', '1 set', 'sub polițele de sus', '7')])
