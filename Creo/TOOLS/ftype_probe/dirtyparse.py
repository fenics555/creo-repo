# -*- coding: utf-8 -*-
"""ТОКЕНИЗАТОР «ГРЯЗНОГО» ПОТОКА crv_pnt_arr.
Идея: обходить побайтово, пропуская заглушки FF и бинарные вставки,
и извлекать числа по ПОДТВЕРЖДЁННОЙ формуле 2^(E+1)*(1+F/4096).
⚠️ В формуле E = (b & 0xF0) >> 4 (старший ниббл), а НЕ b & 0x0F.
Запуск: python dirtyparse.py [папка] [файлов]
Вывод: dirtyparse_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK = (0x2F, 0x48)

def decode(b1, b2):
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

def tokenize(body):
    """Возвращает (значения, статистика)."""
    vals = []
    i = 0
    n = len(body)
    ff = ins = 0
    while i < n:
        if body[i:i + 4] == b'\xFF\xFF\xFF\xFF':
            i += 4
            ff += 1
            continue
        if body[i:i + 2] == b'\xE0\x2E':
            j = i + 2
            while j < n - 1:
                if body[j] == 0x18 and body[j + 1] in MARK:
                    break
                j += 1
            ins += 1
            i = j
            continue
        if body[i] == 0x18 and i + 3 < n and body[i + 1] in MARK:
            vals.append(decode(body[i + 2], body[i + 3]))
            i += 4
            continue
        i += 1
    return vals, ff, ins

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

    out = io.open('dirtyparse_out.txt', 'w', encoding='utf-8')
    out.write('ТОКЕНИЗАТОР грязного потока crv_pnt_arr · папка %s\n\n' % base)

    recs = cleanrec = 0
    allvals = []
    tot_ff = tot_ins = 0
    empty = 0
    examples = []
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
            body = payload[3:]                    # маркер F9 XX 04 = 3 байта
            if not (8 <= len(body) <= 200):
                continue
            recs += 1
            vals, ff, ins = tokenize(body)
            tot_ff += ff
            tot_ins += ins
            allvals.extend(vals)
            if len(body) % 4 == 0 and all(body[k + 1] in MARK for k in range(0, len(body), 4)):
                cleanrec += 1
            if not vals:
                empty += 1
            if len(examples) < 10 and vals:
                examples.append((os.path.basename(fp), payload, vals))

    good = [v for v in allvals if 0.001 <= abs(v) <= 1e6]
    out.write('записей разобрано:        %d\n' % recs)
    out.write('  из них чистых (4-байт.): %d\n' % cleanrec)
    out.write('  без единого числа:       %d (%.1f %%)\n'
              % (empty, 100.0 * empty / max(1, recs)))
    out.write('пропущено FF-подставок:   %d\n' % tot_ff)
    out.write('пропущено вставок 2E:     %d\n' % tot_ins)
    out.write('\nдекодировано значений:    %d\n' % len(allvals))
    out.write('правдоподобных:           %d = %.1f %%\n'
              % (len(good), 100.0 * len(good) / max(1, len(allvals))))
    c = collections.Counter(round(v, 4) for v in good)
    out.write('ТОП-25 значений: %s\n'
              % ', '.join('%g×%d' % (k, v) for k, v in c.most_common(25)))
    out.write('\n=== ПРИМЕРЫ ===\n')
    for nm, p, vals in examples:
        out.write('\n%s: %s\n   -> %s\n' % (nm, ' '.join('%02X' % b for b in p[:40]),
                  ', '.join('%g' % v for v in vals[:12])))
    out.close()
    print('dirtyparse_out.txt recs=%d vals=%d' % (recs, len(allvals)))

if __name__ == '__main__':
    main()