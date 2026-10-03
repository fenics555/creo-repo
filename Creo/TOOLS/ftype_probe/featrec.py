# -*- coding: utf-8 -*-
"""ПОЛНЫЙ ПАРСЕР ЗАПИСЕЙ FeatDefs: id + type + поля, с выводом в таблицу.
Ищет закономерность type <-> feat_name и собирает дерево по parent/prev.
Запуск: python featrec.py <файл> [<_recs.dat для дерева>]
Вывод: featrec_out.txt
"""
import re, sys, io, os

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def section(data, name):
    m = re.search(rb'\n#' + name.encode() + rb'[\r\n]', data)
    if not m:
        return None
    start = m.end()
    nxt = re.search(rb'\n#[A-Za-z_][A-Za-z0-9_]{2,30}[\r\n]', data[start:start + 4_000_000])
    end = start + (nxt.start() if nxt else len(data) - start)
    return start, end

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})')

def parse_records(data, start, end, marker=b'feat_defs_'):
    """[(имя_метки, абс_позиция_метки)] -> режем на блоки"""
    marks = []
    s = start
    while True:
        i = data.find(marker, s, end)
        if i < 0:
            break
        m = re.match(rb'feat_defs_([0-9]+)\x00', data[i:i + 24])
        if m:
            marks.append((i, int(m.group(1))))
        s = i + 10
    recs = []
    for k, (pos, num) in enumerate(marks):
        stop = marks[k + 1][0] if k + 1 < len(marks) else end
        recs.append((pos, stop, num, data[pos:stop]))
    return recs

def fields(chunk):
    """Список (имя, значение_байты) — значение до следующего поля-маркера E0."""
    out = []
    hits = list(FIELD.finditer(chunk))
    for k, m in enumerate(hits):
        name = m.group(2).decode('ascii', 'replace')
        vstart = m.end()
        vend = hits[k + 1].start() if k + 1 < len(hits) else len(chunk)
        out.append((name, chunk[vstart:vend]))
    return out

# коды-маркеры значения (первый байт после имени поля)
SKIP = {0xF6: 1, 0xF8: 1, 0xF7: 1, 0xFB: 1, 0x84: 1, 0xF9: 1, 0xC0: 1, 0xE1: 1, 0xE3: 1,
        0xF1: 1, 0xF2: 1, 0xE2: 1, 0xE4: 1, 0xE5: 1, 0x0A: 0}

def value(val):
    """Разбор значения поля: снять маркер, вернуть (маркер, число/строка)."""
    if not val:
        return None, ''
    b = val[0]
    rest = val[1:]
    if b == 0x00:
        return 0, '0'
    if b in SKIP:
        if b == 0x0A or b in (0xF1, 0xF2):
            # строка до NUL
            z = rest.find(b'\x00')
            st = rest[:z] if z >= 0 else rest
            try:
                s = st.decode('utf-8')
            except Exception:
                s = st.decode('cp1251', 'replace')
            return b, s
        # короткое целое: 1..2 байта BE
        n = 0
        for c in rest[:2]:
            if c in SKIP or c == 0xE0:
                break
            n = (n << 8) | c
        return b, n
    return b, rest

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('featrec_out.txt', 'w', encoding='utf-8')
    out.write('FILE %s size=%d\n' % (os.path.basename(path), len(data)))
    rng = section(data, 'FeatDefs')
    if not rng:
        out.write('нет FeatDefs\n'); out.close(); return
    start, end = rng
    out.write('FeatDefs абс.%d..%d (%d б)\n' % (start, end, end - start))
    recs = parse_records(data, start, end)
    out.write('записей feat_defs_*: %d\n\n' % len(recs))

    tstats = {}
    rows = []
    for pos, stop, num, chunk in recs:
        fs = fields(chunk)
        d = {}
        for nm, val in fs:
            mk, v = value(val)
            d[nm] = v
        if 'feat_defs_%d' % num in d:
            pass
        rows.append((pos, num, d, chunk))

    out.write('%-10s %-6s %-8s %-10s %s\n' % ('позиция', '№', 'id', 'type', 'имена'))
    tstats = {}
    for pos, num, d, chunk in rows:
        idv = d.get('id')
        ty = d.get('type')
        names = [k for k in d if 'name' in k.lower()]
        out.write('%-10d %-6d %-8s %-10s %s\n' % (pos, num, idv, ty, ','.join(names)))
        tstats.setdefault(str(ty), 0)
        tstats[str(ty)] += 1

    out.write('\n=== СТАТИСТИКА type ===\n')
    for k, v in sorted(tstats.items(), key=lambda x: -x[1]):
        out.write('  type=%-8s встречается %d\n' % (k, v))

    # сырые дампы первых записей с type
    out.write('\n=== СЫРЫЕ ЗАПИСИ (первые 6) ===\n')
    shown = 0
    for pos, num, d, chunk in rows:
        if 'type' not in d:
            continue
        out.write('--- абс.%d feat_defs_%d type=%s id=%s len=%d\n' % (pos, num, d['type'], d.get('id'), len(chunk)))
        for off in range(0, min(len(chunk), 200), 16):
            part = chunk[off:off + 16]
            out.write('%08X  %s\n' % (pos + off, ' '.join('%02X' % c for c in part)))
        fs = fields(chunk)
        out.write('  ' + ' | '.join('%s=%r' % (nm, value(val)[1]) for nm, val in fs[:24]) + '\n\n')
        shown += 1
        if shown >= 6:
            break
    out.close()
    print('featrec_out.txt records=%d' % len(rows))

if __name__ == '__main__':
    main()