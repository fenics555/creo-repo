# -*- coding: utf-8 -*-
"""Перекрестный поиск полей по набору файлов: где встречается feat_name/ftype/etc.
Запуск: python fieldhunt.py <файл1> [файл2 ...] [--bytes N]
Вывод: fieldhunt_out.txt
"""
import re, sys, io, os, glob

TARGETS = [b'feat_name', b'ft_type', b'ftype', b'feat_type', b'prev_feat_id',
           b'sort_feat_ids', b'feat_ids', b'pat_group_header_id', b'is_header',
           b'comp_type', b'created_features', b'MTTyped_CreateData', b'Sld_FeatTree',
           b'feat_tree', b'order_table', b'parchild_table', b'feat_num']

def expand(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for ext in ('*.prt.1', '*.asm.1', '*.drw.1'):
                out += glob.glob(os.path.join(p, '**', ext), recursive=True)
        elif os.path.isfile(p):
            out.append(p)
    return sorted(set(out))

def main():
    argv = sys.argv[1:]
    nb = 0
    if '--bytes' in argv:
        i = argv.index('--bytes')
        nb = int(argv[i + 1])
        del argv[i:i + 2]
    files = expand(argv)
    out = io.open('fieldhunt_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛОВ: %d\n' % len(files))
    table = {}
    for f in files:
        try:
            with open(f, 'rb') as fh:
                data = fh.read()
        except Exception as e:
            continue
        found = []
        for t in TARGETS:
            c = data.count(t)
            if c:
                found.append('%s=%d' % (t.decode(), c))
                table.setdefault(t.decode(), []).append((os.path.basename(f), c))
        out.write('%-46s %8d  %s\n' % (os.path.basename(f)[:46], len(data), ', '.join(found)))
    out.write('\n=== ИТОГ ПО ПОЛЯМ ===\n')
    for k, v in sorted(table.items(), key=lambda x: -sum(c for _, c in x[1])):
        out.write('\n%s : в %d файлах, всего %d\n' % (k, len(v), sum(c for _, c in v)))
        for nm, c in v[:8]:
            out.write('    %-40s %d\n' % (nm, c))
    out.close()
    print('fieldhunt_out.txt files=%d' % len(files))

if __name__ == '__main__':
    main()