"""R04: plan electric R03 cu referinte R06 si balcon explicit."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripturi'))
wrapper=(ROOT/'scripturi/plan_electric_R03.py').read_text(encoding='utf-8')
wrapper=wrapper[:wrapper.rfind('exec(compile(SRC,')]
exec(compile(wrapper,'plan_electric_R03_base','exec'))
SRC=SRC.replace('Apartament_184_Plan_electric_R03.pdf','Apartament_184_Plan_electric_R05.pdf').replace('Apartament_184_Registru_electric_R03.csv','Apartament_184_Registru_electric_R05.csv')
SRC=SRC.replace('R03 |','R05 |')
SRC=SRC.replace('exec(patch_prefix(prefix))',"exec(patch_prefix(prefix).replace('05.10.2026','06.10.2026'))")
SRC=SRC.replace("'revision':'R03'","'revision':'R05'")
SRC=SRC.replace('Plafonieră Balcon închis','Plafonieră Balcon închis / LED, IP54 propus')
SRC=SRC.replace('Montaj electric R05','Montaj electric R07').replace('montajul electric R05','montajul electric R07')
import re
POS={'J01': [7250, -3750, 2400], 'J02': [7100, -3750, 2400], 'J03': [3550, -3600, 2400], 'J04': [2525, -4050, 2400], 'J05': [9000, -3470, 2400], 'J06': [9875, -2350, 2400]}
replacement='BOXES='+repr([(k,v[0],v[1],{'J01':'Hol / perete spre sufragerie','J02':'Sufragerie / perete spre hol','J03':'Dormitor / perete spre sufragerie','J04':'Vestibul / perete spre baie','J05':'Bucătărie / perete spre hol','J06':'Debara / perete spre bucătărie'}[k],{'J01':'C02','J02':'C01','J03':'C01','J04':'C03','J05':'C02','J06':'C02'}[k]) for k,v in POS.items()])
SRC=re.sub(r'BOXES=\[.*?\]\n',lambda m:replacement+'\n',SRC,count=1)
SRC=SRC.replace('2300','2400')
exec(compile(SRC,'plan_electric_R05','exec'))

