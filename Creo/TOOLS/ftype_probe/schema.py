# -*- coding: utf-8 -*-
"""Дамп блока СХЕМЫ: все поля, встречающиеся ровно 1-3 раза, с окружением.
Гипотеза: файл описывает собственную структуру (schema) - по ней можно
восстановить РАЗМЕТКА полей и найти, где лежат данные фич.
Запуск: python schema.py <файл> [радиус]
Вывод: schema_out.txt
"""
import re, sys, io, os, collections

def load(p):
    with open(p, 'rb') as f:
        return f.read()

F = re.compile(rb'([\xe0-\xff][\x00-\x0f])([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def section(data, name):
    m = re.search(rb'\n#' + name.encode() + rb'[\r\n]', data)
    if not m:
        return None
    start = m.end()
    nxt = re.search(rb'\n#[A-Za-z_][A-Za-z0-9_]{2,30}[\r\n]', data[start:])
    return start, start + (nxt.start() if nxt else len(data) - start)

def main():
    path = sys.argv[1]
    rad = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    data = load(path)
    out = io.open('schema_out.txt', 'w', encoding='utf-8')
    out.write('FILE %s size=%d\n' % (os.path.basename(path), len(data)))
    secs = section(data, 'BasicData')
    cnt = collections.Counter()
    for m in F.finditer(data):
        cnt[m.group(2)] += 1
    rare = [k for k, v in cnt.items() if 1 <= v <= 3]
    out.write('редких полей (1-3 вхождения): %d\n' % len(rare))

    # склеиваем: найти максимальный кластер редких полей подряд
    hits = []
    for m in F.finditer(data):
        if m.group(2) in cnt and cnt[m.group(2)] <= 3:
            hits.append((m.start(), m.group(2).decode()))
    out.write('\nвсего редких вхождений: %d\n' % len(hits))

    # кластеры: если 3+ редких поля в пределах 3000 байт
    clusters = []
    cur = [hits[0]] if hits else []
    for h in hits[1:]:
        if h[0] - cur[-1][0] < 3000:
            cur.append(h)
        else:
            if len(cur) >= 4:
                clusters.append(cur)
            cur = [h]
    if len(cur) >= 4:
        clusters.append(cur)
    out.write('кластеров: %d\n\n' % len(clusters))
    for ci, cl in enumerate(clusters):
        lo = max(0, cl[0][0] - rad)
        hi = min(len(data), cl[-1][0] + rad)
        out.write('########## КЛАСТЕР %d: абс.%d..%d  полей=%d ##########\n'
                  % (ci, lo, hi, len(cl)))
        chunk = data[lo:hi]
        for off in range(0, len(chunk), 16):
            part = chunk[off:off + 16]
            asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in part)
            out.write('%08X  %s  %s\n' % (lo + off,
                       ' '.join('%02X' % c for c in part), asc))
        out.write('поля кластера: ' + ', '.join(n for _, n in cl) + '\n\n')
    out.close()
    print('schema_out.txt clusters=%d' % len(clusters))

if __name__ == '__main__':
    main()