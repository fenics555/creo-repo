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

ok = bad = 0
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
                        c = (win[j-1], lead, trail, len(body))
                        if hit is None or c[3] > hit[3]:
                            hit = c
            if not hit:
                continue
            tag, lead, trail, ln = hit
            payload = be[lead:8-trail]
            # ДЕКОДЕР ПРЕДЛОЖЕНИЯ
            got = None
            if 0x55 <= tag <= 0x9F and len(payload) >= 6:
                got = struct.unpack('>d', b'\x40\x06' + payload[:6])[0]
            elif 0x23 <= tag <= 0x2D and len(payload) >= 7:
                got = struct.unpack('>d',
                    (b'\x40' if tag == 0x2D else b'\x3f') + payload[:7])[0]
            elif tag == 0xED and len(payload) >= 8:
                got = struct.unpack('>d', payload[:8])[0]
            elif tag == 0x2F and len(payload) >= 2:
                got = struct.unpack('>d',
                    b'\x40\x46' + payload[:2] + b'\x00' * 4)[0]
            if got is None:
                continue
            good = abs(got - v) < 1e-9 * max(1.0, abs(v))
            ok += good; bad += (not good)
            rows.append((good, tag, p['name'], v, got))
    except Exception:
        pass

print('ПРОВЕРЕНО: %d   ВЕРНО: %d   ОШИБОК: %d' % (ok + bad, ok, bad))
print()
print('%-6s %-22s %-20s %-20s' % ('ТЕГ', 'истинное', 'декодер дал', 'имя'))
for good, tag, name, v, got in sorted(rows, key=lambda r: r[0])[:18]:
    print('0x%02X %-3s %-22.12g %-20.12g %s'
          % (tag, 'ВЕРНО' if good else 'ОШИБ', v, got, name[:20]))
print()
print('первый байт оригинала у ОШИБОК:')
for good, tag, name, v, got in rows:
    if not good:
        print('  0x%02X  %-14.10g  be[0:2]=%s  %s'
              % (tag, v, struct.pack('>d', v)[:2].hex(' ').upper(), name[:18]))