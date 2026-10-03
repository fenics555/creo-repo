# -*- coding: utf-8 -*-
"""ПРОВЕРКА УТВЕРЖДЕНИЯ «payload всегда кратен 3, иначе кратен 2».
Утверждение пришло из параллельной ноги. Проверяем на реальной боевой базе.
Запуск: python divcheck.py [папка] [файлов]
Вывод: divcheck_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')

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

    raw = collections.Counter()      # длина всего payload
    bodyl = collections.Counter()    # длина после маркера F9 xx 04
    d3 = d2 = none_ = 0
    bad = []
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
            raw[len(payload)] += 1
            bl = len(payload) - 4
            bodyl[bl] += 1
            if bl % 3 == 0:
                d3 += 1
            elif bl % 2 == 0:
                d2 += 1
            else:
                none_ += 1
                bad.append((os.path.basename(fp), payload[:16].hex(' ').upper()))

    out = io.open('divcheck_out.txt', 'w', encoding='utf-8')
    out.write('ПРОВЕРКА КРАТНОСТИ · папка %s\n\n' % base)
    out.write('записей всего:            %d\n' % (d3 + d2 + none_))
    out.write('  длина body кратна 3:    %d (%.1f %%)\n' % (d3, 100.0 * d3 / max(1, d3 + d2 + none_)))
    out.write('  длина body кратна 2 (не 3): %d (%.1f %%)\n' % (d2, 100.0 * d2 / max(1, d3 + d2 + none_)))
    out.write('  НЕ кратна ни 2, ни 3:  %d (%.1f %%)  ← опровергает утверждение\n'
              % (none_, 100.0 * none_ / max(1, d3 + d2 + none_)))
    out.write('\n=== ПРИМЕРЫ «БИТЫХ» ДЛИН ===\n')
    for nm, hx in bad[:20]:
        out.write('   %-44s %s\n' % (nm[:44], hx))
    out.write('\n=== РАСПРЕДЕЛЕНИЕ ДЛИН BODY (нечётные) ===\n')
    odd = [(L, c) for L, c in bodyl.items() if L % 2 == 1]
    for L, c in sorted(odd)[:20]:
        out.write('   %3d байт : %d\n' % (L, c))
    out.close()
    print('divcheck_out.txt d3=%d d2=%d none=%d' % (d3, d2, none_))

if __name__ == '__main__':
    main()