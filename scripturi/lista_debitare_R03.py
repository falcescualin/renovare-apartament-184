"""Lista de debitare R03 – COMPLETĂ, piesă cu piesă, pentru tot mobilierul la comandă (06.10.2026).

Sursa cotelor: fișierele FreeCAD salvate (tmp/inventar_freecad_mobilier.json, din inventar_freecad_mobilier.py).
În FreeCAD, corpurile bucătăriei, noptierele, comodele, machiajul și sertarele sunt desenate ca blocuri pline;
aici fiecare bloc e desfăcut în plăci după regulile de construcție de mai jos. Dulapul din hol folosește lista
exactă din excel_debitare.py (verificată cu modelul).

REGULI (aceleași pentru toate corpurile):
- dimensiunile sunt FINITE, cu cantul inclus (atelierul scade grosimea cantului la debitare);
- L = lungimea piesei; la stejar fibra merge pe L (piesele de stejar nu se rotesc pe placă);
- canturi: L1, L2 = muchiile lungi, W1, W2 = muchiile scurte; „2” = ABS 2 mm, „0.8” = ABS 0,8 mm,
  „42” = ABS 42 × 2 mm (blaturi dublate / blat de lucru), „-” = fără cant;
- fronturi: cant 2 mm pe toate laturile; corp: muchia din față 2 mm; muchii ascunse fără cant;
- spate: HDF alb 3 mm, bătut pe spate (H − 4, L − 4 mm), sau încastrat între laterale unde e precizat;
- sertare Blum MOVENTO (16 mm): lățime interioară = LW − 42; lateral = NL − 10; fund 16 mm cu retragere 13 mm;
  față/spate interioare = înălțime laterală − 29 mm (ca la dulapul din hol);
- piesele mai lungi decât placa (2780 utili) se împart în dreptul unui despărțitor / al unei îmbinări ascunse.
Iese: tmp/lista_debitare_R03.json (+ CSV). Rulează: python lista_debitare_R03.py"""
import json, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = {(x['doc'], x['label']): x for x in json.loads((ROOT / 'tmp/inventar_freecad_mobilier.json').read_text(encoding='utf-8'))}

MAT = {
    'ALB18': 'PAL alb 18 mm (corp)',
    'CAS18': 'PAL cashmere 18 mm (fronturi, comode, noptiere)',
    'STJ18': 'PAL stejar 18 mm (comodă dormitor, machiaj, blat comodă TV)',
    'ALB16': 'PAL alb 16 mm (cutii de sertar)',
    'HDF3': 'HDF alb 3 mm (spate)',
    'BLAT38': 'Blat de lucru stejar 38 mm 4100 × 600',
}
P = []          # rânduri: dict


def add(mob, cod, den, mat, L, W, n=1, e=('-', '-', '-', '-'), note='', src='', forma=''):
    """e = (L1, L2, W1, W2); forma = '' / 'trapez' / 'oblic' (tăieturi în afara dreptunghiului)"""
    assert L > 0 and W > 0, (cod, L, W)
    P.append(dict(mob=mob, cod=cod, den=den, mat=mat, L=round(L, 1), W=round(W, 1), n=n, L1=e[0], L2=e[1], W1=e[2], W2=e[3],
                  fibra='L' if mat in ('STJ18', 'BLAT38') else '', note=note, src=src, forma=forma))


def inv(doc, label):
    return INV[(doc, label)]


def dims(doc, label):
    b = inv(doc, label)['bb']
    return b[3] - b[0], b[4] - b[1], b[5] - b[2]


FRONT = ('2', '2', '2', '2')


def sertar_movento(mob, cod, LW, NL, H, n, note=''):
    """Cutie de sertar Blum MOVENTO din PAL 16 mm (ALB16)."""
    lw = LW - 42
    add(mob, cod + '.L', 'Lateral sertar (MOVENTO NL %d)' % NL, 'ALB16', NL - 10, H, 2 * n, ('0.8', '-', '-', '-'), 'L1 = muchia de sus. ' + note)
    # fața interioară și spatele stau între laterale, pe fund: grosimea nu contează pentru glisieră → din plăcile de 18 mm
    add(mob, cod + '.FS', 'Față interioară + spate sertar', 'ALB18', lw, H - 29, 2 * n, ('0.8', '-', '-', '-'), 'L1 = muchia de sus; spate: găuri cârlig MOVENTO')
    add(mob, cod + '.F', 'Fund sertar', 'ALB16', lw, NL - 10, n, note='între laterale, retras 13 mm')
    return lw


