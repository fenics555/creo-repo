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

WIN_L = 200  # байт до имени
WIN_R = 200  # байт после имени
MIN_NAME = 4  # короче — ловится внутри других слов («В» давал 481 мусор)


def dec(b, k):
    b0 = b[k]
    tag = b0 & 0xC0
    if tag == 0xC0:
        return ((b0 & 0x3F) << 16) | (b[k+1] << 8) | b[k+2], 3
    if tag == 0x80:
        return ((b0 & 0x7F) << 8) | b[k+1], 2
    return b0, 1


def verified_windows(b, nm, fid):
    """Окна, привязанные к ID фичи. Обе формы записи:
       A) <имя>\\0 01 00 [18 E5] <varint id>   (ASCII-имена)
       B) e3 <varint id> <длина> <имя>        (кириллица и часть ASCII)
    Окно центрируется на позиции varint, поэтому смещения сопоставимы.
    """
    pat = []
    i = fid
    if i < 0x80:
        pat = bytes([i])
    elif i < 0x4000:
        pat = bytes([0x80 | ((i >> 8) & 0x7F), i & 0xFF])
    else:
        pat = bytes([0xC0 | ((i >> 16) & 0x3F), (i >> 8) & 0xFF, i & 0xFF])

    out = []
    start = 0
    while True:
        p = b.find(pat, start)
        if p < 0:
            break
        start = p + 1
        ok = False
        if p >= 3 and b[p - 3:p] == b'\x00\x01\x00':
            ok = True                       # форма A
        if not ok and p >= 1 and b[p - 1] == 0xE3:
            tail = b[p + len(pat):p + len(pat) + 2]
            if tail and nm.startswith(tail[1:2]):
                ok = True                   # форма B: <длина><имя>
        if not ok:
            continue
        lo, hi = max(0, p - WIN_L), min(len(b), p + WIN_R)
        if hi - lo == WIN_L + WIN_R:
            out.append((p, b[lo:hi]))
    return out


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

    # собираем окна: тип -> список окон, ТОЛЬКО по проверенным записям
    per_type = defaultdict(list)
    found = 0
    for f in fl:
        nm = f['name'].encode('utf-8')
        if len(nm) < MIN_NAME:
            continue
        wins = verified_windows(b, nm, f['feat_id'])
        if not wins:
            continue
        per_type[f['type']].extend(w[1] for w in wins)
        found += len(wins)
    if found == 0:
        print('проверенных записей не найдено')
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