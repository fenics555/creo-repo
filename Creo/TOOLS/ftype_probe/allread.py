# -*- coding: utf-8 -*-
"""ПЕРЕБОР ВСЕХ ВОЗМОЖНЫХ ПРОЧТЕНИЙ СРАЗУ.
Идея: не гадать по одной гипотезе, а перечислить все разумные варианты
и проверить их ОДНИМ критерием, который случайный шум не проходит:
  ДОЛЯ «КРАСИВЫХ» чисел — кратных 0.25 или 0.5 (инженерные размеры).
У правильного прочтения эта доля высока; у случайного — близка к нулю.
Запуск: python allread.py <файл>
Вывод: allread_out.txt
"""
import re, sys, io, os, struct, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)
MARK4 = MARK3 + (0x18,)

def nice(v):
    """Красивое инженерное число: кратно 0.25"""
    if v is None or v != v:
        return False
    if not (0.001 <= abs(v) <= 1e5):
        return False
    r = v * 4
    return abs(r - round(r)) < 1e-9

def inrange(v):
    return v is not None and v == v and 0.001 <= abs(v) <= 1e5

# ---------------- ВСЕ ВОЗМОЖНЫЕ ПРОЧТЕНИЯ ----------------
def rd_packed3(b0, b1, b2):
    """маркер 2F|48 + [E:F12]"""
    if b0 not in MARK3:
        return None
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

def rd_packed4(b0, b1, b2, b3):
    """[E:Fhi] [F:lo] ..."""
    e = (b0 & 0xF0) >> 4
    f = ((b0 & 0x0F) << 8) | b1
    return 2 ** (e + 1) * (1 + f / 4096.0)

def rd_dbl_be(b, o): return struct.unpack_from('>d', b, o)[0]
def rd_dbl_le(b, o): return struct.unpack_from('<d', b, o)[0]
def rd_i32be(b, o): return struct.unpack_from('>i', b, o)[0] / 1e7
def rd_i32le(b, o): return struct.unpack_from('<i', b, o)[0] / 1e7
def rd_i16be(b, o): return struct.unpack_from('>h', b, o)[0] / 1e2
def rd_i16le(b, o): return struct.unpack_from('<h', b, o)[0] / 1e2
def rd_nib(b0, b1):
    """старший ниббл как показатель степени: 2^(n-15)"""
    return 2.0 ** (((b0 & 0xF0) >> 4) - 15)

READERS = {
    'упаков.3 маркер': ('f3', rd_packed3, 3),
    'упаков.4 ниббл':   ('f4', rd_packed4, 4),
    'double BE':       ('d', rd_dbl_be, 8),
    'double LE':       ('d', rd_dbl_le, 8),
    'int32 BE /1e7':   ('i', rd_i32be, 4),
    'int32 LE /1e7':   ('i', rd_i32le, 4),
    'int16 BE /1e2':   ('i', rd_i16be, 2),
    'int16 LE /1e2':   ('i', rd_i16le, 2),
    'ниббл показатель': ('n', None, 2),
}

def read_body(body, key):
    kind, fn, step = READERS[key]
    vals = []
    if kind == 'f3':
        for i in range(len(body) - 2):
            v = rd_packed3(body[i], body[i + 1], body[i + 2])
            if v is not None:
                vals.append(v)
    elif kind == 'f4':
        for i in range(len(body) - 3):
            vals.append(rd_packed4(body[i], body[i + 1], body[i + 2], body[i + 3]))
    elif kind == 'n':
        for i in range(0, len(body) - 1, 2):
            vals.append(rd_nib(body[i], body[i + 1]))
    else:
        for i in range(0, len(body) - step + 1, step):
            try:
                vals.append(fn(body, i))
            except Exception:
                pass
    return vals

def main():
    path = sys.argv[1]
    data = open(path, 'rb').read()
    hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
            for m in FIELD.finditer(data)]
    bodies = []
    for i, (pos, nm, end) in enumerate(hits):
        if nm != 'crv_pnt_arr':
            continue
        nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
        b = data[end + 3:nxt]
        if 16 <= len(b) <= 200:
            bodies.append(b)
    out = io.open('allread_out.txt', 'w', encoding='utf-8')
    out.write('ПЕРЕБОР ВСЕХ ПРОЧТЕНИЙ · %s\nзаписей: %d, байт: %d\n\n'
              % (os.path.basename(path), len(bodies), sum(len(b) for b in bodies)))
    out.write('%-20s %8s %8s %8s %8s\n' % ('ПРОЧТЕНИЕ', 'значений', 'в норме', 'красивых', '%крас.'))
    out.write('-' * 60 + '\n')
    rows = []
    for key in READERS:
        vals = []
        for b in bodies:
            vals.extend(read_body(b, key))
        if not vals:
            continue
        g = sum(1 for v in vals if inrange(v))
        n = sum(1 for v in vals if nice(v))
        rows.append((100.0 * n / len(vals), key, len(vals), g, n))
    rows.sort(reverse=True)
    for pct, key, tot, g, n in rows:
        out.write('%-20s %8d %8d %8d %7.1f %%\n' % (key, tot, g, n, pct))
    out.write('\n(критерий: у правильного прочтения %%красивых заметно выше;\n')
    out.write(' случайный шум даёт доли, близкие к 1/4 = 25 %)\n')
    out.close()
    print('allread_out.txt best=%s' % (rows[0][1] if rows else '-'))

if __name__ == '__main__':
    main()