# =====================================================================  DULAP HOL (lista exactă existentă)
D = {}
exec((ROOT / 'scripturi/excel_debitare.py').read_text(encoding='utf-8').split('# ---------------------------------------------------------------- gaurire')[0], D)
MAPM = {D['W18']: 'ALB18', D['U18']: 'CAS18', D['HDF']: 'HDF3'}
for p in D['P']:
    cod, den, matname, t, L, l, n, e1, e2, e3, e4 = p[:11]
    mat = 'ALB16' if t == 16 else MAPM[matname]
    ce = lambda s: {'2 mm': '2', '0,8 mm': '0.8', '-': '-'}[s]
    forma = 'trapez' if cod in ('C03', 'C04', 'C09') else ''
    add('Dulap hol', 'DH-' + cod, den, mat, L, l, n, (ce(e1), ce(e2), ce(e3), ce(e4)), p[12], 'excel_debitare.py', forma)

# =====================================================================  DRESSING (dressing.FCStd)
M = 'Dressing'
J = 5115.0                                  # îmbinare bază / blat / spate / mască: axul despărțitorului 2 (x 5106–5124)
add(M, 'DR-01', 'Lateral', 'ALB18', 2380, 580, 2, ('2', '-', '0.8', '0.8'), 'L1 = față', 'Lateral_stanga/dreapta')
add(M, 'DR-02', 'Bază (bucata vest)', 'ALB18', J - 3728, 577, 1, ('2', '-', '-', '-'), 'îmbinare sub despărțitorul 2', 'Baza')
add(M, 'DR-03', 'Bază (bucata est)', 'ALB18', 7072 - J, 577, 1, ('2', '-', '-', '-'), 'îmbinare sub despărțitorul 2', 'Baza')
add(M, 'DR-04', 'Blat sus (bucata vest)', 'ALB18', J - 3728, 577, 1, ('2', '-', '-', '-'), 'îmbinare deasupra despărțitorului 2', 'Blat_sus')
add(M, 'DR-05', 'Blat sus (bucata est)', 'ALB18', 7072 - J, 577, 1, ('2', '-', '-', '-'), 'îmbinare deasupra despărțitorului 2', 'Blat_sus')
add(M, 'DR-06', 'Despărțitor', 'ALB18', 2344, 577, 4, ('2', '-', '-', '-'), '', 'Despartitor_1..4')
add(M, 'DR-07', 'Poliță fixă sus 680', 'ALB18', 680, 557, 4, ('2', '-', '-', '-'), 'M1, M2, M4, M5; LED sub muchia din față', 'Polita_sus_M1/2/4/5')
add(M, 'DR-08', 'Poliță fixă sus M3', 'ALB18', 557, 552, 1, ('-', '-', '2', '-'), 'W1 = față (552)', 'Polita_sus_M3')
add(M, 'DR-09', 'Raft mobil 680', 'ALB18', 678, 557, 9, ('2', '-', '-', '-'), 'M2 ×5, M4 ×3, M5 ×1; pe pini Ø5', 'Raft_M2/M4/M5')
add(M, 'DR-10', 'Raft mobil M3', 'ALB18', 557, 550, 2, ('-', '-', '2', '-'), 'W1 = față (550)', 'Raft_M3_1/2')
add(M, 'DR-11', 'Soclu (ascuns de uși)', 'ALB18', 1672, 80, 2, note='retras 40 mm; 2 bucăți cap la cap', src='Soclu')
# spatele: 3 bucăți, cu îmbinările pe despărțitorii 1 și 3 (axe x 4417 / 5685) — încap pe 4 plăci HDF în loc de 5
add(M, 'DR-12', 'Spate HDF (M1)', 'HDF3', 2376, 4417 - 3729, 1, note='încastrat între laterale, bătut pe bază/blat/despărțitori', src='Spate_HDF')
add(M, 'DR-13', 'Spate HDF (M2–M3)', 'HDF3', 2376, 5685 - 4417, 1, note='îmbinări pe despărțitorii 1 și 3', src='Spate_HDF')
add(M, 'DR-13b', 'Spate HDF (M4–M5)', 'HDF3', 2376, 7071 - 5685, 1, note='', src='Spate_HDF')
for w, n, mods in ((704, 2, 'M1, M5'), (695, 2, 'M2, M4'), (567, 1, 'M3')):
    add(M, 'DR-U%d' % w, 'Ușă jos %s' % mods, 'CAS18', 2068, w, n, FRONT, 'push-to-open TIP-ON; 1 cm de podea', 'Usa_jos_*')
    add(M, 'DR-S%d' % w, 'Ușă sus %s' % mods, 'CAS18', w, 377, n, FRONT, '', 'Usa_sus_*')
