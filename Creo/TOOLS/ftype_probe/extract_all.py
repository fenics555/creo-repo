import sys
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
from creo_sections import read_toc

P = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
toc, size = read_toc(P)
d = open(P, 'rb').read()

targets = [('cutextrude', b'cutextrude'),
           ('ВЫТЯГИВАНИЕ', 'ВЫТЯГИВАНИЕ'.encode('utf-8')),
           ('ОПОРНАЯ ПЛОСКОСТЬ', 'ОПОРНАЯ ПЛОСКОСТЬ'.encode('utf-8'))]

for label, pat in targets:
    i = d.find(pat)
    print('%-18s @ %s' % (label, hex(i) if i >= 0 else 'НЕ НАЙДЕНО'))
    if i >= 0:
        hit = None
        for n, (off, ln) in toc.items():
            if off <= i < off + ln:
                hit = (n, off, ln)
                break
        if hit:
            n, off, ln = hit
            print('      -> секция %-16s @0x%07x len=%d' % (n, off, ln))
        else:
            print('      -> ни одна секция не содержит (за пределами оглавления)')

print()
print('ДИАПАЗОНЫ СЕКЦИЙ:')
for n, (off, ln) in sorted(toc.items(), key=lambda x: x[1][0]):
    print('   %-18s 0x%07x - 0x%07x %9d' % (n, off, off + ln, ln))
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
from creo_sections import read_toc, section, classes

P = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
toc, size = read_toc(P)
print('ОГЛАВЛЕНИЕ: %d секций' % len(toc))
print()

# ---------- 1. ФИЧИ из AllFeatur ----------
blob, _, _ = section(P, 'AllFeatur')
print('=' * 72)
print('1. ФИЧИ — секция AllFeatur (%d байт)' % len(blob))
print('=' * 72)

txt = blob.decode('latin-1')
# имена фич: DTM*, LOCAL_GROUP*, ASM_* + базовые
names = re.findall(
    r'([A-Z][A-Za-z0-9_]{2,30})\x00', txt)
seen = []
for n in names:
    if n in seen:
        continue
    if re.match(r'^(DTM\d+|LOCAL_GROUP\d*|ASM_[A-Z_]+|PRT_CSYS_DEF|'
                r'RIGHT|TOP|FRONT|BOTTOM|LEFT|BACK|WCS|COORD_SYS)$', n):
        seen.append(n)
print('уникальных имён фич: %d' % len(seen))
print('  первые: %s' % ', '.join(seen[:18]))

# типы рядом
types = re.findall(r'\x00([a-z]{3,12}(?:extrude|round|plane|hole|sketch|'
                   r'revolve|group|csys|pattern|draft|rib|shell)\x00)', txt)
tset = {}
for t in types:
    tset[t] = tset.get(t, 0) + 1
print('  типов найдено: %d' % len(tset))
for t, c in sorted(tset.items(), key=lambda x: -x[1])[:12]:
    print('     %-14s %d' % (t, c))

# операции кириллицей
ops = re.findall(r'\x00([А-ЯЁ][А-ЯЁа-яё ]{3,28}\s\d*)', txt)
oset = {}
for o in ops:
    oset[o.strip()] = oset.get(o.strip(), 0) + 1
print('  операций (кириллица): %d уникальных' % len(oset))
for o in sorted(oset)[:14]:
    print('     %-26s %d' % (o, oset[o]))

# ---------- 2. BOM из MdlRefInfo ----------
print()
print('=' * 72)
print('2. BOM — секция MdlRefInfo')
print('=' * 72)
blob2, _, _ = section(P, 'MdlRefInfo')
print('размер: %d байт' % len(blob2))
t2 = blob2.decode('latin-1')
refs = re.findall(r'([A-Za-z0-9_\-\.]{3,44}\.(?:prt|PRT|asm|ASM))', t2)
uniq = sorted(set(refs))
print('ссылок на модели: %d вхождений, %d уникальных' % (len(refs), len(uniq)))
for r in uniq[:25]:
    print('   -> %s' % r)

# ---------- 3. FeatDefs — словарь типов ----------
print()
print('=' * 72)
print('3. СЛОВАРЬ ТИПОВ — секция FeatDefs')
print('=' * 72)
blob3, _, _ = section(P, 'FeatDefs')
print('размер: %d байт' % len(blob3))
t3 = blob3.decode('latin-1')
ty = sorted(set(re.findall(r'feat_[a-z]{3,14}', t3)))
print('feat_* кодов: %d' % len(ty))
print('   %s' % ', '.join(ty[:26]))