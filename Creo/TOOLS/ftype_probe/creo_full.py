"""ПОЛНЫЙ ИЗВЛЕКАТЕЛЬ ФАЙЛОВ CREO — без Creo.

Читает оглавление #UGC_TOC, достаёт секции по адресам, разбирает записи.
Выход: JSON по каждой модели.
"""
import os, re, json, sys

TOCRE = re.compile(
    rb'^([A-Za-z_][A-Za-z0-9_]*)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)'
    rb'\s+[0-9a-f]+\s+[0-9a-zA-Z_]+\s+(-?[0-9a-f]+)\s+([0-9a-f]{4})\s+([0-9a-f]{4})',
    re.M)

TYPE_CODES = ('group', 'dtmplane', 'csys', 'cutextrude', 'featround',
              'protrevolve', 'feathole', 'featsketch', 'featssrf', 'featpattern')

FEATURE_NAMES = ('DTM', 'LOCAL_GROUP', 'ASM_', 'PRT_CSYS', 'RIGHT', 'TOP',
                 'FRONT', 'BOTTOM', 'LEFT', 'BACK', 'WCS', 'COORD_SYS')


def read_model(path):
    raw = open(path, 'rb').read()
    name = os.path.basename(path)
    out = {'file': name, 'size': len(raw)}

    # --- шапка ---
    head = raw[:400].decode('latin-1')
    m = re.search(r'#UGC:2\s+(\w+)', head)
    out['type'] = m.group(1) if m else '?'
    m = re.search(r'#-\s+CMNM\s+\w+(\S+)', head)
    out['model_name'] = m.group(1) if m else name
    m = re.search(r'#Creo\s+TM\s+([\d.]+)', head)
    out['creo_version'] = m.group(1) if m else '?'

    # --- оглавление ---
    i = raw.find(b'#UGC_TOC')
    j = raw.find(b'\n', i) + 1
    end = raw.find(b'NEXT_TOC_ENTRY', j)
    if end < 0:
        end = min(len(raw), j + 12000)
    toc = {}
    for mm in TOCRE.finditer(raw[j:end]):
        toc[mm.group(1).decode()] = (int(mm.group(2), 16), int(mm.group(3), 16))
    for mm in re.finditer(rb'ND:0:([A-Za-z0-9_]+):\d+\s+([0-9a-f]+)\s+([0-9a-f]+)', raw[j:end]):
        toc.setdefault(mm.group(1).decode(), (int(mm.group(2), 16), int(mm.group(3), 16)))
    out['sections'] = len(toc)

    def sect(nm):
        if nm not in toc:
            return b''
        o, l = toc[nm]
        return raw[o:o + l]

    # --- ДЕРЕВО И ТИПЫ: MdlStatus ---
    st = sect('MdlStatus').decode('utf-8', 'replace')
    types = {}
    for c in TYPE_CODES:
        n = st.count(c)
        if n:
            types[c] = n
    out['type_counts'] = types

    # операции: кириллическое имя + код типа
    ops = []
    for mm in re.finditer(r'([А-ЯЁ][А-ЯЁа-яё ]{2,26}\s?\d*)\x00[\s\S]{0,400}?'
                          r'\x00(featssrf|cutextrude|featround|protrevolve|'
                          r'feathole|featsketch)\x00', st):
        ops.append({'name': mm.group(1).strip(), 'type': mm.group(2)})
    seen = set()
    out['operations'] = [o for o in ops
                         if not (o['name'] in seen or seen.add(o['name']))]

    # поверхности: имя идёт в поле feat_name, тип в icon_name -> featssrf
    surf = []
    for mm in re.finditer(r'([A-Za-zА-Яа-я][\w А-Яа-я]{2,30}?)\x00[\s\S]{0,300}?'
                          r'featssrf\x00[\s\S]{0,20}?'
                          r'([\w ]+?) id (\d+)', st):
        nm = mm.group(1).strip()
        if nm in ('ADMIN', 'fpn', 'fch', 'fpr'):
            continue
        surf.append({'name': nm, 'kind': mm.group(2).strip(),
                     'id': int(mm.group(3))})
    out['surfaces'] = surf

    # --- ФИЧИ: имена ---
    names = []
    for nm in ('AllFeatur', 'MdlStatus'):
        t = sect(nm).decode('latin-1')
        for mm in re.finditer(r'\x00([A-Z][A-Za-z0-9_]{2,30})\x00', t):
            s = mm.group(1)
            if s.startswith(FEATURE_NAMES) and s not in names:
                names.append(s)
    out['features'] = names

    # --- BOM: MdlRefInfo ---
    refs = sect('MdlRefInfo').decode('latin-1')
    stem = name.split('.')[0].lower()
    comp = sorted(set(mm.group(1) for mm in
                      re.finditer(r'([A-Za-z0-9_\-]{2,40}\.(?:prt|PRT|asm|ASM))', refs)
                      if not mm.group(1).lower().startswith(stem)))
    # если в MdlRefInfo пусто — ищем прямые ссылки по всему файлу (без геометрии)
    if not comp:
        i = raw.find(b'#UGC_TOC')
        j = raw.find(b'\n', i) + 1
        scan = raw[j:]
        e = scan.find(b'SolidPrimdata')
        if e > 0:
            scan = scan[:e]
        comp = sorted(set(mm.group(1) for mm in
                          re.finditer(rb'([A-Za-z0-9_\-]{2,40}\.(?:prt|PRT|asm|ASM))', scan)
                          if not mm.group(1).lower().startswith(stem.encode())))
        comp = [c.decode('latin-1') for c in comp]
    out['bom'] = comp

    # --- параметры кириллицей из LargeText/BasicText ---
    txt = (sect('LargeText') + sect('BasicText')).decode('utf-8', 'replace')
    out['cyrillic_params'] = sorted(set(re.findall(
        r'[А-ЯЁ][А-ЯЁа-яё_]{3,28}', txt)))[:60]

    # --- масса: нет в файле ---
    out['mass_properties'] = None
    return out


if __name__ == '__main__':
    dirs = [l.strip().strip('"') for l in
            open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
            if l.strip()]
    models = []
    for dd in dirs:
        try:
            for f in os.listdir(dd):
                if f.lower().endswith(('.prt.1', '.asm.1')):
                    models.append(os.path.join(dd, f))
        except Exception:
            pass
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else len(models)
    OUT = r'D:\AI\repo\Creo\TOOLS\ftype_probe\plm_final.jsonl'
    ok = ops_n = surf_n = bom_n = ru_n = feat_n = 0
    with open(OUT, 'w', encoding='utf-8') as fh:
        for p in sorted(models)[:lim]:
            try:
                r = read_model(p)
            except Exception as e:
                continue
            ok += 1
            ops_n += len(r['operations'])
            surf_n += len(r['surfaces'])
            bom_n += len(r['bom'])
            ru_n += len(r['cyrillic_params'])
            feat_n += len(r['features'])
            fh.write(json.dumps(r, ensure_ascii=False) + '\n')
    print('ОБРАБОТАНО МОДЕЛЕЙ: %d' % ok)
    print('  операций      : %d' % ops_n)
    print('  поверхностей  : %d' % surf_n)
    print('  компонентов   : %d' % bom_n)
    print('  кириллических параметров: %d' % ru_n)
    print('  имён фич      : %d' % feat_n)
    print('файл: %s' % OUT)