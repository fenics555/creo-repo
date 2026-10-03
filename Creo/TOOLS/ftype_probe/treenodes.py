# -*- coding: utf-8 -*-
"""СТРУКТУРА УЗЛОВ ДЕРЕВА: декодирование списка узлов item_data.
Установлено по байтам (din933.prt.1, MdlStatus):
   F6 C2 00 20 | E3 <ID:2 байта> 75 00 00 | E3 <len> "<ИМЯ>" 00
   → узел дерева = 2-байтовый ID + имя (PLANES, QUILTS, SOLID, …)
Проверяем: собрать все узлы на 2+ моделях, проверить диапазон ID и полноту.
Запуск: python treenodes.py <файл> [файл2]
"""
import re, sys, io, os, collections

# E3 <ID:2> 75 00 00 E3 <len> "NAME" 00   — узел
NODE = re.compile(rb'\xE3(.)(.)\x75\x00\x00\xE3([A-Za-z0-9_\-\.]{1,40})\x00')

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    out = io.open('treenodes_out.txt', 'w', encoding='utf-8')
    allnodes = {}
    for path in sys.argv[1:]:
        data = load(path)
        out.write('\n' + '=' * 76 + '\n%s\n' % os.path.basename(path) + '=' * 76 + '\n')
        nodes = []
        for m in NODE.finditer(data):
            idv = (m.group(1)[0] << 8) | m.group(2)[0]
            nm = m.group(3).decode('ascii', 'replace')
            nodes.append((idv, nm, m.start()))
        out.write('узлов найдено: %d\n' % len(nodes))
        for idv, nm, pos in nodes:
            out.write('   ID 0x%04X  %-22s @%d\n' % (idv, nm[:22], pos))
        if nodes:
            ids = [n[0] for n in nodes]
            out.write('\nдиапазон ID: 0x%04X .. 0x%04X\n' % (min(ids), max(ids)))
            out.write('уникальных ID: %d из %d\n' % (len(set(ids)), len(ids)))
            pref = collections.Counter(i >> 8 for i in ids)
            out.write('старшие байты ID: %s\n'
                      % ', '.join('0x%02X:%d' % (k, v) for k, v in pref.most_common()))
        allnodes[os.path.basename(path)] = {n[1] for n in nodes}

    if len(allnodes) >= 2:
        out.write('\n' + '=' * 76 + '\nПЕРЕСЕЧЕНИЕ ИМЁН УЗЛОВ\n' + '=' * 76 + '\n')
        names = list(allnodes)
        a, b = allnodes[names[0]], allnodes[names[1]]
        out.write('%s: %s\n' % (names[0], sorted(a)))
        out.write('%s: %s\n' % (names[1], sorted(b)))
        out.write('>>> ОБЩИЕ: %s\n' % sorted(a & b))
    out.close()
    print('treenodes_out.txt')

if __name__ == '__main__':
    main()