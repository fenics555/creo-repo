import struct, json

F = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
b = open(F, 'rb').read()
off, ln = 0x70b0, 1398927
blob = b[off:off + ln]
print('SolidPrimdata: %d байт' % len(blob))

dims = json.load(open(r'D:\AI\repo\Creo\TOOLS\ftype_probe\dims_137.json',
                      encoding='utf-8'))['dims']
want = {d['name']: float(d['value']) for d in dims}
print('известных размеров: %d -> %s' % (len(want), list(want.items())[:6]))
print()

# полное сканирование IEEE-754 в секции
hits = []
for i in range(len(blob) - 8):
    h = blob[i:i + 8]
    e = ((h[0] & 0x7F) << 4) | (h[1] >> 4)
    if not (1020 <= e <= 1040):
        continue
    try:
        v = struct.unpack('>d', h)[0]
    except Exception:
        continue
    if 1e-4 < abs(v) < 1e7:
        hits.append((i, v))

print('ВСЕГО IEEE-754 double в секции: %d' % len(hits))

# СВЕРКА с размерами
print()
print('=== СВЕРКА С РАЗМЕРАМИ CREOSON ===')
hitset = {round(v, 4): i for i, v in hits}
matched = 0
for nm, val in want.items():
    for cand in (round(val, 4), round(-val, 4),
                 round(val * 2, 4), round(val / 2, 4),
                 round(val * 25.4, 4)):
        if cand in hitset:
            print('   %-5s = %-10.4f  найдено в SolidPrimdata @ +%d (0x%x)'
                  % (nm, val, hitset[cand], hitset[cand]))
            matched += 1
            break
print()
print('СОВПАДЕНИЙ: %d из %d размеров' % (matched, len(want)))

# статистика значений
vals = [v for _, v in hits]
if vals:
    print()
    print('ДИАПАЗОН: от %.4f до %.4f' % (min(vals), max(vals)))
    neg = sum(1 for v in vals if v < 0)
    print('отрицательных (координаты): %d из %d' % (neg, len(vals)))

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