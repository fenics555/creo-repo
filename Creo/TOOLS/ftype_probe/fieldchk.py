# -*- coding: utf-8 -*-
"""Проверка полей чертежа: существуют ли mdl_id/mdl_name/mdl_type и где.
Аргумент — файл. Аргументы берутся из sys.argv, поэтому кириллица в пути
не искажается (в отличие от cmd -c).
"""
import sys

FIELDS = ['mdl_id', 'mdl_name', 'mdl_type', 'from_mdl_name', 'to_mdl_name',
          'comp_type', 'feat_name', 'Dwg_Models', 'rel_model_name']

data = open(sys.argv[1], 'rb').read()
print('РАЗМЕР ФАЙЛА: %d байт' % len(data))
print('максимальное допустимое смещение: %06X\n' % len(data))
for f in FIELDS:
    n = data.count(f.encode('ascii'))
    first = data.find(f.encode('ascii'))
    pos = ('@%06X' % first) if n else '-'
    print('  %-16s вхождений %-4d первое %s' % (f, n, pos))