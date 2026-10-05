"""Факт: что лежит МЕЖДУ концом имени и типом — по каждой записи.

Вместо того чтобы гадать о varint, показываем сырые байты и проверяем
кандидатов детерминированно: длина L такая, что b[e+1+L] == 0 и дальше
сразу идёт известный тип.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _feat9 import toc_of, TYPES

TSET = {t: None for t in TYPES}


def records(b):
    """Все позиции \\x00<тип>\\x00, для каждой — имя и хвост перед типом."""
    # все позиции \x00<тип>\x00
    out = []
    for ty in TYPES:
        needle = b'\x00' + ty + b'\x00'
        s = 0
        while True:
            s = b.find(needle, s)
            if s < 0:
                break
            tpos = s + 1                      # первая буква типа
            # структура:  <ИМЯ> \x00 <OWNER> \x00 <ТИП> \x00
            if tpos < 1 or b[tpos - 1] != 0:
                s += 1
                continue
            p = b.rfind(b'\x00', max(0, tpos - 220), tpos - 1)  # конец имени
            if p <= 0:
                s += 1
                continue
            p0 = b.rfind(b'\x00', max(0, p - 220), p)           # конец пред. поля
            sname = p0 + 1 if p0 >= 0 else 0
            tail = b[p + 1:tpos - 1]           # OWNER между именем и типом
            out.append((sname, p, b[sname:p], tail, ty.decode()))
            s += 1
    out.sort(key=lambda r: r[0])
    return out


for fp in (r'Z:\PTC\Work\00080\00080-03.prt.1',
           r'Z:\PTC\Work\00132\00132.prt.1',
           r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
    if not os.path.exists(fp):
        continue
    raw = open(fp, 'rb').read()
    t = toc_of(raw)
    if 'MdlStatus' not in t:
        continue
    o, l = t['MdlStatus']
    b = raw[o:o + l]
    recs = records(b)
    print('\n== %s  записей=%d' % (os.path.basename(fp), len(recs)))

    # раскладка хвоста: сколько байт, начинается ли на f6
    shapes = {}
    for sname, e, name, tail, ty in recs:
        key = (len(tail), tail[:1] == b'\xf6')
        shapes.setdefault(key, []).append((name, tail, ty))
    for k in sorted(shapes):
        v = shapes[k]
        print('   хвост %d байт, f6=%s : %d записей'
              % (k[0], k[1], len(v)))
        for name, tail, ty in v[:3]:
            try:
                nm = name.decode('utf-8')
            except UnicodeDecodeError:
                nm = repr(name)
            print('       %-26r tail=%-14s %s'
                  % (nm[:24], tail.hex(' '), ty))

    # проверка: длина OWNER согласуется с первым байтом (схема varint)
    rule_ok = 0
    lens = {}
    for sname, p, name, tail, ty in recs:
        lens[len(tail)] = lens.get(len(tail), 0) + 1
        if not tail:
            continue
        b0 = tail[0]
        want = 1 if b0 < 0x80 else (2 if b0 < 0xC0 else 3)
        if want == len(tail):
            rule_ok += 1
    print('   длины OWNER: %s' % sorted(lens.items()))
    print('   совпало со схемой varint (<80:1, <C0:2, иначе 3): %d / %d'
          % (rule_ok, len(recs)))
    # расхождения — по первому байту
    odd = {}
    for sname, p, name, tail, ty in recs:
        if not tail:
            continue
        b0 = tail[0]
        want = 1 if b0 < 0x80 else (2 if b0 < 0xC0 else 3)
        if want != len(tail):
            odd.setdefault((hex(b0), len(tail)), 0)
            odd[(hex(b0), len(tail))] += 1
    if odd:
        print('   расхождения (байт, фактич.длина): %s'
              % sorted(odd.items(), key=lambda x: -x[1])[:8])

