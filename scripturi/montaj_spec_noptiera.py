"""Specificatie de montaj: noptiera (R04, codurile N-xx din planul de debitare R03).
Sertare Blum MOVENTO 760H3500S + TIP-ON BLUMOTION, dupa catalogul Blum (2022/23 p. 437, 2024/25 p. 419 / 428) si MD TIP-ON BLUMOTION.
Ordine: blatul dublu se lipeste primul (24 h), glisierele se prind pe laterale cat sunt intinse pe podea, cutia de sustinere se fixeaza
din interiorul corpului inainte de sertare, TIP-ON BLUMOTION + bara de sincronizare inainte de cutiile de sertar."""
from montaj_specs import Spec, drawer
import montaj_hw


def noptiera():
    S = Spec('noptiera', 'Noptieră', 'Noptieră cu 2 sertare și blat plutitor',
             'Dormitor, lângă pat, pe partea ferestrei, cu spatele spre peretele de vest', (500, 420, 516),
             'Corp de 500 × 382 × 355 mm (pe soclu de 5 mm) cu două sertare Blum MOVENTO cu TIP-ON BLUMOTION, cutie de susținere pe partea dinspre pat '
             'și blat plutitor de 36 mm, cu bandă LED în nișa de sub blat.')
    W, D = 500, 382
    S.rail_letter = 'M'
    # (x mic = dreapta, x mare = stanga, privit din fata; fata = +y)
    S.part('lat_d', 'N-01', 'Lateral dreapta', (0, 0, 5, 18, D, 355), 'front', 2)
    S.part('lat_s', 'N-01', 'Lateral stânga', (W - 18, 0, 5, 18, D, 355), 'front', 2)
    S.part('baza', 'N-02', 'Bază corp', (18, 0, 5, W - 36, D, 18), 'front', 3)
    S.part('blat_c', 'N-02', 'Blat corp (placa de sus)', (18, 0, 342, W - 36, D, 18), 'front', 3)
    S.part('spate', 'N-03', 'Spate HDF', (2, -3, 8, W - 4, 3, 351), 'hdf', 4)
    S.part('sb_jos', 'N-06', 'Suport blat – fund', (380, 0, 360, 120, 260, 18), 'front', 5)
    S.part('sb_sus', 'N-06', 'Suport blat – capac', (380, 0, 462, 120, 260, 18), 'front', 5)
    S.part('sb_l1', 'N-07', 'Suport blat – lateral dreapta', (380, 0, 378, 18, 260, 84), 'front', 5)
    S.part('sb_l2', 'N-07', 'Suport blat – lateral stânga', (482, 0, 378, 18, 260, 84), 'front', 5)
    # sertare: profilul glisierei de jos la 1 mm peste baza (glisierele se prind inainte de asamblare: +1 mm, Blum)
    G1 = drawer(S, 's1', 'N-S', 18, D, 24.0, W - 36, 350, 120, 7, 2, 8, (2, D, 8, 496, 18, 174), 'N-04', 'Front sertar jos', step_tob=6)
    G2 = drawer(S, 's2', 'N-S', 18, D, 190.0, W - 36, 350, 120, 7, 2, 8, (2, D, 185, 496, 18, 173), 'N-05', 'Front sertar sus', step_tob=6)
    S.part('sb_f', 'N-08', 'Suport blat – capac față (încastrat)', (398, 242, 378, 84, 18, 84), 'front', 9)
    S.part('blat1', 'N-09', 'Blat plutitor – strat 1', (0, 0, 480, 500, 420, 18), 'top', 9)
    S.part('blat2', 'N-09', 'Blat plutitor – strat 2 (lipit)', (0, 0, 498, 500, 420, 18), 'top', 9)
    S.part('led', 'LED', 'Bandă LED 24 V în nișa de sub blat', (20, 350, 475, 350, 17, 5), 'led', 9)
    S.part('perete', 'PERETE', 'Peretele de vest', (-60, -63, 0, 620, 60, 600), 'perete', 11, role='context')
    for p in S.parts:                                    # glisierele se misca odata cu lateralul pe care sunt prinse
        if p['code'] == 'SL':
            p['follow'] = 'lat_s' if p.get('mirror') else 'lat_d'
    # capacul N-08 se prinde doar in laterale (fundul cutiei e deja fixat pe corp, capacul cutiei poarta blatul)
    S.skip_joints = [('sb_f', 'sb_jos'), ('sb_f', 'sb_sus')]
    S.final_views = ['fata', 'sus']
    S.views = {'dedesubt': [-0.45, 0.7, -1.0]}
    S.front_detail = True
    S.front_step = 8
    S.gbox = (300, -950, 720, -450)
    S.time = '≈ 4 ore de lucru + 24 de ore pentru lipirea blatului (se face primul)'
    S.people = '1 (2 la ridicarea corpului)'
    S.wall = dict(kind='antirasturnare', unit_h=360, unit_d=382, note='noptieră joasă: colțarul e opțional, dar recomandat dacă locuiesc copii sau în cutremur')
    S.pre = ['Podeaua finită (parchet) din dormitor e montată, iar peretele de vest vopsit.',
             'Alimentarea LED 24 V (sursa comună din dormitor) e adusă lângă noptieră înainte de montajul blatului.',
             'Priza dublă din dreapta patului (P02, la 750 mm) rămâne liberă: noptiera se așază în fața ei, nu o acoperă.']
    S.notes = ['Cote Blum MOVENTO 760H (NL 350): lățimea interioară a sertarului SKW = LW − 42 = 422; lungimea SKL = NL − 10 = 340; '
               'fundul retras 13 mm; fundul la 28,5 mm deasupra profilului glisierei; bara de sincronizare LW − 267 = %d mm.' % G1['rod']]

    # ------------------------------------------------------------------ feronerie pozitionata explicit
    # spatele HDF: 3,5 x 16 la ~150 mm, in muchiile lateralelor, bazei si blatului corp
    for x in (9.0, W - 9.0):
        for z in (40.0, 182.0, 328.0):
            S.hw_at(4, 'surub_3_5x16', (x, -3.0, z), az=(0, -1, 0), attach='spate', explode=45, letter='D')
    for z in (14.0, 351.0):
        for x in (70.0, 190.0, 310.0, 430.0):
            S.hw_at(4, 'surub_3_5x16', (x, -3.0, z), az=(0, -1, 0), attach='spate', explode=45, letter='D')
    # cutia de sustinere pe corp: 4 suruburi 4 x 30 de jos, prin blatul corpului (18) in fundul cutiei (12)
    for x in (405.0, 465.0):
        for y in (45.0, 215.0):
            S.hw_at(5, 'surub_4x30', (x, y, 342.0), az=(0, 0, -1), attach='blat_c', explode=55, letter='E')
    # fronturile: 4 x 25 + saiba din interior, prin fata interioara (18) in front (7 mm)
    for g, tag in ((G1, 's1'), (G2, 's2')):
        x0, x1 = g['xo'] + 16 + 40, g['xo'] + 16 + g['lw'] - 40
        z0, z1 = g['zb'] + 16 + 20, g['zb'] + 16 + 91 - 20
        for x in (x0, x1):
            for z in (z0, z1):
                S.hw_at(8, 'saiba', (x, D - 18.8, z), az=(0, -1, 0), attach=tag + '.fa', explode=40, letter='N', tag='w')
                S.hw_at(8, 'surub_4x25', (x, D - 18.8 - 3.0, z), az=(0, -1, 0), attach=tag + '.fa', explode=60, letter='N', tag='s')
        for x in (g['xo'] + 16 + 70, g['xo'] + 16 + g['lw'] - 170):
            S.hw_at(8, 'banda_dublu', (x, D, z1 + 4), az=(0, 1, 0), ax=(1, 0, 0), attach=tag + '.fr', explode=0, letter='H', dash=False)
    # blatul: 4 x 30 din interiorul cutiei, prin capac (18) in blat (12)
    for x in (410.0, 470.0):
        for y in (50.0, 210.0):
            S.hw_at(9, 'surub_4x30', (x, y, 462.0), az=(0, 0, -1), attach='sb_sus', explode=45, letter='E')
    # colțarul anti-rasturnare: pe blatul corpului, lipit de perete
    S.hw_at(11, 'coltar_40', (170.0, -3.0, 360.0), az=(0, 0, 1), ax=(1, 0, 0), explode=60, letter='L', dash=False)
    for y in (11.0, 27.0):
        S.hw_at(11, 'surub_4x16', (180.0, y, 362.0), az=(0, 0, 1), explode=110, letter='I')
    S.hw_at(11, 'diblu_6x40', (180.0, -3.0, 390.0), az=(0, 1, 0), explode=70, letter='T')
    S.hw_at(11, 'surub_4x40', (180.0, -1.0, 390.0), az=(0, 1, 0), explode=125, letter='U')
    info = montaj_hw.auto(S)
    # capace pe confirmatele vizibile (fețele laterale ale corpului si ale cutiei)
    for h in [h for h in S.hwi if h['model'] == 'confirmat']:
        if h['attach'] in ('lat_d', 'lat_s', 'sb_l1', 'sb_l2') and abs(h['az'][0]) > 0.9:
            S.hw_at(10, 'capac_confirmat', h['at'], az=h['az'], attach=h['attach'], explode=30, letter='B', dash=False)

    # ------------------------------------------------------------------ lista de feronerie (cantitatile se numara din model)
    n = montaj_hw.count(S)
    q = lambda L, extra=0: sum(v for (l, m), v in n.items() if l == L) + extra
    S.hardware('A', 'Confirmat Ø7 × 50, hex 4', q('A', 6), '%d în model + 6 rezervă' % q('A'), '3, 5, 7, 9', model='confirmat')
    S.hardware('B', 'Capac confirmat, culoarea plăcii (cashmere)', q('B', 4), 'pe confirmatele vizibile', '10', model='capac_confirmat')
    S.hardware('C', 'Cep lemn Ø8 × 35', q('C', 4), 'ghidare în îmbinări; cu puțin adeziv în muchie', '3, 5, 7, 9', model='cep')
    S.hardware('D', 'Șurub PAL 3,5 × 16, cap înecat', q('D', 2), 'spatele HDF, la ~150 mm', '4', model='surub_3_5x16')
    S.hardware('E', 'Șurub PAL 4 × 30, cap înecat', q('E'), '4 cutia pe corp (de jos) + 4 blatul pe cutie (din interior)', '5, 9', model='surub_4x30')
    S.hardware('F', 'Blum MOVENTO 760H3500S, pereche stânga + dreapta (NL 350)', '2 perechi', 'se prind pe laterale înainte de asamblare', '2', model='glisiera_movento')
    S.hardware('G', 'Blum TIP-ON BLUMOTION pentru MOVENTO (S1), pereche', '2 perechi', 'se clipsează pe glisieră, în spate', '6', model='tip_on')
    S.hardware('Q', 'Bară de sincronizare TIP-ON BLUMOTION, tăiată la %d mm (LW − 267)' % G1['rod'], 2, 'una pe sertar', '6', model='bara_sincronizare')
    S.hardware('M', 'Șurub PAL Blum 3,5 × 15 (609.1500)', q('M', 4), '12 glisiere (3 pe glisieră) + 8 cleme (2 pe clemă) + rezervă', '2, 7', model='surub_3_5x15')
    S.hardware('P', 'Clemă de cuplare Blum MOVENTO T51.7601, pereche', '2 perechi', 'sub fundul sertarului, în colțurile din față', '7', model='cleme_movento')
    S.hardware('H', 'Bandă dublu adeziv 25 mm + distanțiere 2 și 3 mm', '1 set', 'poziționarea fronturilor înainte de șuruburi', '8', model='banda_dublu')
    S.hardware('N', 'Șurub PAL 4 × 25 cap bombat + șaibă M4 (Ø9)', '%d + %d' % (n.get(('N', 'surub_4x25'), 0), n.get(('N', 'saiba'), 0)), 'fronturile, din interior (4 pe front)', '8', model='surub_4x25')
    S.hardware('J', 'Adeziv lemn PVAC D3 + 4–6 clești', '1 tub', 'lipirea celor 2 straturi de blat', '1')
    S.hardware('K', 'Bandă LED 24 V COB, 350 mm + profil + cablu 2 × 0,75', '1 set', 'sursa de 24 V e comună cu restul LED-urilor din dormitor', '9')
    S.hardware('L', 'Colțar anti-răsturnare 40 × 40', 1, 'opțional, se pune la perete (vezi „Prindere în perete”)', '11', model='coltar_40')
    S.hardware('I', 'Șurub PAL 4 × 16, cap bombat', 2, 'colțarul în blatul corpului', '11', model='surub_4x16')
    S.hardware('T', 'Diblu nylon Ø6 × 40', 1, 'în perete, după tipul peretelui', '11', model='diblu_6x40')
    S.hardware('U', 'Șurub PAL 4 × 40, cap înecat', 1, 'colțarul în diblu', '11', model='surub_4x40')

    for j in [('Bază – lateral dreapta', 'N-02', 'N-01', D), ('Bază – lateral stânga', 'N-02', 'N-01', D),
              ('Blat corp – lateral dreapta', 'N-02', 'N-01', D), ('Blat corp – lateral stânga', 'N-02', 'N-01', D)]:
        S.joint(3, *j)
    S.joint(5, 'Suport: laterale – fund', 'N-07', 'N-06', 260)
    S.joint(5, 'Suport: laterale – capac', 'N-07', 'N-06', 260)
    S.joint(7, 'Sertar: laterale – față / spate', 'N-S.FS', 'N-S.L', 91)
    S.joint(7, 'Sertar: laterale – fund', 'N-S.F', 'N-S.L', 340)

    # ------------------------------------------------------------------ pasii
    lat_out = {'lat_d': [-110, 0, 0], 'lat_s': [110, 0, 0]}
    S.step(1, 'Pregătire: blatul dublu (se usucă 24 de ore)', 'sus',
           ['Lipește cele două straturi N-09 (2 × 18 mm = 36 mm): adeziv PVAC pe toată fața unuia, în zig-zag, întins cu o spatulă.',
            'Pune straturile unul peste altul, cu muchiile aliniate (fețele decorate în afară), și strânge cu 4–6 clești, cu șipci între clești și placă.',
            'Șterge imediat adezivul ieșit pe margini cu o cârpă umedă.',
            'Lasă blatul 24 de ore: între timp montezi corpul și sertarele. Cantul de 42 × 2 mm se pune după uscare (sau comanzi blatul dublat de la atelier).'],
           warn=['Fără clești, blatul se curbează: nu îl lăsa doar sub greutăți.'],
           check=['Muchiile celor două straturi sunt aliniate; grosime totală 36 mm.'], hw='J',
           extra={'solo': ['blat1', 'blat2'], 'explode': {'blat2': [0, 0, 70]}, 'frame': 'new'})
    S.step(2, 'Glisierele pe laterale (înainte de asamblare)', 'fata',
           ['Pune lateralele N-01 pe covor, cu fața interioară în sus și muchia din față spre tine. Lateralele sunt în oglindă.',
            'Găurește întâi confirmatele (Ø7, de la exterior) și cepurile, după „Desene de găurire”.',
            'Trasează pe fața interioară axa șuruburilor glisierei, măsurată de la muchia de jos a lateralului: %g mm (sertarul de jos) și %g mm (sertarul de sus).'
            % (G1['screw_z'] - 5, G2['screw_z'] - 5),
            'Pune glisierele (F) cu capătul din față la muchia din față a lateralului și prinde-le cu câte 3 șuruburi Blum 3,5 × 15 (M): la 37, 69 și 261 mm de muchia din față.',
            'Glisiera din dreapta merge pe lateralul din dreapta (N-01 dreapta), cea din stânga pe stânga: sunt marcate pe ambalaj (L / R).'],
           warn=['Cotele de înălțime includ +1 mm cerut de Blum când glisierele se montează înainte de asamblarea corpului.',
                 'Folosește șablonul Blum T65.1000.02 sau un distanțier tăiat la cota de mai sus: nu trasa fiecare gaură cu metrul.'],
           check=['Cele două glisiere de pe același lateral sunt paralele cu muchia de jos.', 'Glisierele din stânga și din dreapta sunt la aceeași înălțime.'],
           hw='F M',
           extra={'explode': {'s1.rl': [40, 0, 0], 's2.rl': [40, 0, 0], 's1.rr': [-40, 0, 0], 's2.rr': [-40, 0, 0]},
                  'detail': {'view': 'stanga', 'hide': ['lat_d', 's1.rl', 's2.rl'], 'frame': 'all',
                                            'text': 'Lateralul din stânga, fața interioară: profilele MOVENTO cu câte 3 șuruburi 3,5 × 15. Axa șuruburilor la %g / %g mm de muchia de jos.'
                                            % (G1['screw_z'] - 5, G2['screw_z'] - 5)}})
    S.step(3, 'Corpul: bază și blat corp între laterale', 'fata',
           ['Bate cepurile (C) cu puțin adeziv în muchiile bazei și ale blatului corpului (N-02).',
            'Așază un lateral pe muchie, apoi bază și blatul corp pe cepuri; închide cu al doilea lateral.',
            'Prinde cu confirmate (A) de la exteriorul lateralelor: întâi baza, apoi blatul corp, la 342 mm deasupra bazei.',
            'Verifică unghiurile cu un colțar și măsoară diagonalele (diferență sub 2 mm). Strânge confirmatele abia după, cu cuplu mic.'],
           warn=['Cantul de 2 mm al bazei și al blatului corp merge în față.'],
           check=['Lățime exterioară 500 mm, adâncime 382 mm, înălțime 355 mm.', 'Diagonale egale ±2 mm.'], hw='A C',
           extra={'explode': dict(lat_out)})
    S.step(4, 'Spatele HDF', 'spate',
           ['Întoarce corpul cu fața în jos, pe covor, și pune spatele HDF 3 mm (N-03) pe muchiile din spate.',
            'Aliniază un colț, verifică diagonalele corpului și prinde spatele cu șuruburi 3,5 × 16 (D) la ~150 mm, începând din colțuri.',
            'Spatele ține corpul în unghi drept: dacă diagonalele sunt egale înainte de fixare, rămân egale și după.'],
           check=['Spatele nu iese în afara corpului.'], hw='D',
           extra={'explode': {'spate': [0, -80, 0]}})
    S.step(5, 'Cutia de susținere a blatului', 'fata',
           ['Asamblează cutia din fund și capac (N-06) și laterale (N-07), cu cepuri (C) și confirmate (A) prin fund și capac. Capacul din față (N-08) se pune abia la pasul 9.',
            'Așază cutia pe placa de sus a corpului, în dreapta-spate (privit din față: pe partea dinspre pat), aliniată la spate și la lateralul corpului.',
            'Prinde-o din interiorul corpului, de jos, cu 4 șuruburi 4 × 30 (E) prin placa de sus a corpului în fundul cutiei.',
            'Prinde fundul cutiei și de muchia lateralului de corp cu 2 confirmate (A), prin deschiderea din față a cutiei.'],
           warn=['Cutia susține blatul în consolă: nu o monta fără cepuri și fără cele 4 șuruburi de jos.'],
           check=['Cutia e la spate, aliniată cu lateralul și cu spatele corpului.'], hw='A C E',
           extra={'explode': {k: [0, 0, 130] for k in ('sb_jos', 'sb_sus', 'sb_l1', 'sb_l2')},
                  'detail': {'view': 'dedesubt', 'hide': ['baza', 'lat_d', 's1.rl', 's2.rl', 's1.rr', 's2.rr', 'spate', 'sb_jos', 'sb_sus', 'sb_l1', 'sb_l2'], 'frame': 'hw',
                             'hw': ['E'], 'with': [],
                             'text': 'Văzut de jos, din interiorul corpului (baza și lateralul din dreapta ascunse): cele 4 șuruburi 4 × 30 prin placa de sus a corpului în fundul cutiei.'}})
    S.step(6, 'TIP-ON BLUMOTION și bara de sincronizare', 'fata',
           ['Trage în față elementele glisante ale glisierelor (sunt deja în corp, de la pasul 2).',
            'Clipsează unitatea TIP-ON BLUMOTION (G) pe fiecare glisieră și împinge-o spre spate până face clic.',
            'Taie bara de sincronizare (Q) la %d mm (LW − 267 = 464 − 267) și introdu-i capetele în cele două unități ale aceluiași sertar, până se aude clicul.' % G1['rod'],
            'Împinge glisierele înapoi. Repetă pentru al doilea sertar.'],
           warn=['Bara netăiată sau tăiată prea scurt blochează sincronizarea: măsoară lumina corpului (LW) pe loc înainte să tai.'],
           check=['Unitățile stânga și dreapta sunt clipsate la fel (aceeași poziție pe glisieră).'], hw='G Q',
           extra={'explode': {}, 'frame': 'all'})
    S.step(7, 'Cutiile de sertar și clemele', 'fata',
           ['Pentru fiecare sertar: două laterale (N-S.L), față și spate interioare (N-S.FS) și fundul (N-S.F) de 16 mm, retras 13 mm față de muchia de jos a lateralelor.',
            'Prinde cutia cu cepuri (C) și confirmate (A): prin laterale în față, spate și fund, și prin fund în față și spate. Verifică unghiurile.',
            'Dă în capătul din spate al fiecărui lateral o gaură Ø6 × 10 (7 mm de fața exterioară, 11 mm de jos): aici intră cârligul glisierei.',
            'Prinde sub fund, în colțurile din față, clemele de cuplare (P), lipite de lateral și de față, cu câte 2 șuruburi 3,5 × 15 (M).',
            'Așază cutia pe glisierele trase în față și împinge-o până se aud clemele. Reglează înălțimea și lateral din roata clemei.'],
           warn=['Fără gaura Ø6 din spate, sertarul nu se prinde în cârlig și sare de pe glisieră.'],
           check=['Lățimea interioară a sertarului este 422 mm (LW − 42), lungimea 340 mm (NL − 10).', 'Sertarul intră până la capăt fără frecare.'], hw='A C P M',
           extra={'explode': {k: [0, 300, 0] for k in ('s1.l1', 's1.l2', 's1.fu', 's1.fa', 's1.sp', 's2.l1', 's2.l2', 's2.fu', 's2.fa', 's2.sp')},
                  'detail': {'view': 'jos', 'hide': [p['id'] for p in S.parts if p['step'] < 7], 'frame': 'new', 'hw': ['P', 'M'],
                             'text': 'Sertarul văzut de dedesubt: clemele de cuplare în colțurile din față, cu câte 2 șuruburi; găurile Ø6 × 10 pentru cârlig în capătul din spate al lateralelor.'}})
    S.step(8, 'Fronturile', 'fata',
           ['Fixează fronturile (N-04 jos, N-05 sus) pe cutiile de sertar, urmând cele două pagini de detaliu (poziționare cu distanțiere, bandă dublu adeziv (H), apoi 4 șuruburi 4 × 25 cu șaibă (N) din interior).',
            'Rosturile: 2 mm pe laterale, 3 mm între fronturi și sub front, egale peste tot.',
            'Apasă pe front: TIP-ON BLUMOTION deschide sertarul; la închidere trebuie să se amortizeze.'],
           check=['Cele două fronturi sunt aliniate și cu rost egal.', 'Sertarele se deschid prin apăsare și se închid amortizat.'], hw='H N',
           extra={'explode': {'s1.fr': [0, 110, 0], 's2.fr': [0, 110, 0]}})
    S.step(9, 'Blatul plutitor, capacul cutiei și LED-ul', 'sus',
           ['Pune blatul dublu (uscat de la pasul 1) pe cutie: aliniat la spate și la lateralul din stânga corpului; iese 38 mm în față.',
            'Prinde-l din interiorul cutiei, prin deschiderea din față, cu 4 șuruburi 4 × 30 (E) prin capacul cutiei (18 mm) în blat (12 mm).',
            'Închide cutia cu capacul din față N-08 (încastrat), prins cu cepuri și confirmate prin lateralele cutiei.',
            'Lipește banda LED în nișa de sub blat, la 20 mm de muchia din față, și trece cablul spre spate.'],
           warn=['Șuruburile de 30 mm trec prin 18 mm de capac: nu folosi mai lungi, ies prin fața blatului.'], hw='E A C K',
           extra={'explode': {'blat1': [0, 0, 140], 'blat2': [0, 0, 140], 'sb_f': [0, 120, 0], 'led': [0, 60, -40]}})
    S.step(10, 'Capacele de confirmat', 'fata',
           ['Pune capacele (B) pe confirmatele vizibile: pe lateralele corpului și pe lateralele cutiei.', 'Curăță de praf și amprente.'],
           check=['Niciun confirmat vizibil.'], hw='B', extra={'explode': {}})
    S.step(11, 'Poziționare și prindere în perete', 'stanga',
           ['Așază noptiera lângă pat, pe partea ferestrei, cu spatele la perete. Cablul LED trece prin spate.',
            'Verifică nivelarea: corpul stă pe muchiile lateralelor, cu baza la 5 mm de podea; la nevoie pune plăcuțe sub laterale.',
            'Prinde colțarul (L) de placa de sus a corpului cu 2 șuruburi 4 × 16 (I) și de perete cu diblu Ø6 × 40 (T) și șurub 4 × 40 (U), după pagina „Prindere în perete”.'],
           hw='L I T U', extra={'explode': {}, 'detail': {'view': 'stanga', 'hide': ['blat1', 'blat2', 'led'], 'frame': 'new',
                                                       'text': 'Colțarul pe placa de sus a corpului (sub blat), lipit de perete: 2 șuruburi 4 × 16 în corp, diblu Ø6 × 40 și șurub 4 × 40 în perete.'}})
    return S
