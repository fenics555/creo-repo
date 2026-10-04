# -*- coding: utf-8 -*-
"""ИЗОЛЯЦИЯ вложенных структур внутри геометрических массивов.
Ищем маркеры, которые прерывают 4-байтовый ритм: E0 xx (поле) и FF-подставки.
Для каждого — измеряем длину «вставки» до возврата к ритму.
Запуск: python embfield.py <файл>
Вывод: embfield_out.txt
"""
import re, sys, io, os, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)

def main():
    path = sys.argv[1]
    data = open(path, 'rb').read()
    out = io.open('embfield_out.txt', 'w', encoding='utf-8')
    out.write('ФАЙЛ %s (%d байт)\n\n' % (os.path.basename(path), len(data)))

    # 1) все поля, встречающиеся ВНУТРИ payload'ов crv_pnt_arr
    hits = [(m.start(), m.group(1)[0], m.group(2).decode('ascii', 'replace'), m.end())
            for m in FIELD.finditer(data)]
    inner = collections.Counter()
    inner_samples = []
    inside = 0
    for i, (pos, code, nm, end) in enumerate(hits):
        if nm != 'crv_pnt_arr':
            continue
        nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
        payload = data[end:nxt]
        if not (8 <= len(payload) <= 200):
            continue
        inside += 1
        # ищем поля внутри payload
        for m in FIELD.finditer(payload):
            fld = m.group(2).decode('ascii', 'replace')
            inner[fld] += 1
            if len(inner_samples) < 12:
                seg = payload[max(0, m.start() - 12):m.end() + 20]
                inner_samples.append((fld, seg))

    out.write('payload crv_pnt_arr разобрано: %d\n' % inside)
    out.write('ПОЛЯ, найденные ВНУТРИ массива:\n')
    if inner:
        for f, c in inner.most_common(20):
            out.write('   %-28s %d\n' % (f, c))
    else:
        out.write('   (нет полей с ASCII-именем — структуры бинарные)\n')

    # 2) байтовые маркеры внутри массива
    out.write('\n=== СЫРЫЕ БЛОКИ ВОКРУГ НАЙДЕННЫХ ПОЛЕЙ ===\n')
    for fld, seg in inner_samples[:8]:
        out.write('\n  %s: %s\n' % (fld, ' '.join('%02X' % c for c in seg)))
        asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in seg)
        out.write('  %s\n' % asc)

    # 3) «разрушители ритма» во всех payload
    out.write('\n=== ЧАСТОТА БАЙТОВ ВНУТРИ МАССИВОВ (топ-20) ===\n')
    cnt = collections.Counter()
    for i, (pos, code, nm, end) in enumerate(hits):
        if nm != 'crv_pnt_arr':
            continue
        nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
        payload = data[end:nxt]
        if 8 <= len(payload) <= 200:
            cnt.update(payload)
    for b, c in cnt.most_common(20):
        out.write('   %02X : %d\n' % (b, c))

    # 4) сколько массивов содержат E0
    out.write('\n=== МАССИВЫ СО ВЛОЖЕННЫМ E0 ===\n')
    n_e0 = n_ff = n_tot = 0
    for i, (pos, code, nm, end) in enumerate(hits):
        if nm != 'crv_pnt_arr':
            continue
        nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
        payload = data[end:nxt]
        if not (8 <= len(payload) <= 200):
            continue
        n_tot += 1
        if b'\xE0' in payload[4:]:
            n_e0 += 1
        if re.search(rb'\xFF{3,}', payload[4:]):
            n_ff += 1
    out.write('   всего массивов:            %d\n' % n_tot)
    out.write('   содержат E0 (вложенное поле): %d (%.1f %%)\n' % (n_e0, 100.0 * n_e0 / max(1, n_tot)))
    out.write('   содержат FF-подставки:      %d (%.1f %%)\n' % (n_ff, 100.0 * n_ff / max(1, n_tot)))
    out.close()
    print('embfield_out.txt inside=%d inner=%d' % (inside, len(inner)))

if __name__ == '__main__':
    main()