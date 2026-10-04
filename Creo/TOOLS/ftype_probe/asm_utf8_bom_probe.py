import os, re

P = r'Z:\PTC\Work\MOST-75\most-75.asm.1'
d = open(P, 'rb').read()
print('ФАЙЛ %s (%d байт)' % (os.path.basename(P), len(d)))

# ---- УДАР 1: зона вокруг SBORKA_MM ----
i = d.find(b'SBORKA_MM')
print()
print('=== УДАР 1: SBORKA_MM @%s ===' % hex(i))
print('HEX -40/+60:')
print(d[max(0, i-40):i+60].hex(' ').upper())
print('TXT:')
print(d[max(0, i-60):i+90].decode('ascii', 'replace'))

# все вхождения SBORKA / MFG
print()
print('все вхождения SBORKA:')
for m in re.finditer(rb'[A-Z_]*SBORKA[A-Z_]*', d):
    print('   @%-9s %s' % (hex(m.start()), m.group(0).decode()))

# ---- УДАР 2: все @-подобные маркеры вокруг ----
print()
print('=== УДАР 2: окно 0x1aa00..0x1ac00 ===')
print(d[0x1aa00:0x1ac00].hex(' ').upper()[:900])

# ---- УДАР 3: ВСЕ имена с кириллицей / транслитом ----
print()
print('=== УДАР 3: UTF-8 кириллица в файле ===')
for m in re.finditer(rb'[\xd0-\xd1][\x80-\xbf]{1,15}', d):
    try:
        s = m.group(0).decode('utf-8')
    except Exception:
        continue
    if len(s) >= 3:
        print('   @%-9s %s' % (hex(m.start()), s[:40]))