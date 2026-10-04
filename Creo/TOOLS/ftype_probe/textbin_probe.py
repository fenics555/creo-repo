import re

def analyze(path, label):
    d = open(path, 'rb').read()
    print('=' * 70)
    print('%s  %s  (%d байт)' % (label, path.split('\\')[-1], len(d)))

    # Где кончается текст? Ищем первый участок без ASCII-печати длиннее 64 байт
    BLOCK = 64
    first_bin = None
    for i in range(0, len(d) - BLOCK, BLOCK):
        chunk = d[i:i + BLOCK]
        printable = sum(1 for b in chunk if 32 <= b < 127 or b in (10, 13, 9))
        if printable < BLOCK * 0.6:
            first_bin = i
            break
    print('  текст до ~%s (%.0f%% файла)'
          % (hex(first_bin) if first_bin else '?',
             100.0 * (first_bin or 0) / len(d)))

    # Проверяем: есть ли кириллица в текстовой части?
    head = d[:first_bin or 200000]
    ru = set()
    for m in re.finditer(rb'[А-Яа-яЁё]{4,}', head):
        ru.add(m.group(0).decode('utf-8'))
    print('  кириллица В ТЕКСТОВОЙ ЧАСТИ: %d уникальных' % len(ru))
    if ru:
        print('     %s' % ', '.join(sorted(ru)[:12]))

    # операции: ищем по всему файлу
    ops = set()
    for m in re.finditer(rb'(?:^|\x00)([\xd0-\xd1][\x80-\xbf][\x80-\xbf]'
                         rb'(?:[\xd0-\xd1][\x80-\xbf]|\w| ){3,30})\x00', d):
        try:
            s = m.group(1).decode('utf-8')
        except UnicodeDecodeError:
            continue
        if len(s) >= 4:
            ops.add(s)
    print('  строк-кандидатов в операции (по всему файлу): %d' % len(ops))
    sample = [o for o in sorted(ops) if any(ch.isalpha() for ch in o)][:10]
    for o in sample:
        print('     %r' % o)


analyze(r'Z:\PTC\Work\MOST-75\most-75.asm.1', 'СБОРКА')
analyze(r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1', 'ДЕТАЛЬ')
analyze(r'Z:\PTC\Work\137.011.0041\137_011_0041.asm.1', 'СБОРКА 137')