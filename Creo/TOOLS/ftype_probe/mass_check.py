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
    import re, os, collections

REC2 = re.compile(
    rb'\xe3\xc0(..)(..)(?:\xf6)?\xc0(..)'
    rb'([\w\xd0-\xd1][\w\xd0-\xd1 ]{1,30}?)\x00'
    rb'\xc0(..)(.)(\w+)\x00', re.S)


def toc_of(raw):
    i = raw.find(b'#UGC_TOC')
    j = raw.find(b'\n', i) + 1
    e = raw.find(b'NEXT_TOC_ENTRY', j)
    blob = raw[j:e if e > 0 else j + 12000]
    t = {}
    for mm in re.finditer(
            rb'^([A-Za-z_][A-Za-z0-9_]*)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+'
            rb'([0-9a-f]+)\s+[0-9a-f]+\s+[0-9a-zA-Z_]+\s+(-?[0-9a-f]+)', blob, re.M):
        t[mm.group(1).decode()] = (int(mm.group(2), 16), int(mm.group(3), 16))
    return t


print('=== СТАРЫЙ ФОРМАТ (Creo 9): где записи фич ===')
for fp in (r'Z:\PTC\Work\00080\00080-03.prt.1',
           r'Z:\PTC\Work\00132\00132.prt.1',
           r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
    if not os.path.exists(fp):
        continue
    raw = open(fp, 'rb').read()
    t = toc_of(raw)
    print('\n--- %s (%d байт) ---' % (os.path.basename(fp), len(raw)))
    for sname in ('MdlStatus', 'FeatDefs', 'AllFeatur'):
        if sname not in t:
            continue
        o, l = t[sname]
        b = raw[o:o + l]
        # какие маркеры записи встречаются
        marks = collections.Counter()
        for tag in (b'\xe3\xc0', b'\xe2\x32', b'\xe3\x32', b'\xf7\x1a', b'\xf7\x19'):
            if b.count(tag):
                marks[tag.hex()] = b.count(tag)
        print('   %-10s %8d байт  маркеры: %s'
              % (sname, len(b), dict(marks)))
        if sname == 'MdlStatus':
            # контекст вокруг кириллического имени фичи
            RU = ('[А-ЯЁ][А-ЯЁа-яё ]{2,26}\\s?\\d*').encode('utf-8')
            hits = list(re.finditer(rb'\x00(' + RU + rb')\x00', b))
            print('      кириллических имён: %d' % len(hits))
            for m in hits[:3]:
                s = max(0, m.start() - 20)
                print('      %-20s ...%s | %s...'
                      % (m.group(1).decode('utf-8', 'replace').strip()[:18],
                         b[s:m.start()].hex(' ')[:52],
                         b[m.end():m.end() + 14].hex(' ')))
            print('\n\n' + '=' * 70)
print('РАЗВЕДКА CREO 9: где лежат имена и связи')
print('=' * 70)

for FP in (r'Z:\PTC\Work\00080\00080-03.prt.1',
           r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
    if not os.path.exists(FP):
        continue
    raw = open(FP, 'rb').read()
    tt = toc_of(raw)
    print('\n########## %s ##########' % os.path.basename(FP))
    for sname in ('MdlStatus', 'FeatDefs'):
        if sname not in tt:
            continue
        o, l = tt[sname]
        b = raw[o:o + l]
        print('\n--- %s (%d байт) ---' % (sname, len(b)))
        for tp in (b'featssrf', b'cutextrude', b'featround', b'feathole',
                   b'featsketch', b'protrevolve', b'group', b'dtmplane', b'csys'):
            c = b.count(tp)
            if not c:
                continue
            m = re.search(tp + rb'\x00', b)
            if not m:
                continue
            before = b[max(0, m.start() - 30):m.start()]
            after = b[m.end():m.end() + 34]
            print('\n  %-11s x%-5d' % (tp.decode(), c))
            print('     до  : %r' % before.decode('latin-1'))
            print('     после: %r' % after.decode('latin-1', 'replace')[:32])

print('\n=== ГИПОТЕЗА СТАРОГО ФОРМАТА: <ТИП>\\x00<ИМЯ> id <N>\\x00 ===')
OLD = re.compile(
    rb'(featssrf|cutextrude|featround|protrevolve|feathole|featsketch|group)'
    rb'\x00(?:[\xf6-\xff][\s\S]{0,12})?'
    rb'([\w\xd0-\xd1][\w\xd0-\xd1 ]{1,28}?)\x00', re.S)
for fp in (r'Z:\PTC\Work\00080\00080-03.prt.1',
           r'Z:\PTC\Work\00132\00132.prt.1',
           r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
    if not os.path.exists(fp):
        continue
    raw = open(fp, 'rb').read()
    t = toc_of(raw)
    o, l = t['MdlStatus']
    b = raw[o:o + l]
    hits = list(OLD.finditer(b))
    good = [m for m in hits if re.search(rb'\s\d+$', m.group(2))]
    print('\n%s: всего %d, с «ИМЯ N» %d'
          % (os.path.basename(fp), len(hits), len(good)))
    for m in good[:9]:
        try:
            nm = m.group(2).decode('utf-8')
        except Exception:
            nm = m.group(2).decode('latin-1')
        print('   %-24s [%s]' % (nm.strip()[:22], m.group(1).decode()))
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