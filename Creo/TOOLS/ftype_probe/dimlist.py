# -*- coding: utf-8 -*-
"""СПИСОК РАЗМЕРОВ по именам: dim_name / dtl_named_item.
Размеры в детали позиционные, но ИМЕНА размеров читаются.
Запуск: python dimlist.py <файл.prt.1>
Вывод: dimlist_out.txt
"""
import re, sys, io, os, collections

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('dimlist_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n\n' % (os.path.basename(path), len(data)))

    total = 0
    for pat, label in ((rb'dim_name', 'dim_name'), (rb'dtl_named_item', 'dtl_named_item'),
                       (rb'\xE0\x0A dtl_item', 'dtl_item')):
        pat = pat.replace(b' ', b'')
        hits = list(re.finditer(re.escape(pat), data))
        out.write('=== %s : %d вхождений ===\n' % (label, len(hits)))
        for m in hits[:12]:
            p = m.end()
            seg = data[p:p + 40]
            out.write('  @%-9d %s\n' % (m.start(), ' '.join('%02X' % c for c in seg[:24])))
            asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in seg[:24])
            out.write('             %s\n' % asc)
        total += len(hits)
        out.write('\n')

    # имена вида dNNN / ДТ-* / размеры
    out.write('=== ИМЕНА РАЗМЕРОВ (dNNN и подобные) ===\n')
    names = collections.Counter(m.group(1).decode('ascii', 'replace')
                                for m in re.finditer(rb'([Dd]\d{1,4})(?![A-Za-z0-9])', data))
    for n, c in names.most_common(40):
        out.write('   %-12s x%d\n' % (n, c))

    # tol_class / tol_table_index — сколько их на файл
    for f in (b'tol_class', b'tol_table_index', b'digits', b'places_denom'):
        out.write('%-18s вхождений: %d\n' % (f.decode(), data.count(f)))
    out.close()
    print('dimlist_out.txt')

if __name__ == '__main__':
    main()