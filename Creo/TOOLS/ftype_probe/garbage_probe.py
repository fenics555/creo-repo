import re

P = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
d = open(P, 'rb').read()
print('ФАЙЛ 137_011_0041.prt.1 (%d байт)\n' % len(d))

# НАСТОЯЩИЙ маркер: E0 <hexlen> <поле>\0 <hexlen> <значение>\0
FIELD = re.compile(
    rb'[E0F1E1]\s?[0-9A-Fa-f]{1,3}\s([A-Za-z_][A-Za-z0-9_]{2,30})\x00'
    rb'(?:[0-9A-Fa-f]{1,3}\s)?')

recs = []
for m in FIELD.finditer(d[:400000]):
    pos = m.end()
    # читаем значение до NUL
    val = re.match(rb'[^\x00]{1,80}\x00', d[pos:pos + 90])
    if not val:
        continue
    raw = val.group(0)[:-1]
    if not raw:
        continue
    try:
        s = raw.decode('utf-8')
    except UnicodeDecodeError:
        s = raw.decode('latin-1')
    recs.append((m.group(1).decode(), s))

print('НАЙДЕНО ЗАПИСЕЙ ПОЛЕЙ: %d\n' % len(recs))
seen = set()
for f, v in recs:
    if f in seen:
        continue
    seen.add(f)
    print('  %-18s = %r' % (f, v[:60]))
print()

print('=== КИРИЛЛИЦА ЧЕРЕЗ ПРАВИЛЬНЫЕ ПОЛЯ ===')
for f, v in recs:
    if max(v.encode('utf-8', 'ignore')) > 127:
        print('  %-18s = %r' % (f, v[:60]))

P = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
d = open(P, 'rb').read()
print('ФАЙЛ 137_011_0041.prt.1 (%d байт)\n' % len(d))

# МОЯ СТАРАЯ РЕГУЛЯРКА (даёт мусор)
OLD = re.compile(rb'\xe3([A-Za-z\xd0-\xd1][^\x00]{1,40})\x00')

print('=== 5 примеров "мусора" из моей выборки ===')
n = 0
for m in OLD.finditer(d):
    raw = m.group(1)
    if max(raw) <= 127:
        continue          # только кириллица
    print('\n--- смещение %s ---' % hex(m.start()))
    print('  МОЙ ЗАХВАТ : %r' % raw.decode('utf-8', 'replace'))
    print('  БАЙТЫ      : %s' % raw.hex(' ').upper())
    # что реально лежит НЕПОСРЕДСТВЕННО перед кириллицей?
    i = 0
    while i < len(raw) and raw[i] < 0x80:
        i += 1
    if i < len(raw):
        print('  ДО КИРИЛЛИЦЫ (хвост прошлого поля): %r / %s'
              % (raw[:i].decode('utf-8', 'replace'), raw[:i].hex(' ').upper()))
        print('  САМО ИМЯ (с кириллицы): %r' % raw[i:].decode('utf-8', 'replace'))
    n += 1
    if n >= 5:
        break