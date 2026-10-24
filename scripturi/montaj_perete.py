"""Pagina „Prindere in perete”: desen de sectiune (colțar anti-rasturnare / suspendare cu sina) + tabel pe tip de perete + pasi."""
from reportlab.lib.colors import HexColor, white
INK = HexColor('#14323f'); TEAL = HexColor('#2f8f88'); MUT = HexColor('#6b7f87'); GRID = HexColor('#c9d6da')
WARN = HexColor('#fbeee9'); WARN_B = HexColor('#c0562c'); PALE = HexColor('#e7f3f1'); STEEL = HexColor('#8a9499')

WALLS = [
    ['Beton armat (planșeu, perete structural)', 'Diblu nylon Ø6 × 40 sau Ø8 × 60 (pentru încărcări mari); burghiu SDS Ø6 / Ø8, adâncime = lungimea dibluului + 10 mm', 'Cel mai sigur. Nu atinge armătura: dacă burghiul se oprește pe metal, mută gaura 20 mm.'],
    ['Cărămidă plină', 'Diblu Ø6 × 40 / Ø8 × 60; burghiu cu percuție slabă', 'Evită rostul de mortar: pune dibluul în cărămidă.'],
    ['Cărămidă cu goluri / blocuri ceramice', 'Diblu cu manșon lung Ø8 × 80 sau ancoră chimică; burghiu FĂRĂ percuție', 'Dibluul obișnuit nu ține în goluri. Se folosește manșon sau chimic.'],
    ['BCA (beton celular autoclavizat)', 'Diblu special pentru BCA (spirală, Ø8 × 60) sau ancoră chimică', 'Dibluul de nylon obișnuit nu se prinde în BCA.'],
    ['Gips-carton', 'Ancoră metalică cu expandare (tip Molly) Ø6; pentru greutăți mari, șurub în profilul metalic sau în placă de OSB 18 mm montată în spatele plăcii', 'Se fixează numai în profil sau în placă de consolidare. Singură, placa nu ține corpuri încărcate.'],
]
STEPS_ANTI = [
    'Așază corpul la locul final, nivelat, cu spatele la perete (cu 1–2 mm joc).',
    'Din interior, marchează pe perete centrul colțarului: la 45 mm de muchia de sus a corpului, pe axa găurii colțarului.',
    'Trage corpul 20 cm în față, verifică cu detectorul ca în perete să nu fie țevi sau cabluri (planul electric R11 și cel sanitar) și găurește Ø6 × 50.',
    'Pune dibluul (Ø6 × 40), apoi prinde colțarul de perete cu șurub 4 × 40.',
    'Împinge corpul la perete și fixează colțarul de placa de sus a corpului cu șurub 4 × 16 (din interior, în blatul corpului).',
    'Verifică: corpul nu se mai înclină când tragi de sertarul de sus.',
]
STEPS_HANG = [
    'Marchează cu nivela linia șinei de suspendare la înălțimea din plan (centrul șinei, cota de sub tavan din documentul corpului).',
    'Verifică cu detectorul traseele din perete, apoi găurește pentru șină: câte un diblu la maximum 300 mm, minimum 3 pe corp.',
    'Fixează șina cu șuruburi 5 × 60 cu cap plat și dibluri alese după tipul peretelui; verifică nivela șinei pe toată lungimea.',
    'Montează suporții de suspendare în colțurile de sus ale corpului (cu șuruburi 4 × 16, din interior) și agață corpul pe șină.',
    'Reglează în înălțime și adâncime din șuruburile suporților, apoi blochează cu șuruburile de siguranță.',
    'Corpurile alăturate se prind între ele cu șuruburi de îmbinare (după ce sunt nivelate) înainte de a pune fronturile.',
]


def hatch(P, PH, x, top, w, h, step=9):
    c = P.c
    c.setStrokeColor(STEEL); c.setLineWidth(.4)
    P.rect(x, top, w, h, fill=HexColor('#e8ecee'), stroke=INK, lw=1)
    c.saveState(); p = c.beginPath(); p.rect(x, PH - top - h, w, h); c.clipPath(p, stroke=0, fill=0)
    xx = x - h
    while xx < x + w:
        c.line(xx, PH - top - h, xx + h, PH - top); xx += step
    c.restoreState()


