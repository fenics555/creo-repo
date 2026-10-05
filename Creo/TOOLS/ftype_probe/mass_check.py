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
print('=== покрытие по базам ===')
for f in ('plm_final.jsonl', 'plm_library.jsonl'):
    rows = [json.loads(l) for l in open(f, encoding='utf-8') if l.strip()]
    mp = [r for r in rows if r.get('mass_properties')]
    print('%s : %d моделей, mass_properties у %d (%.0f%%)'
          % (f, len(rows), len(mp), 100.0 * len(mp) / len(rows)))
    dens = collections.Counter(
        round(r['mass_properties']['density_g_cm3'], 2) for r in mp
        if r['mass_properties'].get('density_g_cm3'))
    print('   топ плотностей (г/см³): %s' % dens.most_common(6))
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