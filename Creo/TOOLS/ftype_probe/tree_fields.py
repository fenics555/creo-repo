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

print('\n=== MdlStatus: имена фич + ближайший id ===')
b = sect('MdlStatus')
RU = ('[А-ЯЁ][А-ЯЁа-яё ]{2,26}\\s?\\d*').encode('utf-8')
TYP = (rb'(featssrf|cutextrude|featround|protrevolve|feathole|'
        rb'featsketch|group)')
hits = list(re.finditer(rb'\x00(' + RU + rb')\x00[\s\S]{0,80}?' + TYP + rb'\x00', b))
print('найдено пар имя+тип: %d' % len(hits))
for m in hits[:12]:
    nm = m.group(1).decode('utf-8', 'replace').strip()
    tail = b[m.end():m.end() + 40]
    print('   %-26s [%s]' % (nm, m.group(2).decode()))
    print('      после типа: %s' % tail.hex(' '))

print('\n=== ЗАПИСИ ФИЧ: e3 c0 <id> ... f6 c0 <prev> <ИМЯ> 00 c0 <id> 00 <тип> ===')
b = sect('MdlStatus')
REC = re.compile(
    rb'\xe3\xc0(..)'                      # начало записи + id записи
    rb'(..)'                              # код типа записи (2 байта)
    rb'(?:\xf6(.{0,4}?))?'                # возможная ссылка (f6 + что-то)
    rb'\xc0(..)'                          # id ФИЧИ — стоит непосредственно перед именем
    rb'([\w\xd0-\xd1][\w\xd0-\xd1 ]{1,30}?)\x00'
    rb'\xc0(..)\x00'                      # id (повтор)
    rb'(\w+)\x00',
    re.S)
recs = []
for m in REC.finditer(b):
    fid = (m.group(4)[0] << 8) | m.group(4)[1]
    dup = (m.group(6)[0] << 8) | m.group(6)[1]
    ref = m.group(3)
    prev = None
    if ref and ref[:1] == b'\xc0' and len(ref) >= 3:
        prev = (ref[1] << 8) | ref[2]
    try:
        nm = m.group(5).decode('utf-8')
    except Exception:
        nm = m.group(5).decode('latin-1')
    recs.append((fid, prev, nm.strip(), m.group(7).decode(), dup))
print('записей: %d' % len(recs))
print('id совпадает с дублем: %d из %d'
      % (sum(1 for r in recs if r[0] == r[4]), len(recs)))

print('\n--- ПЕРВЫЕ 18 ---')
for fid, prev, nm, tp, dup in recs[:18]:
    print('   fid=%-6d prev=%-6s %-24s [%s]  dup=%d' % (fid, prev, nm, tp, dup))

kids = {}
for fid, prev, nm, tp, _ in recs:
    kids.setdefault(prev, []).append((fid, nm, tp))
br = [(p, v) for p, v in kids.items() if p is not None and len(v) > 1]
print('\nузлов с >1 ребёнком: %d' % len(br))
for p, v in br[:5]:
    print('   prev=%-6s -> %s' % (p, [x[1] for x in v][:8]))