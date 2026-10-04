# -*- coding: utf-8 -*-
"""АВТОКОРРЕЛЯЦИЯ payload crv_pnt_arr.
Ищем не ПОЛНУЮ периодичность (она дала 0), а статистический ПИК:
для каждого шага p считаем долю позиций, где buf[i] == buf[i+p].
Если формат с фиксированным шагом — будет резкий пик.
Если пика нет — формат переменной длины, и тогда нужен бит-уровень.
Запуск: python pntacorr.py [папка] [файлов]
Вывод: pntacorr_out.txt
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

    out = io.open('pntacorr_out.txt', 'w', encoding='utf-8')
    out.write('АВТОКОРРЕЛЯЦИЯ payload crv_pnt_arr\n\n')
    prof = collections.defaultdict(list)   # шаг -> доли
    examples = []
    n = 0
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
            body = data[end + 4:nxt]
            if not (10 <= len(body) <= 60):
                continue
            n += 1
            if n <= 8:
                examples.append((os.path.basename(fp), body))
            L = len(body)
            for p in range(1, 17):
                same = sum(1 for k in range(L - p) if body[k] == body[k + p])
                prof[p].append(same / max(1, L - p))

    out.write('записей разобрано: %d\n\n' % n)
    out.write('шаг | среднее совпадение | записей с >0.5 | записей с >0.8\n')
    out.write('-' * 58 + '\n')
    for p in sorted(prof):
        v = prof[p]
        hi5 = sum(1 for x in v if x > 0.5)
        hi8 = sum(1 for x in v if x > 0.8)
        out.write(' %3d | %.3f               | %8d        | %d\n'
                  % (p, sum(v) / len(v), hi5, hi8))

    base_rate = 1.0 / 256
    out.write('\nслучайная база (1/256) = %.4f\n' % base_rate)
    best = max(prof, key=lambda p: sum(prof[p]) / len(prof[p])) if prof else None
    if best:
        out.write('ЛУЧШИЙ ШАГ: %d (среднее %.3f, x%.0f от случайной базы)\n'
                  % (best, sum(prof[best]) / len(prof[best]),
                     (sum(prof[best]) / len(prof[best])) / base_rate))
    out.write('\n=== ПРИМЕРЫ ЗАПИСЕЙ ===\n')
    for nm, body in examples:
        out.write('\n%s (%d б):\n' % (nm, len(body)))
        for k in range(0, len(body), 16):
            out.write('   %s\n' % ' '.join('%02X' % c for c in body[k:k + 16]))
    out.close()
    print('pntacorr_out.txt n=%d' % n)

if __name__ == '__main__':
    main()