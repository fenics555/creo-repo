# -*- coding: utf-8 -*-
"""ВЫБОРКА crv_pnt_arr: 30 записей, поиск длины одной точки.
Метод: собрать payload'ы, измерить длины, найти повторяющиеся маски (хвосты),
       вычислить предполагаемый шаг = длина / (число точек, если известно).
Запуск: python pntsample.py <файл> [N]
Вывод: pntsample_out.txt
"""
import re, sys, io, os, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')

def main():
    path = sys.argv[1]
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    data = open(path, 'rb').read()
    out = io.open('pntsample_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n' % (os.path.basename(path), len(data)))

    # все поля; значение crv_pnt_arr читаем до следующего поля E0/E1/E2/E3
    hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
            for m in FIELD.finditer(data)]
    recs = []
    for i, (pos, nm, end) in enumerate(hits):
        if nm != 'crv_pnt_arr':
            continue
        nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 300)
        payload = data[end:nxt]
        recs.append((pos, payload))
    out.write('записей crv_pnt_arr: %d (берём %d)\n\n' % (len(recs), min(N, len(recs))))

    recs = recs[:N]
    lens = collections.Counter(len(p) for _, p in recs)
    out.write('=== ДЛИНЫ PAYLOAD ===\n')
    for L, c in lens.most_common(12):
        out.write('   %4d байт : %d раз\n' % (L, c))

    out.write('\n=== ПЕРВЫЕ БАЙТЫ PAYLOAD (маркер массива) ===\n')
    head = collections.Counter(p[:4].hex(' ').upper() for _, p in recs if len(p) >= 4)
    for h, c in head.most_common(12):
        out.write('   %-12s x%d\n' % (h, c))

    out.write('\n=== ПОЛНЫЕ ЗАПИСИ (первые 12) ===\n')
    for pos, p in recs[:12]:
        out.write('\n@%d  длина %d\n' % (pos, len(p)))
        for k in range(0, min(len(p), 120), 16):
            part = p[k:k + 16]
            asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in part)
            out.write('   %s  %s\n' % (' '.join('%02X' % c for c in part), asc))

    # повторяющиеся хвосты внутри записей
    out.write('\n=== ПОВТОРЯЮЩИЕСЯ 6-БАЙТОВЫЕ ХВОСТЫ ===\n')
    tail = collections.Counter()
    for pos, p in recs:
        for i in range(4, len(p) - 5):
            tail[p[i:i + 6]] += 1
    for t, c in tail.most_common(10):
        out.write('   %s  x%d\n' % (' '.join('%02X' % c for c in t), c))

    # разности ведущих байтов
    out.write('\n=== ВЕДУЩИЕ БАЙТЫ ЗНАЧЕНИЙ (после F9 xx xx) ===\n')
    lead = collections.Counter()
    for pos, p in recs:
        for i in range(4, len(p)):
            lead[p[i]] += 1
    for b, c in lead.most_common(16):
        out.write('   %02X : %d\n' % (b, c))
    out.close()
    print('pntsample_out.txt recs=%d' % len(recs))

if __name__ == '__main__':
    main()