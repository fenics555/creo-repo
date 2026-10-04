"""Сверка фич из эталонного JSON (CREOSON) с байтами файла.

Ищет запись каждой фичи по имени (UTF-8 и латиница) и печатает байты
после ID — так ищется числовой FEATTYPE: у фич одного типа хвост должен
совпадать, у разных — отличаться.

Запуск: python feat_probe2.py <файл> <etalon.json> [макс]
"""
import json, io, sys


def dec(b, k):
    b0 = b[k]
    tag = b0 & 0xC0
    if tag == 0xC0:
        return ((b0 & 0x3F) << 16) | (b[k+1] << 8) | b[k+2], 3
    if tag == 0x80:
        return ((b0 & 0x7F) << 8) | b[k+1], 2
    return b0, 1


def find_feat(b, name):
    """Ищет запись `<имя>\\0 01 00 [18 E5] <varint>`. Возвращает (id, хвост) или None."""
    nb = name.encode('utf-8')
    start = 0
    while True:
        i = b.find(nb, start)
        if i < 0:
            return None
        start = i + 1
        k = i + len(nb)
        if b[k:k + 3] == b'\x00\x01\x00':
            p = k + 3
            if b[p:p + 2] == b'\x18\xe5':
                p += 2
            try:
                fid, w = dec(b, p)
            except IndexError:
                continue
            return fid, b[p + w:p + w + 14]


def main():
    path, meta = sys.argv[1], sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    b = open(path, 'rb').read()
    d = json.load(io.open(meta, encoding='utf-8'))
    fl = d['data']['featlist']
    print('файл %s (%d б), эталон: %d фич' % (path, len(b), len(fl)))
    ok = miss = 0
    for f in fl[:limit]:
        r = find_feat(b, f['name'])
        if r is None:
            print('  %-22s id=%-6d %-20s НЕ НАЙДЕНА'
                  % (f['name'][:22], f['feat_id'], f['type'][:20]))
            miss += 1
            continue
        fid, tail = r
        mark = 'OK' if fid == f['feat_id'] else 'ID!=%d' % f['feat_id']
        if fid == f['feat_id']:
            ok += 1
        print('  %-22s id=%-6d %-20s %-8s хвост: %s'
              % (f['name'][:22], fid, f['type'][:20], mark,
                 ' '.join('%02X' % c for c in tail)))
    print('\nсовпало ID: %d, не найдено: %d' % (ok, miss))


if __name__ == '__main__':
    main()