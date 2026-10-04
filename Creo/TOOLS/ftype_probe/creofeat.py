"""ЕДИНЫЙ ЧИТАТЕЛЬ ФИЧ .prt — то, что реально доказано (04.10.2026).

Читает: имена фич, feat_id (varint 1/2/3 байта), порядок построения.
Не читает (долг 7): числовой тип операции — см. _INDEX.md.

Использование:
    python creofeat.py <файл.prt.1>            кратко
    python creofeat.py <файл.prt.1> --audit    сколько фич найдено
"""
import sys, io
from collections import defaultdict


def dec(b, k):
    """varint: длина в двух старших битах первого байта."""
    b0 = b[k]
    tag = b0 & 0xC0
    if tag == 0xC0:
        return ((b0 & 0x3F) << 16) | (b[k+1] << 8) | b[k+2], 3
    if tag == 0x80:
        return ((b0 & 0x7F) << 8) | b[k+1], 2
    return b0, 1


def read_features(b):
    """Все записи вида <имя>\\0 01 00 [18 E5] <varint id>."""
    out = []
    i = 0
    n = len(b)
    while i < n - 8:
        if b[i + 1:i + 4] == b'\x00\x01\x00' and 32 <= b[i] < 127:
            # имя: ASCII подряд перед этим байтом
            j = i - 1
            k = j
            while k >= 0 and 32 <= b[k] < 127:
                k -= 1
            if k >= 0 and 1 <= (i - k) <= 60:
                name = b[k + 1:i + 1]
                p = i + 4
                if b[p:p + 2] == b'\x18\xe5':
                    p += 2
                try:
                    fid, w = dec(b, p)
                except IndexError:
                    i += 1
                    continue
                if 0 < fid < 2_000_000:
                    try:
                        nm = name.decode('utf-8')
                    except UnicodeDecodeError:
                        nm = name.decode('latin-1')
                    out.append((fid, nm, i))
        i += 1
    return out


def read_order(b):
    """Списки `f8 <N>` + N*varint(id) — кандидаты на порядок построения."""
    out = []
    i = 0
    n = len(b)
    while i < n - 2:
        if b[i] == 0xF8 and 2 <= b[i + 1] <= 200:
            cnt = b[i + 1]
            k = i + 2
            ids = []
            for _ in range(cnt):
                if k >= n - 3:
                    break
                try:
                    v, w = dec(b, k)
                except IndexError:
                    break
                if v == 0 or v > 2_000_000:
                    break
                ids.append(v)
                k += w
            if len(ids) == cnt:
                out.append((i, ids))
        i += 1
    return out


def main():
    path = sys.argv[1]
    b = open(path, 'rb').read()
    feats = read_features(b)
    orders = read_order(b)

    print('файл: %s' % path)
    print('размер: %d б' % len(b))
    print('фич с ID: %d, списков-кандидатов порядка: %d'
          % (len(feats), len(orders)))

    if '--audit' in sys.argv:
        # ⚠️ ВАЖНО: без эталона список порядка выбрать НЕЛЬЗЯ.
        # Проверено: «самый длинный» и «возрастающие ID» дают ложные
        # списки (в 137 обедают на 192 и 90 «элементов» вместо верных 73).
        # Надёжен только отбор по сверке с эталоном CREOSON — feat_order.py.
        print('списков-кандидатов: %d' % len(orders))
        print('⚠️ выбор списка порядка требует эталона CREOSON → feat_order.py')
        return

    byid = defaultdict(list)
    for fid, nm, off in feats:
        byid[fid].append(nm)
    print('\n--- ФИЧИ (имя, ID) ---')
    seen = set()
    for fid, nm, off in feats:
        if fid in seen:
            continue
        seen.add(fid)
        print('  id=%-8d %s' % (fid, nm))


if __name__ == '__main__':
    main()