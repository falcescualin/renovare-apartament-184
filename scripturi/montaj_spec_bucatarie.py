"""Specificatie de montaj R04: bucataria liniara (6 corpuri jos inclusiv coloana, 5 corpuri sus, blat 38 mm).
Coordonate locale: x = -gy - 250 (coloana M6 la x = 0..600, usa la x = 3220), y = gx - 7250 (peretele la y = 0, fata corpurilor jos la 560), z de la pardoseala.
Piese din R03 (BJ-xx); pozitii din FreeCAD bucatarie (corpuri ca blocuri, impartite aici in placi dupa R03)."""
from montaj_specs import Spec, drawer
import montaj_hw, montaj_lib as L
from montaj_comun import B, caps, finish
from montaj_spec_dulapuri import VIEWS

ZJ0, ZJ1 = 150.0, 870.0          # corpuri jos: pe picioare de 150, inaltime 720
ZS0, ZS1 = 1450.0, 2410.0        # corpuri sus: 960
YS = 10.0                        # corpurile de sus stau la 10 mm de perete (sina de suspendare)


def base_unit(S, m, x0, W, step, back=True, shelf=False, code=None):
    """corp jos: laterale 720 x 557 (spatele HDF aplicat), baza intre laterale, 2 traverse de 100 sub blat"""
    c = code or ('BJ-%s' % m)
    B(S, m + '.ld', c + '.L', 'Lateral corp jos %s (dreapta)' % m, x0, x0 + 18, 3, 560, ZJ0, ZJ1, step)
    B(S, m + '.ls', c + '.L', 'Lateral corp jos %s (stânga)' % m, x0 + W - 18, x0 + W, 3, 560, ZJ0, ZJ1, step)
    B(S, m + '.b', c + '.B', 'Bază %s' % m, x0 + 18, x0 + W - 18, 3, 560, ZJ0, ZJ0 + 18, step)
    B(S, m + '.tf', c + '.T', 'Traversă față %s' % m, x0 + 18, x0 + W - 18, 460, 560, ZJ1 - 18, ZJ1, step)
    B(S, m + '.tb', c + '.T', 'Traversă spate %s' % m, x0 + 18, x0 + W - 18, 3, 103, ZJ1 - 18, ZJ1, step)
    if back:
        B(S, m + '.h', c + '.H', 'Spate HDF %s' % m, x0 + 6, x0 + W - 6, 0, 3, ZJ0 + 6, ZJ1 - 6, step)
    if shelf:
        B(S, m + '.r', c + '.R', 'Raft %s' % m, x0 + 19, x0 + W - 19, 23, 543, 450, 468, step + 6, role='shelf')


def wall_unit(S, m, x0, W, H, step, shelves=(), z0=ZS0):
    c = 'BJ-%s' % m
    z1 = z0 + H
    B(S, m + '.ld', c + '.L', 'Lateral corp sus %s (dreapta)' % m, x0, x0 + 18, YS + 3, YS + 332, z0, z1, step)
    B(S, m + '.ls', c + '.L', 'Lateral corp sus %s (stânga)' % m, x0 + W - 18, x0 + W, YS + 3, YS + 332, z0, z1, step)
    B(S, m + '.b', c + '.B', 'Bază corp sus %s' % m, x0 + 18, x0 + W - 18, YS + 3, YS + 332, z0, z0 + 18, step)
    B(S, m + '.t', c + '.B', 'Blat corp sus %s' % m, x0 + 18, x0 + W - 18, YS + 3, YS + 332, z1 - 18, z1, step)
    B(S, m + '.h', c + '.H', 'Spate HDF %s' % m, x0 + 6, x0 + W - 6, YS, YS + 3, z0 + 6, z1 - 6, step)
    for k, z in enumerate(shelves):
        B(S, '%s.r%d' % (m, k), c + '.R', 'Raft %s' % m, x0 + 19, x0 + W - 19, YS + 23, YS + 323, z, z + 18, step + 9, role='shelf')


