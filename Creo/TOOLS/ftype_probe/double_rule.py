import struct, re

P = r'Z:\PTC\Work'

def find_file(name):
    import os
    for root, dirs, fs in os.walk(P):
        for f in fs:
            if f.lower() == name.lower():
                return os.path.join(root, f)
    return None

CASES = [
    (r'ruscam-ufa-1014-01.prt.1', [('MASS', 2.799001052172452),
                                   ('DEFAULT2', 590903076.7953686),
                                   ('DEFAULT_XHATCH_ANGLE', 45.0),
                                   ('DEFAULT_XHATCH_SPACING', 2.0)]),
    (r'is-10_001_001_003.prt.1', [('MASS', 0.6253065868809754)]),
]

# ===== гипотеза №2: нулевое усечение =====
import os as _os
_pp = find_file('ruscam-ufa-1014-01.prt.1')
_dd = open(_pp, 'rb').read()
print()
print('=== гипотеза нулевого усечения')
for _pn, _v in [('DEFAULT_XHATCH_ANGLE', 45.0),
                ('DEFAULT_XHATCH_SPACING', 2.0),
                ('MASS', 2.799001052172452)]:
    _nb = _pn.encode('utf-8')
    _i = _dd.find(b'\xe3' + _nb + b'\x00')
    if _i < 0:
        _i = _dd.find(b'\xe3' + _nb)
    if _i < 0:
        print('  %-24s имя НЕ найдено' % _pn); continue
    _be = struct.pack('>d', _v)
    _win = _dd[_i:_i+80]
    _hits = []
    for _n in range(1, 9):
        _j = _win.find(_be[:_n])
        if _j >= 0:
            _hits.append('%dб=%s@+%d' % (_n, _be[:_n].hex(' ').upper(), _j))
    print('  %-24s эталон=%s' % (_pn, _be.hex(' ').upper()))
    print('      префиксы в окне: %s' % (', '.join(_hits) if _hits else 'НИ ОДНОГО'))
    print('      после имени: %s' % _win[3:25].hex(' ').upper())

print()
for fname, params in CASES:
    path = find_file(fname)
    if not path:
        print('не найден', fname); continue
    d = open(path, 'rb').read()
    print('=== %s (%d б)' % (fname, len(d)))
    for pname, val in params:
        nb = pname.encode('utf-8')
        i = d.find(b'\xe3' + nb + b'\x00')
        if i < 0:
            i = d.find(b'\xe3' + nb)
        if i < 0:
            print('   %-24s запись не найдена' % pname); continue
        # ищем 7-байтовую мантиссу в окне после имени
        win = d[i:i+60]
        be = struct.pack('>d', val)
        tail7 = be[1:]
        j = win.find(tail7)
        if j < 0:
            print('   %-24s значение %.10f  мантисса НЕ НАЙДЕНА' % (pname, val))
            continue
        # ПОБАЙТОВОЕ СРАВНЕНИЕ: гипотеза о сдвиге экспоненты
        orig = be
        found = tail7
        print('   %-22s эталон=%-18.10f' % (pname, val))
        print('      оригинал BE (8 б): %s' % orig.hex(' ').upper())
        print('      найдено в файле(7): %s' % found.hex(' ').upper())
        print('      ориг[1]=%02X   найденный[0]=%02X   РАВНЫ: %s'
              % (orig[1], found[0], orig[1] == found[0]))
        print('      хвост ориг[1:] == найденное: %s'
              % (orig[1:] == found))
        # гипотеза: в первом байте найденного куска сидят 4 бита экспоненты
        print('      ориг[0]=0x%02X (знак=%d, эксп верх=%d)'
              % (orig[0], orig[0] >> 7, ((orig[0] & 0x7F) << 4) | (orig[1] >> 4)))