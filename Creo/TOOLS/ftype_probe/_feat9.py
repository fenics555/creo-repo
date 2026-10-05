"""Разбор записей фичи в MdlStatus — БЕЗ regex, детерминированно.

Шаблон имени+типа одинаков в Creo 3.0 и Creo 9:
    <prev_feat_id varint> <ИМЯ> \x00 \xf6\x00 <ТИП> \x00 ...

Маркер e3 c0 в Creo 9 отсутствует, поэтому он не нужен.

КЛЮЧЕВОЕ: перед именем стоит varint = prev_feat_id, а НЕ байт имени.
Причина, из-за которой regex давал мусор «gDTM1», «rSplit Surface 2»:
varint длинной 1 байт (<0x80) — это просто значение, и если оно попадает
в диапазон ASCII-букв, regex принимал его за начало имени.

Схема varint (подтверждена на sort_feat_ids):
    <0x80     → 1 байт  = значение          (67      → 103)
    0x80..BF  → 1 байт  после префикса      (80 93   → 147)
    0xC0..FF  → 2 байта после префикса      (c0 89 72 → 35186)

Проверка смысла: префикс указывает на id ПРЕДЫДУЩУЙ фичи в файле.
    137: «Split_surface id 35186», следующая запись начинается с c0 89 72 = 35186.
Это и есть prev_feat_id — поле, которое раньше не извлекалось.
"""
import os
import re
import sys

TYPES = (b'featssrf', b'cutextrude', b'featround', b'protrevolve',
         b'feathole', b'featsketch', b'group', b'dtmplane', b'csys',
         b'featpattern', b'featdim', b'featinst')

ID_RE = re.compile(r' id (\d+)$')


def toc_of(raw):
    """Секции из #UGC_TOC: имя -> (смещение, длина)."""
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


def read_varint(b, p):
    """Возвращает (длина, значение) или None. p — позиция первого байта."""
    if p >= len(b):
        return None
    b0 = b[p]
    if b0 < 0x80:
        return 1, b0
    if b0 < 0xC0:
        if p + 1 >= len(b):
            return None
        return 2, b[p + 1]
    if p + 2 >= len(b):
        return None
    return 3, (b[p + 1] << 8) | b[p + 2]


def parse_feats(b):
    """Все записи фичи: список dict(prev, name, type, id, name_off).

    Запись:  <prev varint> <ИМЯ> \\x00 \\xf6\\x00 <ТИП> \\x00 <поле id> \\x00
    Якорь — завершение: <ИМЯ> \\x00 \\xf6\\x00 <ТИП> \\x00.
    Вперёд идём от \\xf6, длину varint читаем по его первому байту.
    """
    out = []
    i = 0
    n = len(b)
    while True:
        i = b.find(b'\xf6', i)
        if i < 0:
            break
        p = i + 1
        r = read_varint(b, p)
        if r is None:
            break
        k, pid = r
        s = p + k                      # здесь начинается имя
        if s >= n:
            break
        e = b.find(b'\x00', s)
        if e < 0 or e == s:            # пустое имя — не запись фичи
            i += 1
            continue
        if b[e + 1:e + 3] != b'\xf6\x00':   # после имени должен идти \xf6\x00
            i += 1
            continue
        t0 = e + 3
        t1 = b.find(b'\x00', t0)
        if t1 < 0:
            i += 1
            continue
        typ = b[t0:t1]
        if typ not in TYPES:
            i += 1
            continue
        raw_name = b[s:e]
        try:
            name = raw_name.decode('utf-8')
        except UnicodeDecodeError:
            i += 1
            continue
        # поле id идёт СЛЕДУЮЩИМ после типа: «<имя> id <N>» либо просто имя
        f_id, feat_id = b'', None
        u1 = b.find(b'\x00', t1 + 1)
        if u1 > t1 + 1:
            f_id = b[t1 + 1:u1]
            try:
                m = ID_RE.search(f_id.decode('utf-8'))
                if m:
                    feat_id = int(m.group(1))
            except UnicodeDecodeError:
                pass
        out.append({'prev': pid, 'name': name, 'type': typ.decode(),
                    'id': feat_id, 'id_field': f_id.decode('utf-8', 'replace'),
                    'name_off': s})
        i = t1
    return out


def scan(path, verbose=True):
    raw = open(path, 'rb').read()
    t = toc_of(raw)
    if 'MdlStatus' not in t:
        return None
    o, l = t['MdlStatus']
    b = raw[o:o + l]
    feats = parse_feats(b)
    ids = {}
    for f in feats:
        if f['id'] is not None:
            ids[f['id']] = f
    linked = sum(1 for f in feats if f['prev'] in ids)
    if verbose:
        groups = sum(1 for f in feats if f['type'] == 'group')
        print('  %-24s записей=%-4d уник=%-4d id=%-4d prev->id=%-4d групп=%d'
              % (os.path.basename(path), len(feats),
                 len({f['name'] for f in feats}), len(ids), linked, groups))
        for f in feats[:8]:
            print('      prev=%-6s id=%-6s %-22r %-11s field=%r'
                  % (f['prev'], f['id'], f['name'], f['type'], f['id_field']))
    return feats


if __name__ == '__main__':
    print('=== разбор записей фичи (без regex) ===')
    for fp in (r'Z:\PTC\Work\00080\00080-03.prt.1',
               r'Z:\PTC\Work\00132\00132.prt.1',
               r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
        if os.path.exists(fp):
            scan(fp)
