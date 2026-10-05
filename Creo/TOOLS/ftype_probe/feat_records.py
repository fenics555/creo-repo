"""Разбор записей фичи в MdlStatus — детерминированный, без regex.

Шаблон одинаков в Creo 3.0 и Creo 9. Маркер e3 c0 НЕ нужен — он есть только
в 137 (Creo 3.0), в Creo 9 его нет, а формат записи тот же:

    e3 <id varint> <код>  f6 <prev varint> <ИМЯ> \\x00
                          <OWNER varint> <is_header> <ТИП> \\x00
                          [<ИМЯ> id <N>] \\x00

Схема varint (подтверждена на sort_feat_ids и на owner):
    <0x80     → 1 байт  = значение            (67        → 103)
    0x80..BF  → 1 байт  после префикса        (80 93     → 147)
    0xC0..FF  → 2 байта после префикса        (c0 89 72  → 35186)

ГДЕ Я ОШИБАЛСЯ РАНЬШЕ — три ловушки подряд:
  1. Regex брал varint-префикс в состав имени, если тот попадал в ASCII,
     и давал мусор «gDTM1», «rSplit Surface 2», «fОТВЕРСТИЕ 1».
  2. После имени НЕТ \\x00 — сразу OWNER, затем is_header, затем тип.
     Фильтр «b[e+1]==\\x00» отбрасывал записи с is_header=01.
  3. Кириллицу в байтовом regex нельзя писать классом [\\xd0-\\xd1]: это
     два байта одного символа, нужна альтернатива (?:...|...).

Проверка смысла: prev указывает на id ПРЕДЫДУЩУЙ фичи.
    137: «Split_surface id 35186», следующая запись начинается с c0 89 72
    = 35186.  Это prev_feat_id — поле, которое раньше не извлекалось.
"""
import os
import re

TYPES = (b'featssrf', b'cutextrude', b'featround', b'protrevolve',
         b'feathole', b'featsketch', b'group', b'dtmplane', b'csys',
         b'featpattern', b'featdim', b'featinst', b'featshell',
         b'featmirror', b'featmerge', b'copygeom')

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
    """(длина, значение) или None. p — позиция первого байта."""
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



def record_id(b, f6):
    """(id, код) записи — читаются НАЗАД от метки f6.

    Раскладка:  <id varint> <код varint> f6 <prev varint> <ИМЯ> ...
    Длины varint заранее неизвестны, поэтому перебираем 1..3 и требуем,
    чтобы разбор кончался ровно на границе.  Значение при этом не хрупкое:
    если истинная длина 2 (80 93 -> 0x93), то вариант длины 1 отбрасывается,
    потому что 0x93 >= 0x80 и разбор даст 2, а не 1.
    """
    for lc in (1, 2, 3):
        cs = f6 - lc
        if cs < 0:
            continue
        rc = read_varint(b, cs)
        if rc is None or rc[0] != lc:
            continue
        for li in (1, 2, 3):
            i0 = cs - li
            if i0 < 0:
                continue
            ri = read_varint(b, i0)
            if ri is None or ri[0] != li:
                continue
            return ri[1], rc[1]
    return None


def parse_feats(b):
    """Записи фичи из MdlStatus.

    f6 — метка строкового поля: f6 <varint> <строка> \\x00.  Ищем от неё,
    чтобы не гадать, где начинается имя.  Фильтр ложных срабатываний
    (например, «group» внутри pat_group_header_id) — известный тип сразу
    после owner+is_header.
    """
    out = []
    i = 0
    n = len(b)
    while True:
        i = b.find(b'\xf6', i)
        if i < 0:
            break
        r = read_varint(b, i + 1)
        if r is None:
            break
        k, prev = r
        s = i + 1 + k                       # начало имени
        if s >= n:
            break
        e = b.find(b'\x00', s)
        if e < 0 or e == s:                 # пустое имя — не запись фичи
            i += 1
            continue

        # после имени: OWNER varint, is_header, ТИП \x00
        # Две раскладки: (a) тип приходит как строка f6 <id>; (b) обычную
        # owner+is_header.  Ветку помечаем — она нужна для статистики.
        q = e + 1
        if q < n and b[q] == 0xf6:          # тип приходит как строка f6
            r2 = read_varint(b, q + 1)
            if r2 is None:
                i += 1
                continue
            k2, owner = r2
            hdr, t0, br = None, q + 1 + k2, 'str'
        else:
            r2 = read_varint(b, q)
            if r2 is None:
                i += 1
                continue
            k2, owner = r2
            if q + k2 >= n:
                i += 1
                continue
            hdr, t0, br = b[q + k2], q + k2 + 1, 'plain'

        for ty in TYPES:
            if b.startswith(ty + b'\x00', t0):
                break
        else:
            i += 1                          # это не запись фичи
            continue

        try:
            name = b[s:e].decode('utf-8')
        except UnicodeDecodeError:
            i += 1
            continue

        # после типа: [<имя> id <N>] \x00 — id есть не у всех типов
        # u0 указывает на \x00, закрывающий тип, поэтому ищем СЛЕДУЮЩИЙ
        f_id, feat_id = b'', None
        u0 = t0 + len(ty)
        u1 = b.find(b'\x00', u0 + 1)
        if u1 > u0 + 1:
            f_id = b[u0 + 1:u1]
            try:
                m = ID_RE.search(f_id.decode('utf-8'))
                if m:
                    feat_id = int(m.group(1))
            except UnicodeDecodeError:
                pass

        out.append({'prev': prev, 'owner': owner, 'is_header': hdr,
                    'branch': br, 'name': name, 'type': ty.decode(),
                    'id': feat_id,
                    'id_field': f_id.decode('utf-8', 'replace'),
                    'f6_off': i, 'name_off': s})
        i = u0
    return out


def section(path, name='MdlStatus'):
    """Байты секции из TOC или None."""
    raw = open(path, 'rb').read()
    t = toc_of(raw)
    if name not in t:
        return None
    o, l = t[name]
    return raw[o:o + l]


def scan(path, verbose=True):
    b = section(path)
    if b is None:
        return None
    feats = parse_feats(b)
    if not verbose:
        return feats
    ids = {f['id']: f for f in feats if f['id'] is not None}
    linked = sum(1 for f in feats if f['prev'] in ids)
    heads = sum(1 for f in feats if f['is_header'] == 1)
    brs = {}
    for f in feats:
        brs[f['branch']] = brs.get(f['branch'], 0) + 1
    print('  %-24s записей=%-4d уник=%-4d id=%-4d prev->id=%-4d '
          'заголовков=%d ветки=%s'
          % (os.path.basename(path), len(feats),
             len({f['name'] for f in feats}), len(ids), linked, heads,
             sorted(brs.items())))
    for f in feats[:8]:
        print('      prev=%-6s own=%-6s hdr=%-4s id=%-6s %-20r %-11s'
              % (f['prev'], f['owner'], f['is_header'], f['id'],
                 f['name'], f['type']))
    return feats


if __name__ == '__main__':
    print('=== записи фичи (Creo 3.0 и Creo 9 — один формат) ===')
    for fp in (r'Z:\PTC\Work\00080\00080-03.prt.1',
               r'Z:\PTC\Work\00132\00132.prt.1',
               r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'):
        if os.path.exists(fp):
            scan(fp)

