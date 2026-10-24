"""Specificatii de montaj R04: comoda TV dormitor, machiaj, comoda TV camera de zi, corp spate pat.
Coordonate locale: mm, fata = +y, sus = +z, x mic = dreapta privit din fata. Piesele (dimensiuni) din planul de debitare R03;
pozitiile din modelele FreeCAD perete_TV / perete_TV_dormitor / corp_spate_pat (inventar 07.10.2026), rotite cu fata spre +y."""
from montaj_specs import Spec, drawer
import montaj_hw, montaj_lib as L
from montaj_comun import B, caps, finish, R03
from montaj_spec_mici import VIEWS


def _oak_box(S, step, top, base, verticals):
    """blat + baza de stejar peste laterale si despartitor: cepuri + colțare pe interior (fara confirmate vizibile)"""
    for pid, inside in verticals:
        for f in (top, base):
            L.hidden_joint(S, step, f, pid, inside)


def _drawer_ids(S):
    return [p['id'] for p in S.parts if p['id'][:3] in ('s1.', 's2.') and p['code'] != 'SL' and not p['id'].endswith('.fr')]


RAILS_OUT = {'s1.rl': [40, 0, 0], 's2.rl': [40, 0, 0], 's1.rr': [-40, 0, 0], 's2.rr': [-40, 0, 0]}


