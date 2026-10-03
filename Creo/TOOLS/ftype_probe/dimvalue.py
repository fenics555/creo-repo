# -*- coding: utf-8 -*-
"""ПЕРЕПИСЬ ЧИСЕЛ: все правдоподобные IEEE-754 значения в файле, оба эндиана.
Не гадаем номиналы — собираем факты: где лежат числа и какие они.
Запуск: python dimvalue.py <файл.prt.1> [проверить_значения: 10.0,1.5,...]
Вывод: dimvalue_out.txt
"""
import re, sys, io, os, struct, collections

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def plausible(v):
    if v != v or v in (float('inf'), float('-inf')):
        return False
    a = abs(v)
    return 0.01 <= a <= 1e6

def census(data, out):
    """Все 8-байтовые окна как BE-double, с фильтром правдоподобности."""
    hits = collections.defaultdict(list)      # значение -> позиции (BE)
    n = len(data)
    for i in range(n - 8):
        chunk = data[i:i + 8]
        v = struct.unpack('>d', chunk)[0]
        if plausible(v):
            hits[round(v, 6)].append(i)
    return hits

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('dimvalue_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n\n' % (os.path.basename(path), len(data)))

    # 1) конкретные значения из задания
    if len(sys.argv) > 2:
        out.write('=== ПРОВЕРКА КОНКРЕТНЫХ ЗНАЧЕНИЙ ===\n')
        for s in sys.argv[2].split(','):
            try:
                val = float(s)
            except ValueError:
                continue
            be = struct.pack('>d', val)
            le = struct.pack('<d', val)
            pb = [i for i in range(len(data) - 8) if data.startswith(be, i)]
            pl = [i for i in range(len(data) - 8) if data.startswith(le, i)]
            out.write('  %-8s BE: %-4d %s\n' % (val, len(pb), ['@%06X' % p for p in pb[:6]]))
            out.write('  %-8s LE: %-4d %s\n' % ('', len(pl), ['@%06X' % p for p in pl[:6]]))
        out.write('\n')

    # 2) перепись BE-double
    hits = census(data, out)
    out.write('=== ПЕРЕПИСЬ BE-double: %d уникальных правдоподобных значений ===\n' % len(hits))
    # только «инженерные» числа: целые и кратные 0.5/0.25 в разумном диапазоне
    nice = []
    for v, ps in hits.items():
        if 0.5 <= abs(v) <= 10000:
            r = v * 4
            if abs(r - round(r)) < 1e-9:      # кратно 0.25
                nice.append((v, len(ps), ps[:3]))
    nice.sort(key=lambda x: -x[1])
    out.write('кратных 0.25 в диапазоне 0.5..10000: %d\n\n' % len(nice))
    out.write('%-16s %6s  %s\n' % ('значение', 'раз', 'позиции'))
    for v, c, ps in nice[:60]:
        out.write('%-16s %6d  %s\n' % (('%g' % v), c, ', '.join('@%06X' % p for p in ps)))

    # 3) маркер перед самыми частыми
    out.write('\n=== ЧТО СТОИТ ПЕРЕД ЧИСЛАМИ (байт на 1 позицию назад) ===\n')
    mk = collections.Counter()
    for v, c, ps in nice[:60]:
        for p in ps:
            if p > 0:
                mk[data[p - 1]] += 1
    for b, c in mk.most_common(15):
        out.write('   маркер %02X : %d\n' % (b, c))

    out.close()
    print('dimvalue_out.txt uniq=%d nice=%d' % (len(hits), len(nice)))

if __name__ == '__main__':
    main()