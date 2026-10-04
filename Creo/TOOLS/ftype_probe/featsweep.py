import os, re, random, collections

def dec_varint(b, i):
    b0 = b[i]
    if b0 & 0xC0 == 0x00:
        return b0, i + 1
    if b0 & 0xC0 == 0x80:
        return ((b0 & 0x7F) << 8) | b[i+1], i + 2
    return ((b0 & 0x3F) << 16) | (b[i+1] << 8) | b[i+2], i + 3

def read_feats(d):
    feats = {}
    for m in re.finditer(rb'([A-Za-z_][A-Za-z0-9_\.]{2,40})\x00', d):
        nm = m.group(1).decode('latin-1')
        if not re.match(r'^(DTM|DAT|PRT_|RIGHT|TOP|FRONT|LEFT|BACK|BOTTOM|'
                        r'LOCAL_GROUP|CO|EXT|SURF)', nm):
            continue
        i = m.end()
        if d[i:i+2] != b'\x01\x00':
            continue
        j = i + 2
        if d[j:j+2] == b'\x18\xe5':
            j += 2
        try:
            val, nxt = dec_varint(d, j)
        except Exception:
            continue
        feats.setdefault(nm, val)
    return feats

dirs = [l.strip().strip('"') for l in
        open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
        if l.strip()]
cands = []
for dd in dirs:
    try:
        for f in os.listdir(dd):
            if f.lower().endswith('.prt.1'):
                p = os.path.join(dd, f)
                cands.append((os.path.getsize(p), p))
    except Exception:
        pass
random.seed(5)
random.shuffle(cands)

# разбивка по размеру: маленькие / средние / большие
buckets = {'<500KB': [], '500KB-2MB': [], '>2MB': []}
for sz, p in cands:
    if sz < 500 * 1024:
        buckets['<500KB'].append(p)
    elif sz < 2 * 1024 * 1024:
        buckets['500KB-2MB'].append(p)
    else:
        buckets['>2MB'].append(p)

print('ВСЕГО .prt.1 в search.pro: %d' % len(cands))
for k in ('<500KB', '500KB-2MB', '>2MB'):
    print('   %-12s %d' % (k, len(buckets[k])))
print()

GRAND = 0
for name in ('<500KB', '500KB-2MB', '>2MB'):
    lst = buckets[name][:8]
    print('=' * 62)
    print('КОРИЗОР %s — проверяем %d моделей' % (name, len(lst)))
    tot_feats = 0
    tot_sz = 0
    ok_models = 0
    for p in lst:
        try:
            d = open(p, 'rb').read()
            f = read_feats(d)
            sz = len(d) / 1048576.0
            if not f:
                print('   %-34s %6.1f MB  ФИЧ НЕТ (0)' % (os.path.basename(p)[:34], sz))
                continue
            tot_feats += len(f)
            tot_sz += sz
            ok_models += 1
            ks = list(f.items())[:5]
            print('   %-34s %6.1f MB  ФИЧ=%-4d  %s'
                  % (os.path.basename(p)[:34], sz, len(f),
                     ', '.join('%s=%d' % (a[:12], b) for a, b in ks)))
        except Exception as e:
            print('   %-34s ОШИБКА %s' % (os.path.basename(p)[:34], e))
    print('   ИТОГО: моделей с фичами %d/%d, фич суммарно %d'
          % (ok_models, len(lst), tot_feats))
    GRAND += tot_feats
    print()

print('=' * 62)
print('ВСЕГО ПРОЧИТАНО ФИЧ ПО ВСЕМ КОРИЗОРАМ: %d' % GRAND)