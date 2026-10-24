"""Specificatii de montaj pe corp (R03): piese cu cutii 3D (mm, local; fata = +y), pasi, feronerie, imbinari.
Folosit de montaj_blender.py (imagini pas cu pas) si montaj_pdf.py (documentul PDF).
Codurile pieselor sunt cele din tmp/lista_debitare_R03.json (planul de debitare R03)."""
import math

# --------------------------------------------------------------------------------------------- generale
TOOLS = [
    ('Șurubelniță electrică + biți PZ2', 'pentru confirmate și șuruburi PAL'),
    ('Mașină de găurit cu burghie Ø5, Ø7, Ø8, Ø35 (Forstner)', 'șablon de găurire; opritor de adâncime'),
    ('Nivelă cu bulă (60 cm) și metru', 'verificare plan, vertical, diagonale'),
    ('Ciocan de cauciuc', 'pentru cepuri; nu se lovește direct în cant'),
    ('Șurubelniță dinamometrică sau cheie imbus 4 mm', 'reglarea balamalelor și picioarelor'),
    ('Clești de strângere (2–4 buc.) și colțare de ghidare', 'la lipirea și strângerea plăcilor'),
    ('Covor sau carton gros pe podea', 'plăcile cu cant se montează pe suprafață moale'),
    ('Aspirator mic și cârpă moale', 'praf de PAL la găurire, curățare finală'),
]
SAFETY = [
    'Se lucrează în doi la piesele mai mari de 1,2 m sau mai grele de 15 kg.',
    'Plăcile se pun pe covor sau carton, cu fața finită în jos, ca să nu zgârie cantul sau decorul.',
    'Nu se strâng confirmatele cu forță maximă: PAL-ul se sparge. Șurubelnița electrică se reglează pe cuplu mic.',
    'Corpurile înalte (peste 1,2 m) se fixează de perete cu colțarele anti-răsturnare înainte de a se încărca.',
    'Înainte de găurit în perete se verifică traseele electrice din planul electric R11 și de apă din planul sanitar.',
]
CONF_RULES = [
    'Confirmat Ø7 × 50: gaură pilot Ø5 × 55 în muchia plăcii și gaură de trecere Ø7 în fața plăcii vecine, la 9 mm de la marginea plăcii.',
    'Poziții: primul confirmat la 50 mm de capete, apoi distanțe de cel mult 250–300 mm între ele. Minimum 2 pe îmbinare.',
    'Lângă fiecare al doilea confirmat se pune un cep Ø8 × 35 pentru ghidare și ca să nu se rotească piesa.',
    'Se găuresc doar piesele din același corp, cu șablonul pus de aceeași parte (fața vizibilă în jos), ca să nu se oglindească pozițiile.',
    'Capacele de confirmat se pun la final, pe fețele vizibile.',
]


def joint_positions(L):
    n = max(2, math.ceil(L / 260.0))
    if L < 160:
        return [round(L * 0.25), round(L * 0.75)]
    return [round(50 + i * (L - 100) / (n - 1)) for i in range(n)]


