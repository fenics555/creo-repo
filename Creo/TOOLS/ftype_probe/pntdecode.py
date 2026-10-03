# -*- coding: utf-8 -*-
"""ДЕКОДЕР ТОЧЕК: применяем формулу 2^(E+1)x(1+F/4096) к потоку crv_pnt_arr.
Эмпирика, а не теория: перебираем, какая сегментация даёт правдоподобные значения.
Проверяем 3 гипотезы формата:
  Г1: фикс. 3 байта  = 2F|48 (E<<4|F>>8) (F&0xFF)
  Г2: 1 байт         = старший ниббл = E, значение = 2^(E-15)
  Г3: 2 байта        = байт маркера + байт E:F
Запуск: python pntdecode.py [папка] [файлов]
Вывод: pntdecode_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)

def val3(b0, b1, b2):
    if b0 not in MARK3:
        return None
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

def val1(b):
    e = (b & 0xF0) >> 4
    return 2.0 ** (e - 15)

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    nf = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            if f.lower().endswith('.prt.1'):
                files.append(os.path.join(root, f))
        if len(files) > 30000:
            break
    random.seed(11)
    random.shuffle(files)
    files = files[:nf]

    out = io.open('pntdecode_out.txt', 'w', encoding='utf-8')
    out.write('ДЕКОДЕР ТОЧЕК · папка %s · файлов %d\n\n' % (base, nf))

    g3 = g1 = 0
    v3 = []
    v1 = []
    samples = []
    for fp in files:
        try:
            data = open(fp, 'rb').read()
        except Exception:
            continue
        if b'crv_pnt_arr' not in data:
            continue
        hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
                for m in FIELD.finditer(data)]
        for i, (pos, nm, end) in enumerate(hits):
            if nm != 'crv_pnt_arr':
                continue
            nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            payload = data[end:nxt]
            if len(payload) < 12 or len(payload) > 120:
                continue
            body = payload[4:]              # снимаем маркер F9 xx 04
            # Г3: фикс 3 байта
            d3 = 0
            loc3 = []
            for k in range(0, len(body) - 2, 3):
                x = val3(body[k], body[k + 1], body[k + 2])
                if x is not None:
                    d3 += 1
                    loc3.append(x)
                    v3.append(x)
            if d3:
                g3 += 1
                if len(samples) < 6 and d3 >= 3:
                    samples.append((os.path.basename(fp), payload, loc3))
            # Г1: все байты как 1-байтовые
            loc1 = [val1(b) for b in body if (b & 0xF0)]
            if loc1:
                g1 += 1
                v1.extend(loc1)

    def stats(vals, name):
        if not vals:
            out.write('%s: нет данных\n' % name)
            return
        good = [v for v in vals if 0.001 <= abs(v) <= 1000]
        out.write('%s: всего %d, правдоподобных (0.001..1000) %d = %.1f%%\n'
                  % (name, len(vals), len(good), 100.0 * len(good) / len(vals)))
        good2 = sorted(good)
        if good2:
            out.write('   мин %.5g  макс %.5g  медиана %.5g\n'
                      % (good2[0], good2[-1], good2[len(good2) // 2]))
            cnt = collections.Counter(round(v, 4) for v in good2)
            out.write('   ТОП-12 значений: %s\n'
                      % ', '.join('%g×%d' % (k, c) for k, c in cnt.most_common(12)))

    out.write('записей, где Г3 дала хоть одно число: %d\n' % g3)
    out.write('записей, где Г1 применима: %d\n\n' % g1)
    stats(v3, 'Г3 (3 байта, маркер 2F/48)')
    stats(v1, 'Г1 (1 байт, ниббл=E)')

    out.write('\n=== ПРИМЕРЫ ДЕКОДИРОВАНИЯ ===\n')
    for nm, payload, loc3 in samples:
        out.write('\n--- %s, payload %d б ---\n' % (nm, len(payload)))
        out.write('   hex  : %s\n' % ' '.join('%02X' % c for c in payload[:48]))
        out.write('   Г3   : %s\n' % ', '.join('%.5g' % v for v in loc3[:14]))
    out.close()
    print('pntdecode_out.txt g3=%d g1=%d' % (g3, g1))

if __name__ == '__main__':
    main()