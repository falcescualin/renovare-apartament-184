"""Extragerea pentru planul de mobilare R03 (06.10.2026): rulează extrage_mobilier_plan.py nemodificat, cu dormitorul refăcut de Codex:
- dulapul nou (colecția Dulap_dormitor_custom) în locul dulapului existent, fără LED, senzori, cabluri și profile;
- corpul îngust din spatele patului (Corp_spate_pat_custom) ca piesă nouă CP; tabloul nu apare pe plan;
- patul: conturul cadrului HALD, fără pilotă, pled și perne (care ies peste cadru);
- piesele ascunse la randare din Mobilier și Noptiera_sud (patul vechi, dulapul existent, noptiera de sud) nu mai intră.
Scrie tmp/mobilier_plan_R03.json; tmp/mobilier_plan.json rămâne neatins (îl folosesc și planurile electrice).
Rulează: blender --background apartament_184_randare.blend --python extrage_mobilier_plan_R03.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'extrage_mobilier_plan.py'), encoding='utf-8').read()
REP = [(r'tmp\mobilier_plan.json"', r'tmp\mobilier_plan_R03.json"'),
       ("    ('Mobilier', r'^Dulap_dormitor', 'DD', 'Dulap dormitor existent 220 × 60', 'inalt'),\n",
        "    ('Dulap_dormitor_custom', r'LED|Senzor|Sursa|Cablu|Canal|Distribuitor|Profil_aluminiu', None, None, None),\n"
        "    ('Dulap_dormitor_custom', r'.', 'DD', 'Dulap dormitor 220 × 60 (la comandă)', 'inalt'),\n"
        "    ('Corp_spate_pat_custom', r'.', 'CP', 'Corp îngust în spatele patului', 'jos'),\n"
        "    ('Tablou_pat_custom', r'.', None, None, None),\n"),
       ("    ('Mobilier', r'^Pat', 'PT', 'Pat 160 × 200 cu ladă', 'liber'),\n",
        "    ('Mobilier', r'^Pat_(perna|pilota|pled|saltea)', None, None, None),\n"
        "    ('Mobilier', r'^Pat', 'PT', 'Pat 160 × 200 cu ladă', 'liber'),\n"),
       ("        if o.type != 'MESH':\n            continue\n",
        "        if o.type != 'MESH' or (o.hide_render and col.name in ('Mobilier', 'Noptiera_sud')):\n            continue\n")]
for a, b in REP:
    assert src.count(a) == 1, a
    src = src.replace(a, b)
exec(compile(src, 'extrage_mobilier_plan.py', 'exec'), {'__name__': '__main__', '__file__': os.path.join(HERE, 'extrage_mobilier_plan.py')})
