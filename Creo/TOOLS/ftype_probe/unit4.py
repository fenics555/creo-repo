# -*- coding: utf-8 -*-
"""ДЕШИФРОВКА ЭТАЛОННОЙ ЗАПИСИ 19 байт из nik-st-40-720.prt.1
    F9 02 04 | 18 2F 42 00 | 18 2F 42 00 | 18 2F 87 A0 | 18 2F 87 A0
Считаем по формуле и СВЕРЯЕМ с массовыми свойствами той же детали
(их умеем читать: ED + BE-double).
Запуск: python unit4.py <файл.prt.1>
Вывод: unit4_out.txt
"""
import re, sys, io, os, struct

def val3(b1, b2):
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

def be(b):
    return struct.unpack('>d', b)[0] if len(b) == 8 else None

def main():
    path = sys.argv[1]
    data = open(path, 'rb').read()
    out = io.open('unit4_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n\n' % (os.path.basename(path), len(data)))

    out.write('=== ЭТАЛОННАЯ ЗАПИСЬ 19 байт ===\n')
    units = [bytes([0x18, 0x2F, 0x42, 0x00]),
             bytes([0x18, 0x2F, 0x87, 0xA0])]
    for u in units:
        # маркер 2F стоит в u[1]; данные экспоненты — u[2] и u[3]
        v = val3(u[2], u[3])
        e = (u[2] & 0xF0) >> 4
        f = ((u[2] & 0x0F) << 8) | u[3]
        out.write('\n  %s   ->  значение = %g\n'
                  % (' '.join('%02X' % c for c in u), v))
        out.write('     E = %d,  F = %d  (2^%d x (1 + %d/4096))\n' % (e, f, e + 1, f))
        out.write('     префикс 0x%02X = %d\n' % (u[0], u[0]))

    out.write('\n=== МАССОВЫЕ СВОЙСТВА ЭТОЙ ЖЕ ДЕТАЛИ (для сверки) ===\n')
    for name in (b'volume', b'surfarea', b'outline', b'inertia'):
        for m in re.finditer(name + rb'\x00', data):
            p = m.end()
            if data[p] == 0xED:
                v = be(data[p + 1:p + 9])
                if v is not None and 1e-6 < abs(v) < 1e9:
                    out.write('  %-10s @%-9d = %g\n' % (name.decode(), m.start(), v))
                    break

    out.write('\n=== ПАРАМЕТРЫ ДЕТАЛИ (текстовые, если есть) ===\n')
    for pat in (rb'PRO_MP_[A-Z_]{2,20}\x00', rb'PRO_[A-Z_]{2,20}\x00'):
        for m in list(re.finditer(pat, data))[:15]:
            end = m.end()
            z = data.find(b'\x00', end + 1)
            val = data[end + 1:z if z > 0 else end + 30]
            try:
                s = val.decode('utf-8')
            except Exception:
                continue
            out.write('  %-24s = %s\n' % (m.group().rstrip(b'\x00').decode('ascii', 'replace'), s))
    out.close()
    print('unit4_out.txt')

if __name__ == '__main__':
    main()