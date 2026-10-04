"""FEATTYPE: поля obj_id + obj_type (04.10.2026) — решающая проверка.

Найдена секция `item_names`:
    E3 E0 0A name\0 <ИМЯ>  E0 01 obj_id\0 <varint>  E0 01 obj_type\0 <БАЙТ>
    F1 F7 2E  E3 <ИМЯ>\0 <varint> 03          (сокращённая форма)

`obj_type` — число рядом с именем и ID. Проверяем по эталону CREOSON:
одинаково ли оно у фич одного типа и различно ли у разных.

Запуск: python ftype_obj.py <файл> <etalon.json>
"""
import json, io, sys
from collections import defaultdict

FIELD_ID = b'\xe0\x01obj_id\x00'
FIELD_TYPE = b'\xe0\x01obj_type\x00'


def dec(b, k):
    b0 = b[k]
    tag = b0 & 0xC0
    if tag == 0xC0:
        return ((b0 & 0x3F) << 16) | (b[k+1] << 8) | b[k+2], 3
    if tag == 0x80:
        return ((b0 & 0x7F) << 8) | b[k+1], 2
    return b0, 1


def read_cstr(b, k):
    st = k
    while k < len(b) and b[k] != 0:
        k += 1
    return b[st:k], k


def main():
    path, meta = sys.argv[1], sys.argv[2]
    b = open(path, 'rb').read()
    fl = json.load(io.open(meta, encoding='utf-8'))['data']['featlist']
    byid = dict((f['feat_id'], f) for f in fl)

    # полная форма: <имя>\0 ... obj_id\0 <varint> ... obj_type\0 <байт>
    pairs = {}
    s = 0
    while True:
        i = b.find(FIELD_ID, s)
        if i < 0:
            break
        s = i + 1
        j = i + len(FIELD_ID)
        try:
            oid, w = dec(b, j)
        except IndexError:
            continue
        t = b.find(FIELD_TYPE, j)
        if t < 0 or t - i > 60:
            continue
        # между obj_id и obj_type не должно быть других полей
        if FIELD_TYPE[:6] not in b[j + w:t]:
            continue
        pairs[oid] = b[t + len(FIELD_TYPE)]

    print('файл: %s' % path)
    print('записей obj_id+obj_type: %d, из них в эталоне: %d'
          % (len(pairs), len([k for k in pairs if k in byid])))

    type2val = defaultdict(lambda: defaultdict(int))
    for oid, val in sorted(pairs.items()):
        f = byid.get(oid)
        if not f:
            continue
        type2val[f['type']][val] += 1
        print('  %-22s %-20s obj_type=0x%02X (%d)'
              % (f['name'][:22], f['type'][:20], val, val))

    print('\n=== СОГЛАСОВАННОСТЬ: эталонный тип -> obj_type ===')
    good = bad = 0
    for t in sorted(type2val):
        d = type2val[t]
        if len(d) == 1:
            good += 1
            print('  ✅ %-24s -> 0x%02X (%d)' % (t, list(d)[0], list(d.values())[0]))
        else:
            bad += 1
            print('  ❌ %-24s -> %s' % (t, ', '.join(
                '0x%02X(%d)' % (k, v) for k, v in d.items())))
    print('\nоднозначных: %d, неоднозначных: %d' % (good, bad))


if __name__ == '__main__':
    main()