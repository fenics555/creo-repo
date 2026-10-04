import urllib.request, json, os, random, sys, collections
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
import creo_json as cj

def call(cmd, fn, sid=None, data=None):
    body = {'command': cmd, 'function': fn}
    if sid is not None:
        body['sessionId'] = sid
    body['data'] = data or {}
    req = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(req, timeout=180).read().decode('utf-8'))

def is_noise(nm):
    """Однобуквенные и двухбуквенные имена — шум схемы, не фичи."""
    return len(nm) <= 2

dirs = [l.strip().strip('"') for l in
        open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
        if l.strip()]
cands = []
for dd in dirs:
    try:
        for f in os.listdir(dd):
            if f.lower().endswith('.prt.1'):
                cands.append(os.path.join(dd, f[:-2]))
    except Exception:
        pass
random.seed(11); random.shuffle(cands)
print('кандидатов .prt: %d' % len(cands))

TOT_OK = TOT_WRONG = TOT_MISS = 0
MODELS = 0
raw_all = filt_all = 0
bad = []

for f in cands[:40]:
    try:
        sid = call('connection', 'connect')['sessionId']
        if call('file', 'open', sid, {'file': f})['status']['error']:
            continue
        fl = call('feature', 'list', sid, {'file': f}).get('data', {}) \
              .get('featlist') or []
        if not fl:
            continue
        MODELS += 1
        d = open(f + '.1', 'rb').read()
        got = cj.read_features(d)
        raw_all += len(got)
        clean = [x for x in got if not is_noise(x[1])]
        filt_all += len(clean)
        byid = {}
        for fid, nm, forma in clean:
            byid.setdefault(fid, []).append(nm)
        ok = wr = ms = 0
        for x in fl:
            fid = x['feat_id']
            if fid not in byid:
                ms += 1
            elif x['name'] in byid[fid]:
                ok += 1
            else:
                wr += 1
        TOT_OK += ok; TOT_WRONG += wr; TOT_MISS += ms
        prec = ok / float(ok + wr) if (ok + wr) else 0
        print('%-30s этал=%-4d чист=%-4d точн=%-4d шум=%d  %.1f%%'
              % (os.path.basename(f)[:30], len(fl), len(clean), ok,
                 len(got) - len(clean), prec * 100))
        if wr or ms:
            bad.append((os.path.basename(f), wr, ms))
    except Exception as e:
        pass

print()
print('=' * 60)
print('МОДЕЛЕЙ ОБРАБОТАНО: %d' % MODELS)
print('СЫРОЙ ПАРСЕР:  %d записей' % raw_all)
print('ПОСЛЕ ФИЛЬТРА: %d записей' % filt_all)
print('ОТСЕЯНО ШУМА:  %d (%.0f%%)' % (raw_all - filt_all,
      (raw_all - filt_all) * 100.0 / raw_all if raw_all else 0))
print()
print('ТОЧНОСТЬ: верно=%d  неверно=%d  не найдено=%d' % (TOT_OK, TOT_WRONG, TOT_MISS))
if TOT_OK + TOT_WRONG:
    print('PRECISION = %.2f%%' % (TOT_OK * 100.0 / (TOT_OK + TOT_WRONG)))
if TOT_OK + TOT_MISS:
    print('RECALL    = %.2f%%' % (TOT_OK * 100.0 / (TOT_OK + TOT_MISS)))
print()
print('модели с расхождениями: %d' % len(bad))
for b in bad[:6]:
    print('   %s  неверно=%d не найдено=%d' % b)