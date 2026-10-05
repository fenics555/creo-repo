"""Все вхождения типа в MdlStatus: сколько записей реально и что мешает разбору."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _feat9 import toc_of, parse_feats, TYPES

for fp in (r'Z:\PTC\Work\00080\00080-03.prt.1',
           r'Z:\PTC\Work\00132\00132.prt.1',
           r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
    if not os.path.exists(fp):
        continue
    raw = open(fp, 'rb').read()
    t = toc_of(raw)
    if 'MdlStatus' not in t:
        continue
    o, l = t['MdlStatus']
    b = raw[o:o + l]
    print('\n== %s  (%d байт)' % (os.path.basename(fp), len(b)))

    # все вхождения типов — только как целое слово (\x00<TIP>\x00),
    # иначе 'group' матчится внутри 'pat_group_header_id'
    occ = []
    for ty in TYPES:
        s = 0
        while True:
            s = b.find(b'\x00' + ty + b'\x00', s)
            if s < 0:
                break
            occ.append((s + 1, ty.decode()))
            s += 1
    occ.sort()
    print('   вхождений типов (\\x00тип\\x00): %d' % len(occ))

    feats = parse_feats(b)
    parsed_at = {f['name_off'] for f in feats}
    print('   разобрано записей: %d' % len(feats))

    # что вокруг неразобранных
    ok = 0
    for pos, ty in occ:
        b0 = b.rfind(b'\x00', max(0, pos - 120), pos)
        near = any(abs(p - b0) < 60 for p in parsed_at) if b0 > 0 else False
        ok += int(near)
        if not near:
            print('   --- НЕ разобрано: тип %-11s @%d' % (ty, pos))
            print('       дo : %s' % b[max(0, pos - 46):pos].hex(' '))
            print('       после: %s'
                  % b[pos + len(ty):pos + len(ty) + 34].hex(' '))
    print('   из них рядом с разобранной записью: %d' % ok)
