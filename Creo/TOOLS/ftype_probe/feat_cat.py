"""КАТЕГОРИИ ДЕРЕВА: какая фича что есть (04.10.2026).

В файле дерево построения описано читаемыми именами категорий:
`E3 ... <КАТЕГОРИЯ>\0\0 F8 <N> [F8 <M> <байты>] <N × varint(feat_id)>`
Категории: PLANES, AXES, NOTES, SOLID, QUILTS, DATUMS…

Это даёт ТИП-ОБЫЧНОСТЬ фичи офлайн (плоскость/ось/заметка/тело/оболочка),
что проверяется эталоном CREOSON.

Запуск: python feat_cat.py <файл> [<etalon.json>]
"""
import json, io, re, sys
from collections import defaultdict

CATS = (b'PLANES', b'AXES', b'NOTES', b'SOLID', b'QUILTS', b'DATUMS',
        b'DATUM', b'FEATURES', b'CURVES', b'SURFS', b'MERGE', b'COPY')


def dec(b, k):
    b0 = b[k]
    tag = b0 & 0xC0
    if tag == 0xC0:
        return ((b0 & 0x3F) << 16) | (b[k+1] << 8) | b[k+2], 3
    if tag == 0x80:
        return ((b0 & 0x7F) << 8) | b[k+1], 2
    return b0, 1


def extract(b):
    """Возвращает [(категория, [id…])]."""
    out = []
    for m in re.finditer(rb'[A-Z]{3,9}', b):
        w = m.group()
        if w not in CATS:
            continue
        p = m.end()
        if b[p:p + 2] != b'\x00\x00':       # имя закрыто NUL NUL
            continue
        q = p + 2
        if b[q] != 0xF8:
            continue
        n = b[q + 1]
        if not (1 <= n <= 250):
            continue
        k = q + 2
        ids = []
        ok = True
        for _ in range(n):
            if k >= len(b) - 3:
                ok = False
                break
            v, wv = dec(b, k)
            if v == 0 or v > 2_000_000:
                ok = False
                break
            ids.append(v)
            k += wv
        if ok and ids:
            out.append((w.decode(), ids))
    return out


def main():
    path = sys.argv[1]
    b = open(path, 'rb').read()
    cats = extract(b)
    print('файл: %s (%d б)' % (path, len(b)))
    print('найдено категорий: %d' % len(cats))
    allids = {}
    for c, ids in cats:
        print('  %-9s фич: %-4d %s' % (c, len(ids),
                                      ', '.join(str(x) for x in ids[:8])))
        for x in ids:
            allids.setdefault(x, c)

    if len(sys.argv) > 2:
        fl = json.load(io.open(sys.argv[2], encoding='utf-8'))['data']['featlist']
        print('\n=== СВЕРКА С ЭТАЛОНОМ (тип -> категория) ===')
        t2c = defaultdict(lambda: defaultdict(int))
        for f in fl:
            c = allids.get(f['feat_id'])
            if c:
                t2c[f['type']][c] += 1
        for t in sorted(t2c):
            d = t2c[t]
            mark = '✅' if len(d) == 1 else '⚠️'
            print('  %s %-24s -> %s' % (mark, t, ', '.join(
                '%s(%d)' % (k, v) for k, v in sorted(d.items()))))
        cov = len([f for f in fl if f['feat_id'] in allids])
        print('\nпокрытие категориями: %d из %d (%.0f%%)'
              % (cov, len(fl), 100 * cov / len(fl)))


if __name__ == '__main__':
    main()