# ================================================================== COMODA TV DORMITOR (suspendata, pe peretele cu riflaje)
def comoda_tv_dormitor():
    S = Spec('comoda_tv_dormitor', 'Comodă TV dormitor', 'Comodă TV suspendată, dormitor',
             'Dormitor, pe peretele cu riflaje de stejar, cu baza la 300 mm de pardoseală (LED dedesubt)', (1700, 341, 280),
             'Corp suspendat de stejar 1700 × 320 × 280 mm cu două sertare Blum MOVENTO (NL 300) cu TIP-ON BLUMOTION, '
             'blat și bază de stejar prinse ascuns (cepuri + colțare), spate HDF și bandă LED dedesubt.')
    W, D0, D1, H = 1700.0, 3.0, 323.0, 280.0
    B(S, 'lat_d', 'CTD-02', 'Lateral dreapta', 0, 18, D0, D1, 18, H - 18, 1)
    B(S, 'lat_s', 'CTD-02', 'Lateral stânga', W - 18, W, D0, D1, 18, H - 18, 1)
    B(S, 'div', 'CTD-03', 'Despărțitor', 841, 859, D0, 320, 18, H - 18, 1)
    B(S, 'baza', 'CTD-01', 'Bază (stejar)', 0, W, D0, D1, 0, 18, 2)
    B(S, 'blat', 'CTD-01', 'Blat (stejar)', 0, W, D0, D1, H - 18, H, 2)
    B(S, 'spate', 'CTD-04', 'Spate HDF', 2, W - 2, 0, 3, 2, H - 2, 3)
    B(S, 'perete', 'PERETE', 'Peretele cu riflaje', -80, W + 80, -70, -10, -300, H + 300, 4, mat='perete', role='context')
    g1 = drawer(S, 's1', 'CTD-S', 18, D1, 19.0, 823, 300, 180, 6, 1, 7, (2, D1, 2, 847, 18, 276), 'CTD-05', 'Front sertar dreapta', step_tob=5,
                offs_l=(37, 101, 261), side_r='lat_d', side_l='div')
    drawer(S, 's2', 'CTD-S', 859, D1, 19.0, 823, 300, 180, 6, 1, 7, (851, D1, 2, 847, 18, 276), 'CTD-05', 'Front sertar stânga', step_tob=5,
           offs_r=(69, 133, 229), side_r='div', side_l='lat_s')
    B(S, 'led', 'LED', 'Bandă LED sub comodă', 20, W - 20, 103, 120, -5, 0, 8, mat='led', role='hw')
    _oak_box(S, 2, 'blat', 'baza', [('lat_d', (1, 0, 0)), ('lat_s', (-1, 0, 0)), ('div', (1, 0, 0))])
    L.back_screws(S, 3, 'spate')
    L.hangers(S, 4, 'lat_d', 'lat_s', 'blat', wall_y=-10.0)
    montaj_hw.auto(S)
    S.final_views = ['fata']
    S.views = dict(VIEWS)
    S.gbox = (3200, -2900, 3520, -1200)
    S.front_detail = True
    S.front_step = 7
    S.time = '≈ 3 ore'
    S.people = '2 la agățarea pe perete'
    S.wall = dict(kind='suspendare', unit_h=280, note='Șina se prinde prin riflaje în peretele din spate, cu șuruburi lungi și dibluri, în dreptul unei lamele; '
                  'dacă lamelele sunt pe pâslă, pune o șipcă de 10 mm în spatele șinei ca să nu strivească pâsla.')
    S.pre = ['Riflajele de pe perete sunt montate.', 'Alimentarea LED 24 V e adusă la cota de sub comodă (300 mm).']
    S.step(1, 'Glisierele pe laterale și pe despărțitor', 'fata',
           ['Pune lateralele CTD-02 și despărțitorul CTD-03 pe covor, cu fața pe care vin glisierele în sus.',
            'Trasează axa șuruburilor glisierelor la %g mm de muchia de jos a lateralelor și a despărțitorului.' % (g1['screw_z'] - 18),
            'Prinde glisierele MOVENTO NL 300 cu câte 3 șuruburi Blum 3,5 × 15, pe laterale la 37 / 69 / 261 mm de muchia din față.',
            'Pe despărțitor vin glisiere pe ambele fețe: pe o față la 37 / 101 / 261 mm, pe cealaltă la 69 / 133 / 229 mm, ca șuruburile să nu se întâlnească.'],
           warn=['Despărțitorul are 18 mm, iar șuruburile 15 mm: dacă le pui în aceleași puncte pe ambele fețe, se ating.'],
           extra={'explode': dict(RAILS_OUT)})
    S.step(2, 'Corpul: blatul și baza de stejar, fără confirmate vizibile', 'fata',
           ['Blatul și baza sunt de stejar la vedere: nu se pun confirmate prin ele.',
            'Bate cepurile cu adeziv în muchiile de sus și de jos ale lateralelor și despărțitorului și așază blatul și baza pe ele.',
            'Prinde fiecare îmbinare pe interior cu colțare 40 × 40 și câte 4 șuruburi 4 × 16 (2 în stejar, 2 în lateral).',
            'Verifică diagonalele înainte ca adezivul să se întărească.'],
           warn=['Șuruburile de 16 mm intră 14 mm în stejarul de 18 mm: nu folosi mai lungi.'],
           extra={'explode': {'blat': [0, 0, 130], 'baza': [0, 0, -130]}})
    S.step(3, 'Spatele HDF', 'spate', ['Prinde spatele HDF CTD-04 pe muchiile din spate cu șuruburi 3,5 × 16 la ~150 mm.',
                                       'Taie în HDF două decupaje de 40 × 25 mm în colțurile de sus, în dreptul agățătorilor.'],
           extra={'explode': {'spate': [0, -80, 0]}})
    S.step(4, 'Agățătorile, șina și agățarea pe perete', 'fata',
           ['Prinde agățătorile în colțurile de sus-spate, pe lateralele corpului, cu câte 2 șuruburi 4 × 16.',
            'Marchează cu nivela linia șinei; prinde șina prin riflaje în perete cu dibluri și șuruburi la maximum 300 mm.',
            'Agață corpul pe șină, reglează înălțimea (baza la 300 mm) și adâncimea din șuruburile agățătorilor.'],
           warn=['Comoda încărcată poate avea 30–40 kg: șina se prinde în zidărie, nu doar în riflaje.'], extra={'explode': {}})
    S.step(5, 'TIP-ON BLUMOTION și barele de sincronizare', 'fata',
           ['Clipsează unitățile TIP-ON BLUMOTION pe glisiere (în spate) și împinge-le până fac clic.',
            'Taie barele de sincronizare la %d mm (LW − 267 = 823 − 267) și introdu-le între unitățile aceluiași sertar.' % g1['rod']],
           extra={'explode': {}})
    S.step(6, 'Cutiile de sertar și clemele', 'fata',
           ['Asamblează cutiile: laterale CTD-S.L, față și spate CTD-S.FS, fund CTD-S.F retras 13 mm, cu confirmate și cepuri.',
            'Găurește Ø6 × 10 în capătul din spate al lateralelor (7 mm de fața exterioară, 11 mm de jos) pentru cârligul glisierei.',
            'Prinde sub fund clemele de cuplare, în colțurile din față, cu câte 2 șuruburi 3,5 × 15, și împinge cutiile pe glisiere până se aud clemele.'],
           check=['Lățimea interioară a sertarului este 781 mm (LW − 42), lungimea 290 mm (NL − 10).'],
           extra={'explode': {k: [0, 300, 0] for k in _drawer_ids(S)}})
    S.step(7, 'Fronturile de stejar', 'fata',
           ['Fixează fronturile CTD-05 pe cutii după paginile de detaliu (distanțiere, bandă dublu adeziv, 4 șuruburi 4 × 25 cu șaibă din interior).',
            'Fibra stejarului e orizontală și continuă pe cele două fronturi: pune-le în ordinea marcată de atelier pe spate.'],
           extra={'explode': {'s1.fr': [0, 110, 0], 's2.fr': [0, 110, 0]}})
    S.step(8, 'Banda LED și verificarea', 'jos_fata', ['Lipește banda LED în profil sub bază, la 100 mm de perete, și conectează-o la sursa de 24 V.',
                                                        'Verifică deschiderea prin apăsare și închiderea amortizată la ambele sertare.'],
           extra={'explode': {'led': [0, 0, -60]}})
    return finish(S, notes=['Cote Blum MOVENTO 760H3000S (NL 300): SKW = LW − 42 = 781; SKL = NL − 10 = 290; fundul retras 13 mm; '
                            'bara de sincronizare LW − 267 = %d mm.' % g1['rod']],
                  extra=[('K', 'Bandă LED 24 V + profil + cablu', '1 set', 'sub comodă', '8')])


