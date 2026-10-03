# -*- coding: utf-8 -*-
"""ДИФФЕРЕНЦИАЛЬНЫЙ АНАЛИЗ feat_defs_*: ищем поле, которое РАЗЛИЧАЕТСЯ
между фичами ВНУТРИ одной модели (обязательное условие для FEATTYPE).
Метод: сравниваем байты блоков на ОДИНАКОВЫХ смещениях; если число 1..279
стоит на одном и том же смещении, но значения разные — это и есть кандидат.
Проверяем на 2 моделях: кандидат должен быть на одном смещении в обеих.
Запуск: python featdiff.py <файл> [файл2]
"""
import re, sys, io, os, collections

HEAD = re.compile(rb'\xF8.\xF7.\xFB\xE3\xE0\x01id\x00')
FEATDEF = re.compile(rb'feat_defs_([0-9]+)\x00')

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    out = io.open('featdiff_out.txt', 'w', encoding='utf-8')
    positions = {}
    for path in sys.argv[1:]:
        data = load(path)
        out.write('\n' + '=' * 76 + '\n%s\n' % os.path.basename(path) + '=' * 76 + '\n')
        heads = [m.start() for m in HEAD.finditer(data)]
        fdefs = [(m.start(), int(m.group(1))) for m in FEATDEF.finditer(data)]
        blocks = []
        for p, num in fdefs:
            h = None
            for hh in heads:
                if hh <= p + 40:
                    h = hh
                else:
                    break
            lo = h if h is not None else p
            nxt = None
            for hh in heads:
                if hh > lo:
                    nxt = hh
                    break
            end = nxt if nxt else min(len(data), lo + 8000)
            blocks.append((num, lo, data[lo:end]))

        out.write('блоков: %d  длины: %s\n'
                  % (len(blocks), [b[2].__len__() for b in blocks]))

        # кандидаты: смещение -> набор значений (только если >=3 блоков и >=2 разных)
        cand = collections.defaultdict(set)
        for num, lo, b in blocks:
            for i in range(len(b) - 1):
                v = b[i + 1]
                if 1 <= v <= 279 and b[i] in (0xE0, 0xE1, 0xE2, 0xE3, 0xF1, 0xF2):
                    cand[i].add(v)

        multi = {k: v for k, v in cand.items() if len(v) >= 2}
        out.write('смещений с РАЗНЫМИ значениями: %d\n' % len(multi))
        for off in sorted(multi)[:60]:
            out.write('  смещение %-6d значения: %s\n' % (off, sorted(multi[off])))
        positions[os.path.basename(path)] = {off: multi[off] for off in sorted(multi)}

        # показать контекст 5 самых ранних различающихся смещений
        out.write('\n--- КОНТЕКСТ первых 5 различающихся смещений ---\n')
        for off in sorted(multi)[:5]:
            out.write('\n  смещение %d:\n' % off)
            for num, lo, b in blocks[:6]:
                seg = b[max(0, off - 24):off + 24]
                out.write('    feat_defs_%-5d %s\n' % (num, ' '.join('%02X' % c for c in seg)))

    if len(positions) >= 2:
        out.write('\n' + '=' * 76 + '\nПЕРЕСЕЧЕНИЕ СМЕЩЕНИЙ (кандидат на обеих моделях)\n' + '=' * 76 + '\n')
        names = list(positions)
        a, b = positions[names[0]], positions[names[1]]
        common = set(a) & set(b)
        out.write('общих смещений: %d\n' % len(common))
        for off in sorted(common)[:40]:
            out.write('  смещение %-6d %s: %s | %s: %s\n'
                      % (off, names[0][:14], sorted(a[off]), names[1][:14], sorted(b[off])))
    out.close()
    print('featdiff_out.txt')

if __name__ == '__main__':
    main()