# -*- coding: utf-8 -*-
"""ЧЕСТНАЯ ПРОВЕРКА: какой процент байт массива реально покрывается форматом?
Раньше мерилось «доля правдоподобных среди НАЙДЕННЫХ чисел» — это другая величина.
Здесь: сколько байт body удаётся разобрать как 3-байтные упакованные числа.
Если формат верен — покрытие должно быть близко к 100 %.
Запуск: python pntcover.py [папка] [файлов]
Вывод: pntcover_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)

def val3(b0, b1, b2):
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

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

    out = io.open('pntcover_out.txt', 'w', encoding='utf-8')
    out.write('ПОКРЫТИЕ ФОРМАТА · папка %s\n\n' % base)
    tot_body = 0
    tot_used = 0
    tot_nums = 0
    good = 0
    per_rec = []
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
            if not (8 <= len(payload) <= 200):
                continue
            body = payload[4:]
            used = 0
            nums = []
            k = 0
            while k + 2 < len(body):
                if body[k] in MARK3:
                    v = val3(body[k], body[k + 1], body[k + 2])
                    nums.append(v)
                    used += 3
                    k += 3
                else:
                    k += 1          # не маркер — ищем дальше
            tot_body += len(body)
            tot_used += used
            tot_nums += len(nums)
            g = sum(1 for v in nums if 0.001 <= abs(v) <= 1e5)
            good += g
            if len(body) >= 8:
                per_rec.append((len(body), used, len(nums), g,
                                [round(v, 3) for v in nums[:9]]))

    out.write('ВСЕГО записей: %d\n' % len(per_rec))
    out.write('байт в массивах:      %d\n' % tot_body)
    out.write('покрыто форматом:    %d = %.1f %%\n'
              % (tot_used, 100.0 * tot_used / max(1, tot_body)))
    out.write('декодировано чисел:   %d\n' % tot_nums)
    out.write('из них правдоподобных: %d = %.1f %% (0.001..1e5)\n'
              % (good, 100.0 * good / max(1, tot_nums)))

    cov = collections.Counter()
    for bl, us, nn, gg, vals in per_rec:
        cov[round(100.0 * us / bl)] += 1
    out.write('\n=== РАСПРЕДЕЛЕНИЕ ПОКРЫТИЯ ПО ЗАПИСЯМ (%% байт разобранных) ===\n')
    for c, n in sorted(cov.items()):
        out.write('   %3d %% : %d записей\n' % (c, n))

    out.write('\n=== ЗАПИСИ С НАИЛУЧШИМ ПОКРЫТИЕМ ===\n')
    per_rec.sort(key=lambda r: -r[1] / max(1, r[0]))
    for bl, us, nn, gg, vals in per_rec[:10]:
        out.write('\n   %d/%d байт (%.0f %%), чисел %d, правдоподобных %d'
                  % (us, bl, 100.0 * us / bl, nn, gg))
        out.write('\n   значения: %s\n' % ', '.join('%.4g' % v for v in vals))
    out.close()
    print('pntcover_out.txt recs=%d cover=%.1f%%' % (len(per_rec), 100.0 * tot_used / max(1, tot_body)))

if __name__ == '__main__':
    main()