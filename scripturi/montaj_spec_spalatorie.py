"""Specificatie de montaj R04: spalatoria din vestibul (corp masina + coloana laterala). Coordonate: x = gx - 2538, y = gy + 5550 (peretele din spate y = 0,
fata y = 650), z de la pardoseala. Piese din R03 (SP-xx), pozitii din FreeCAD spalatorie_vestibul (inventar 07.10.2026).
Corpul are 2460 x 650 mm: diagonala 2544 mm > tavanul (~2500), deci se asambleaza IN PICIOARE, pe loc (nu culcat)."""
from montaj_specs import Spec, drawer
import montaj_hw, montaj_lib as L
from montaj_comun import B, caps, finish
from montaj_spec_dulapuri import VIEWS, bracket_under_top, poly_part


def spalatorie():
    S = Spec('spalatorie', 'Spălătorie', 'Spălătorie în vestibul: corp mașină + coloană',
             'Vestibulul băii: mașina de spălat pe platformă, dulap deasupra, coloană îngustă lângă coloana de scurgere', (1000, 650, 2497),
             'Corp de 1000 × 650 × 2460 mm: nișă pentru mașina de spălat pe platformă metalică, sertar pentru 2 coșuri și poliță extractibilă (Blum MOVENTO) dedesubt, '
             'dulap cu 3 polițe și 2 uși încastrate deasupra, coloană de 264 mm cu 5 rafturi și 2 uși.')
    S.views = dict(VIEWS)
    B(S, 'perete', 'PERETE', 'Peretele din spate', -60, 1060, -60, 0, 0, 2500, 1, mat='perete', role='context')
    B(S, 'masca_f', 'PERETE', 'Masca fonică a coloanei de scurgere', 767, 1012, 0, 245, 0, 2500, 1, mat='perete', role='context')
    # platforma metalica a masinii (produs) - context
    for i, (x, y) in enumerate(((40, 35), (40, 570), (620, 35), (620, 570))):
        B(S, 'st%d' % i, 'PLAT', 'Stâlp platformă', x, x + 40, y, y + 40, 10, 480, 1, mat='metal', role='context')
    B(S, 'plat', 'PLAT', 'Platformă mașină (produs)', 30, 670, 25, 625, 480, 510, 1, mat='metal', role='context')
    # corpul masinii
    B(S, 'lat_s', 'SP-01', 'Lateral exterior (dreapta)', 0, 18, 0, 650, 10, 2470, 3)
    B(S, 'sepA', 'SP-02', 'Separator corp mașină', 682, 700, 0, 650, 10, 2452, 3)
    B(S, 'baza_s', 'SP-04', 'Bază corp superior', 18, 682, 0, 650, 1420, 1438, 3)
    B(S, 'spate_s', 'SP-06', 'Spate corp superior (PAL 16 încastrat)', 18, 682, 0, 16, 1438, 2452, 3)
    for i, z in enumerate((1800.0, 1910.0, 2230.0)):
        B(S, 'pol%d' % i, 'SP-05', 'Poliță corp superior', 18, 682, 16, 632, z, z + 18, 3)
    # coloana laterala
    B(S, 'sepB', 'SP-02', 'Separator coloană', 700, 718, 0, 650, 10, 2452, 4)
    B(S, 'lat_d', 'SP-01b', 'Lateral exterior scurtat (stânga)', 982, 1000, 245, 650, 10, 2470, 4)
    B(S, 'baza_c', 'SP-11', 'Bază coloană', 718, 982, 250, 632, 90, 108, 4)
    capac = [(18.0, 0.0), (762.0, 0.0), (762.0, 245.0), (982.0, 245.0), (982.0, 650.0), (18.0, 650.0)]
    poly_part(S, 'capac', 'SP-03', 'Capac sus (în L, decupaj pentru coloana de scurgere)', capac, 2452.0, 18.0, 5)
    for i, z in enumerate((790.0, 1160.0, 1550.0, 1910.0, 2230.0)):
        B(S, 'rc%d' % i, 'SP-12', 'Raft coloană', 719, 981, 250, 632, z, z + 18, 7, role='shelf')
    B(S, 'masina', 'MAS', 'Mașina de spălat (pe platformă)', 52, 647, 50, 608, 510, 1355, 8, mat='metal', role='context')
    # sertar pentru 2 cosuri (MOVENTO NL 500 + TIP-ON BLUMOTION) cu front incastrat; cutia la 632 (in spatele frontului)
    g = drawer(S, 'sc', 'SP-SC', 18, 632, 40.0, 664, 500, 100, 9, 2, 9, (20, 632, 30, 658, 18, 380), 'SP-08', 'Front sertar coșuri', step_tob=9,
               side_r='lat_s', side_l='sepA')
    # polita extractibila pe MOVENTO (pe 2 distantiere de 46 mm: polita are 530 mm, lumina 664)
    B(S, 'dst1', 'DST', 'Distanțier glisieră (PAL 18 × 46 × 600, nu e în R03)', 18, 64, 32, 632, 370, 430, 10, mat='corp')
    B(S, 'dst2', 'DST', 'Distanțier glisieră (PAL 18 × 46 × 600, nu e în R03)', 636, 682, 32, 632, 370, 430, 10, mat='corp')
    B(S, 'pe', 'SP-09', 'Poliță extractibilă (coș încărcare)', 85, 615, 32, 632, 410, 428, 10)
    B(S, 'pe_f', 'SP-10', 'Front poliță extractibilă', 80, 620, 632, 650, 412, 472, 10)
    for pid, x, mir, side in (('pe.rl', 64, False, 'dst1'), ('pe.rr', 636, True, 'dst2')):
        S.part(pid, 'SL', 'Glisieră MOVENTO poliță', (x - (3 if mir else 0), 632 - 501, 381.5, 3, 499, 46), 'hw', 10)
        S.parts[-1].update(model='glisiera_movento@500', zs=381.5 + 38.0, offs=[37, 261, 293], place=[x, 632, 381.5], mirror=mir, follow=side)
    # usi incastrate
    B(S, 'u1', 'SP-07', 'Ușă depozitare sus 1', 20, 348, 632, 650, 1820, 2467, 11, role='door')
    B(S, 'u2', 'SP-07', 'Ușă depozitare sus 2', 352, 680, 632, 650, 1820, 2467, 11, role='door')
    B(S, 'u3', 'SP-13', 'Ușă tehnică coloană (robinet, priză)', 721, 979, 632, 650, 100, 760, 11, role='door')
    B(S, 'u4', 'SP-14', 'Ușă accesorii coloană', 721, 979, 632, 650, 810, 2467, 11, role='door')
    B(S, 'masca', 'SP-15', 'Mască tavan', 0, 1000, 632, 650, 2470, 2497, 13)
    L.hinges(S, 11, 'u1', 'lat_s')
    L.hinges(S, 11, 'u2', 'sepA')
    L.hinges(S, 11, 'u3', 'lat_d')
    L.hinges(S, 11, 'u4', 'lat_d')
    L.tipon(S, 12, 'u1', 'capac', 320.0, y_front=632.0)
    L.tipon(S, 12, 'u2', 'capac', 380.0, y_front=632.0)
    L.tipon(S, 12, 'u3', 'baza_c', 760.0, y_front=632.0)
    L.tipon(S, 12, 'u4', 'capac', 760.0, y_front=632.0)
    for k in range(5):
        L.shelf_pins(S, 7, 'rc%d' % k, 'sepB', 'lat_d')
    for y in (100.0, 550.0):
        for z in (600.0, 1800.0):
            S.hw_at(4, 'surub_4x30', (718.0, y, z), az=(1, 0, 0), attach='sepB', explode=50, letter='E')
    bracket_under_top(S, 6, 300.0, 16.0, 2452.0)
    bracket_under_top(S, 6, 850.0, 245.0, 2452.0)
    for x in (250.0, 750.0):
        S.hw_at(13, 'coltar_40', (x, 632.0, 2470.0), az=(0, 0, 1), ax=(-1, 0, 0), explode=40, letter='L', dash=False)
    montaj_hw.auto(S)
    caps(S, 14, ('lat_s', 'lat_d', 'sepA', 'sepB'))
    S.final_views = ['fata']
    S.gbox = (2538, -5550, 3538, -4900)
    S.front_detail = False
    S.time = '≈ 1,5 zile'
    S.people = '2'
    S.wall = dict(kind='antirasturnare', unit_h=2460, note='2 colțare sub capac, în perete. Corpul se asamblează în picioare, pe loc: culcat nu încape sub tavan la ridicare.')
    S.pre = ['Racordurile mașinii de spălat (apă, scurgere, priză) sunt montate și testate; robinetul de rezervă e accesibil prin ușa tehnică.',
             'Masca fonică a coloanei de scurgere e gata (colțul din spate-stânga).',
             'Pardoseala e finită; laturile stau pe 10 mm (pene de nivelare sau nivelatoare M8 în muchia de jos).']
    S.step(1, 'Platforma mașinii', 'fata_sus',
           ['Montează platforma metalică pentru mașina de spălat (produs) la locul ei, nivelată, cu partea de sus la 510 mm.',
            'Verifică distanța față de perete: lateralul și separatorul trebuie să încapă de o parte și de alta (682 mm lumină).'],
           extra={'explode': {}, 'frame': 'all'})
    S.step(2, 'Glisierele pe lateral și pe separator (pe podea)', 'culcat',
           ['Pe lateralul SP-01 și pe separatorul corpului mașinii prinde glisierele MOVENTO NL 500 ale sertarului de coșuri (cu axa șuruburilor la %g mm de muchia de jos).' % (g['screw_z'] - 10),
            'Frontul sertarului e încastrat (în gol): glisierele încep la 18 mm în spatele muchiei din față, deci șuruburile vin la 55 / 279 / 311 mm de muchie.'],
           extra={'explode': {'sc.rl': [40, 0, 0], 'sc.rr': [-40, 0, 0]}})
    S.step(3, 'Corpul mașinii, asamblat în picioare', 'fata_sus',
           ['Corpul are 2460 × 650 mm: diagonala (2544 mm) e mai mare decât înălțimea camerei, deci NU se asamblează culcat. Se montează în picioare, pe loc.',
            'Stă lateralul SP-01 și separatorul SP-02 în picioare, pe pene de 10 mm, și prinde între ele baza corpului superior SP-04 (la 1420 mm) cu confirmate și cepuri.',
            'Introdu spatele SP-06 (PAL 16 încastrat) și polițele SP-05; ține ansamblul cu clești până pui capacul.'],
           warn=['Lucrați în doi: plăcile de 2,46 m stau în picioare abia după ce sunt legate de baza corpului superior.'],
           extra={'explode': {'baza_s': [0, 150, 0], 'spate_s': [0, -100, 0], 'pol0': [0, 150, 0], 'pol1': [0, 150, 0], 'pol2': [0, 150, 0]}})
    S.step(4, 'Coloana laterală', 'fata_sus',
           ['Pune al doilea separator SP-02 lipit de primul (separatoarele sunt duble: unul al corpului mașinii, unul al coloanei) și prinde-le între ele cu 4 șuruburi 4 × 30.',
            'Stă lateralul scurtat SP-01b (începe la 245 mm de perete, lângă masca fonică) și prinde baza coloanei SP-11 la 90 mm.'],
           extra={'explode': {'lat_d': [140, 0, 0], 'baza_c': [0, 150, 0]}})
    S.step(5, 'Capacul în L', 'fata_sus', ['Pune capacul SP-03 peste laterale și separatoare: decupajul de 220 × 245 mm vine în colțul din spate-stânga, în jurul coloanei de scurgere.',
                                          'Prinde-l cu confirmate și cepuri în toate cele 4 plăci verticale; verifică diagonalele nișei mașinii.'],
           extra={'explode': {'capac': [0, 0, 150]}})
    S.step(6, 'Colțarele de perete', 'fata', ['Prinde 2 colțare sub capac, în perete (corp mașină și coloană).'], extra={'explode': {}})
    S.step(7, 'Rafturile coloanei', 'fata', ['5 rafturi SP-12 de 382 mm (scurtate din cauza coloanei de scurgere), pe câte 4 pini.'],
           extra={'explode': {('rc%d' % k): [0, 0, 100] for k in range(5)}})
    S.step(8, 'Mașina de spălat', 'fata', ['Racordează și împinge mașina pe platformă; nivelează-i picioarele și verifică că nu atinge separatorul la centrifugare (minimum 10 mm pe fiecare parte).'],
           extra={'explode': {}})
    S.step(9, 'Sertarul de coșuri', 'fata', ['Clipsează TIP-ON BLUMOTION pe glisiere și taie bara de sincronizare la %d mm.' % g['rod'],
                                             'Asamblează cutia (SP-SC.L, SP-SC.FS, SP-SC.F retras 13 mm), clemele sub fund și frontul încastrat SP-08 (rost de 2 mm de jur-împrejur).'],
           extra={'explode': {k: [0, 400, 0] for k in [p['id'] for p in S.parts if p['id'][:3] == 'sc.' and p['code'] != 'SL']}})
    S.step(10, 'Polița extractibilă', 'fata', ['Polița SP-09 are 530 mm, iar lumina e de 664 mm: glisierele ei se prind pe 2 distanțiere de PAL de 46 mm, înșurubate pe lateral și pe separator.',
                                                'Prinde polița pe glisiere cu clemele de blocare și frontul SP-10 de 60 mm.'],
           warn=['Distanțierele nu sunt în planul de debitare R03: taie 2 fâșii de 46 × 600 mm din resturi sau comandă polița la 622 mm lățime (fără distanțiere).'],
           extra={'explode': {'pe': [0, 300, 0], 'pe_f': [0, 300, 0], 'dst1': [-80, 0, 0], 'dst2': [80, 0, 0]}})
    S.step(11, 'Ușile încastrate', 'fata_sus', ['Ușile sunt încastrate (în gol): se folosesc balamale Blum CLIP top încastrate 70T3750, nu aplicate.',
                                               'Ușile de sus au câte 2 balamale, ușa tehnică 2, ușa de accesorii 4. Rost de 2–3 mm de jur-împrejur.'],
           extra={'explode': {k: [0, 260, 0] for k in ('u1', 'u2', 'u3', 'u4')},
                  'detail': {'view': 'spate_usa', 'only': ['u4'], 'hw': ['BA', 'D17'], 'text': 'Ușa de accesorii, din spate: 4 balamale încastrate, fiecare cu 2 șuruburi 3,5 × 17.'}})
    S.step(12, 'TIP-ON pe uși', 'jos_fata', ['TIP-ON-urile stau în spatele ușilor încastrate: sub capac (ușile de sus și ușa de accesorii) și pe baza coloanei (ușa tehnică).'],
           extra={'explode': {k: [0, 260, 0] for k in ('u1', 'u2', 'u3', 'u4')}})
    S.step(13, 'Masca de tavan', 'fata_sus', ['Taie masca SP-15 la înălțimea reală și prinde-o pe capac cu 2 colțare.'], extra={'explode': {'masca': [0, 0, 100]}})
    S.step(14, 'Capacele de confirmat', 'fata', ['Pune capacele pe confirmatele vizibile.'], extra={'explode': {}})
    S.inset_hinges = getattr(S, 'inset_hinges', 0)
    return finish(S, notes=['Ușile sunt încastrate: balamale Blum CLIP top 70T3750 (devizul R04 are 70T3550/70T3650 – de corectat la comandă).',
                            'Polița extractibilă de 530 mm are nevoie de 2 distanțiere de 46 mm (nu sunt în R03) sau de o poliță de 622 mm.',
                            'Sertarul de coșuri: Blum MOVENTO 760H5000S + TIP-ON BLUMOTION, SKW = 664 − 42 = 622, bara de sincronizare %d mm.' % g['rod']],
                  extra=[('ST', 'Platformă metalică pentru mașina de spălat (produs) + 2 coșuri de rufe detașabile', '1 + 2', 'nișa mașinii', '1, 9')])
