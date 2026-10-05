"""Смоук-тест read_model: дерево из файла на 3 файлах и на выборке."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from creo_full import read_model

KEYS = (r'Z:\PTC\Work\00080\00080-03.prt.1',
        r'Z:\PTC\Work\00132\00132.prt.1',
        r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1')

for p in KEYS:
    if not os.path.exists(p):
        print('  НЕТ: %s' % p)
        continue
    r = read_model(p)
    ft = r.get('feature_tree_from_file')
    print('%-24s дерево=%s' % (os.path.basename(p), 'ЕСТЬ' if ft else 'нет'))
    if ft:
        print('      nodes=%s linked=%s иерарх=%s источник=%s'
              % (ft['nodes'], ft['linked'], ft['hierarchy'], ft.get('source')))
    print('      масса=%s объём=%s'
          % (r.get('mass_properties', {}) and r['mass_properties'].get('mass'),
             r.get('mass_properties', {}) and r['mass_properties'].get('volume')))

# выборка: сколько моделей в целом получают дерево
print('\n=== выборка по каталогам ===')
try:
    dirs = [l.strip().strip('"') for l in
            open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
            if l.strip()]
except Exception as e:
    dirs = []
    print('  search.pro недоступен: %s' % e)

models = []
for dd in dirs:
    try:
        for f in os.listdir(dd):
            if f.lower().endswith(('.prt.1', '.asm.1')):
                models.append(os.path.join(dd, f))
    except Exception:
        pass
print('  моделей найдено: %d' % len(models))
sample = models[::25][:40]
n_tree = n_all = 0
srcs = {}
for p in sample:
    try:
        r = read_model(p)
    except Exception:
        continue
    n_all += 1
    ft = r.get('feature_tree_from_file')
    if ft:
        n_tree += 1
        s = ft.get('source') or 'e3c0'
        srcs[s] = srcs.get(s, 0) + 1
print('  прочитано: %d | с деревом: %d | источники: %s'
      % (n_all, n_tree, srcs))
