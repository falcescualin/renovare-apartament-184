"""Raport defalcat al devizului, cu surse si ipoteze vizibile."""
from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parents[1]
REV=json.loads((ROOT/'tmp/deviz.json').read_text(encoding='utf-8')).get('revision','R02')
prefix=(ROOT/'scripturi/plan_termic_pdf.py').read_text(encoding='utf-8').split('# T00')[0]
prefix=prefix.replace("OUT=ROOT/'output/pdf/Apartament_184_Plan_termic_R01.pdf'","OUT=ROOT/'output/pdf/Apartament_184_Deviz_materiale_%s.pdf'"%REV)
prefix=prefix.replace('COORDONARE ȘI OFERTARE - NU PLAN DE EXECUȚIE VALIDAT','DEVIZ DE BUGET - LEI CU TVA - FĂRĂ MANOPERĂ DE ȘANTIER')
prefix=prefix.replace('R01 |',REV+' |')
exec(prefix)
D=json.loads((ROOT/'tmp/deviz.json').read_text(encoding='utf-8'))
R,S,REZ=D['rows'],D['summary'],D['rez'];TMIN,TMAX=D['tot_min'],D['tot_max']
c.setTitle('Apartament 184 - Deviz materiale si raport defalcat '+D.get('revision','R02'))
NV=sum(r['st']=='verificat' for r in R);NL=sum(r['st']!='verificat' and bool(r['url']) for r in R)
styles[8]=ParagraphStyle('p8',parent=style,fontSize=8,leading=10.8)
num=0

def money(v):return ('{:,.2f}'.format(v)).replace(',',' ').replace('.',',')
def euro(v):return ('{:,.0f}'.format(v)).replace(',',' ')
def esc(s):return html.escape(str(s))
def new(title,sub):
 global num
 num+=1;start('D'+str(num).zfill(2),title,sub)
def make_table(rows,widths,size=9):
 t=Table([[Paragraph(str(v),styles[size]) for v in row] for row in rows],colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),.35,GRAY),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f7f9fa')])]))
 _,height=t.wrap(sum(widths),2000)
 return t,height

def drawtable(t,height,y=157):
 assert y+height<H-74,(PAGE,y,height)
 t.drawOn(c,42,H-y-height)

new('Deviz de materiale și echipamente','Apartament 184 / Bloc L14 / 05.10.2026 / continuarea devizului început')
for i,(label,value,detail) in enumerate([('CELE MAI BUNE OFERTE',TMIN*1.07,'Cel mai mic preț găsit online + rezervă 7%'),('MEDIA',(TMIN+TMAX)/2*1.07,'Media celor două variante'),('ALTERNATIVĂ: MAGAZINE COMODE',TMAX*1.07,'Cumpărat din magazinele uzuale + rezervă 7%')]):
 x=42+i*373;rect(x,150,352,90,LIGHT,GRAY,.5);txt(x+13,173,label,10,TEAL,True);txt(x+13,205,euro(value)+' lei',24,INK,True);txt(x+13,226,detail,9,MUT)
rows=[['Categorie','Cele mai bune oferte, lei','Alternativă, lei','Articole','Preț verificat']]+[[s['cat'],money(s['tmin']),money(s['tmax']),s['n'],s['ver']] for s in S]
rows += [['Subtotal',money(TMIN),money(TMAX),'',''],['Rezervă financiară 7%',money(TMIN*.07),money(TMAX*.07),'',''],['TOTAL cu rezervă',money(TMIN*1.07),money(TMAX*1.07),'','']]
t,h=make_table(rows,[580,170,170,90,96],9);drawtable(t,h,266)
para(42,266+h+14,1106,'<b>Scop:</b> materiale, echipamente, mobilier, livrări și taxe de atelier. Manopera de șantier, demolările și evacuarea molozului sunt excluse. Cele '+str(len(R))+' articole includ cantități CAD și provizioane. Prețurile observate au link; celelalte sunt estimări explicite. Opționalele sunt separate de total.',10)
end()

