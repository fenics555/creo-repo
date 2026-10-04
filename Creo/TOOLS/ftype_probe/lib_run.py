import os, sys, json
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
from creo_full import read_model
from creo_tree_builder import build_tree

ROOT = r'Z:\PTC\CREO-START\Libraries'
files = []
for r, d, fs in os.walk(ROOT):
    for f in fs:
        if f.lower().endswith(('.prt.1', '.asm.1')):
            files.append(os.path.join(r, f))
print('ФАЙЛОВ В БИБЛИОТЕКЕ PTC: %d' % len(files))

OUT = r'D:\AI\repo\Creo\TOOLS\ftype_probe\plm_library.jsonl'
ok = ops = surf = bom = ru = feat = 0
trees = 0
with open(OUT, 'w', encoding='utf-8') as fh:
    for p in sorted(files):
        try:
            rec = read_model(p)
        except Exception:
            continue
        try:
            t, nodes, links, toc = build_tree(p)
            rec['tree'] = t
            rec['tree_nodes'] = len(nodes)
            trees += 1
        except Exception:
            rec['tree'] = []
            rec['tree_nodes'] = 0
        ok += 1
        ops += len(rec['operations'])
        surf += len(rec['surfaces'])
        bom += len(rec['bom'])
        ru += len(rec['cyrillic_params'])
        feat += len(rec['features'])
        fh.write(json.dumps(rec, ensure_ascii=False) + '\n')

print('ОБРАБОТАНО: %d (с деревом: %d)' % (ok, trees))
print('  операций      %d' % ops)
print('  поверхностей  %d' % surf)
print('  компонентов   %d' % bom)
print('  кириллицы     %d' % ru)
print('  имён фич      %d' % feat)
print('файл: %s' % OUT)

# пример дерева
for line in open(OUT, encoding='utf-8'):
    r = json.loads(line)
    if r.get('tree') and r['tree_nodes'] > 20:
        print()
        print('ДЕРОВО %s (%d узлов):' % (r['file'], r['tree_nodes']))

        def show(ns, d=0, lim=[0]):
            for n in ns:
                if lim[0] >= 12:
                    return
                lim[0] += 1
                print('%s%s [%s]' % ('  ' * d, n['name'][:32], n['type']))
                show(n['children'], d + 1, lim)
        show(r['tree'])
        break