# ================================================================== MACHIAJ (suspendat, cu oglinda LED deasupra)
def machiaj():
    S = Spec('machiaj', 'Machiaj', 'Masă de machiaj suspendată',
             'Dormitor, lângă fereastră, sub oglinda cu LED, cu blatul la 750 mm de pardoseală', (630, 418, 150),
             'Corp suspendat de stejar 630 × 400 × 150 mm cu două sertare Blum MOVENTO (NL 350) cu TIP-ON BLUMOTION, '
             'blat și bază de stejar prinse ascuns, spate PAL 16 mm încastrat prin care corpul se prinde de perete.')
    W, D, H = 630.0, 400.0, 150.0
    B(S, 'lat_d', 'MJ-02', 'Lateral dreapta', 0, 18, 0, D, 18, H - 18, 1)
    B(S, 'lat_s', 'MJ-02', 'Lateral stânga', W - 18, W, 0, D, 18, H - 18, 1)
    B(S, 'div', 'MJ-03', 'Despărțitor (scurtat la 384)', 306, 324, 16, D, 18, H - 18, 1)
    B(S, 'baza', 'MJ-01', 'Bază (stejar)', 0, W, 0, D, 0, 18, 2)
    B(S, 'blat', 'MJ-01', 'Blat (stejar)', 0, W, 0, D, H - 18, H, 2)
    B(S, 'spate', 'MJ-04', 'Spate PAL 16 (încastrat)', 18, W - 18, 0, 16, 18, H - 18, 3)
    B(S, 'perete', 'PERETE', 'Peretele de sub oglindă', -80, W + 80, -60, 0, -200, H + 300, 4, mat='perete', role='context')
    g1 = drawer(S, 's1', 'MJ-S', 18, D, 19.0, 288, 350, 90, 6, 1, 7, (2, D, 2, 311, 18, 146), 'MJ-05', 'Front sertar dreapta', step_tob=5,
                offs_l=(37, 101, 261), side_r='lat_d', side_l='div')
    drawer(S, 's2', 'MJ-S', 324, D, 19.0, 288, 350, 90, 6, 1, 7, (317, D, 2, 311, 18, 146), 'MJ-05', 'Front sertar stânga', step_tob=5,
           offs_r=(69, 133, 229), side_r='div', side_l='lat_s')
    _oak_box(S, 2, 'blat', 'baza', [('lat_d', (1, 0, 0)), ('lat_s', (-1, 0, 0)), ('div', (1, 0, 0))])
    for f in ('blat', 'baza'):
        L.hidden_joint(S, 3, f, 'spate', (0, 1, 0), brackets=[120.0, 490.0])
    S.skip_joints += [('spate', 'lat_d'), ('spate', 'lat_s'), ('spate', 'div')]
    sp = next(p for p in S.parts if p['id'] == 'spate')
    for x in (80.0, W - 80.0):
        for z in (45.0, 105.0):
            S.hw_at(4, 'diblu_6x40', (x, 0.0, z), az=(0, 1, 0), explode=90, letter='T')
            S.hw_at(4, 'surub_4x40', (x, 16.0, z), az=(0, 1, 0), explode=150, letter='U')
            S.hw_at(4, 'saiba', (x, 16.0, z), az=(0, 1, 0), explode=120, letter='W', dash=False)
            L.hole(sp, 'hang', (x, 16.0, z), (0, 1, 0), 6.0, 16, 'șurub în perete', through=True)
    montaj_hw.auto(S)
    S.final_views = ['fata']
    S.views = dict(VIEWS)
    S.gbox = (3150, -1160, 3550, -530)
    S.front_detail = True
    S.front_step = 7
    S.time = '≈ 2,5 ore'
    S.people = '2 la prinderea pe perete'
    S.wall = dict(kind='prin_spate', unit_h=150, note='Masa de machiaj e folosită și ca birou: prinde-o în 4 puncte, în zidărie. Oglinda cu LED se montează după masă.')
    S.pre = ['Peretele de sub oglindă e finisat; alimentarea oglinzii LED e adusă.']
    S.step(1, 'Glisierele pe laterale și pe despărțitor', 'fata',
           ['Prinde glisierele MOVENTO NL 350 cu câte 3 șuruburi Blum 3,5 × 15, cu axa la %g mm de muchia de jos a lateralelor.' % (g1['screw_z'] - 18),
            'Pe despărțitor (glisiere pe ambele fețe) decalează șuruburile: 37 / 101 / 261 pe o față, 69 / 133 / 229 pe cealaltă.',
            'Despărțitorul MJ-03 din planul de debitare are 397 mm: scurtează-l la 384 mm (adâncimea minus spatele de 16 mm) înainte de montaj.'],
           warn=['Fără scurtarea despărțitorului, spatele încastrat nu intră.'], extra={'explode': dict(RAILS_OUT)})
    S.step(2, 'Corpul: blatul și baza de stejar, fără confirmate vizibile', 'fata',
           ['Bate cepurile cu adeziv în muchiile lateralelor și ale despărțitorului; așază blatul și baza.',
            'Prinde fiecare îmbinare pe interior cu colțare 40 × 40 și șuruburi 4 × 16.'], extra={'explode': {'blat': [0, 0, 110], 'baza': [0, 0, -110]}})
    S.step(3, 'Spatele PAL 16 încastrat', 'spate', ['Introdu spatele MJ-04 între blat, bază și laterale și prinde-l cu cepuri și 4 colțare pe interior.'],
           extra={'explode': {'spate': [0, -90, 0]}})
    S.step(4, 'Prinderea pe perete', 'fata', ['Marchează linia blatului la 750 mm de pardoseală.',
                                             'Prinde corpul prin spate în 4 puncte, cu dibluri și șuruburi 4 × 40 cu șaibă (pagina „Prindere în perete”).'],
           extra={'explode': {}})
    S.step(5, 'TIP-ON BLUMOTION și barele de sincronizare', 'fata',
           ['Clipsează unitățile TIP-ON BLUMOTION pe glisiere.',
            'Lumina corpului e de doar 288 mm (sub 293): bara de sincronizare se taie la LW − 241 = %d mm (varianta Blum pentru corpuri înguste).' % g1['rod']],
           extra={'explode': {}})
    S.step(6, 'Cutiile de sertar și clemele', 'fata',
           ['Asamblează cutiile MJ-S, fundul retras 13 mm; găurile Ø6 × 10 pentru cârlig în spatele lateralelor.',
            'Prinde clemele sub fund și împinge cutiile pe glisiere.'],
           check=['Lățimea interioară a sertarului este 245 mm (LW − 42 = 246, toleranță −1,5).'],
           extra={'explode': {k: [0, 260, 0] for k in _drawer_ids(S)}})
    S.step(7, 'Fronturile de stejar', 'fata', ['Fixează fronturile MJ-05 după paginile de detaliu.'], extra={'explode': {'s1.fr': [0, 100, 0], 's2.fr': [0, 100, 0]}})
    return finish(S, notes=['Cote Blum MOVENTO 760H3500S (NL 350): SKW = LW − 42 = 246 (planul: 245); SKL = 340; bara de sincronizare LW − 241 = %d mm (LW ≤ 293). '
                            'Despărțitorul MJ-03 se scurtează de la 397 la 384 mm.' % g1['rod']])


