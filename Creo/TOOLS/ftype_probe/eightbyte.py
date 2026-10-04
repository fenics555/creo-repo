# -*- coding: utf-8 -*-
"""ДВУХФАКТОРНОЕ ЧТЕНИЕ 8-байтовых блоков «немых» записей.
Пробуем: BE/LE double, BE/LE int64, BE/LE int32-пара, fixed-point (×1e7, ×1e3).
Ищем интерпретацию, дающую КОНСТРУКТОРСКИЙ диапазон (0.001..100000).
Запуск: python eightbyte.py [папка] [файлов]
Вывод: eightbyte_out.txt
"""
import re, sys, io, os, random, struct, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK = (0x2F, 0x48)

def ok(v):
    return v is not None and v == v and 0.001 <= abs(v) <= 1e5

def interpretations(b):
    res = {}
    res['double BE'] = struct.unpack('>d', b)[0]
    res['double LE'] = struct.unpack('<d', b)[0]
    res['int64 BE'] = struct.unpack('>q', b)[0]
    res['int64 LE'] = struct.unpack('<q', b)[0]
    i1b, i2b = struct.unpack('>ii', b)
    res['int32x2 BE /1e7'] = i1b / 1e7
    res['int32x2 BE /1e3'] = i1b / 1e3
    i1l, i2l = struct.unpack('<ii', b)
    res['int32x2 LE /1e7'] = i1l / 1e7
    res['int32x2 LE /1e3'] = i1l / 1e3
    return res

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

    good = collections.Counter()
    total = 0
    samples = []
    has46 = 0
    for fp in files[:nf]:
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
            nxti = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            body = data[end + 3:nxti]
            if not (16 <= len(body) <= 200):
                continue
            if any(b in MARK for b in body):
                continue
            ps = [k for k in range(len(body)) if body[k] == 0x46]
            if ps:
                has46 += 1
            for off in range(0, len(body) - 7, 8):
                b = body[off:off + 8]
                total += 1
                d = interpretations(b)
                goodk = [k for k, v in d.items() if ok(v)]
                for k in goodk:
                    good[k] += 1
                if len(samples) < 8 and goodk:
                    samples.append((os.path.basename(fp), b, d, goodk))

    out = io.open('eightbyte_out.txt', 'w', encoding='utf-8')
    out.write('ДВУХФАКТОРНОЕ ЧТЕНИЕ 8-БАЙТОВЫХ БЛОКОВ\n')
    out.write('немых записей: %d (из них с маркером 46: %d)\n' % (has46, has46))
    out.write('8-байтовых блоков разобрано: %d\n\n' % total)
    out.write('=== СКОЛЬКО БЛОКОВ ДАЛИ КОНСТРУКТОРСКИЙ ДИАПАЗОН ===\n')
    for k, c in good.most_common():
        out.write('   %-24s %5d = %.1f %% блоков\n' % (k, c, 100.0 * c / max(1, total)))
    out.write('\n=== ПРИМЕРЫ ===\n')
    for nm, b, d, gk in samples:
        out.write('\n%s  %s\n' % (nm, ' '.join('%02X' % c for c in b)))
        for k in gk:
            out.write('   %-24s = %g\n' % (k, d[k]))
    out.close()
    print('eightbyte_out.txt total=%d has46=%d' % (total, has46))

if __name__ == '__main__':
    main()