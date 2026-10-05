"""Поиск полей иерархии фич (feat_id / prev_feat_id) в секциях Creo.

Цель — заменить эвристику «последняя открытая группа» на реальные связи.
"""
import re, sys, struct, collections

P = sys.argv[1] if len(sys.argv) > 1 else \
    r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
raw = open(P, 'rb').read()

i = raw.find(b'#UGC_TOC')
j = raw.find(b'\n', i) + 1
end = raw.find(b'NEXT_TOC_ENTRY', j)
toc = {}
blob = raw[j:end if end > 0 else j + 12000]
for mm in re.finditer(
        rb'^([A-Za-z_][A-Za-z0-9_]*)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+'
        rb'([0-9a-f]+)\s+[0-9a-f]+\s+[0-9a-zA-Z_]+\s+(-?[0-9a-f]+)', blob, re.M):
    toc[mm.group(1).decode()] = (int(mm.group(2), 16), int(mm.group(3), 16))
for mm in re.finditer(rb'ND:0:([A-Za-z0-9_]+):\d+\s+([0-9a-f]+)\s+([0-9a-f]+)', blob):
    toc.setdefault(mm.group(1).decode(),
                   (int(mm.group(2), 16), int(mm.group(3), 16)))


def sect(n):
    if n not in toc:
        return b''
    o, l = toc[n]
    return raw[o:o + l]


print('=== поля, похожие на иерархию ===')
for name in ('FeatDefs', 'AllFeatur', 'MdlStatus', 'FeatOrder', 'FeatInfo'):
    b = sect(name)
    if not b:
        print('\n%s — секции нет' % name)
        continue
    hits = collections.Counter(m.group(0) for m in re.finditer(rb'[a-z_]{3,24}', b))
    want = [(k.decode('latin-1'), v) for k, v in hits.items()
            if any(w in k for w in (b'_id', b'prev', b'parent', b'feat', b'ref'))]
    print('\n%s (%d байт) — релевантных полей %d:' % (name, len(b), len(want)))
    for k, v in sorted(want, key=lambda x: -x[1])[:16]:
        print('   %-26s %d' % (k, v))

print('\n=== где вообще встречаются " id <N>" ===')
cnt = collections.Counter()
for m in re.finditer(rb'([A-Za-z_][A-Za-z0-9_ ]{2,30}) id (\d+)', raw):
    cnt[m.group(1).decode('latin-1')] += 1
print('уникальных подписей: %d, всего: %d' % (len(cnt), sum(cnt.values())))
for k, v in cnt.most_common(15):
    print('   %-30s %d' % (k, v))

print('\n=== sort_feat_ids: сырые байты ===')
b = sect('MdlStatus')
for m in list(re.finditer(rb'sort_feat_ids\x00', b))[:6]:
    w = b[m.end():m.end() + 46]
    print('\n@%-6d %s' % (m.start(), w.hex(' ')))
    print('        %r' % w)