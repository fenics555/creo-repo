"""ПАКЕТНЫЙ ЭТАЛОН: сопоставление feat_id(CREOSON) с записями в файле.

ДОКАЗАНО (04.10.2026, ручной разбор байтов): в файле лежит САМ feat_id,
записанный varint'ом, где старший бит первого байта = флаг «2 байта».
    id < 128  -> 1 байт: [id]
    иначе    -> 2 байта: [ (id>>8)|0x80 , id&0xFF ]
Смещения НЕТ. Прежняя гипотеза «+0x8001» ОПРОВЕРГНУТА — совпадала по шуму.

Запуск: python etalonbatch.py [папка] [N]
"""
import json, sys, io, os, random, re, urllib.request

URL = 'http://127.0.0.1:8080/creoson'


def enc_varint(i):
    """Кодек файла: <128 -> 1 байт, иначе 2 байта со старшим битом-флагом."""
    if i < 128:
        return bytes([i & 0xFF])
    return bytes([((i >> 8) & 0x7F) | 0x80, i & 0xFF])

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request(URL, data=json.dumps(body).encode('utf-8'),
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {'status': {'error': True, 'message': str(e)}, 'data': None}

def find_in_file(path, name, fid):
    """Ищем ID ТОЛЬКО рядом с именем фичи, а не где попало по файлу.

    Шаблон записи: <имя>\\0 01 00 [18 E5] <varint feat_id>
    (префикс 18 E5 опционален — в некоторых моделях его нет).
    """
    data = open(path, 'rb').read()
    nb = name.encode('utf-8')
    hits_name = [m.start() for m in re.finditer(re.escape(nb), data)]
    want = enc_varint(fid)
    # ID может идти сразу после "00 01 00" либо через префикс "18 E5" (din933)
    hit_id = []
    for p in hits_name:
        base = p + len(nb) + 3
        for skip in (0, 2):
            if data[base + skip:base + skip + len(want)] == want:
                hit_id.append(p); break
    return hits_name, hit_id, fid

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    c = call('connection', 'connect')
    sid = c.get('sessionId')
    if not sid:
        print('CREOSON недоступен'); return
    out = io.open('etalonbatch_out.txt', 'w', encoding='utf-8')
    out.write('ПАКЕТНЫЙ ЭТАЛОН CREOSON · ID в файле = feat_id БЕЗ СМЕЩЕНИЯ (varint)\n\n')

    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            if f.lower().endswith('.prt.1'):
                files.append(os.path.join(root, f))
        if len(files) > 20000:
            break
    random.seed(5)
    random.shuffle(files)
    used = 0
    tot_f = hit_f = 0
    for fp in files:
        if used >= N:
            break
        p = fp[:-2]          # «.prt.1» → «.prt» (срезаем «.1», а не только цифру)
        # свежая сессия на КАЖДЫЙ файл (иначе список пустеет)
        c2 = call('connection', 'connect')
        sid = c2.get('sessionId')
        if not sid:
            continue
        r = call('file', 'open', sid, {'file': p})
        if r.get('status', {}).get('error'):
            out.write('   [не открылся] %s\n' % os.path.basename(p))
            continue
        fr = call('feature', 'list', sid, {'file': p})
        fl = (fr.get('data') or {}).get('featlist')
        if not fl:
            out.write('   [пустой featlist] %s\n' % os.path.basename(p))
            continue
        used += 1
        out.write('=== %s — фич: %d ===\n' % (os.path.basename(fp), len(fl)))
        for ft in fl[:12]:
            nm = ft.get('name', '')
            fid = ft.get('feat_id')
            ty = ft.get('type', '')
            if fid is None:
                out.write('   %-14s тип=%-22s feat_id=?\n' % (nm[:14], ty[:22]))
                continue
            try:
                hn, hi, fidx = find_in_file(fp, nm, fid)
            except Exception as e:
                out.write('   %-14s ошибка %s\n' % (nm[:14], e)); continue
            tot_f += 1
            ok = bool(hi)
            if ok:
                hit_f += 1
            out.write('   %-14s тип=%-22s id=%-6s файл_id=0x%04X  имя:%d ID:%d %s\n'
                      % (nm[:14], ty[:22], fid, fidx, len(hn), len(hi),
                         '✅' if ok else '—'))
        out.write('\n')
    out.write('ИТОГО: фич %d, feat_id найден рядом с именем у %d\n' % (tot_f, hit_f))
    out.close()
    print('etalonbatch_out.txt files=%d feats=%d hit=%d' % (used, tot_f, hit_f))

if __name__ == '__main__':
    main()