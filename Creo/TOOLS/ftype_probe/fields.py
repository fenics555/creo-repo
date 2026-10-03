# -*- coding: utf-8 -*-
"""Инвентаризация полей: все <len> <имя>\\0 вхождения с частотой.
Запуск: python fields.py <файл> [секция]
"""
import re, sys, io, os, collections

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def section(data, name):
    m = re.search(rb'\n#' + name.encode() + rb'[\r\n]', data)
    if not m:
        return None
    start = m.end()
    nxt = re.search(rb'\n#[A-Za-z_][A-Za-z0-9_]{2,30}[\r\n]', data[start:])
    end = start + (nxt.start() if nxt else len(data) - start)
    return start, end

F = re.compile(rb'([\xe0-\xff][\x00-\x0f])([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def main():
    path = sys.argv[1]
    sec = sys.argv[2] if len(sys.argv) > 2 else None
    data = load(path)
    if sec:
        rng = section(data, sec)
        chunk = data[rng[0]:rng[1]] if rng else b''
    else:
        chunk = data
    cnt = collections.Counter()
    for m in F.finditer(chunk):
        cnt[m.group(2).decode('ascii', 'replace')] += 1
    out = io.open('fields_out.txt', 'w', encoding='utf-8')
    out.write('FILE %s  объём=%d  уникальных=%d\n\n' % (os.path.basename(path), len(chunk), len(cnt)))
    for k, v in cnt.most_common(400):
        out.write('%-40s %d\n' % (k, v))
    out.close()
    print('fields_out.txt uniq=%d' % len(cnt))

if __name__ == '__main__':
    main()