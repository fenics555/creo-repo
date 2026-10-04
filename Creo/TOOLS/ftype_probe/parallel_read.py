import urllib.request, json, re

def call(cmd, fn, sid=None, data=None):
    b = {'command': cmd, 'function': fn}
    if sid is not None:
        b['sessionId'] = sid
    b['data'] = data or {}
    r = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(b).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(r, timeout=180).read().decode('utf-8'))

MODEL = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt'
d = open(MODEL + '.1', 'rb').read()

# ---------- ПАРАЛЛЕЛЬНО: эталон из CREOSON ----------
sid = call('connection', 'connect')['sessionId']
call('file', 'open', sid, {'file': MODEL})
pl = (call('parameter', 'list', sid, {'file': MODEL}).get('data') or {}).get('paramlist') or []
fl = (call('feature', 'list', sid, {'file': MODEL}).get('data') or {}).get('featlist') or []
print('ЭТАЛОН CREOSON: параметров=%d  фич=%d' % (len(pl), len(fl)))
print('ФАЙЛ ПРОЧИТАН: %d байт\n' % len(d))

def where(text):
    b = text.encode('utf-8')
    return d.find(b)

# ---------- 1. ПАРАМЕТРЫ ----------
print('=' * 78)
print('1. ПАРАМЕТРЫ: эталон -> байты')
print('=' * 78)
pf = pm = 0
for p in pl:
    v = str(p.get('value', ''))
    if not v:
        continue
    i = where(v)
    if i >= 0:
        pf += 1
        print('  %-24s %-9s @%s' % (v[:24], p.get('type', ''), hex(i)))
    else:
        pm += 1
        print('  %-24s %-9s НЕ НАЙДЕН' % (v[:24], p.get('type', '')))
print('\n  найдено %d, не найдено %d' % (pf, pm))

# ---------- 2. ФИЧИ ----------
print()
print('=' * 78)
print('2. ФИЧИ: эталон -> байты')
print('=' * 78)
ff = fm = 0
nohit = []
for x in fl:
    i = where(x['name'])
    if i >= 0:
        ff += 1
    else:
        fm += 1
        nohit.append(x)
print('  найдено имён: %d из %d  (%.0f%%)' % (ff, len(fl), ff * 100.0 / max(1, len(fl))))
if nohit:
    print('  не найдено (первые 10):')
    for x in nohit[:10]:
        print('     ID %-7d %-18s %s' % (x['feat_id'], x['name'][:18], x['type']))

# ---------- 3. ТИПЫ ----------
print()
print('=' * 78)
print('3. ТИПЫ: русифицированный CREOSON -> английский код в файле')
print('=' * 78)
MAP = {'ОПОРНАЯ ПЛОСКОСТЬ': 'dtmplane', 'ЗАГОЛОВОК ГРУППЫ': 'group',
       'СИСТЕМА КООРДИНАТ': 'csys'}
seen = set()
for x in fl:
    t = x['type']
    if t in seen:
        continue
    seen.add(t)
    codes = []
    for c in (MAP.get(t, ''), t, t.upper()):
        if c:
            i = where(c)
            codes.append('%s=%s' % (c, hex(i) if i >= 0 else 'нет'))
    print('  %-26s %s' % (t, ' | '.join(c for c in codes if c)))

# ---------- 4. МАССА ----------
print()
print('=' * 78)
print('4. МАССА: сколько записей PRO_MP_MASS и разные ли они')
print('=' * 78)
offs = [m.start() for m in re.finditer(rb'PRO_MP_MASS', d)]
print('  вхождений PRO_MP_MASS: %d' % len(offs))
chunks = []
for o in offs:
    c = d[o + 10:o + 10 + 8]
    if c not in chunks:
        chunks.append(c)
print('  уникальных байтовых хвостов: %d' % len(chunks))
for c in chunks[:6]:
    print('     %s' % c.hex(' ').upper())
if len(chunks) > 1:
    print('  -> значения РАЗНЫЕ: масса пересчитывается, IEEE-754 не хранится')