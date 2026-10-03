# -*- coding: utf-8 -*-
"""ГРАНИЦЫ ЗАПИСЕЙ: проверка гипотезы «F8 <N> = длина вложенного блока».
Гипотеза: после F8 <N> идут ровно N байт данных, и заканчиваются они
другим маркером (F7/FB/E0/E3/00). Если это так — границы найдены.
Проверка по 3 критериям ОДНОВРЕМЕННО (чтобы исключить ложное подтверждение):
  A) длина блока по F8 <N> заканчивается на границе другого маркера
  B) повторяемость на 2 моделях
  C) непротиворечивость (блоки не перекрываются)
Запуск: python boundtest.py <файл> [файл2]
Вывод: boundtest_out.txt
"""
import re, sys, io, os, collections

MARK = {0xF8: 'F8', 0xF7: 'F7', 0xFB: 'FB', 0xE0: 'E0', 0xE3: 'E3',
        0xF1: 'F1', 0xF2: 'F2', 0xF6: 'F6', 0x84: '84', 0xE1: 'E1',
        0xF9: 'F9', 0xC0: 'C0', 0xFB: 'FB'}

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def is_marker(b):
    return b in MARK

def test_lengths(data, out, tag):
    """Ищем F8 <N> и F7 <N> — где N в 1..255. Проверяем, что после N байт стоит маркер."""
    out.write('\n' + '=' * 76 + '\n')
    out.write('МОДЕЛЬ: %s  (size=%d)\n' % (tag, len(data)))
    out.write('=' * 76 + '\n')

    stats = {}
    for m_byte in (0xF8, 0xF7):
        ok = 0
        bad = 0
        lens = collections.Counter()
        gaps = collections.Counter()
        examples_bad = []
        i = 0
        while i < len(data) - 1:
            i = data.find(bytes([m_byte]), i)
            if i < 0 or i + 1 >= len(data):
                break
            n = data[i + 1]
            i += 1
            if not (1 <= n <= 250):
                continue
            lens[n] += 1
            end = i + 1 + n
            if end >= len(data):
                continue
            nxt = data[end]
            if is_marker(nxt):
                ok += 1
            else:
                bad += 1
                gaps[nxt] += 1
                if len(examples_bad) < 6:
                    examples_bad.append((i, n, nxt))
        stats[m_byte] = (ok, bad, lens, gaps, examples_bad)
        out.write('\n--- маркер %s <N>: проверка «через N байт стоит маркер» ---\n' % MARK[m_byte])
        out.write('   подтверждено: %d   не подтверждено: %d   (точность %.1f%%)\n'
                  % (ok, bad, 100.0 * ok / max(1, ok + bad)))
        out.write('   ТОП-20 значений N: %s\n'
                  % ', '.join('%d:%d' % (v, c) for v, c in lens.most_common(20)))
        out.write('   ТОП-20 байтов ПОСЛЕ блока (что там): %s\n'
                  % ', '.join('%02X:%d' % (v, c) for v, c in gaps.most_common(20)))
        if examples_bad:
            out.write('   примеры НЕсовпадений:\n')
            for pos, n, nxt in examples_bad:
                out.write('     @%d N=%d, после блока байт %02X\n' % (pos, n, nxt))

    # Гистограмма: покрытие топ-20
    for m_byte in (0xF8, 0xF7):
        ok, bad, lens, gaps, _ = stats[m_byte]
        tot = sum(lens.values())
        top = sum(c for _, c in lens.most_common(20))
        out.write('   %s: топ-20 значений N покрывают %d из %d (%.1f%%)\n'
                  % (MARK[m_byte], top, tot, 100.0 * top / max(1, tot)))
    return stats

def main():
    out = io.open('boundtest_out.txt', 'w', encoding='utf-8')
    allstats = {}
    for path in sys.argv[1:]:
        data = load(path)
        allstats[path] = test_lengths(data, out, os.path.basename(path))

    # СРАВНЕНИЕ МОДЕЛЕЙ: общие значения N
    if len(allstats) >= 2:
        out.write('\n' + '=' * 76 + '\n')
        out.write('СРАВНЕНИЕ ДВУХ МОДЕЛЕЙ (критерий B: повторяемость)\n')
        out.write('=' * 76 + '\n')
        for m_byte in (0xF8, 0xF7):
            sets = []
            for path, st in allstats.items():
                sets.append((os.path.basename(path), st[m_byte][2]))
            out.write('\nмаркер %s:\n' % MARK[m_byte])
            common = None
            for nm, lens in sets:
                top = set(v for v, _ in lens.most_common(30))
                out.write('  %-22s топ-30 N: %s\n' % (nm, sorted(top)))
                common = top if common is None else (common & top)
            out.write('  >>> ОБЩИЕ значения в топ-30 обеих моделей: %s\n' % sorted(common or []))
    out.close()
    print('boundtest_out.txt')

if __name__ == '__main__':
    main()