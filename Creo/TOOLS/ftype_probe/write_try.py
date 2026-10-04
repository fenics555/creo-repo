"""ПРОБА ПЕРЕЗАПИСИ в .prt «в лоб» — строго по протоколу SKILL_creo_write_raw.md.

Правило: менять ТОЛЬКО текст той же длины, в PROBA, с бэкапом и приёмкой.
Запуск: python write_try.py <копия.prt.1>
"""
import sys, io

KEY = b'text_value\x00'
OLD = '1. *- размеры для справок;'
NEW = '1. *- ПРОБА ЗАПИСИ длина!'


def check(path):
    b = open(path, 'rb').read()
    print('=== ПРИЁМКА %s ===' % path)
    print('размер: %d' % len(b))
    print('шапка #UGC: %r' % b[:24])
    # оглавление цело?
    toc = b.find(b'\nNotes ')
    print('секция Notes в оглавлении: %s' % ('на месте' if toc > 0 else 'ПОБИТА'))
    # число секций в TOC (строки между маркерами)
    print('записей в оглавлении: %d'
          % len([x for x in b[:20000].split(b'\n') if b'#' in x[:2]]))
    # все ли секции читаются
    i = b.find(b'#UGC_TOC')
    names = []
    if i >= 0:
        seg = b[i:i + 20000]
        for line in seg.split(b'\n')[1:]:
            if b'#' in line[:2]:
                names.append(line[1:40].split(b' ')[0])
            if line.startswith(b'#-'):
                break
    print('секций в TOC: %d -> %s' % (len(names), b', '.join(names[:12])))
    j = b.find(KEY)
    k = j + len(KEY)
    e = b.find(b'\x00', k)
    print('text_value = %r (len=%d)' % (b[k:e].decode('utf-8', 'replace'), e - k))
    return len(b)


def main():
    path = sys.argv[1]
    before = open(path, 'rb').read()
    n0 = len(before)
    i = before.find(KEY) + len(KEY)
    j = before.find(b'\x00', i)
    old = before[i:j]
    old_txt = old.decode('utf-8')
    new_txt = NEW
    # подгоняем длину в байтах UTF-8 ровно под старую
    while len(new_txt.encode('utf-8')) < len(old):
        new_txt += '.'
    new = new_txt.encode('utf-8')[:len(old)]
    if len(new) != len(old):
        print('ДЛИНЫ НЕ СОВПАДАЮТ — запись отменена')
        return
    print('старое (%d б): %r' % (len(old), old_txt))
    print('новое  (%d б): %r' % (len(new), new.decode('utf-8')))
    print('замена по смещению %d' % i)

    out = bytearray(before)
    out[i:i + len(old)] = new
    with open(path, 'wb') as f:
        f.write(bytes(out))

    print('\nзаписано, размер файла: %d -> %d' % (n0, len(bytes(out))))
    check(path)


if __name__ == '__main__':
    main()