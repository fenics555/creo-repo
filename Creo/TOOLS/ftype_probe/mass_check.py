r"""ПРИЁМКА чтения массовых свойств из байтов против эталона JLINK.

Эталоны получены 04.10.2026 инструментом
    D:\AI\tools\agent\creo_export\mass_probe.bat   (JLINK, GetMass/GetVolume/GetSurfaceArea)
Формат записи и метод восстановления ведущего байта — см. creo_full.mass_properties.
"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from creo_full import mass_properties

# (файл, MASS, VOLUME, AREA) — эталоны JLINK 04.10.2026, mass_probe.bat
ET = [
    (r'Z:\PTC\Work\00080\00080-03.prt.1',
     0.21461530730689607, 27339.529593235176, 13275.370841291067),
    (r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1',
     6.6861510413184720, 846348.23307828768, 305184.13606400805),
]

print('%-18s %-8s %-22s %-22s %s' % ('МОДЕЛЬ', 'СВОЙСТ.', 'ИЗ ФАЙЛА', 'ЭТАЛОН JLINK', ''))
print('-' * 84)
ok = tot = 0
for path, em, ev, ea in ET:
    got = mass_properties(open(path, 'rb').read())
    if not got:
        print('%-18s НЕ ПРОЧИТАНО' % os.path.basename(path))
        tot += 3
        continue
    for key, want in (('mass', em), ('volume', ev), ('area', ea)):
        g = got.get(key)
        tot += 1
        if g is None:
            print('%-18s %-8s %-22s %-22.15g НЕТ'
                  % (os.path.basename(path), key, '—', want))
            continue
        good = abs(g - want) < 1e-9 * max(1.0, abs(want))
        ok += good
        print('%-18s %-8s %-22.15g %-22.15g %s'
              % (os.path.basename(path), key, g, want, 'СОВПАЛО' if good else 'НЕТ'))
    print('   плотность = %.4f г/см³' % got['density_g_cm3'])

print()
print('СОВПАДЕНИЙ: %d из %d' % (ok, tot))
if ok != tot:
    sys.exit(1)

import json, collections, os

print()
print('=== ДИАГНОСТИКА: почему дерево только у 1 модели из 661 ===')
rows = [json.loads(l) for l in open('plm_final.jsonl', encoding='utf-8') if l.strip()]
have = [r for r in rows if r.get('feature_tree_from_file')]
print('с деревом: %d' % len(have))

print('\n=== ПРЯМАЯ ПРОВЕРКА РАЗБОРА НА НЕСКОЛЬКИХ ФАЙЛАХ ===')
import re as _re
REC = _re.compile(
    rb'\xe3\xc0(..)(..)(?:\xf6)?\xc0(..)'
    rb'([\w\xd0-\xd1][\w\xd0-\xd1 ]{1,30}?)\x00'
    rb'\xc0(..)(.)(\w+)\x00', _re.S)


def toc_of(raw):
    i = raw.find(b'#UGC_TOC')
    j = raw.find(b'\n', i) + 1
    e = raw.find(b'NEXT_TOC_ENTRY', j)
    blob = raw[j:e if e > 0 else j + 12000]
    t = {}
    for mm in _re.finditer(
            rb'^([A-Za-z_][A-Za-z0-9_]*)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+'
            rb'([0-9a-f]+)\s+[0-9a-f]+\s+[0-9a-zA-Z_]+\s+(-?[0-9a-f]+)', blob, _re.M):
        t[mm.group(1).decode()] = (int(mm.group(2), 16), int(mm.group(3), 16))
    return t


for fp in (r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1',
           r'Z:\PTC\Work\00080\00080-03.prt.1',
           r'Z:\PTC\Work\00132\00132.prt.1'):
    if not os.path.exists(fp):
        continue
    raw = open(fp, 'rb').read()
    t = toc_of(raw)
    st = raw[t['MdlStatus'][0]:t['MdlStatus'][0] + t['MdlStatus'][1]] \
        if 'MdlStatus' in t else b''
    n = len(REC.findall(st))
    e3 = st.count(b'\xe3\xc0')
    print('   %-20s MdlStatus=%-6d e3 c0=%-5d REC совпадений=%d'
          % (os.path.basename(fp)[:18], len(st), e3, n))
    if 'FeatDefs' in t:
        fd = raw[t['FeatDefs'][0]:t['FeatDefs'][0] + t['FeatDefs'][1]]
        o = len(REC.findall(fd))
        OWN = _re.compile(rb'\xc0(..)\xf6\x02\xe3.\x49\xc0(..)', _re.S)
        print('       FeatDefs=%-8d REC=%-5d owner-пар=%d' % (len(fd), o, len(OWN.findall(fd))))
nosh = [r for r in rows if not r.get('feature_tree_from_file')][:6]
print('\nверсии Creo: с деревом vs без')
for r in (have[:2] + nosh):
    print('   %-22s v%-8s секций=%-4s %s'
          % (r['model_name'][:20], r['creo_version'],
             r.get('sections'),
             'ДЕРЕВО' if r.get('feature_tree_from_file') else 'нет'))
cv = {}
for r in rows:
    cv.setdefault(r['creo_version'], [0, 0])
    cv[r['creo_version']][1] += 1
    if r.get('feature_tree_from_file'):
        cv[r['creo_version']][0] += 1
print('\nразбивка по версиям (с деревом / всего):')
for v, (a, b) in sorted(cv.items(), key=lambda kv: -kv[1][1])[:8]:
    print('   Creo %-8s %d / %d' % (v, a, b))
for f in ('plm_final.jsonl', 'plm_library.jsonl'):
    rows = [json.loads(l) for l in open(f, encoding='utf-8') if l.strip()]
    mp = [r for r in rows if r.get('mass_properties')]
    ft = [r for r in rows if r.get('feature_tree_from_file')]
    nodes = sum(r['feature_tree_from_file']['nodes'] for r in ft)
    linked = sum(r['feature_tree_from_file']['linked'] for r in ft)
    print('%s: %d моделей | mass %d (%.0f%%) | дерево из файла %d (%.0f%%), узлов %d, связей %d'
          % (f, len(rows), len(mp), 100.0 * len(mp) / len(rows),
             len(ft), 100.0 * len(ft) / len(rows), nodes, linked))
    dens = collections.Counter(
        round(r['mass_properties']['density_g_cm3'], 2) for r in mp
        if r['mass_properties'].get('density_g_cm3'))
    print('   топ плотностей (г/см³): %s' % dens.most_common(5))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# (файл, MASS, VOLUME, AREA) — точные значения из JLINK
ET = [
    (r'Z:\PTC\Work\00080\00080-03.prt.1',
     0.21461530730689607, 27339.529593235176, 13275.370841291067),
    (r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1',
     6.6861510413184720, 846348.23307828768, 305184.13606400805),
]

print('%-18s %-8s %-22s %-22s %s' % ('МОДЕЛЬ', 'СВОЙСТ.', 'ИЗ ФАЙЛА', 'ЭТАЛОН JLINK', ''))
print('-' * 84)
ok = tot = 0
for path, em, ev, ea in ET:
    got = mass_properties(open(path, 'rb').read())
    if not got:
        print('%-18s НЕ ПРОЧИТАНО' % os.path.basename(path))
        tot += 3
        continue
    for key, want in (('mass', em), ('volume', ev), ('area', ea)):
        g = got.get(key)
        tot += 1
        if g is None:
            print('%-18s %-8s %-22s %-22.15g НЕТ' % (os.path.basename(path), key, '—', want))
            continue
        good = abs(g - want) < 1e-9 * max(1.0, abs(want))
        ok += good
        print('%-18s %-8s %-22.15g %-22.15g %s'
              % (os.path.basename(path), key, g, want, 'СОВПАЛО' if good else 'НЕТ'))
    print('   плотность = %.4f г/см³' % got['density_g_cm3'])

print()
print('СОВПАДЕНИЙ: %d из %d' % (ok, tot))
sys.exit(0 if ok == tot else 1)