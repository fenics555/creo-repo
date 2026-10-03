# -*- coding: utf-8 -*-
"""РЕШАЮЩИЙ ТЕСТ: F8/F7 — это ДЛИНА или МАРКЕР?
Признак длины: значение N распределено широко, и после N байт стоит осмысленный маркер.
Признак маркера: значение почти всегда из МАЛОГО множества (как код типа поля).
Проверяем на 2 моделях + ищем реальные якоря длины (sort_feat_ids).
Запуск: python lenormark.py <файл> [файл2]
"""
import re, sys, io, os, collections

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def analyse(data, out, tag):
    out.write('\n' + '=' * 76 + '\n%s\n' % tag + '=' * 76 + '\n')
    for mb, nm in ((0xF8, 'F8'), (0xF7, 'F7'), (0xE0, 'E0'), (0xE3, 'E3'), (0xFB, 'FB')):
        cnt = collections.Counter()
        i = 0
        while i < len(data) - 1:
            i = data.find(bytes([mb]), i)
            if i < 0 or i + 1 >= len(data):
                break
            cnt[data[i + 1]] += 1
            i += 1
        tot = sum(cnt.values())
        top = cnt.most_common(12)
        uniq = len(cnt)
        out.write('\n%s <N>: всего=%d  РАЗНЫХ значений N=%d\n' % (nm, tot, uniq))
        out.write('   топ-12: %s\n' % ', '.join('%02X:%d' % (v, c) for v, c in top))
        top1 = top[0][1] if top else 0
        out.write('   доля топ-1 значения: %.1f%%  %s\n'
                  % (100.0 * top1 / max(1, tot),
                     'МАРКЕР (выборка мала)' if uniq < 30 else 'длина (выборка велика)'))

def anchors(data, out):
    """Реальные якоря: известно, что sort_feat_ids имеет f8 <число байт>."""
    out.write('\n--- ЯКОРЬ: sort_feat_ids (длина в байтах, проверено ранее) ---\n')
    for m in re.finditer(rb'sort_feat_ids', data):
        pos = m.end()
        seg = data[pos:pos + 60]
        # ищем F8 <N> в ближайших 12 байтах
        out.write('  @%d  %s\n' % (m.start(), ' '.join('%02X' % c for c in seg[:24])))
        mm = re.search(rb'\xF8(.)', seg)
        if mm:
            n = mm.group(1)[0]
            ids = seg[mm.end():mm.end() + 24]
            out.write('        F8 %02X (%d) -> далее %s\n'
                      % (n, n, ' '.join('%02X' % c for c in ids[:16])))
            out.write('        >> если N=%d и следом %d байт ID по 2 => %s\n'
                      % (n, n, 'СХОДИТСЯ' if n % 2 == 0 else 'не чётное -> не длина ID'))

def main():
    out = io.open('lenormark_out.txt', 'w', encoding='utf-8')
    for path in sys.argv[1:]:
        data = load(path)
        analyse(data, out, os.path.basename(path))
        anchors(data, out)
    out.close()
    print('lenormark_out.txt')

if __name__ == '__main__':
    main()