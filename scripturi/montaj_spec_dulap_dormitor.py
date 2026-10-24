"""Specificatie de montaj R04: dulapul din dormitor (model Codex, 2200 x 578 x 2280 pe soclu 80). Coordonate = FreeCAD dulap_dormitor (fata = +y).
Piese din R03 (DD-xx). Sertarele interioare sunt PROVIZORII in R03 (atingeau balamalele): aici sunt retrase cu 45 mm (fronturile la 515 mm),
propunere de rezolvare fara schimbarea dimensiunilor. Balamalele usilor 2 si 3 (pe despartitorul din mijloc) sunt decalate cu 40 mm."""
from montaj_specs import Spec
import montaj_hw, montaj_lib as L
from montaj_comun import B, caps, finish
from montaj_spec_dulapuri import VIEWS, bracket_under_top, clothes_rail

L.HINGE_MODEL.setdefault('71B3650', 'balama_70T3650')
PX = [(0.0, 18.0), (545.5, 563.5), (1091.0, 1109.0), (1636.5, 1654.5), (2182.0, 2200.0)]
MODS = [(18.0, 545.5), (563.5, 1091.0), (1109.0, 1636.5), (1654.5, 2182.0)]
FR_Y = 515.0                      # fata din fata a fronturilor interioare (retrase; in modelul Codex 558)
DRW = [('pij', 'DD-F188', 'DD-S180', 113.0, 188.0, 180.0), ('sos', 'DD-F168', 'DD-S160', 318.0, 168.0, 160.0),
       ('len', 'DD-F168L', 'DD-S160', 503.0, 168.0, 160.0), ('cea', 'DD-F103', 'DD-S95', 688.0, 103.0, 95.0)]


def interior_drawers(S, who, mod, step_slides, step_box):
    a, b = MODS[mod]
    pr, pl = 'p%d' % mod, 'p%d' % (mod + 1)
    for tag, cf, cs, z0, fh, H in DRW:
        t = '%s.%s' % (who, tag)
        yf = FR_Y - 18 - 4                     # spatele frontului (4 mm joc)
        zb = z0 + (fh - H) / 2
        ox = a + 16.0
        B(S, t + '.l1', cs + '.L', 'Lateral cutie sertar', ox, ox + 18, yf - 450, yf, zb, zb + H, step_box, mat='sertar')
        B(S, t + '.l2', cs + '.L', 'Lateral cutie sertar', b - 16 - 18, b - 16, yf - 450, yf, zb, zb + H, step_box, mat='sertar')
        B(S, t + '.fu', cs + '.F', 'Fund cutie sertar', ox + 18, b - 34, yf - 450, yf, zb, zb + 18, step_box, mat='sertar')
        B(S, t + '.fa', cs + '.FS', 'Față interioară cutie', ox + 18, b - 34, yf - 18, yf, zb + 18, zb + H, step_box, mat='sertar')
        B(S, t + '.sp', cs + '.FS', 'Spate cutie', ox + 18, b - 34, yf - 450, yf - 432, zb + 18, zb + H, step_box, mat='sertar')
        B(S, t + '.fr', cf, 'Front sertar interior', a + 3, b - 3, FR_Y - 18, FR_Y, z0, z0 + fh, step_box + 1, role='door')
        zc = zb + H / 2
        S.hw_at(step_slides, 'glisiera_bile_450', (a, yf, zc), az=(0, 0, 1), ax=(1, 0, 0), attach=pr, explode=0, letter='GB', dash=False)
        S.hw_at(step_slides, 'glisiera_bile_450', (b, yf, zc), az=(0, 0, 1), ax=(1, 0, 0), mirror=True, attach=pl, explode=0, letter='GB', dash=False)
        for x, sx, pid in ((a, 1, pr), (b, -1, pl)):
            for off in (35.0, 163.0, 355.0):
                S.hw_at(step_slides, 'surub_3_5x15', (x + sx * 1.2, yf - off, zc), az=(sx, 0, 0), attach=pid, explode=50, letter='D15')
                L.hole(next(p for p in S.parts if p['id'] == pid), 'pil25', (x, yf - off, zc), (sx, 0, 0), 2.5, 12, 'glisieră cu bile')
        for xx in (a + 3 + 60, b - 3 - 60):
            for zz in (z0 + 25, z0 + fh - 25):
                S.hw_at(step_box + 1, 'surub_4x25', (xx, yf - 3.0, zz), az=(0, -1, 0), attach=t + '.fa', explode=50, letter='N')


