# -*- coding: utf-8 -*-
"""Что означает байт после E0: длина значения, код типа или конец значения?
Считаем для каждого кода распределение первых байтов значения и длину
значения до следующего маркера поля E0/0xE1-0xFF.
Запуск: python codewhat.py <файл>
"""
import re, sys, io, os, collections

def load(p):
    with open(p, 'rb') as f:
        return f.read()

FIELD = re.compile(rb'([\xe0-\xff][\x00-\x0f])([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('codewhat_out.txt', 'w', encoding='utf-8')
    hits = [(m.start(), m.end(), m.group(1)[0], m.group(2).decode('ascii', 'replace'))
            for m in FIELD.finditer(data)]
    out.write('FILE %s полей=%d\n\n' % (os.path.basename(path), len(hits)))

    firstbyte = collections.defaultdict(collections.Counter)
    vlen = collections.defaultdict(list)
    for k, (s, e, code, nm) in enumerate(hits):
        nxt = hits[k + 1][0] if k + 1 < len(hits) else min(len(data), e + 40)
        v = data[e:nxt]
        if v:
            firstbyte[code][v[0]] += 1
            vlen[code].append(len(v))

    for code in sorted(firstbyte):
        L = vlen[code]
        L.sort()
        out.write('=== КОД 0x%02X  полей=%d  длина_значения: min=%d медиана=%d max=%d\n'
                  % (code, len(L), L[0], L[len(L) // 2], L[-1]))
        top = firstbyte[code].most_common(8)
        out.write('    первые байты значения: %s\n\n'
                  % ', '.join('%02X:%d' % (b, c) for b, c in top))

    # Проверка "код = длина значения": код == длина значения?
    out.write('\n=== ГИПОТЕЗА: код == длина значения ===\n')
    eq = ne = 0
    ex = []
    for k, (s, e, code, nm) in enumerate(hits):
        nxt = hits[k + 1][0] if k + 1 < len(hits) else e
        ln = nxt - e
        if code == ln:
            eq += 1
            if len(ex) < 12:
                ex.append('  %-22s код=%d длина=%d' % (nm, code, ln))
        else:
            ne += 1
    out.write('  совпало: %d   не совпало: %d\n' % (eq, ne))
    for x in ex:
        out.write(x + '\n')
    out.close()
    print('codewhat_out.txt fields=%d eq=%d ne=%d' % (len(hits), eq, ne))

if __name__ == '__main__':
    main()