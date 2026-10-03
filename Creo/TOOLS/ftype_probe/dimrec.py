# -*- coding: utf-8 -*-
"""ИМЕНОВАННЫЕ РАЗМЕРЫ: что вокруг маркера E3 32 + упакованного числа.
Ищем не число, а ЗАПИСЬ размера: имя, тип, значение, допуск.
Запуск: python dimrec.py <файл.prt.1>
Вывод: dimrec_out.txt
"""
import re, sys, io, os, collections

PACK = re.compile(rb'\xE3\x32(.)(.)([\x30-\x39])')
FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def dec(e, f):
    return 2 ** (e + 1) * (1 + f / 4096.0)

def main():
    path = sys.argv[1]
    data = open(path, 'rb').read()
    out = io.open('dimrec_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n\n' % (os.path.basename(path), len(data)))

    recs = []
    for m in PACK.finditer(data):
        e = (m.group(1)[0] & 0xF0) >> 4
        f = ((m.group(1)[0] & 0x0F) << 8) | m.group(2)[0]
        v = dec(e, f)
        if 0.001 <= v <= 1e6:
            recs.append((m.start(), v, e, f))
    out.write('ЗАПИСЕЙ E3 32 <упакованное>: %d\n' % len(recs))

    vals = collections.Counter(round(r[1], 6) for r in recs)
    out.write('уникальных значений: %d\n\n' % len(vals))
    out.write('%-14s %5s  %s\n' % ('значение', 'раз', 'позиции'))
    for v, c in vals.most_common(40):
        ps = ['@%06X' % r[0] for r in recs if round(r[1], 6) == v][:5]
        out.write('%-14g %5d  %s\n' % (v, c, ', '.join(ps)))

    # поля вокруг каждой записи
    out.write('\n=== ПОЛЯ В ОКРЕСТИИ ЗАПИСЕЙ ===\n')
    agg = collections.Counter()
    shown = 0
    for pos, v, e, f in recs:
        win = data[max(0, pos - 120):pos + 120]
        fs = [(mm.start(), mm.group(2).decode('ascii', 'replace'))
              for mm in FIELD.finditer(win)]
        for _, nm in fs:
            agg[nm] += 1
        if shown < 6 and v in (10.0, 20.0, 40.0, 50.0, 16.0, 5.0):
            shown += 1
            lo = max(0, pos - 80)
            seg = data[lo:pos + 80]
            out.write('\n--- v=%g @%06X ---\n' % (v, pos))
            for k in range(0, len(seg), 16):
                part = seg[k:k + 16]
                asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in part)
                out.write('  %08X  %s  %s\n' % (lo + k,
                          ' '.join('%02X' % c for c in part), asc))
            out.write('  поля: %s\n' % ', '.join(n for _, n in fs))
    out.write('\n=== ЧАСТЫЕ ПОЛЯ ВОКРУГ ЗНАЧЕНИЙ ===\n')
    for nm, c in agg.most_common(30):
        out.write('   %-32s %d\n' % (nm, c))
    out.close()
    print('dimrec_out.txt recs=%d' % len(recs))

if __name__ == '__main__':
    main()