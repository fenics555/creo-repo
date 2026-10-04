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
    return tree, nodes, links, toc


def _walk(n, links):
    for c in n['children']:
        for lbl, num in links:
            if lbl == c['name']:
                c['links'].append({'rel': lbl, 'id': num})
        _walk(c, links)


if __name__ == '__main__':
    import json
    P = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
    tree, nodes, links, toc = build_tree(P)
    print('секций: %d' % len(toc))
    print('узлов (имя+тип): %d' % len(nodes))
    print('связей "<ТИП> id N": %d' % len(links))
    print('корневых узлов: %d' % len(tree))
    print()

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