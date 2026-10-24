"""Bază comună pentru planșele A3 refăcute pe 05.10.2026 cu ultimele decizii: plan electric R03, montaj electric R05,
plan sanitar R02, plan termic R02, plan de mobilare R02.

Nu modifică scripturile originale (plan_termic_pdf.py, plan_electric_pdf.py, ...): le citește și le actualizează la rulare.
- patch_prefix(): fundalul de mobilier vine din tmp/mobilier_plan.json (36 de piese extrase din scena 3D de
  extrage_mobilier_plan.py, cu conturul real); corpurile suspendate se desenează cu linie întreruptă. Adaugă și
  funcții de desen comune (tbl, dvrow, dvlink) în același spațiu cu prefixul.
- DVR: rândurile devizului curent (tmp/deviz.json, R03), cu cea mai bună ofertă, magazin și link.
- cable_circuits(): cablul de 230 V calculat exact pe traseele complete din montajul electric."""
import json, math, collections, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DV = json.loads((ROOT / 'tmp/deviz.json').read_text(encoding='utf-8'))
DVR = {r['id']: r for r in DV['rows']}
MOBP = json.loads((ROOT / 'tmp/mobilier_plan.json').read_text(encoding='utf-8'))['items']

# circuitele din planul electric (plan_electric_pdf.py): id, puncte, destinație, cablu, protecție
CIRCUITE = [
    ('C01', 'L01, L02, F03', 'Iluminat dormitor + cameră de zi', '3×1,5', 'B10 + AFDD'),
    ('C02', 'L03–L06, F01, F02, F04–F06', 'Iluminat hol, bucătărie, debara, balcon + LED', '3×1,5', 'B10'),
    ('C03', 'L07, L08, F07', 'Iluminat vestibul + baie + ventilator', '3×1,5', 'B10'),
    ('C04', 'P01–P05', 'Prize dormitor', '3×2,5', 'B16 + AFDD'),
    ('C05', 'P06–P11', 'Prize cameră de zi, TV, birou, fier de călcat', '3×2,5', 'B16'),
    ('C06', 'P13', 'Prize baie', '3×2,5', 'B16'),
    ('C07', 'P12', 'Mașina de spălat rufe', '3×2,5', 'B16'),
    ('C08', 'P17', 'Mașina de spălat vase', '3×2,5', 'B16'),
    ('C09', 'P20', 'Cuptor', '3×2,5', 'B16'),
    ('C10', 'P15, P16, P18, P19, P21, P22', 'Prize bucătărie, hotă, aprindere plită, microunde', '3×2,5', 'B16'),
    ('C11', 'P14', 'Frigider', '3×2,5', 'B16'),
    ('C12', 'P23', 'Internet: ONT, router, switch', '3×2,5', 'B16')]

OLD_FURN = (" for f in DATA['furniture']:\n"
            "  b=f['bbox'];p=P(b[0],b[4]);rect(*p,(b[3]-b[0])*k,(b[4]-b[1])*k,fill=HexColor('#eef0f1'),stroke=GRAY,lw=.5)\n")
NEW_FURN = (" for f in MOB:\n"
            "  if f['code'] in ('R1','R2','RP'):continue\n"
            "  for q in f.get('polys') or [f['poly']]:\n"
            "   pts=[P(*v) for v in q]\n"
            "   if f['kind']=='sus':c.setDash([3,2]);poly(pts,color=HexColor('#9aa7b0'),lw=.5);c.setDash([])\n"
            "   else:poly(pts,fill=HexColor('#eef0f1'),color=GRAY,lw=.5)\n")
OLD_DATA = "DATA=json.loads((ROOT/'tmp/termic_model.json').read_text(encoding='utf-8'))\n"

# funcții de desen adăugate la prefix (au nevoie de c, H, styles, ... din prefix)
HELPERS = r'''
import html as _html
MOB=json.loads((ROOT/'tmp/mobilier_plan.json').read_text(encoding='utf-8'))['items']
if 8 not in styles:styles[8]=ParagraphStyle('p8',parent=style,fontSize=8,leading=10.2)
def esc(s):return _html.escape(str(s),quote=False)
def lei(v):return '{:,.0f}'.format(v).replace(',','.')
def lei2(v):return '{:,.2f}'.format(v).replace(',','#').replace('.',',').replace('#','.')
def tbl(x,y,widths,rows,size=9,pad=4,total=False,head=True):
 ps=styles[size]
 cells=[[Paragraph(str(cell),ps) for cell in row] for row in rows]
 t=Table(cells,colWidths=widths,repeatRows=1 if head else 0,hAlign='LEFT')
 st=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad),('LINEBELOW',(0,1),(-1,-1),.35,GRAY)]
 if head:st+=[('BACKGROUND',(0,0),(-1,0),LIGHT),('LINEBELOW',(0,0),(-1,0),1,TEAL)]
 if total:st+=[('BACKGROUND',(0,-1),(-1,-1),LIGHT),('LINEABOVE',(0,-1),(-1,-1),1,TEAL)]
 t.setStyle(TableStyle(st))
 _,h=t.wrapOn(c,sum(widths),3000)
 if y+h>H-75:raise ValueError('Tabel prea lung pe pagina '+str(PAGE)+': '+str(round(y+h)))
 c.setLineWidth(.6);t.drawOn(c,x,H-y-h);return y+h
def dvlink(r,label=None):
 s=label or where(r)
 if r.get('url'):return '<link href="'+_html.escape(r['url'])+'" color="#277dba"><u>'+esc(s)+'</u></link>'
 return esc(s)
def qty(r):return ('%g'%r['q']).replace('.',',')+' '+r['um']
def dvrow(i,art=None,extra=None):
 r=DVR[i];row=[i,'<b>'+esc(art or r['art'])+'</b>'+('<br/>'+extra if extra else ''),qty(r),lei(r['tmin']),dvlink(r)]
 return row
'''


