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
o, l = toc['FeatDefs']
fd = raw[o:o + l]

print('FeatDefs: %d байт' % len(fd))

# 1) есть ли тут кириллические имена фич
RU = ('[А-ЯЁ][А-ЯЁа-яё ]{2,26}\\s?\\d*').encode('utf-8')
print('кириллических имён: %d' % len(re.findall(rb'\x00(' + RU + rb')\x00', fd)))
for m in list(re.finditer(rb'\x00(' + RU + rb')\x00', fd))[:6]:
    print('   %s' % m.group(1).decode('utf-8', 'replace').strip())

# 2) структура записи: что стоит РЯДОМ с каждым именем
print('\n=== контекст после кириллического имени ===')
for m in list(re.finditer(rb'\x00(' + RU + rb')\x00', fd))[:5]:
    s = m.end()
    print('   %-22s %s' % (m.group(1).decode('utf-8', 'replace').strip()[:20],
                          fd[s:s + 26].hex(' ')))

# 3) ищем указатель на родителя: 2 байта id, встречающиеся >1 раза как значение
print('\n=== частые 2-байтовые значения после c0 ===')
cnt = collections.Counter()
for m in re.finditer(rb'\xc0(..)', fd):
    cnt[(m.group(1)[0] << 8) | m.group(1)[1]] += 1
print('уникальных значений: %d' % len(cnt))
print('топ-15 по частоте (кандидаты на «владельца группы»):')
for v, c in cnt.most_common(15):
    print('   id=%-6d встречается %d раз' % (v, c))

# 4) проверка: встречается ли каждый feat_id из MdlStatus в FeatRefs
print('\n=== feat_id из MdlStatus в FeatDefs ===')
mo, ml = toc['MdlStatus']
ms = raw[mo:mo + ml]
import sys as _s
_s.path.insert(0, '.')
from creo_tree_builder import build_tree
t, n, lk, tc, oi, feats = build_tree(P)
fids = set(f['feat_id'] for f in feats)
found = sum(1 for f in fids if fd.count(f.to_bytes(2, 'big')))
print('feat_id из MdlStatus (%d), найдено в FeatDefs как 2 байта: %d'
      % (len(fids), found))

# --- ГЛАВНОЕ: как feat_id из MdlStatus соотносится с FeatDefs ---
print('=== ПОИСК СВЯЗИ MdlStatus <-> FeatDefs ===')
by_id = {f['feat_id']: f for f in feats}

# как реально выглядит feat_id внутри FeatDefs? ищем один известный
sample = sorted(by_id)[0]
needle = sample.to_bytes(2, 'big')
print('пример feat_id=%d, байты %s' % (sample, needle.hex(' ')))
for m in list(re.finditer(re.escape(needle), fd))[:4]:
    s = max(0, m.start() - 14)
    print('   @%-8d %s' % (m.start(), fd[s:m.start() + 16].hex(' ')))
    print('              %r' % fd[s:m.start() + 16])

# ищем id СРАЗУ ПОСЛЕ кириллического/латинского имени фичи
print('\n=== id сразу после известных имён ===')
names = [f['name'] for f in feats[:40] if f['name']]
print('проверяю %d имён' % len(names))
pat = re.compile(rb'\x00(' + ('|'.join(re.escape(n.encode('utf-8'))
                                        for n in names)) + rb')\x00(.{0,6})', re.S)
found = 0
for m in list(pat.finditer(fd))[:8]:
    tail = m.group(2)
    print('   %-22s после: %s' % (m.group(1).decode('utf-8'), tail.hex(' ')))
    found += 1
print('совпадений: %d' % found)

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

print('\n=== pat_group_header_id / is_header / флаг записи ===')
print('pat_group_header_id: %d вхождений' % len(re.findall(rb'pat_group_header_id', st)))
for m in re.finditer(rb'pat_group_header_id\x00', st):
    w = st[m.end():m.end() + 24]
    print('   @%-6d %s  %r' % (m.start(), w.hex(' '), w[:20]))

print('\nis_header: %d вхождений' % len(re.findall(rb'is_header', st)))
for m in re.finditer(rb'is_header\x00', st):
    w = st[m.end():m.end() + 10]
    print('   @%-6d %s  %r' % (m.start(), w.hex(' '), w[:8]))

print('\nфлаги в записях (байт между c0<C> и типом):')
fc = collections.Counter()
for m in REC.finditer(st):
    fc[(m.group(6)[0], m.group(7).decode())] += 1
for (f, t), n in sorted(fc.items()):
    print('   0x%02X  %-12s %d' % (f, t, n))

print('\n=== ГРУППЫ: записи с типом group ===')
groups = [r for r in recs if r['type'] == 'group']
print('всего записей group: %d' % len(groups))
for r in groups[:12]:
    print('   A=%-6d B=%-6d C=%-6d %s' % (r['A'], r['B'], r['C'], r['name']))

print('\n=== ФЛАГ 0x01 = ЗАГОЛОВОК ГРУППЫ -> ДЕРЕВО ===')
by_a = {r['A']: r for r in recs}
gid = [(u16(m.group(1)), m.group(6)[0]) for m in REC.finditer(st)]
owner, cur = {}, None
for aid, fl in gid:
    if fl == 0x01:
        cur = aid
    elif cur is not None:
        owner[aid] = cur
nleaf = sum(1 for _, f in gid if f == 0x00)
print('заголовков(0x01): %d   листьев(0x00): %d   с хозяином: %d'
      % (len(groups), nleaf, len(owner)))

gc = collections.defaultdict(list)
for aid, o in owner.items():
    gc[o].append(aid)

print('\n--- содержимое первых 10 групп ---')
for g in groups[:10]:
    ch = [by_a[c]['name'][:20] for c in gc.get(g['A'], [])[:7]]
    print('   %-20s (%2d) %s' % (g['name'][:20], len(gc.get(g['A'], [])),
                                 ch if ch else '-- ПУСТО'))

empt = [g for g in groups if not gc.get(g['A'])]
multi = [(g['name'], len(gc[g['A']])) for g in groups if len(gc.get(g['A'], [])) > 3]
print('\nпустых групп: %d из %d' % (len(empt), len(groups)))
print('групп с >3 детейми: %d' % len(multi))
for n, c in multi[:6]:
    print('   %-22s %d детей' % (n, c))

# вложенность: группа внутри группы
nest = [(g['name'], by_a[owner[g['A']]]['name'])
        for g in groups if g['A'] in owner]
print('\nгрупп, вложенных в другую группу: %d' % len(nest))
for c, p in nest[:5]:
    print('   %-20s внутри %s' % (c, p))
