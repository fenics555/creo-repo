import re, os

FILE_PATH = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
d = open(FILE_PATH, 'rb').read()
print('ФАЙЛ: %s  (%d байт)' % (os.path.basename(FILE_PATH), len(d)))

SIG = b'\x18\xe6\xf8\x02'
hits = list(re.finditer(re.escape(SIG), d))
print('вхождений 18 E6 F8 02: %d' % len(hits))
print()

NAMEPAT = re.compile(rb'([A-Za-z][A-Za-z0-9_]{1,29})\x00')

owners = {}
for m in hits:
    pos = m.start()
    back = d[max(0, pos - 40):pos]
    names = NAMEPAT.findall(back)
    if names:
        nm = names[-1].decode('latin-1')
        owners[nm] = owners.get(nm, 0) + 1

print('уникальных имён владельцев: %d' % len(owners))
print()
print('=== ТОП-20 владельцев ===')
for nm, n in sorted(owners.items(), key=lambda x: -x[1])[:20]:
    print('   %-24s %d' % (nm, n))

print()
print('=== есть ли RIGHT / базовые? ===')
for k in ('RIGHT', 'TOP', 'FRONT', 'PRT_CSYS_DEF', 'LEFT', 'BOTTOM', 'BACK'):
    print('   %-14s %d' % (k, owners.get(k, 0)))

print()
print('=== 20 байт ДО сигнатуры (сырой вид) для первых 12 вхождений ===')
for k, m in enumerate(hits[:12]):
    pos = m.start()
    print('   @%-9s %s' % (hex(pos),
          d[max(0, pos - 20):pos + 12].hex(' ').upper()))