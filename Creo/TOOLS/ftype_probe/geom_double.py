import struct

F = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
b = open(F, 'rb').read()
off = 0x70b0
blob = b[off:off + 400]

print('=== Попытка: ищем IEEE-754 double в SolidPrimdata ===')
print('Известные размеры модели: d9=360 d10=27 d11=43 d12=1200 d13=30')
print()

# ищем все 8-байтовые окна, где байты[6:8] — старший байт double
found = []
for i in range(len(blob) - 8):
    h = blob[i:i + 8]
    e = ((h[0] & 0x7F) << 4) | (h[1] >> 4)
    if 1020 <= e <= 1040:            # разумный порядок
        try:
            v = struct.unpack('>d', h)[0]
        except Exception:
            continue
        if 0.0001 < abs(v) < 1e7:
            found.append((i, v, h.hex(' ').upper()))

print('найдено «разумных» double: %d' % len(found))
print()
for i, v, hx in found[:26]:
    mark = ''
    for d, t in (('d9', 360.0), ('d10', 27.0), ('d11', 43.0),
                 ('d12', 1200.0), ('d13', 30.0), ('d15', 10.0)):
        if abs(v - t) < 1e-6:
            mark = '   <<< = %s' % d
    print('  +%-5d %-26s = %-16.6g%s' % (i, hx, v, mark))