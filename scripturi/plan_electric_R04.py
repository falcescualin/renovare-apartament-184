"""R04: plan electric R03 cu referinte R06 si balcon explicit."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripturi'))
wrapper=(ROOT/'scripturi/plan_electric_R03.py').read_text(encoding='utf-8')
wrapper=wrapper[:wrapper.rfind('exec(compile(SRC,')]
exec(compile(wrapper,'plan_electric_R03_base','exec'))
SRC=SRC.replace('Apartament_184_Plan_electric_R03.pdf','Apartament_184_Plan_electric_R04.pdf').replace('Apartament_184_Registru_electric_R03.csv','Apartament_184_Registru_electric_R04.csv')
SRC=SRC.replace('R03 |','R04 |')
SRC=SRC.replace('exec(patch_prefix(prefix))',"exec(patch_prefix(prefix).replace('05.10.2026','06.10.2026'))")
SRC=SRC.replace("'revision':'R03'","'revision':'R04'")
SRC=SRC.replace('Plafonieră Balcon închis','Plafonieră Balcon închis / LED, IP54 propus')
SRC=SRC.replace('Montaj electric R05','Montaj electric R06').replace('montajul electric R05','montajul electric R06')
exec(compile(SRC,'plan_electric_R04','exec'))