add(M, 'DR-14', 'Mască tavan (vest)', 'CAS18', J - 3710, 60, 1, ('2', '-', '-', '-'), 'se taie 60, se ajustează pe tavan (37 mm în model)', 'Masca_tavan')
add(M, 'DR-15', 'Mască tavan (est)', 'CAS18', 7090 - J, 60, 1, ('2', '-', '-', '-'), 'îmbinare în dreptul rostului M2/M3', 'Masca_tavan')
sertar_movento(M, 'DR-SI', 680, 500, 150, 6, 'sertare interioare: M2 ×2, M4 ×4')

# =====================================================================  SPĂLĂTORIE VESTIBUL (spalatorie_vestibul.FCStd)
M = 'Spălătorie'
add(M, 'SP-01', 'Lateral exterior stânga', 'ALB18', 2460, 650, 1, ('2', '-', '0.8', '-'), 'W1 = sus', 'Lateral_stanga')
add(M, 'SP-01b', 'Lateral exterior dreapta (scurtat: ocolește masca coloanei de scurgere)', 'ALB18', 2460, 405, 1, ('2', '-', '0.8', '-'), 'W1 = sus; începe la 245 mm de peretele din spate (masca fonică Ø110)', 'Lateral_dreapta')
add(M, 'SP-02', 'Separator (dublu: corp mașină + coloană)', 'ALB18', 2442, 650, 2, ('2', '-', '-', '-'),
    'modelul are un singur separator, dar golurile (664 + 264) cer două; sub capacul de sus', 'Separator_lateral')
add(M, 'SP-03', 'Capac sus', 'ALB18', 964, 650, 1, ('2', '-', '-', '-'), 'cu decupaj în colț 220 × 245 mm pentru coloana de scurgere (piesă în L, trecută ca dreptunghi întreg)', 'Capac_sus')
add(M, 'SP-04', 'Bază corp superior', 'ALB18', 664, 650, 1, ('2', '-', '-', '-'), 'deasupra nișei de detergenți', 'Baza_corp_superior')
add(M, 'SP-05', 'Poliță corp superior', 'ALB18', 664, 616, 3, ('2', '-', '-', '-'), '', 'Polita_superioara')
add(M, 'SP-06', 'Spate corp superior (încastrat)', 'ALB16', 1014, 664, 1, note='PAL 16 alb în loc de 8 mm (se vede în nișa de detergenți)', src='Spate_corp_superior')
add(M, 'SP-07', 'Ușă depozitare sus', 'CAS18', 647, 328, 2, FRONT, 'aplicată în gol', 'Usa_depozitare_sus_1/2')
add(M, 'SP-08', 'Front sertar coșuri', 'CAS18', 658, 380, 1, FRONT, '', 'Front_sertar_cosuri')
sertar_movento(M, 'SP-SC', 664, 500, 100, 1, 'sertar jos pentru cele 2 coșuri detașabile')
add(M, 'SP-09', 'Poliță extractibilă (coș încărcare)', 'ALB18', 600, 530, 1, ('2', '-', '-', '-'), 'pe glisiere MOVENTO cu blocare', 'Polita_cos_incarcare')
add(M, 'SP-10', 'Front poliță extractibilă', 'CAS18', 540, 60, 1, FRONT, '60 mm în loc de 30 (cantul nu se aplică pe fâșii sub 60 mm)', 'Front_polita')
add(M, 'SP-11', 'Bază coloană laterală', 'ALB18', 382, 264, 1, ('2', '-', '-', '-'), '', 'Baza_laterala')
add(M, 'SP-12', 'Raft coloană laterală', 'ALB18', 382, 264, 5, ('2', '-', '-', '-'), 'scurtat de la 624 la 382 mm: colțul din spate e ocupat de coloana de scurgere izolată fonic', 'Raft_lateral')
add(M, 'SP-13', 'Ușă tehnică laterală', 'CAS18', 660, 258, 1, FRONT, 'acces robinet / priză', 'Usa_tehnica_laterala')
add(M, 'SP-14', 'Ușă accesorii laterală', 'CAS18', 1657, 258, 1, FRONT, '', 'Usa_accesorii_laterala')
add(M, 'SP-15', 'Mască tavan', 'CAS18', 1000, 60, 1, ('2', '-', '-', '-'), 'se ajustează pe tavan', 'Masca_tavan')