def draw_anti(P, st, PH, x, top, w, h, wall):
    """sectiune laterala: perete (stanga), spate HDF, blat corp, colțar L."""
    c = P.c
    P.rect(x, top, w, h, stroke=GRID, lw=.6, r=4)
    P.text('SECȚIUNE VERTICALĂ (privit din lateral)', x + 14, top + 12, 'SegB', 10, TEAL)
    ox = x + 70; base = top + h - 70
    # perete
    hatch(P, PH, ox - 56, top + 36, 56, h - 36 - 70)
    P.text('PERETE', ox - 28, top + 50, 'SegB', 8, INK, 'c')
    # podea
    P.rect(ox - 56, base, w - 20, 8, fill=HexColor('#d6c6a8'), stroke=INK, lw=.8)
    uh = 220                       # inaltimea corpului in desen
    ud = 260                       # adancimea
    # spate HDF
    P.rect(ox + 1, base - uh, 5, uh, fill=HexColor('#d8d8d0'), stroke=INK, lw=.8)
    P.text('spate HDF 3 mm', ox + 10, base - uh + 4, 'Seg', 7.5, MUT)
    # blat corp (placa de sus) si baza
    P.rect(ox + 6, base - uh, ud, 18, fill=HexColor('#c9c5bd'), stroke=INK, lw=.9)
    P.rect(ox + 6, base - 18, ud, 18, fill=HexColor('#c9c5bd'), stroke=INK, lw=.9)
    P.text('placa de sus a corpului (18 mm)', ox + 70, base - uh - 12, 'Seg', 8, INK)
    # lateral (linie)
    P.rect(ox + 6, base - uh + 18, ud, 3, fill=HexColor('#e1ddd5'), stroke=None)
    # colțar L: orizontal sub placa de sus, vertical spre perete
    cx = ox - 1
    P.rect(cx - 8, base - uh + 18, 54, 6, fill=STEEL, stroke=INK, lw=.7)       # ramura orizontala sub placa
    P.rect(cx - 8, base - uh + 18, 6, 52, fill=STEEL, stroke=INK, lw=.7)       # ramura verticala spre perete (in fata peretelui)
    # decupaj in spate
    c.setStrokeColor(WARN_B); c.setLineWidth(1.2); c.setDash(3, 2)
    c.rect(ox - 3, PH - (base - uh + 70), 12, 52, stroke=1, fill=0); c.setDash()
    # diblu + surub in perete
    P.rect(cx - 46, base - uh + 36, 38, 4, fill=HexColor('#e9c46a'), stroke=INK, lw=.6)
    P.text('diblu Ø6 × 40 + șurub 4 × 40', cx + 56, base - uh + 52, 'Seg', 8, INK)
    # surub in placa de sus
    P.rect(cx + 26, base - uh + 12, 4, 18, fill=HexColor('#e9c46a'), stroke=INK, lw=.6)
    P.text('șurub 4 × 16 în placa de sus', cx + 40, base - uh - 40, 'Seg', 8, INK)
    # cote
    c.setStrokeColor(MUT); c.setLineWidth(.5)
    xx = ox + ud + 40
    c.line(xx, PH - (base - uh), xx, PH - base); c.line(xx - 4, PH - (base - uh), xx + 4, PH - (base - uh)); c.line(xx - 4, PH - base, xx + 4, PH - base)
    P.text('%g mm' % wall['unit_h'], xx + 8, base - uh / 2 - 4, 'SegB', 8.5, INK)
    P.para('<b>Decupajul din spate</b> (linie punctată): taie în HDF un dreptunghi de 45 × 20 mm în dreptul colțarului, ca să treacă ramura spre perete.', x + 14, top + h - 56, w - 28, st(8.5, MUT))


def draw_hang(P, st, PH, x, top, w, h, wall):
    c = P.c
    P.rect(x, top, w, h, stroke=GRID, lw=.6, r=4)
    P.text('SECȚIUNE VERTICALĂ: SUSPENDARE PE ȘINĂ', x + 14, top + 12, 'SegB', 10, TEAL)
    ox = x + 70; base = top + h - 40
    hatch(P, PH, ox - 56, top + 36, 56, h - 36 - 40)
    P.text('PERETE', ox - 28, top + 50, 'SegB', 8, INK, 'c')
    uh = 250; ud = 140
    # sina
    P.rect(ox, top + 90, 8, 50, fill=STEEL, stroke=INK, lw=.8)
    P.text('șină de suspendare', ox + 14, top + 100, 'Seg', 8, INK)
    for yy in (98, 130):
        P.rect(ox - 30, top + yy, 38, 4, fill=HexColor('#e9c46a'), stroke=INK, lw=.6)
    P.text('șurub 5 × 60 + diblu, la ≤ 300 mm', ox - 56, top + 150, 'Seg', 8, INK)
    # corp
    P.rect(ox + 8, top + 80, ud, 18, fill=HexColor('#c9c5bd'), stroke=INK, lw=.9)
    P.rect(ox + 8, top + 80 + uh - 18, ud, 18, fill=HexColor('#c9c5bd'), stroke=INK, lw=.9)
    P.rect(ox + 8, top + 80, 4, uh, fill=HexColor('#d8d8d0'), stroke=INK, lw=.7)
    # suport de suspendare
    P.rect(ox + 12, top + 98, 40, 12, fill=HexColor('#7a8a94'), stroke=INK, lw=.8)
    P.text('suport de suspendare reglabil', ox + 60, top + 106, 'Seg', 8, INK)
    P.text('placa de sus a corpului', ox + 40, top + 66, 'Seg', 8, INK)
    P.para('Fiecare corp suspendat are minimum 2 suporți, câte unul în fiecare colț de sus. Greutatea corpului încărcat se împarte pe șină, nu pe un singur șurub.', x + 14, top + h - 36, w - 28, st(8.5, MUT))


