"""Specificatie de montaj R04: rafturile din debara (4 niveluri: raft L la geam + peretele bucatariei, pereche de trapeze in dreapta intrarii).
Contururile exacte vin din FreeCAD (tmp/debara_poligoane.json, citit din sesiunea GUI). Coordonate locale: x = gx - 9875 (peretele de vest la x = 0),
y = gy + 3465, z = cota de la pardoseala."""
import json
from pathlib import Path
from montaj_specs import Spec
import montaj_lib as L
from montaj_comun import B, finish

ROOT = Path(__file__).resolve().parents[1]
X0, Y0 = 9875.0, -3465.0
LEVELS = (700.0, 1100.0, 1500.0, 1900.0)


def _poly(S, pid, code, label, pts, z0, step, mat='corp'):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    S.part(pid, code, label, (min(xs), min(ys), z0, max(xs) - min(xs), max(ys) - min(ys), 18.0), mat, step, role='shelf')
    S.parts[-1]['poly'] = [list(p) for p in pts]
    return S.parts[-1]


def _bracket(S, step, at, room, a, letter='CO'):
    """consola L sub raft: o aripa pe perete (in jos), una sub raft (spre camera); 2 suruburi in perete cu diblu, 2 in raft"""
    ax = (room[1], -room[0], 0) if False else ((0, 1, 0) if room == (1, 0, 0) else (1, 0, 0) if room == (0, -1, 0) else (-1, 0, 0))
    az = (0, 0, -1)
    ay = room
    m = 'coltar_40@%d' % a
    S.hw_at(step, m, at, az=az, ax=ax, explode=0, letter=letter, dash=False, tag='consola')
    for h in (30.0, a - 30.0):
        pw = L._xf(at, ax, ay, az, (15.0, 3.0, h))
        S.hw_at(step, 'diblu_6x40', [pw[i] - ay[i] * 3.0 for i in range(3)], az=ay, explode=60, letter='T')
        S.hw_at(step, 'surub_4x40', pw, az=ay, explode=110, letter='U')
    for h in (30.0, a - 30.0):
        ps = L._xf(at, ax, ay, az, (15.0, h, 3.0))
        S.hw_at(step + 1, 'surub_4x16', ps, az=(0, 0, -1), explode=70, letter='I')


