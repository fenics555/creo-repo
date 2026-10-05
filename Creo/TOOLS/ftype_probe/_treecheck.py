"""Быстрая проверка feats_from_file: регрессия 137 + новые файлы Creo 9."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from creo_tree_builder import feats_from_file
from feat_records import toc_of

for fp in (r'Z:\PTC\Work\00080\00080-03.prt.1',
           r'Z:\PTC\Work\00132\00132.prt.1',
           r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
    if not os.path.exists(fp):
        print('  НЕТ: %s' % fp)
        continue
    raw = open(fp, 'rb').read()
    toc = toc_of(raw)
    fr = feats_from_file(raw, toc)
    print('%-24s' % os.path.basename(fp), end='')
    if not fr:
        print('  ДЕРЕВА НЕТ')
        continue
    print('  nodes=%-4d linked=%-4d иерарх=%-5s источник=%s'
          % (fr['nodes'], fr['linked'], fr['hierarchy'], fr.get('source')))
    if fr.get('source') == 'records':
        print('      ids_confirmed=%s заголовков=%s'
              % (fr['ids_confirmed'], fr['headers']))
        for r in fr['roots'][:5]:
            print('      корень: %-22r [%s] id=%s owner=%s'
                  % (r['name'][:20], r['type'], r['feat_id'], r.get('owner_id')))


# связка «фича -> владелец» из FeatDefs — есть ли она в Creo 9?
import re
from feat_records import section, parse_feats, record_id

OWN = re.compile(rb'\xc0(..)\xf6\x02\xe3.\x49\xc0(..)', re.S)


def u16(b):
    b = bytes(b)
    while len(b) < 2:
        b += b'\x00'
    return (b[0] << 8) | b[1]


print('\n=== связка FeatDefs «фича -> владелец» ===')
for fp in (r'Z:\PTC\Work\00080\00080-03.prt.1',
           r'Z:\PTC\Work\00132\00132.prt.1',
           r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
    if not os.path.exists(fp):
        continue
    st = section(fp, 'MdlStatus')
    fdd = section(fp, 'FeatDefs')
    fs = parse_feats(st)
    ids = set()
    for f in fs:
        r = record_id(st, f['f6_off'])
        if r:
            ids.add(r[0])
    links = [(u16(m.group(1)), u16(m.group(2))) for m in OWN.finditer(fdd or b'')]
    hit = [(a, b) for a, b in links if a in ids]
    print('  %-24s связок в FeatDefs=%-4d из них с нашим id=%d'
          % (os.path.basename(fp), len(links), len(hit)))
    for a, b in hit[:6]:
        print('       %s -> %s' % (a, b))
