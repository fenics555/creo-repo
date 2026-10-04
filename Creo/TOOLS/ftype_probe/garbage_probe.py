import re

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