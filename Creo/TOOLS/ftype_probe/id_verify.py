"""ЧЕСТНАЯ ПРОВЕРКА отображения feat_id(CREOSON) -> байты в .prt файле.

Не ищет ID где попало по файлу (это даёт ложные ✅).
Для каждой фичи: находит все вхождения ИМЕНИ в файле и печатает байты
вокруг них, чтобы увидеть, какое 2-байтовое число стоит рядом с именем.

Запуск: python id_verify.py [папка] [N_файлов]
"""
import json, sys, os, re, urllib.request, io

URL = 'http://127.0.0.1:8080/creoson'
CTX = 60  # байт контекста вокруг имени


def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request(URL, data=json.dumps(body).encode('utf-8'),
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        return {'status': {'error': True, 'message': str(e)}, 'data': None}


def collect(base, nfiles):
    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            if f.lower().endswith('.prt.1'):
                files.append(os.path.join(root, f))
        if len(files) > 5000:
            break
    files.sort()
    step = max(1, len(files) // max(1, nfiles))
    return files[::step][:nfiles]


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'D:\AI\PROBA'
    nfiles = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    out = io.open('id_verify_out.txt', 'w', encoding='utf-8')
    todo = collect(base, nfiles)

    total_feat = 0
    name_found = 0
    for v1 in todo:
        p = v1[:-2]  # срезаем '.1'
        sid = (call('connection', 'connect') or {}).get('sessionId')
        if not sid:
            out.write('[нет сессии] %s\n' % os.path.basename(p)); continue
        if (call('file', 'open', sid, {'file': p}) or {}).get('status', {}).get('error'):
            out.write('[не открылся] %s\n' % os.path.basename(p)); continue
        fr = call('feature', 'list', sid, {'file': p})
        fl = (fr.get('data') or {}).get('featlist') or []
        if not fl:
            out.write('[пусто] %s\n' % os.path.basename(p)); continue
        data = open(v1, 'rb').read()
        out.write('\n===== %s  фич=%d  размер=%d =====\n'
                  % (os.path.basename(v1), len(fl), len(data)))
        for ft in fl[:25]:
            nm = ft.get('name', '')
            fid = ft.get('feat_id')
            ty = ft.get('type', '')
            total_feat += 1
            if not nm:
                continue
            nb = nm.encode('utf-8', 'ignore')
            pos = [m.start() for m in re.finditer(re.escape(nb), data)]
            if not pos:
                out.write('%-16s id=%-6s тип=%-24s ИМЯ НЕ НАЙДЕНО\n' % (nm[:16], fid, ty[:24]))
                continue
            name_found += 1
            out.write('%-16s id=%-6s тип=%-24s вхождений=%d\n' % (nm[:16], fid, ty[:24], len(pos)))
            for q in pos[:3]:
                lo = max(0, q - CTX); hi = min(len(data), q + len(nb) + 16)
                win = data[lo:hi]
                hexs = ' '.join('%02X' % b for b in win)
                mark = ' ' * (q - lo + CTX) + '^'
                out.write('   %s\n   %s\n' % (hexs, mark))
        # слишком длинный лог — режем после 400 строк на файл
    out.write('\nИТОГО фич=%d, имя найдено у %d\n' % (total_feat, name_found))
    out.close()
    print('id_verify_out.txt feats=%d namefound=%d' % (total_feat, name_found))


if __name__ == '__main__':
    main()