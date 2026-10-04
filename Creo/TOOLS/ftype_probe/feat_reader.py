"""ЧИТАТЕЛЬ ДЕРЕВА ФИЧ — разбор записи, не поиск подстрок.

Схема подтверждена чтением файла как текста (строки 47710-47752 файла
137_011_0041.prt.1):
    typed_data(MTTyped_CreateData) / created_features
    feat_id / ft_type / comp_type / prev_feat_id / feat_name / icon_name
    в данных:  <ИМЯ> <ТИП>   парами, напр. DTM2 dtmplane, ВЫТЯГИВАНИЕ 2 cutextrude
"""
import re

TYPES = ('group', 'dtmplane', 'csys', 'cutextrude', 'featround',
         'protrevolve', 'feathole', 'featsketch', 'featpattern', 'protrusion')

# пара: <имя> <тип>, где имя — слово либо кириллица
PAIR = re.compile(
    r'([A-Za-zА-Яа-яЁё_][A-Za-z0-9А-Яа-яЁё_\- .]{1,40}?)\s+'
    r'(' + '|'.join(TYPES) + r')\b')


def read_feature_tree(path):
    raw = open(path, 'rb').read()
    # latin-1: 1 байт = 1 символ, позиции совпадают с байтовыми
    txt = raw.decode('latin-1')

    pairs = []
    for m in PAIR.finditer(txt):
        name = m.group(1).strip(' ,;')
        typ = m.group(2)
        if not name:
            continue
        pairs.append((name, typ, m.start()))

    # вложенность: операция принадлежит последней открытой группе.
    # Имена групп идут подряд, операции — после них.
    tree = []
    cur = None
    for name, typ, pos in pairs:
        node = {'name': name, 'type': typ, 'children': []}
        if typ == 'group':
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
    return tree, pairs, len(raw)


def walk(tree, depth=0):
    out = []
    for n in tree:
        out.append('%s%s  [%s]%s'
                   % ('  ' * depth, n['name'][:36], n['type'],
                      '  -> %d' % len(n['children']) if n['children'] else ''))
        out.extend(walk(n['children'], depth + 1))
    return out


if __name__ == '__main__':
    import sys
    P = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
    tree, pairs, size = read_feature_tree(P)
    print('ФАЙЛ: %s (%d байт)' % (P.split('\\')[-1], size))
    print('НАЙДЕНО ПАР имя+тип: %d' % len(pairs))
    print('УЗЛОВ В ДЕРЕВЕ: %d' % len(tree))
    print()
    for line in walk(tree)[:70]:
        print('   ' + line)
    print()
    print('--- уникальные типы в файле ---')
    seen = {}
    for nm, t, p in pairs:
        seen.setdefault(t, []).append(nm[:22])
    for t in sorted(seen):
        print('   %-14s %4d шт  %s' % (t, len(seen[t]),
                                       ', '.join(seen[t][:3])))