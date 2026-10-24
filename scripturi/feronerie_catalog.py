"""Catalogul feroneriei folosite in apartament (R2, 07.10.2026): metadate pure (fara FreeCAD), folosite de feronerie_cad.py (modele),
feronerie_blender.py (randari) si montaj_izo.py (pagini PDF).
precizie: 'exact'   = geometrie dupa standard / fisa oficiala (toate cotele care conteaza la montaj si la vedere)
          'gabarit' = cote de montaj si gabarit din documentatia Blum; mecanismul interior e simplificat (STEP oficial Blum il inlocuieste)
          'generic' = produsul exact nu e ales inca; model tipic pentru categoria lui
Conventie geometrica (mm): +Z iese din placa; z = 0 e fata placii / capul surubului; corpul piesei merge spre -Z.
Piesele Blum si cele de corp au cadrul lor descris in 'cadru'."""

COL = {'zinc': (0.80, 0.81, 0.83), 'zinc_galben': (0.86, 0.77, 0.47), 'nichel': (0.76, 0.77, 0.79), 'otel': (0.60, 0.62, 0.65),
       'inox': (0.82, 0.84, 0.86), 'crom': (0.90, 0.91, 0.93), 'negru': (0.09, 0.09, 0.10), 'lemn': (0.84, 0.69, 0.48),
       'alb': (0.94, 0.94, 0.92), 'cashmere': (0.80, 0.76, 0.70), 'gri_blum': (0.53, 0.54, 0.55), 'gri_inchis': (0.30, 0.31, 0.33),
       'nylon': (0.88, 0.88, 0.85), 'galben': (0.95, 0.76, 0.22), 'rosu': (0.78, 0.22, 0.20), 'magnet': (0.22, 0.22, 0.24)}
METAL = {'zinc', 'zinc_galben', 'nichel', 'otel', 'inox', 'crom', 'magnet'}

BLUM_TD = 'Blum: Product details 71T3550 / 71B3590; MD „CLIP top BLUMOTION, CLIP top, CLIP” (11.24); TD-151 CLIP top BLUMOTION 105°'
SRC_SCR = 'DIN 7505 / EN 14592 (cap, miez, pas nominal)'

