# -*- coding: utf-8 -*-
"""УНИВЕРСАЛЬНЫЙ СВИП: все прочтения × все файлы, сразу.
Критерии адаптивные (без сита кратности 0.25):
  К1 доля значений в широком инженерном диапазоне 1e-4 .. 1e6
  К2 ГЛАДКОСТЬ: малая дисперсия последовательных дельт (для траекторий)
  К3 МОНОТОННОСТЬ: доля соседних пар со знаком дельты
Для каждого файла выбирается ПОБЕДИТЕЛЬ по К2/К3, и печатается таблица.
Запуск: python sweepall.py [папка] [N]
Вывод: sweepall_out.txt
"""
import re, sys, io, os, random, struct, collections, statistics

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)
LO, HI = 1e-4, 1e6

def readers():
    R = {}
    def add(nm, fn, step):
        R[nm] = (fn, step)
    add('f32 BE', lambda b, o: struct.unpack_from('>ff', b, o), 8)
    add('f32 LE', lambda b, o: struct.unpack_from('<ff', b, o), 8)
    add('f64 BE', lambda b, o: (struct.unpack_from('>d', b, o)[0],), 8)
    add('f64 LE', lambda b, o: (struct.unpack_from('<d', b, o)[0],), 8)
    add('i16BE/1e3', lambda b, o: tuple(x/1e3 for x in struct.unpack_from('>hhhh', b, o)), 8)
    add('i16LE/1e3', lambda b, o: tuple(x/1e3 for x in struct.unpack_from('<hhhh', b, o)), 8)
    add('i16BE/1e1', lambda b, o: tuple(x/1e1 for x in struct.unpack_from('>hhhh', b, o)), 8)
    add('i16LE/1e1', lambda b, o: tuple(x/1e1 for x in struct.unpack_from('<hhhh', b, o)), 8)
    add('i32BE/1e7', lambda b, o: (struct.unpack_from('>i', b, o)[0]/1e7,), 8)
    add('i32LE/1e7', lambda b, o: (struct.unpack_from('<i', b, o)[0]/1e7,), 8)
    def p3(b, o):
        if b[o] in MARK3:
            e = (b[o+1] & 0xF0) >> 4
            f = ((b[o+1] & 0x0F) << 8) | b[o+2]
            return (2 ** (e+1) * (1 + f/4096.0),)
        return ()
    add('упаков3', p3, 3)
    def p4(b, o):
        e = (b[o] & 0xF0) >> 4
        f = ((b[o] & 0x0F) << 8) | b[o+1]
        return (2 ** (e+1) * (1 + f/4096.0),)
    add('упаков4', p4, 4)
    return R

R = readers()

def analyse(bodies, fn, step):
    vals = []
    for b in bodies:
        i = 0
        while i + step <= len(b):
            try:
                vs = fn(b, i)
            except Exception:
                vs = ()
            vals.extend([v for v in vs if v == v and abs(v) < 1e30])
            i += step
    if len(vals) < 3:
        return 0, 0, 0, 0.0
    inr = sum(1 for v in vals if LO <= abs(v) <= HI)
    sv = sorted(vals)
    deltas = [sv[i+1] - sv[i] for i in range(len(sv)-1)]
    mono = 0
    same = 0
    for i in range(len(sv)-1):
        d = sv[i+1] - sv[i]
        if d == 0:
            same += 1
        elif d > 0:
            mono += 1
    spread = statistics.pstdev(deltas) if len(deltas) > 1 else 1e30
    # гладкость: чем меньше дисперсия дельт относительно их модуля
    md = statistics.mean([abs(d) for d in deltas]) or 1e30
    smooth = 100.0 * (1.0 - min(1.0, spread / md))
    return len(vals), inr, mono + same, smooth

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            lf = f.lower()
            if lf.endswith('.prt.1') or lf.endswith('.prt'):
                files.append(os.path.join(root, f))
        if len(files) > 30000:
            break
    random.seed(11)
    random.shuffle(files)

    out = io.open('sweepall_out.txt', 'w', encoding='utf-8')
    out.write('УНИВЕРСАЛЬНЫЙ СВИП · %s · %d прочтений × файлы\n\n' % (base, len(R)))

    winners = collections.Counter()
    nfiles = 0
    for fp in files:
        if nfiles >= N:
            break
        try:
            data = open(fp, 'rb').read()
        except Exception:
            continue
        if b'crv_pnt_arr' not in data:
            continue
        hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
                for m in FIELD.finditer(data)]
        bodies = []
        for i, (pos, nm, end) in enumerate(hits):
            if nm != 'crv_pnt_arr':
                continue
            nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            b = data[end + 3:nxt]
            if 16 <= len(b) <= 200 and not any(x in MARK3 for x in b):
                bodies.append(b)
        if not bodies:
            continue
        nfiles += 1
        rows = []
        for nm, (fn, step) in R.items():
            tot, inr, mono, smooth = analyse(bodies, fn, step)
            rows.append((smooth, 100.0*inr/max(1,tot), mono/max(1,tot)*100, nm, tot, inr))
        rows.sort(reverse=True)
        best = rows[0]
        winners[best[3]] += 1
        out.write('=== %s  («немых» записей: %d, байт %d) ===\n'
                  % (os.path.basename(fp)[:44], len(bodies), sum(len(b) for b in bodies)))
        out.write('   %-12s гладкость %5.1f%%  в диапазоне %5.1f%%  монотонн %5.1f%%\n'
                  % (best[3], best[0], best[1], best[2]))
        for sm, ir, mo, nm, tot, inr in rows[1:4]:
            out.write('   %-12s гладкость %5.1f%%  в диапазоне %5.1f%%\n' % (nm, sm, ir))
        out.write('\n')

    out.write('=== ПОБЕДИТЕЛИ ПО %d ФАЙЛАМ ===\n' % nfiles)
    for k, c in winners.most_common():
        out.write('   %-12s выиграл в %d файлах\n' % (k, c))
    out.close()
    print('sweepall_out.txt files=%d' % nfiles)

if __name__ == '__main__':
    main()