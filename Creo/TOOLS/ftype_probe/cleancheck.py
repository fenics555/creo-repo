# -*- coding: utf-8 -*-
"""ДОЛЯ ЧИСТЫХ записей crv_pnt_arr на боевой базе.
«Чистая» = payload целиком разбирается на 4-байтовые единицы вида
18 2F <E:b> <F&0xFF>  (или 15 2F …, 48 2F … — префикс 1 байт + маркер 2F + 2 байта).
Это и есть мера реального покрытия.
Запуск: python cleancheck.py [папка] [файлов]
Вывод: cleancheck_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK = (0x2F, 0x48)

def is_unit(b):
    """4-байтовая единица: [префикс] MARK E:Fhi Flo — префикс любой, но 2-й=MARK."""
    return len(b) == 4 and b[1] in MARK

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

    clean = dirty = 0
    tb = tu = 0
    prefixes = collections.Counter()
    vals = []
    samples = []
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
            # маркер массива = F9 XX 04 — это ТРИ байта, а не четыре!
            body = payload[3:]
            if not (8 <= len(body) <= 200) or len(body) % 4 != 0:
                dirty += 1
                continue
            units = [body[k:k + 4] for k in range(0, len(body), 4)]
            if all(is_unit(u) for u in units):
                clean += 1
                tb += len(body)
                tu += len(body)
                for u in units:
                    prefixes['%02X' % u[0]] += 1
                    e = (u[2] & 0xF0) >> 4
                    f = ((u[2] & 0x0F) << 8) | u[3]
                    vals.append(2 ** (e + 1) * (1 + f / 4096.0))
                if len(samples) < 8:
                    samples.append((os.path.basename(fp), payload))
            else:
                dirty += 1
                tb += len(body)

    out = io.open('cleancheck_out.txt', 'w', encoding='utf-8')
    out.write('ЧИСТОТА ЗАПИСЕЙ crv_pnt_arr · папка %s\n\n' % base)
    tot = clean + dirty
    out.write('всего записей:      %d\n' % tot)
    out.write('ЧИСТЫХ (4-байт.ед.):  %d = %.1f %%\n' % (clean, 100.0 * clean / max(1, tot)))
    out.write('грязных:             %d = %.1f %%\n' % (dirty, 100.0 * dirty / max(1, tot)))
    out.write('\nПОКРЫТИЕ по чистым записям: %d / %d байт = %.1f %%\n'
              % (tu, tb, 100.0 * tu / max(1, tb)))
    out.write('\nпрефиксы единиц (частые): %s\n'
              % ', '.join('%s:%d' % (k, v) for k, v in prefixes.most_common(10)))
    if vals:
        good = [v for v in vals if 0.001 <= abs(v) <= 1e6]
        out.write('\nдекодировано значений: %d, правдоподобных: %d = %.1f %%\n'
                  % (len(vals), len(good), 100.0 * len(good) / len(vals)))
        c = collections.Counter(round(v, 4) for v in good)
        out.write('ТОП-20 значений: %s\n'
                  % ', '.join('%g×%d' % (k, v) for k, v in c.most_common(20)))
    out.write('\n=== ПРИМЕРЫ ЧИСТЫХ ЗАПИСЕЙ ===\n')
    for nm, p in samples:
        out.write('\n%s (%d б): %s\n' % (nm, len(p),
                  ' '.join('%02X' % c for c in p)))
    out.close()
    print('cleancheck_out.txt clean=%d dirty=%d' % (clean, dirty))

if __name__ == '__main__':
    main()