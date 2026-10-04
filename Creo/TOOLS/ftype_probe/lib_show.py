import json

P = r'D:\AI\repo\Creo\TOOLS\ftype_probe\plm_library.jsonl'
rows = [json.loads(l) for l in open(P, encoding='utf-8')]

print('=== СБОРКИ С СОСТАВОМ ===')
n = 0
for r in rows:
    if r['bom'] and r['type'] == 'ASSEMBLY':
        print('%-28s %d: %s' % (r['file'][:28], len(r['bom']),
                                ', '.join(r['bom'][:6])))
        n += 1
        if n >= 10:
            break

print()
print('=== ДЕРЕВЬЯ (узлов > 15) ===')
n = 0
for r in rows:
    if r['tree_nodes'] > 15:
        print('%-28s узлов %d, корней %d'
              % (r['file'][:28], r['tree_nodes'], len(r['tree'])))
        n += 1
        if n >= 6:
            break

print()
print('=== ТИПЫ МОДЕЛЕЙ ===')
c = {}
for r in rows:
    c[r['type']] = c.get(r['type'], 0) + 1
print('   %s' % c)

print()
print('=== ПРИМЕР: сборка soldatik ===')
for r in rows:
    if 'soldatik' in r['file'] and r['type'] == 'ASSEMBLY':
        print('   BOM: %s' % r['bom'])
        print('   операций: %d, фич: %d' % (len(r['operations']), len(r['features'])))
        print('   кириллица: %s' % r['cyrillic_params'][:10])
        break