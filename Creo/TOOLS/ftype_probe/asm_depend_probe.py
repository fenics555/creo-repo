import os, re

A = r'Z:\PTC\Work\001_10 AGV\NUTS\nut_m12x1_5-sl.asm.1'
d = open(A, 'rb').read()
i = d.find(b'@depend')
print('СБОРКА: %s (%d байт)' % (os.path.basename(A), len(d)))
print('@depend @%s' % hex(i))
print()
print('=== СЫРОЙ ТЕКСТОВЫЙ БЛОК (400 байт) ===')
blk = d[max(0, i - 64):i + 400]
print(blk.decode('ascii', 'replace'))
print()
print('=== ТОКЕНЫ @depend/@model/@end ===')
for m in re.finditer(rb'@[A-Za-z_]+', d):
    print('   @%-9s %s' % (hex(m.start()), m.group(0).decode()))

ASMS = [r'Z:\PTC\Work\00080\00080-03.asm.1',
        r'Z:\PTC\Work\00132\00132.asm.1',
        r'Z:\PTC\Work\00143\00143.asm.1',
        r'Z:\PTC\Work\001_10 AGV\NUTS\nut_m12x1_5-sl.asm.1']

MARKERS = [b'@depend', b'depend', b'DEPEND', b'component', b'component_name',
           b'member', b'#UGC_DEPEND', b'prt_name', b'subassy', b'sub_assembly']

PRT = re.compile(rb'([A-Za-z0-9_\-\. ]{2,44}\.(?:[Pp][Rr][Tt]|[Pp][Rr][Tt]\.\d))')

for A in ASMS:
    if not os.path.exists(A):
        print('НЕТ ФАЙЛА:', A); continue
    d = open(A, 'rb').read()
    base = os.path.basename(A)
    stem = base.split('.')[0]
    print('=' * 70)
    print('СБОРКА %s (%d байт)' % (base, len(d)))
    print()

    print('  --- МАРКЕРЫ ---')
    for kw in MARKERS:
        i = d.find(kw)
        if i >= 0:
            print('    %-12s @%-9s %s' % (kw.decode(), hex(i),
                  d[max(0, i-8):i+len(kw)+24].hex(' ').upper()))

    print()
    print('  --- ССЫЛКИ НА .prt ---')
    all_refs = set(m.group(1).decode('latin-1') for m in PRT.finditer(d))
    ext = sorted(r for r in all_refs if stem not in r)
    print('    всего уникальных: %d, сторонних (без %s): %d'
          % (len(all_refs), stem, len(ext)))
    for r in ext[:25]:
        print('      ->', r.strip())
    print()