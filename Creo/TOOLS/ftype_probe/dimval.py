# -*- coding: utf-8 -*-
"""Снятие ЗНАЧЕНИЙ из записи размера: F1 18, E3 ... F8 02 0C 00 0C 9A.
Собираем ВСЕ записи nominal_value из файла и проверяем гипотезы:
  Г1: после nominal_value идёт 1-байтовое число (маркер F1/18...)
  Г2: это упакованное число 2^(E+1)*(1+F/4096)
  Г3: это BE-double
Запуск: python dimval.py <файл.prt.1>
Вывод: dimval_out.txt
"""
import re, sys, io, os, struct, collections

def packed(e, f):
    return 2 ** (e + 1) * (1 + f / 4096.0)

def main():
    path = sys.argv[1]
    data = open(path, 'rb').read()
    out = io.open('dimval_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n\n' % (os.path.basename(path), len(data)))

    rows = []
    for m in re.finditer(rb'\xE0\x02nominal_value\x00', data):
        p = m.end()
        tail = data[p:p + 16]
        rows.append((m.start(), tail))

    out.write('ЗАПИСЕЙ nominal_value: %d\n\n' % len(rows))
    out.write('%-10s %-3s %-24s %-12s %-12s %s\n'
              % ('смещение', 'марк', '16 байт после', 'как 1-байт', 'как упаков.', 'как double'))
    g1 = collections.Counter()
    g2 = collections.Counter()
    g3 = collections.Counter()
    for pos, tail in rows[:40]:
        mark = tail[0]
        b1 = mark
        # Г1: однобайтовое значение = tail[1]
        v1 = tail[1] if len(tail) > 1 else None
        # Г2: упакованное из 3 байт после маркера
        v2 = None
        if len(tail) > 3 and (tail[1] & 0xF0):
            e = (tail[1] & 0xF0) >> 4
            f = ((tail[1] & 0x0F) << 8) | tail[2]
            v2 = packed(e, f)
        # Г3: BE-double
        v3 = None
        if len(tail) > 9:
            try:
                d = struct.unpack('>d', tail[1:9])[0]
                if 1e-6 < abs(d) < 1e7:
                    v3 = d
            except Exception:
                pass
        if v1 is not None:
            g1[v1] += 1
        if v2:
            g2[round(v2, 4)] += 1
        if v3:
            g3[round(v3, 4)] += 1
        out.write('%-10d %-3s %-24s %-12s %-12s %s\n' % (
            pos, '%02X' % mark, ' '.join('%02X' % c for c in tail[:10]),
            v1 if v1 is not None else '-',
            ('%.4f' % v2) if v2 else '-',
            ('%.4f' % v3) if v3 else '-'))

    out.write('\n=== Г1: значения «как 1-байтовое» (частые) ===\n')
    for v, c in g1.most_common(12):
        out.write('   %-8s x%d\n' % (v, c))
    out.write('\n=== Г2: значения «как упакованное» (частые) ===\n')
    for v, c in g2.most_common(12):
        out.write('   %-10.4f x%d\n' % (v, c))
    out.write('\n=== Г3: значения «как BE-double» (частые) ===\n')
    for v, c in g3.most_common(12):
        out.write('   %-12.4f x%d\n' % (v, c))
    out.close()
    print('dimval_out.txt rows=%d' % len(rows))

if __name__ == '__main__':
    main()