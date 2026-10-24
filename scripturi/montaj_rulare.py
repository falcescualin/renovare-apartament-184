"""Genereaza spec.json, randarile Blender si PDF-ul de montaj pentru un corp.
  python montaj_rulare.py <corp> [spec|blender|panouri|pdf|all]      (corp = noptiera, dulap_wc, ... ; vezi REG)
Randarile se fac cu Blender in fundal (nu se atinge scena deschisa). PDF-ul cere Python-ul cu reportlab (runtime Codex).
Modelele de feronerie parametrice lipsa (ex. sina_suspendare@614) se exporta automat cu freecadcmd."""
import sys, json, subprocess, os, importlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripturi'))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
FREECADCMD = r"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe"
REG = {
    'noptiera': ('montaj_spec_noptiera', 'noptiera'),
    'dulap_wc': ('montaj_spec_mici', 'dulap_wc'),
    'corp_spate_pat': ('montaj_spec_comode', 'corp_spate_pat'),
    'comoda_tv_dormitor': ('montaj_spec_comode', 'comoda_tv_dormitor'),
    'machiaj': ('montaj_spec_comode', 'machiaj'),
    'comoda_tv_zi': ('montaj_spec_comode', 'comoda_tv_zi'),
    'debara': ('montaj_spec_debara', 'debara'),
    'spalatorie': ('montaj_spec_spalatorie', 'spalatorie'),
    'dulap_hol': ('montaj_spec_dulapuri', 'dulap_hol'),
    'dressing': ('montaj_spec_dressing', 'dressing'),
    'dulap_dormitor': ('montaj_spec_dulap_dormitor', 'dulap_dormitor'),
    'bucatarie': ('montaj_spec_bucatarie', 'bucatarie'),
}


def load(slug):
    mod, fn = REG[slug]
    return getattr(importlib.import_module(mod), fn)()


def ensure_models(S):
    obj = ROOT / 'tmp' / 'feronerie_R2' / 'obj'
    need = sorted({h['model'] for h in S.hwi} | {p['model'] for p in S.parts if p.get('model')})
    miss = [m for m in need if not (obj / (m + '.obj')).exists()]
    if miss:
        r = subprocess.run([FREECADCMD, str(ROOT / 'scripturi' / 'feronerie_cad_export.py')] + miss, capture_output=True, text=True)
        print('export feronerie:', miss, [l for l in r.stdout.splitlines() if l.startswith(('OK', 'EROARE'))])


if __name__ == '__main__':
    slug = sys.argv[1]
    what = sys.argv[2] if len(sys.argv) > 2 else 'all'
    S = load(slug)
    D = ROOT / 'tmp' / 'montaj' / slug
    D.mkdir(parents=True, exist_ok=True)
    if what in ('spec', 'blender', 'all'):
        (D / 'spec.json').write_text(json.dumps(S.to_json(), ensure_ascii=False, indent=1), encoding='utf-8')
    if what in ('blender', 'all'):
        ensure_models(S)
        blend = getattr(S, 'blend', None)
        cmd = [BLENDER, '--background', '--python', str(ROOT / 'scripturi' / 'montaj_blender.py'), '--', str(D / 'spec.json'), str(D)]
        if blend:
            cmd += [blend]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print([l for l in r.stdout.splitlines() if 'MONTAJ_OK' in l or 'Error' in l or 'LIPSA' in l][-5:], r.stderr[-400:])
    if what in ('panouri', 'all'):
        import montaj_panouri
        montaj_panouri.build(S, D, run=True)
    if what in ('pdf',):
        import montaj_pdf
        print(montaj_pdf.build(S, D))
