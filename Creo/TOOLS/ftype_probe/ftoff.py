# -*- coding: utf-8 -*-
"""ЧИСТО ОФЛАЙН: собирает ВСЕ вхождения ft_type рядом с именами фич
и проверяет главное — группируются ли значения ПО ТИПУ ОПЕРАЦИИ.
Если да -> это FEATTYPE, CREOSON не нужен.
Если нет -> ft_type не является типом операции.
Запуск: python ftoff.py <файл.prt.1>
Вывод: ftoff_out.txt
"""
import re, sys, io, os, collections

CYR = ['Вытягивание', 'СКРУГЛЕНИЕ', 'Скругление', 'Эскиз', 'Отверстие',
       'Сечение', 'Габарит', 'опорная', 'Отверстие', 'Вытягивание']

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('ftoff_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n' % (os.path.basename(path), len(data)))
    out.write('ВОПРОС: значения ft_type группируются по типу операции?\n\n')

    # 1) все вхождения ft_type в файле
    hits = [m.start() for m in re.finditer(rb'ft_type\x00', data)]
    out.write('всего вхождений "ft_type\\x00": %d\n' % len(hits))
    for p in hits:
        v = data[p + 8:p + 12]
        out.write('   @%-9d после: %s\n' % (p, ' '.join('%02X' % c for c in v)))
    out.write('\n')

    # 2) имена фич рядом (окно 96 байт)
    names = []
    for w in set(CYR):
        pat = w.encode('utf-8')
        s = 0
        while True:
            i = data.find(pat, s)
            if i < 0:
                break
            names.append((i, w))
            s = i + 1
    out.write('имён фич найдено: %d\n' % len(names))

    rows = []
    for p in hits:
        lo, hi = max(0, p - 96), min(len(data), p + 96)
        near = [n for n in names if lo <= n[0] <= hi]
        val = data[p + 8]
        out.write('\nft_type @%d  значение=%d (0x%02X)\n' % (p, val, val))
        out.write('   hex: %s\n' % ' '.join('%02X' % c for c in data[p - 24:p + 32]))
        if near:
            for n in near[:3]:
                out.write('   рядом имя: «%s» @%d (сдвиг %+d)\n' % (n[1], n[0], n[0] - p))
                rows.append((n[1], val))
        else:
            out.write('   рядом имён фич НЕТ\n')

    # 3) ВЕРДИКТ
    out.write('\n' + '=' * 70 + '\nГРУППИРОВКА: тип операции -> значения ft_type\n' + '=' * 70 + '\n')
    g = collections.defaultdict(collections.Counter)
    for w, v in rows:
        g[w][v] += 1
    for w in sorted(g):
        vals = g[w]
        mark = ' КОНСТАНТА' if len(vals) == 1 else ' РАЗНЫЕ'
        out.write('  %-14s %s%s\n' % (w, dict(vals), mark))
    if not rows:
        out.write('  НЕТ ДАННЫХ: ft_type не найден рядом с именами фич.\n')
    out.close()
    print('ftoff_out.txt')

if __name__ == '__main__':
    main()