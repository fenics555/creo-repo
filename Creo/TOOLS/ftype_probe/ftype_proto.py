"""FEATTYPE НАЙДЕН: имя прототипа фичи — это её тип (04.10.2026).

В записи фичи лежит:
    E2 <имя>\0  F7 4D F6 00 <ПРОТОТИП>\0  00  E2 "id <N>\0"

Примеры прототипов и их соответствие эталону CREOSON:
    dtmplane     -> ОПОРНАЯ ПЛОСКОСТЬ
    protextrude  -> ВЫСТУП / ВЫТЯГИВАНИЕ
    cutextrude   -> ВЫРЕЗ
    dtmsktcurve  -> эскиз на базовой плоскости
    project16    -> проекция / сечение

Запуск: python ftype_proto.py <файл> [<etalon.json>]
"""
import sys, io, re
from collections import Counter

PROTO_KEY = b'\xf7\x4d\xf6\x00'
ID_RE = re.compile(rb'id (\d+)')


def read_cstr(b, k):
    st = k
    while k < len(b) and b[k] != 0:
        k += 1
    return b[st:k], k


def extract(b):
    """Все (прототип, id, имя_фичи) — по структуре F7 4D F6 00 <прото>."""
    out = []
    s = 0
    while True:
        i = b.find(PROTO_KEY, s)
        if i < 0:
            break
        s = i + 1
        proto, after = read_cstr(b, i + len(PROTO_KEY))
        try:
            pname = proto.decode('utf-8')
        except UnicodeDecodeError:
            pname = proto.decode('latin-1')
        # сразу после NUL идёт "id NNNN" (иногда через 00 E2)
        win = b[after:after + 60]
        m = ID_RE.search(win)
        fid = int(m.group(1)) if m else None
        # имя фичи — перед прототипом: "E2 <имя>\0"
        nm = None
        back = b[max(0, i - 60):i]
        for k in range(len(back) - 2, 0, -1):
            if back[k] == 0:
                raw = back[k + 1:]
                if 1 <= len(raw) <= 50:
                    try:
                        nm = raw.decode('utf-8')
                    except UnicodeDecodeError:
                        nm = raw.decode('latin-1')
                break
        out.append((pname, fid, nm))
    return out


def main():
    path = sys.argv[1]
    b = open(path, 'rb').read()
    rows = extract(b)
    print('файл: %s (%d б)' % (path, len(b)))
    print('записей с прототипом: %d' % len(rows))
    c = Counter(p for p, _, _ in rows)
    print('\nуникальных прототипов: %d' % len(c))
    for k, v in c.most_common():
        print('   %-26s %d' % (k, v))

    if len(sys.argv) > 2:
        fl = json.load(io.open(sys.argv[2], encoding='utf-8'))['data']['featlist']
        byid = dict((f['feat_id'], f) for f in fl)
        print('\n=== СВЕРКА С ЭТАЛОНОМ CREOSON ===')
        ok = bad = 0
        for pname, fid, nm in rows:
            if fid is None or fid not in byid:
                continue
            f = byid[fid]
            flag = ''
            mark = nm or '?'
            print('  %-14s id=%-6d прототип=%-16s эталон_тип=%s'
                  % (mark[:14], fid, pname, f['type']))
            ok += 1
        print('\nсопоставлено по id: %d' % ok)


if __name__ == '__main__':
    import json
    main()