# -*- coding: utf-8 -*-
"""AllFeatur: записи фич. Для каждой записи с именем ищем рядом поле типа.
Проверка гипотезы: у признаков, где имя однозначно определяет тип
(DTM* = DATUM_PLANE/AXIS, SOLID, FQUILTS), должно быть одно и то же число.
Запуск: python featall.py <файл> [макс]
Вывод: featall_out.txt
"""
import re, sys, io, os

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

NAMEPAT = re.compile(rb'([\xe0-\xff][\x00-\x0f])([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def main():
    path = sys.argv[1]
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    data = load(path)
    out = io.open('featall_out.txt', 'w', encoding='utf-8')
    rng = section(data, 'AllFeatur')
    if not rng:
        out.write('нет AllFeatur\n'); out.close(); return
    start, end = rng
    out.write('FILE %s size=%d\nAllFeatur абс.%d..%d (%d б)\n\n' %
              (os.path.basename(path), len(data), start, end, end - start))

    hits = [(m.start() + start, m.group(2).decode('ascii', 'replace'))
            for m in NAMEPAT.finditer(data[start:end])]

    # группировка: запись = от предыдущего имени-метки до следующего
    recs = []
    for k, (pos, nm) in enumerate(hits):
        lo = hits[k - 1][0] if k > 0 else pos - 40
        hi = hits[k + 1][0] if k + 1 < len(hits) else pos + 40
        recs.append((pos, nm, lo, hi))

    stats = {}
    for pos, nm, lo, hi in recs[:mx]:
        tail = data[pos:pos + 64]
        # вытащить байты после NUL имени
        z = tail.find(b'\x00')
        if z < 0:
            continue
        rest = tail[z + 1:]
        out.write('абс.%d  %-26s  хвост: %s\n' % (pos, nm[:26],
                  ' '.join('%02X' % c for c in rest[:24])))
        stats.setdefault(nm, set()).add(tuple(rest[:12]))

    out.write('\n=== ПОСТОЯНСТВО ХВОСТА ПО ИМЕНАМ (кандидат на тип) ===\n')
    for nm, s in sorted(stats.items(), key=lambda x: -len(x[1])):
        if len(s) == 1 and len(list(s)[0]) >= 4:
            out.write('  %-26s хвост ПОСТОЯНЕН: %s\n' % (nm[:26],
                      ' '.join('%02X' % c for c in list(s)[0])))
    out.close()
    print('featall_out.txt recs=%d' % len(recs[:mx]))

if __name__ == '__main__':
    main()