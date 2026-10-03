# -*- coding: utf-8 -*-
"""ПРОВЕРКА: F8 <N> = ЧИСЛО ЭЛЕМЕНТОВ (а не длина в байтах)?
Якорь: sort_feat_ids — за ним идут 2-байтные ID. Если N = счётчик ID,
то ровно N пар байт должны идти до следующего маркера E0/F8.
Запуск: python counttest.py <файл> [файл2]
"""
import re, sys, io, os, collections

MARKERS = {0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xF1, 0xF2, 0xF6, 0xF7, 0xF8,
           0xF9, 0xFB, 0xFC, 0xC0}

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    out = io.open('counttest_out.txt', 'w', encoding='utf-8')
    for path in sys.argv[1:]:
        data = load(path)
        out.write('\n' + '=' * 76 + '\n%s\n' % os.path.basename(path) + '=' * 76 + '\n')
        out.write('\n--- ВСЕ F8 <N> рядом с sort_feat_ids ---\n')
        for m in re.finditer(rb'sort_feat_ids', data):
            pos = m.end()
            seg = data[pos:pos + 120]
            mm = re.search(rb'\xF8(.)', seg)
            if not mm:
                continue
            n = mm.group(1)[0]
            ids = seg[mm.end():]
            out.write('\n  sort_feat_ids @%d  F8 %02X (%d)\n' % (m.start(), n, n))
            out.write('  байты после: %s\n' % ' '.join('%02X' % c for c in ids[:40]))
            # вариант A: N = байт
            a_ok = None
            if mm.end() + n <= len(seg):
                a_ok = seg[mm.end() + n]
            # вариант B: N = пар по 2 байта
            b_end = mm.end() + 2 * n
            b_ok = seg[b_end] if b_end < len(seg) else None
            out.write('   A) N байт=%2d -> следующий байт @%d = %s\n'
                      % (n, mm.end() + n, ('%02X' % a_ok) if a_ok is not None else 'мимо'))
            out.write('   B) N пар  =%2d байт -> следующий байт @%d = %s\n'
                      % (2 * n, b_end, ('%02X' % b_ok) if b_ok is not None else 'мимо'))
            out.write('   ВЕРДИКТ: %s\n' % (
                'B (N=число пар ID)' if (b_ok in MARKERS and (a_ok not in MARKERS or a_ok == 0))
                else 'A (N=байты)' if a_ok in MARKERS else 'не определено'))

        # Общая проверка: F8 <N> где далее ID-пары
        out.write('\n--- СКВОЗНАЯ ПРОВЕРКА F8 <N>: конец по N байт vs по 2N байт ---\n')
        okA = badA = okB = badB = 0
        i = 0
        while i < len(data) - 2:
            if data[i] == 0xF8:
                n = data[i + 1]
                if 1 <= n <= 100:
                    if i + 1 + n < len(data):
                        if data[i + 1 + n] in MARKERS:
                            okA += 1
                        else:
                            badA += 1
                    if i + 1 + 2 * n < len(data):
                        if data[i + 1 + 2 * n] in MARKERS:
                            okB += 1
                        else:
                            badB += 1
            i += 1
        tot = max(1, okA + badA)
        out.write('   N байт : подтверждено %5d / %5d  = %.1f%%\n' % (okA, tot, 100.0 * okA / tot))
        tot2 = max(1, okB + badB)
        out.write('   2N байт: подтверждено %5d / %5d  = %.1f%%\n' % (okB, tot2, 100.0 * okB / tot2))
    out.close()
    print('counttest_out.txt')

if __name__ == '__main__':
    main()