# =====================================================================  DULAP WC (baie.FCStd)
M = 'Dulap WC'
add(M, 'DW-01', 'Lateral', 'ALB18', 800, 250, 2, ('2', '-', '0.8', '0.8'), '', 'Dulap_WC_lateral_*')
add(M, 'DW-02', 'Bază / blat / poliță', 'ALB18', 614, 234, 3, ('2', '-', '-', '-'), 'jos, mijloc, sus', 'Dulap_WC_polita*')
add(M, 'DW-03', 'Spate (încastrat)', 'ALB16', 764, 614, 1, note='PAL 16 în loc de HDF/8 mm: rezistă mai bine la umezeala din baie', src='Dulap_WC_spate')
add(M, 'DW-04', 'Ușă', 'CAS18', 796, 321, 2, FRONT, '', 'Dulap_WC_usa*')

# =====================================================================  NOPTIERE (noptiera.FCStd) – tot cashmere
# 06.10.2026: noptiera de sud e ascunsă în FreeCAD (Codex: corp îngust în spatele patului); rămâne doar cea de nord
NOPT = 1
M = 'Noptieră' if NOPT == 1 else 'Noptiere (×%d)' % NOPT
add(M, 'N-01', 'Lateral corp', 'CAS18', 382, 355, 2 * NOPT, ('2', '2', '2', '-'), 'L1 sus, L2 jos, W1 față; vizibil din exterior', 'Noptiera_*_Corp')
add(M, 'N-02', 'Blat corp / bază', 'CAS18', 464, 382, 2 * NOPT, ('2', '-', '-', '-'), 'între laterale', 'Noptiera_*_Corp')
add(M, 'N-03', 'Spate', 'HDF3', 496, 351, NOPT, src='Noptiera_*_Corp')
add(M, 'N-04', 'Front sertar jos', 'CAS18', 497, 174, NOPT, FRONT, '', 'Noptiera_*_Front_sertar_jos')
add(M, 'N-05', 'Front sertar sus', 'CAS18', 497, 173, NOPT, FRONT, '', 'Noptiera_*_Front_sertar_sus')
sertar_movento(M, 'N-S', 464, 350, 120, 2 * NOPT, '2 sertare, MOVENTO 760H3500S')
add(M, 'N-06', 'Suport blat: sus / jos', 'CAS18', 260, 120, 2 * NOPT, ('-', '-', '2', '-'), 'cutie 120 × 120 × 260', 'Noptiera_*_Suport_blat')
add(M, 'N-07', 'Suport blat: lateral', 'CAS18', 260, 84, 2 * NOPT, ('-', '-', '2', '-'), '', 'Noptiera_*_Suport_blat')
add(M, 'N-08', 'Suport blat: capac față', 'CAS18', 84, 84, NOPT, note='încastrat, fără cant', src='Noptiera_*_Suport_blat')
add(M, 'N-09', 'Blat plutitor (2 straturi lipite)', 'CAS18', 500, 420, 2 * NOPT, ('42', '-', '42', '42'),
    '2 × 18 = 36 mm, cant 42 × 2 pe față și laterale (serviciu „dublare”)', 'Noptiera_*_Blat_plutitor')

