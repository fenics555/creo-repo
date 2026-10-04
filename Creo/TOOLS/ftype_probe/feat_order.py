"""Читает дерево построения: список ID фич в порядке создания.

Найдено 04.10.2026: последовательность `f8 <N>` + N×varint(id) содержит
ID фич ровно в порядке построения (сверено с эталоном CREOSON).

Запуск: python feat_order.py <файл> <etalon.json>
"""
import json, io, sys


def dec(b, k):
    b0 = b[k]
    tag = b0 & 0xC0
    if tag == 0xC0:
        return ((b0 & 0x3F) << 16) | (b[k+1] << 8) | b[k+2], 3
    if tag == 0x80:
        return ((b0 & 0x7F) << 8) | b[k+1], 2
    return b0, 1


def find_lists(b):
    """Все места вида f8 <N> N×varint, где N — осмысленный размер."""
    out = []
    i = 0
    n = len(b)
    while i < n - 2:
        if b[i] == 0xF8:
            cnt = b[i + 1]
            if 2 <= cnt <= 200:
                k = i + 2
                ids = []
                ok = True
                for _ in range(cnt):
                    if k >= n - 3:
                        ok = False
                        break
                    try:
                        v, w = dec(b, k)
                    except IndexError:
                        ok = False
                        break
                    # разумный ID фичи: 1..2 000 000
                    if v == 0 or v > 2_000_000:
                        ok = False
                        break
                    ids.append(v)
                    k += w
                if ok and ids:
                    out.append((i, ids))
        i += 1
    return out


def main():
    path, meta = sys.argv[1], sys.argv[2]
    b = open(path, 'rb').read()
    fl = json.load(io.open(meta, encoding='utf-8'))['data']['featlist']
    known = set(f['feat_id'] for f in fl)
    name_by_id = dict((f['feat_id'], f) for f in fl)

    lists = find_lists(b)
    print('файл: %s (%d б), эталонных фич: %d' % (path, len(b), len(fl)))
    print('найдено списков f8<N>+ID: %d' % len(lists))
    best = None
    for off, ids in lists:
        hit = len([i for i in ids if i in known])
        if hit >= 3 and (best is None or hit > best[2]):
            best = (off, ids, hit)
    if not best:
        print('список, где >=3 ID совпали с эталоном, не найден')
        return
    off, ids, hit = best
    print('\nЛУЧШИЙ список @%07X: %d элементов, %d совпали с эталоном'
          % (off, len(ids), hit))
    for i, v in enumerate(ids):
        f = name_by_id.get(v)
        tag = ('%-22s %s' % (f['name'][:22], f['type'][:20])) if f else '(нет в эталоне)'
        print('  %2d  id=%-7d %s' % (i, v, tag))


if __name__ == '__main__':
    main()