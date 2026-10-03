# -*- coding: utf-8 -*-
"""РАЗБОР БЛОКОВ FeatDefs: ищем FEATTYPE внутри.
Три независимых признака границы (не полагаемся на один F8):
  1) начало: маркер F8 <N> F7 <M> FB E3 E0 01 "id"
  2) конец:   позиция следующего такого же начала
  3) внутри ищем: числа 1..279, о��торые НЕ являются ID и повторяются у фич одного класса
Сравниваем 2 модели.
Запуск: python blockwalk.py <файл> [файл2]
"""
import re, sys, io, os, collections

FIELD = re.compile(rb'([\xe0-\xff][\x00-\x0f])([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def section(data, name):
    m = re.search(rb'\n#' + name.encode() + rb'[\r\n]', data)
    if not m:
        return None
    start = m.end()
    nxt = re.search(rb'\n#[A-Za-z_][A-Za-z0-9_]{2,30}[\r\n]', data[start:])
    return start, start + (nxt.start() if nxt else len(data) - start)

# начало блока: ... F8 ?? F7 ?? FB E3 E0 01 "id" 00
HEAD = re.compile(rb'\xF8.\xF7.\xFB\xE3\xE0\x01id\x00')

def main():
    out = io.open('blockwalk_out.txt', 'w', encoding='utf-8')
    for path in sys.argv[1:]:
        data = load(path)
        out.write('\n' + '#' * 78 + '\n# %s  (%d байт)\n' % (os.path.basename(path), len(data)) + '#' * 78 + '\n')
        rng = section(data, 'FeatDefs')
        if not rng:
            out.write('секции FeatDefs нет\n')
            continue
        start, end = rng
        out.write('секция FeatDefs: %d..%d  (%d байт)\n' % (start, end, end - start))

        heads = [(m.start(), m.group()) for m in HEAD.finditer(data, start, end + 4000)]
        out.write('НАЙДЕНО начал блоков (F8?F7?FB E3 E0 01 id): %d\n' % len(heads))
        for p, g in heads:
            out.write('   @%d  %s\n' % (p, ' '.join('%02X' % c for c in g)))
        if not heads:
            continue

        out.write('\n--- РАЗБОР БЛОКОВ (граница = следующее начало) ---\n')
        blocks = []
        for k, (p, g) in enumerate(heads):
            stop = heads[k + 1][0] if k + 1 < len(heads) else end
            blocks.append((p, stop, stop - p))
            out.write('\n### блок %d: @%d..%d  длина %d байт\n' % (k + 1, p, stop, stop - p))
            chunk = data[p:stop]
            fs = [(m.start(), m.group(2).decode('ascii', 'replace')) for m in FIELD.finditer(chunk)]
            out.write('   полей: %s\n' % ', '.join(n for _, n in fs[:40]))
            # числа 1..279, исключая позиции ID (84 xx, 85 xx, 83 xx...)
            cands = collections.Counter()
            for i in range(len(chunk) - 1):
                b0, b1 = chunk[i], chunk[i + 1]
                if b0 in (0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89):
                    continue          # это ID, не число
                if 0x01 <= b1 <= 279 and b0 in (0xE0, 0xE3, 0xE1, 0xF1, 0xF2, 0xFB, 0xF8, 0xF7):
                    cands[b1] += 1
            out.write('   числа 1..279 (без ID): %s\n'
                      % ', '.join('%d:%d' % (v, c) for v, c in cands.most_common(15)))
            # первый сырой дамп 160 байт
            out.write('   hex[0:160]: %s\n' % ' '.join('%02X' % c for c in chunk[:160]))
    out.close()
    print('blockwalk_out.txt')

if __name__ == '__main__':
    main()