def patch_prefix(src):
    """Prefixul din plan_termic_pdf.py cu mobilierul actual ca fundal și funcțiile comune adăugate la sfârșit."""
    assert OLD_FURN in src and OLD_DATA in src, 'prefixul din plan_termic_pdf.py s-a schimbat'
    return src.replace(OLD_FURN, NEW_FURN) + HELPERS


def where(r):
    """unde se cumpără, pe scurt (fără data observării)"""
    s = r.get('magazin') or r.get('price_basis') or ''
    s = s.replace(' (05.10.2026)', '')
    if s.startswith('Cea mai bună ofertă: '):
        s = s[len('Cea mai bună ofertă: '):].split('; alternativă:')[0]
    if s.startswith('Buget provizoriu') or not s:
        s = 'estimat, produsul se alege la cumpărare'
    return s


# ---------------------------------------------------------------- cabluri pe traseele complete (montaj electric)
def routes_file():
    return Path(sorted(glob.glob(str(ROOT / 'output/pdf/Apartament_184_Trasee_complete_R0*.json')))[-1])


def union_len(paths):
    """lungimea reuniunii segmentelor (m): porțiunile suprapuse se numără o singură dată"""
    groups = collections.defaultdict(list)
    other = 0
    for p in paths:
        for a, b in zip(p, p[1:]):
            v = [b[i] - a[i] for i in range(3)]
            nz = [i for i in range(3) if abs(v[i]) > 0.5]
            if not nz:
                continue
            if len(nz) == 1:
                ax = nz[0]
                key = (ax,) + tuple(round(a[i]) for i in range(3) if i != ax)
                groups[key].append(sorted([a[ax], b[ax]]))
            else:
                other += math.dist(a, b)
    tot = other
    for iv in groups.values():
        iv.sort()
        m = []
        for lo, hi in iv:
            if m and lo <= m[-1][1] + 1:
                m[-1][1] = max(m[-1][1], hi)
            else:
                m.append([lo, hi])
        tot += sum(h - l for l, h in m)
    return tot / 1000


def drop(p):
    """coborârea verticală finală până la aparat (m)"""
    a, b = p[-2], p[-1]
    return abs(a[2] - b[2]) / 1000 if a[0] == b[0] and a[1] == b[1] else 0


def cable_circuits(routes):
    """Cablul de 230 V pe fiecare circuit. Aparatele de pe un circuit se leagă unul după altul, deci traseul comun se
    numără o singură dată; la prize se adaugă urcarea înapoi la tavan între prize (fără ultima), 1 m la tablou și 0,3 m
    la fiecare aparat (întrerupătoarele au deja coborârea lor). LED-ul de 24 V de la noptiere (F08A/B) nu intră aici."""
    out = []
    for ci, ids, dest, sec, prot in CIRCUITE:
        rs = [r for r in routes if r.get('circuit') == ci and r['kind'] != 'V']
        pts = [r for r in rs if r['kind'] in 'PFLS']
        u = union_len([r['points'] for r in rs])
        up = sum(sorted(drop(r['points']) for r in pts)[:-1]) if ci >= 'C04' and len(pts) > 1 else 0
        cap = 0.3 * sum(1 for r in pts if r['kind'] != 'S')
        out.append(dict(id=ci, ids=ids, dest=dest, sec=sec, prot=prot, n=len(pts), union=u, urcari=up, te=1.0, capete=cap,
                        total=u + up + 1.0 + cap))
    return out


def cable_totals(cc):
    t15 = sum(r['total'] for r in cc if r['sec'] == '3×1,5')
    t25 = sum(r['total'] for r in cc if r['sec'] == '3×2,5')
    return math.ceil(t15), math.ceil(t25)


def data_lines(routes):
    """Cat6 și coaxial în stea: fiecare priză are cablul ei până la distribuitorul NET; +2 m rezervă pe legătură
    (1 m ordonat la distribuitor, 0,3 m în doză, restul la tăiere)."""
    return [dict(id=r['id'], kind=r['kind'], desc=r['desc'], geo=r['length_m'], buy=r['length_m'] + 2.0)
            for r in routes if r['kind'] in ('D', 'T')]