def bucatarie():
    S = Spec('bucatarie', 'Bucătărie', 'Bucătărie liniară pe peretele de est',
             'Bucătăria: rândul de corpuri pe peretele de est, de la coloana de lângă geam până la ușă', (3220, 600, 2497),
             'Bucătărie liniară de 3,22 m: 5 corpuri jos pe picioare (chiuvetă, mașină de vase, 400, plită cu 2 sertare, 400), coloană de 2,26 m pentru cuptor și microunde, '
             '5 corpuri suspendate (picurător, hotă încorporată), blat de 38 mm, fronturi cashmere fără mâner (TIP-ON).')
    S.views = dict(VIEWS)
    S.views.update({'bucatarie': [0.5, 1.0, 0.55]})
    B(S, 'perete', 'PERETE', 'Peretele de est', -60, 3300, -60, 0, 0, 2500, 5, mat='perete', role='context')
    # corpuri jos: M6 coloana 0..600, M5 600..1000, M4 600 (plita) 1000..1600, M3 1600..2000, M2 masina de vase 2000..2600, M1 chiuveta 2600..3200
    base_unit(S, 'M5', 600, 400, 2, shelf=True)
    base_unit(S, 'M4', 1000, 600, 2)
    base_unit(S, 'M3', 1600, 400, 2, shelf=True)
    base_unit(S, 'M1', 2600, 600, 2, back=False)
    # coloana M6
    B(S, 'M6.ld', 'BJ-M6.L', 'Lateral coloană (dreapta)', 0, 18, 3, 560, ZJ0, 2410, 3)
    B(S, 'M6.ls', 'BJ-M6.L', 'Lateral coloană (stânga)', 582, 600, 3, 560, ZJ0, 2410, 3)
    for k, (z, lab) in enumerate(((ZJ0, 'Bază coloană'), (837, 'Poliță sub cuptor'), (1437, 'Poliță sub microunde'), (1827, 'Poliță peste microunde'), (2392, 'Blat coloană'))):
        B(S, 'M6.p%d' % k, 'BJ-M6.B', lab, 18, 582, 3, 560, z, z + 18, 3)
    B(S, 'M6.h', 'BJ-M6.H', 'Spate coloană HDF', 6, 594, 0, 3, ZJ0 + 6, 2404, 3)
    B(S, 'M6.r', 'BJ-M6.R', 'Raft mobil coloană', 19, 581, 23, 543, 2110, 2128, 9, role='shelf')
    # corpuri sus
    wall_unit(S, 'S5', 600, 400, 960, 4, shelves=(1770, 2090))
    wall_unit(S, 'S4', 1000, 600, 760, 4, shelves=(2030,), z0=1650.0)
    wall_unit(S, 'S3', 1600, 400, 960, 4, shelves=(1770, 2090))
    wall_unit(S, 'S2', 2000, 600, 960, 4, shelves=(1770, 2090))
    wall_unit(S, 'S1', 2600, 600, 960, 4)
    B(S, 'S4c1', 'BJ-S4C', 'Cutie tub hotă: lateral', 1212, 1230, YS + 3, YS + 183, 1668, 2392, 4)
    B(S, 'S4c2', 'BJ-S4C', 'Cutie tub hotă: lateral', 1312, 1330, YS + 3, YS + 183, 1668, 2392, 4)
    B(S, 'S4cf', 'BJ-S4F', 'Cutie tub hotă: față', 1230, 1312, YS + 165, YS + 183, 1668, 2392, 4)
    # aparate (context)
    B(S, 'vase', 'APA', 'Mașină de vase încorporabilă (60)', 2002, 2598, 10, 550, 10, 865, 5, mat='metal', role='context')
    B(S, 'cuptor', 'APA', 'Cuptor', 13, 587, 13, 560, 855, 1437, 9, mat='metal', role='context')
    B(S, 'mw', 'APA', 'Cuptor cu microunde', 211, 587, 13, 560, 1455, 1827, 9, mat='metal', role='context')
    B(S, 'hota', 'APA', 'Hotă încorporată', 1000, 1600, 13, 345, 1450, 1650, 7, mat='metal', role='context')
    # blat de lucru 38 mm (decupaje chiuveta + plita facute la atelier)
    B(S, 'blat', 'BJ-BL', 'Blat de lucru 38 mm (decupaje chiuvetă și plită)', 600, 3220, 0, 600, ZJ1, ZJ1 + 38, 8, mat='blat')
    B(S, 'P1', 'BJ-P1', 'Panou capăt (lângă ușă)', 3200, 3218, 0, 578, ZJ0, ZJ1, 6)
    # sertare: M4 (2 x NL 500, H 180) cu TIP-ON BLUMOTION; M6 sub cuptor (NL 500, H 250)
    g4a = drawer(S, 'm4a', 'BJ-M4S', 1018, 560, ZJ0 + 19, 564, 500, 180, 11, 1, 12, (1001.5, 560, 152, 597, 18, 357), 'BJ-F05', 'Front M4 jos', step_tob=10,
                 side_r='M4.ld', side_l='M4.ls')
    g4b = drawer(S, 'm4b', 'BJ-M4S', 1018, 560, ZJ0 + 19 + 357, 564, 500, 180, 11, 1, 12, (1001.5, 560, 512, 597, 18, 356), 'BJ-F06', 'Front M4 sus', step_tob=10,
                 side_r='M4.ld', side_l='M4.ls')
    g6 = drawer(S, 'm6s', 'BJ-M6S', 18, 560, ZJ0 + 19, 564, 500, 250, 11, 1, 12, (1.5, 560, 152, 597, 18, 696), 'BJ-F07', 'Front M6 sertar', step_tob=10,
                side_r='M6.ld', side_l='M6.ls')
    # usi
    doors = [('uM1', 'BJ-F01', 'Ușă M1 chiuvetă', 2601.5, 3198.5, 560, ZJ0 + 2, ZJ1 - 2, 'M1.ld'),
             ('uM3', 'BJ-F03', 'Ușă M3', 1601.5, 1998.5, 560, ZJ0 + 2, ZJ1 - 2, 'M3.ld'),
             ('uM5', 'BJ-F04', 'Ușă M5', 601.5, 998.5, 560, ZJ0 + 2, ZJ1 - 2, 'M5.ls'),
             ('uM6', 'BJ-F08', 'Ușă M6 sus', 1.5, 598.5, 560, 1835, 2408, 'M6.ld'),
             ('uS1', 'BJ-F09', 'Ușă S1 picurător', 2601.5, 3198.5, YS + 332, ZS0 + 2, ZS1 - 2, 'S1.ls'),
             ('uS2', 'BJ-F09', 'Ușă S2', 2001.5, 2598.5, YS + 332, ZS0 + 2, ZS1 - 2, 'S2.ld'),
             ('uS3', 'BJ-F10', 'Ușă S3', 1601.5, 1998.5, YS + 332, ZS0 + 2, ZS1 - 2, 'S3.ld'),
             ('uS4', 'BJ-F11', 'Ușă S4 (peste hotă)', 1001.5, 1598.5, YS + 332, 1652, ZS1 - 2, 'S4.ld'),
             ('uS5', 'BJ-F10', 'Ușă S5', 601.5, 998.5, YS + 332, ZS0 + 2, ZS1 - 2, 'S5.ls')]
    for pid, code, lab, a, b, y, z0, z1, side in doors:
        B(S, pid, code, lab, a, b, y, y + 18, z0, z1, 13, role='door')
        L.hinges(S, 13, pid, side, '70T3550')
    B(S, 'fvase', 'BJ-F02', 'Front mașină de vase (pe ușa aparatului)', 2001.5, 2598.5, 560, 578, ZJ0 + 2, ZJ1 - 2, 15, role='door')
    tip = {'uM1': ('M1.tf', 2640), 'uM3': ('M3.tf', 1960), 'uM5': ('M5.tf', 640), 'uM6': ('M6.p4', 560),
           'uS1': ('S1.b', 2640), 'uS2': ('S2.b', 2560), 'uS3': ('S3.b', 1960), 'uS4': ('S4.b', 1560), 'uS5': ('S5.b', 640)}
    for d, (p, x) in tip.items():
        L.tipon(S, 14, d, p, x)
    # spatele HDF
    for m in ('M3', 'M4', 'M5'):
        L.back_screws(S, 2, m + '.h')
    L.back_screws(S, 3, 'M6.h')
    for m in ('S1', 'S2', 'S3', 'S4', 'S5'):
        L.back_screws(S, 4, m + '.h')
    # picioare H150 (4 pe corp jos, 4 la coloana) + cleme de soclu pe picioarele din fata
    legs = {'M6.p0': [(60, 60), (540, 60), (60, 470), (540, 470)], 'M5.b': [(640, 60), (960, 60), (640, 470), (960, 470)],
            'M4.b': [(1060, 60), (1540, 60), (1060, 470), (1540, 470)], 'M3.b': [(1640, 60), (1960, 60), (1640, 470), (1960, 470)],
            'M1.b': [(2660, 60), (3140, 60), (2660, 470), (3140, 470)]}
    for b, pos in legs.items():
        L.legs(S, 5, b, pos, h=150)
    for x in (60, 640, 960, 1540, 1960, 2660, 3140, 1060):
        S.hw_at(15, 'clema_soclu', (x, 470, 40.0), az=(0, 0, 1), ax=(1, 0, 0), explode=0, letter='CS', dash=False)
    B(S, 'soc1', 'BJ-P2', 'Soclu (bucata 1)', 0, 1620, 492, 510, 0, 150, 15)
    B(S, 'soc2', 'BJ-P3', 'Soclu (bucata 2)', 1620, 3200, 492, 510, 0, 150, 15)
    B(S, 'soc3', 'BJ-P4', 'Soclu retur la capăt', 3200, 3218, 0, 492, 0, 150, 15)
    # suruburi de legatura intre corpurile alaturate (4 x 30 prin lateral, 4 pe imbinare)
    for xa in (600, 1000, 1600, 2600):
        for z in (300, 760):
            for y in (80, 480):
                S.hw_at(6, 'surub_4x30', (xa - 18.0, y, z), az=(-1, 0, 0), explode=60, letter='E')
    # corpurile de sus: agatatori + sine pe perete
    for m in ('S5', 'S4', 'S3', 'S2', 'S1'):
        L.hangers(S, 7, m + '.ld', m + '.ls', m + '.t', wall_y=0.0)
    # blatul: 4 x 30 de jos prin traversele din fata si din spate
    for m, x0, W in (('M5', 600, 400), ('M4', 1000, 600), ('M3', 1600, 400), ('M1', 2600, 600)):
        for t, y in (('tf', 510.0), ('tb', 53.0)):
            for x in (x0 + 60, x0 + W - 60):
                S.hw_at(8, 'surub_4x30', (x, y, ZJ1 - 18), az=(0, 0, -1), attach=m + '.' + t, explode=60, letter='E')
    # rafturi pe pini
    for m in ('M3', 'M5'):
        L.shelf_pins(S, 9, m + '.r', m + '.ld', m + '.ls')
    L.shelf_pins(S, 9, 'M6.r', 'M6.ld', 'M6.ls')
    for m, ks in (('S2', 2), ('S3', 2), ('S4', 1), ('S5', 2)):
        for k in range(ks):
            L.shelf_pins(S, 9, '%s.r%d' % (m, k), m + '.ld', m + '.ls', inset=30.0)
    B(S, 'P5', 'BJ-P5', 'Mască tavan (bucata 1)', 0, 1620, 560, 578, 2410, 2497, 16)
    B(S, 'P6', 'BJ-P6', 'Mască tavan (bucata 2)', 1620, 3200, YS + 332, YS + 350, 2410, 2497, 16)
    B(S, 'P7', 'BJ-P7', 'Mască tavan retur la capăt', 3200, 3218, 0, YS + 350, 2410, 2497, 16)
    montaj_hw.auto(S)
    caps(S, 16, tuple(p['id'] for p in S.parts if p['id'].endswith(('.ld', '.ls'))))
    S.final_views = ['fata']
    S.gbox = (7250, -3470, 7850, -250)
    S.front_detail = True
    S.front_step = 12
    S.time = '≈ 3 zile (2 persoane) + racordurile și electrocasnicele'
    S.people = '2'
    S.wall = dict(kind='suspendare', unit_h=960, note='Corpurile de sus: câte 2 agățători pe corp, pe șină, la 1450 mm (S4: 1650). Corpurile de jos și coloana se prind de perete cu colțare sub traversa din spate.')
    S.pre = ['Instalațiile sanitare și electrice ale bucătăriei sunt gata și verificate (prizele din planul electric R11, racordurile chiuvetei și ale mașinii de vase).',
             'Pardoseala epoxidică e întărită; peretele de est e finisat, iar zona dintre blat și corpurile de sus e placată (sau se placează după montaj).',
             'Electrocasnicele sunt la fața locului, cu fișele de montaj (cuptor, microunde, plită, hotă, mașină de vase).']
    S.step(1, 'Glisierele pe laterale (pe podea)', 'culcat',
           ['Corpul M4 (sub plită) are 2 sertare, coloana M6 un sertar mare sub cuptor: prinde glisierele MOVENTO NL 500 pe laterale cât sunt pe podea.',
            'Axa șuruburilor: %g și %g mm (M4) și %g mm (M6) de la muchia de jos a lateralelor; șuruburi la 37 / 261 / 293 mm de muchia din față.'
            % (g4a['screw_z'] - ZJ0, g4b['screw_z'] - ZJ0, g6['screw_z'] - ZJ0)],
           extra={'explode': {k: ([40, 0, 0] if k.endswith('.rl') else [-40, 0, 0]) for k in ('m4a.rl', 'm4a.rr', 'm4b.rl', 'm4b.rr', 'm6s.rl', 'm6s.rr')}})
    S.step(2, 'Corpurile de jos M1, M3, M4, M5', 'bucatarie',
           ['Fiecare corp: 2 laterale, baza între ele, 2 traverse de 100 mm sus (față și spate), cu confirmate și cepuri.',
            'Spatele HDF se pune pe muchiile din spate, cu 6 mm mai mic pe fiecare latură (rămân 12 mm din cantul lateralelor la vedere). M1 (chiuvetă) nu are spate.',
            'Verifică diagonalele fiecărui corp înainte de spate.'],
           extra={'explode': {k: [0, 0, 0] for k in ()}})
    S.step(3, 'Coloana M6', 'bucatarie', ['Coloana se asamblează culcată pe spate: 2 laterale de 2260 mm și 5 plăci orizontale (bază, sub cuptor, sub microunde, peste microunde, blat).',
                                         'Verifică nișele: cuptor 855–1437 mm, microunde 1455–1827 mm (după fișele aparatelor), apoi prinde spatele HDF.'],
           extra={'explode': {'M6.ld': [-120, 0, 0], 'M6.ls': [120, 0, 0]}})
    S.step(4, 'Corpurile de sus S1–S5', 'bucatarie', ['Asamblează corpurile de sus (laterale, bază, blat, spate HDF); S4 are cutia de mascare a tubului de hotă în colțul din spate și decupaj de 70 × 150 mm în bază și blat.'],
           extra={'explode': {}})
    S.step(5, 'Picioarele de 150 mm', 'jos_fata', ['Întoarce fiecare corp de jos și coloana și prinde câte 4 picioare H150 (4 șuruburi 4 × 16 fiecare).'], extra={'explode': {}})
    S.step(6, 'Corpurile de jos și coloana pe loc', 'bucatarie',
           ['Trasează cu nivela laser linia de 870 mm (partea de sus a corpurilor) pe perete.',
            'Așază coloana și corpurile de jos, nivelează-le din picioare la linie și leagă-le între ele cu câte 4 șuruburi 4 × 30 prin laterale.',
            'Lasă locul de 600 mm pentru mașina de vase între M3 și M1; prinde panoul de capăt BJ-P1 lângă M1.'],
           warn=['Coloana se prinde de perete sus (colțar sub blatul ei) înainte de a pune cuptorul.'], extra={'explode': {}})
    S.step(7, 'Corpurile de sus pe șine', 'bucatarie',
           ['Trasează linia șinelor; prinde șinele cu dibluri la maximum 300 mm (după tipul peretelui).',
            'Agață corpurile de sus pe agățători, reglează-le la nivel și adâncime și leagă-le între ele (4 × 30 prin laterale).'],
           extra={'explode': {}})
    S.step(8, 'Blatul de lucru', 'bucatarie',
           ['Blatul de 38 mm vine cu decupajele pentru chiuvetă și plită făcute la atelier (după șabloanele aparatelor). Etanșează muchiile decupajelor cu silicon sanitar.',
            'Așază blatul pe corpurile M5–M1, la 600 mm adâncime, și prinde-l de jos prin traverse cu șuruburi 4 × 30 (12 mm în blat).',
            'Siliconează rostul dintre blat și perete.'],
           extra={'explode': {'blat': [0, 0, 160]}})
    S.step(9, 'Rafturile pe pini', 'bucatarie', ['Rafturi pe pini Ø5: M3, M5, coloana (sus), S2, S3, S4, S5.'], extra={'explode': {}})
    S.step(10, 'TIP-ON BLUMOTION și barele de sincronizare', 'fata', ['Clipsează unitățile TIP-ON BLUMOTION pe glisierele din M4 și M6; barele de sincronizare la %d mm.' % g4a['rod']],
           extra={'explode': {}})
    S.step(11, 'Cutiile de sertar', 'fata', ['Asamblează cele 3 cutii (BJ-M4S × 2, BJ-M6S), fundul retras 13 mm, găurile pentru cârlig și clemele; împinge-le pe glisiere.'],
           extra={'explode': {k: [0, 450, 0] for k in [p['id'] for p in S.parts if p['id'][:4] in ('m4a.', 'm4b.', 'm6s.') and p['code'] != 'SL' and not p['id'].endswith('.fr')]}})
    S.step(12, 'Fronturile de sertar', 'fata', ['Fixează fronturile BJ-F05, BJ-F06 (M4) și BJ-F07 (M6) după paginile de detaliu.'],
           extra={'explode': {'m4a.fr': [0, 120, 0], 'm4b.fr': [0, 120, 0], 'm6s.fr': [0, 120, 0]}})
    S.step(13, 'Ușile: plăcuțe și balamale', 'bucatarie', ['Toate ușile sunt aplicate pe lateralul propriului corp: balamale 70T3550. Ușile de 716–756 mm au 2 balamale, cele de 956 mm câte 3.'],
           extra={'explode': {d[0]: [0, 250, 0] for d in doors}})
    S.step(14, 'TIP-ON pe uși și reglajul', 'jos_fata', ['TIP-ON sub traversa din față (corpurile de jos), în baza corpurilor de sus și sub blatul coloanei, lângă marginea de deschidere. Reglează rosturile la 3 mm.'],
           extra={'explode': {d[0]: [0, 250, 0] for d in doors}})
    S.step(15, 'Soclul, mașina de vase și frontul ei', 'fata', ['Prinde clemele pe picioarele din față și apasă soclul (2 bucăți + returul de la capăt), tăiat la înălțimea reală.',
                                                                 'Montează mașina de vase și frontul ei BJ-F02 după fișa producătorului.'],
           extra={'explode': {'soc1': [0, 150, 0], 'soc2': [0, 150, 0], 'soc3': [80, 0, 0]}})
    S.step(16, 'Masca de tavan și capacele', 'bucatarie', ['Taie măștile P5, P6, P7 la înălțimea reală până la tavan (110 din care rămân ~87) și prinde-le pe blaturile corpurilor cu colțare.',
                                                          'Pune capacele pe confirmatele vizibile.'], extra={'explode': {'P5': [0, 0, 100], 'P6': [0, 0, 100], 'P7': [0, 0, 100]}})
    return finish(S, notes=['Toate ușile sunt aplicate pe lateralul propriului corp: 22 de balamale 70T3550 (devizul R04 are 10 × 70T3550 + 14 × 70T3650).',
                            'Corpurile de sus sunt la 10 mm de perete (loc pentru șina de suspendare); fronturile lor vin la 360 mm de perete.',
                            'Sertare Blum MOVENTO 760H5000S + TIP-ON BLUMOTION: SKW = 564 − 42 = 522; bare de sincronizare %d mm.' % g4a['rod']],
                  extra=[('SI2', 'Silicon sanitar transparent', '1 tub', 'decupaje blat, rost blat–perete', '8'),
                         ('APA', 'Electrocasnice (cuptor, microunde, plită, hotă, mașină de vase) cu șuruburile lor de prindere', '—', 'după fișele producătorilor', '15')])
