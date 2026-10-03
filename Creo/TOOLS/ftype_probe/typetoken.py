# -*- coding: utf-8 -*-
"""ТОКЕН ТИПА ОПЕРАЦИИ: 4 байта непосредственно перед "F7 29 E2 <имя>".
Если для разных типов операций эти байты РАЗНЫЕ и ПОВТОРЯЮТСЯ —
это внутренний идентификатор типа операции.
Запуск: python typetoken.py <файл>
Вывод: typetoken_out.txt
"""
import re, sys, io, os, collections

WORDS = ['Вытягивание', 'СКРУГЛЕНИЕ', 'Эскиз', 'Отверстие', 'Сечение',
         'Габарит', 'опорная', 'Датка', 'Скругление', 'ко']
MARK = b'\xF7\x29\xE2'

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('typetoken_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n\n' % (os.path.basename(path), len(data)))
    out.write('Гипотеза: 4 байта перед F7 29 E2 = токен типа операции\n')
    out.write('Проверка: одинаков ли токен внутри типа и РАЗНЫЙ ли между типами\n\n')

    table = {}
    for w in WORDS:
        pat = w.encode('utf-8')
        s = 0
        toks = collections.Counter()
        n = 0
        while True:
            i = data.find(pat, s)
            if i < 0:
                break
            s = i + 1
            # ищем ближайший F7 29 E2 перед именем (в пределах 64 байт)
            j = data.rfind(MARK, max(0, i - 64), i)
            if j < 0:
                continue
            tok = data[j - 4:j]
            toks[' '.join('%02X' % c for c in tok)] += 1
            n += 1
        if n:
            table[w] = (n, toks)

    for w, (n, toks) in table.items():
        top = ', '.join('%s ×%d' % (t, c) for t, c in toks.most_common(4))
        out.write('%-14s вхождений с F7 29 E2: %-4d  токены: %s\n' % (w, n, top))

    out.write('\n=== ВЕРДИКТ ===\n')
    if len(table) >= 2:
        names = list(table)
        common = None
        for w in names:
            s = set(table[w][1])
            common = s if common is None else (common & s)
        out.write('общий токен у ВСЕХ типов: %s\n' % (sorted(common) if common else 'ПУСТО -> токен РАЗНЫЙ'))
        for w in names:
            out.write('  %-14s уникальные токены: %s\n'
                      % (w, sorted(t for t in table[w][1] if t not in (common or set()))[:5]))
    out.close()
    print('typetoken_out.txt')

if __name__ == '__main__':
    main()