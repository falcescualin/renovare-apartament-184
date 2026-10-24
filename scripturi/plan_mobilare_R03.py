"""Plan de mobilare R03 (06.10.2026): rulează plan_mobilare_pdf.py nemodificat, cu:
- decorurile Kronospan în locul celor Egger (8685 alb, 5981 Cashmere, 3025 Sonoma), prețurile din devizul R04;
- baia în microciment olive grey (holul și vestibulul rămân alb cald);
- dormitorul refăcut de Codex: dulap nou la comandă (DD), corp îngust cu tablou în spatele patului (CP), o singură noptieră;
  conturul pieselor vine din tmp/mobilier_plan_R03.json (extrage_mobilier_plan_R03.py), nu din tmp/mobilier_plan.json;
- randările noi (texturi Kronospan, baie și dormitor refăcute, expunere automată), de zi și de seară, plus D_04.
Rulează cu Python-ul care are reportlab. Iese: output/pdf/Apartament_184_Plan_mobilare_R03.pdf"""
import sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripturi'))
import plan_comun                                     # mobilierul pentru fundal și tabele: extragerea R03
plan_comun.HELPERS = plan_comun.HELPERS.replace("tmp/mobilier_plan.json", "tmp/mobilier_plan_R03.json")
plan_comun.MOBP = json.loads((ROOT / 'tmp/mobilier_plan_R03.json').read_text(encoding='utf-8'))['items']
assert 'mobilier_plan_R03' in plan_comun.HELPERS
src = (ROOT / 'scripturi/plan_mobilare_pdf.py').read_text(encoding='utf-8')
REP = [("'Apartament_184_Plan_mobilare_R02.pdf'", "'Apartament_184_Plan_mobilare_R03.pdf'"),
       ("'R02 | 05.10.2026 | PLAN DE MOBILARE", "'R03 | 06.10.2026 | PLAN DE MOBILARE"),
       ("c.setTitle('Apartament 184 - Plan de mobilare - R02')", "c.setTitle('Apartament 184 - Plan de mobilare - R03')"),
       ("'R02: refăcut din modelul 3D actual, cu produsele alese, prețurile celor mai bune oferte (deviz R03), pardoseli, praguri și randări'",
        "'R03: decoruri Kronospan, baie olive grey, dormitor refăcut (dulap nou, corp și tablou în spatele patului), deviz R04, randări de zi și de seară'"),
       ("corp U702 greige", "corp Kronospan 5981 Cashmere"), ("stejar H1145", "stejar Kronospan 3025 Sonoma"),
       ("fronturi U702", "fronturi 5981 Cashmere"), ("corp W1000", "corp alb 8685"), ("W1000 / U702", "alb 8685 / 5981 Cashmere"),
       ("Rafturi W1000", "Rafturi albe 8685"),
       ("'Microciment · cadă 150 × 70", "'Microciment olive grey · cadă 150 × 70"),
       ("['Microciment alb cald', 'hol, vestibul, baie'", "['Microciment: alb cald (hol, vestibul), olive grey (baie)', 'hol, vestibul, baie'"),
       ("('microciment', 'microciment alb cald')", "('microciment', 'microciment (alb cald; baia olive grey)')"),
       # dormitorul refăcut de Codex (06.10.2026)
       ("    'N2': dict(t='Ca N1, în oglindă; LED din priza P02', lot=True),\n", ""),
       ("    'DD': dict(t='Dulapul existent 220 × 60 se păstrează, rotit pe peretele de lângă ușă'),\n",
        "    'DD': dict(t='La comandă (model Codex): 220 × 60 × 236, alb 8685, 4 uși cu mâner negru, 8 sertare interioare, bare de umerașe, "
        "2 suporturi de pantaloni, LED pornit de senzorii de ușă; feroneria în M105', ids=['M105'], lot=True),\n"
        "    'CP': dict(t='La comandă: corp îngust 160 × 13 cm, înalt de 114 cm, în spatele patului, alb 8685 cu blat de stejar 3025; "
        "deasupra, tabloul 110 × 70 (rândul de mai jos)', lot=True),\n"),
       ("CUSTOM = {'DH', 'DR', 'MC', 'BJ', 'BS', 'DB', 'SP', 'CTV', 'CTD', 'N1', 'N2', 'MJ', 'DW', 'NS'}",
        "CUSTOM = {'DH', 'DR', 'MC', 'BJ', 'BS', 'DB', 'SP', 'CTV', 'CTD', 'N1', 'DD', 'CP', 'MJ', 'DW', 'NS'}"),
       ("EXIST, HEAT = {'DD'}, {'R1', 'R2', 'RP'}", "EXIST, HEAT = set(), {'R1', 'R2', 'RP'}"),
       ("ORDER = [('Dormitor', ['PT', 'N1', 'N2', 'DD', 'CTD', 'TV2', 'RF', 'MJ', 'PF', 'R1']),",
        "ORDER = [('Dormitor', ['PT', 'N1', 'CP', 'DD', 'CTD', 'TV2', 'RF', 'MJ', 'PF', 'R1']),"),
       ("'%d la comandă · %d cumpărate · %d existentă · %d radiatoare' % (n['custom'], n['buy'], n['exist'], n['heat'])",
        "'%d la comandă · %d cumpărate · %d radiatoare' % (n['custom'], n['buy'], n['heat'])"),
       ("('M03', 'Dormitor', 'Parchet stejar · pat centrat pe TV · dulapul existent rotit lângă ușă', [(0, 3700, -4000, 150)], ['PT', 'N1', 'N2', 'DD', 'CTD', 'TV2', 'RF', 'MJ', 'PF', 'R1'],\n"
        "     [('M100', 'Lenjerie, perne, pătură decorativă', None)]),",
        "('M03', 'Dormitor', 'Parchet stejar · pat centrat pe TV · dulap nou la comandă lângă ușă · corp îngust și tablou în spatele patului', [(0, 3700, -4000, 150)],\n"
        "     ['PT', 'N1', 'CP', 'DD', 'CTD', 'TV2', 'RF', 'MJ', 'PF', 'R1'],\n"
        "     [('M106', None, None), ('M100', 'Lenjerie, perne, pătură decorativă', None)]),"),
       ("găsite pe 05.10.2026 și linkul", "găsite pe 05–06.10.2026 și linkul"),
       ("['M10–M11', 'Randări de zi pe încăperi']", "['M10–M13', 'Randări de zi și de seară pe încăperi']"),
       # randări: D_04 nou și paginile de seară
       ("('D_01_pat_noptiere', 'Dormitor / pat și noptiere')", "('D_01_pat_noptiere', 'Dormitor / pat și noptieră')"),
       ("('D_03_zona_machiaj', 'Dormitor / zona de machiaj'), ", "('D_03_zona_machiaj', 'Dormitor / zona de machiaj'), ('D_04_dulap_tablou', 'Dormitor / dulap nou și tablou'), "),
       ("for pg, chunk in enumerate((REND[:9], REND[9:])):\n"
        "    start('M%d' % (10 + pg), 'Randări de zi' + (' (2)' if pg else ''), 'Cycles, lumină de zi; variantele de seară sunt în randari/noapte')\n",
        "for pg, (mode, chunk) in enumerate([(m_, ch) for m_ in ('zi', 'noapte') for ch in (REND[:9], REND[9:])]):\n"
        "    start('M%d' % (10 + pg), ('Randări de zi' if mode == 'zi' else 'Randări de seară') + (' (2)' if pg % 2 else ''),\n"
        "          'Cycles, lumină de zi prin ferestre' if mode == 'zi' else 'Cycles, seara: plafoniere și benzi LED aprinse, fără soare')\n"),
       ("c.drawImage(str(ROOT / 'randari/web/zi' / (f + '.jpg')), x, H - y - h_, w_, h_)",
        "c.drawImage(str(ROOT / 'randari/web' / mode / (f + '.jpg')), x, H - y - h_, w_, h_)")]
for a, b in REP:
    assert a in src, a
    src = src.replace(a, b)
exec(compile(src, 'plan_mobilare_pdf.py', 'exec'), {'__name__': '__main__', '__file__': str(ROOT / 'scripturi/plan_mobilare_pdf.py')})
