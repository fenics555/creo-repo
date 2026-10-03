# -*- coding: utf-8 -*-
"""MTTyped_CreateData: разбор записей created_features -> feat_id / ft_type / feat_name.
Цель: найти числовой тип операции (ft_type) прямо в байтах.
Запуск: python ftprobe.py <файл> [смещение_окружения 20] [окно 64]
"""
import re, sys, os

def hx(b):
    return ' '.join('%02X' % c for c in b)

def load(path):
    with open(path, 'rb') as f:
        return f.read()

def find_records(data, anchor=b'MTTyped_CreateData'):
    """Все позиции, где встречается якорь записи."""
    pos = []
    start = 0
    while True:
        i = data.find(anchor, start)
        if i < 0:
            break
        pos.append(i)
        start = i + 1
    return pos

def show(data, pos, window=90):
    lo = max(0, pos - window)
    return lo, data[lo:pos + window]

def main():
    path = sys.argv[1]
    win = int(sys.argv[2]) if len(sys.argv) > 2 else 90
    data = load(path)
    print('ФАЙЛ: %s  (%d байт)' % (os.path.basename(path), len(data)))
    pos = find_records(data)
    print('MTTyped_CreateData: %d вхождений\n' % len(pos))
    for n, p in enumerate(pos[:40], 1):
        lo, chunk = show(data, p, win)
        # печатаем раскладку: смещение от якоря, ascii-поля
        fields = []
        for m in re.finditer(rb'[A-Za-z][A-Za-z0-9_/\.]{1,60}\x00', chunk):
            name = m.group()[:-1].decode('ascii', 'replace')
            fields.append((m.start() + lo - p, name))
        print('--- #%d  абс.%d (окно с %d) ---' % (n, p, lo))
        print('  hex: ' + hx(chunk))
        print('  поля: ' + ', '.join('%s@%+d' % (f[1], f[0]) for f in fields))
        print()

if __name__ == '__main__':
    main()