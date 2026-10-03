# -*- coding: utf-8 -*-
"""ЧТЕНИЕ МАССОВЫХ СВОЙСТВ ИЗ БАЙТОВ (проверка гипотезы «геометрия читается»).
Гипотеза: volume = маркер ED + BE-double(8 байт).
Проверка: значение должно давать разумный объём (мм³) и совпадать в двух записях.
Запуск: python massprop.py <файл.prt.1>
"""
import re, sys, io, os, struct

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def be_double(b):
    """8 байт BE -> float. Возвращает None если не разумное."""
    try:
        v = struct.unpack('>d', b)[0]
    except Exception:
        return None
    return v

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('massprop_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n\n' % (os.path.basename(path), len(data)))
    out.write('ПОЛЕ      | маркер | 8 байт           | BE-double      | вердикт\n')
    out.write('-' * 78 + '\n')

    rows = []
    for name in ('volume', 'surfarea', 'inertia', 'aver_density', 'density',
                 'mass', 'eps', 'outline'):
        pat = name.encode()
        s = 0
        while True:
            i = data.find(pat, s)
            if i < 0:
                break
            s = i + 1
            e = i + len(pat)
            if e < len(data) and data[e] == 0x00:
                mark = data[e + 1] if e + 1 < len(data) else None
                raw = data[e + 2:e + 10]
                v = be_double(raw) if len(raw) == 8 else None
                # разумность: |v| между 1e-9 и 1e12
                ok = v is not None and (1e-9 < abs(v) < 1e12)
                out.write('%-10s | %s     | %s | %s | %s\n' % (
                    name,
                    '%02X' % mark if mark is not None else '-',
                    ' '.join('%02X' % c for c in raw),
                    ('%14.6g' % v) if v is not None else 'не число',
                    'РАЗУМНО' if ok else 'нет'))
                rows.append((name, mark, v, ok))

    out.write('\n=== СВОДКА ПО ПОЛЯМ ===\n')
    agg = {}
    for name, mark, v, ok in rows:
        agg.setdefault((name, mark), []).append(v)
    for (name, mark), vals in sorted(agg.items()):
        good = [v for v in vals if v is not None and 1e-9 < abs(v) < 1e12]
        out.write('  %-14s маркер %s: %d значений, разумных %d  %s\n' % (
            name, '%02X' % mark if mark is not None else '-', len(vals), len(good),
            'РАЗНЫЕ' if len(set(good)) > 1 else ('ОДИНАКОВЫЕ' if good else 'все неразумные')))
    out.close()
    print('massprop_out.txt')

if __name__ == '__main__':
    main()