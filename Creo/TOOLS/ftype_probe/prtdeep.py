# -*- coding: utf-8 -*-
"""ГЛУБОКАЯ ОБОЙМА ТОЛЬКО ПО ДЕТАЛЯМ (.prt).
Добавляем: int16 с масштабами, float32 с масштабированием, double в [-1..1],
и ОТДЕЛЬНЫЙ тест Granite ID (монотонность uint32).
Запуск: python prtdeep.py [папка] [N]
Вывод: prtdeep_out.txt
"""
import re, sys, io, os, random, struct, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)

def nice(v):
    if v is None or v != v:
        return False
    if not (0.001 <= abs(v) <= 1e5):
        return False
    r = v * 4
    return abs(r - round(r)) < 1e-9

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

    out = io.open('prtdeep_out.txt', 'w', encoding='utf-8')
    out.write('ГЛУБОКАЯ ОБОЙМА · ТОЛЬКО .prt · папка %s\n\n' % base)

    agg = collections.defaultdict(lambda: [0, 0])
    pairs = []                      # (файл, блоки uint32) для теста Granite
    silent_n = 0
    for fp in files:
        if len(pairs) >= N:
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
            if not (16 <= len(b) <= 200):
                continue
            if any(x in MARK3 for x in b):
                continue                # только «немые»
            mine.append(b)
        if not mine:
            continue
        silent_n += len(mine)
        out.write('  %-44s «немых»: %d\n' % (os.path.basename(fp)[:44], len(mine)))
        for b in mine:
            for o in range(0, len(b) - 7, 8):
                blk = b[o:o + 8]
                # 1) int16 с масштабами
                for s in (1e3, 1e4, 1e5):
                    for e, tag in (('>hhhh', 'BE'), ('<hhhh', 'LE')):
                        vals = [x / s for x in struct.unpack(e, blk)]
                        k = '4x_int16_%s /%g' % (tag, s)
                        agg[k][0] += len(vals)
                        agg[k][1] += sum(1 for v in vals if nice(v))
                # 2) float32 с масштабированием
                for m, mt in ((1, 'x1'), (10, 'x10'), (0.1, '/10')):
                    for e, tag in (('>ff', 'BE'), ('<ff', 'LE')):
                        vals = [x * m for x in struct.unpack(e, blk)]
                        k = '2x_float32_%s %s' % (tag, mt)
                        agg[k][0] += len(vals)
                        agg[k][1] += sum(1 for v in vals if nice(v))
                # 3) double в [-1..1]
                for e, tag in (('>d', 'BE'), ('<d', 'LE')):
                    x = struct.unpack(e, blk)[0]
                    k = 'double %s в[-1..1]' % tag
                    agg[k][0] += 1
                    if x == x and -1.0 <= x <= 1.0:
                        agg[k][1] += 1
                # 4) Granite ID
                pairs.append(struct.unpack('>II', blk))

    out.write('\n«НЕМЫХ» записей деталей обработано: %d\n' % silent_n)
    out.write('\n%-26s %10s %10s %8s\n' % ('ПРОЧТЕНИЕ', 'значений', 'красивых', '%'))
    out.write('-' * 60 + '\n')
    for k, (tot, n) in sorted(agg.items(), key=lambda x: -x[1][1] / max(1, x[1][0]))[:16]:
        out.write('%-26s %10d %10d %7.1f %%\n' % (k, tot, n, 100.0 * n / max(1, tot)))

    # --- Granite ID: монотонность ---
    out.write('\n=== ТЕСТ GRANITE ID (монотонность uint32) ===\n')
    out.write('блоков: %d\n' % len(pairs))
    mono1 = sum(1 for a, b in zip(pairs, pairs[1:]) if b[0] - a[0] == 1)
    mono1b = sum(1 for a, b in zip(pairs, pairs[1:]) if b[1] - a[1] == 1)
    inc = sum(1 for a, b in zip(pairs, pairs[1:]) if b[0] > a[0])
    dec = sum(1 for a, b in zip(pairs, pairs[1:]) if b[0] < a[0])
    out.write('  возрастают по первому: %d из %d\n' % (inc, max(1, len(pairs) - 1)))
    out.write('  убывают по первому:   %d\n' % dec)
    out.write('  шаг ровно +1 (поле1): %d\n' % mono1)
    out.write('  шаг ровно +1 (поле2): %d\n' % mono1b)
    out.write('\nпервые 16 пар uint32:\n')
    for a, b in zip(pairs, pairs[1:16]):
        out.write('   %10d %10d -> %10d %10d\n' % (a[0], a[1], b[0], b[1]))
    out.close()
    print('prtdeep_out.txt silent=%d pairs=%d' % (silent_n, len(pairs)))

if __name__ == '__main__':
    main()