# =====================================================================  DULAP DORMITOR (dulap_dormitor.FCStd, Codex, 06.10.2026)
# carcasă 2200 × 600 × 2360, 4 module de 527,5 mm, 4 uși de 546 × 2276, 8 sertare interioare (fronturi albe),
# culorile din model: carcasă și uși alb cald → alb 8685; soclul negru e profil cumpărat; organizatoarele de sertar și
# suporturile de pantaloni sunt accesorii cumpărate.
M = 'Dulap dormitor'
add(M, 'DD-01', 'Bază / capac', 'ALB18', 2200, 578, 2, ('2', '-', '-', '-'), 'pe soclu de 80 mm (profil negru cumpărat)', 'Baza, Capac')
add(M, 'DD-02', 'Lateral / despărțitor', 'ALB18', 2244, 578, 5, ('2', '-', '-', '-'), 'între bază și capac; module de 527,5 mm', 'Panou_0..4')
add(M, 'DD-03', 'Spate HDF (modul de capăt)', 'HDF3', 2262, 554.5, 2, note='4 bucăți, îmbinate pe axele despărțitorilor (încap pe 6 plăci HDF în loc de 7); decupaj priză sus-dreapta', src='Spate')
add(M, 'DD-03b', 'Spate HDF (modul din mijloc)', 'HDF3', 2262, 545.5, 2, note='în model 8 mm, dintr-o bucată', src='Spate')
add(M, 'DD-04', 'Raft fix depozitare sezonieră', 'ALB18', 535, 527.5, 4, ('-', '-', '2', '-'), 'W1 = față (527,5)', 'Depozitare_sezoniera')
add(M, 'DD-05', 'Raft reglabil', 'ALB18', 525.5, 515, 10, ('2', '-', '-', '-'), 'pe pini Ø5; L1 = față', 'Raft_reglabil_tricouri')
add(M, 'DD-06', 'Raft inferior pentru cutii', 'ALB18', 527.5, 520, 2, ('2', '-', '-', '-'), '', 'Raft_inferior')
add(M, 'DD-07', 'Ușă', 'ALB18', 2276, 546, 4, FRONT, '5 balamale / ușă; mâner negru aplicat', 'Usa 1..4')
for nm, h, hb in (('pijamale', 188, 180), ('șosete', 168, 160), ('lenjerie', 168, 160), ('ceasuri', 103, 95)):
    add(M, 'DD-F%d' % h if nm != 'lenjerie' else 'DD-F%dL' % h, 'Front sertar interior – %s' % nm, 'ALB18', 521.5, h, 2, FRONT,
        'PROVIZORIU: în model fronturile de 188 și 168 (lenjerie) ating balamalele de jos; lățimea finală după feronerie / distanțiere; modulele de capăt', 'Sertar ' + nm)
# cutiile sertarelor: în model 495,5 × 480, „feronerie de dimensionat” (16 mm pe fiecare parte până la laterale) →
# PROVIZORIU, cu cotele modelului: cutie din PAL 18 mm, laterale 450 (glisieră 450), fund de 18 între laterale, față/spate
# pe fund. Se recalculează după glisiera aleasă (la glisiere cu bile 12,7 mm/parte: cutia 502, față/spate 466).
# Verificat: și cu 466 sau cu distanțiere de 18–25 mm tot 17 plăci albe ies.
for nm, hb in (('pijamale', 180), ('șosete și lenjerie', 160), ('ceasuri', 95)):
    n_ = 4 if 'lenjerie' in nm else 2
    add(M, 'DD-S%d.L' % hb, 'Lateral cutie sertar – %s' % nm, 'ALB18', 450, hb, 2 * n_, ('0.8', '-', '-', '-'), 'PROVIZORIU (feronerie de ales); L1 = sus; glisieră 450 mm', 'sertar extractibil')
    add(M, 'DD-S%d.FS' % hb, 'Față interioară + spate – %s' % nm, 'ALB18', 459.5, hb - 18, 2 * n_, ('0.8', '-', '-', '-'), 'PROVIZORIU; pe fund', 'sertar extractibil')
    add(M, 'DD-S%d.F' % hb, 'Fund cutie sertar – %s' % nm, 'ALB18', 459.5, 450, n_, note='PROVIZORIU; între laterale', src='sertar extractibil')

# =====================================================================  CORP ÎNGUST ÎN SPATELE PATULUI (corp_spate_pat.FCStd, Codex)
M = 'Corp spate pat'
add(M, 'CP-01', 'Blat stejar', 'STJ18', 1600, 130, 1, ('2', '-', '2', '2'), 'în model 20 mm; fibra pe lungime', 'Blat_stejar')
add(M, 'CP-02', 'Lateral / reazem central', 'ALB18', 1100, 112, 3, ('2', '-', '-', '-'), 'L1 = față', 'Laterala_1/2, Reazem_central')
add(M, 'CP-03', 'Spate', 'HDF3', 1564, 1100, 1, note='în model 8 mm', src='Panou_spate')

