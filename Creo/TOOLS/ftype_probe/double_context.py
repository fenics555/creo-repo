import os, struct

TARGETS = [('MASS', 2.799001052172452),
           ('DEFAULT2', 590903076.7953686),
           ('DEFAULT_XHATCH_ANGLE', 45.0),
           ('DEFAULT_XHATCH_SPACING', 2.0)]

path = None
for root, dirs, fs in os.walk(r'Z:\PTC\Work'):
    for f in fs:
        if f.lower() == 'ruscam-ufa-1014-01.prt.1':
            path = os.path.join(root, f)
if not path:
    raise SystemExit('не найден')
d = open(path, 'rb').read()
print('файл: %s (%d б)' % (path, len(d)))

for name, val in TARGETS:
    nb = name.encode('utf-8')
    # ищем ВСЕ вхождения имени
    occ = []
    s = 0
    while True:
        i = d.find(nb, s)
        if i < 0:
            break
        occ.append(i)
        s = i + 1
    be = struct.pack('>d', val)
    print()
    print('=== %-24s эталон=%.10f' % (name, val))
    print('    BE(8) = %s' % be.hex(' ').upper())
    print('    вхождений имени: %d -> %s' % (len(occ), [hex(x) for x in occ[:6]]))
    # для каждого вхождения ищем максимальный суффикс BE, реально лежащий рядом
    for i in occ[:3]:
        win = d[max(0, i - 12):i + len(nb) + 40]
        best = 0
        for n in range(1, 9):
            if d.find(be[:n], i - 12, i + len(nb) + 40) >= 0:
                best = n
        tail = 0
        for n in range(8, 0, -1):
            if d.find(be[:n], i, i + len(nb) + 40) >= 0:
                tail = n
                break
        print('    @%s  окно: %s' % (hex(i), win.hex(' ').upper()))
        print('           ASCII: %s' % win.decode('ascii', 'replace'))
        print('           префикс BE найден: %d байт' % best)