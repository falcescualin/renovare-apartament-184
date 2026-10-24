"""Rulează: blender --background apartament_184_randare.blend --python materiale_dormitor_codex_blender.py [-- --nu-salva]
Piesele noi din dormitor (dulap_dormitor, corp_spate_pat, tablou – modelate de Codex pe 06.10.2026) au venit în Blender
cu materiale simple „Dormitor_R_G_B” după culoarea din FreeCAD. Aici primesc materialele de randare ale proiectului:
- alb cald (232,230,217 / 232,224,209)  → R_Egger_W1000_ST9_alb   (= Kronospan 8685 BS, carcasă și uși);
- lemn (163,110,64 / 163,122,82)        → R_Stejar_natural_H1145  (= Kronospan 3025 SN, blatul corpului din spatele patului);
- negru (41,46,48 / 38,41,46 / 51,51,51 / 33,38,36) → R_Negru_mat (mânere, soclu, ramă tablou);
- gri metalic (161,168,176 / 166,173,178 / 204,204,204) → R_Inox_periat (bare, colțare, profile);
- galben LED (255,212,102)              → R_LED_alb_cald;
- culorile tabloului → vopsea mată pe pânză (materiale noi R_Tablou_*), cu textura fină a pânzei din rough_linen.
Obiectele vechi (dulapul existent, noptiera sud) rămân ascunse, cum le-a lăsat sincronizarea."""
import bpy, os, sys

SAVE = '--nu-salva' not in sys.argv
TX = r"C:\Users\Falcescu Alin\Desktop\Apartament_184_Bloc_L14\texturi"
MAP = {(232, 230, 217): 'R_Egger_W1000_ST9_alb', (232, 224, 209): 'R_Egger_W1000_ST9_alb',
       (163, 110, 64): 'R_Stejar_natural_H1145', (163, 122, 82): 'R_Stejar_natural_H1145',
       (41, 46, 48): 'R_Negru_mat', (38, 41, 46): 'R_Negru_mat', (51, 51, 51): 'R_Negru_mat',
       (161, 168, 176): 'R_Inox_periat', (166, 173, 178): 'R_Inox_periat', (166, 173, 179): 'R_Inox_periat', (204, 204, 204): 'R_Inox_periat',
       (255, 212, 102): 'R_LED_alb_cald'}
PAINT = {(235, 224, 201): 'fond crem', (163, 158, 128): 'bej', (74, 97, 82): 'verde', (184, 107, 48): 'ocru',
         (166, 82, 56): 'teracota', (33, 38, 36): 'negru'}


def srgb_lin(c):
    return tuple(((v / 255 + 0.055) / 1.055) ** 2.4 if v / 255 > 0.04045 else v / 255 / 12.92 for v in c) + (1.0,)


def paint(rgb, name):
    mn = 'R_Tablou_' + name.replace(' ', '_')
    m = bpy.data.materials.get(mn) or bpy.data.materials.new(mn)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (400, 0)
    b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.location = (100, 0)
    b.inputs['Base Color'].default_value = srgb_lin(rgb)
    b.inputs['Roughness'].default_value = 0.82
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    lin = os.path.join(TX, 'polyhaven', 'rough_linen')
    nrm = [f for f in os.listdir(lin) if '_nor_gl_' in f]
    if nrm:                                                     # țesătura pânzei, foarte fină
        tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-800, 0)
        mp = nt.nodes.new('ShaderNodeMapping'); mp.location = (-600, 0); mp.inputs['Scale'].default_value = (12, 12, 12)
        im = nt.nodes.new('ShaderNodeTexImage'); im.location = (-400, -150)
        im.image = bpy.data.images.load(os.path.join(lin, nrm[0]), check_existing=True); im.image.colorspace_settings.name = 'Non-Color'
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.location = (-150, -150); nm.inputs['Strength'].default_value = 0.25
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], im.inputs['Vector'])
        nt.links.new(im.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], b.inputs['Normal'])
    m['tablou'] = name
    return m


def rgb_of(mname):
    try:
        return tuple(int(v) for v in mname.split('_')[1:4])
    except Exception:
        return None


n, miss = 0, set()
for o in bpy.data.objects:
    if o.type != 'MESH' or not o.name.startswith(('Dulap_dormitor_custom', 'Corp_spate_pat_custom', 'Tablou_pat_custom')):
        continue
    for s in o.material_slots:
        if not s.material or not s.material.name.startswith('Dormitor_'):
            continue
        c = rgb_of(s.material.name)
        if o.name.startswith('Tablou_pat_custom') and c in PAINT and not (o.name.endswith('Rama_tablou')):
            s.material = paint(c, PAINT[c]); n += 1
        elif c in MAP:
            s.material = bpy.data.materials[MAP[c]]; n += 1
        else:
            miss.add(s.material.name)
# LED-ul lateral al oglinzii de machiaj (reparat în FreeCAD pe 06.10): material de bandă LED
o = bpy.data.objects.get('Perete_TV_dormitor_custom__Machiaj_LED_lateral_fereastra')
if o is not None and bpy.data.materials.get('R_LED_oglinda'):
    o.data.materials.clear(); o.data.materials.append(bpy.data.materials['R_LED_oglinda'])
print('DORMITOR_CODEX materiale schimbate:', n, '| necunoscute:', sorted(miss))
if SAVE:
    bpy.ops.wm.save_mainfile()
