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
            left = win[max(0, j-12):j]
            hdr = left.hex(' ').upper()
            rows.append((lead, tag, v, be[:2].hex(' ').upper(), hdr,
                         p['name'], d.find(nb, 0)))
    except Exception:
        pass

print('ВСЕГО: %d' % len(rows))
print()
print('=== lead=2 (пропадают 2 байта): заголовок vs истинный be[0:2] ===')
corr = collections.defaultdict(set)
for lead, tag, v, be2, hdr, name, _ in rows:
    if lead != 2:
        continue
    corr[hdr].add(be2)
    print('  %-12s be[0:2]=%-7s tag=0x%02X  %-20s' % (be2, '', tag, name[:20]))

print()
print('=== УНИКАЛЬНЫЕ заголовки -> какие be[0:2] им соответствуют ===')
for h, s in corr.items():
    print('  %-38s -> %s' % (h, sorted(s)))

print()
print('=== ПОЛНЫЙ контекст слева (последние 12 б) ===')
for lead, tag, v, be2, hdr, name, _ in rows:
    if lead == 2:
        print('  be=%-7s tag=0x%02X  %s' % (be2, tag, hdr))