"""КОРРЕЛЯЦИОННЫЙ ПОИСК FEATTYPE (04.10.2026).

Идея: если тип закодирован числом где-то рядом с именем фичи, то существует
СМЕЩЕНИЕ относительно имени, где байт ОДИНАКОВ у всех фич одного эталонного
типа и РАЗЛИЧЕН у разных. Перебираем все смещения в окне и проверяем.

Строгость: смещение принимается, только если
  - у КАЖДОГО типа значение одно и то же,
  - и значения разных типов попарно различны.
Иначе это шум (как 0x03, который в одной модели держал 4 разных типа).

Запуск: python ftype_correl.py <файл> <etalon.json> [окно]
"""
import json, io, sys
from collections import defaultdict

WIN_L = 30   # байт до имени
WIN_R = 60   # байт после имени


def cstr(b, k):
    out = b''
    while k < len(b) and b[k] != 0:
        out += bytes([b[k]])
        k += 1
    return out


def main():
    path, meta = sys.argv[1], sys.argv[2]
    b = open(path, 'rb').read()
    fl = json.load(io.open(meta, encoding='utf-8'))['data']['featlist']

    # собираем окна: тип -> список окон (только фичи, реально найденные)
    per_type = defaultdict(list)
    found = 0
    for f in fl:
        nm = f['name'].encode('utf-8')
        if not nm:
            continue
        start = 0
        while True:
            i = b.find(nm, start)
            if i < 0:
                break
            start = i + 1
            lo, hi = max(0, i - WIN_L), min(len(b), i + len(nm) + WIN_R)
            if hi - lo < WIN_L + WIN_R:
                continue
            per_type[f['type']].append(b[lo:hi])
            found += 1
    if found == 0:
        print('имена не найдены')
        return

    print('файл: %s' % path)
    print('типов: %d, найденных вхождений имён: %d' % (len(per_type), found))
    for t, w in sorted(per_type.items()):
        print('  %-24s вхождений: %d' % (t, len(w)))

    types = sorted(per_type)
    # окна должны быть одинаковой длины, чтобы смещения совпадали
    L = min(len(w) for v in per_type.values() for w in v)
    good = []
    for off in range(L):
        val = {}
        ok = True
        for t in types:
            s = set(w[off] for w in per_type[t])
            if len(s) != 1:
                ok = False
                break
            val[t] = s.pop()
        if not ok:
            continue
        if len(set(val.values())) == len(val) and len(val) >= 2:
            good.append((off, val))

    if not good:
        print('\nсмещений, разделяющих ТИПЫ, не найдено')
        return
    print('\n=== НАЙДЕНО %d разделяющих смещений ===' % len(good))
    for off, val in good[:10]:
        rel = off - WIN_L
        print('\nсмещение %+d относительно имени:' % rel)
        for t in sorted(val):
            print('    0x%02X (%3d)  %s' % (val[t], val[t], t))


if __name__ == '__main__':
    main()