# --------------------------------------------------------------------------------------------- util: piese
class Spec:
    def __init__(self, slug, mob, title, where, dims, desc):
        self.slug, self.mob, self.title, self.where, self.dims, self.desc = slug, mob, title, where, dims, desc
        self.parts, self.steps, self.hw, self.joints, self.pre, self.final, self.notes = [], [], [], [], [], [], []
        self.views = {}
        self.final_views = ['fata']
        self.gbox = None          # (x0, y0, x1, y1) global, mm, pentru harta de amplasare
        self.time = ''
        self.people = '1–2'
        self.blend = None         # .blend cu piese reale (optional)
        self.extra_final = []     # puncte suplimentare de verificare
        self.pre = []             # conditii inainte de montaj (perete, electric, podea)
        self.hwi = []             # feronerie 3D pozitionata: model, pozitie, axe, pasul, explodare
        self.skip_joints = []     # perechi de piese fara confirmate automate (ex. capac incastrat prins doar lateral)

    def part(self, pid, code, label, box, mat, step, role=None):
        if role is None:
            role = {'hw': 'hw', 'led': 'hw', 'metal': 'hw', 'hdf': 'back', 'top': 'glue', 'blat': 'glue', 'oglinda': 'door'}.get(mat, 'panel')
        self.parts.append(dict(id=pid, code=code, label=label, box=[round(float(v), 1) for v in box], mat=mat, step=step, role=role))

    def step(self, n, title, view, text, warn=(), check=(), hw='', frame='all', extra=None):
        ids = [p['id'] for p in self.parts if p['step'] == n]
        d = dict(n=n, title=title, view=view, text=list(text), warn=list(warn), check=list(check), hw=hw, parts=ids, frame=frame)
        d.update(extra or {})
        self.steps.append(d)

    def hw_at(self, step, model, at, az=(0, 0, 1), ax=None, mirror=False, attach=None, explode=0.0, letter=None, dash=True, tag=None):
        """o piesa de feronerie: modelul (id din feronerie_catalog, mm) are axa +Z pe 'az' si +X pe 'ax', originea in 'at';
        'attach' = piesa cu care se misca in vederea explodata; 'explode' = cat iese pe axa +Z in pasul in care e noua."""
        az = [float(v) for v in az]
        if ax is None:
            ax = [1.0, 0.0, 0.0] if abs(az[0]) < 0.9 else [0.0, 1.0, 0.0]
            d = sum(a * b for a, b in zip(ax, az)); ax = [a - d * b for a, b in zip(ax, az)]
        self.hwi.append(dict(step=step, model=model, at=[round(float(v), 2) for v in at], az=az, ax=[float(v) for v in ax], mirror=mirror,
                             attach=attach, explode=float(explode), letter=letter, dash=dash, tag=tag))

    def hardware(self, letter, name, qty, note='', steps='', model=None):
        self.hw.append(dict(letter=letter, name=name, qty=qty, note=note, steps=steps, model=model))

    def joint(self, step, name, a, b, L, kind='A'):
        self.joints.append(dict(step=step, name=name, a=a, b=b, L=L, kind=kind, pos=joint_positions(L)))

    def to_json(self):
        return dict(slug=self.slug, mob=self.mob, title=self.title, parts=self.parts, steps=self.steps, views=self.views, final_views=self.final_views, hwi=self.hwi)


