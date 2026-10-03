# -*- coding: utf-8 -*-
"""ГДЕ ЛЕЖАТ ДАННЫЕ РАЗМЕРОВ: ищем поля dim_* по всему файлу и печатаем секцию.
Запуск: python dimwhere.py <файл.prt.1>
"""
import re, sys, io, os

FIELDS = ['nominal_value', 'dim_type', 'digits', 'tol_class', 'override_value',
          'bound', 'places_denom', 'dim_array', 'dtl_named_item', 'dtl_item',
          'dim_dat_ptr', 'attach_ptr', 'parent_dim_id', 'symbol', 'dim_cosm_ptr']

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('dimwhere_out.txt', 'w', encoding='utf-8')

    secs = []
    for m in re.finditer(rb'\n#([A-Za-z_][A-Za-z0-9_]{2,30})[\r\n]', data):
        secs.append((m.end(), m.group(1).decode()))
    secs.sort()

    def sec_of(pos):
        cur = '(до секций)'
        for s, n in secs:
            if s <= pos:
                cur = n
            else:
                break
        return cur

    out.write('ФАЙЛ %s (%d байт)\n\n' % (os.path.basename(path), len(data)))
    out.write('%-18s %5s  %-22s %s\n' % ('поле', 'раз', 'секция', 'смещения'))
    for f in FIELDS:
        hits = [m.start() for m in re.finditer(f.encode(), data)]
        if not hits:
            out.write('%-18s %5d  %s\n' % (f, 0, '—'))
            continue
        seclist = collections_counter([sec_of(h) for h in hits])
        out.write('%-18s %5d  %-22s %s\n' % (
            f, len(hits), ', '.join('%s×%d' % (k, v) for k, v in seclist.items()),
            ', '.join('@%d' % h for h in hits[:6])))
    out.close()
    print('dimwhere_out.txt')

def collections_counter(pairs):
    import collections
    c = collections.Counter(pairs)
    return c.most_common(4)

if __name__ == '__main__':
    main()