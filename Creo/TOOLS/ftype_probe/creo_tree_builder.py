"""ВЕКТОР 1: сборщик иерархического графа дерева фич.

Данные — секция MdlStatus (дерево и типы) + секция AllFeatur (данные фич).
Связи в файле записаны строками:  "<ТИП> id <N>"
"""
import re


def build_tree(path):
    raw = open(path, 'rb').read()
    i = raw.find(b'#UGC_TOC')
    j = raw.find(b'\n', i) + 1
    end = raw.find(b'NEXT_TOC_ENTRY', j)
    toc = {}
    for mm in re.finditer(
            rb'^([A-Za-z_][A-Za-z0-9_]*)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+'
            rb'([0-9a-f]+)\s+[0-9a-f]+\s+[0-9a-zA-Z_]+\s+(-?[0-9a-f]+)',
            raw[j:end if end > 0 else j + 12000], re.M):
        toc[mm.group(1).decode()] = (int(mm.group(2), 16), int(mm.group(3), 16))
    for mm in re.finditer(rb'ND:0:([A-Za-z0-9_]+):\d+\s+([0-9a-f]+)\s+([0-9a-f]+)',
                         raw[j:end if end > 0 else j + 12000]):
        toc.setdefault(mm.group(1).decode(),
                       (int(mm.group(2), 16), int(mm.group(3), 16)))

    def sect(n):
        if n not in toc:
            return b''
        o, l = toc[n]
        return raw[o:o + l]

    st = sect('MdlStatus')
    txt = st.decode('utf-8', 'replace')

    # 1) узлы: имя операции + её тип
    NODE = re.compile(
        r'((?:[А-ЯЁ][А-ЯЁа-яё ]{2,26}\s?\d*)|(?:LOCAL_GROUP[_\d]*)|'
        r'(?:ASM_[A-Z_]+)|(?:RIGHT|TOP|FRONT|BOTTOM|LEFT|BACK|'
        r'PRT_CSYS_DEF|WCS))'
        r'\x00[\s\S]{0,220}?\x00?'
        r'(group|dtmplane|csys|cutextrude|featround|protrevolve|'
        r'feathole|featsketch|featssrf)\x00')
    nodes = {}
    order = []
    for mm in NODE.finditer(txt):
        nm = mm.group(1).strip()
        tp = mm.group(2)
        if nm not in nodes:
            nodes[nm] = {'name': nm, 'type': tp, 'children': [], 'links': []}
            order.append(nm)

    # 2) связи: "ОПОРНАЯ ПЛОСКОСТЬ id 33943"
    LINK = re.compile(r'([А-ЯЁ][А-ЯЁа-яё ]{2,26}|LOCAL_GROUP[^\x00]{0,12}) id (\d+)')
    links = []
    for mm in LINK.finditer(txt):
        links.append((mm.group(1).strip(), int(mm.group(2))))

    # 3) иерархия: операция попадает в последнюю открытую группу
    tree = []
    cur = None
    for nm in order:
        node = nodes[nm]
        if node['type'] == 'group':
            if cur is not None:
                cur['children'].append(node)
                cur = node
            else:
                tree.append(node)
                cur = node
        else:
            if cur is not None:
                cur['children'].append(node)
            else:
                tree.append(node)
    for n in tree:
        _walk(n, links)
    # 2a) РЕАЛЬНЫЕ ЗАПИСИ ФИЧ из MdlStatus — данные файла, не эвристика.
    #     Структура: e3 c0 <id> <код 2 байта> [f6 <ссылка>] c0 <id> <ИМЯ> 00 c0 <id> 00 <ТИП>
    stb = sect('MdlStatus')          # БАЙТЫ, не декодированная строка
    FEATREC = re.compile(
        rb'\xe3\xc0(..)(..)(?:\xf6)?\xc0(..)'
        rb'([\w\xd0-\xd1][\w\xd0-\xd1 ]{1,30}?)\x00'
        rb'\xc0(..)(.)(\w+)\x00',
        re.S)
    def u16(b):
        b = bytes(b)
        while len(b) < 2:
            b += b'\x00'
        return (b[0] << 8) | b[1]