def drawer(S, tag, code, x0, yf, zp, W, NL, H, step_box, step_rail, step_front, front_box, front_code, front_label, step_tob=None, rec=13.0,
           offs_r=None, offs_l=None, fs_t=18.0, side_r=None, side_l=None, codes=None, fu_t=16.0):
    """Sertar Blum MOVENTO 760H (+ TIP-ON BLUMOTION) cu cutie din PAL 16 mm, dupa catalogul Blum (2022/23 p. 437, 2024/25 p. 419 / 428):
    SKW = LW - 42 (latimea interioara a sertarului), SKL = NL - 10, laterale de 16 la 5 mm de lateralul corpului,
    fundul retras rec = 13 mm (12-15), fata de jos a fundului la 28,5 deasupra profilului glisierei, suruburile glisierei la 38 deasupra profilului.
    x0 = fata interioara a lateralului din dreapta, yf = muchia din fata a corpului (fata = +y), zp = baza profilului glisierei."""
    lw = W - 42
    ext = lw + 32
    xo = x0 + 5
    ln = NL - 10
    zs = zp + 28.5 - rec          # muchia de jos a lateralelor de sertar
    zb = zp + 28.5                # fata de jos a fundului
    base_offs = (37, 69, 261) if NL < 380 else (37, 261, 293)          # catalog Blum: NL 300-350 -> 37 / 261 (+69); NL 380-520 -> 37 / 261 / 293
    offs_r = offs_r or base_offs
    offs_l = offs_l or base_offs
    cL, cFS, cF = (codes['L'], codes['FS'], codes['F']) if codes else (code + '.L', code + '.FS', code + '.F')
    cFS2, cF2 = (codes.get('FS2', cFS), codes.get('F2', cF)) if codes else (cFS, cF)
    gm = 'glisiera_movento' if NL == 350 else 'glisiera_movento@%d' % NL
    S.part(f'{tag}.rl', 'SL', 'Glisieră MOVENTO dreapta', (x0, yf - NL - 1, zp, 3, NL - 1, 46), 'hw', step_rail)
    S.parts[-1].update(model=gm, zs=zp + 38.0, offs=list(offs_r), place=[x0, yf, zp], mirror=False, follow=side_r)
    S.part(f'{tag}.rr', 'SL', 'Glisieră MOVENTO stânga', (x0 + W - 3, yf - NL - 1, zp, 3, NL - 1, 46), 'hw', step_rail)
    S.parts[-1].update(model=gm, zs=zp + 38.0, offs=list(offs_l), place=[x0 + W, yf, zp], mirror=True, follow=side_l)
    S.part(f'{tag}.l1', cL, 'Lateral sertar dreapta', (xo, yf - ln, zs, 16, ln, H), 'sertar', step_box)
    S.parts[-1]['hook'] = [xo + 7, zs + 11]                  # gaura Ø6 x 10 pentru carligul din spate
    S.part(f'{tag}.l2', cL, 'Lateral sertar stânga', (xo + ext - 16, yf - ln, zs, 16, ln, H), 'sertar', step_box)
    S.parts[-1]['hook'] = [xo + ext - 7, zs + 11]
    S.part(f'{tag}.fu', cF2, 'Fund sertar', (xo + 16, yf - ln, zb, lw, ln, fu_t), 'sertar', step_box)
    S.part(f'{tag}.fa', cFS2, 'Față interioară sertar', (xo + 16, yf - fs_t, zb + fu_t, lw, fs_t, H - rec - fu_t), 'sertar', step_box)
    S.part(f'{tag}.sp', cFS2, 'Spate sertar', (xo + 16, yf - ln, zb + fu_t, lw, fs_t, H - rec - fu_t), 'sertar', step_box)
    if front_box:
        S.part(f'{tag}.fr', front_code, front_label, front_box, 'front', step_front, role='door')
    # cleme de cuplare sub fund, in coltul din fata (lipite de lateral si de fata sertarului)
    S.hw_at(step_box, 'cleme_movento', (xo + 16, yf, zb), attach=f'{tag}.fu', explode=-40, letter='P', tag=tag)
    S.hw_at(step_box, 'cleme_movento', (xo + ext - 16, yf, zb), mirror=True, attach=f'{tag}.fu', explode=-40, letter='P', tag=tag)
    for (xx, yy) in ((26.0, -36.0), (12.0, -46.0)):
        for sx, x_ in ((1, xo + 16), (-1, xo + ext - 16)):
            S.hw_at(step_box, 'surub_3_5x15', (x_ + sx * xx, yf + yy, zb - 5.0), az=(0, 0, -1), attach=f'{tag}.fu', explode=70, letter=getattr(S, 'rail_letter', 'D15'), tag=tag)
    L = W - 267 if W >= 294 else W - 241          # MD Blum TIP-ON BLUMOTION p. 3: MOVENTO LW - 267 (LW >= 294) / LW - 241 (LW <= 293)
    if step_tob:
        tm = 'tip_on' if NL == 350 else 'tip_on@%d' % NL
        S.hw_at(step_tob, tm, (x0, yf, zp), explode=-35, letter='G', tag=tag)
        S.hw_at(step_tob, tm, (x0 + W, yf, zp), mirror=True, explode=-35, letter='G', tag=tag)
        S.hw_at(step_tob, 'bara_sincronizare@%d' % L, (x0 + (W - L) / 2, yf - NL + 105.0, zp + 10.0), az=(0, 0, 1), ax=(1, 0, 0), explode=-60, letter='Q', tag=tag)
    return dict(zs=zs, zb=zb, ext=ext, xo=xo, ln=ln, lw=lw, rod=L, screw_z=zp + 38.0)
