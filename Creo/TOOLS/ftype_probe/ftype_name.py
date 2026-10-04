"""FEATTYPE: связь фичи с именем прототипа (правильный тест, 04.10.2026).

⚠️ ПРЕДЫДУЩИЙ ТЕСТ БЫЛ НЕВЕРНЫМ: он искал ОДИН И ТОТ ЖЕ байт у всех фич
одного типа. Но тип закодирован НЕ числом, а ИМЕНЕМ (`dtmplane`) переменной
длины — такой тест не мог сработать в принципе.

Здесь ищем ИМЯ ПРОТОТИПА в окне вокруг записи фичи и проверяем согласованность:
все фичи одного эталонного типа должны отображаться в ОДИН прототип.

Запуск: python ftype_name.py <файл> <etalon.json>
"""
import json, io, re, sys
from collections import defaultdict

WIN = 120          # байт после записи фичи
PROTO_RE = re.compile(
    rb'(?:prot|dtm|cut|proj|hole|fillet|chamf|shell|draft|pattern|rib|'
    rb'merge|dome|pipe|axis|mirror|trim|surf)[a-z0-9_]{2,28}')


def dec(b, k):
    b0 = b[k]
    tag = b0 & 0xC0
    if tag == 0xC0:
        return ((b0 & 0x3F) << 16) | (b[k+1] << 8) | b[k+2], 3
    if tag == 0x80:
        return ((b0 & 0x7F) << 8) | b[k+1], 2
    return b0, 1


def record_positions(b, fid):
    """Позиции ID фичи в обеих формах записи."""
    if fid < 0x80:
        pat = bytes([fid])
    elif fid < 0x4000:
        pat = bytes([0x80 | ((fid >> 8) & 0x7F), fid & 0xFF])
    else:
        pat = bytes([0xC0 | ((fid >> 16) & 0x3F), (fid >> 8) & 0xFF,
                     fid & 0xFF])
    out = []
    s = 0
    while True:
        p = b.find(pat, s)
        if p < 0:
            break
        s = p + 1
        if p >= 3 and b[p-3:p] == b'\x00\x01\x00':
            out.append(p)                      # форма A
        elif p >= 1 and b[p-1] == 0xE3:
            out.append(p)                      # форма B
    return out


def main():
    path, meta = sys.argv[1], sys.argv[2]
    b = open(path, 'rb').read()
    fl = json.load(io.open(meta, encoding='utf-8'))['data']['featlist']

    type2proto = defaultdict(lambda: defaultdict(int))   # тип -> прототип -> раз
    found = 0
    print('файл: %s' % path)
    for f in fl:
        hits = {}
        for p in record_positions(b, f['feat_id']):
            win = b[p:p + WIN]
            for m in PROTO_RE.finditer(win):
                name = m.group().decode('latin-1')
                hits[name] = hits.get(name, 0) + 1
        if not hits:
            continue
        found += 1
        # берём самый частый прототип рядом с записью
        best = max(hits.items(), key=lambda kv: kv[1])[0]
        type2proto[f['type']][best] += 1
        print('  %-22s %-20s -> %s' % (f['name'][:22], f['type'][:20], best))

    print('\n=== СОГЛАСОВАННОСТЬ: эталонный тип -> прототип ===')
    good = bad = 0
    for t in sorted(type2proto):
        d = type2proto[t]
        if len(d) == 1:
            good += 1
            print('  ✅ %-22s -> %s' % (t, list(d)[0]))
        else:
            bad += 1
            print('  ❌ %-22s -> %s' % (t, ', '.join(
                '%s(%d)' % (k, v) for k, v in d.items())))
    print('\nоднозначных типов: %d, неоднозначных: %d, фич обработано: %d'
          % (good, bad, found))


if __name__ == '__main__':
    main()