# =====================================================================  COMODĂ TV CAMERA DE ZI (perete_TV.FCStd)
M = 'Comodă TV cameră de zi'
add(M, 'CTV-01', 'Lateral', 'CAS18', 382, 380, 2, ('-', '2', '2', '-'), 'L2 jos, W1 față (suspendată, se vede de jos)', 'Comoda_corp')
add(M, 'CTV-02', 'Bază', 'CAS18', 2364, 382, 1, ('2', '-', '-', '-'), 'se vede de jos', 'Comoda_corp')
add(M, 'CTV-03', 'Blat corp (ascuns sub blatul de stejar)', 'ALB18', 2364, 382, 1, ('-', '-', '-', '-'), 'nu se vede: alb, fără cant', 'Comoda_corp')
add(M, 'CTV-04', 'Despărțitor', 'ALB18', 344, 380, 2, ('-', '-', '2', '-'), 'W1 față', 'Comoda_corp')
add(M, 'CTV-05', 'Spate', 'HDF3', 2396, 376, 1, note='+ 2 șine de suspendare', src='Comoda_corp')
add(M, 'CTV-06', 'Ușă', 'CAS18', 797, 376, 3, FRONT, 'TIP-ON', 'Comoda_front_1..3')
add(M, 'CTV-07', 'Blat stejar (2 straturi lipite)', 'STJ18', 2400, 400, 2, ('42', '-', '42', '42'),
    '2 × 18 = 36 mm (modelul are 25), cant 42 × 2 pe față și capete', 'Comoda_blat_stejar')

# =====================================================================  COMODĂ TV DORMITOR (perete_TV_dormitor.FCStd) – stejar
M = 'Comodă TV dormitor'
add(M, 'CTD-01', 'Blat / bază', 'STJ18', 1700, 320, 2, ('2', '-', '2', '2'), 'peste laterale; fibra pe lungime', 'Comoda_TV_corp')
add(M, 'CTD-02', 'Lateral', 'STJ18', 244, 320, 2, ('2', '-', '-', '-'), 'între blat și bază; L1 = față', 'Comoda_TV_corp')
add(M, 'CTD-03', 'Despărțitor', 'ALB18', 317, 244, 1, ('-', '-', '2', '-'), '', 'Comoda_TV_corp')
add(M, 'CTD-04', 'Spate', 'HDF3', 1696, 276, 1, src='Comoda_TV_corp')
add(M, 'CTD-05', 'Front sertar', 'STJ18', 847, 276, 2, FRONT, 'fibra orizontală, continuă pe cele 2 fronturi', 'Comoda_TV_front_1/2')
sertar_movento(M, 'CTD-S', 823, 300, 180, 2, 'MOVENTO 760H3000S (adâncime 320)')

# =====================================================================  MACHIAJ (perete_TV_dormitor.FCStd) – stejar
M = 'Machiaj'   # 06.10: blat scurtat de la 800 la 630 mm (lasă loc draperiei din fața radiatorului); oglinda rămâne 800
add(M, 'MJ-01', 'Blat / bază', 'STJ18', 630, 400, 2, ('2', '-', '2', '2'), 'peste laterale', 'Machiaj_corp')
add(M, 'MJ-02', 'Lateral', 'STJ18', 114, 400, 2, ('2', '-', '-', '-'), '', 'Machiaj_corp')
add(M, 'MJ-03', 'Despărțitor', 'ALB18', 397, 114, 1, ('-', '-', '2', '-'), '', 'Machiaj_corp')
add(M, 'MJ-04', 'Spate (încastrat)', 'ALB16', 594, 114, 1, note='PAL 16 între blat, bază și laterale; HDF-ul ar cere o placă în plus', src='Machiaj_corp')
add(M, 'MJ-05', 'Front sertar', 'STJ18', 311, 146, 2, FRONT, '', 'Machiaj_front_1/2')
sertar_movento(M, 'MJ-S', 287, 350, 90, 2, 'MOVENTO 760H3500S')

# =====================================================================  DEBARA (debara.FCStd) – 4 niveluri
M = 'Debara'
add(M, 'DB-01', 'Raft geam (trapez 1050,6 / 960,3 × 350)', 'ALB18', 1051, 350, 4, ('2', '-', '-', '-'),
    'capătul dinspre perete tăiat oblic (90 mm); L1 = față', 'Raft_2..5', 'oblic')
add(M, 'DB-02', 'Raft perete bucătărie (850 / 500 × 250, capăt teșit)', 'ALB18', 850, 250, 4, ('2', '-', '-', '-'),
    'teșit pe ultimii 350 mm de la 250 la 0; cant și pe oblic', 'Raft_2..5', 'oblic')
add(M, 'DB-03', 'Raft dreapta intrării – pereche (2 trapeze 1245 × 542,5 / 221,4)', 'ALB18', 1245, 769, 2, ('-', '-', '2', '2'),
    'din fiecare dreptunghi ies 2 rafturi printr-o tăietură oblică; cant pe oblic și pe capătul de 542,5', 'Raft_sud_2..5', 'trapez')

