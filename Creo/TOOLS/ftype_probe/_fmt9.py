"""Формат записи фичи: одинаков ли в Creo 9 и Creo 3.0?

Маркер e3 c0 в Creo 9 отсутствует, но САМ шаблон имени+типа совпадает:
    137:        Split Surface 1 \x00 \xf6\x00 featssrf \x00 Split_surface id 35186 \x00
    00080-03:   ОТВЕРСТИЕ 1   \x00 \xf6\x00 feathole  \x00 ОТВЕРСТИЕ  id 147 \x00

Поэтому ищем ПО БАЙТАМ, но кириллицу матчим ПАРАМИ байтов:
    [\xd0-\xd1][\x80-\xbf] = ровно один символ UTF-8.

Две ошибки, из-за которых давалось 0 и мусор:
  1. CYR — это ДВА байта. Вставлять её внутрь [ ... ] нельзя: класс станет
     «[A-Za-z|d0|d1]», и следующий байт потребуется вдобавок. Нужен (?:...|...).
  2. \xf6 нельзя кодировать в UTF-8 литералом 'ö' — в файле байт один (0xf6),
     а в UTF-8 он два (c3 b6). Строковый разбор (str) поэтому всегда 0.
"""
import re
import os
import sys

TYPES = (b'featssrf', b'cutextrude', b'featround', b'protrevolve',
         b'feathole', b'featsketch', b'group', b'dtmplane', b'csys',
         b'featpattern', b'featdim')

CYR = rb'[\xd0-\xd1][\x80-\xbf]'            # один символ кириллицы = 2 байта
# альтернатива: ASCII-символ ЛИБО один символ кириллицы
CHAR = rb'(?:[A-Za-z0-9_]|' + CYR + rb')'
# первый символ имени: буква (ASCII или кириллица)
FIRST = rb'(?:[A-Za-z]|' + CYR + rb')'
# тело имени: символ ЛИБО кириллица — не конкатенация!
BODY = rb'(?:[\w \-]|' + CYR + rb')'

NTB = re.compile(
    rb'(' + FIRST + BODY + rb'{1,28}?)\x00(?:\xf6\x00)?'
    rb'(' + rb'|'.join(TYPES) + rb')\x00'
    rb'(' + BODY + rb'{1,34}?)\x00')


def toc_of(raw):
    i = raw.find(b'#UGC_TOC')
    j = raw.find(b'\n', i) + 1
    e = raw.find(b'NEXT_TOC_ENTRY', j)
    blob = raw[j:e if e > 0 else j + 12000]
    t = {}
    for mm in re.finditer(
            rb'^([A-Za-z_][A-Za-z0-9_]*)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+'
            rb'([0-9a-f]+)\s+[0-9a-f]+\s+[0-9a-zA-Z_]+\s+(-?[0-9a-f]+)',
            blob, re.M):
        t[mm.group(1).decode()] = (int(mm.group(2), 16), int(mm.group(3), 16))
    return t


# --- 1. ЭТАЛОН: проверка регулярки на заведомо известной записи ---
# Литерал \xf6 собираем из БАЙТОВ: 'ö' в UTF-8 это c3 b6, а в файле 0xf6.
S = (b'Split Surface 1\x00\xf6\x00featssrf\x00'
     b'Split_surface id 35186\x00')
print('эталон %d байт: %s' % (len(S), S[:26].hex(' ')))
m = NTB.search(S)
print('  NTB на эталоне: %s' % (repr(m.group(1)) if m else 'НЕТ'))
print()

# --- 2. Реальные файлы ---
print('%-24s %-8s %-7s %s' % ('ФАЙЛ', 'записей', 'уник', 'типы'))
print('-' * 84)
for fp in (r'Z:\PTC\Work\00080\00080-03.prt.1',
           r'Z:\PTC\Work\00132\00132.prt.1',
           r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
    if not os.path.exists(fp):
        print('  НЕТ: %s' % fp)
        continue
    raw = open(fp, 'rb').read()
    t = toc_of(raw)
    if 'MdlStatus' not in t:
        continue
    o, l = t['MdlStatus']
    b = raw[o:o + l]
    hits = list(NTB.finditer(b))
    uniq, seen = [], set()
    for m in hits:
        try:
            n = m.group(1).decode('utf-8').strip()
        except Exception:
            continue
        if n and n not in seen:
            seen.add(n)
            uniq.append((n, m.group(2).decode()))
    types = {}
    for _, ty in uniq:
        types[ty] = types.get(ty, 0) + 1
    print('%-24s %-8d %-7d %s'
          % (os.path.basename(fp), len(hits), len(uniq),
             sorted(types.items(), key=lambda x: -x[1])))
    print('    примеры: %s' % [x[0] for x in uniq[:6]])