new('Ce s-a corectat în deviz','Diferențele față de fișierul inițial și efectul asupra bugetului')
changes=[['Corecție','Bază / efect'],['Cele mai bune oferte (R03)','Pentru fiecare articol am căutat cel mai mic preț online (Hornbach, Leroy Merlin, Electricon, Celon, Regency, Feromob, Triton, Darel, JYSK, IKEA, Sanitino, Neakaisa etc.). Feroneria Blum și debitarea sunt calculate pe bucăți și pe metri. Fiecare articol are o etapă de cheltuieli și o săptămână de plată.'],['Microciment pentru pardoseală și pereți','Prețul de 1.368 lei era pentru un kit de mobilier. Acum: 2 kituri impermeabile pentru 10,58 m² pardoseală și 2 kituri de perete pentru 12 m² estimați. Bugetul folosește ambalaje întregi; o ofertă la suprafața exactă poate reduce surplusul.'],['Prețuri verificate (R02)',str(NV)+' din '+str(len(R))+' linii au preț observat online pe 05.10.2026 la produsul ales, cu link (Dedeman, eMAG, IKEA, Hornbach, Mambricolaj, furnizori Blum etc.). Alte '+str(NL)+' linii au link de reper, dar conțin părți estimate. Restul sunt loturi fără produs ales.'],['Instalația electrică R04','35 mecanisme Schuko, 4 RJ45, 3 coaxiale, 8 plafoniere și 8 comenzi. Adăugate 2 cabluri HDMI și 2 seturi tub/ieșiri. Lungimile cablurilor de putere rămân bugete preliminare, nu cantități finale de comandă.'],['Protecții și LED','10 RCBO + 2 ansambluri complete AFDD/RCBO, fără dublarea protecției incluse. 8 surse LED de buget: 6 grupuri + 2 noptiere.'],['Cadă și instalații','Cadă separat de kitul de susținere, neincluse în ofertă. Adăugat provizion pentru racordurile mașinii de spălat din vestibul și accesoriile de gaz ale plitei.'],['Pardoseli și șapă','Poligoanele modelului dau 51,09 m² interior. Șapa pentru zone uscate și cea pentru baie sunt separate. Grosimea medie de 5 mm rămâne ipoteză. Nu am introdus termopan nou pentru balconul deja închis.']]
t,h=make_table(changes,[260,846],11);drawtable(t,h)
para(42,157+h+18,1106,'<b>Reconciliere:</b> subtotal inițial '+money(D['old_total'][0])+'–'+money(D['old_total'][1])+' lei; subtotal actual '+money(TMIN)+'–'+money(TMAX)+' lei. Diferență '+money(TMIN-D['old_total'][0])+'–'+money(TMAX-D['old_total'][1])+' lei, înainte de rezerva de 7%.',11)
end()

