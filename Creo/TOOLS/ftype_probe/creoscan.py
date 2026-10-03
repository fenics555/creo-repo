# -*- coding: utf-8 -*-
"""Универсальный поиск структурных записей в файлах Creo (offline).
Каждая запись = набор ASCII-имён полей. Печать в файл UTF-8.
Запуск: python creoscan.py <файл> <поле1> [поле2 ...] [--before N --after N]
"""
import re, sys, io, os, argparse

def load(path):
    with open(path, 'rb') as f:
        return f.read()

def sections(data):
    """Возвращает {имя: (смещение_содержимого, длина)} по маркерам \\n#Имя."""
    out = {}
    for m in re.finditer(rb'\n#([A-Za-z_][A-Za-z0-9_]{2,30})[\r\n]', data):
        name = m.group(1).decode('ascii')
        start = m.end()
        if name not in out:
            out[name] = (start, len(data) - start)
    return out

def fields(chunk, lo=0):
    """[(offset_от_lo, имя_поля)] для NUL-терминированных ASCII-имён."""
    res = []
    for m in re.finditer(rb'[A-Za-z][A-Za-z0-9_/\.\-\(\)]{1,60}\x00', chunk):
        res.append((m.start() + lo, m.group()[:-1].decode('ascii', 'replace')))
    return res

def hx(b, start=0):
    lines = []
    for i in range(0, len(b), 16):
        part = b[i:i + 16]
        lines.append('%08X  %s' % (start + i, ' '.join('%02X' % c for c in part)))
    return '\n'.join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('names', nargs='+')
    ap.add_argument('--before', type=int, default=0)
    ap.add_argument('--after', type=int, default=120)
    ap.add_argument('--max', type=int, default=40)
    ap.add_argument('--field', default=None, help='печатать только записи, где это поле есть рядом')
    a = ap.parse_args()

    data = load(a.file)
    out = io.open('out_scan.txt', 'w', encoding='utf-8')
    out.write('FILE %s  size=%d\n' % (a.file, len(data)))
    secs = sections(data)
    out.write('SECTIONS %d: %s\n\n' % (len(secs), ', '.join(sorted(secs))))

    total = 0
    for name in a.names:
        pat = name.encode()
        cnt = data.count(pat)
        out.write('=== "%s": %d вхождений ===\n' % (name, cnt))
        start = 0
        shown = 0
        while shown < a.max:
            i = data.find(pat, start)
            if i < 0:
                break
            start = i + 1
            if a.field is not None:
                near = data[max(0, i - a.after):i + a.after]
                if a.field.encode() not in near:
                    continue
            lo = max(0, i - a.before)
            chunk = data[lo:i + a.after]
            fl = fields(chunk, lo)
            out.write('--- абс.%d (окно с %d) ---\n' % (i, lo))
            out.write(hx(chunk, lo) + '\n')
            out.write('поля: ' + ', '.join('%s@%d' % (n, o) for o, n in fl) + '\n\n')
            shown += 1
            total += 1
    out.write('ВСЕГО показано %d\n' % total)
    out.close()
    print('written out_scan.txt, shown=%d' % total)

if __name__ == '__main__':
    main()