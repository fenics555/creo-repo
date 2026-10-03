# -*- coding: utf-8 -*-
"""ПРОВЕРКА УПАКОВАННОГО ФОРМАТА по формуле из скилов:
    значение = 2^(E+1) × (1 + F/4096)
    байты:   [маркер 0x2F|0x48] [E:F12] ...
Для значения 10.0:  10 = 2^3 × 1.25  → E=2, F=0.25*4096=0x400
    → байты: 2F 24 00   (E<<4 | F>>8 = 0x24, F&0xFF = 0x00)
Это ПРЕДСКАЗАНИЕ из уже задокументированного закона — проверяем, а не гадаем.
Запуск: python packedpred.py <файл> [значения]
Вывод: packedpred_out.txt
"""
import re, sys, io, os

MARKERS = (0x2F, 0x48)

def encode(v):
    """Значение -> возможные байтовые последовательности по формуле."""
    out = []
    for m in MARKERS:
        for e in range(0, 16):
            base = 2 ** (e + 1)
            f = (v / base - 1.0) * 4096
            if abs(f - round(f)) < 1e-9 and 0 <= round(f) <= 4095:
                fi = int(round(f))
                seq = bytes([m, (e << 4) | (fi >> 8), fi & 0xFF])
                out.append((seq, e, fi))
    return out

def decode(b0, b1, b2):
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

def main():
    path = sys.argv[1]
    vals = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else \
           [10.0, 1.5, 16.0, 20.0, 30.0, 40.0, 50.0, 5.0, 8.0, 12.0]
    data = open(path, 'rb').read()
    out = io.open('packedpred_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n' % (os.path.basename(path), len(data)))
    out.write('Проверка предсказания из формулы 2^(E+1)x(1+F/4096)\n\n')
    out.write('%-10s %-14s %6s  %s\n' % ('значение', 'байты', 'раз', 'позиции'))
    for v in vals:
        seqs = encode(v)
        if not seqs:
            out.write('%-10s (не представимо)\n' % v)
            continue
        for seq, e, f in seqs[:2]:
            pos = []
            s = 0
            while True:
                i = data.find(seq, s)
                if i < 0:
                    break
                pos.append(i)
                s = i + 1
                if len(pos) >= 12:
                    break
            out.write('%-10s %-14s %6d  %s\n' % (
                '%g' % v, ' '.join('%02X' % c for c in seq), len(pos),
                ', '.join('@%06X' % p for p in pos[:8])))
            if pos:
                p0 = pos[0]
                lo = max(0, p0 - 24)
                seg = data[lo:p0 + 24]
                out.write('            контекст: %s\n' % ' '.join('%02X' % c for c in seg))

    # контрольная проверка: сколько всего распознаваемых упакованных чисел
    out.write('\n=== ПРОВЕРКА ДЕКОДЕРА (по всему файлу) ===\n')
    good = collections.Counter()
    for i in range(len(data) - 3):
        b0, b1, b2 = data[i], data[i + 1], data[i + 2]
        if b0 in MARKERS:
            v = decode(b0, b1, b2)
            if 0.001 <= v <= 1e5:
                good[round(v, 6)] += 1
    out.write('уникальных значений: %d\n' % len(good))
    out.write('ТОП-25 по частоте:\n')
    for v, c in good.most_common(25):
        out.write('   %-14g %d\n' % (v, c))
    out.close()
    print('packedpred_out.txt uniq=%d' % len(good))

import collections
if __name__ == '__main__':
    main()