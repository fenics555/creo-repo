"""Валидация record_id: читается ли id записи назад от f6.

Две независимые проверки:
  A) id из заголовка  ==  id из поля «<имя> id <N>» (7 записей в 137).
  B) id(k) == prev(k+1): prev указывает на предыдущую фичу в порядке.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from feat_records import section, parse_feats, record_id

P = (r'Z:\PTC\Work\00080\00080-03.prt.1',
     r'Z:\PTC\Work\00132\00132.prt.1',
     r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1')

for p in P:
    if not os.path.exists(p):
        continue
    b = section(p)
    feats = parse_feats(b)
    miss = 0
    for f in feats:
        r = record_id(b, f['f6_off'])
        if r is None:
            miss += 1
            f['rid'] = None
        else:
            f['rid'] = r[0]
    print('\n== %s  записей=%d  id не прочитан=%d'
          % (os.path.basename(p), len(feats), miss))

    # A) сверка с полем id
    a_ok = a_bad = 0
    for f in feats:
        if f['id'] is None or f['rid'] is None:
            continue
        if f['id'] == f['rid']:
            a_ok += 1
        else:
            a_bad += 1
            print('   A РАСХОЖДЕНИЕ %-24r id_field=%s id_заголовка=%s'
                  % (f['name'][:22], f['id'], f['rid']))
    print('   A) id_заголовка == id_поля:  совпало=%d расхождений=%d'
          % (a_ok, a_bad))

    # B) id(k) == prev(k+1)
    b_ok = b_bad = 0
    for k in range(len(feats) - 1):
        rid = feats[k]['rid']
        nxt = feats[k + 1]['prev']
        if rid is None:
            continue
        if rid == nxt:
            b_ok += 1
        else:
            b_bad += 1
            if b_bad <= 5:
                print('   B РАСХОЖДЕНИЕ k=%d %-22r id=%s prev(k+1)=%s'
                      % (k, feats[k]['name'][:20], rid, nxt))
    print('   B) id(k)==prev(k+1):          совпало=%d расхождений=%d'
          % (b_ok, b_bad))

    # сколько id уникальны
    ids = [f['rid'] for f in feats if f['rid'] is not None]
    print('   уникальных id: %d из %d' % (len(set(ids)), len(ids)))
    print('   примеры: %s' % [(f['name'][:16], f['rid'], f['owner'],
                               f['is_header'])
                              for f in feats[:6]])
