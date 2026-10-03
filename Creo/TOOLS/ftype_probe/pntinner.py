# -*- coding: utf-8 -*-
"""ВНУТРЕННЯЯ СТРУКТУРА массива crv_pnt_arr: что лежит МЕЖДУ началом и концом.
Наблюдения, требующие объяснения:
  F9 02 04 46 38 FF FF FF FF FF E0 2E 38 FF 39 30 ...
  -> FF FF FF FF (заглушка/пропуск), E0 2E (вложенное ПОЛЕ), 18 E4 (маркер)
Запуск: python pntinner.py [папка] [файлов]
Вывод: pntinner_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    nf = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            if f.lower().endswith('.prt.1'):
                files.append(os.path.join(root, f))
        if len(files) > 30000:
            break
    random.seed(11)
    random.shuffle(files)

    out = io.open('pntinner_out.txt', 'w', encoding='utf-8')
    out.write('ВНУТРЕННЯЯ СТРУКТУРА crv_pnt_arr\n\n')

    inner = collections.Counter()
    ff_runs = collections.Counter()
    n = 0
    for fp in files[:nf]:
        try:
            data = open(fp, 'rb').read()
        except Exception:
            continue
        if b'crv_pnt_arr' not in data:
            continue
        hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
                for m in FIELD.finditer(data)]
        for i, (pos, nm, end) in enumerate(hits):
            if nm != 'crv_pnt_arr':
                continue
            nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            payload = data[end:nxt]
            if not (8 <= len(payload) <= 120):
                continue
            n += 1
            if n <= 14:
                out.write('\n--- %s  payload %d б ---\n' % (os.path.basename(fp), len(payload)))
                for k in range(0, len(payload), 16):
                    part = payload[k:k + 16]
                    asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in part)
                    out.write('   %s  %s\n' % (' '.join('%02X' % c for c in part), asc))
            # поля внутри payload
            for m in FIELD.finditer(payload):
                inner[m.group(2).decode('ascii', 'replace')] += 1
            # серии FF
            for m in re.finditer(rb'\xFF{3,}', payload):
                ff_runs[len(m.group())] += 1

    out.write('\n=== ПОЛЯ ВНУТРИ МАССИВА (частые) ===\n')
    for f, c in inner.most_common(25):
        out.write('   %-30s %d\n' % (f, c))
    out.write('\n=== СЕРИИ FF (длина -> сколько раз) ===\n')
    for L, c in ff_runs.most_common(12):
        out.write('   %2d байт FF : %d\n' % (L, c))
    out.write('\nвсего записей разобрано: %d\n' % n)
    out.close()
    print('pntinner_out.txt n=%d inner=%d' % (n, len(inner)))

if __name__ == '__main__':
    main()