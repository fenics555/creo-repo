import sys, os, re, collections
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
import creo_json as cj

F = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
d = open(F, 'rb').read()
print('ФАЙЛ: %s  (%d байт)' % (os.path.basename(F), len(d)))
print()

# === ЧИТАЕМ САМИ: все E3-объекты (имя + ID по форме A) ===
PAT = re.compile(rb'\xe3([A-Za-z_][A-Za-z0-9_\.]{2,40})\x00')

def dec_varint(b, i):
    b0 = b[i]
    if b0 & 0xC0 == 0x00:
        return b0, i + 1
    if b0 & 0xC0 == 0x80:
        return ((b0 & 0x7F) << 8) | b[i+1], i + 2
    return ((b0 & 0x3F) << 16) | (b[i+1] << 8) | b[i+2], i + 3

PAT = re.compile(rb'\xe3([A-Za-z_][A-Za-z0-9_\.]{2,40})\x00')
# ВАЖНО: после E3 идут 2 служебных байта, потом имя — или имя сразу.
# Ищем имя в любом случае, потом проверяем хвост.

def dec_varint(b, i):
    b0 = b[i]
    if b0 & 0xC0 == 0x00:
        return b0, i + 1
    if b0 & 0xC0 == 0x80:
        return ((b0 & 0x7F) << 8) | b[i+1], i + 2
    return ((b0 & 0x3F) << 16) | (b[i+1] << 8) | b[i+2], i + 3

feats = {}
for m in re.finditer(rb'([A-Za-z_][A-Za-z0-9_\.]{2,40})\x00', d):
    nm = m.group(1).decode('latin-1')
    if not re.match(r'^(DTM|PRT_|RIGHT|TOP|FRONT|LEFT|BACK|BOTTOM|LOCAL_GROUP|CO)', nm):
        continue
    i = m.end()
    if d[i:i+2] != b'\x01\x00':
        continue
    j = i + 2
    if d[j:j+2] == b'\x18\xe5':
        j += 2
    try:
        val, nxt = dec_varint(d, j)
    except Exception:
        continue
    feats.setdefault(nm, val)

print('=== ПРОЧИТАНО: %d имён с ID ===' % len(feats))
items = sorted(feats.items(), key=lambda x: x[1])
for nm, fid in items[:45]:
    print('   ID %-7d %s' % (fid, nm))
print('   ... всего %d' % len(items))
print()
print('=== DTM1 / DTM2 / RIGHT / TOP / FRONT ===')
for k in ('DTM1', 'DTM2', 'RIGHT', 'TOP', 'FRONT', 'PRT_CSYS_DEF'):
    print('   %-14s = %s' % (k, feats.get(k, 'НЕ НАЙДЕНО')))

print('=== ПРОЧИТАНО ФОРМОЙ A: %d уникальных имён ===' % len(feats))
print()

# группировка по типу имени
groups = collections.defaultdict(list)
for nm, fid in feats.items():
    if re.match(r'^(DTM|DAT|PLN)', nm):        groups['Datum (DTM/DAT/PLN)'].append(nm)
    elif nm.startswith('LOCAL_GROUP'):         groups['Group (LOCAL_GROUP)'].append(nm)
    elif nm in ('RIGHT','TOP','FRONT','BOTTOM','LEFT','BACK'):
                                                     groups['Базовая плоскость'].append(nm)
    elif 'CSYS' in nm:                         groups['Система координат'].append(nm)
    elif re.search(r'\d+$', nm) and re.match(r'^[A-Za-z]{2,4}', nm):
                                                     groups['Прочее с номером'].append(nm)
    else:                                      groups['Прочее'].append(nm)

for t in sorted(groups):
    v = groups[t]
    print('  %-24s %3d шт: %s' % (t, len(v), ', '.join(sorted(v)[:9])))
print()

print('=== ПОЛНЫЙ СПИСОК ПЕРВЫХ 60 ИМЁН С ID ===')
for k, (nm, fid) in enumerate(sorted(feats.items(), key=lambda x: x[1])[:60]):
    print('  ID %-7d %s' % (fid, nm))
print()

# сколько имён НЕ похоже на фичи (латиница, длина>2) — это реальные операции
print('=== ВСЕГО прочитано имён: %d ===' % len(feats))

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(req, timeout=180).read().decode('utf-8'))

# модель с РЕАЛЬНОЙ геометрией (26 фич по прошлому прогону)
for F in [r'Z:\PTC\Work\00080\00080-03.prt',
          r'Z:\PTC\Work\137.011.0041\137_011_0041.prt']:
    try:
        sid = call('connection', 'connect')['sessionId']
        if call('file', 'open', sid, {'file': F})['status']['error']:
            print('%s — не открылась' % F)
            continue
        ET = call('feature', 'list', sid, {'file': F})['data']['featlist']
        d = open(F + '.1', 'rb').read()
        got = cj.read_features(d)
        names = set(x[1] for x in got)
        ok = [x for x in ET if x['name'] in names]
        bad = [x for x in ET if x['name'] not in names]
        print('=' * 58)
        print('%s' % os.path.basename(F))
        print('  эталонных фич: %d' % len(ET))
        print('  НАЙДЕНО: %d   НЕ НАЙДЕНО: %d' % (len(ok), len(bad)))
        print()
        print('  --- ТИПЫ НАЙДЕННЫХ (доказательство, что не только плоскости) ---')
        import collections
        tc = collections.Counter(x['type'] for x in ok)
        for t, n in tc.most_common():
            print('     %-30s %d' % (t, n))
        print()
        print('  --- ПРИМЕРЫ НАЙДЕННЫХ ИМЁН ---')
        print('     ', ', '.join(x['name'] for x in ok[:14]))
        print()
        print('  --- НЕ НАЙДЕНЫ ---')
        for x in bad[:8]:
            print('     %-16s %-26s ID=%d' % (x['name'], x['type'], x['feat_id']))
        print()
    except Exception as e:
        print('%s — ошибка %s' % (F, e))