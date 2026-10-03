# -*- coding: utf-8 -*-
"""МАССОВЫЙ АНАЛИЗ crv_pnt_arr по боевой базе (read-only).
Цель: собрать ТЫСЯЧИ записей и статистически определить раскладку точки.
Метод: для каждого payload ищем самый длинный повторяющийся блок (период),
      считаем распределение длин и периодов. На тысячах выборок период,
      встречающийся чаще всего, и есть истинный шаг.
Запуск: python pntmass.py [папка] [файлов] [записей_на_файл]
Вывод: pntmass_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')

def period_of(buf):
    """Длина повторяющегося блока: ищем минимальный p, при котором buf[p:] == buf[:-p]."""
    n = len(buf)
    for p in range(1, n // 2 + 1):
        if buf[p:] == buf[:n - p]:
            return p
    return None

def sample(base, nf):
    allf = []
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.lower().endswith('.prt.1'):
                allf.append(os.path.join(root, f))
        if len(allf) > 30000:
            break
    random.seed(11)
    random.shuffle(allf)
    return allf[:nf]

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    nf = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    files = sample(base, nf)
    out = io.open('pntmass_out.txt', 'w', encoding='utf-8')
    out.write('МАССОВЫЙ АНАЛИЗ crv_pnt_arr · папка %s · файлов %d\n\n' % (base, nf))

    lens = collections.Counter()
    pers = collections.Counter()
    heads = collections.Counter()
    recs = []
    for fp in files:
        try:
            data = open(fp, 'rb').read()
        except Exception:
            continue
        if b'crv_pnt_arr' not in data:
            continue
        hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
                for m in FIELD.finditer(data)]
        got = 0
        for i, (pos, nm, end) in enumerate(hits):
            if nm != 'crv_pnt_arr':
                continue
            nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            payload = data[end:nxt]
            if len(payload) < 10 or len(payload) > 400:
                continue
            lens[len(payload)] += 1
            heads[payload[:4].hex(' ').upper()] += 1
            p = period_of(payload)
            pers[p] += 1
            recs.append(payload)
            got += 1
            if got >= cap:
                break

    out.write('СОБРАНО записей: %d\n\n' % len(recs))
    out.write('=== ПЕРВЫЕ 4 БАЙТА (маркер массива) ===\n')
    for h, c in heads.most_common(10):
        out.write('   %-14s x%d\n' % (h, c))
    out.write('\n=== ДЛИНЫ PAYLOAD (топ-20) ===\n')
    for L, c in lens.most_common(20):
        out.write('   %4d байт : %d\n' % (L, c))
    out.write('\n=== ПЕРИОД ПОВТОРЕНИЯ (минимальный блок) ===\n')
    for p, c in pers.most_common(15):
        out.write('   %-6s x%d\n' % (p if p else 'нет', c))
    out.write('\n=== ПРИМЕРЫ С ЧИСТЫМ ПЕРИОДОМ ===\n')
    shown = 0
    for payload in recs:
        p = period_of(payload)
        if p and p >= 4:
            out.write('\nпериод %d, длина %d\n' % (p, len(payload)))
            for k in range(0, min(len(payload), 96), 16):
                part = payload[k:k + 16]
                out.write('   %s\n' % ' '.join('%02X' % c for c in part))
            shown += 1
            if shown >= 6:
                break
    out.close()
    print('pntmass_out.txt recs=%d' % len(recs))

if __name__ == '__main__':
    main()