def dulap_dormitor():
    S = Spec('dulap_dormitor', 'Dulap dormitor', 'Dulap dormitor, 2 persoane',
             'Dormitor, pe peretele de nord, în stânga ușii', (2200, 596, 2360),
             'Dulap de 2200 × 578 × 2280 mm pe soclu negru de 80 mm, în 4 module de 527,5 mm (câte 2 pentru fiecare persoană): sertare interioare, rafturi, '
             'bară de cămăși și suport extractibil de pantaloni, 4 uși albe de 2276 mm cu 5 balamale Blum CLIP top BLUMOTION și mâner negru.')
    S.views = dict(VIEWS)
    Z0, Z1 = 80.0, 2360.0
    B(S, 'baza', 'DD-01', 'Bază', 0, 2200, 0, 578, Z0, Z0 + 18, 2)
    B(S, 'capac', 'DD-01', 'Capac', 0, 2200, 0, 578, Z1 - 18, Z1, 2)
    for i, (a, b) in enumerate(PX):
        B(S, 'p%d' % i, 'DD-02', 'Lateral' if i in (0, 4) else 'Despărțitor %d' % i, a, b, 0, 578, Z0 + 18, Z1 - 18, 1)
    for i, (a, b) in enumerate(MODS):
        B(S, 'sz%d' % i, 'DD-04', 'Raft fix depozitare sezonieră M%d' % (i + 1), a, b, 26, 561, 2050, 2068, 3)
    for i in (1, 2):
        a, b = MODS[i]
        B(S, 'ri%d' % i, 'DD-06', 'Raft inferior pentru cutii M%d' % (i + 1), a, b, 26, 546, 240, 258, 3)
    hd = [('h1', 'DD-03', 0, 554.5), ('h2', 'DD-03b', 554.5, 1100), ('h3', 'DD-03b', 1100, 1645.5), ('h4', 'DD-03', 1645.5, 2200)]
    for pid, code, a, b in hd:
        B(S, pid, code, 'Spate HDF ' + code, a, b, -3, 0, Z0 + 18, Z1, 4)
    B(S, 'perete', 'PERETE', 'Peretele de nord', -80, 2280, -63, -3, 0, 2500, 6, mat='perete', role='context')
    B(S, 'soclu', 'SOCLU', 'Soclu negru 80 mm (profil cumpărat)', 0, 2200, 538, 558, 0, 80, 6, mat='hw', role='hw')
    for k, z in enumerate((810.0, 1080.0, 1350.0, 1620.0, 1890.0)):
        for who, m in (('A', 0), ('B', 3)):
            a, b = MODS[m]
            B(S, 'rr%s%d' % (who, k), 'DD-05', 'Raft reglabil tricouri %s' % who, a + 1, b - 1, 26, 541, z, z + 18, 8, role='shelf')
    interior_drawers(S, 'A', 0, 1, 9)
    interior_drawers(S, 'B', 3, 1, 9)
    for who, m in (('A', 1), ('B', 2)):
        a, b = MODS[m]
        B(S, 'pant%s' % who, 'PANT', 'Suport pantaloni extractibil %s (produs)' % who, a + 25, b - 25, 62, 522, 960, 984, 7, mat='metal', role='hw')
        clothes_rail(S, 7, a, b, 302, 1940, who)
    doors = [(2, 548), (552, 1098), (1102, 1648), (1652, 2198)]
    for i, (a, b) in enumerate(doors, 1):
        B(S, 'u%d' % i, 'DD-07', 'Ușă %d' % i, a, b, 578, 596, 82, 2358, 11, role='door')
    zs = [200.0, 650.0, 1130.0, 1650.0, 2220.0]
    L.hinges(S, 11, 'u1', 'p0', '71B3550', zs=zs)
    L.hinges(S, 11, 'u2', 'p2', '71B3650', zs=zs)
    L.hinges(S, 11, 'u3', 'p2', '71B3650', zs=[z + 40 for z in zs])
    L.hinges(S, 11, 'u4', 'p4', '71B3550', zs=zs)
    for pid, code, a, b in hd:
        L.back_screws(S, 4, pid)
    L.legs(S, 5, 'baza', [(x, y) for x in (60.0, 820.0, 1380.0, 2140.0) for y in (60.0, 470.0)], h=80)
    for x in (60.0, 820.0, 1380.0, 2140.0):
        S.hw_at(6, 'clema_soclu', (x, 470, 20.0), az=(0, 0, 1), ax=(1, 0, 0), explode=0, letter='CS', dash=False)
    for x in (280.0, 830.0, 1370.0, 1920.0):
        bracket_under_top(S, 6, x, -3.0, Z1 - 18)
    for k in range(5):
        for who, (l_, r_) in (('A', ('p0', 'p1')), ('B', ('p3', 'p4'))):
            L.shelf_pins(S, 8, 'rr%s%d' % (who, k), l_, r_)
    montaj_hw.auto(S)
    caps(S, 12, tuple('p%d' % i for i in range(5)) + tuple('sz%d' % i for i in range(4)))
    S.final_views = ['fata']
    S.gbox = (150, -3845, 2350, -3223)
    S.front_detail = False
    S.time = '≈ 2 zile'
    S.people = '2'
    S.wall = dict(kind='antirasturnare', unit_h=2280, note='4 colțare sub capac, prin decupaje în spatele HDF; dulapul cu uși grele se răstoarnă ușor dacă nu e prins.')
    S.pre = ['Pardoseala e finită, peretele de nord vopsit; priza din spatele dulapului (sus dreapta) e accesibilă prin decupajul din spate.',
             'Sursa LED 24 V / 60 W și distribuitorul au loc în modulul 4, sus.']
    RA = {}
    S.step(1, 'Glisierele cu bile pe panouri (pe podea)', 'culcat',
           ['Sertarele interioare sunt în modulul 1 (persoana A) și în modulul 4 (persoana B), câte 4 pe modul: pijamale, șosete, lenjerie, ceasuri.',
            'Prinde glisierele cu bile de 450 mm (extragere totală, soft-close) pe lateralul și pe despărțitorul fiecărui modul, cu câte 3 șuruburi 3,5 × 15.',
            'Glisierele încep la 22 mm în spatele muchiei din față a panourilor: sertarele sunt retrase ca să nu atingă balamalele ușilor.'],
           warn=['Sertarele sunt PROVIZORII în R03: verifică glisierele cumpărate (450 mm, 12,7 mm grosime) înainte de găurire.'], extra={'explode': {}})
    S.step(2, 'Corpul culcat pe spate: bază, capac, laterale și despărțitori', 'culcat',
           ['Bate cepurile și prinde baza și capacul (DD-01) de cele 5 panouri DD-02 cu confirmate, la 527,5 mm lumină între ele.',
            'Măsoară diagonalele fiecărui modul (sub 2 mm diferență).'],
           extra={'explode': {'baza': [0, 0, -140], 'capac': [0, 0, 140], 'p0': [-140, 0, 0], 'p4': [140, 0, 0]}})
    S.step(3, 'Rafturile fixe', 'culcat', ['Rafturile de depozitare sezonieră DD-04 la 2050 mm în toate modulele și rafturile inferioare DD-06 la 240 mm în modulele 2 și 3, cu confirmate și cepuri.'],
           extra={'explode': {k: [0, 160, 0] for k in ('sz0', 'sz1', 'sz2', 'sz3', 'ri1', 'ri2')}})
    S.step(4, 'Spatele HDF din 4 bucăți', 'spate', ['Spatele vine din 4 bucăți cu îmbinările pe axele despărțitorilor; prinde-l cu 3,5 × 16 la ~150 mm.',
                                                    'Taie decupajul pentru priza din spatele dulapului (sus, dreapta) și 4 decupaje de 45 × 20 mm sub capac pentru colțarele de perete.'],
           extra={'explode': {k: [0, -120, 0] for k in ('h1', 'h2', 'h3', 'h4')}})
    S.step(5, 'Picioarele și ridicarea', 'fata_sus', ['Prinde cele 8 picioare de 80 mm sub bază. Cu picioarele, diagonala e 2430 mm: încape sub tavan, dar ridicați corpul în doi, încet.'],
           extra={'explode': {}})
    S.step(6, 'Nivelare, colțare de perete și soclu', 'fata', ['Nivelează din picioare; prinde cele 4 colțare sub capac, în perete.',
                                                             'Prinde soclul negru de 80 mm (profil cumpărat) pe clemele de pe picioarele din față.'], extra={'explode': {'soclu': [0, 150, 0]}})
    S.step(7, 'Barele de cămăși, suporturile de pantaloni și LED-urile', 'fata',
           ['Modulele 2 și 3: bara de cămăși la 1940 mm și suportul extractibil de pantaloni la 960 mm (după fișa produsului).',
            'Profilele LED cu senzor de deschidere pe muchiile din față ale panourilor; sursa și distribuitorul în modulul 4, sus.'], extra={'explode': {}})
    S.step(8, 'Rafturile reglabile', 'fata', ['5 rafturi DD-05 în modulul 1 și 5 în modulul 4, pe câte 4 pini Ø5 (rânduri de găuri la 32 mm).'],
           extra={'explode': {p['id']: [0, 0, 100] for p in S.parts if p['id'].startswith('rr')}})
    S.step(9, 'Cutiile sertarelor interioare', 'fata', ['Asamblează cele 8 cutii din PAL 18 (laterale, fund între laterale, față și spate pe fund) și prinde-le pe glisiere.'],
           extra={'explode': {p['id']: [0, 400, 0] for p in S.parts if p['id'][:2] in ('A.', 'B.') and not p['id'].endswith('.fr')}})
    S.step(10, 'Fronturile sertarelor interioare', 'fata', ['Prinde fronturile interioare pe cutii din interior (4 șuruburi 4 × 25 cu șaibă); fronturile sunt la 515 mm de perete, în spatele brațelor balamalelor.',
                                                                       'Montează mânerele negre: 240 mm pe uși (la 980–1220 mm), 120 mm pe fronturile interioare. Reglează ușile din balamale.'],
           extra={'explode': {p['id']: [0, 120, 0] for p in S.parts if p['id'].endswith('.fr')}})
    S.step(11, 'Ușile: plăcuțe, balamale BLUMOTION și mânere', 'fata_sus',
           ['Fiecare ușă are 5 balamale cu amortizare (CLIP top BLUMOTION). Ușile 1 și 4 sunt aplicate pe laterale (71B3550).',
            'Mânerele negre de 240 mm se montează pe uși la 980–1220 mm, înainte de agățare.',
            'Ușile 2 și 3 se întâlnesc pe despărțitorul din mijloc: balamale semiaplicate (71B3650), iar cele ale ușii 3 sunt decalate cu 40 mm în sus, ca plăcuțele de pe cele două fețe ale despărțitorului să nu aibă șuruburile în același punct.'],
           warn=['Devizul R04 are 20 × 71B3550: pentru ușile 2 și 3 sunt necesare 10 × 71B3650 (semiaplicate).'],
           extra={'explode': {'u1': [0, 260, 0], 'u2': [0, 260, 0], 'u3': [0, 260, 0], 'u4': [0, 260, 0]},
                  'detail': {'view': 'spate_usa', 'only': ['u3'], 'hw': ['BA', 'D17'], 'text': 'Ușa 3, din spate: 5 balamale semiaplicate 71B3650, decalate cu 40 mm față de ușa 2.'}})
    S.step(12, 'Capacele de confirmat', 'fata', ['Pune capacele pe confirmatele vizibile din module.'], extra={'explode': {}})
    return finish(S, notes=['PROPUNERE pentru sertarele interioare (provizorii în R03): fronturile retrase la 515 mm de perete (în model 558), ca să nu atingă brațele balamalelor; '
                            'dimensiunile pieselor rămân cele din R03.',
                            'Balamale: ușile 1 și 4 aplicate (71B3550), ușile 2 și 3 semiaplicate pe despărțitorul din mijloc (71B3650), decalate cu 40 mm.'],
                  extra=[('MN', 'Mâner negru 240 mm (uși) + 120 mm (sertare interioare)', '4 + 8', 'după modelul ales', '11'),
                         ('PT', 'Suport pantaloni extractibil + bară de cămăși', '2 + 2', 'modulele 2 și 3', '7'),
                         ('K', 'Profile LED 24 V cu senzori + sursă 60 W + distribuitor', '1 set', 'muchiile panourilor', '7')])
