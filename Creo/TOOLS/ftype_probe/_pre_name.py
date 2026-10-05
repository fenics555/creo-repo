"""Что стоит НЕПОСРЕДСТВЕННО перед именем фичи? Где настоящее начало имени."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fmt9 import toc_of, NTB

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
    print('\n== %s' % os.path.basename(fp))
    for m in list(NTB.finditer(b))[:8]:
        pre = b[max(0, m.start() - 18):m.start()]
        post = b[m.end():m.end() + 18]
        print('  имя  : %-24r' % m.group(1).decode('utf-8', 'replace'))
        print('   дo   : %s' % pre.hex(' '))
        print('   полн : %s' % b[m.start():m.end()].hex(' '))
        print('   после: %s' % post.hex(' '))