# =====================================================================  BUCĂTĂRIE (bucatarie.FCStd)
M = 'Bucătărie'
def corp_jos(cod, W, nume, raft=True, spate=True):
    add(M, cod + '.L', 'Lateral corp jos %s' % nume, 'ALB18', 720, 557, 2, ('2', '-', '-', '-'), 'L1 = față; pe picioare 150', cod)
    add(M, cod + '.B', 'Bază corp jos %s' % nume, 'ALB18', W - 36, 557, 1, ('2', '-', '-', '-'), '', cod)
    add(M, cod + '.T', 'Traversă sus %s' % nume, 'ALB18', W - 36, 100, 2, ('2', '-', '-', '-'), 'față + spate, sub blat', cod)
    if raft:
        add(M, cod + '.R', 'Raft %s' % nume, 'ALB18', W - 38, 520, 1, ('2', '-', '-', '-'), '', cod)
    if spate:
        add(M, cod + '.H', 'Spate %s' % nume, 'HDF3', W - 12, 708, 1, note='6 mm mai mic pe fiecare latură (prindere 12 mm pe cantul lateralelor)', src=cod)


def corp_sus(cod, W, H, nume, rafturi):
    add(M, cod + '.L', 'Lateral corp sus %s' % nume, 'ALB18', H, 329, 2, ('2', '-', '-', '0.8'), 'W2 = jos (se vede de dedesubt)', cod)
    add(M, cod + '.B', 'Bază / blat corp sus %s' % nume, 'ALB18', W - 36, 329, 2, ('2', '-', '-', '-'), '', cod)
    if rafturi:
        add(M, cod + '.R', 'Raft corp sus %s' % nume, 'ALB18', W - 38, 300, rafturi, ('2', '-', '-', '-'), '', cod)
    add(M, cod + '.H', 'Spate %s' % nume, 'HDF3', W - 12, H - 12, 1, src=cod)


corp_jos('BJ-M1', 600, 'M1 chiuvetă', raft=False, spate=False)
corp_jos('BJ-M3', 400, 'M3')
corp_jos('BJ-M4', 600, 'M4 plită (2 sertare)', raft=False)
sertar_movento(M, 'BJ-M4S', 564, 500, 180, 2, 'sub plită')
corp_jos('BJ-M5', 400, 'M5')
add(M, 'BJ-M6.L', 'Lateral coloană M6', 'ALB18', 2260, 557, 2, ('2', '-', '-', '-'), 'cuptor 855–1440, microunde 1455–1827', 'M6_coloana_corp')
add(M, 'BJ-M6.B', 'Bază / blat / polițe fixe coloană', 'ALB18', 564, 557, 5, ('2', '-', '-', '-'), 'jos, sub cuptor, sub microunde, peste microunde, sus', 'M6_coloana_corp')
add(M, 'BJ-M6.R', 'Raft mobil coloană (sus)', 'ALB18', 562, 520, 1, ('2', '-', '-', '-'), '', 'M6_coloana_corp')
add(M, 'BJ-M6.H', 'Spate coloană', 'HDF3', 2248, 588, 1, src='M6_coloana_corp')
sertar_movento(M, 'BJ-M6S', 564, 500, 250, 1, 'sertar mare sub cuptor (acces la priza cuptor/microunde)')
corp_sus('BJ-S1', 600, 960, 'S1 picurător', 0)
corp_sus('BJ-S2', 600, 960, 'S2', 2)
corp_sus('BJ-S3', 400, 960, 'S3', 2)
corp_sus('BJ-S4', 600, 760, 'S4 peste hotă', 1)
corp_sus('BJ-S5', 400, 960, 'S5', 2)
add(M, 'BJ-S4C', 'Cutie mascare tub hotă: lateral', 'ALB18', 724, 180, 2, ('-', '-', '-', '-'), 'în colțul din spate al S4; decupaj 70 × 150 în bază și blat S4', 'Cutie_mascare_tub_S4')
add(M, 'BJ-S4F', 'Cutie mascare tub hotă: față', 'ALB18', 724, 64, 1, note='fâșie fără cant', src='Cutie_mascare_tub_S4')
fr = [('M1 chiuvetă', 716, 597, 1), ('M2 mașină vase incorporabilă', 716, 597, 1), ('M3', 716, 397, 1), ('M5', 716, 397, 1),
      ('M4 sertare', 597, 357, 1), ('M4 sertare', 597, 356, 1), ('M6 sertar jos', 696, 597, 1), ('M6 ușă sus', 597, 573, 1),
      ('S1, S2', 956, 597, 2), ('S3, S5', 956, 397, 2), ('S4', 756, 597, 1)]
