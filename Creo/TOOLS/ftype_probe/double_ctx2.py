import os, struct, json, urllib.request, random, collections

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

TAG = collections.defaultdict(set)
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
            # ищем(tag + суффикс BE) в окне
            hit = None
            for lead in range(0, 5):
                for trail in range(0, 9):
                    body = be[lead:8-trail] if 8-trail > lead else b''
                    if not body:
                        continue
                    j = win.find(body)
                    if j >= 0:
                        cand = (win[j-1], lead, trail, len(body))
                        if hit is None or cand[3] > hit[3]:
                            hit = cand
            if hit:
                tag, lead, trail, ln = hit
                TAG[(tag, lead, trail, ln)].add(round(v, 9))
                rows.append((tag, lead, trail, ln, v, p['name']))
    except Exception:
        pass

print('РАЗОБРАНО DOUBLE: %d' % len(rows))
print()
print('%-6s %-5s %-6s %-5s  %-22s %s' % ('ТЕГ', 'lead', 'trail', 'длина', 'пример', 'кол-во'))
agg = collections.Counter((t[0], t[1], t[2], t[3]) for t in TAG)
for k, c in agg.most_common():
    ex = list(TAG[k])[:2]
    print('0x%02X   %-5d %-6d %-5d  %-22s %d' % (k[0], k[1], k[2], k[3],
          ','.join('%.6g' % x for x in ex), c))
print()
tl = collections.defaultdict(set)
for (t, lead, trail, ln) in agg:
    tl[t].add((lead, trail, ln))
print('ТЕГ -> (lead,trail,длина):')
for t in sorted(tl):
    print('  0x%02X -> %s' % (t, sorted(tl[t])))