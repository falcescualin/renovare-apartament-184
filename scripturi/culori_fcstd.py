"""Citește culorile (ShapeAppearance) obiectelor dintr-un .FCStd fără interfață FreeCAD: GuiDocument.xml leagă
fiecare obiect de un fișier binar „ShapeAppearanceN” (listă de materiale; primul are culoarea difuză).
Folosire: from culori_fcstd import culori; culori('dulap_dormitor.FCStd') → {nume_obiect: (r, g, b) 0–255}"""
import zipfile, re, struct


def culori(path):
    z = zipfile.ZipFile(path)
    gui = z.read('GuiDocument.xml').decode('utf-8', 'replace')
    out = {}
    for name, body in re.findall(r'<ViewProvider name="([^"]+)"[^>]*>(.*?)</ViewProvider>', gui, re.S):
        m = re.search(r'<Property name="ShapeAppearance"[^>]*>\s*<MaterialList file="([^"]+)"', body)
        if not m or m.group(1) not in z.namelist():
            continue
        b = z.read(m.group(1))
        if len(b) < 12:
            continue
        n = struct.unpack('<I', b[:4])[0]
        if n < 1:
            continue
        v = struct.unpack('<I', b[8:12])[0]                 # ambient, apoi difuz
        out[name] = ((v >> 24) & 255, (v >> 16) & 255, (v >> 8) & 255)
    return out


if __name__ == '__main__':
    import sys, collections
    for f in sys.argv[1:]:
        c = culori(f)
        cnt = collections.Counter(c.values())
        print(f, len(c), cnt.most_common(12))