# ================================================================== COMODA TV CAMERA DE ZI (suspendata, 2,4 m, blat de stejar dublu)
def comoda_tv_zi():
    S = Spec('comoda_tv_zi', 'Comodă TV cameră de zi', 'Comodă TV suspendată, cameră de zi',
             'Camera de zi, pe peretele TV, cu baza la 200 mm de pardoseală', (2400, 400, 416),
             'Corp suspendat cashmere de 2400 × 382 × 380 mm cu trei uși fără mâner (balamale Blum CLIP top fără arc + TIP-ON), '
             'două despărțitoare, blat de stejar dublu de 36 mm și bandă LED dedesubt.')
    W, D, H = 2400.0, 382.0, 380.0
    B(S, 'lat_d', 'CTV-01', 'Lateral dreapta', 0, 18, 0, D, 0, H, 2)
    B(S, 'lat_s', 'CTV-01', 'Lateral stânga', W - 18, W, 0, D, 0, H, 2)
    B(S, 'baza', 'CTV-02', 'Bază (se vede de jos)', 18, W - 18, 0, D, 0, 18, 2)
    B(S, 'blat_c', 'CTV-03', 'Blat corp (sub blatul de stejar)', 18, W - 18, 0, D, H - 18, H, 2)
    B(S, 'div1', 'CTV-04', 'Despărțitor dreapta', 791, 809, 0, 380, 18, H - 18, 2)
    B(S, 'div2', 'CTV-04', 'Despărțitor stânga', 1591, 1609, 0, 380, 18, H - 18, 2)
    B(S, 'spate', 'CTV-05', 'Spate HDF', 2, W - 2, -3, 0, 2, H - 2, 3)
    B(S, 'perete', 'PERETE', 'Peretele TV', -80, W + 80, -73, -13, -200, H + 400, 4, mat='perete', role='context')
    B(S, 'st1', 'CTV-07', 'Blat stejar – strat 1', 0, W, 0, 400, H, H + 18, 5)
    B(S, 'st2', 'CTV-07', 'Blat stejar – strat 2 (lipit)', 0, W, 0, 400, H + 18, H + 36, 5)
    B(S, 'u1', 'CTV-06', 'Ușă dreapta', 2, 799, D, D + 18, 2, H - 2, 6, role='door')
    B(S, 'u2', 'CTV-06', 'Ușă mijloc', 801.5, 1598.5, D, D + 18, 2, H - 2, 6, role='door')
    B(S, 'u3', 'CTV-06', 'Ușă stânga', 1601, 2398, D, D + 18, 2, H - 2, 6, role='door')
    B(S, 'led', 'LED', 'Bandă LED sub comodă', 20, W - 20, 300, 317, -5, 0, 8, mat='led', role='hw')
    L.back_screws(S, 3, 'spate')
    L.hangers(S, 4, 'lat_d', 'lat_s', 'blat_c', wall_y=-13.0)
    for x in (120.0, 680.0, 920.0, 1480.0, 1720.0, 2280.0):
        for y in (70.0, 310.0):
            S.hw_at(5, 'surub_4x30', (x, y, H - 18.0), az=(0, 0, -1), attach='blat_c', explode=60, letter='E')
    L.hinges(S, 6, 'u1', 'lat_d', '70T3550')
    L.hinges(S, 6, 'u2', 'div1', '70T3650')
    L.hinges(S, 6, 'u3', 'lat_s', '70T3550')
    L.tipon(S, 7, 'u1', 'blat_c', 760.0)
    L.tipon(S, 7, 'u2', 'blat_c', 1560.0)
    L.tipon(S, 7, 'u3', 'blat_c', 1640.0)
    montaj_hw.auto(S)
    caps(S, 8, ('lat_d', 'lat_s', 'baza'))
    S.final_views = ['fata']
    S.views = dict(VIEWS)
    S.gbox = (3700, -3850, 4100, -1450)
    S.time = '≈ 4 ore + 24 de ore pentru lipirea blatului de stejar'
    S.people = '2 (corpul are 2,4 m)'
    S.wall = dict(kind='suspendare', unit_h=380, note='Comoda are 2,4 m și blat de stejar de 36 mm: șina se prinde la maximum 300 mm, numai în zidărie. '
                  'Dacă peretele TV e din gips-carton, cere o placă de consolidare (OSB 18) în spatele lui.')
    S.pre = ['Peretele TV e finisat; alimentarea LED 24 V e adusă la 200 mm de pardoseală.']
    S.step(1, 'Pregătire: blatul de stejar dublu (24 de ore)', 'sus',
           ['Lipește cele două straturi CTV-07 (2 × 18 = 36 mm) cu adeziv PVAC și strânge-le cu 6–8 clești pe toată lungimea de 2,4 m.',
            'Pune cantul 42 × 2 pe față și pe capete după uscare (sau comanzi blatul dublat gata de la atelier).'],
           extra={'solo': ['st1', 'st2'], 'explode': {'st2': [0, 0, 80]}, 'frame': 'new'})
    S.step(2, 'Corpul: laterale, bază, blat corp și despărțitoare', 'fata',
           ['Corpul are 2,4 m: montează-l pe podea, pe covor, cu spatele în jos.',
            'Bate cepurile în muchiile bazei, blatului corp și despărțitoarelor; prinde baza și blatul corp între laterale cu confirmate.',
            'Prinde despărțitoarele (la 791 și 1591 mm de lateralul din dreapta) prin bază și prin blatul corp cu confirmate.',
            'Verifică diagonalele (diferență sub 3 mm) înainte să strângi confirmatele.'],
           extra={'explode': {'lat_d': [-120, 0, 0], 'lat_s': [120, 0, 0], 'blat_c': [0, 0, 120], 'baza': [0, 0, -120]}})
    S.step(3, 'Spatele HDF', 'spate', ['Prinde spatele CTV-05 cu șuruburi 3,5 × 16 la ~150 mm, în muchiile din spate.',
                                       'Taie decupaje de 40 × 25 mm în colțurile de sus pentru agățători.'], extra={'explode': {'spate': [0, -90, 0]}})
    S.step(4, 'Agățătorile, șina și agățarea pe perete', 'fata',
           ['Prinde agățătorile în colțurile de sus-spate, pe laterale.', 'Fixează șina pe perete, la nivelă, cu dibluri la maximum 300 mm.',
            'Agață corpul (în doi), reglează înălțimea (baza la 200 mm) și adâncimea.'], extra={'explode': {}})
    S.step(5, 'Blatul de stejar pe corp', 'sus',
           ['Pune blatul de stejar (uscat de la pasul 1) pe corp: aliniat la spate, iese 18 mm în față (acoperă ușile).',
            'Prinde-l de jos, din interiorul compartimentelor, cu 12 șuruburi 4 × 30 prin blatul corpului (18 mm) în stejar (12 mm).'],
           warn=['Șuruburi de maximum 30 mm: blatul de stejar are 36 mm.'], extra={'explode': {'st1': [0, 0, 150], 'st2': [0, 0, 150]}})
    S.step(6, 'Ușile: plăcuțe și balamale', 'sus',
           ['Ușa din dreapta se prinde pe lateralul din dreapta (balamale aplicate 70T3550), cea din stânga pe lateralul din stânga.',
            'Ușa din mijloc se prinde pe despărțitorul din dreapta, cu balamale semiaplicate (70T3650): ușile se întâlnesc pe despărțitor.',
            'Găurește cupele Ø35 × 13 (TB 5 la aplicate, 6 la semiaplicate), prinde balamalele cu 3,5 × 17 și plăcuțele cu 3,5 × 15 la 37 mm de muchia din față.'],
           extra={'explode': {'u1': [0, 260, 0], 'u2': [0, 260, 0], 'u3': [0, 260, 0]},
                  'detail': {'view': 'spate_usa', 'only': ['u2'], 'hw': ['BA', 'D17'],
                             'text': 'Ușa din mijloc, din spate: 2 balamale semiaplicate 70T3650 în cupele Ø35 × 13, fiecare cu 2 șuruburi 3,5 × 17.'}})
    S.step(7, 'TIP-ON și reglajul ușilor', 'jos_fata',
           ['Prinde sub blatul corpului câte un adaptor TIP-ON în dreptul marginii de deschidere a fiecărei uși și introdu TIP-ON-urile.',
            'Pune plăcile metalice Ø15 pe spatele ușilor, în dreptul magneților, și reglează ușile: rost 2–3 mm între ele.'],
           extra={'explode': {'u1': [0, 260, 0], 'u2': [0, 260, 0], 'u3': [0, 260, 0]}})
    S.step(8, 'Capace și LED', 'jos_fata', ['Pune capacele pe confirmatele de pe laterale și de sub bază.', 'Lipește banda LED în profil sub bază și conecteaz-o.'],
           extra={'explode': {'led': [0, 0, -60]}})
    return finish(S, extra=[('J', 'Adeziv lemn PVAC D3 + 6–8 clești', '1 tub', 'blatul de stejar dublu', '1'), ('K', 'Bandă LED 24 V + profil', '1 set', 'sub comodă', '8')])


