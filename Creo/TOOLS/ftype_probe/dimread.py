# -*- coding: utf-8 -*-
"""РАЗМЕРЫ «В ЛОБ» — долг: таблица размеров детали.
Секция FullMData; поля (видны в схеме файла):
  dim_array · dtl_named_item · dtl_item · dim_type · dim_dat_ptr · bck_value
  tol_ptr · tol_type · digits · tol_class · tol_table_index
  nominal_value · override_value · bound · datum_def_id · places_denom
  attach_ptr · parent_dim_id · symbol · line_array · text_array
Запуск: python dimread.py <файл.prt.1>
Вывод: dimread_out.txt
"""
import re, sys, io, os, collections, struct

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')
DIM_FIELDS = ['nominal_value', 'dim_type', 'digits', 'tol_class', 'tol_table_index',
              'override_value', 'bound', 'places_denom', 'datum_def_id',
              'dim_array', 'dtl_named_item', 'dtl_item', 'attach_ptr',
              'parent_dim_id', 'symbol', 'dim_dat_ptr', 'tol_ptr', 'tol_type']

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def be(b):
    return struct.unpack('>d', b)[0] if len(b) == 8 else None

def packed(b):
    """Упакованное число: старший байт + E:F12 (известный формат)."""
    if len(b) < 2:
        return None
    try:
        e = (b[1] & 0xF0) >> 4
        f = ((b[1] & 0x0F) << 8) | b[2]
        return 2 ** (e + 1) * (1 + f / 4096.0)
    except Exception:
        return None

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('dimread_out.txt', 'w', encoding='utf-8')

    # границы секции FullMData
    m = re.search(rb'\n#FullMData[\r\n]', data)
    if m:
        start = m.end()
        nxt = re.search(rb'\n#[A-Za-z_][A-Za-z0-9_]{2,30}[\r\n]', data[start:])
        end = start + (nxt.start() if nxt else 40000)
    else:
        start, end = 0, len(data)
    out.write('ФАЙЛ %s (%d байт)\n' % (os.path.basename(path), len(data)))
    out.write('секция FullMData: %d..%d (%d байт)\n\n' % (start, end, end - start))

    chunk = data[start:end]
    fields = [(m.start(), m.group(1)[0], m.group(2).decode('ascii', 'replace'), m.end())
              for m in FIELD.finditer(chunk)]

    out.write('ПОЛЕ             | вхождений | примеры значений\n')
    out.write('-' * 74 + '\n')
    for name in DIM_FIELDS:
        vals = []
        n = 0
        for pos, code, nm, e in fields:
            if nm != name:
                continue
            n += 1
            tail = chunk[e:e + 12]
            if code == 0x02 or tail[:1] == b'\xed':
                raw = tail[1:9] if tail[:1] == b'\xed' else tail[:8]
                v = be(raw)
                if v is not None and 1e-9 < abs(v) < 1e9:
                    vals.append('%g' % v)
                else:
                    vals.append(hx(tail[:8]))
            else:
                vals.append(hx(tail[:6]))
        if n:
            out.write('%-16s | %9d | %s\n' % (name, n, ', '.join(vals[:6])))

    # Подробный дамп первой записи dim_array
    out.write('\n=== ДАМП ЗАПИСЕЙ dim_* ===\n')
    shown = 0
    for i, (pos, code, nm, e) in enumerate(fields):
        if nm not in ('dim_array', 'dtl_named_item', 'dtl_item', 'dim_dat_ptr'):
            continue
        shown += 1
        if shown > 3:
            break
        lo = max(0, pos - 16)
        hi = min(len(chunk), pos + 220)
        out.write('\n--- %s @%+d ---\n' % (nm, pos))
        seg = chunk[lo:hi]
        for k in range(0, len(seg), 16):
            part = seg[k:k + 16]
            asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in part)
            out.write('  %08X  %s  %s\n' % (lo + k, ' '.join('%02X' % c for c in part), asc))
        out.write('  поля в окне: %s\n' % ', '.join(
            n for p, c, n, ee in fields if lo <= p < hi))
    out.close()
    print('dimread_out.txt')

def hx(b):
    return ' '.join('%02X' % c for c in b)

if __name__ == '__main__':
    main()