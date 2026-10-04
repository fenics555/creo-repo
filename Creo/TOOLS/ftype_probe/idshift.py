import sys, os, urllib.request, json, re
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(req, timeout=180).read().decode('utf-8'))

dirs = [l.strip().strip('"') for l in
        open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
        if l.strip()]
cands = []
for dd in dirs:
    try:
        for f in os.listdir(dd):
            if f.lower().endswith('.prt.1'):
                cands.append(os.path.join(dd, f[:-2]))
    except Exception:
        pass

TARGET = None
for f in cands:
    try:
        sid = call('connection', 'connect')['sessionId']
        if call('file', 'open', sid, {'file': f})['status']['error']:
            continue
        fl = call('feature', 'list', sid, {'file': f}).get('data', {}) \
              .get('featlist') or []
        if len(fl) == 4:
            TARGET = (f, fl)
            break
    except Exception:
        pass

if not TARGET:
    print('модель с 4 фичами не найдена')
    raise SystemExit(1)

F, ET = TARGET
print('МОДЕЛЬ: %s' % F)
print('ЭТАЛОН:')
for x in ET:
    print('   ID %-6d %-16s %s' % (x['feat_id'], x['name'], x['type']))
print()

d = open(F + '.1', 'rb').read()
et = {x['name']: x['feat_id'] for x in ET}

# ищем КАЖДОЕ эталонное имя в файле и смотрим, что стоит рядом
for x in ET:
    nm = x['name']
    nb = nm.encode('utf-8')
    print('=== %s (эталонный ID %d) ===' % (nm, x['feat_id']))
    for m in re.finditer(re.escape(nb) + b'\x00', d):
        i = m.start()
        ctx = d[max(0, i - 10):i + len(nb) + 26]
        print('   @%-8s %s' % (hex(i), ctx.hex(' ').upper()))
    print()