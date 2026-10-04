import os, sys, json, time
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
from bom_extract import extract_universal_bom

OUT = r'D:\AI\repo\Creo\TOOLS\ftype_probe\plm_export.jsonl'

dirs = [l.strip().strip('"') for l in
        open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
        if l.strip()]
asms = []
for dd in dirs:
    try:
        for f in os.listdir(dd):
            if f.lower().endswith('.asm.1'):
                asms.append(os.path.join(dd, f))
    except Exception:
        pass

print('СБОРОК К ПРОГОНУ: %d' % len(asms))
t0 = time.time()
stats = {'ASSEM_MFG': 0, 'СБ (прямые ссылки)': 0,
         'обёртка (@comp_ids)': 0, 'N/A': 0}
withbom = 0
total_comps = 0
lines = 0

with open(OUT, 'w', encoding='utf-8') as fh:
    for p in sorted(asms):
        try:
            d = open(p, 'rb').read()
        except Exception as e:
            print('  пропуск', p, e)
            continue
        bom, kind, note = extract_universal_bom(d, p)
        stats[kind] = stats.get(kind, 0) + 1
        if bom:
            withbom += 1
            total_comps += len(bom)
        rec = {
            "file": os.path.basename(p),
            "path": p,
            "kind": kind,
            "note": note,
            "component_count": len(bom),
            "bom": bom,
        }
        fh.write(json.dumps(rec, ensure_ascii=False) + '\n')
        lines += 1

print()
print('=== ИТОГ ===')
print('строк JSONL:      %d' % lines)
print('с ненулевым BOM:  %d' % withbom)
print('всего компонентов:%d' % total_comps)
print()
for k, v in sorted(stats.items(), key=lambda x: -x[1]):
    print('   %-26s %d' % (k, v))
print()
print('время: %.1f с' % (time.time() - t0))
print('файл: %s' % OUT)
print()
print('=== пример: сборки с BOM > 0 ===')
with open(OUT, encoding='utf-8') as fh:
    n = 0
    for line in fh:
        r = json.loads(line)
        if r['component_count'] > 1:
            print('   %-30s %d: %s' % (r['file'][:30], r['component_count'],
                                        ', '.join(r['bom'][:6])))
            n += 1
            if n >= 10:
                break