# -*- coding: utf-8 -*-
"""ПОКРЫТИЕ ПО ВСЕМ ПОЛЯМ ТОЧКИ вместе.
Раньше мерилось только crv_pnt_arr (13.7 %). Точки разделены между
crv_pnt_arr / crv_pnt_arr2 / crv_pnts — считаем их суммарно.
Запуск: python pntcover2.py [папка] [файлов]
Вывод: pntcover2_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)
PT_FIELDS = ('crv_pnt_arr', 'crv_pnt_arr2', 'crv_pnts')

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

    out = io.open('pntcover2_out.txt', 'w', encoding='utf-8')
    out.write('ПОКРЫТИЕ ПО ВСЕМ ПОЛЯМ ТОЧКИ · папка %s\n\n' % base)

    per_field = {k: [0, 0, 0] for k in PT_FIELDS}   # body_bytes, used, nums
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
            if nm not in PT_FIELDS:
                continue
            nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            payload = data[end:nxt]
            if not (6 <= len(payload) <= 200):
                continue
            body = payload[4:]
            used = 0
            nums = 0
            k = 0
            while k + 2 < len(body):
                if body[k] in MARK3:
                    val3(body[k], body[k + 1], body[k + 2])
                    used += 3
                    nums += 1
                    k += 3
                else:
                    k += 1
            st = per_field[nm]
            st[0] += len(body)
            st[1] += used
            st[2] += nums

    out.write('%-16s %10s %10s %8s %8s\n' % ('поле', 'байт', 'покрыто', '%', 'чисел'))
    tb = tu = tn = 0
    for f in PT_FIELDS:
        b, u, n = per_field[f]
        tb += b; tu += u; tn += n
        out.write('%-16s %10d %10d %7.1f%% %8d\n' % (f, b, u, 100.0 * u / max(1, b), n))
    out.write('\n%-16s %10d %10d %7.1f%% %8d\n'
              % ('ИТОГО', tb, tu, 100.0 * tu / max(1, tb), tn))
    out.write('\n(для сравнения: только crv_pnt_arr давало 13.7 %%)\n')
    out.close()
    print('pntcover2_out.txt total=%.1f%%' % (100.0 * tu / max(1, tb)))

if __name__ == '__main__':
    main()