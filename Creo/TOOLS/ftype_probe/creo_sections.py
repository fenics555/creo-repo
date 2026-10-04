"""ЧИТАТЕЛЬ ФАЙЛОВ CREO — обход по оглавлению, разбор секций.

Не ищет подстроки по всему файлу: читает #UGC_TOC, берёт секцию по имени
и разбирает её по схеме typed_data(<КЛАСС>) с полями и длинами.
"""
import re

TOC = re.compile(
    rb'^([A-Za-z_][A-Za-z0-9_]*)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)'
    rb'\s+[0-9a-f]+\s+[0-9a-zA-Z_]+\s+(-?[0-9a-f]+)\s+([0-9a-f]{4})\s+([0-9a-f]{4})',
    re.M)

CLS = re.compile(rb'typed_data\(([A-Za-z_][A-Za-z0-9_]*)\)')
FIELD = re.compile(rb'([A-Za-z_][A-Za-z0-9_]{2,40})\x00')


def read_toc(path):
    """Возвращает {имя секции: (смещение, длина)}."""
    raw = open(path, 'rb').read()
    i = raw.find(b'#UGC_TOC')
    j = raw.find(b'\n', i) + 1
    # оглавление идёт до первой строки без '#' и до NEXT_TOC_ENTRY
    end = raw.find(b'NEXT_TOC_ENTRY', j)
    if end < 0:
        end = min(len(raw), j + 9000)
    blk = raw[j:end]
    out = {}
    for m in TOC.finditer(blk):
        name = m.group(1).decode()
        out[name] = (int(m.group(2), 16), int(m.group(3), 16))
    for m in re.finditer(rb'ND:0:([A-Za-z0-9_]+):\d+\s+([0-9a-f]+)\s+([0-9a-f]+)', blk):
        out.setdefault(m.group(1).decode(),
                       (int(m.group(2), 16), int(m.group(3), 16)))
    return out, len(raw)


def section(path, name):
    """Возвращает байты секции по имени."""
    toc, size = read_toc(path)
    if name not in toc:
        return None, toc, size
    off, ln = toc[name]
    raw = open(path, 'rb').read()
    return raw[off:off + ln], toc, size


def classes(blob):
    """Все имена классов в секции, по порядку."""
    return [m.group(1).decode() for m in CLS.finditer(blob)]


def pairs(blob):
    """Пары 'имя значения' — регулярка длины перед именем."""
    out = []
    for m in re.finditer(rb'([A-Za-z_][A-Za-z0-9_]{2,40})\x00', blob):
        out.append(m.group(1).decode())
    return out


if __name__ == '__main__':
    import sys
    for P in [r'Z:\PTC\Work\MOST-75\most-75.asm.1',
              r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1']:
        toc, size = read_toc(P)
        print('=' * 74)
        print('%s  (%d байт)' % (P.split('\\')[-1], size))
        print('секций в оглавлении: %d' % len(toc))
        for n in ('SolidPrimdata', 'AllFeatur', 'FeatDefs', 'FeatDefsIndex',
                  'MdlRefInfo', 'LargeText', 'Geomlists'):
            if n in toc:
                off, ln = toc[n]
                print('   %-15s @0x%-7x %8d б' % (n, off, ln))
        print()
        for target in ('AllFeatur', 'FeatDefs', 'FeatDefsIndex'):
            blob, toc2, _ = section(P, target)
            if not blob:
                continue
            cl = classes(blob)
            fld = pairs(blob)
            print('--- секция %s (%d байт)' % (target, len(blob)))
            print('    классы : %s' % (', '.join(sorted(set(cl))[:8]) or '—'))
            print('    поля   : %s' % (', '.join(sorted(set(fld))[:14]) or '—'))
            print()