"""Materiale realiste (procedurale), tavan, cer/soare si setari Cycles pentru apartamentul 184.
Se ruleaza in Blender pe scena importata (apartament_184.blend). Nu modifica geometria pieselor."""
import bpy, math

sc = bpy.context.scene


def srgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


def new_mat(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (600, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (300, 0)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return m, nt, bsdf


def setp(bsdf, name, val):
    if name in bsdf.inputs:
        bsdf.inputs[name].default_value = val


def simple(name, hexcol, rough=0.5, metal=0.0, sheen=0.0, coat=0.0):
    m, nt, b = new_mat(name)
    b.inputs["Base Color"].default_value = (*srgb(hexcol), 1)
    setp(b, "Roughness", rough); setp(b, "Metallic", metal)
    setp(b, "Sheen Weight", sheen); setp(b, "Coat Weight", coat)
    m.diffuse_color = (*srgb(hexcol), 1)
    return m


def bump(nt, bsdf, scale=200.0, strength=0.05, detail=8.0, coords="Object"):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = detail
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = strength
    nt.links.new(tc.outputs[coords], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], bsdf.inputs["Normal"])
    return tc


def wood(name, light="#C9A27A", dark="#9C7550", rough=0.42, scale=1.0, axis_rot=0.0):
    m, nt, b = new_mat(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (scale * 1.0, scale * 12.0, scale * 1.0)
    mp.inputs["Rotation"].default_value = (0, 0, axis_rot)
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 3.0; wv.inputs["Distortion"].default_value = 6.0
    wv.inputs["Detail"].default_value = 4.0
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 40.0; nz.inputs["Detail"].default_value = 6.0
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = 'FLOAT'; mix.inputs["Factor"].default_value = 0.35
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*srgb(dark), 1); ramp.color_ramp.elements[1].color = (*srgb(light), 1)
    ramp.color_ramp.elements[0].position = 0.25; ramp.color_ramp.elements[1].position = 0.8
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], wv.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    nt.links.new(wv.outputs["Fac"], mix.inputs["A"])
    nt.links.new(nz.outputs["Fac"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.08
    nt.links.new(mix.outputs["Result"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    setp(b, "Roughness", rough)
    m.diffuse_color = (*srgb(light), 1)
    return m


def planks(name, light="#C49B6E", dark="#A47A50", plank_w=0.19, plank_l=1.4, rough=0.38):
    """Parchet: placi decalate (Brick) + fibra lemn."""
    m, nt, b = new_mat(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = plank_l; br.inputs["Row Height"].default_value = plank_w
    br.inputs["Mortar Size"].default_value = 0.0015; br.inputs["Mortar Smooth"].default_value = 0.2
    br.offset = 0.37; br.inputs["Bias"].default_value = 0.0
    br.inputs["Color1"].default_value = (*srgb(light), 1); br.inputs["Color2"].default_value = (*srgb(dark), 1)
    br.inputs["Mortar"].default_value = (*srgb("#5a4632"), 1)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 14.0, 1.0)
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 2.0; wv.inputs["Distortion"].default_value = 8.0
    mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs["Factor"].default_value = 0.25
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], wv.inputs["Vector"])
    nt.links.new(br.outputs["Color"], mul.inputs["A"]); nt.links.new(wv.outputs["Color"], mul.inputs["B"])
    nt.links.new(mul.outputs["Result"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.3; bp.invert = True
    nt.links.new(br.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    setp(b, "Roughness", rough)
    m.diffuse_color = (*srgb(light), 1)
    return m


def tiles(name, col="#CFC8BC", grout="#B5ADA0", size=0.6, rough=0.25):
    m, nt, b = new_mat(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = size; br.inputs["Row Height"].default_value = size
    br.inputs["Mortar Size"].default_value = 0.002; br.offset = 0.0
    br.inputs["Color1"].default_value = (*srgb(col), 1); br.inputs["Color2"].default_value = (*srgb(col), 1)
    br.inputs["Mortar"].default_value = (*srgb(grout), 1)
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 6.0
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = 'RGBA'; mix.blend_type = 'OVERLAY'; mix.inputs["Factor"].default_value = 0.08
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"]); nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(br.outputs["Color"], mix.inputs["A"]); nt.links.new(nz.outputs["Color"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.2; bp.invert = True
    nt.links.new(br.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    setp(b, "Roughness", rough)
    m.diffuse_color = (*srgb(col), 1)
    return m


def stone(name, a="#E2D6C3", c="#C9B89D", rough=0.32):
    m, nt, b = new_mat(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 6.0; nz.inputs["Detail"].default_value = 14.0
    nz.inputs["Distortion"].default_value = 0.6
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 5.0, 1.0)
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*srgb(c), 1); ramp.color_ramp.elements[1].color = (*srgb(a), 1)
    pores = nt.nodes.new("ShaderNodeTexVoronoi"); pores.inputs["Scale"].default_value = 180.0
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.12; bp.invert = True
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tc.outputs["Object"], pores.inputs["Vector"])
    nt.links.new(pores.outputs["Distance"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    setp(b, "Roughness", rough)
    m.diffuse_color = (*srgb(a), 1)
    return m


def fabric(name, hexcol, rough=0.9, sheen=0.6, scale=600.0):
    m, nt, b = new_mat(name)
    b.inputs["Base Color"].default_value = (*srgb(hexcol), 1)
    setp(b, "Roughness", rough); setp(b, "Sheen Weight", sheen); setp(b, "Sheen Roughness", 0.5)
    bump(nt, b, scale=scale, strength=0.15)
    m.diffuse_color = (*srgb(hexcol), 1)
    return m


def emission(name, rgb=(1.0, 0.74, 0.46), strength=20.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*rgb, 1); em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs[0])
    m.diffuse_color = (*rgb, 1)
    return m


def glass(name, tint=(0.95, 0.97, 0.97), rough=0.0):
    m, nt, b = new_mat(name)
    b.inputs["Base Color"].default_value = (*tint, 1)
    setp(b, "Transmission Weight", 1.0); setp(b, "Roughness", rough); setp(b, "IOR", 1.45)
    m.diffuse_color = (*tint, 0.3)
    return m


MAT = {
    "perete": simple("R_Vopsea_perete_alb_cald", "#ECE8E1", rough=0.85),
    "tavan": simple("R_Tavan_alb", "#F3F1EC", rough=0.9),
    "w1000": simple("R_Egger_W1000_ST9_alb", "#E9E8E3", rough=0.45, sheen=0.1),
    "u702": simple("R_Egger_U702_ST9_Cashmere", "#B8AEA2", rough=0.5, sheen=0.1),
    "stejar": wood("R_Stejar_natural_H1145"),
    "stejar_deschis": wood("R_Stejar_deschis_riflaje", light="#D9B98F", dark="#B8936A"),
    "parchet": planks("R_Parchet_stejar"),
    "gresie": tiles("R_Gresie_60x60_greige"),
    "gresie_baie": tiles("R_Gresie_baie_60x120", col="#D8D2C8", size=0.6),
    "travertin": stone("R_Travertin_bej"),
    "canapea": fabric("R_Textil_canapea_gri_bej", "#B9B2A8"),
    "pat": fabric("R_Textil_pat_alb_cald", "#D8D2C9"),
    "draperie": fabric("R_Draperie_in_bej", "#BFB3A2", sheen=0.4, scale=900.0),
    "boucle": fabric("R_Boucle_alb", "#E7E2DA", sheen=0.3, scale=120.0),
    "scaun_textil": fabric("R_Textil_scaune", "#8F8A84"),
    "pasla": fabric("R_Pasla_antracit", "#3A3633", sheen=0.2),
    "sticla": glass("R_Sticla_clara"),
    "oglinda": simple("R_Oglinda", "#E8ECEE", rough=0.02, metal=1.0),
    "inox": simple("R_Inox_periat", "#C9CACB", rough=0.28, metal=1.0),
    "frigider": simple("R_TCL_gri_quartz", "#6E7073", rough=0.3, metal=0.7),
    "negru": simple("R_Negru_mat", "#1C1C1D", rough=0.5),
    "metal_negru": simple("R_Metal_negru", "#202022", rough=0.35, metal=0.8),
    "ecran": simple("R_Ecran_TV", "#050506", rough=0.05, coat=1.0),
    "sticla_neagra": simple("R_Sticla_neagra", "#0B0B0D", rough=0.04, coat=1.0),
    "ceramica": simple("R_Ceramica_alba", "#F4F3EF", rough=0.06, coat=0.6),
    "usa": simple("R_Usa_interior_alb_satinat", "#E6E3DD", rough=0.35),
    "beton": simple("R_Beton", "#8D8A86", rough=0.9),
    "led": emission("R_LED_alb_cald", (1.0, 0.72, 0.45), 18.0),
    "plafoniera": emission("R_Plafoniera_LED", (1.0, 0.86, 0.70), 6.0),
}

RULES = [  # (cheie material, lista de fragmente din numele obiectului) - prima potrivire castiga
    ("HIDE", ["Usa_baie_sens_propus"]),
    ("plafoniera", ["Plafoniera"]),
    ("oglinda", ["Machiaj_oglinda_LED"]),
    ("led", ["LED_", "_LED", "LED"]),
    ("oglinda", ["oglinda", "Oglinda"]),
    ("sticla_neagra", ["Cuptor_usa_sticla", "MW_fereastra_usa", "MW_front_sticla", "MW_corp", "Cuptor_panou_comanda"]),
    ("sticla", ["Geamuri", "geam", "Geam", "Paravan_sticla", "Perete_sticla", "Hublou_sticla", "planseta"]),
    ("ecran", ["_ecran"]),
    ("parchet", ["Pardoseala_CameraDeZi", "Pardoseala_Dormitor", "Pardoseala_Hol", "Pardoseala_Vestibul"]),
    ("gresie_baie", ["Pardoseala_Baie"]),
    ("gresie", ["Pardoseala_Bucatarie", "Pardoseala_Nisa", "Balcon_placa"]),
    ("perete", ["Pereti", "Balcon_parapet", "Bagheta", "Cornisa"]),
    ("tavan", ["Balcon_tavan"]),
    ("beton", ["Placa_baza"]),
    ("travertin", ["travertin"]),
    ("pasla", ["pasla"]),
    ("stejar_deschis", ["Riflaje_lamele"]),
    ("stejar", ["stejar", "Comoda_TV_corp", "Comoda_TV_front", "Machiaj_corp", "Machiaj_front", "Picior_cilindru",
                "Bucatarie_custom__Blat", "Masa_blat", "Comoda_blat"]),
    ("canapea", ["Canapea"]),
    ("pat", ["Pat"]),
    ("draperie", ["Draperie", "Rulou_bucatarie_material"]),
    ("boucle", ["Puf_boucle"]),
    ("scaun_textil", ["Scaun_1", "Scaun_2"]),
    ("usa", ["Usa_U"]),
    ("frigider", ["TCL_corp", "TCL_usa"]),
    ("inox", ["Cuptor_corp", "Cuptor_front", "Cuptor_maner", "Plita_tabla", "Chiuveta", "Baterie", "Hota", "M2_masina_vase",
              "TCL_maner", "Bara", "Tub_hota", "Calorifer_prosop", "Profil_paravan", "Balama", "Masa_calcat_unitate", "Uscator_rufe"]),
    ("metal_negru", ["suport_", "Aplica_liniara", "Masa_picior", "Scaun_birou"]),
    ("negru", ["carcasa", "Arzator", "Gratar", "_buton", "Plita_buton", "Cuptor_buton", "display", "Masa_TROTTEN"]),
    ("ceramica", ["Cada", "Lavoar_60", "WC_suspendat", "Colac_WC"]),
]
FRONT_COLORS = {"FC_ccc2b3_t0", "FC_ccc1b2_t0", "FC_b8b4ab_t0"}   # fronturi greige (U702) din FreeCAD


def lightness(mat):
    c = mat.diffuse_color
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


stats = {}
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    key = None
    for k, frags in RULES:
        if any(f in o.name for f in frags):
            key = k; break
    if key == "HIDE":
        o.hide_render = True; continue
    cur = o.data.materials[0] if o.data.materials else None
    if key is None and cur is not None:
        if cur.name in FRONT_COLORS:
            key = "u702"
        elif cur.name.startswith("FC_") and lightness(cur) > 0.75:
            key = "w1000"
    if key is None:
        if cur is not None and cur.use_nodes:   # culoare FreeCAD pastrata, rugozitate realista
            b = cur.node_tree.nodes.get("Principled BSDF")
            if b: b.inputs["Roughness"].default_value = 0.5
        stats["(culoare FreeCAD)"] = stats.get("(culoare FreeCAD)", 0) + 1
        continue
    o.data.materials.clear(); o.data.materials.append(MAT[key])
    stats[key] = stats.get(key, 0) + 1
    if key == "led":
        o.visible_shadow = False

# masa de birou TROTTEN: blat alb, picioare albe
for n in ("Masa",):
    o = bpy.data.objects.get(n)
    if o: o.data.materials.clear(); o.data.materials.append(MAT["w1000"])

# tavanul balconului vizibil la randare
bt = bpy.data.objects.get("Balcon_tavan")
if bt:
    bt.hide_render = False; bt.hide_set(False)

# tavan apartament (placa 15 cm la 2,50 m) - doar pentru randare
col = bpy.data.collections.get("RANDARE") or bpy.data.collections.new("RANDARE")
if col.name not in sc.collection.children:
    sc.collection.children.link(col)
if not bpy.data.objects.get("R_Tavan_apartament"):
    me = bpy.data.meshes.new("R_Tavan_apartament")
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(me); bm.free()
    t = bpy.data.objects.new("R_Tavan_apartament", me)
    t.scale = (11.2, 5.75, 0.15); t.location = (5.6, -2.85, 2.575)
    col.objects.link(t)
    bpy.context.view_layer.objects.active = t; t.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); t.select_set(False)
    t.data.materials.append(MAT["tavan"])
# sol exterior (apartament la etaj)
if not bpy.data.objects.get("R_Sol_exterior"):
    bpy.ops.mesh.primitive_plane_add(size=200, location=(5.5, -3.0, -9.0))
    g = bpy.context.active_object; g.name = "R_Sol_exterior"
    for c in list(g.users_collection): c.objects.unlink(g)
    col.objects.link(g)
    g.data.materials.append(simple("R_Sol_iarba_gri", "#6F7A5E", rough=0.95))

# cer + soare
world = sc.world or bpy.data.worlds.new("World"); sc.world = world
world.use_nodes = True
wn = world.node_tree; wn.nodes.clear()
wo = wn.nodes.new("ShaderNodeOutputWorld")
sky = wn.nodes.new("ShaderNodeTexSky")
try:
    sky.sky_type = 'NISHITA'
except Exception:
    pass
for attr, val in (("sun_elevation", math.radians(28)), ("sun_rotation", math.radians(200)), ("sun_disc", False),
                  ("altitude", 30.0), ("air_density", 1.0), ("dust_density", 1.2)):
    try: setattr(sky, attr, val)
    except Exception: pass
bg = wn.nodes.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = 0.35
wn.links.new(sky.outputs[0], bg.inputs[0]); wn.links.new(bg.outputs[0], wo.inputs[0])

sun = bpy.data.objects.get("R_Soare")
if not sun:
    sd = bpy.data.lights.new("R_Soare", 'SUN'); sun = bpy.data.objects.new("R_Soare", sd); col.objects.link(sun)
sun.data.energy = 4.0; sun.data.angle = math.radians(1.5); sun.data.color = (1.0, 0.93, 0.84)
sun.rotation_euler = (math.radians(62), 0, math.radians(200))

# Cycles pe GPU (OptiX)
sc.render.engine = 'CYCLES'
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'; prefs.get_devices()
    for d in prefs.devices: d.use = (d.type == 'OPTIX')
    sc.cycles.device = 'GPU'
except Exception:
    pass
sc.cycles.samples = 512
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.01
sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPTIX'
except Exception: pass
sc.cycles.max_bounces = 12; sc.cycles.diffuse_bounces = 6; sc.cycles.glossy_bounces = 6
sc.cycles.transmission_bounces = 8; sc.cycles.sample_clamp_indirect = 8.0
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1200, 100
try:
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    pass
sc.view_settings.exposure = 0.6
result_stats = stats
print("MATERIALE", stats)