# id, cod in documente, nume, dimensiuni, unde se foloseste, sursa, precizie, cadru
CATALOG = [
    ('confirmat', 'A', 'Confirmat Ø7 × 50, hex 4', 'filet Ø7 × 38, miez Ø4,75, pas 3; umăr Ø7 × 9; cap înecat Ø10 × 3; hex 4',
     'îmbinări de corp: laterale cu baze, blaturi, despărțitori; cutii de sertar', "McFeely's 7050-CSP (cotele), GTV WK-CF0750-01 (hex 4)", 'exact', 'standard'),
    ('capac_confirmat', 'B', 'Capac pentru confirmat (hex 4)', 'cap Ø14 × 1,6, știft hexagonal 4 × 3,5', 'peste capul confirmatului, pe fețele vizibile',
     'tip uzual pentru hex 4', 'generic', 'standard'),
    ('cep', 'C', 'Cep de lemn Ø8 × 35', 'Ø8 × 35, teșit 1 × 45°, 10 caneluri drepte', 'ghidare și blocare în îmbinări (între confirmate)', 'DIN 68150', 'exact', 'standard'),
    ('surub_3_5x15', 'D15', 'Șurub PAL Blum 3,5 × 15 (609.1500)', 'cap înecat Ø7, PZ2, miez Ø2,25, pas 1,6', 'plăcuțe de balama, glisiere MOVENTO, cleme',
     'catalog Blum 2024/25 p. 426; ' + SRC_SCR, 'exact', 'standard'),
    ('surub_3_5x17', 'D17', 'Șurub PAL Blum 3,5 × 17 (609.1700)', 'cap înecat Ø7, PZ2', 'cupa balamalei în ușă (2 pe balama)',
     'catalog Blum 2024/25 p. 426; MD CLIP top p. 4', 'exact', 'standard'),
    ('surub_3_5x16', 'D', 'Șurub PAL 3,5 × 16', 'cap înecat Ø7, PZ2', 'spate HDF 3 mm, la ~150 mm', SRC_SCR, 'exact', 'standard'),
    ('surub_4x16', 'I', 'Șurub PAL 4 × 16, cap bombat', 'cap Ø8 × 3, PZ2, miez Ø2,55, pas 1,8', 'fund sertar, colțare', SRC_SCR, 'exact', 'standard'),
    ('surub_4x25', 'N', 'Șurub PAL 4 × 25, cap bombat', 'cap Ø8 × 3, PZ2', 'fronturi de sertar, din interior, cu șaibă', SRC_SCR, 'exact', 'standard'),
    ('surub_4x30', 'E', 'Șurub PAL 4 × 30, cap înecat', 'cap Ø8, PZ2', 'cutii de susținere, cutii de sertar', SRC_SCR, 'exact', 'standard'),
    ('surub_4x40', 'K', 'Șurub PAL 4 × 40, cap înecat, filet parțial', 'cap Ø8, filet 24, tijă Ø2,9', 'colțare anti-răsturnare în diblu', SRC_SCR, 'exact', 'standard'),
    ('saiba', 'W', 'Șaibă M4 (ISO 7089)', 'Ø4,3 / Ø9 × 0,8', 'fronturi de sertar (reglaj ±1 mm prin gaura Ø5)', 'ISO 7089', 'exact', 'standard'),
    ('capsa', 'D*', 'Capsă 10 × 14 (alternativă la șurubul de spate)', 'coroană 10, picioare 14, sârmă 1,2 × 0,6', 'spate HDF, cu capsator pneumatic', 'tip 80/14', 'exact', 'standard'),
    ('pin_raft', 'H', 'Suport raft Ø5 cu talpă', 'știft Ø5 × 8, talpă 9 × 11', 'rafturi mobile (rânduri de găuri Ø5 la 32)', 'tip uzual', 'generic', 'standard'),
    ('coltar_40', 'F', 'Colțar 40 × 40 × 20', 'tablă 2 mm, nervură, 2 găuri Ø4,5 pe aripă', 'îmbinări în unghi, prinderi ascunse', 'tip uzual', 'generic', 'colțul pe axa X; aripi pe +Y și +Z'),
    ('anti_rasturnare', 'AR', 'Colțar anti-răsturnare 35 × 35', 'tablă 2 mm, gaură ovală în aripa de perete', 'prinderea corpurilor înalte de perete', 'tip uzual', 'generic', 'colțul pe axa X; aripi pe +Y și +Z'),
    ('diblu_6x40', 'L*', 'Diblu nylon Ø6 × 40', 'Ø6, 2 fante, aripioare anti-rotire', 'prinderi în perete: colțare, șine', 'tip Fischer SX', 'generic', 'standard'),
    ('balama_blum', 'N*', 'Balama Blum CLIP top 110° aplicată, fără arc (70T3550)', 'cupă Ø35 × 11,3; flanșă 57 × 22 × 3,2; găuri 45 / 9,5; braț 21,5',
     'uși cu TIP-ON (fără arc)', BLUM_TD, 'gabarit', 'z ⟂ ușă (ușa la z<0), x ⟂ lateral (lateral la x<0), y vertical'),
    ('balama_70T3650', 'N2', 'Balama Blum CLIP top 110° semiaplicată, fără arc (70T3650)', 'ca 70T3550, braț cotit 9,5', 'uși pe lateral comun (două uși pe același perete)',
     BLUM_TD, 'gabarit', 'ca 70T3550'),
    ('balama_71B3550', 'N3', 'Balama Blum CLIP top BLUMOTION 110° aplicată (71B3550)', 'cupă Ø35 cu amortizor integrat; flanșă 57 × 22', 'uși cu mâner (dulap dormitor)',
     BLUM_TD, 'gabarit', 'ca 70T3550'),
    ('placuta_balama', 'O', 'Plăcuță Blum CLIP în cruce 0 mm (173L6100)', 'H 8,5; găuri la 32 pe verticală, la 37 de muchia din față; găuri ovale pentru reglaj pe înălțime',
     'pe lateralul corpului, 2 șuruburi 3,5 × 15', 'Blum MD CLIP top p. 3 și 5', 'gabarit', 'ca balamaua: lateralul la x = 0, muchia din față la z = 0'),
    ('tipon_usa', 'G2', 'Blum TIP-ON scurt, cu magnet (956.1004)', 'corp Ø10 × 50, reglaj +4 / −1', 'uși fără mâner (deschidere prin apăsare)', 'Blum MD-019 TIP-ON uși', 'gabarit',
     'axa pe Z; fața din față a corpului la z = 0'),
    ('adaptor_tipon', 'G3', 'Adaptor drept Blum pentru TIP-ON (956.1201)', '53 × 18 × 22, ax la 14,5; șuruburi la 20 și 37', 'TIP-ON prins pe blatul / baza corpului', 'Blum MD-019 p. 5; flyer 956.1201',
     'gabarit', 'baza pe planul y = 0, axa TIP-ON pe Z'),
    ('placa_tipon', 'G4', 'Placă metalică Ø15 pentru TIP-ON cu magnet', 'Ø15 × 1, cu șurub', 'pe ușă, în dreptul TIP-ON', 'Blum MD-019 p. 4', 'gabarit', 'standard'),
    ('glisiera_movento', 'F*', 'Glisieră Blum MOVENTO 760H3500S (NL 350)', 'fund la 28,5 deasupra profilului; lateral sertar la 21 de lateral; șuruburi la 38 mm, la 37 / 69 / 261 (NL 350); SKW = LW − 42, SKL = NL − 10',
     'sertare (noptieră, comode, bucătărie, dressing)', 'catalog Blum 2024/25 p. 419 (secțiune); MD TIP-ON BLUMOTION p. 3', 'gabarit',
     'lateralul la x = 0, muchia din față la y = 0, corpul spre −y; baza profilului la z = 0'),
    ('tip_on', 'G', 'Blum TIP-ON BLUMOTION pentru MOVENTO (S1)', 'unitate ≈ 170 × 81 × 12, se clipsează pe glisieră; bara intră la 133,5 mm de lateral', 'deschidere prin apăsare + închidere amortizată, sertare',
     'Blum MD TIP-ON BLUMOTION LEGRABOX / MOVENTO (formă, LW − 267); catalog 2022/23 p. 437 (secțiune)', 'gabarit', 'ca glisiera'),
    ('cleme_movento', 'CL', 'Clemă de cuplare Blum MOVENTO (T51.7601)', '≈ 52 × 36 × 12 (pană), roată de reglaj, 2 șuruburi 3,5 × 15', 'sub fundul sertarului, în față (prinde sertarul de glisieră)',
     'Blum MD MOVENTO p. 3 și 7', 'gabarit', 'fața de sus (lipită de fund) la z = 0, lateralul sertarului la x = 0, fața sertarului la y = 0'),
    ('bara_sincronizare', 'SY', 'Bară de sincronizare TIP-ON BLUMOTION', 'Ø8, tăiată la LW − 267 (MOVENTO, LW ≥ 294)', 'leagă cele două unități TIP-ON BLUMOTION', 'Blum MD TIP-ON BLUMOTION p. 3', 'gabarit', 'axa pe X'),
    ('glisiera_bile_450', 'GB', 'Glisieră cu bile 450 mm, extragere totală, soft-close', 'înălțime 45, grosime 12,7, 3 elemente', 'sertare interioare dulap dormitor (provizoriu)',
     'standard pentru glisiere 45 × 12,7', 'generic', 'lateralul la x = 0, muchia din față la y = 0'),
    ('picior', 'P', 'Picior reglabil H100', 'talpă Ø60, tub Ø32, reglaj 95–115', 'corpuri de bucătărie, dulapuri înalte', 'tip uzual', 'generic', 'talpa sub bază la z = 0, piciorul spre −z'),
    ('clema_soclu', 'PS', 'Clemă de soclu pentru picior', 'inel Ø32 + talpă 30 × 40', 'prinde plinta de picioare', 'tip uzual', 'generic', 'axa piciorului pe Z'),
    ('suport_suspendare', 'S', 'Agățătoare de corp suspendat', '15 × 52 × 66, reglaj pe înălțime și adâncime', 'colțurile de sus ale corpurilor suspendate', 'tip Camar 807', 'generic',
     'lateralul la x = 0, spatele la y = 0'),
    ('sina_suspendare', 'R', 'Șină de suspendare 300 mm', 'profil 50 × 10 × 1,5', 'pe perete, sub corpurile suspendate', 'tip Camar', 'generic', 'peretele la y = 0'),
    ('bara_ovala', 'BO', 'Bară ovală de dulap 30 × 15', 'țeavă ovală 30 × 15 × 1', 'umerașe (dressing, dulap hol, dulap dormitor)', 'tip uzual', 'generic', 'axa pe X'),
    ('suport_bara', 'SB', 'Suport de capăt pentru bara ovală', 'flanșă Ø42, 3 găuri', 'capetele barei ovale', 'tip uzual', 'generic', 'flanșa pe x = 0'),
    ('banda_dublu', 'T', 'Bandă dublu adeziv 25 mm', '25 × 100 × 0,6 (fâșie)', 'poziționarea fronturilor înainte de șuruburi', 'tip uzual', 'exact', 'standard'),
]
INFO = {c[0]: c for c in CATALOG}
