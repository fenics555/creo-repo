# -*- coding: utf-8 -*-
"""ТЕСТ «БОЛЬШИХ КООРДИНАТ» Float32 — без сита кратности.
Идея: реальные координаты НЕ обязаны быть кратны 0.25 (14273.815 — нормальное число).
Поэтому здесь критерий другой: доля значений, попавших в ПРОМЫШЛЕННЫЙ диапазон
[1000 .. 50000] мм. Случайный float32 туда попадает крайне редко.
Запуск: python bigcoord.py [папка] [N]
Вывод: bigcoord_out.txt
"""
import re, sys, io, os, random, struct, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            lf = f.lower()
            if lf.endswith('.prt.1') or lf.endswith('.prt'):
                files.append(os.path.join(root, f))
        if len(files) > 30000:
            break
    random.seed(11)
    random.shuffle(files)

    out = io.open('bigcoord_out.txt', 'w', encoding='utf-8')
    out.write('ТЕСТ БОЛЬШИХ КООРДИНАТ (float32) · ТОЛЬКО .prt\n')
    out.write('критерий: доля значений в диапазоне [1000..50000] мм\n\n')

    tot = collections.Counter()
    ranges = {}
    used = 0
    for fp in files:
        if used >= N:
            break
        try:
            data = open(fp, 'rb').read()
        except Exception:
            continue
        if b'crv_pnt_arr' not in data:
            continue
        hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
                for m in FIELD.finditer(data)]
        mine = []
        for i, (pos, nm, end) in enumerate(hits):
            if nm != 'crv_pnt_arr':
                continue
            nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            b = data[end + 3:nxt]
            if 16 <= len(b) <= 200 and not any(x in MARK3 for x in b):
                mine.append(b)
        if not mine:
            continue
        used += 1
        vals_be, vals_le = [], []
        for b in mine:
            for o in range(0, len(b) - 7, 8):
                blk = b[o:o + 8]
                x, y = struct.unpack('>ff', blk)
                vals_be.extend([x, y])
                x, y = struct.unpack('<ff', blk)
                vals_le.extend([x, y])
        tot['BE всего'] += len(vals_be)
        tot['BE в диапазоне'] += sum(1 for v in vals_be if 1000 <= abs(v) <= 50000)
        tot['BE конечные'] += sum(1 for v in vals_be if v == v and abs(v) < 1e30)
        tot['LE всего'] += len(vals_le)
        tot['LE в диапазоне'] += sum(1 for v in vals_le if 1000 <= abs(v) <= 50000)
        tot['LE конечные'] += sum(1 for v in vals_le if v == v and abs(v) < 1e30)
        good = sorted(abs(v) for v in vals_be if 1000 <= abs(v) <= 50000)
        if good:
            ranges[os.path.basename(fp)] = good
        out.write('  %-40s значений %d, в диапазоне %d\n'
                  % (os.path.basename(fp)[:40], len(vals_be),
                     sum(1 for v in vals_be if 1000 <= abs(v) <= 50000)))

    out.write('\n=== СВОДКА ===\n')
    for tag in ('BE', 'LE'):
        t = tot[tag + ' всего']
        g = tot[tag + ' в диапазоне']
        f = tot[tag + ' конечные']
        out.write('  float32 %s: всего %d, конечных %d, в [1000..50000] %d = %.1f %%\n'
                  % (tag, t, f, g, 100.0 * g / max(1, t)))
    out.write('\n(случайные float32 в этот диапазон попадают единицы процентов;\n')
    out.write(' много значений подряд = реальные координаты)\n')

    out.write('\n=== ЗНАЧЕНИЯ ПО ФАЙЛАМ ===\n')
    for nm, g in ranges.items():
        out.write('\n%s (%d значений):\n   %s\n'
                  % (nm, len(g), ', '.join('%.1f' % v for v in g[:24])))
    out.close()
    print('bigcoord_out.txt files=%d' % used)

if __name__ == '__main__':
    main()