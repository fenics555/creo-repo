import json, urllib.request, struct

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode('utf-8'))

MODEL = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
F = MODEL[:-2]
sid = call('connection', 'connect')['sessionId']
r = call('file', 'open', sid, {'file': F})
print('FULL RESPONSE:', json.dumps(r, ensure_ascii=False)[:900])
print('open error:', r['status']['error'])
pl = (call('parameter', 'list', sid, {'file': F}).get('data')
      or {}).get('paramlist') or []
d = open(MODEL, 'rb').read()

# извлекаем хвосты PRO_MP_* из файла
import re
tails = {}
for m in re.finditer(rb'\xe3(PRO_MP_[A-Z_0-9]{1,30})\x00', d):
    nm = m.group(1).decode('latin-1')
    win = d[m.end():m.end() + 30]
    tails[nm] = win

print('всего параметров: %d' % len(pl))
print('имена с PRO_MP:', [p['name'] for p in pl if 'PRO_MP' in p.get('name', '')])
print('все не-STRING:', [(p['name'], p.get('type'), p.get('value'))
                        for p in pl if p.get('type') != 'STRING'])
print()
print('PRO_MP_* в байтах файла:', sorted(set(
    m.group(1).decode('latin-1')
    for m in re.finditer(rb'\xe3(PRO_MP_[A-Z_0-9]{1,30})\x00', d))))
for p in pl:
    nm = p['name']
    if not nm.startswith('PRO_MP_') or p.get('type') == 'STRING':
        continue
    try:
        v = float(p['value'])
    except Exception:
        continue
    be = struct.pack('>d', v)
    tw = tails.get(nm)
    res = 'нет записи'
    if tw:
        hit = None
        for lead in range(0, 5):
            for trail in range(0, 9):
                body = be[lead:8 - trail] if 8 - trail > lead else b''
                if body and tw.find(body) >= 0:
                    if hit is None or len(body) > len(be[hit[0]:8 - hit[1]]):
                        hit = (lead, trail)
        if hit:
            lead, trail = hit
            ok = (lead == 0)
            res = 'lead=%d %s' % (lead, 'ПОЛНЫЙ' if ok else 'усечён')
        else:
            res = 'НЕ НАЙДЕНО'
    print('%-22s %-24.12g %-10s %-20s %s'
          % (nm[:22], v, be[:4].hex(' ').upper(),
             (tw[:10].hex(' ').upper() if tw else '-'), res))