"""Валидация feat_records: семантика полей на 3 файлах (Creo 3.0 и Creo 9).

Проверяем три гипотезы ДАННЫМИ, а не на глаз:
  H1: в ветке «f6» после имени лежит is_header (0/1), owner отсутствует.
  H2: в ветке «plain» после имени лежит owner, затем is_header.
  H3: id фичи k = prev фичи k+1 (prev указывает на предыдущую в порядке).
      Проверяется там, где id есть в поле «<имя> id <N>».
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from feat_records import section, parse_feats, toc_of

P137 = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
P80 = r'Z:\PTC\Work\00080\00080-03.prt.1'
P132 = r'Z:\PTC\Work\00132\00132.prt.1'

print('=== H1: ветка f6 — это is_header? ===')
for p in (P80, P132, P137):
    if not os.path.exists(p):
        continue
    feats = parse_feats(section(p))
    st = {}
    for f in feats:
        if f['branch'] == 'str':
            st.setdefault((f['owner'], f['type']), 0)
            st[(f['owner'], f['type'])] += 1
    print('  %-24s (значение, тип) -> %s'
          % (os.path.basename(p), sorted(st.items(), key=lambda x: -x[1])[:6]))

print('\n=== H2: ветка plain — is_header vs тип ===')
for p in (P137,):
    if not os.path.exists(p):
        continue
    feats = parse_feats(section(p))
    ct = {}
    for f in feats:
        if f['branch'] == 'plain':
            ct[(f['is_header'], f['type'])] = ct.get((f['is_header'], f['type']), 0) + 1
    for k in sorted(ct, key=lambda x: -ct[x])[:12]:
        print('   hdr=%-4s %-12s -> %d' % (k[0], k[1], ct[k]))

print('\n=== H3: id(k) == prev(k+1), сверка с полем «id N» ===')
for p in (P80, P132, P137):
    if not os.path.exists(p):
        continue
    feats = parse_feats(section(p))
    ok = bad = 0
    for k in range(len(feats) - 1):
        fid = feats[k]['id']
        if fid is None:
            continue
        derived = feats[k + 1]['prev']
        if fid == derived:
            ok += 1
        else:
            bad += 1
            if bad <= 4:
                print('   РАСХОЖДЕНИЕ %s: id_field=%s, prev(k+1)=%s  %r'
                      % (os.path.basename(p), fid, derived, feats[k]['name'][:26]))
    print('  %-24s совпало=%d расхождений=%d' % (os.path.basename(p), ok, bad))
