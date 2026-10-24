"""Unelte comune pentru specificatiile de montaj ale corpurilor (R04): piese din planul de debitare R03, lista de feronerie generata din model."""
import json
from pathlib import Path
from feronerie_catalog import INFO
import montaj_hw

ROOT = Path(__file__).resolve().parents[1]
R03 = {p['cod']: p for p in json.loads((ROOT / 'tmp/lista_debitare_R03.json').read_text(encoding='utf-8'))['piese']}
MAT = {'ALB18': 'corp', 'CAS18': 'front', 'STJ18': 'stj', 'HDF3': 'hdf', 'ALB16': 'corp', 'BLAT38': 'blat'}

# literele feroneriei, aceleasi in toate documentele (R04)
NAMES = {
    'A': ('confirmat', 'Confirmat Ø7 × 50, hex 4'), 'B': ('capac_confirmat', 'Capac confirmat, culoarea plăcii'), 'C': ('cep', 'Cep lemn Ø8 × 35'),
    'D': ('surub_3_5x16', 'Șurub PAL 3,5 × 16, cap înecat'), 'D15': ('surub_3_5x15', 'Șurub PAL Blum 3,5 × 15 (609.1500)'),
    'D17': ('surub_3_5x17', 'Șurub PAL Blum 3,5 × 17 (609.1700)'), 'E': ('surub_4x30', 'Șurub PAL 4 × 30, cap înecat'),
    'I': ('surub_4x16', 'Șurub PAL 4 × 16, cap bombat'), 'N': ('surub_4x25', 'Șurub PAL 4 × 25, cap bombat'), 'W': ('saiba', 'Șaibă M4 (Ø9)'),
    'U': ('surub_4x40', 'Șurub PAL 4 × 40, cap înecat'), 'T': ('diblu_6x40', 'Diblu nylon Ø6 × 40 (după tipul peretelui)'),
    'L': ('coltar_40', 'Colțar 40 × 40'), 'H': ('banda_dublu', 'Bandă dublu adeziv 25 mm + distanțiere 2 și 3 mm'),
    'F': ('glisiera_movento', 'Glisieră Blum MOVENTO 760H, pereche stânga + dreapta'), 'GB': ('glisiera_bile_450', 'Glisieră cu bile 450 mm, extragere totală, soft-close (bucăți; 2 pe sertar)'), 'G': ('tip_on', 'Blum TIP-ON BLUMOTION pentru MOVENTO, pereche'),
    'Q': ('bara_sincronizare', 'Bară de sincronizare TIP-ON BLUMOTION (tăiată la lungime)'), 'P': ('cleme_movento', 'Clemă de cuplare Blum MOVENTO T51.7601, pereche'),
    'BA': ('balama_blum', 'Balama Blum CLIP top 110°'), 'PB': ('placuta_balama', 'Plăcuță Blum CLIP în cruce 0 mm (173L6100)'),
    'TO': ('tipon_usa', 'Blum TIP-ON scurt cu magnet (956.1004)'), 'AD': ('adaptor_tipon', 'Adaptor drept Blum TIP-ON (956.1201)'),
    'PM': ('placa_tipon', 'Placă metalică Ø15 pentru TIP-ON'), 'PR': ('pin_raft', 'Suport raft Ø5 cu talpă'),
    'AG': ('suport_suspendare', 'Agățătoare de corp suspendat'), 'SI': ('sina_suspendare', 'Șină de suspendare (tăiată la lungime)'),
    'PI': ('picior', 'Picior reglabil H100'), 'CS': ('clema_soclu', 'Clemă de soclu'), 'BO': ('bara_ovala', 'Bară ovală 30 × 15 (tăiată la lungime)'),
    'SB': ('suport_bara', 'Suport de capăt bară ovală'), 'CO': ('coltar_40', 'Consolă / colțar de raft'),
}
HINGE_NAMES = {'balama_blum': 'Balama Blum CLIP top 110° aplicată, fără arc (70T3550)', 'balama_70T3650': 'Balama Blum CLIP top 110° semiaplicată, fără arc (70T3650)',
               'balama_71B3550': 'Balama Blum CLIP top BLUMOTION 110° aplicată (71B3550)'}
