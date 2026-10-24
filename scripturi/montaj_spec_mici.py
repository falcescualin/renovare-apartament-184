"""Specificatii de montaj R04 pentru corpurile mici: dulap WC, comoda TV dormitor, machiaj, comoda TV camera de zi, corp spate pat, debara.
Coordonate locale: mm, fata corpului = +y, sus = +z, x mic = dreapta privit din fata. Dimensiunile pieselor sunt cele din planul de debitare R03;
pozitiile vin din modelele FreeCAD (inventar 07.10.2026), rotite cu fata spre +y."""
from montaj_specs import Spec, drawer
import montaj_hw, montaj_lib as L
from montaj_comun import B, caps, finish, R03, LIB_LETTERS

VIEWS = {'spate_usa': [0.45, -1.0, 0.4], 'dedesubt': [-0.45, 0.7, -1.0], 'jos_fata': [0.4, 1.0, -0.55]}


# ================================================================== DULAP WC (baie, deasupra rezervorului)
def dulap_wc():
    S = Spec('dulap_wc', 'Dulap WC', 'Dulap suspendat deasupra WC-ului',
             'Baie, pe peretele din spatele WC-ului, cu baza la 1350 mm de pardoseală', (650, 268, 800),
             'Corp suspendat de 650 × 250 × 800 mm cu o poliță fixă, spate PAL 16 mm încastrat (rezistă la umezeală) și două uși fără mâner, '
             'cu balamale Blum CLIP top fără arc și TIP-ON.')
    W, D, H = 650.0, 250.0, 800.0
    B(S, 'lat_d', 'DW-01', 'Lateral dreapta', 0, 18, 0, D, 0, H, 1)
    B(S, 'lat_s', 'DW-01', 'Lateral stânga', W - 18, W, 0, D, 0, H, 1)
    B(S, 'baza', 'DW-02', 'Bază', 18, W - 18, 16, D, 0, 18, 1)
    B(S, 'polita', 'DW-02', 'Poliță (fixă)', 18, W - 18, 16, D, 390, 408, 1)
    B(S, 'blat', 'DW-02', 'Blat corp', 18, W - 18, 16, D, H - 18, H, 1)
    B(S, 'spate', 'DW-03', 'Spate PAL 16 (încastrat)', 18, W - 18, 0, 16, 18, H - 18, 2)
    B(S, 'perete', 'PERETE', 'Peretele din spatele WC-ului', -60, W + 60, -60, 0, -80, H + 80, 3, mat='perete', role='context')
    B(S, 'usa_d', 'DW-04', 'Ușă dreapta', 2, 323, D, D + 18, 2, H - 2, 4, role='door')
    B(S, 'usa_s', 'DW-04', 'Ușă stânga', 327, W - 2, D, D + 18, 2, H - 2, 4, role='door')
    # prindere prin spate: 4 puncte
    for x in (80.0, W - 80.0):
        for z in (60.0, H - 60.0):
            S.hw_at(3, 'diblu_6x40', (x, 0.0, z), az=(0, 1, 0), explode=90, letter='T')
            S.hw_at(3, 'surub_4x40', (x, 16.0, z), az=(0, 1, 0), explode=150, letter='U')
            S.hw_at(3, 'saiba', (x, 16.0, z), az=(0, 1, 0), explode=120, letter='W', dash=False)
            L.hole(S.parts[5], 'hang', (x, 16.0, z), (0, 1, 0), 6.0, 16, 'șurub în perete', through=True)
    L.hinges(S, 4, 'usa_d', 'lat_d', '70T3550')
    L.hinges(S, 4, 'usa_s', 'lat_s', '70T3550')
    L.tipon(S, 5, 'usa_d', 'blat', 283.0)
    L.tipon(S, 5, 'usa_s', 'blat', 367.0)
    montaj_hw.auto(S)
    caps(S, 6, ('lat_d', 'lat_s'))
    S.final_views = ['fata']
    S.views = dict(VIEWS)
    S.gbox = (1750, -5550, 2400, -5300)
    S.time = '≈ 2 ore'
    S.people = '2 la prinderea pe perete'
    S.wall = dict(kind='prin_spate', unit_h=800, note='Peretele din spatele WC-ului: deasupra cadrului de instalare (1210 mm) e peretele existent. Verifică traseele de apă înainte să găurești.')
    S.pre = ['Faianța din spatele WC-ului e montată și rostuită.', 'Cadrul WC și clapeta sunt montate (clapeta rămâne accesibilă sub dulap).']
    S.step(1, 'Corpul: laterale, bază, poliță și blat', 'fata',
           ['Pune lateralele DW-01 pe covor și bate cepurile în muchiile bazei, poliței și blatului (DW-02).',
            'Prinde baza, polița (la 390 mm) și blatul între laterale cu confirmate, de la exteriorul lateralelor.',
            'Verifică diagonalele înainte să strângi confirmatele.'],
           check=['Corpul are 650 × 800 mm la exterior; diagonalele sunt egale ±2 mm.'],
           extra={'explode': {'lat_d': [-90, 0, 0], 'lat_s': [90, 0, 0]}})
    S.step(2, 'Spatele PAL 16 încastrat', 'spate',
           ['Așază corpul cu fața în jos și introdu spatele DW-03 între laterale, bază și blat.',
            'Prinde-l cu confirmate prin laterale, bază și blat în muchiile spatelui, iar prin spate în muchia poliței.'],
           warn=['Spatele de 16 mm ține corpul pe perete: nu îl înlocui cu HDF.'], extra={'explode': {'spate': [0, -90, 0]}})
    S.step(3, 'Prinderea pe perete', 'fata',
           ['Marchează pe perete linia de jos a corpului la 1350 mm de pardoseală.',
            'Prezintă corpul pe linie, marchează cele 4 găuri prin spate (la 80 mm de laterale și 60 mm de sus și de jos), apoi ia-l jos.',
            'Găurește după tipul peretelui (pagina „Prindere în perete”), pune dibluurile și prinde corpul cu șuruburi 4 × 40 cu șaibă.'],
           warn=['Nu găuri în dreptul țevilor de apă ale rezervorului (cadrul WC e dedesubt).'], extra={'explode': {}})
    S.step(4, 'Ușile: plăcuțe pe laterale, balamale pe uși', 'sus',
           ['Găurește în fiecare ușă 2 cupe Ø35 × 13 (Forstner) la 22,5 mm de muchia dinspre balama (TB = 5), la 102 mm de sus și de jos.',
            'Prinde balamalele în cupe cu câte 2 șuruburi 3,5 × 17 și plăcuțele pe laterale cu câte 2 șuruburi 3,5 × 15, la 37 mm de muchia din față.',
            'Agață ușa: clipsează brațul balamalei pe plăcuță (întâi de sus).'],
           extra={'explode': {'usa_d': [0, 260, 0], 'usa_s': [0, 260, 0]},
                  'detail': {'view': 'spate_usa', 'only': ['usa_d'], 'hw': ['BA', 'D17'],
                             'text': 'Spatele ușii din dreapta: 2 balamale în cupele Ø35 × 13, fiecare cu 2 șuruburi 3,5 × 17. Cupa e la 22,5 mm de muchie (TB 5).'}})
    S.step(5, 'TIP-ON și reglajul ușilor', 'jos_fata',
           ['Prinde sub blatul corpului câte un adaptor TIP-ON în dreptul marginii de deschidere a fiecărei uși, cu 2 șuruburi, și introdu TIP-ON-ul în adaptor.',
            'Lipește sau înșurubează placa metalică Ø15 pe spatele ușii, în dreptul magnetului.',
            'Reglează ușile din balamale: rost 3–4 mm între ele, 2 mm pe laterale; apoi reglează TIP-ON-ul (+4 / −1 mm) până ușa se deschide la apăsare și se închide fără să sară.'],
           extra={'explode': {'usa_d': [0, 260, 0], 'usa_s': [0, 260, 0]}})
    S.step(6, 'Capacele de confirmat', 'fata', ['Pune capacele pe confirmatele de pe lateralele corpului.'], extra={'explode': {}})
    return finish(S, notes=['Dulapul e 268 mm adânc cu ușile (250 corpul + 18 ușile). Ușile sunt aplicate peste laterale (FA 16, TB 5).'])
