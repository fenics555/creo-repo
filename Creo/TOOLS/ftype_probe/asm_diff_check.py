# -*- coding: utf-8 -*-
"""ДИФФЕРЕНЦИАЛЬНЫЙ АНАЛИЗ: почему comp_type=02 срабатывает только в ~48 % сборок.
Берём РЕАЛЬНЫЕ .asm с Z: (только чтение), делим на HIT / MISS,
и в MISS смотрим, что стоит вокруг имён .PRT и какие поля там конкурируют.
Запуск: python asm_diff_check.py [папка] [N]
Вывод: asm_diff_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')
PRTN = re.compile(rb'([A-Za-z0-9][A-Za-z0-9_\-\.]{2,40}\.PRT)(?![A-Za-z0-9])')

def sample(base, n):
    allf = []
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.lower().endswith('.asm.1') or f.lower().endswith('.asm'):
                allf.append(os.path.join(root, f))
        if len(allf) > 40000:
            break
    random.seed(7)
    random.shuffle(allf)
    return allf[:n]

def analyse(path):
    try:
        data = open(path, 'rb').read()
    except Exception as e:
        return None
    hits = len(re.findall(rb'comp_type\x00\x02', data))
    prts = PRTN.findall(data)
    return {'path': path, 'data': data, 'hits': hits,
            'prts': prts, 'size': len(data)}

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    files = sample(base, n)
    out = io.open('asm_diff_out.txt', 'w', encoding='utf-8')
    out.write('ДИФФЕРЕНЦИАЛ comp_type · папка %s · файлов %d\n\n' % (base, len(files)))

    res = [analyse(f) for f in files]
    res = [r for r in res if r]
    hit = [r for r in res if r['hits'] > 0]
    miss = [r for r in res if r['hits'] == 0]
    out.write('HIT (comp_type=02 найден): %d\n' % len(hit))
    out.write('MISS (не найден, но есть .PRT): %d\n'
             % len([r for r in miss if r['prts']]))
    out.write('MISS без .PRT вовсе: %d\n\n' % len([r for r in miss if not r['prts']]))

    # какие поля встречаются перед именами .PRT — в HIT и в MISS
    def fields_around(r, limit=6):
        names = collections.Counter()
        samples = []
        for m in PRTN.finditer(r['data']):
            pos = m.start()
            win = r['data'][max(0, pos - 96):pos]
            fs = [(mm.start(), mm.group(2).decode('ascii', 'replace'))
                  for mm in FIELD.finditer(win)]
            for _, nm in fs:
                names[nm] += 1
            if len(samples) < limit:
                samples.append((pos, win[-64:] + b'.PRT'))
        return names, samples

    for label, group in (('HIT', hit), ('MISS', [r for r in miss if r['prts']])):
        if not group:
            continue
        agg = collections.Counter()
        for r in group:
            names, _ = fields_around(r, 0)
            agg.update(names)
        out.write('=== ПОЛЯ В ОКРЕСТИИ .PRT — группа %s (%d файлов) ===\n' % (label, len(group)))
        for nm, c in agg.most_common(28):
            out.write('   %-32s %d\n' % (nm, c))
        out.write('\n')

    # СЫРЫЕ БАЙТЫ: 3 примера из MISS
    if miss:
        target = [r for r in miss if r['prts']][:2]
        for r in target:
            out.write('=== СЫРОЙ СРЕЗ: %s (hits=%d, prts=%d) ===\n'
                      % (os.path.basename(r['path']), r['hits'], len(r['prts'])))
            for pos, seg in [(p, s) for p, s in []] or []:
                pass
            _, samples = fields_around(r, 3)
            for pos, seg in samples:
                lo = max(0, pos - 64)
                out.write('  @%d hex : %s\n' % (pos, ' '.join('%02X' % c for c in seg)))
                asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in seg)
                out.write('        ascii: %s\n' % asc)
            out.write('\n')
    out.close()
    print('asm_diff_out.txt hit=%d miss=%d' % (len(hit), len(miss)))

if __name__ == '__main__':
    main()