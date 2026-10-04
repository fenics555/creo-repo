import json

P = r'D:\AI\repo\Creo\TOOLS\ftype_probe\plm_final.jsonl'
n = 0
for line in open(P, encoding='utf-8'):
    r = json.loads(line)
    if r['surfaces'] or (r['type'] == 'ASSEMBLY' and len(r['bom']) > 1):
        print('%-26s %-9s surf=%d bom=%d %s'
              % (r['file'][:26], r['type'], len(r['surfaces']),
                 len(r['bom']), [s['name'] for s in r['surfaces'][:3]]))
        if r['bom']:
            print('        BOM: %s' % r['bom'][:6])
        n += 1
        if n >= 10:
            break