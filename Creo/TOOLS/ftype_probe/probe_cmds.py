import json, urllib.request

def call(c, f, s=None, d=None):
    b = {'command': c, 'function': f}
    if s:
        b['sessionId'] = s
    b['data'] = d or {}
    r = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(b).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(r, timeout=60).read().decode('utf-8'))

M = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt'
s = call('connection', 'connect')['sessionId']
call('file', 'open', s, {'file': M})

d = call('dimension', 'list', s, {'file': M})['data']['dimlist']
print('РАЗМЕРОВ ВСЕГО: %d' % len(d))
for x in d[:24]:
    print('   %-5s = %s' % (x['name'], x['value']))

l = call('layer', 'list', s, {'file': M})['data']['layers']
print('СЛОЁВ: %s' % [(x['name'], x['id']) for x in l])

out = r'D:\AI\repo\Creo\TOOLS\ftype_probe\dims_137.json'
json.dump({'dims': d, 'layers': l}, open(out, 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('сохранено: %s' % out)

def call(cmd, fn, sid=None, data=None):
    b = {'command': cmd, 'function': fn}
    if sid is not None:
        b['sessionId'] = sid
    b['data'] = data or {}
    r = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(b).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(r, timeout=60).read().decode('utf-8'))

MODEL = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt'
sid = call('connection', 'connect')['sessionId']
print('open:', call('file', 'open', sid, {'file': MODEL})['status']['error'])
print()

print('=== ВСЕ ФУНКЦИИ у geometry / bom ===')
for c in ('geometry', 'bom'):
    for f in ('list', 'get', 'info', 'read', 'dump', 'mass', 'props',
              'properties', 'surface', 'measure', 'tree', 'count'):
        try:
            r = call(c, f, sid, {'file': MODEL})
            m = r.get('status', {}).get('message', 'OK')
            t = json.dumps(r.get('data'), ensure_ascii=False)
            print('  %s/%-11s %s' % (c, f, m[:40]))
            if t and t != 'null':
                print('      ДАННЫЕ: %s' % t[:300])
        except Exception as e:
            pass

print()
print('=== dimension/list и layer/list ===')
for c in ('dimension', 'layer'):
    r = call(c, 'list', sid, {'file': MODEL})
    t = json.dumps(r.get('data'), ensure_ascii=False)
    print('  %s/list -> %s' % (c, t[:600]))

def call(cmd, fn, sid=None, data=None):
    b = {'command': cmd, 'function': fn}
    if sid is not None:
        b['sessionId'] = sid
    b['data'] = data or {}
    r = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(b).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(r, timeout=30).read().decode('utf-8'))

CANDS = """file parameter feature connection session geometry geom solid mass
massprop mass_property property material unit units measure draw dimension
trail relation equation expr bom component member assembly part model tree
layer data info status version config system admin tool execute run script
macro print query export import save load create delete rename copy
list get set add remove find search check""".split()

FN = ['list', 'get']

known = set()
for c in CANDS:
    for f in FN:
        try:
            r = call(c, f)
            msg = r.get('status', {}).get('message', '')
            if 'Invalid command' in msg:
                break                      # команды нет — дальше не идём
            known.add('%s/%s' % (c, f))
            print('ЕСТЬ %-18s %s' % ('%s/%s' % (c, f), msg[:70]))
        except Exception as e:
            pass
print()
print('НАЙДЕНО комбинаций: %d' % len(known))
print(', '.join(sorted(known)))