if 'etape' in D:
 new('Etape de cheltuieli și plăți pe săptămâni','Când se cumpără fiecare grup de materiale | start lucrări luni 12.10.2026')
 rows=[['Etapă','Ce conține','Săptămâna','Cele mai bune oferte, lei','Alternativă, lei']]
 DESC={'E1':'cabluri, tuburi, doze, tablou; țevi PPR, canalizare, Geberit, cadă; radiatoare și racorduri','E2':'amorsă, șape, hidroizolație, rigips hidrofug','E3':'glet, vopsea, microciment, epoxid, parchet, plinte, praguri, baghete, riflaje','E4':'plăci Egger, debitare, cant, găurire, blat, oglinzi, feronerie Blum, LED','E5':'prize, întrerupătoare, protecții, plafoniere, aplice, obiecte sanitare finale','E6':'chiuvetă, baterie, hotă, gaz plită, electrocasnice, televizoare, suporturi','E7':'canapea, pat, saltea, masă, scaun, covor, draperii, rulouri, lenjerie','E8':'transport, împărțit pe săptămânile 1–7'}
 for st_ in D['etape']:rows.append([st_['cod']+' – '+esc(st_['nume']),DESC.get(st_['cod'],''),st_.get('sapt_txt',''),money(st_['tmin']),money(st_['tmax'])])
 rows.append(['<b>Total fără rezervă</b>','','','<b>'+money(TMIN)+'</b>','<b>'+money(TMAX)+'</b>'])
 t,h=make_table(rows,[300,446,90,135,135],9);drawtable(t,h)
 y0=157+h+40;txt(42,y0,'Plăți pe săptămâni (bara închisă = cele mai bune oferte, deschisă = alternativă)',11,INK,True)
 CF=D['cashflow'];mx=max(cf['tmax'] for cf in CF) or 1;bw=110;base=y0+200
 for k,cf in enumerate(CF):
  x=60+k*122;hh=170*cf['tmax']/mx;rect(x,base-hh,bw,hh,HexColor('#cfe6e2'),HexColor('#cfe6e2'),.1)
  hh2=170*cf['tmin']/mx;rect(x+18,base-hh2,bw-36,hh2,TEAL,TEAL,.1)
  txt(x,base+16,cf['sapt']+' · '+cf['data'][:5],9,INK,True);txt(x,base+30,euro(cf['tmin'])+' – '+euro(cf['tmax']),8.5,MUT)
  txt(x,base+43,esc(cf.get('ce','')),8,MUT)
 end()
widths=[44,305,46,44,83,83,94,94,313]
header=['ID / preț','Articol','Cant.','UM','Ofertă','Alternativă','Total ofertă','Total alt.','Cantitate / sursă / condiții']
for s in S:
 items=[r for r in R if r['cat']==s['cat']];page_rows=[header];part=1
 def catstart():
  new(s['cat']+(' / continuare '+str(part) if part>1 else ''),'Cantitate × preț unitar | lei cu TVA | V = preț observat; E = interval estimat')
 catstart()
 for r in items:
  url='<br/><link href="'+esc(r['url'])+'" color="#277dba">Sursă / exemplu</link>' if r['url'] else '<br/>Ofertă de solicitat'
  nr=[r['id']+'<br/>'+('V' if r['st']=='verificat' else 'E'),esc(r['art']),str(r['q']).replace('.',','),r['um'],money(r['pmin']),money(r['pmax']),money(r['tmin']),money(r['tmax']),esc(r['note'])+url]
  _,height=make_table(page_rows+[nr],widths,9)
  if height>550:
   t,h=make_table(page_rows,widths,9);drawtable(t,h);para(42,157+h+15,1106,'Capitolul continuă pe pagina următoare; subtotalul integral apare la finalul capitolului.',10);end();part+=1;catstart();page_rows=[header]
  page_rows.append(nr)
 total=['','<b>Subtotal capitol</b>','','','','','<b>'+money(s['tmin'])+'</b>','<b>'+money(s['tmax'])+'</b>','Fără rezervă financiară']
 _,height=make_table(page_rows+[total],widths,9)
 if height>575:
  t,h=make_table(page_rows,widths,9);drawtable(t,h);end();part+=1;catstart();page_rows=[header]
 page_rows.append(total);t,h=make_table(page_rows,widths,9);drawtable(t,h)
 para(42,157+h+14,1106,'<b>Prețuri:</b> V indică o observație pe pagina sursă, inclusiv promoție/preț standard când ambele sunt afișate. E indică buget de confirmat. Linkurile către fișe tehnice ori exemple de selecție nu confirmă prețul. Totalurile sunt fără rezerva financiară de 7%.',10)
 end()

