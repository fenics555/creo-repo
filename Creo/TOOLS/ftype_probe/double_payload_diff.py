import os, struct, json, urllib.request, random

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
random.seed(7); random.shuffle(cands)

rows = []
for f in cands[:60]:
    try:
        sid = call('connection', 'connect')['sessionId']
        if call('file', 'open', sid, {'file': f})['status']['error']:
            continue
        pl = (call('parameter', 'list', sid, {'file': f}).get('data')
              or {}).get('paramlist') or []
        d = open(f + '.1', 'rb').read()
        for p in pl:
            if p.get('type') == 'STRING':
                continue
            try:
                v = float(p['value'])
            except Exception:
                continue
            be = struct.pack('>d', v)
            nb = p['name'].encode('utf-8')
            i = d.find(b'\xe3' + nb + b'\x00')
            if i < 0:
                continue
            win = d[i:i+70]
            hit = None
            for lead in range(0, 5):
                for trail in range(0, 9):
                    body = be[lead:8-trail] if 8-trail > lead else b''
                    if not body:
                        continue
                    j = win.find(body)
                    if j >= 0:
                        c = (win[j-1], lead, trail, len(body), j)
                        if hit is None or c[3] > hit[3]:
                            hit = c
            if not hit:
                continue
            tag, lead, trail, ln, j = hit
            if tag != 0x2F:
                continue
            left = win[max(0, j-9):j]
            right = win[j+ln:j+ln+6]
            rows.append((p['name'], v, be.hex(' ').upper(), left.hex(' ').upper(),
                         win[j:j+ln].hex(' ').upper(),
                         right.hex(' ').upper(), lead, trail, ln))
    except Exception:
        pass

seen = set()
print('=== записи с тегом 0x2F ===')
print('%-20s %-9s %-8s %-22s %-18s %s' % ('имя', 'знач', 'lead/trail', 'СЛЕВА от тега', 'payload', 'СПРАВА'))
for name, v, beh, left, pay, right, lead, trail, ln in rows:
    k = (name, v)
    if k in seen:
        continue
    seen.add(k)
    print('%-20s %-9.6g %d/%d/%d    %-22s %-18s %s'
          % (name[:20], v, lead, trail, ln, left, pay, right))

print()
print('=== уникальные значения при теге 0x2F ===')
uv = sorted(set(r[1] for r in rows))
print('значения:', ['%.10g' % x for x in uv])
print()
print('=== совпадают ли байты СЛЕВА для разных значений? ===')
lm = {}
for name, v, beh, left, pay, right, lead, trail, ln in rows:
    lm.setdefault(left, []).append(v)
for left, vs in lm.items():
    print('  %-28s -> значения: %s' % (left, ['%.8g' % x for x in sorted(set(vs))][:6]))