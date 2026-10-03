# -*- coding: utf-8 -*-
"""ПРОВЕРКА ГИПОТЕЗЫ "E0 <len> <имя>00":
гипотеза A: байт после E0 = длина имени
гипотеза B: байт после E0 = код типа значения
Запуск: python checklen.py <файл>
"""
import re, sys, io, os, collections

def load(p):
    with open(p, 'rb') as f:
        return f.read()

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('checklen_out.txt', 'w', encoding='utf-8')
    hits = list(FIELD.finditer(data))
    out.write('FILE %s size=%d\nПолей найдено: %d\n\n' % (os.path.basename(path), len(data), len(hits)))

    agree = 0
    disagree = []
    for m in hits:
        code = m.group(1)[0]
        name = m.group(2)
        if code == len(name):
            agree += 1
        else:
            disagree.append((code, len(name), name.decode('ascii', 'replace')))

    out.write('ГИПОТЕЗА A (байт = длина имени):\n')
    out.write('  совпало: %d из %d\n' % (agree, len(hits)))
    out.write('  НЕ совпало: %d\n\n' % len(disagree))

    out.write('=== ПРИМЕРЫ НЕСОВПАДЕНИЙ (первые 40) ===\n')
    for code, L, nm in disagree[:40]:
        out.write('  E0 %02X  код=%d  длина_имени=%2d  %s\n' % (code, code, L, nm))

    out.write('\n=== ТАБЛИЦА: код типа -> длина имени -> примеры ===\n')
    tab = collections.defaultdict(list)
    for m in hits:
        code = m.group(1)[0]
        nm = m.group(2).decode('ascii', 'replace')
        tab[code].append((len(nm), nm))
    for code in sorted(tab):
        items = tab[code]
        lens = sorted(set(l for l, _ in items))
        out.write('\nКОД 0x%02X (%d)  встречается %d раз\n' % (code, code, len(items)))
        out.write('   длины имён: %s\n' % (lens[:14],))
        # какое значение идёт после имени
        ex = []
        for m in hits:
            if m.group(1)[0] == code:
                val = data[m.end():m.end() + 6]
                ex.append('%s -> %s' % (m.group(2).decode('ascii', 'replace'),
                                       ' '.join('%02X' % c for c in val)))
                if len(ex) >= 6:
                    break
        for e in ex:
            out.write('     %s\n' % e)
    out.close()
    print('checklen_out.txt fields=%d agree=%d disagree=%d' % (len(hits), agree, len(disagree)))

if __name__ == '__main__':
    main()