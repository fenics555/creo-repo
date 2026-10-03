# -*- coding: utf-8 -*-
"""СОПОСТАВЛЕНИЕ obj_id (Sld_MdlStatus) с блоками данных в файле.
Цель: найти, где в файле лежит блок, соответствующий obj_id, и есть ли
рядом число, похожее на FEATTYPE (0..279).
Метод: берём obj_id из MdlStatus, ищем его 2-байтовое/1-байтовое представление
(84 <b>) во всём файле и смотрим контекст каждого вхождения.
Запуск: python objid_map.py <файл>
Вывод: objid_map_out.txt
"""
import re, sys, io, os, collections

# FEATTYPE-подобные значения 0..279 (для проверки «похоже на тип»)
def load(p):
    with open(p, 'rb') as f:
        return f.read()

def section(data, name):
    m = re.search(rb'\n#' + name.encode() + rb'[\r\n]', data)
    if not m:
        return None
    start = m.end()
    nxt = re.search(rb'\n#[A-Za-z_][A-Za-z0-9_]{2,30}[\r\n]', data[start:])
    return start, start + (nxt.start() if nxt else len(data) - start)

FIELD = re.compile(rb'([\xe0-\xff][\x00-\x0f])([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

ITEM = re.compile(rb'item_names')

def collect_objs(data):
    """Разбор блока item_names.

    Формат (установлен по байтам, din933.prt.1):
        E0 0A "name" 00 "DTM1" 00 84 7B | E0 01 "obj_id" 00 05 | ...
        E3 "DTM2" 00 84 7D 05
        E3 "DTM3" 00 84 7F 05
        E3 "A_1"  00 84 B1 15
    Т.е. имена полей здесь = СХЕМА (встречается 1 раз), а дальше идут
    ПОЗИЦИОННЫЕ записи: <E3> <имя\\0> <ID: 84/85 + байт(ы)> <код типа>.
    """
    res = []
    m = ITEM.search(data)
    if not m:
        return res
    lo = m.start()
    chunk = data[lo:lo + 3000]
    # позиционные записи: E3 <имя> 00 <84|85|86..> <байты> <код типа>
    pat = re.compile(rb'\xE3([A-Za-z0-9_\-\.]{1,40})\x00(.)(.)\x00?')
    for mm in pat.finditer(chunk):
        nm = mm.group(1).decode('ascii', 'replace')
        idmark = mm.group(2)[0]
        idval = mm.group(3)[0]
        # код типа: байт после ID (для 1-байтовых ID)
        rest = chunk[mm.end():mm.end() + 4]
        tcode = rest[0] if rest else None
        if idmark in (0x84, 0x85, 0x86, 0x87, 0x88, 0x89):
            res.append((idmark, idval, nm, tcode, lo + mm.start()))
    return res

def find_id_occurrences(data, val, marker=0x84):
    """Все позиции, где встречается 84 <val>."""
    pat = bytes([marker, val])
    out = []
    s = 0
    while True:
        i = data.find(pat, s)
        if i < 0:
            break
        out.append(i)
        s = i + 1
    return out

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('objid_map_out.txt', 'w', encoding='utf-8')
    out.write('FILE %s size=%d\n\n' % (os.path.basename(path), len(data)))

    objs = collect_objs(data)
    out.write('=== НАЙДЕНО записей в блоке item_names: %d ===\n' % len(objs))
    out.write('%-6s %-6s %-16s %-9s %-10s %s\n'
              % ('марк', 'ID', 'имя', 'код_тип', 'позиция', 'вхождений марк+ID'))
    table = []
    for idmark, idval, nm, t, pos in objs:
        occ = find_id_occurrences(data, idval, marker=idmark)
        table.append((idmark, idval, nm, t, pos, occ))
        out.write('0x%02X   0x%02X   %-16s %-9s %-10d %d %s\n' % (
            idmark, idval, nm[:16], t if t is not None else '-', pos, len(occ),
            ('@' + ','.join(str(x) for x in occ[:8])) if occ else ''))

    # Анализ: в каких секциях встречаются эти ID
    out.write('\n=== В КАКИХ СЕКЦИЯХ ВСТРЕЧАЮТСЯ obj_id ===\n')
    secs = []
    for m in re.finditer(rb'\n#([A-Za-z_][A-Za-z0-9_]{2,30})[\r\n]', data):
        secs.append((m.end(), m.group(1).decode()))
    secs.sort()

    def sec_of(pos):
        cur = '(до начала)'
        for s, n in secs:
            if s <= pos:
                cur = n
            else:
                break
        return cur

    counter = collections.Counter()
    for idmark, idval, nm, t, pos, occ in table:
        for o in occ:
            counter[sec_of(o)] += 1
    for s, c in counter.most_common(25):
        out.write('  %-22s %d вхождений\n' % (s, c))

    out.write('\n=== ДЕТАЛЬНО ПО ПЕРВЫМ 5 ID: контекст вхождений ===\n')
    for idmark, idval, nm, t, pos, occ in table[:5]:
        out.write('\n--- ID 0x%02X 0x%02X  "%s"  код_тип=%s  всего вхождений=%d ---\n'
                  % (idmark, idval, nm, t, len(occ)))
        for o in occ[:6]:
            lo = max(0, o - 60)
            chunk = data[lo:o + 60]
            fl = [(mm.start() + lo, mm.group(2).decode('ascii', 'replace'))
                  for mm in FIELD.finditer(chunk)]
            out.write('  @%d секция=%s\n' % (o, sec_of(o)))
            out.write('    hex: %s\n' % ' '.join('%02X' % c for c in chunk))
            out.write('    поля: %s\n' % ', '.join(n for _, n in fl))
            # числа 1..3 байт после позиции
            nums = []
            for L in (1, 2):
                for k in range(o + 2, min(o + 12, len(data) - L)):
                    v = int.from_bytes(data[k:k + L], 'big')
                    if 0 < v <= 279:
                        nums.append('+%d:%d' % (k - o, v))
            out.write('    числа 0..279 рядом: %s\n' % (', '.join(nums[:10]) or 'нет'))
    out.close()
    print('objid_map_out.txt objs=%d' % len(objs))

if __name__ == '__main__':
    main()