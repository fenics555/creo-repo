# -*- coding: utf-8 -*-
"""ПУТЬ A: конец блока FeatDefs через цепочку F8-счётчиков.
КРИТЕРИЙ: на блоке предсказываем позицию следующего начала (FB E3 / F7 FB)
и сравниваем с ФАКТОМ. Сходится на 2 блоках подряд -> границы найдены.
⚠️ F8 перегружен: считаем попадания по ТИПАМ цели (FB, F7, E3), а не любым.
Запуск: python chainwalk.py <файл>
"""
import re, sys, io, os, collections

START = re.compile(rb'\xF8.\xF7.\xFB\xE3\xE0\x01id\x00')
SENSE = {0xFB: 'FB', 0xF7: 'F7', 0xE3: 'E3', 0xE0: 'E0', 0xF8: 'F8'}

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('chainwalk_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n' % (os.path.basename(path), len(data)))

    starts = [m.start() for m in START.finditer(data)]
    out.write('начал блоков: %d -> %s\n\n' % (len(starts), starts))
    if len(starts) < 2:
        out.write('мало блоков\n'); out.close(); return

    # берём блоки подряд (1-й и 2-й) и один большой (по границе секции)
    pairs = [(starts[i], starts[i + 1]) for i in range(len(starts) - 1)]
    pairs.sort(key=lambda p: p[1] - p[0], reverse=True)

    results = []
    for lo, hi in pairs[:3]:
        b = data[lo:hi]
        out.write('=' * 76 + '\nБЛОК @%d..%d  длина %d байт\n' % (lo, hi, len(b)) + '=' * 76 + '\n')

        # все F8 <N> внутри блока
        f8s = []
        i = 0
        while True:
            i = b.find(b'\xF8', i)
            if i < 0 or i + 1 >= len(b):
                break
            n = b[i + 1]
            if 1 <= n <= 200:
                f8s.append((i, n))
            i += 1
        out.write('вхождений F8<N> с 1<=N<=200: %d\n' % len(f8s))

        # проверка: конец по 2N и по N -> какой там байт
        res2N = collections.Counter()
        resN = collections.Counter()
        pred_ok = pred_bad = 0
        details = []
        for pos, n in f8s:
            e2 = pos + 2 + 2 * n
            e1 = pos + 2 + n
            b2 = b[e2] if e2 < len(b) else None
            b1 = b[e1] if e1 < len(b) else None
            res2N[SENSE.get(b2, '%02X' % b2 if b2 is not None else '--')] += 1
            resN[SENSE.get(b1, '%02X' % b1 if b1 is not None else '--')] += 1
            if b2 in SENSE:
                pred_ok += 1
            else:
                pred_bad += 1
            if len(details) < 14:
                details.append('   @%+-6d N=%-4d конец2N@%d=%s  конец1N@%d=%s'
                               % (pos, n, e2, SENSE.get(b2, '%02X' % b2 if b2 is not None else '--'),
                                  e1, SENSE.get(b1, '%02X' % b1 if b1 is not None else '--')))

        out.write('\nпервые совпадения:\n')
        for d in details:
            out.write(d + '\n')
        out.write('\nкуда попадает конец блока по 2N: %s\n' % dict(res2N.most_common(8)))
        out.write('куда попадает конец блока по 1N: %s\n' % dict(resN.most_common(8)))
        tot = max(1, pred_ok + pred_bad)
        out.write('\n>>> ПРЕДСКАЗАНИЕ по 2N: попало в маркер %d из %d = %.1f%%\n'
                  % (pred_ok, tot, 100.0 * pred_ok / tot))
        results.append((lo, hi, pred_ok, tot))
        out.write('\n')

    out.write('\n' + '=' * 76 + '\nИТОГ\n' + '=' * 76 + '\n')
    good = 0
    for lo, hi, ok, tot in results:
        pct = 100.0 * ok / max(1, tot)
        out.write('блок @%d (%d б): %.1f%%\n' % (lo, hi - lo, pct))
        if pct >= 90.0:
            good += 1
    out.write('\nблоков с >=90%% попаданием: %d из %d\n' % (good, len(results)))
    out.write('КРИТЕРИЙ УСПЕХА: >=2 блока подряд с >=90%%.\n')
    out.close()
    print('chainwalk_out.txt good=%d/%d' % (good, len(results)))

if __name__ == '__main__':
    main()