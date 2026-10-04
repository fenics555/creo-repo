# -*- coding: utf-8 -*-
"""ИНВЕНТАРИЗАЦИЯ МАРКЕРА 46 в «немых» записях crv_pnt_arr.
Проверяем: (а) какие байты идут сразу за 46, (б) инкрементный ли это индекс.
Запуск: python mark46.py [папка] [файлов]
Вывод: mark46_out.txt
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

    nxt = collections.Counter()
    gaps = collections.Counter()
    seq_ok = seq_bad = 0
    samples = []
    nrec = 0
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
            nxti = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            body = data[end + 3:nxti]
            if not (8 <= len(body) <= 200):
                continue
            if any(b in MARK for b in body):
                continue                      # не «немые»
            nrec += 1
            ps = [k for k in range(len(body)) if body[k] == 0x46]
            for p in ps:
                if p + 1 < len(body):
                    nxt[body[p + 1]] += 1
            for a, b in zip(ps, ps[1:]):
                gaps[b - a] += 1
            if len(ps) >= 3:
                vals = [body[p + 1] for p in ps if p + 1 < len(body)]
                inc = all((vals[k + 1] - vals[k]) % 256 in (1, 2, 3)
                          for k in range(len(vals) - 1))
                if inc:
                    seq_ok += 1
                else:
                    seq_bad += 1
                if len(samples) < 10:
                    samples.append((os.path.basename(fp), body, vals))

    out = io.open('mark46_out.txt', 'w', encoding='utf-8')
    out.write('МАРКЕР 46 в «немых» записях · папка %s\n' % base)
    out.write('немых записей: %d\n\n' % nrec)
    out.write('=== БАЙТЫ СРАЗУ ПОСЛЕ 46 (топ-25) ===\n')
    for b, c in nxt.most_common(25):
        out.write('   %02X : %4d%s\n' % (b, c,
                  '  ← известные 5F/60' if b in (0x5F, 0x60) else ''))
    out.write('\n=== РАССТОЯНИЕ МЕЖДУ ПОЯВЛЕНИЯМИ 46 (топ-15) ===\n')
    for g, c in gaps.most_common(15):
        out.write('   %3d байт : %d\n' % (g, c))
    out.write('\n=== ИНКРЕМЕНТНОСТЬ ===\n')
    out.write('   возрастающих подряд: %d\n' % seq_ok)
    out.write('   не возрастающих:     %d\n' % seq_bad)
    out.write('\n=== ПРИМЕРЫ ===\n')
    for nm, body, vals in samples:
        out.write('\n%s: %s\n' % (nm, ' '.join('%02X' % c for c in body[:64])))
        out.write('   после 46: %s\n' % ', '.join('0x%02X' % v for v in vals[:16]))
    out.close()
    print('mark46_out.txt nrec=%d inc_ok=%d inc_bad=%d' % (nrec, seq_ok, seq_bad))

if __name__ == '__main__':
    main()