def debara():
    S = Spec('debara', 'Debara', 'Rafturi debara (4 niveluri)',
             'Debara de lângă bucătărie: raft în L la geam și pe peretele bucătăriei, pereche de rafturi trapez în dreapta intrării', (1051, 3215, 1918),
             'Rafturi din PAL alb 18 mm pe 4 niveluri (700, 1100, 1500, 1900 mm), pe console metalice prinse în perete, cu profil LED 24 V sub muchia din față.')
    P = json.loads((ROOT / 'tmp' / 'debara_poligoane.json').read_text(encoding='utf-8'))
    loc = lambda pts: [(round(x - X0, 1), round(y - Y0, 1)) for x, y in pts]
    lpoly = loc(P['Raft_2']['pts'])
    spoly = loc(P['Raft_sud_2']['pts'])
    # raftul L se taie din 2 piese: DB-01 (la geam, pe peretele de nord) si DB-02 (pe peretele bucatariei, cu capatul tesit)
    ymin_n = 2865.0
    nord = [(1050.6, 3215.0), (0.0, 3215.0), (0.0, ymin_n), (960.3, ymin_n)]
    vest = [(0.0, ymin_n), (0.0, 2015.0), (250.0, 2365.0), (250.0, ymin_n)]
    B(S, 'perete_v', 'PERETE', 'Peretele bucătăriei (vest)', -60, 0, -100, 3300, 0, 2400, 1, mat='perete', role='context')
    B(S, 'perete_n', 'PERETE', 'Peretele cu geam (nord)', -60, 1150, 3215, 3275, 0, 2400, 1, mat='perete', role='context')
    for i, z in enumerate(LEVELS, 1):
        _poly(S, 'n%d' % i, 'DB-01', 'Raft geam (nord) – nivelul %d' % i, nord, z, 3)
        _poly(S, 'v%d' % i, 'DB-02', 'Raft perete bucătărie – nivelul %d' % i, vest, z, 3)
        _poly(S, 's%d' % i, 'DB-03', 'Raft dreapta intrării – nivelul %d' % i, spoly, z, 3)
        B(S, 'ln%d' % i, 'LED', 'LED sub raftul de la geam', 250, 950, ymin_n + 8, ymin_n + 25, z - 8, z, 4, mat='led', role='hw')
        B(S, 'ls%d' % i, 'LED', 'LED sub raftul din dreapta intrării', 10, 533, 1228, 1245, z - 8, z, 4, mat='led', role='hw')
        _bracket(S, 2, (250.0, 3215.0, z), (0, -1, 0), 300)
        _bracket(S, 2, (850.0, 3215.0, z), (0, -1, 0), 300)
        _bracket(S, 2, (0.0, 2300.0, z), (1, 0, 0), 200)
        _bracket(S, 2, (0.0, 2700.0, z), (1, 0, 0), 200)
        _bracket(S, 2, (0.0, 200.0, z), (1, 0, 0), 400)
        _bracket(S, 2, (0.0, 1000.0, z), (1, 0, 0), 250)
    S.final_views = ['iso']
    S.views = {'iso': [1.0, -0.35, 0.75], 'nord': [0.6, -1.0, 0.6]}
    S.gbox = (9875, -3465, 10926, -250)
    S.time = '≈ 3 ore'
    S.people = '1 (2 la rafturile lungi)'
    S.wall = None
    S.pre = ['Pereții debaralei sunt vopsiți.', 'Alimentarea LED 24 V (sursa de sus, lângă tavan) e adusă.',
             'Tipul peretelui e verificat (pagina „Prindere în perete” de la celelalte corpuri): consolele țin rafturi încărcate.']
    S.step(1, 'Trasarea nivelurilor', 'iso',
           ['Cu nivela laser, trasează pe pereți liniile de sub rafturi: 700, 1100, 1500 și 1900 mm de la pardoseala finită.',
            'Marchează pozițiile consolelor: la geam la 250 și 850 mm de colț, pe peretele bucătăriei la 2300 și 2700 mm, în dreapta intrării la 200 și 1000 mm de capăt.',
            'Verifică cu detectorul traseele electrice și de apă înainte de găurit.'],
           extra={'explode': {}, 'frame': 'all'})
    S.step(2, 'Consolele pe perete', 'iso',
           ['Prinde fiecare consolă cu 2 dibluri Ø6 × 40 și șuruburi 4 × 40, cu aripa scurtă în sus, lipită de linie.',
            'Consolele de 400 mm vin sub capătul lat al rafturilor din dreapta intrării, cele de 300 sub raftul de la geam.'],
           warn=['Pune consolele la nivelă între ele: rafturile nu se reglează după montaj.'], extra={'explode': {}})
    S.step(3, 'Rafturile pe console', 'iso',
           ['Pune rafturile pe console: întâi raftul de la geam (DB-01), apoi cel de pe peretele bucătăriei (DB-02), cap la cap în colț.',
            'Rafturile din dreapta intrării (DB-03) se pun cu latura lungă la perete și capătul lat spre intrare.',
            'Prinde fiecare raft de console de dedesubt cu șuruburi 4 × 16.'],
           extra={'explode': {k: [0, 0, 120] for k in [p['id'] for p in S.parts if p['code'].startswith('DB')]}})
    S.step(4, 'Profilele LED', 'iso',
           ['Lipește profilele LED sub muchia din față a rafturilor și trece cablurile pe perete până la sursa de 24 V de sus.'],
           extra={'explode': {}})
    return finish(S, extra=[('K', 'Profil LED 24 V + bandă + cablu (4 niveluri)', '1 set', 'sub muchia din față', '4')],
                  notes=['Consolele sunt modelate ca L-uri de 200–400 mm; prețul din deviz (24 × suport raft) e pentru console simple.'])
