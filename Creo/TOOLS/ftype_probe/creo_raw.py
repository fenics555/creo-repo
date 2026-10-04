"""УНИВЕРСАЛЬНЫЙ ЧИТАТЕЛЬ ФАЙЛОВ CREO — только байты, без Creo.

КРИТЕРИЙ "ЧИТАЕМ ЛОБ":
  файл читается лоб, если его полезная часть лежит ОТКРЫТЫМ ТЕКСТОМ.
  Проверка одной строкой: data[:2048].decode('ascii','replace') читаемо
  и содержит служебные маркеры (#UGC, @тег, E0 <len>).
"""
import os, re, json, sys

TEXT_MARKERS = [b'#UGC:', b'#-END_OF_UGC_HEADER', b'@model_name',
                b'@comp_ids', b'@depend', b'to_name', b'#P_OBJECT']

TAGVAL = re.compile(rb'@(\w+)\s+\d+\s+\d+\s*\n\d+\s+\d+\s+([^\n\x00]{1,120})')
TONAME = re.compile(rb'E0 [\dA-Fa-f]{1,3} to_name\x00(?:[\dA-Fa-f]{1,3} )?([^\x00]{2,48})')
DIRECT = re.compile(rb'd \d+ \(([A-Za-z0-9_\-\.]{2,48}\.(?:[Pp][Rr][Tt]|[Aa][Ss][Mm]))\)')
PARAM = re.compile(rb'\xe3([A-Za-z\xd0-\xd1][^\x00]{1,40})\x00')


def is_plain_text(data):
    head = data[:2048]
    try:
        head.decode('ascii')
    except UnicodeDecodeError:
        return False
    return any(m in data[:40000] for m in TEXT_MARKERS)


def read_creo(path):
    d = open(path, 'rb').read()
    name = os.path.basename(path)
    ext = 'asm' if '.asm' in name.lower() else 'prt'
    head = d[:200].decode('ascii', 'replace')

    out = {
        'file': name,
        'path': path,
        'kind': ext,
        'readable_raw': is_plain_text(d),
        'is_cnc_model': 'ASSEM_MFG' in d[:2000].decode('latin-1'),
    }

    # ---- текстовые поля заголовка ----
    fields = {}
    for m in TAGVAL.finditer(d[:40000]):
        fields.setdefault(m.group(1).decode(), m.group(2).decode('latin-1').strip())
    out['fields'] = fields

    # ---- состав изделия ----
    bom = []
    stem = name.split('.')[0].upper()
    for m in DIRECT.finditer(d):
        s = m.group(1).decode('latin-1').strip()
        if s.split('.')[0].upper() != stem:
            bom.append(s)
    for m in TONAME.finditer(d):
        s = m.group(1).decode('latin-1').strip()
        if s.upper() != stem and not s.upper().startswith(stem):
            item = s + '.ASM'
            if item not in bom:
                bom.append(item)
    out['bom'] = sorted(set(bom))
    out['component_count'] = len(out['bom'])

    # ---- автор, дата, комментарий ----
    out['author'] = fields.get('name', '')
    out['revnum'] = fields.get('revnum', '')
    out['comment'] = fields.get('comment', '')
    out['date'] = ''
    if fields.get('tm_year'):
        out['date'] = '%s-%02s-%02s' % (fields.get('tm_year', ''),
                                         fields.get('tm_mon', ''),
                                         fields.get('tm_mday', ''))

    # ---- параметры кириллицей (UTF-8) ----
    ru = []
    for m in PARAM.finditer(d):
        raw = m.group(1)
        if max(raw) > 127:
            try:
                s = raw.decode('utf-8')
            except UnicodeDecodeError:
                continue
            if len(s) >= 3:
                ru.append(s)
    out['cyrillic_fields'] = sorted(set(ru))[:40]

    out['mass'] = None
    return out


if __name__ == '__main__':
    dirs = [l.strip().strip('"') for l in
            open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
            if l.strip()]
    targets = []
    for dd in dirs:
        try:
            for f in os.listdir(dd):
                if f.lower().endswith(('.prt.1', '.asm.1')):
                    targets.append(os.path.join(dd, f))
        except Exception:
            pass
    if len(sys.argv) > 1:
        targets = targets[:int(sys.argv[1])]

    ok = 0
    text_ok = 0
    withbom = 0
    comps = 0
    withru = 0
    withmeta = 0
    n = 0
    outp = r'D:\AI\repo\Creo\TOOLS\ftype_probe\creo_raw_all.jsonl'
    with open(outp, 'w', encoding='utf-8') as fh:
        for t in sorted(targets):
            try:
                r = read_creo(t)
            except Exception:
                continue
            n += 1
            ok += 1
            text_ok += r['readable_raw']
            withbom += r['component_count'] > 0
            comps += r['component_count']
            withru += len(r['cyrillic_fields']) > 0
            withmeta += bool(r['author'] or r['date'])
            fh.write(json.dumps(r, ensure_ascii=False) + '\n')

    print('ФАЙЛОВ ПРОЧИТАНО:      %d' % ok)
    print('  читаются лоб (текст): %d  (%.0f%%)' % (text_ok, text_ok * 100.0 / max(1, ok)))
    print('  с составом (BOM):     %d' % withbom)
    print('  компонентов всего:    %d' % comps)
    print('  с кириллицей:         %d' % withru)
    print('  с автором/датой:      %d' % withmeta)
    print()
    print('файл: %s' % outp)