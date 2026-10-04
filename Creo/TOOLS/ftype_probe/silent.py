# -*- coding: utf-8 -*-
"""РАЗБОР «НЕМЫХ» записей crv_pnt_arr (тех, где не нашлось ни одного 3-байтного числа).
Ищем: доминирующие байты, повторяющиеся триплеты, частотные подставки.
Запуск: python silent.py [папка] [файлов]
Вывод: silent_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK = (0x2F, 0x48)

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

    silent = []
    dom = collections.Counter()
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
            body = data[end + 3:nxt]          # маркер F9 XX 04 = 3 байта
            if not (8 <= len(body) <= 200):
                continue
            cnt = sum(1 for b in body if b in MARK)
            if cnt == 0:                        # ни одного 3-байтового числа
                silent.append((os.path.basename(fp), body))
                dom.update(body)

    out = io.open('silent_out.txt', 'w', encoding='utf-8')
    out.write('«НЕМЫЕ» ЗАПИСИ (нет ни одного маркера 2F/48)\n')
    out.write('найдено: %d\n\n' % len(silent))
    out.write('=== ДОМИНИРУЮЩИЕ БАЙТЫ (топ-25) ===\n')
    for b, c in dom.most_common(25):
        note = ''
        if 0x0D <= b <= 0x18:
            note = '  ← диапазон коротких значений по скилам'
        if b in MARK:
            note = '  ← маркер'
        out.write('   %02X : %4d%s\n' % (b, c, note))

    # повторяющиеся триплеты
    out.write('\n=== ПОВТОРЯЮЩИЕСЯ ПАТТЕРНЫ (в каждой записи) ===\n')
    pat2 = collections.Counter()
    pat3 = collections.Counter()
    for nm, body in silent:
        for k in range(len(body) - 1):
            pat2[body[k:k + 2]] += 1
        for k in range(len(body) - 2):
            pat3[body[k:k + 3]] += 1
    out.write('частая пара 2 байта: %s\n'
              % ', '.join(' '.join('%02X' % c for c in p) + ':%d' % v
                          for p, v in pat2.most_common(10)))
    out.write('частая тройка 3 байта: %s\n'
              % ', '.join(' '.join('%02X' % c for c in p) + ':%d' % v
                          for p, v in pat3.most_common(10)))

    out.write('\n=== ПРИМЕРЫ «НЕМЫХ» ЗАПИСЕЙ ===\n')
    for nm, body in silent[:14]:
        out.write('\n%s (%d б):\n' % (nm, len(body)))
        for k in range(0, min(len(body), 96), 16):
            out.write('   %s\n' % ' '.join('%02X' % c for c in body[k:k + 16]))
    out.close()
    print('silent_out.txt silent=%d' % len(silent))

if __name__ == '__main__':
    main()