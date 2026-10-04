import os, struct

# поиск файла
path = None
for root, dirs, fs in os.walk(r'Z:\PTC\Work'):
    for f in fs:
        if f.lower() == 'is-10_001_001_003.prt.1':
            path = os.path.join(root, f)
if not path:
    raise SystemExit('файл не найден')
d = open(path, 'rb').read()
print('ФАЙЛ: %s (%d байт)' % (path, len(d)))
print()

NAMES = {'ДИАМЕТР': 19.05, 'MASS': 0.6253065868809754}

print('=' * 70)
print('УДАР 1 + 2: позиции имён и их BE-эталоны')
print('=' * 70)
pos = {}
for nm, v in NAMES.items():
    nb = nm.encode('utf-8')
    print('%s  utf8 = %s' % (nm, nb.hex(' ').upper()))
    be = struct.pack('>d', v)
    print('   значение %.15g' % v)
    print('   BE(8) = %s' % be.hex(' ').upper())
    occ = []
    s = 0
    while True:
        i = d.find(b'\xe3' + nb + b'\x00', s)
        if i < 0:
            break
        occ.append(i)
        s = i + 1
    pos[nm] = occ
    print('   вхождений "E3 <имя> 00": %d -> %s' % (len(occ), [hex(x) for x in occ]))
    print()

print('=' * 70)
print('УДАР 3: полный контекст каждой записи')
print('=' * 70)
for nm, v in NAMES.items():
    be = struct.pack('>d', v)
    for i in pos[nm]:
        win = d[i:i + 80]
        print('--- %s @ %s  (значение %.15g)' % (nm, hex(i), v))
        print('    %s' % win[:60].hex(' ').upper())
        print('    ASCII: %s' % repr(win[:60].decode('ascii', 'replace')))
        # ищем какой кусрок BE реально лежит рядом
        found = []
        for lead in range(0, 5):
            for trail in range(0, 9):
                body = be[lead:8 - trail] if 8 - trail > lead else b''
                if not body:
                    continue
                j = win.find(body)
                if j >= 0:
                    found.append((len(body), lead, trail, win[j - 1], j))
        found.sort(reverse=True)
        if found:
            ln, lead, trail, tag, j = found[0]
            print('    СОВПАДЕНИЕ: tag=0x%02X lead=%d trail=%d длина=%d'
                  % (tag, lead, trail, ln))
            print('    контекст: %s' % win[max(0, j - 10):j + ln + 4].hex(' ').upper())
        else:
            print('    СОВПАДЕНИЙ BE НЕТ в окне 80 байт')
        print()

print('=' * 70)
print('СКВОЗНАЯ ЛЕНТА: от первого ДИАМЕТР до первого MASS')
print('=' * 70)
if pos['ДИАМЕТР'] and pos['MASS']:
    a = pos['ДИАМЕТР'][0]
    b = pos['MASS'][0]
    lo, hi = min(a, b), max(a, b)
    print('ДИАМЕТР @ %s, MASS @ %s, расстояние %d байт'
          % (hex(a), hex(b), hi - lo))
    seg = d[lo:hi]
    print('длина сегмента: %d' % len(seg))
    print()
    # все E3-объекты внутри сегмента
    import re
    print('E3-объекты между ними:')
    for m in re.finditer(rb'\xe3([\x20-\x7e\xd0-\xf0][\x20-\x7e\x80-\xbf]{1,40}?)\x00', seg):
        print('   @+%d  %r' % (m.start(), m.group(1).decode('utf-8', 'replace')))
    print()
    print('первые 160 байт сегмента:')
    print('   %s' % seg[:160].hex(' ').upper())