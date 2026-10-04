import urllib.request, json, re, os

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(req, timeout=180).read().decode('utf-8'))

MODEL = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt'
FILE = MODEL + '.1'

sid = call('connection', 'connect')['sessionId']
print('open:', call('file', 'open', sid, {'file': MODEL})['status']['error'])

pl = (call('parameter', 'list', sid, {'file': MODEL}).get('data')
      or {}).get('paramlist') or []
fl = (call('feature', 'list', sid, {'file': MODEL}).get('data')
      or {}).get('featlist') or []

print('ЭТАЛОН: параметров=%d, фич=%d' % (len(pl), len(fl)))
print()

d = open(FILE, 'rb').read()
print('ФАЙЛ: %d байт\n' % len(d))


def find_bytes(text):
    """Ищем строку в байтах файла как UTF-8 и как latin-1."""
    hits = []
    for enc in ('utf-8', 'utf-16-le'):
        try:
            b = text.encode(enc)
        except Exception:
            continue
        i = d.find(b)
        if i >= 0:
            hits.append((enc, i))
    return hits


print('%-26s %-12s %-34s %s' % ('ЗНАЧЕНИЕ', 'ТИП', 'НАЙДЕНО В БАЙТАХ', 'СМЕЩЕНИЕ'))
print('-' * 90)
found = 0
miss = 0
for p in pl:
    v = str(p.get('value', ''))
    if not v:
        continue
    h = find_bytes(v)
    if h:
        found += 1
        print('%-26s %-12s %-34s %s' % (v[:26], p.get('type', ''),
                                        ','.join(e for e, _ in h),
                                        ','.join(hex(i) for _, i in h[:3])))
    else:
        miss += 1
        print('%-26s %-12s %-34s' % (v[:26], p.get('type', ''), '*** НЕТ ***'))
print()
print('НАЙДЕНО: %d   НЕ НАЙДЕНО: %d' % (found, miss))

print()
print('=== ФИЧИ: имена ищутся в байтах? ===')
ff = 0
fm = 0
for x in fl[:20]:
    h = find_bytes(x['name'])
    if h:
        ff += 1
        print('  ID %-7d %-16s %-22s %s'
              % (x['feat_id'], x['name'][:16], ','.join(e for e, _ in h),
                 ','.join(hex(i) for _, i in h[:2])))
    else:
        fm += 1
        print('  ID %-7d %-16s НЕТ' % (x['feat_id'], x['name'][:16]))
print()
print('фич первых 20: найдено %d, не найдено %d' % (ff, fm))