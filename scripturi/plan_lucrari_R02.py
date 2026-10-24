"""Plan de lucrări R02 (06.10.2026): plan_lucrari_pdf.py nemodificat, cu plățile din devizul R04 (plăci Kronospan,
debitare exactă). Rulează cu Python-ul care are reportlab. Iese: output/pdf/Apartament_184_Plan_lucrari_R02.pdf"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
src = (ROOT / 'scripturi/plan_lucrari_pdf.py').read_text(encoding='utf-8')
for a, b in [("'output/pdf/Apartament_184_Plan_lucrari_R01.pdf'", "'output/pdf/Apartament_184_Plan_lucrari_R02.pdf'"),
             ("Plan de lucrari si calendar - R01", "Plan de lucrari si calendar - R02")]:
    assert a in src, a
    src = src.replace(a, b)
src = src.replace("'R01 |", "'R02 |")
exec(compile(src, 'plan_lucrari_pdf.py', 'exec'), {'__name__': '__main__', '__file__': str(ROOT / 'scripturi/plan_lucrari_pdf.py')})