STEPS_BACK = [
    'Marchează cu nivela linia de jos a corpului pe perete, la cota din plan.',
    'Ține corpul pe linie (sau pe un suport provizoriu) și marchează prin spate cele 4 găuri (la 60–80 mm de colțuri).',
    'Ia corpul jos, verifică cu detectorul traseele din perete (planul electric R11 și cel sanitar) și găurește după tipul peretelui (tabelul de mai jos).',
    'Pune dibluurile și prinde corpul cu șuruburi 4 × 40 prin spatele de 16 mm, cu șaibă; strânge întâi cele de sus, verifică nivela, apoi cele de jos.',
    'Verifică: corpul nu se mișcă la tragere în jos și în față.',
]


def draw_back(P, st, PH, x, top, w, h, wall):
    P.rect(x, top, w, h, stroke=GRID, lw=.6, r=4)
    P.text('SECȚIUNE VERTICALĂ: PRINDERE PRIN SPATE', x + 14, top + 12, 'SegB', 10, TEAL)
    ox = x + 90
    hatch(P, PH, ox - 56, top + 36, 56, h - 76)
    P.text('PERETE', ox - 28, top + 50, 'SegB', 8, INK, 'c')
    uh, ud = 250, 160
    t0 = top + 70
    P.rect(ox, t0, 12, uh, fill=HexColor('#d8d8d0'), stroke=INK, lw=.8)
    P.text('spate PAL 16 mm', ox + 18, t0 + uh / 2, 'Seg', 8, INK)
    P.rect(ox, t0, ud, 14, fill=HexColor('#c9c5bd'), stroke=INK, lw=.9)
    P.rect(ox, t0 + uh - 14, ud, 14, fill=HexColor('#c9c5bd'), stroke=INK, lw=.9)
    for yy in (t0 + 40, t0 + uh - 40):
        P.rect(ox - 40, yy - 3, 40, 6, fill=HexColor('#e9c46a'), stroke=INK, lw=.6)
        P.rect(ox + 12, yy - 5, 6, 10, fill=STEEL, stroke=INK, lw=.6)
    P.text('diblu + șurub 4 × 40 cu șaibă', ox + 26, t0 + 34, 'Seg', 8, INK)
    P.para('Corpul mic stă direct pe perete, prins prin spatele de 16 mm în 4 puncte. Pentru un spate HDF de 3 mm nu se folosește această prindere.', x + 14, top + h - 40, w - 28, st(8.5, MUT))


def wall_page(P, st, PH, S):
    w = getattr(S, 'wall', None)
    if not w: return
    P.page('Prindere în perete', S.title)
    if w['kind'] == 'antirasturnare':
        draw_anti(P, st, PH, 40, 80, 520, 420, w); steps = STEPS_ANTI
    elif w['kind'] == 'prin_spate':
        draw_back(P, st, PH, 40, 80, 520, 420, w); steps = STEPS_BACK
    else:
        draw_hang(P, st, PH, 40, 80, 520, 420, w); steps = STEPS_HANG
    steps = w.get('steps', steps)
    P.text('PAȘI', 600, 84, 'SegB', 12, TEAL)
    top = 108
    for i, t in enumerate(steps, 1):
        h = P.para('<b>%d.</b> %s' % (i, t), 600, top, 550, st(10.5)); top += h + 6
    P.text('ALEGE FIXAREA DUPĂ TIPUL PERETELUI', 600, top + 12, 'SegB', 12, TEAL)
    P.table(['Perete', 'Fixare', 'Observație'], WALLS, 600, top + 36, [140, 230, 180], 8.5, pad=3)
    P.rect(40, 520, 520, 120, fill=WARN, stroke=WARN_B, r=6)
    P.para('<b>Înainte să găurești:</b> tipul peretelui din dormitor și din restul apartamentului nu e confirmat în model (decizia M2 din documentul electric). '
           'Pereții de 150 mm dintre camere pot fi din BCA sau gips-carton; verifică cu un burghiu de test într-un loc ascuns și alege diblul în consecință. '
           'Nu găuri în dreptul prizelor, întrerupătoarelor sau al traseelor din planul electric R11.', 54, 530, 496, st(10))
    if w.get('note'):
        P.para('<i>%s</i>' % w['note'], 40, 650, 520, st(9.5, MUT))
