# -*- coding: utf-8 -*-
"""СРАВНЕНИЕ ГЕОМЕТРИИ ПО ТИПАМ ФАЙЛОВ: .prt / .asm / .drw.
Ранее все замеры делались ТОЛЬКО по .prt — возможно, «немые» записи
встречаются и в других типах, где кодировка иная.
Запуск: python geomtypes.py [папка] [файлов_на_тип]
Вывод: geomtypes_out.txt
"""
import re, sys, io, os, random, collections

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

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    per = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    groups = {'prt': [], 'asm': [], 'drw': []}
    for root, dirs, fs in os.walk(base):
        for f in fs:
            lf = f.lower()
            for k in groups:
                if lf.endswith('.' + k + '.1') or lf.endswith('.' + k):
                    groups[k].append(os.path.join(root, f))
        if sum(len(v) for v in groups.values()) > 40000:
            break
    random.seed(11)
    for k in groups:
        random.shuffle(groups[k])

    out = io.open('geomtypes_out.txt', 'w', encoding='utf-8')
    out.write('ГЕОМЕТРИЯ ПО ТИПАМ ФАЙЛОВ\n')
    for k in groups:
        out.write('  %s: всего %d\n' % (k, len(groups[k])))

    for kind in ('prt', 'asm', 'drw'):
        out.write('\n' + '=' * 74 + '\nТИП .%s\n' % kind + '=' * 74 + '\n')
        stats = collections.Counter()
        with_pnt = with_arr = silent = tot = 0
        b_all = b_silent = n_p3 = n_n3 = n_p4 = n_n4 = 0
        files_used = 0
        for fp in groups[kind][:per]:
            try:
                data = open(fp, 'rb').read()
            except Exception:
                continue
            if b'crv_pnt_arr' not in data:
                continue
            files_used += 1
            hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
                    for m in FIELD.finditer(data)]
            for i, (pos, nm, end) in enumerate(hits):
                if nm not in ('crv_pnt_arr', 'crv_pnts'):
                    continue
                if nm == 'crv_pnts':
                    with_pnt += 1
                else:
                    with_arr += 1
                nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
                body = data[end + 3:nxt]
                if not (16 <= len(body) <= 200):
                    continue
                tot += 1
                b_all += len(body)
                has = any(x in MARK3 for x in body)
                if not has:
                    silent += 1
                    b_silent += len(body)
                for k in range(len(body) - 2):
                    if body[k] in MARK3:
                        n_p3 += 1
                        if nice(rd_packed3(body[k], body[k + 1], body[k + 2])):
                            n_n3 += 1
                for k in range(len(body) - 3):
                    if nice(rd_packed4(body[k], body[k + 1])):
                        n_n4 += 1
        out.write('файлов с crv_pnt_arr: %d\n' % files_used)
        out.write('вхождений: crv_pnt_arr=%d, crv_pnts=%d, записей разобрано=%d\n'
                  % (with_arr, with_pnt, tot))
        out.write('«НЕМЫХ» записей: %d = %.1f %%\n'
                  % (silent, 100.0 * silent / max(1, tot)))
        out.write('упаков.3 — красивых %d из %d = %.1f %%\n'
                  % (n_n3, n_p3, 100.0 * n_n3 / max(1, n_p3)))
        out.write('упаков.4 — красивых %d из %d байт-пар\n' % (n_n4, max(1, b_all - 3)))
    out.close()
    print('geomtypes_out.txt')

if __name__ == '__main__':
    main()