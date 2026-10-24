from pathlib import Path
p=Path('scripturi/plan_termic_pdf.py')
s=p.read_text(encoding='utf-8-sig')
needle="y=table(42,150,[60,390,55,100,501],rows,10)"
inject='''links_termice={
 'IT01':('https://www.purmo.com/docs/purmo-catalog-radiatoare-panou-ro.pdf','Catalog Purmo Compact'),
 'IT02':('https://www.purmo.com/docs/purmo-catalog-radiatoare-panou-ro.pdf','Catalog Purmo Compact'),
 'IT03':('https://www.purmo.com/ro-ro/produse/14407/santorini/','Purmo Santorini'),
 'IT04':('https://www.purmo.com/docs/purmo-catalog-radiatoare-panou-ro.pdf','Console / accesorii'),
 'IT05':('https://assets.danfoss.com/documents/latest/208753/AB370141588735ro-RO0101.pdf','Set Danfoss / fișă'),
 'IT06':('https://assets.danfoss.com/documents/latest/208753/AB370141588735ro-RO0101.pdf','Retur inclus în set'),
 'IT07':('https://www.purmo.com/docs/purmo-catalog-radiatoare-panou-ro.pdf','Accesorii radiator'),
 'IT08':('https://www.geberit.ro/sisteme-sanitare-tevi/sisteme-de-alimentare-cu-apa/geberit-mapress/geberit-mapress-otel-carbon/','Exemplu sistem de țevi'),
 'IT09':('https://www.geberit.ro/sisteme-sanitare-tevi/sisteme-de-alimentare-cu-apa/geberit-mapress/geberit-mapress-otel-carbon/','Fitinguri de sistem'),
 'IT10':('https://www.geberit.ro/_assets/local-media/geberit-mapress-manual-tehnic-2022.pdf','Detalii de montaj')}
for row in rows[1:]:
 if row[0] in links_termice:
  url,label=links_termice[row[0]]
  row[1]+=' <link href="'+url+'" color="#277dba">'+label+'</link>.'
y=table(42,150,[60,390,55,100,501],rows,10)'''
if 'links_termice=' not in s:s=s.replace(needle,inject)
s=s.replace('Oferta trebuie să separe echipamentele, accesoriile deja incluse, manopera, golirea instalației, evacuarea și refacerile.','Linkurile albastre sunt exemple de selecție, nu produse aprobate; IT05/IT06 pot fi același kit și nu se comandă dublu. Compatibilitatea țevilor cu circuitul se verifică. Oferta separă materialele și manopera.')
p.write_text(s,encoding='utf-8')
print('Thermal links added')
