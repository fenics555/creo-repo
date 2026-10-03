# -*- coding: utf-8 -*-
"""Что реально значит байт после E0: ищем связь кода с формой значения.
Для каждого кода: распределение (первый байт значения) -> является ли строкой.
Запуск: python codetype.py <файл>
"""
import re, sys, io, os, collections

def load(p):
    with open(p, 'rb') as f:
        return f.read()

FIELD = re.compile(rb'([\xe0-\xff][\x00-\x0f])([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')
MARK = {0xF1, 0xF2, 0xF3, 0x0A, 0xF9, 0xF4, 0xF5}

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('codetype_out.txt', 'w', encoding='utf-8')
    hits = [(m.start(), m.end(), m.group(1)[0], m.group(1)[1], m.group(2).decode('ascii', 'replace'))
            for m in FIELD.finditer(data)]
    out.write('FILE %s полей=%d\n' % (os.path.basename(path), len(hits)))
    out.write('коды маркера: %s\n\n' % sorted(set('E0' if h[2] == 0xE0 else '%02X' % h[2] for h in hits)))

    # группируем по ПОЛНОМУ маркеру (E0 + код)
    tab = collections.defaultdict(lambda: {'n': 0, 'str': 0, 'names': collections.Counter(),
                                           'first': collections.Counter()})
    for k, (s, e, m1, code, nm) in enumerate(hits):
        key = '%02X/%02X' % (m1, code)
        v = data[e:e + 40]
        t = tab[key]
        t['n'] += 1
        t['names'][nm] += 1
        if v:
            t['first'][v[0]] += 1
        if v and v[0] in MARK:
            t['str'] += 1

    out.write('маркер/код  полей  %%строковых  первые байты значения            типичные имена\n')
    for key in sorted(tab, key=lambda x: -tab[x]['n']):
        t = tab[key]
        pct = 100.0 * t['str'] / t['n']
        fb = ', '.join('%02X:%d' % (b, c) for b, c in t['first'].most_common(5))
        nm = ', '.join('%s(%d)' % (a, b) for a, b in t['names'].most_common(6))
        out.write('%-9s %6d %6.1f%%  %-32s %s\n' % (key, t['n'], pct, fb, nm[:70]))
    out.close()
    print('codetype_out.txt')

if __name__ == '__main__':
    main()