for i, (nm, a, b, n) in enumerate(fr):
    add(M, 'BJ-F%02d' % (i + 1), 'Front %s' % nm, 'CAS18', a, b, n, FRONT, 'mașina de vase incorporabilă primește front din același decor' if 'M2' in nm else '', nm)
add(M, 'BJ-P1', 'Panou capăt (lângă ușă)', 'CAS18', 720, 578, 1, ('2', '-', '-', '-'), 'L1 = față; în model „Filer_usa” 20 mm', 'Filer_usa')
add(M, 'BJ-P2', 'Soclu (2 bucăți)', 'CAS18', 1620, 150, 1, ('-', '0.8', '-', '-'), 'L2 = jos; se ajustează pe pardoseală; îmbinare la M3/M4', 'Soclu')
add(M, 'BJ-P3', 'Soclu (2 bucăți)', 'CAS18', 1600, 150, 1, ('-', '0.8', '-', '-'), '', 'Soclu')
add(M, 'BJ-P4', 'Soclu retur la capăt', 'CAS18', 490, 150, 1, ('-', '0.8', '-', '-'), '', 'Soclu')
add(M, 'BJ-P5', 'Mască tavan (2 bucăți)', 'CAS18', 1620, 110, 1, ('2', '-', '-', '-'), 'se taie 110, se ajustează pe tavan (87 în model)', 'Masca_tavan')
add(M, 'BJ-P6', 'Mască tavan (2 bucăți)', 'CAS18', 1600, 110, 1, ('2', '-', '-', '-'), '', 'Masca_tavan')
add(M, 'BJ-P7', 'Mască tavan retur la capăt', 'CAS18', 578, 110, 1, ('2', '-', '-', '-'), '', 'Masca_tavan')
add(M, 'BJ-BL', 'Blat de lucru', 'BLAT38', 2620, 600, 1, ('-', '-', '42', '-'),
    'din 1 blat 4100 × 600; W1 = capătul dinspre ușă; decupaj chiuvetă + plită după fișele producătorilor', 'Blat')

# ---------------------------------------------------------------------  verificări de bază
for p in P:
    big = max(p['L'], p['W'])
    if p['mat'] == 'BLAT38':
        assert p['L'] <= 4100 and p['W'] <= 600, p
    elif p['mat'] in ('STJ18',):
        assert p['L'] <= 2770 and p['W'] <= 2040, ('nu încape pe placă (fibra pe L)', p)
    else:
        assert big <= 2770 and min(p['L'], p['W']) <= 2040, ('nu încape pe placă', p)
    for k in ('L1', 'L2', 'W1', 'W2'):
        assert p[k] in ('-', '2', '0.8', '42'), p
    side = {'L1': p['W'], 'L2': p['W'], 'W1': p['L'], 'W2': p['L']}
    for k in ('L1', 'L2', 'W1', 'W2'):           # cantul de mașină cere piesa ≥ 60 mm pe direcția cealaltă
        if p[k] != '-' and side[k] < 60:
            raise ValueError('cant pe fâșie sub 60 mm: %s %s' % (p['cod'], k))

out = dict(revizie='R03', data='06.10.2026', materiale=MAT, piese=P)
(ROOT / 'tmp/lista_debitare_R03.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
with open(ROOT / 'tmp/lista_debitare_R03.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['Mobilier', 'Cod', 'Denumire', 'Material', 'L', 'W', 'Buc', 'L1', 'L2', 'W1', 'W2', 'Fibră', 'Formă', 'Observații'])
    for p in P:
        w.writerow([p['mob'], p['cod'], p['den'], p['mat'], p['L'], p['W'], p['n'], p['L1'], p['L2'], p['W1'], p['W2'], p['fibra'], p['forma'], p['note']])
tot = {}
for p in P:
    t = tot.setdefault(p['mat'], [0, 0.0])
    t[0] += p['n']
    t[1] += p['n'] * p['L'] * p['W'] / 1e6
print('PIESE', sum(p['n'] for p in P), 'rânduri', len(P))
for m, (n, a) in sorted(tot.items()):
    print('  %-7s %4d buc  %6.2f m2' % (m, n, a))
