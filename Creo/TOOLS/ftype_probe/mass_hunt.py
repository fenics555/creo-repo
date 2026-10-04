import struct

F = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
d = open(F, 'rb').read()
VAL = 6.686151041318472
be = struct.pack('>d', VAL)
print('ЭТАЛОН MASS = %.17g' % VAL)
print('BE(8) = %s' % be.hex(' ').upper())
print('ФАЙЛ %d байт\n' % len(d))

# 1) полное 8-байтовое вхождение
full = [hex(i) for i in range(len(d)) if d.startswith(be, i)]
print('1) полное 8-байтовое BE: %s' % (full if full else 'НЕТ'))

# 2) хвост из 7 байт
tail7 = be[1:]
t7 = [hex(i) for i in range(len(d)) if d.startswith(tail7, i)]
print('2) хвост be[1:8] (%s): %d вхождений %s'
      % (tail7.hex(' ').upper(), len(t7), t7[:12]))

# 3) хвост из 6 байт
tail6 = be[2:]
t6 = [hex(i) for i in range(len(d)) if d.startswith(tail6, i)]
print('3) хвост be[2:8] (%s): %d вхождений %s'
      % (tail6.hex(' ').upper(), len(t6), t6[:12]))
print()

# 4) что вокруг PRO_MP_MASS
for tag in (b'PRO_MP_MASS', b'MASS\x00'):
    i = d.find(tag)
    print('4) %s @%s' % (tag, hex(i) if i >= 0 else 'НЕ НАЙДЕНО'))
    if i >= 0:
        print('   %s' % d[i - 16:i + 40].hex(' ').upper())

print()
print('=== ПРИМЕРЫ контекста вокруг хвостов be[2:8] ===')
for i in [int(x, 16) for x in t6[:6]]:
    print('  @%-9s %s' % (hex(i), d[i - 12:i + 12].hex(' ').upper()))