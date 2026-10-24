"""Extrage din scena de randare (apartament_184_randare.blend) amprentele în plan ale mobilierului, grupate ca pe un plan
de mobilare: contur (înfășurătoare convexă) în mm, în coordonatele FreeCAD (Y negativ în jos), cota de jos / sus și tipul.
Rulează: blender --background apartament_184_randare.blend --python extrage_mobilier_plan.py
Iese: tmp/mobilier_plan.json (citit de plan_mobilare_pdf.py și, ca fundal, de planurile electric / sanitar / termic)."""
import bpy, json, os, re, collections

OUT = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\tmp\mobilier_plan.json"

# (colecție, regex pe numele piesei, cod, denumire, tip) – prima regulă care se potrivește câștigă
# tip: jos = pe pardoseală până la ~1 m; inalt = corp până la tavan; sus = suspendat (linie întreruptă); perete = pe perete; liber = mobilier liber
RULES = [
    ('Dulap_hol_custom', r'LED|Senzor|Sursa', None, None, None),
    ('Dulap_hol_custom', r'.', 'DH', 'Dulap hol (uși oglindă)', 'inalt'),
    ('Bucatarie_custom', r'^TCL', 'FR', 'Frigider TCL side-by-side', 'liber'),
    ('Bucatarie_custom', r'^Masa', 'MS', 'Masă 80 × 60', 'liber'),
    ('Bucatarie_custom', r'^Scaun_1', 'SC1', 'Puf / scaun', 'liber'),
    ('Bucatarie_custom', r'^Scaun_2', 'SC2', 'Puf / scaun', 'liber'),
    ('Bucatarie_custom', r'^(S\d|Hota|Masca|Tub|Cutie|Gura)', 'BS', 'Corpuri sus + hotă', 'sus'),
    ('Bucatarie_custom', r'.', 'BJ', 'Bucătărie: corpuri jos, blat, coloană', 'jos'),
    ('Debara_custom', r'^Raft', 'DB', 'Rafturi debara', 'jos'),
    ('Debara_custom', r'.', None, None, None),
    ('Dressing_custom', r'LED|Senzor|Sursa', None, None, None),
    ('Dressing_custom', r'^Masa_calcat_planseta', 'MC', 'Masă de călcat deschisă (M3)', 'sus'),
    ('Dressing_custom', r'.', 'DR', 'Dressing (masă de călcat în M3)', 'inalt'),
    ('Spalatorie_vestibul_custom', r'.', 'SP', 'Corp spălătorie + mașina de spălat', 'inalt'),
    ('Baie_custom', r'^(Cada|Panou_cada|Sifon)', 'CD', 'Cadă 150 × 70', 'jos'),
    ('Baie_custom', r'^Masca_cada', 'NS', 'Mască cu nișe', 'inalt'),
    ('Baie_custom', r'^(Paravan|Profil_paravan|Balama_paravan|Garnitura)', 'PV', 'Paravan rabatabil', 'perete'),
    ('Baie_custom', r'^(Corp_lavoar|Lavoar|Baterie_lavoar)', 'LV', 'Lavoar 60 + mobilier', 'jos'),
    ('Baie_custom', r'^(Masca_WC|Trapa|Cadru_WC|Rezervor|Clapeta|WC_|Colac)', 'WC', 'WC suspendat + mască', 'jos'),
    ('Baie_custom', r'^Dulap_WC', 'DW', 'Dulap deasupra WC', 'sus'),
    ('Baie_custom', r'^Calorifer', 'RP', 'Calorifer port-prosop', 'perete'),
    ('Baie_custom', r'.', None, None, None),
    ('Noptiera_nord', r'LED', None, None, None),
    ('Noptiera_nord', r'.', 'N1', 'Noptieră', 'jos'),
    ('Noptiera_sud', r'LED', None, None, None),
    ('Noptiera_sud', r'.', 'N2', 'Noptieră', 'jos'),
    ('Perete_TV_custom', r'^Comoda', 'CTV', 'Comodă TV suspendată 240 × 40', 'sus'),
    ('Perete_TV_custom', r'.', None, None, None),
    ('Perete_TV_dormitor_custom', r'^Riflaje', 'RF', 'Riflaje stejar', 'perete'),
    ('Perete_TV_dormitor_custom', r'^Comoda_TV', 'CTD', 'Comodă TV dormitor 170 × 35', 'sus'),
    ('Perete_TV_dormitor_custom', r'^Machiaj_(corp|front)', 'MJ', 'Masă de machiaj + oglindă', 'sus'),
    ('Perete_TV_dormitor_custom', r'^Puf', 'PF', 'Puf bouclé', 'liber'),
    ('Perete_TV_dormitor_custom', r'.', None, None, None),
    ('Masuta_cafea_custom', r'travertin|mare', 'MT', 'Măsuță travertin 110 × 65', 'liber'),
    ('Masuta_cafea_custom', r'.', 'MM', 'Măsuță stejar Ø60', 'liber'),
    ('Mobilier', r'^Pat', 'PT', 'Pat 160 × 200 cu ladă', 'liber'),
    ('Mobilier', r'^Dulap_dormitor', 'DD', 'Dulap dormitor existent 220 × 60', 'inalt'),
    ('Mobilier', r'^Canapea', 'CN', 'Canapea extensibilă', 'liber'),
    ('Mobilier', r'^Masa', 'BR', 'Birou IKEA TROTTEN 120 × 70', 'liber'),
    ('Mobilier', r'^Uscator', 'US', 'Uscător de rufe pliabil', 'liber'),
    ('Mobilier', r'^Scaun', 'SB', 'Scaun de birou', 'liber'),
    ('Incalzire - radiatoare noi, pozitii pastrate', r'Dormitor', 'R1', 'Radiator R1', 'perete'),
    ('Incalzire - radiatoare noi, pozitii pastrate', r'.', 'R2', 'Radiator R2', 'perete'),
    ('TV sufragerie - TCL 55C6K Pro pe suport Nexio NX-LPA52-446', r'.', 'TV1', 'TV TCL 55C6K Pro', 'perete'),
    ('TV dormitor - TCL 55P8L pe suport Nexio NX-LPA52-446', r'.', 'TV2', 'TV TCL 55P8L', 'perete'),
]


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


