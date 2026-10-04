import os, sys, json
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
from bom_extract import extract_universal_bom

TESTS = [r'Z:\PTC\Work\MOST-75\most-75.asm.1',
         r'Z:\PTC\Work\00080\00080-03.asm.1',
         r'Z:\PTC\Work\001_10 AGV\NUTS\nut_m12-sl.asm.1']
for t in TESTS:
    if not os.path.exists(t):
        print('нет:', t); continue
    d = open(t, 'rb').read()
    bom, kind, note = extract_universal_bom(d, t)
    print('=' * 62)
    print('%s' % os.path.basename(t))
    print('  тип:  %s   (%s)' % (kind, note))
    print('  BOM:  %d' % len(bom))
    for b in bom[:12]:
        print('      -> %s' % b)