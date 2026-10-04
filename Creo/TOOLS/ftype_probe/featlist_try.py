import urllib.request, json, os, re, struct, sys

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(req, timeout=120).read().decode('utf-8'))

# 1) полный список команд: шлём мусор
r = call('zzz', 'yyy')
print('=== ответ на мусорный запрос ===')
print(json.dumps(r, ensure_ascii=False)[:1200])
print()

# 2) feature:list на 137 — может закрыть дерево фич
F = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt'
sid = call('connection', 'connect')['sessionId']
print('=== открываем 137 ===')
print(json.dumps(call('file', 'open', sid, {'file': F}), ensure_ascii=False)[:300])
print()

res = call('feature', 'list', sid, {'file': F})
fl = res['data']['featlist']
print('эталонных фич: %d' % len(fl))
print('уникальных имён: %d' % len(set(x['name'] for x in fl)))
print()

# СВЕРКА с бинарным парсером
import sys
sys.path.insert(0, '.')
import creo_json as cj
d = open(F + '.1', 'rb').read()
got = cj.read_features(d)
byid = {}
for fid, nm, forma in got:
    byid.setdefault(fid, []).append(nm)

ok = 0
wrong = 0
miss = 0
for x in fl:
    fid = x['feat_id']
    if fid not in byid:
        miss += 1
        continue
    if x['name'] in byid[fid]:
        ok += 1
    else:
        wrong += 1

print('=== СВЕРКА бинарник vs CREOSON ===')
print('совпало по имени: %d' % ok)
print('НЕВЕРНОЕ имя:     %d' % wrong)
print('не найдено ID:     %d' % miss)
print()
print('=== примеры несовпадений ===')
n = 0
for x in fl:
    fid = x['feat_id']
    if fid in byid and x['name'] not in byid[fid]:
        print('  ID %-6d ожидали %-16s а в файле %s'
              % (fid, x['name'], byid[fid][:3]))
        n += 1
        if n >= 8:
            break

print()
print('=== ТИПЫ из etalona (уникальные) ===')
types = {}
for x in fl:
    types.setdefault(x['type'], []).append(x['name'])
for t, names in sorted(types.items()):
    print('  %-28s %d шт: %s' % (t, len(names), ', '.join(names[:4])))