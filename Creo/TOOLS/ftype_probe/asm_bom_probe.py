import os, re

A = r'Z:\PTC\Work\001_10 AGV\NUTS\nut_m12x1_5-sl.asm.1'
d = open(A, 'rb').read()

print('=== БЛОК @comp_ids / @comp_dep_types ===')
i = d.find(b'@comp_ids')
blk = d[i - 60:i + 900]
print(blk.decode('ascii', 'replace'))
print()
print('=== HEX вокруг @comp_ids ===')
print(d[i - 24:i + 60].hex(' ').upper())

A = r'Z:\PTC\Work\001_10 AGV\NUTS\nut_m12x1_5-sl.asm.1'
d = open(A, 'rb').read()
print('СБОРКА %s (%d байт)' % (os.path.basename(A), len(d)))
print()

# 1) Заголовок целиком
i = d.find(b'#END_OF_UGC_HEADER')
print('=== ЗАГОЛОВОК (0..%d) ===' % (i + 20))
print(d[:i + 20].decode('ascii', 'replace'))
print()

# 2) @bom_count во всём файле (не только в заголовке)
print('=== ВСЕ @bom_count ПО ФАЙЛУ ===')
for m in re.finditer(rb'@bom_count[^\n]*', d):
    print('   @%-8s %s' % (hex(m.start()), m.group(0).decode('ascii', 'replace')))

# 3) Что идёт сразу после заголовка
print()
print('=== ПЕРВЫЕ 400 БАЙТ ПОСЛЕ ЗАГОЛОВКА ===')
print(d[i + 20:i + 420].decode('ascii', 'replace'))

# 4) Все @-теги по всему файлу
print()
print('=== ВСЕ @-ТЕГИ (первые 40) ===')
tags = re.findall(rb'@[A-Za-z_]+', d)
seen = []
for t in tags:
    if t not in seen:
        seen.append(t)
print('   уникальных @-тегов: %d' % len(seen))
for t in seen[:40]:
    print('     %s' % t.decode())