# --- разбор записей ---
    # группы: 1=A(id записи) 2=код 3=B 4=имя 5=C 6=флаг 7=тип
    feats = []
    for m in FEATREC.finditer(stb):
        try:
            nm = m.group(4).decode('utf-8')
        except Exception:
            nm = m.group(4).decode('latin-1')
        feats.append({'feat_id': u16(m.group(1)),
                      'prev_in_seq': u16(m.group(3)),
                      'name': nm.strip(),
                      'group_key': u16(m.group(5)),
                      'flag': m.group(6)[0],
                      'type': m.group(7).decode(),
                      'id_confirmed': u16(m.group(1)) == u16(m.group(5)),
                      'prev_feat_id': None})

    # 2c) ГРУППИРОВКА ИЗ ФЛАГА 0x01 (заголовок группы). Это данные файла.
    #     Флаг стоит между c0 <C> и именем типа: 0x01 = group, 0x00 = лист.
    #     Лист принадлежит последнему встреченному заголовку по порядку в файле.
    seq = [(m.group(1), m.group(6)[0]) for m in FEATREC.finditer(stb)]
    owner, cur = {}, None
    for g in seq:
        aid = (g[0][0] << 8) | g[0][1]
        if g[1] == 0x01:
            cur = aid
        elif cur is not None:
            owner[aid] = cur
    for f in feats:
        f['group_id'] = owner.get(f['feat_id'])
        f['is_header'] = (f['type'] == 'group')

    # 2b) РЕАЛЬНЫЙ порядок дерева: sort_feat_ids = 'f8' <n> + n * '82' <id16>
    order_ids = []
    for sm in re.finditer(rb'sort_feat_ids\x00', stb):
        q = sm.end()
        p = q + 1                                  # пропускаем \xf8
        n = stb[p] if p < len(stb) else 0
        p += 1
        ids = []
        for _ in range(n):
            if p + 2 >= len(stb):
                break
            tag = stb[p]
            if tag == 0x82:                        # 1 байт значения
                ids.append(stb[p + 1])
                p += 2
            elif tag == 0xC0:                      # 2 байта значения
                ids.append((stb[p + 1] << 8) | stb[p + 2])
                p += 3
            else:
                break
        if len(ids) == n and n >= 3:
            order_ids = ids
    return tree, nodes, links, toc, order_ids, feats


def _walk(n, links):
    for c in n['children']:
        for lbl, num in links:
            if lbl == c['name']:
                c['links'].append({'rel': lbl, 'id': num})
        _walk(c, links)


if __name__ == '__main__':
    import json
    P = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
    tree, nodes, links, toc, order_ids, feats = build_tree(P)
    print('секций: %d' % len(toc))
    print('узлов (имя+тип, эвристика): %d' % len(nodes))
    print('ЗАПИСЕЙ ФИЧ ИЗ ФАЙЛА: %d' % len(feats))
    conf = sum(1 for f in feats if f['id_confirmed'])
    withprev = sum(1 for f in feats if f['prev_feat_id'])
    withgrp = sum(1 for f in feats if f.get('group_id'))
    heads = [f for f in feats if f['is_header']]
    print('   с подтверждённым id (== дубль): %d' % conf)
    print('   с prev_feat_id: %d  <- НЕ РАБОТАЕТ' % withprev)
    print('   с group_id (флаг 0x01): %d' % withgrp)
    print('   заголовков групп: %d, пустых: %d'
          % (len(heads),
             sum(1 for h in heads
                 if not any(f.get('group_id') == h['feat_id'] for f in feats))))
    print('связей "<ТИП> id N": %d' % len(links))
    print('ПОРЯДОК ИЗ sort_feat_ids: %s' % order_ids)
    print()
    print('=== ЗАПИСИ ФИЧ ИЗ ФАЙЛА (первые 20) ===')
    for f in feats[:20]:
        print('   id=%-6d prev=%-6s %-24s [%s]%s'
              % (f['feat_id'], f['prev_feat_id'], f['name'], f['type'],
                 '' if f['id_confirmed'] else '  (id не подтверждён)'))

    def show(ns, d=0, lim=[0]):
        for n in ns:
            if lim[0] >= 28:
                return
            lim[0] += 1
            ln = ('  ' + ' | '.join('%s=%s' % (x['rel'], x['id'])
                                   for x in n['links'][:2]))
            print('%s%s  [%s]%s' % ('    ' * d, n['name'][:34], n['type'],
                                     ' ' + ln if ln.strip() else ''))
            show(n['children'], d + 1, lim)
    print('=== ДЕРЕВО ===')
    show(tree)