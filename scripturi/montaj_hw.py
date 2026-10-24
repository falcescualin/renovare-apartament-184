"""Feronerie 3D pozitionata automat din gaurile calculate (montaj_holes): confirmate, cepuri, suruburile glisierelor.
auto(S) adauga instantele in S.hwi; count(S) numara bucatile pe litera (pentru lista de feronerie si pentru banda de pe fiecare pas)."""
import montaj_holes


def auto(S, conf_explode=45.0, rail_explode=70.0):
    info = montaj_holes.compute(S)
    seen = set()
    for pid, d in info.items():
        for h in d['h3']:
            key = (h['kind'], tuple(round(v, 1) for v in h['pos']))
            if key in seen:
                continue
            seen.add(key)
            n = h['n_out']
            if h['kind'] == 'conf7':
                S.hw_at(h['step'], 'confirmat', h['pos'], az=n, attach=pid, explode=conf_explode, letter='A', tag='conf')
            elif h['kind'] == 'cep8' and h['face'] != 'muchie' and h.get('with_'):
                # cepul: 12 mm in fata panoului A, 23 mm in muchia lui B; se misca odata cu B (e batut intai in muchie)
                top = [h['pos'][i] - n[i] * 12.0 for i in range(3)]
                S.hw_at(h['step'], 'cep', top, az=[-v for v in n], attach=h['with_'], explode=0.0, letter='C', dash=False, tag='cep')
            elif h['kind'] == 'rail':
                at = [h['pos'][i] + n[i] * 1.5 for i in range(3)]          # capul pe flansa profilului (1,5 mm)
                S.hw_at(h['step'], 'surub_3_5x15', at, az=n, attach=h['with_'], explode=rail_explode, letter=getattr(S, 'rail_letter', 'D15'), tag='rail')
    return info


def count(S, step=None):
    out = {}
    for h in S.hwi:
        if step is not None and h['step'] != step:
            continue
        k = (h['letter'], h['model'].split('@')[0])
        out[k] = out.get(k, 0) + 1
    return out
