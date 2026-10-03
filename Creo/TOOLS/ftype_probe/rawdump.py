# -*- coding: utf-8 -*-
"""ЧИСТЫЙ HEX-ДАМП: 32 байта ДО имени фичи + имя + 32 байта ПОСЛЕ.
Без всякой интерпретации тегов — только байты.
Запуск: python rawdump.py <файл> [--n32] [--words Вытягивание,СКРУГЛЕНИЕ]
Вывод: rawdump_out.txt
"""
import re, sys, io, os

CYR = {  # utf-8 слова фич
    'Вытягивание': 'Вытягивание',
    'СКРУГЛЕНИЕ': 'СКРУГЛЕНИЕ',
    'Эскиз': 'Эскиз',
    'Отверстие': 'Отверстие',
    'Сечение': 'Сечение',
    'Габарит': 'Габарит',
    'опорная': 'опорная',
}

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def hx(b):
    return ' '.join('%02X' % c for c in b)

def ascii_(b):
    return ''.join(chr(c) if 32 <= c < 127 else '.' for c in b)

def main():
    path = sys.argv[1]
    n = 32
    if '--n' in sys.argv:
        n = int(sys.argv[sys.argv.index('--n') + 1])
    words = list(CYR.keys())
    if '--words' in sys.argv:
        i = sys.argv.index('--words') + 1
        words = sys.argv[i].split(',')

    data = load(path)
    out = io.open('rawdump_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ: %s  размер %d байт\n' % (os.path.basename(path), len(data)))
    out.write('Окно: %d байт ДО + имя + %d байт ПОСЛЕ\n\n' % (n, n))

    for w in words:
        pat = CYR.get(w, w).encode('utf-8')
        pos = []
        s = 0
        while True:
            i = data.find(pat, s)
            if i < 0:
                break
            pos.append(i)
            s = i + 1
        out.write('#' * 78 + '\n# СЛОВО: %s   вхождений: %d\n' % (w, len(pos)) + '#' * 78 + '\n')
        for k, i in enumerate(pos[:6], 1):
            lo = max(0, i - n)
            hi = min(len(data), i + len(pat) + n)
            before = data[lo:i]
            name = data[i:i + len(pat)]
            after = data[i + len(pat):hi]
            out.write('\n--- #%d  «%s» @%d (0x%X) ---\n' % (k, w, i, i))
            out.write('  ДО   (%2d б): %s\n' % (len(before), hx(before)))
            out.write('       ascii: %s\n' % ascii_(before))
            out.write('  ИМЯ  (%2d б): %s\n' % (len(name), hx(name)))
            out.write('       текст: %s\n' % name.decode('utf-8', 'replace'))
            out.write('  ПОСЛЕ(%2d б): %s\n' % (len(after), hx(after)))
            out.write('       ascii: %s\n' % ascii_(after))
        out.write('\n')

    # ПРОВЕРКА СЛЕДА ВЛАДЕЛЬЦА: ID 1143-1150 как 2 байта
    out.write('\n' + '#' * 78 + '\n# ПРОВЕРКА: ID 1143-1150 в двух представлениях\n' + '#' * 78 + '\n')
    out.write('# 1143 = 0x0477 | 1145 = 0x0479 | 1150 = 0x047E\n')
    out.write('# BE: 77 04 / 79 04 / 7E 04   LE: 04 77 / 04 79 / 04 7E\n\n')
    for label, pat in (('BE 77 04', b'\x77\x04'), ('BE 79 04', b'\x79\x04'),
                       ('LE 04 77', b'\x04\x77'), ('LE 04 79', b'\x04\x79'),
                       ('BE 7E 04', b'\x7E\x04'), ('LE 04 7E', b'\x04\x7E')):
        out.write('  %s : %d вхождений\n' % (label, data.count(pat)))

    # ищем их рядом с именами фич
    out.write('\n--- Вхождения 77 04 / 79 04 рядом с именами фич (±64 байта) ---\n')
    allnames = []
    for w in words:
        pat = CYR.get(w, w).encode('utf-8')
        s = 0
        while True:
            i = data.find(pat, s)
            if i < 0:
                break
            allnames.append((i, w))
            s = i + 1
    for label, pat in (('77 04', b'\x77\x04'), ('79 04', b'\x79\x04')):
        s = 0
        hits = []
        while True:
            i = data.find(pat, s)
            if i < 0:
                break
            s = i + 1
            for np, w in allnames:
                if abs(np - i) <= 64:
                    hits.append((i, w, np - i))
        out.write('\n  %s: %d вхождений, из них %d рядом с именем фичи\n'
                  % (label, data.count(pat), len(hits)))
        for i, w, d in hits[:10]:
            out.write('     %s @%d  (имя «%s» в %+d байтах)\n' % (label, i, w, d))
    out.close()
    print('rawdump_out.txt')

if __name__ == '__main__':
    main()