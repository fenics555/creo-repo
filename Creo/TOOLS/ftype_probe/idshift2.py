import sys, os, re, urllib.request, json

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(req, timeout=180).read().decode('utf-8'))

F = r'Z:\PTC\Work\00080\00080-03.prt'
sid = call('connection', 'connect')['sessionId']
call('file', 'open', sid, {'file': F})
ET = call('feature', 'list', sid, {'file': F})['data']['featlist']
d = open(F + '.1', 'rb').read()

def dec_varint(b, i):
    b0 = b[i]
    if b0 & 0xC0 == 0x00:
        return b0, i + 1, 1
    if b0 & 0xC0 == 0x80:
        return ((b0 & 0x7F) << 8) | b[i+1], i + 2, 2
    return ((b0 & 0x3F) << 16) | (b[i+1] << 8) | b[i+2], i + 3, 3

print('=== ПОИСК ФОРМЫ: <имя>\\0 01 00 [18 E5] <varint> ===')
for x in ET:
    nm = x['name']; want = x['feat_id']
    nb = nm.encode('utf-8')
    found = []
    for m in re.finditer(re.escape(nb) + b'\x00', d):
        i = m.end()
        if d[i:i+2] != b'\x01\x00':
            continue
        j = i + 2
        if d[j:j+2] == b'\x18\xe5':
            j += 2
        try:
            val, nxt, ln = dec_varint(d, j)
        except Exception:
            continue
        found.append((hex(m.start()), val, ln, 'СОВПАЛ' if val == want else 'нет'))
    print('%-14s ожидаем ID %-4d -> %s' % (nm, want,
          ', '.join('ID=%d(%dб) %s @%s' % (v, l, st, o) for o, v, l, st in found) or 'НЕ НАЙДЕНО'))

print()
print('=== список 6 базовых плоскостей @0x3420c ===')
i = 0x34205
seg = d[i-40:i+120]
print(seg.hex(' ').upper())
print(repr(seg.decode('ascii', 'replace')))