BLUMOTION_HALF = 'Balama Blum CLIP top BLUMOTION 110° semiaplicată (71B3650)'
INSET_NAME = 'Balama Blum CLIP top 110° încastrată, fără arc (70T3750)'
LIB_LETTERS = dict(hinge=('BA', 'PB', 'D17', 'D15'), tipon=('TO', 'AD', 'PM'), hang=('AG', 'SI', 'T', 'U'))
RESERVE = {'A': 6, 'C': 4, 'D': 2, 'D15': 2, 'D17': 2, 'B': 4, 'I': 2}


def B(S, pid, code, label, x0, x1, y0, y1, z0, z1, step, mat=None, role=None):
    S.part(pid, code, label, (x0, y0, z0, x1 - x0, y1 - y0, z1 - z0), mat or MAT[R03[code]['mat']] if code in R03 else (mat or 'corp'), step, role)
    return S.parts[-1]


def caps(S, step, pids, letter='B', explode=30):
    """capace pe confirmatele care ies pe fetele vizibile ale pieselor date"""
    n = 0
    for h in [h for h in S.hwi if h['model'] == 'confirmat']:
        if h['attach'] in pids:
            S.hw_at(step, 'capac_confirmat', h['at'], az=h['az'], attach=h['attach'], explode=explode, letter=letter, dash=False)
            n += 1
    return n


def finish(S, extra=(), notes=()):
    """completeaza: literele de feronerie pe fiecare pas (din model) si lista de feronerie cu cantitati numarate"""
    letters_step = {}
    for h in S.hwi:
        letters_step.setdefault(h['step'], set()).add(h['letter'])
    rails = {}
    for p in S.parts:
        if p['code'] == 'SL':
            letters_step.setdefault(p['step'], set()).add('F')
            rails.setdefault(p.get('model', 'glisiera_movento'), []).append(p)
    order = list(NAMES)
    for st in S.steps:
        if st.get('hw') in (None, 'auto', ''):
            ls = letters_step.get(st['n'], set())
            st['hw'] = ' '.join(sorted(ls, key=lambda l: order.index(l) if l in order else 99) + list(st.get('hw_extra', [])))
    cnt = montaj_hw.count(S)
    steps_of = {}
    for h in S.hwi:
        steps_of.setdefault(h['letter'], set()).add(h['step'])
    for p in S.parts:
        if p['code'] == 'SL':
            steps_of.setdefault('F', set()).add(p['step'])
    S.hw = []
    for L in order:
        mods = {m: v for (l, m), v in cnt.items() if l == L}
        if L == 'F' and rails:
            for m, ps in rails.items():
                nl = m.split('@')[1] if '@' in m else '350'
                S.hardware('F', 'Glisieră Blum MOVENTO 760H%s0S, pereche stânga + dreapta (NL %s)' % (nl, nl), '%d perechi' % (len(ps) // 2),
                           'se prind pe laterale / despărțitori', ', '.join(map(str, sorted(steps_of['F']))), model='glisiera_movento')
            continue
        if not mods:
            continue
        model, name = NAMES[L]
        for m, v in sorted(mods.items()):
            nm = HINGE_NAMES.get(m, name)
            if L == 'BA' and getattr(S, 'inset_hinges', 0) and m == 'balama_70T3650':
                nm = INSET_NAME
            if L == 'BA' and m == 'balama_70T3650' and any(h.get('tip') == '71B3650' for p in S.parts for h in p.get('hinge_info', [])):
                nm = BLUMOTION_HALF
            if m == 'picior':
                hs = sorted({h['model'].split('@')[1] if '@' in h['model'] else '100' for h in S.hwi if h['model'].startswith('picior')})
                nm = 'Picior reglabil H%s (cu placă de prindere)' % '/'.join(hs)
            q = v + RESERVE.get(L, 0)
            if L in ('G', 'P'):
                qs = '%d perechi' % (v // 2)
            elif L in ('Q',):
                qs = '%d' % v
            else:
                qs = '%d' % q
            note = ('%d în model + %d rezervă' % (v, RESERVE[L])) if L in RESERVE else ''
            S.hardware(L, nm, qs, note, ', '.join(map(str, sorted(steps_of[L]))), model=m.split('@')[0])
    for e in extra:
        S.hardware(*e)
    S.notes = list(notes)
    return S
