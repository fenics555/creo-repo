"""Проверка: является ли `c0 <id>` перед именем PREV_FEAT_ID.

Структура записи (с байтов):
    e3 c0 <A:id записи> <код 2 байта> [f6] c0 <B> <ИМЯ> 00 c0 <C> <флаг> <ТИП> 00
Гипотеза: B = prev_feat_id (предок), C = что-то третье.
Признак подтверждения: по B строится корректное дерево — у каждого узла
ровно один предок, есть корни, нет циклов.
"""
import re, sys, collections

P = sys.argv[1] if len(sys.argv) > 1 else \
    r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
raw = open(P, 'rb').read()

i = raw.find(b'#UGC_TOC')
j = raw.find(b'\n', i) + 1
end = raw.find(b'NEXT_TOC_ENTRY', j)
blob = raw[j:end if end > 0 else j + 12000]
toc = {}
for mm in re.finditer(
        rb'^([A-Za-z_][A-Za-z0-9_]*)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+'
        rb'([0-9a-f]+)\s+[0-9a-f]+\s+[0-9a-zA-Z_]+\s+(-?[0-9a-f]+)', blob, re.M):
    toc[mm.group(1).decode()] = (int(mm.group(2), 16), int(mm.group(3), 16))
for mm in re.finditer(rb'ND:0:([A-Za-z0-9_]+):\d+\s+([0-9a-f]+)\s+([0-9a-f]+)', blob):
    toc.setdefault(mm.group(1).decode(),
                   (int(mm.group(2), 16), int(mm.group(3), 16)))

o, l = toc['MdlStatus']
st = raw[o:o + l]


def u16(b):
    return (b[0] << 8) | b[1]


# B = id сразу перед именем; C = id после имени
REC = re.compile(
    rb'\xe3\xc0(..)(..)(?:\xf6)?\xc0(..)'
    rb'([\w\xd0-\xd1][\w\xd0-\xd1 ]{1,30}?)\x00'
    rb'\xc0(..)(.)(\w+)\x00',
    re.S)

recs = []
for m in REC.finditer(st):
    try:
        nm = m.group(4).decode('utf-8')
    except Exception:
        nm = m.group(4).decode('latin-1')
    recs.append({
        'A': u16(m.group(1)), 'B': u16(m.group(3)),
        'C': u16(m.group(5)), 'flag': m.group(6)[0],
        'name': nm.strip(), 'type': m.group(7).decode(),
    })

print('записей: %d' % len(recs))

# --- проверка гипотезы B = предок ---
ids = {r['A'] for r in recs}
kids = collections.defaultdict(list)
for r in recs:
    kids[r['B']].append(r)

known_parent = [r for r in recs if r['B'] in ids]
roots = [r for r in recs if r['B'] not in ids]

print('\n--- Проверка B = prev_feat_id ---')
print('узлов, чей B найден среди A: %d из %d' % (len(known_parent), len(recs)))
print('корней (B не найден среди A): %d' % len(roots))
multi = [b for b, v in kids.items() if len(v) > 1]
print('предков с >1 ребёнком: %d' % len(multi))

# циклы
def depth(a, seen):
    if a in seen:
        return -1
    seen.add(a)
    nxt = next((r['B'] for r in recs if r['A'] == a), None)
    if nxt is None or nxt not in ids:
        return 0
    return 1 + depth(nxt, seen)


by_a = {r['A']: r for r in recs}
cyc = 0
maxd = 0
for r in recs:
    d = depth(r['A'], set())
    if d < 0:
        cyc += 1
    else:
        maxd = max(maxd, d)
print('узлов в цикле: %d   максимальная глубина: %d' % (cyc, maxd))

# --- для сравнения: C ---
kidsC = collections.defaultdict(list)
for r in recs:
    kidsC[r['C']].append(r)
rootsC = [r for r in recs if r['C'] not in ids]
multiC = [c for c, v in kidsC.items() if len(v) > 1]
print('\n--- Для сравнения C ---')
print('корней (C не найден среди A): %d' % len(rootsC))
print('C с >1 ребёнком: %d' % len(multiC))

print('\n--- диагностика: что на самом деле значит B ---')
# если B = предок, то у каждого B должен быть ребёнок. Проверим обратное:
without_kid = [b for b in {r['B'] for r in recs} if b not in kids or not kids[b]]
print('значений B без единого ребёнка: %d' % len(without_kid))

# Проверка «B = предыдущая запись в файле»: расстояние по позиции
pos = {}
for idx, m in enumerate(REC.finditer(st)):
    pos[idx] = m.start()
seq = []
for m in REC.finditer(st):
    seq.append(u16(m.group(1)))
idx_of = {v: k for k, v in enumerate(seq)}
adj = 0
tot = 0
for k, m in enumerate(REC.finditer(st)):
    b = u16(m.group(3))
    tot += 1
    if idx_of.get(b) == k - 1:
        adj += 1
print('B указывает на ПРЕДЫДУЩУЮ по порядку запись: %d из %d' % (adj, tot))

# Проверка «B — предок через иерархию»: строим и смотрим на глубины
print('\n--- цепочка B (как есть) ---')
cur = [r for r in recs if r['B'] not in {x['A'] for x in recs}][:3]
for r in cur:
    ch = r
    line = [r['name'][:18]]
    for _ in range(6):
        nxt = kids.get(ch['A'])
        if not nxt:
            break
        ch = nxt[0]
        line.append(ch['name'][:18])
    print('   %s' % ' -> '.join(line))

# --- Проверка C = РОДИТЕЛЬ ---
print('\n=== ПРОВЕРКА C = РОДИТЕЛЬ (кандидат на настоящее дерево) ===')
by_c = collections.defaultdict(list)
for r in recs:
    by_c[r['C']].append(r)
roots_c = [r for r in recs if r['C'] not in by_c]
multi_c = {c: v for c, v in by_c.items() if len(v) > 1}
print('C найден как родитель у %d из %d' % (len(recs) - len(roots_c), len(recs)))
print('корней: %d' % len(roots_c))
print('родителей с >1 ребёнком: %d' % len(multi_c))

c_parent = {r['A']: r['C'] for r in recs}
allA = set(c_parent)


def cdepth(a, seen):
    if a in seen:
        return -1
    seen.add(a)
    p = c_parent.get(a)
    if p is None or p not in allA:
        return 0
    return 1 + cdepth(p, seen)


cy = md = 0
for a in allA:
    d = cdepth(a, set())
    if d < 0:
        cy += 1
    else:
        md = max(md, d)
print('узлов в цикле: %d   максимальная глубина: %d' % (cy, md))

print('\n--- ДЕРЕВО ПО C (первые 32 строки) ---')
cnt = [0]


def show2(cid, d=0):
    for r in by_c.get(cid, []):
        if cnt[0] > 32:
            return
        cnt[0] += 1
        print('   %s%s [%s]' % ('  ' * d, r['name'][:30], r['type']))
        show2(r['A'], d + 1)


for r in roots_c[:2]:
    print(' КОРЕНЬ: %s [%s]' % (r['name'][:30], r['type']))
    show2(r['A'], 1)
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