# ================================================================== CORP SPATE PAT (ingust, 1100 mm, blat de stejar)
def corp_spate_pat():
    S = Spec('corp_spate_pat', 'Corp spate pat', 'Corp îngust în spatele patului',
             'Dormitor, pe peretele din spatele patului (tăblia patului vine în fața lui)', (1600, 130, 1118),
             'Corp îngust de 1600 × 112 × 1100 mm: două laterale și un reazem central, spate HDF și blat de stejar de 130 mm, prins de perete cu 2 colțare.')
    W = 1600.0
    B(S, 'lat_d', 'CP-02', 'Lateral dreapta', 0, 18, 0, 112, 0, 1100, 1)
    B(S, 'reazem', 'CP-02', 'Reazem central', 791, 809, 0, 112, 0, 1100, 1)
    B(S, 'lat_s', 'CP-02', 'Lateral stânga', W - 18, W, 0, 112, 0, 1100, 1)
    B(S, 'blat', 'CP-01', 'Blat stejar', 0, W, -3, 127, 1100, 1118, 1)
    B(S, 'spate', 'CP-03', 'Spate HDF (1600 × 1100, aplicat)', 0, W, -3, 0, 0, 1100, 2)
    B(S, 'perete', 'PERETE', 'Peretele din spatele patului', -80, W + 80, -63, -3, 0, 1400, 3, mat='perete', role='context')
    for pid, ins in (('lat_d', (1, 0, 0)), ('reazem', (1, 0, 0)), ('lat_s', (-1, 0, 0))):
        L.hidden_joint(S, 1, 'blat', pid, ins, brackets=[20.0])
    L.back_screws(S, 2, 'spate', spacing=200.0)
    for x in (400.0, 1200.0):
        S.hw_at(3, 'coltar_40', (x - 10, -3.0, 1100.0), az=(0, 0, -1), ax=(-1, 0, 0), explode=60, letter='L', dash=False)
        S.hw_at(3, 'diblu_6x40', (x, -3.0, 1070.0), az=(0, 1, 0), explode=70, letter='T')
        S.hw_at(3, 'surub_4x40', (x, -1.0, 1070.0), az=(0, 1, 0), explode=125, letter='U')
        for y in (11.0, 27.0):
            S.hw_at(3, 'surub_4x16', (x, y, 1098.0), az=(0, 0, -1), explode=90, letter='I')
    montaj_hw.auto(S)
    S.final_views = ['fata']
    S.views = dict(VIEWS)
    S.gbox = (0, 0, 130, 1600)
    S.time = '≈ 1,5 ore'
    S.people = '2'
    S.wall = dict(kind='antirasturnare', unit_h=1100, note='Corpul are doar 130 mm adâncime și 1100 mm înălțime: fără colțarele de perete se răstoarnă.')
    S.step(1, 'Blatul de stejar pe laterale și pe reazem', 'fata',
           ['Întoarce blatul CP-01 cu fața în jos, pe covor, și așază pe el lateralele și reazemul central (CP-02), la 0, 791 și 1582 mm.',
            'Prinde fiecare placă de blat cu cepuri (cu adeziv) și un colțar 40 × 40 pe interior, cu 4 șuruburi 4 × 16.'],
           warn=['Fără confirmate prin blat: stejarul rămâne curat.'], extra={'explode': {'lat_d': [0, 0, -120], 'reazem': [0, 0, -120], 'lat_s': [0, 0, -120]}})
    S.step(2, 'Spatele HDF', 'spate', ['Prinde spatele HDF pe muchiile din spate ale lateralelor și reazemului, cu șuruburi 3,5 × 16 la ~200 mm.'],
           warn=['Planul de debitare R03 are spatele de 1564 mm (între laterale), care nu are unde să se prindă. Comandă-l de 1600 × 1100 mm, aplicat pe muchii.'],
           extra={'explode': {'spate': [0, -90, 0]}})
    S.step(3, 'Poziționare și colțarele de perete', 'stanga',
           ['Așază corpul la perete, centrat pe pat, și verifică verticalitatea.',
            'Prinde 2 colțare sub blat, lipite de perete: în blat cu 2 șuruburi 4 × 16, în perete cu diblu Ø6 × 40 și șurub 4 × 40.'],
           extra={'explode': {}})
    return finish(S, notes=['Spatele: R03 are 1564 × 1100 mm (încastrat); recomand 1600 × 1100 aplicat pe muchii, altfel nu are unde să se prindă.'])
