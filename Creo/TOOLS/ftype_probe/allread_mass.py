# -*- coding: utf-8 -*-
"""ПАКЕТНЫЙ ПЕРЕБОР ПО 10+ РАЗНЫМ ФАЙЛАМ.
Каждый файл с «немыми» записями (без маркеров 2F/48) прогоняется
через все прочтения allread. Ищем прочтение, дающее устойчиво высокий
% красивых чисел на РАЗНЫХ файлах.
Запуск: python allread_mass.py [папка] [N]
Вывод: allread_mass_out.txt
"""
import re, sys, io, os, random, struct, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)

def nice(v):
    if v is None or v != v:
        return False
    if not (0.001 <= abs(v) <= 1e5):
        return False
    r = v * 4
    return abs(r - round(r)) < 1e-9

def rd_packed3(b0, b1, b2):
    if b0 not in MARK3:
        return None
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

def rd_packed4(b0, b1):
    e = (b0 & 0xF0) >> 4
    f = ((b0 & 0x0F) << 8) | b1
    return 2 ** (e + 1) * (1 + f / 4096.0)

def rd_nib(b0):
    return 2.0 ** (((b0 & 0xF0) >> 4) - 15)

def variants(body):
    """возвращает {имя: [значения]}"""
    v = {}
    v['упаков.3'] = [rd_packed3(body[i], body[i + 1], body[i + 2])
                     for i in range(len(body) - 2)
                     if body[i] in MARK3]
    v['упаков.4'] = [rd_packed4(body[i], body[i + 1]) for i in range(len(body) - 3)]
    for nm, e, step in (('float32 BE', '>ff', 8), ('float32 LE', '<ff', 8),
                        ('float16 BE', '>eeee', 8), ('float16 LE', '<eeee', 8),
                        ('double BE', '>d', 8), ('double LE', '<d', 8)):
        vals = []
        for i in range(0, len(body) - step + 1, step):
            try:
                vals.extend(struct.unpack(e, body[i:i + step]))
            except Exception:
                pass
        v[nm] = vals
    v['int32 BE/1e7'] = [struct.unpack_from('>i', body, i)[0] / 1e7
                         for i in range(0, len(body) - 3, 4)]
    v['int32 LE/1e7'] = [struct.unpack_from('<i', body, i)[0] / 1e7
                         for i in range(0, len(body) - 3, 4)]
    v['ниббл'] = [rd_nib(body[i]) for i in range(len(body))]
    return v

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            if f.lower().endswith('.prt.1'):
                files.append(os.path.join(root, f))
        if len(files) > 30000:
            break
    random.seed(11)
    random.shuffle(files)

    out = io.open('allread_mass_out.txt', 'w', encoding='utf-8')
    out.write('ПАКЕТНЫЙ ПЕРЕБОР ПО ФАЙЛАМ · %s\n\n' % base)

    chosen = []
    for fp in files:
        if len(chosen) >= N:
            break
        try:
            data = open(fp, 'rb').read()
        except Exception:
            continue
        if b'crv_pnt_arr' not in data:
            continue
        hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
                for m in FIELD.finditer(data)]
        silent = []
        for i, (pos, nm, end) in enumerate(hits):
            if nm != 'crv_pnt_arr':
                continue
            nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            b = data[end + 3:nxt]
            if 16 <= len(b) <= 200 and not any(x in MARK3 for x in b):
                silent.append(b)
        if silent:
            chosen.append((os.path.basename(fp), silent))

    out.write('ФАЙЛОВ С «НЕМЫМИ» ЗАПИСЯМИ: %d\n\n' % len(chosen))
    out.write('%-42s %8s\n' % ('файл', 'записей'))
    for nm, s in chosen:
        out.write('%-42s %8d\n' % (nm[:42], len(s)))

    # суммарная статистика по всем выбранным файлам
    agg = collections.defaultdict(lambda: [0, 0])
    per_file = {}
    for nm, bodies in chosen:
        pf = collections.defaultdict(lambda: [0, 0])
        for b in bodies:
            for key, vals in variants(b).items():
                for x in vals:
                    pf[key][0] += 1
                    if nice(x):
                        pf[key][1] += 1
        per_file[nm] = {k: (100.0 * v[1] / v[0] if v[0] else 0.0) for k, v in pf.items()}
        for k, v in pf.items():
            agg[k][0] += v[0]
            agg[k][1] += v[1]

    out.write('\n=== СВОДНО ПО %d ФАЙЛАМ ===\n' % len(chosen))
    out.write('%-18s %10s %10s %9s\n' % ('ПРОЧТЕНИЕ', 'значений', 'красивых', '%'))
    for k, (tot, n) in sorted(agg.items(), key=lambda x: -x[1][1] / max(1, x[1][0])):
        out.write('%-18s %10d %10d %8.1f %%\n' % (k, tot, n, 100.0 * n / max(1, tot)))

    out.write('\n=== ПОКАЗАТЕЛЬНОСТЬ ПО ФАЙЛАМ (лучшие 4 прочтения) ===\n')
    best = sorted(per_file[chosen[0][0]].items(), key=lambda x: -x[1])[:4] if chosen else []
    out.write('%-42s %s\n' % ('файл', '  '.join('%s=%.0f%%' % (k, v) for k, v in best)))
    for nm, s in chosen:
        pf = per_file[nm]
        top = sorted(pf.items(), key=lambda x: -x[1])[:3]
        out.write('%-42s %s\n' % (nm[:42], '  '.join('%s=%.0f%%' % (k, v) for k, v in top)))
    out.close()
    print('allread_mass_out.txt files=%d' % len(chosen))

if __name__ == '__main__':
    main()