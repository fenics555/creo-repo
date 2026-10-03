# -*- coding: utf-8 -*-
"""КЛАССИФИКАЦИЯ записей crv_pnt_arr по покрытию и поиск ВТОРОЙ кодировки.
Берём записи с НУЛЕВЫМ покрытием (39 %) и ищем в них другие маркеры.
Запуск: python pntclass.py [папка] [файлов]
Вывод: pntclass_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)

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

    zero = []          # записи без единого маркера
    part = []          # частичное покрытие
    heads = collections.Counter()
    fieldnames = collections.Counter()

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
            cov = sum(1 for b in body if b in MARK3)
            heads[payload[:6].hex(' ').upper()] += 1
            # какие поля стоят рядом с этой записью
            for j in range(max(0, i - 4), min(len(hits), i + 5)):
                if j != i:
                    fieldnames[hits[j][1]] += 1
            if cov == 0:
                zero.append((os.path.basename(fp), payload))
            elif cov * 3 < len(body):
                part.append((os.path.basename(fp), payload))

    out = io.open('pntclass_out.txt', 'w', encoding='utf-8')
    out.write('КЛАССИФИКАЦИЯ crv_pnt_arr · папка %s\n\n' % base)
    out.write('записей с НУЛЕВЫМ покрытием : %d\n' % len(zero))
    out.write('записей с ЧАСТИЧНЫМ покрытием: %d\n\n' % len(part))

    out.write('=== ПЕРВЫЕ 6 БАЙТ ВСЕХ ЗАПИСЕЙ (частые) ===\n')
    for h, c in heads.most_common(14):
        out.write('   %-18s x%d\n' % (h, c))

    out.write('\n=== ПОЛЯ РЯДОМ С crv_pnt_arr (частые) ===\n')
    for f, c in fieldnames.most_common(18):
        out.write('   %-34s %d\n' % (f, c))

    out.write('\n=== СЫРОЙ РАЗБОР ЗАПИСЕЙ БЕЗ ПОКРЫТИЯ (первые 14) ===\n')
    for nm, payload in zero[:14]:
        out.write('\n--- %s  длина %d ---\n' % (nm, len(payload)))
        for k in range(0, min(len(payload), 96), 16):
            part16 = payload[k:k + 16]
            asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in part16)
            out.write('   %s  %s\n' % (' '.join('%02X' % c for c in part16), asc))
    out.close()
    print('pntclass_out.txt zero=%d part=%d' % (len(zero), len(part)))

if __name__ == '__main__':
    main()