# piese la care înfășurătoarea convexă ar umple golul (raftul în L al debaralei): se ia conturul real al feței de sus
OUTLINE = {'DB': r'^Raft(_sud)?_2$'}


def top_outline(o):
    """conturul feței de sus a piesei (poate fi neconvex), din triunghiurile orientate în sus de la cota maximă"""
    mw = o.matrix_world
    me = o.data
    zt = max((mw @ v.co).z for v in me.vertices)
    key = lambda v: (round(v.x * 1000, 1), round(v.y * 1000, 1))
    cnt = collections.Counter()
    for f in me.polygons:
        if (mw.to_3x3() @ f.normal).normalized().z > 0.9 and abs((mw @ f.center).z - zt) < 1e-4:
            ks = [key(mw @ me.vertices[i].co) for i in f.vertices]
            for a, b in zip(ks, ks[1:] + ks[:1]):
                if a != b:
                    cnt[tuple(sorted((a, b)))] += 1
    adj = collections.defaultdict(list)
    for (a, b), n in cnt.items():
        if n == 1:
            adj[a].append(b); adj[b].append(a)
    start = min(adj)
    loop, prev, cur = [start], None, start
    while True:
        nxt = [p for p in adj[cur] if p != prev]
        if not nxt or nxt[0] == start:
            break
        prev, cur = cur, nxt[0]
        loop.append(cur)
    # elimină punctele coliniare
    out = []
    for i, p in enumerate(loop):
        a, b = loop[i - 1], loop[(i + 1) % len(loop)]
        if abs((p[0] - a[0]) * (b[1] - a[1]) - (p[1] - a[1]) * (b[0] - a[0])) > 1.0:
            out.append([p[0], p[1]])
    return out


groups = {}
for col in bpy.data.collections:
    for o in col.objects:
        if o.type != 'MESH':
            continue
        short = o.name.split('__')[-1]
        for cname, rx, code, name, kind in RULES:
            if col.name == cname and re.search(rx, short):
                if code:
                    g = groups.setdefault(code, dict(code=code, name=name, kind=kind, comp=cname, parts=[], pts=[], z=[1e9, -1e9]))
                    g['parts'].append(short)
                    if code in OUTLINE and re.search(OUTLINE[code], short):
                        g.setdefault('polys', []).append(top_outline(o))
                    mw = o.matrix_world
                    for v in o.data.vertices:
                        w = mw @ v.co
                        g['pts'].append((round(w.x * 1000, 1), round(w.y * 1000, 1)))
                        g['z'][0] = min(g['z'][0], w.z * 1000); g['z'][1] = max(g['z'][1], w.z * 1000)
                break
items = []
for code, g in groups.items():
    hp = hull(g['pts'])
    xs, ys = [p[0] for p in hp], [p[1] for p in hp]
    it = dict(code=code, name=g['name'], kind=g['kind'], comp=g['comp'], parts=len(g['parts']), poly=[list(p) for p in hp],
              bbox=[min(xs), min(ys), round(g['z'][0]), max(xs), max(ys), round(g['z'][1])])
    if g.get('polys'):
        it['polys'] = g['polys']        # contur real, de desenat în locul înfășurătoarei
    items.append(it)
items.sort(key=lambda i: i['code'])
json.dump(dict(source='apartament_184_randare.blend', items=items), open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('MOBILIER', len(items), [i['code'] for i in items])
