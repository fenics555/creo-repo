"""Формат записи фичи: одинаков ли в Creo 9 и Creo 3.0?

КЛЮЧЕВОЕ: байты F6 и C0 — НЕ текст. Декодируя блок как UTF-8, мы их теряем
(заменяются на U+FFFD). Поэтому ищем ПО БАЙТАМ, но кириллицу матчим ПАРАМИ:
[\xd0-\xd1][\x80-\xbf] = ровно один символ UTF-8.
"""
import re, os

TYPES = (rb'featssrf', rb'cutextrude', rb'featround', rb'protrevolve',
         rb'feathole', rb'featsketch', rb'group', rb'dtmplane', rb'csys')

CYR = rb'[\xd0-\xd1][\x80-\xbf]'      # один символ кириллицы (2 байта)
# БЫЛА ОШИБКА: CYR вставлялась внутрь [ ... ], и это превращалось в требование
# «[A-Za-z|d0|d1], затем [80-bf]» — два байта подряд. Правильно — альтернатива.
FIRST = rb'(?:[A-Za-z]|' + CYR + rb')'
WORD = rb'[\w \-]' + CYR
NTB = re.compile(
    rb'(' + FIRST + WORD + rb'{1,28}?)\x00(?:\xf6\x00)?'
    rb'(' + rb'|'.join(TYPES) + rb')\x00'
    rb'(' + WORD + rb'{1,34}?)\x00')


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


# --- сначала проверяем регулярку на ЭТАЛОНЕ, который точно есть в 137 ---
# ВАЖНО: литерал \xf6 нельзя кодировать в UTF-8 — получится c3 b6 (2 байта).
# В файле байт ОДИН. Поэтому эталон собираем из БАЙТОВ.
S = (b'Split Surface 1\x00\xf6\x00featssrf\x00'
     b'Split_surface id 35186\x00')
print('эталон, %d байт: %s' % (len(S), S[:24].hex(' ')))
for pat, lbl in (
        (rb'([A-Za-z][\w \-]{1,28})\x00\xf6\x00(featssrf)\x00', 'A строгий'),
        (rb'([\w ]+?)\x00\xf6\x00featssrf\x00', 'B ленивый'),
        (rb'([\w ]+)\x00\xf6\x00featssrf\x00', 'C жадный'),
        (rb'([\w ]+?)\x00(?:\xf6\x00)?featssrf\x00', 'D опц.')):
    m = re.search(pat, S)
    print('   %-12s %s' % (lbl, repr(m.group(1)) if m else 'НЕТ'))
print()
m = NTB.search(S)
print('   NTB на эталоне: %s' % (repr(m.group(1)) if m else 'НЕТ'))
print('   NTB групп: %d' % NTB.groups)
sys.exit(0)

print('%-24s %-8s %-7s %s' % ('ФАЙЛ', 'записей', 'уник', 'типы'))
print('-' * 84)
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