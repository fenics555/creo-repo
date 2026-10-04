import json

P = r'D:\AI\repo\Creo\TOOLS\ftype_probe\plm_final.jsonl'
for line in open(P, encoding='utf-8'):
    r = json.loads(line)
    if not r['file'].startswith('137_011_0041.prt'):
        continue
    print('ФАЙЛ      : %s  тип %s  Creo %s' % (r['file'], r['type'],
                                              r['creo_version']))
    print('РАЗМЕР    : %d байт,  секций: %d' % (r['size'], r['sections']))
    print('ТИПЫ      : %s' % r['type_counts'])
    print()
    print('ОПЕРАЦИИ (%d):' % len(r['operations']))
    for o in r['operations'][:10]:
        print('    %-24s %s' % (o['name'], o['type']))
    print()
    print('ПОВЕРХНОСТИ (%d):' % len(r['surfaces']))
    for s in r['surfaces'][:6]:
        print('    %-20s %-16s id %s' % (s['name'], s['kind'], s['id']))
    print()
    print('ИМЕНА ФИЧ (%d): %s' % (len(r['features']),
                                  ', '.join(r['features'][:12])))
    print()
    print('BOM (%d): %s' % (len(r['bom']), ', '.join(r['bom'][:8])))
    print()
    print('КИРИЛЛИЦА (%d): %s' % (len(r['cyrillic_params']),
                                  ', '.join(r['cyrillic_params'][:12])))
    break