from pathlib import Path
import sys,csv,json,math
from collections import Counter
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'output/woodworking_pilot'; TMP=ROOT/'tmp/noptiera_documente'
sys.path.insert(0,str(ROOT/'scripturi'))
from montaj_spec_noptiera import noptiera
S=noptiera()
def read(name):
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
hw=read('Feronerie_noptiera.csv'); holes=read('Gaurire_noptiera.csv'); panels=read('comparatie_R03.csv')
for r in hw:r['Bucati']=int(r['Bucati']);r['Optional']=r['Optional']=='True'
for r in holes:
    for k in ('X_mm','Y_mm','Z_mm','Nx','Ny','Nz','Diametru_mm','Adancime_mm'):r[k]=float(r[k])
    r['Trecere']=r['Trecere']=='True'
for r in panels:
    for k in ('L','W','grosime','R03_L','R03_W','R03_grosime'):r[k]=float(r[k])
    r['conform']=r['conform']=='True'
notes=[
    'Pilot P02, 08.10.2026. Se referă la Noptiera_Woodworking_Feronerie.FCStd.',
    'TIP-ON L1 T60L7340 pentru NL350 și masa totală sertar până la 20 kg. Confirmați masa încărcată înainte de comandă.',
    'Fronturile din pilot au 496 mm, joc lateral 2 mm; lista comună R03 are 497 mm. Documentele R03 nu au fost modificate.',
    'Jocul dintre spatele frontului și muchia corpului: 2,5 mm. Nu se adaugă tampoane care împiedică apăsarea TIP-ON.',
    'Mecanismele Blum sunt modele locale simplificate. Nu s-a validat cinematica sau absența tuturor interferențelor.',
    'Canturile sunt metadate R03. Diametrele pilot pentru șuruburi se adaptează la PAL și șurubul real. Tabelul nu este program CNC.'
]
sources=['https://publications.blum.com/2022/catalogue/en/436/','https://publications.blum.com/2022/catalogue/en/437/','https://ea.blum.com/en/assembly-and-processing-steps-for-tip-on-blumotion/']
data=dict(hw=hw,holes=holes,panels=panels,notes=notes,sources=sources)
(TMP/'date.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
for name,font in [('Seg','segoeui.ttf'),('SegB','segoeuib.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+font))
pdfmetrics.registerFontFamily('Seg',normal='Seg',bold='SegB')
W,H=landscape(A3); INK=HexColor('#24343f'); MUT=HexColor('#62717c'); ACC=HexColor('#b56e35'); LIGHT=HexColor('#f0f3f5')
path=ROOT/'output/pdf/Apartament_184_Montaj_noptiera_Woodworking_P02.pdf'
c=canvas.Canvas(str(path),pagesize=(W,H));c.setTitle('Noptieră - montaj cu feronerie - Woodworking P02');c.setAuthor('Codex')
page=0
def para(text,x,y,width,size=12,color=INK):
    p=Paragraph(text,ParagraphStyle('p',fontName='Seg',fontSize=size,leading=size*1.42,textColor=color))
    _,h=p.wrap(width,900);p.drawOn(c,x,y-h);return y-h-12
def begin(title,sub=''):
    global page
    if page:c.showPage()
    page+=1;c.setFillColor(INK);c.setFont('SegB',24);c.drawString(40,H-52,title)
    c.setStrokeColor(ACC);c.line(40,H-72,W-40,H-72)
    c.setFont('Seg',9);c.setFillColor(MUT);c.drawString(40,23,'Apartament 184, Bloc L14 / Noptieră / Woodworking P02 / 08.10.2026 / cote în mm')
    c.drawRightString(W-40,23,str(page))
    if sub:para(sub,40,H-86,W-80,11,MUT)
def table(rows,x,y,widths,size=10):
    st=ParagraphStyle('cell',fontName='Seg',fontSize=size,leading=size*1.3,textColor=INK)
    head=ParagraphStyle('head',fontName='SegB',fontSize=size,leading=size*1.3,textColor=white)
    rr=[[Paragraph(escape(str(v)),head if i==0 else st) for v in row] for i,row in enumerate(rows)]
    t=Table(rr,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    tw,th=t.wrap(sum(widths),H)
    assert y-th>42,(page,'table overflow',th,y)
    t.drawOn(c,x,y-th);return y-th
def diagram(step,x,y,w,h):
    pp=[p for p in S.parts if p['code'].startswith('N-') and (p['step']<=step or (step==1 and p['code']=='N-09'))]
    if not pp:return
    vertices=[]; polys=[]
    for p in pp:
        bx,by,bz,dx,dy,dz=p['box']
        if p['role']=='door':by+=2.5
        off=(S.steps[step-1].get('explode') or {}).get(p['id'],[0,0,0])
        bx+=off[0];by+=off[1];bz+=off[2]
        vv=[(bx+i*dx,by+j*dy,bz+k*dz) for i,j,k in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]]
        pr=[((a-b)*.707,z+(a+b)*.30) for a,b,z in vv];vertices+=pr;polys.append((p,pr))
    minx=min(v[0] for v in vertices);maxx=max(v[0] for v in vertices);miny=min(v[1] for v in vertices);maxy=max(v[1] for v in vertices)
    scale=min((w-35)/(maxx-minx or 1),(h-40)/(maxy-miny or 1))
    for p,pr in sorted(polys,key=lambda q:sum(q[0]['box'][:2])):
        active=p['step']==step or (step==1 and p['code']=='N-09')
        c.setStrokeColor(ACC if active else MUT);c.setLineWidth(1.3 if active else .6)
        pts=[(x+15+(a-minx)*scale,y+15+(b-miny)*scale) for a,b in pr]
        for i,j in [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]:c.line(*pts[i],*pts[j])
        if active:
            c.setFillColor(ACC);c.setFont('SegB',9);c.drawString(pts[6][0]+3,pts[6][1],p['code'])
    for hw in [h for h in S.hwi if h['step']==step and h['model']!='banda_dublu']:
        a,b,z=hw['at'];px=x+15+((a-b)*.707-minx)*scale;py=y+15+(z+(a+b)*.30-miny)*scale
        c.setFillColor(ACC);c.circle(px,py,2.3,fill=1,stroke=0)
        if not hw['model'].startswith(('surub','confirmat','cep','capac','saiba')):
            c.setFont('SegB',9);c.drawString(px+4,py+4,hw['letter'])
    c.setFont('Seg',10);c.setFillColor(MUT);c.drawString(x,y-8,'Schemă: panouri active și puncte de feronerie în portocaliu.')
begin('Noptieră - plan de montaj cu feronerie','Revizie pilot P02. Citirea modelului, pregătirea pieselor, asamblare și găurire individuală.')
y=H-128
for n in notes:y=para(n,40,y,585,12)
y=para('<b>Ordinea lucrului</b><br/>1. Lipire blat. 2. Glisiere. 3. Corp. 4. Spate. 5. Suport blat. 6. TIP-ON și sincronizare. 7. Cutiile sertarelor. 8. Fronturi. 9. Blat și LED. 10. Capace. 11. Poziționare.',40,y,585,12)
c.drawImage(str(OUT/'Noptiera_cu_feronerie.png'),660,260,460,400,preserveAspectRatio=True,anchor='c',mask='auto')
para('<b>Documentație Blum</b><br/>'+'<br/>'.join(sources),40,160,W-80,9)
begin('Lista feroneriei','Cantități numărate în model, fără rezerve. „Opțional” indică fixarea în perete, ascunsă în model.')
table([['Piesă','Bucăți','Geometrie','Opțional']]+[[r['Denumire'],r['Bucati'],r['Precizie'],'Da' if r['Optional'] else 'Nu'] for r in hw],40,H-125,[730,80,150,150])
begin('Panourile și dimensiunile finite','Cantul este inclus în cotele finite. Atelierul stabilește cota brută de debitare. Fronturile P02: 496 mm.')
bycode={}
for p in panels:bycode.setdefault(p['cod'],[]).append(p)
table([['Cod','Buc.','L × W × grosime (mm)','Material','Cant L1 / L2 / W1 / W2']]+[[cod,len(rr),f"{rr[0]['L']:g} × {rr[0]['W']:g} × {rr[0]['grosime']:g}",rr[0]['material'],' / '.join(rr[0][k] for k in ('L1','L2','W1','W2'))] for cod,rr in bycode.items()],40,H-125,[140,70,270,160,470],11)
para('Canturi: „2” = ABS 2 mm; „0.8” = ABS 0,8 mm; „42” = bandă 42 × 2 mm pe blatul dublat; „-” = fără cant. Panourile cu același cod pot avea găurire în oglindă; folosiți identificatorul individual din paginile următoare.',40,315,W-80,12)
for step in S.steps:
    n=step['n'];begin(f"Pasul {n:02d}. {step['title']}")
    diagram(n,40,185,510,460)
    y=H-112
    texts=[t.replace('S1','L1').replace('Ø8 × 22','Ø8 × 23') for t in step['text']]
    texts=[t.replace('urmând cele două pagini de detaliu (poziționare cu distanțiere, bandă dublu adeziv (H), apoi 4 șuruburi 4 × 25 cu șaibă (N) din interior)', 'folosind fișele individuale de găurire: poziționare provizorie, apoi 4 șuruburi 4 × 25 cu șaibă din interior').replace(', după pagina „Prindere în perete”','; verificați suportul real al peretelui înainte de alegerea diblului') for t in texts]
    for idx,t in enumerate(texts,1):y=para(f'<b>{idx}.</b> '+t,590,y,550,12)
    if n==6:y=para('<b>Corecție P02:</b> L1 T60L7340, NL350, până la 20 kg/sertar încărcat. Bara T60.1125W: 464 - 267 = 197 mm; setul L1 include adaptoarele de sincronizare.',590,y,550,12)
    if n==8:y=para('<b>Corecție P02:</b> fronturi 496 mm; joc lateral 2 mm și joc frontal 2,5 mm. Folosiți șablonul 65.5631. Nu adăugați tampoane de oprire.',590,y,550,12)
    for t in step.get('warn',[]):y=para('<b>Atenție:</b> '+t,590,y,550,11,ACC)
    for t in step.get('check',[]):y=para('<b>Verificați:</b> '+t,590,y,550,11)
    counted=Counter(h['model'] for h in S.hwi if h['step']==n and h['model']!='banda_dublu')
    counted.update(p['model'] for p in S.parts if p['code']=='SL' and p['step']==n)
    y=para('<b>Feronerie la acest pas</b><br/>'+('; '.join(f'{m}: {q} buc.' for m,q in counted.items()) or 'Adeziv și clești / consumabile conform instrucțiunilor.'),590,y,550,10)
    assert y>45,(n,'text overflow',y)

partmap={p['id']:p for p in S.parts if p['code'].startswith('N-')}
kindnames={'conf7':'Confirmat: trecere','pilot5':'Confirmat: pilot muchie','cep8':'Cep','rail':'Prindere glisieră','hook6':'Cârlig MOVENTO','pilot_front':'Pilot front','pilot_suport':'Pilot suport/blat'}
for pid,p in partmap.items():
    hh=[r for r in holes if r['Panou']==pid]
    if not hh:continue
    for chunk in range(0,len(hh),20):
        begin(f"Găurire. {p['code']} - {p['label']}",f'Identificator individual: {pid}. Coordonate globale ale modelului; tabelul include și coordonate locale de la colțul minim al panoului.')
        bx,by,bz,dx,dy,dz=p['box'];by+=2.5 if p['role']=='door' else 0
        y=H-130
        y=para(f'<b>Origine locală globală:</b> X={bx:g}, Y={by:g}, Z={bz:g} mm.<br/><b>Gabarit pe axe:</b> X={dx:g}, Y={dy:g}, Z={dz:g} mm.<br/>+X = stânga privit din față; +Y = fața corpului; +Z = sus. Normală N = direcția spre exterior; burghiul avansează pe -N. Nu oglindiți tabelul după cod.',40,y,310,11)
        rr=[['Nr.','Tip','X local','Y local','Z local','N (X,Y,Z)','Ø','Adânc.','Trecere']]
        for i,r in enumerate(hh[chunk:chunk+20],chunk+1):
            label=kindnames.get(r['Tip'],r['Tip'].replace('fixare_surub_','Șurub '))
            rr.append([i,label,f"{r['X_mm']-bx:g}",f"{r['Y_mm']-by:g}",f"{r['Z_mm']-bz:g}",','.join(f'{r[k]:g}' for k in ('Nx','Ny','Nz')),f"{r['Diametru_mm']:g}",f"{r['Adancime_mm']:g}",'Da' if r['Trecere'] else 'Nu'])
        table(rr,385,H-132,[35,170,66,66,66,100,50,75,65],9)
        y=para('Cep Ø8 × 35: găuri 12 mm în față + 23 mm în muchie. Controlați adâncimea cu opritor. Nu găuriți prin fețele decorative pentru găuri oarbe.',40,y,310,11)
        # Face projection with numbered hole centres; edge holes retain N in table.
        dims=[dx,dy,dz];t=min(range(3),key=lambda i:dims[i]);axes=[i for i in range(3) if i!=t];u,v=axes
        scale=min(280/dims[u],250/dims[v]);ox,oy=45,90
        c.setStrokeColor(MUT);c.rect(ox,oy,dims[u]*scale,dims[v]*scale)
        c.setFont('Seg',9);c.drawString(ox,oy-15,f"Axe proiecție: {'XYZ'[u]} orizontal / {'XYZ'[v]} vertical")
        for i,r in enumerate(hh[chunk:chunk+20],chunk+1):
            local=[r['X_mm']-bx,r['Y_mm']-by,r['Z_mm']-bz];px=ox+local[u]*scale;py=oy+local[v]*scale
            c.setFillColor(ACC);c.circle(px,py,2,fill=1,stroke=0);c.setFont('Seg',7);c.drawString(px+3,py+3,str(i))
begin('Controlul final și punctele de confirmat')
y=H-115
for t in ['24 de panouri, 169 de instanțe de feronerie și 232 de operații de găurire în modelul P02.','Verificări efectuate: solide valide, găurile intersectează panoul, găurile oarbe nu ies din panou; fișierul FreeCAD se redeschide.','Înainte de execuție: confirmați fronturile 496/497 mm, masa fiecărui sertar încărcat și variantele exacte de mecanisme.','La probă: sertarele trebuie să intre fără forțare, să se cupleze în cleme, să se deschidă prin apăsare și să se închidă fără atingerea corpului.','Verificați găurile de cârlig și clemele cu șablonul Blum T65.1000.02. Verificați jocul TIP-ON cu 65.5631.','Modelul mecanismelor este simplificat. Verificarea geometrică de mai sus nu confirmă cinematica, rezistența îmbinărilor sau toate interferențele.']:
    y=para(t,40,y,730,14)
c.save()
print(json.dumps({'pdf':str(path),'pages':page,'hw':sum(r['Bucati'] for r in hw),'holes':len(holes)},ensure_ascii=False))
