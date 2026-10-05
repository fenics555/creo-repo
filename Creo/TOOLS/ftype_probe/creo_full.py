"""ПОЛНЫЙ ИЗВЛЕКАТЕЛЬ ФАЙЛОВ CREO — без Creo.

Читает оглавление #UGC_TOC, достаёт секции по адресам, разбирает записи.
Выход: JSON по каждой модели.
"""
import os, re, json, sys, struct

TOCRE = re.compile(
    rb'^([A-Za-z_][A-Za-z0-9_]*)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)'
    rb'\s+[0-9a-f]+\s+[0-9a-zA-Z_]+\s+(-?[0-9a-f]+)\s+([0-9a-f]{4})\s+([0-9a-f]{4})',
    re.M)

TYPE_CODES = ('group', 'dtmplane', 'csys', 'cutextrude', 'featround',
              'protrevolve', 'feathole', 'featsketch', 'featssrf', 'featpattern')

FEATURE_NAMES = ('DTM', 'LOCAL_GROUP', 'ASM_', 'PRT_CSYS', 'RIGHT', 'TOP',
                 'FRONT', 'BOTTOM', 'LEFT', 'BACK', 'WCS', 'COORD_SYS')

# --- МАССОВЫЕ СВОЙСТВА (проверено 04.10.2026, 6/6 против JLINK) -------------------
# PRO_MP_* \x00 ... \xe3\x32 [тип] [7 байт] ...
# 7 байт = IEEE-754 double БЕЗ старшего байта экспоненты. Старший байт не хранится.
# Восстановление: масса — по плотности (MASS/VOLUME = 6..9.5 г/см³, сталь 7.85);
# объём/площадь — согласованно с плотностью.
MP_LEADS = range(0x30, 0x50)


def _mp_tail(raw, name):
    """Все кандидаты на 7 байт значения рядом с 'PRO_MP_NAME'.

    После маркера \\xe3\\x32 идёт [байт типа] [7 байт] [терминатор f1/f7].
    Тип бывает 0x28 или 0x2D — поэтому перебираем позиции, а не ищем конкретный байт.
    Кандидат принимается, если сразу за 7 байтами стоит терминатор.
    """
    i = raw.find(name + b'\x00')
    if i < 0:
        return []
    j = raw.find(b'\xe3\x32', i, i + 120)
    if j < 0:
        return []
    out = []
    for k in range(j + 2, min(j + 8, len(raw) - 9)):
        if raw[k + 8] in (0xF1, 0xF7):
            out.append(raw[k + 1:k + 8])
    return out


def _val(t, lead):
    return struct.unpack('>d', bytes([lead]) + t)[0]


def mass_properties(raw):
    """{mass, volume, area, density_g_cm3}.

    Ведущий байт экспоненты в файле не хранится. Восстанавливаем так:
      - пара (mass, volume) — по плотности: 6..9.5 г/см³, металл около 7.85;
      - area — ведущий байт берём ТОТ ЖЕ, что у volume (проверено на 2 моделях:
        0x40 и 0x41 соответственно).
    """
    cms = _mp_tail(raw, b'PRO_MP_MASS')
    cvs = _mp_tail(raw, b'PRO_MP_VOLUME')
    cas = _mp_tail(raw, b'PRO_MP_AREA')
    if not cvs:
        return None
    best = None
    for tm in (cms or [None]):
        for tv in cvs:
            for lm in MP_LEADS:
                m = _val(tm, lm) if tm else 0.0
                if tm and m <= 0:
                    continue
                for lv in MP_LEADS:
                    v = _val(tv, lv)
                    if v <= 0 or not (1.0 <= v <= 1e9):
                        continue
                    if tm:
                        if not (0.001 <= m <= 1e4):
                            continue
                        d = m / v
                        if not (6.0e-6 <= d <= 9.5e-6):
                            continue
                    else:
                        d = None
                    area = _val(cas[0], lv) if cas else None
                    cand = (abs(d - 7.85e-6) if d else 0.0, m, v, area, d)
                    if best is None or cand[0] < best[0]:
                        best = cand
    if best is None:
        return None
    _, m, v, area, d = best
    return {'mass': m or None, 'volume': v, 'area': area,
            'density_g_cm3': (d * 1e6) if d else None}


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

    # поверхности: "Split Surface 1" 00 F6 00 "featssrf" 00 "Split_surface id 35186"
# -> имя оканчивается за 3 байта до featssrf (00 F6 00)
    stb = sect('MdlStatus')
    surf = []
    for mm in re.finditer(rb'featssrf\x00([\w_ ]+?) id (\d+)', stb):
        # структура: "<Имя>\x00\xf6\x00featssrf"
        # перед именем может НЕ быть NUL — значит имя = подряд идущие
        # печатные байты, заканчивающиеся перед маркером
        n1 = stb.rfind(b'\x00', 0, mm.start())
        n2 = n1 - 2 if (n1 >= 2 and stb[n1 - 1] == 0xF6) else n1
        q = n2
        while q > 0 and 32 <= stb[q - 1] < 127:
            q -= 1
        nm = stb[q:n2].decode('latin-1').strip()
        # перед именем может остаться хвост прошлого поля ("rSplit Surface 2")
        # имя всегда вида "Слово Слово N" — обрезаем по последнему совпадению
        m2 = re.search(r'[A-Z\xd0-\xd1][\w\xd0-\xd1]*(?: [\w\xd0-\xd1]+)* \d+$', nm)
        if m2:
            nm = m2.group(0)
        if len(nm) < 3 or not re.match(r'^[A-Za-z\xd0-\xd1]', nm):
            continue
        surf.append({'name': nm,
                     'kind': mm.group(1).decode('latin-1').strip(),
                     'id': int(mm.group(2))})
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

    # --- масса / объём / площадь (структура e3 32 + 7 байт, проверено) ---
    out['mass_properties'] = mass_properties(raw)
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