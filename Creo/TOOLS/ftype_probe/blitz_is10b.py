import os, struct, re

path = r'Z:\PTC\Work\IS-10.001.001.003\is-10_001_001_003.prt.1'
d = open(path, 'rb').read()

print('=== 1. Все вхождения d_val ===')
for m in re.finditer(rb'd_val', d):
    i = m.start()
    print('@%s  %s' % (hex(i), d[max(0, i - 24):i + 24].hex(' ').upper()))

print()
print('=== 2. Форма E0 02 <имя> 00 ED <8 байт BE> — полный double ===')
cnt = 0
for m in re.finditer(rb'\xe0\x02([A-Za-z_][A-Za-z0-9_]{1,30})\x00\xed', d):
    tail = d[m.end():m.end() + 8]
    if len(tail) == 8:
        try:
            v = struct.unpack('>d', tail)[0]
        except Exception:
            continue
        nm = m.group(1).decode('latin-1')
        mark = ''
        if abs(v - 0.625306586880975) < 1e-9:
            mark = '   <<< ВОТ ОНО, MASS полностью!'
        print('   %-24s = %.15g%s' % (nm, v, mark))
        cnt += 1
    if cnt > 25:
        break

print()
print('=== 3. Полная запись MASS (2-я копия) целиком ===')
i = d.find(b'\xe3MASS\x00\xe2\x32\xe0\x02value(d_val)\x00')
print('смещение %s' % hex(i) if i >= 0 else 'не найдено')
if i >= 0:
    print(d[i:i + 120].hex(' ').upper())

print()
print('=== 4. Есть ли рядом с d_val байты 3F E4 (be[0:2] MASS) ===')
i = d.find(b'd_val')
if i >= 0:
    seg = d[max(0, i - 300):i + 300]
    for cand, nm in [(bytes.fromhex('3FE4'), 'be[0:2] MASS = 3F E4'),
                     (bytes.fromhex('0282F59411CB'), 'be[2:8] MASS'),
                     (bytes.fromhex('4033'), 'be[0:2] ДИАМЕТР = 40 33')]:
        j = seg.find(cand)
        print('   %-24s в окне ±300: %s' % (nm, hex(j) if j >= 0 else 'НЕТ'))