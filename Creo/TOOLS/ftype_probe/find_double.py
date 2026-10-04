import urllib.request, json, os, random

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode('utf-8'))

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
random.seed(3); random.shuffle(cands)
print('найдено .prt в папках search.pro:', len(cands))

best = 0
scanned = 0
for f in cands[:45]:
    try:
        sid = call('connection', 'connect')['sessionId']
        o = call('file', 'open', sid, {'file': f})
        if o['status']['error']:
            continue
        scanned += 1
        pl = (call('parameter', 'list', sid, {'file': f}).get('data')
              or {}).get('paramlist') or []
        num = [p for p in pl if p.get('type') != 'STRING']
        if len(num) > best:
            best = len(num)
            print('>>> %-44s параметров=%d  НЕ-STRING=%d'
                  % (os.path.basename(f)[:44], len(pl), len(num)))
            for p in num[:6]:
                print('      %-20s %-8s %s' % (p['name'][:20], p['type'],
                                                 p.get('value')))
    except Exception:
        pass
print('открыто моделей: %d, максимум НЕ-STRING: %d' % (scanned, best))