new('Cantități și verificări','Ce este măsurat în model și ce rămâne de confirmat înainte de comandă')
rows=[['Element','Cantitate / calcul','Statut']]
for name,a in D['areas'].items():rows.append([name.replace('Pardoseala_','').replace('Balcon_placa','Balcon').replace('CameraDeZi','Camera de zi').replace('Nisa','Debara'),f'{a:.3f} m²','Arie geometrică CAD; pardoseală finisată de verificat'])
rows.extend([['Parchet living + dormitor','30,24 m² net; 33 m² buget','8% pierderi; cutiile finale de confirmat'],['Microciment pardoseală','10,58 m² net; 20 m² în kituri','Două kituri de 10 m², fără împărțire în bucăți'],['Microciment perete baie','12 m² estimați; 20 m² în kituri','Suprafața nișelor/golurilor încă nemăsurată'],['Internet Cat6','4 linii; 40,675 m geometric; 52 m buget','Rezerve la capete și rutare finală'],['Coaxial','3 linii; 29,113 m geometric; circa 35 m buget','Prize/distribuitor în același set'],['Prize de putere','23 grupuri, 35 mecanisme Schuko','Numărate în R04; rame și grad IP de coordonat'],['Plăci mobilier','31 plăci de buget, dintre care circa 9 bucătărie','Bucătăria nu are încă plan complet de debitare']])
t,h=make_table(rows,[290,350,466],10);drawtable(t,h)
end()

new('Prețurile observate și linkurile','Surse consultate la 05.10.2026; fără garanție de preț sau stoc la comandă')
hdr=[['Articol','Preț unitar, lei','Observație / link']]
obs=[[r['id']+' / '+esc(r['art']),money(r['pmin'])+'–'+money(r['pmax']),esc(r['price_basis'])+'<br/><link href="'+esc(r['url'])+'" color="#277dba">Deschide pagina produsului</link>'] for r in R if r['st']=='verificat']
chunk=[]
for row in obs:
 _,hh=make_table(hdr+chunk+[row],[420,180,506],9)
 if hh>560:
  t,h=make_table(hdr+chunk,[420,180,506],9);drawtable(t,h);end();new('Prețurile observate și linkurile / continuare','Surse consultate la 05.10.2026; fără garanție de preț sau stoc la comandă');chunk=[]
 chunk.append(row)
t,h=make_table(hdr+chunk,[420,180,506],9);drawtable(t,h)
para(42,157+h+20,1106,'<b>Restul articolelor:</b> prețuri estimate, preluate din devizul început sau adăugate ca provizion. Nu există ofertă directă reconfirmată pentru fiecare linie. În Excel, fiecare articol are bază de cantitate, explicație de preț și link, când este disponibil. Pentru furnizorii agreați Debimax/Mambricolaj se solicită o ofertă de atelier; prețul Regency este doar reper pentru PAL.',11)
end()

for off in range(0,len(D['notes']),5):
 new('Ipoteze și limite ale bugetului'+(' / continuare' if off else ''),'Elemente care trebuie confirmate pentru transformarea devizului în comandă')
 yy=155
 for i,note in enumerate(D['notes'][off:off+5],off+1):
  hh=para(42,yy,1106,'<b>'+str(i)+'.</b> '+esc(note),12);yy+=hh+23
 if off==0:para(42,yy+15,1106,'<b>Ordinea ofertării:</b> întâi releveu și soluțiile de montaj; apoi ofertă electric/sanitar/termic, finisaje complete și mobilier cu debitare; la final electrocasnice și textile. Prețurile din tabel nu substituie ofertele executanților.',12)
 end()
new('Opționale, în afara totalului','Apar separat; se adaugă numai după alegerea variantei')
rows=[['Articol','Cant.','Minim total, lei','Maxim total, lei','Condiție']]+[[o[0],str(o[1])+' '+o[2],money(o[1]*o[3]),money(o[1]*o[4]),o[5]] for o in D['opt']]
t,h=make_table(rows,[400,100,160,160,286],11);drawtable(t,h)
para(42,157+h+25,1106,'<b>Folosirea Excelului:</b> modificați cantitățile și prețurile unitare în „Deviz detaliat”. Totalurile pe articole și categorii se recalculează automat. Rezerva financiară este editabilă în F19 din „Rezumat”. Media intervalului este calculată aritmetic. PDF-ul reprezintă valorile salvate la data emiterii; după modificări, raportul se regenerează.',12)
end();c.save()
print(str(OUT));print('Pagini:',PAGE)
