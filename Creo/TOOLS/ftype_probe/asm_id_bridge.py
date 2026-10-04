import os, re

dirs = [l.strip().strip('"') for l in
        open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
        if l.strip()]
asms = []
for dd in dirs:
    try:
        for f in os.listdir(dd):
            if f.lower().endswith('.asm.1'):
                asms.append(os.path.join(dd, f))
    except Exception:
        pass

HEAD = re.compile(rb'#UGC:2\s+([A-Z_/]*)')
TAGLINE = re.compile(rb'@(\w+)\s+(\d+)\s+(\d+)\s*$', re.M)
VAL = re.compile(rb'^\d+\s+(\d+)\s+(.*)$', re.M)

for a in asms:
    try:
        d = open(a, 'rb').read(8000)
    except Exception:
        continue
    m = HEAD.search(d)
    kind = m.group(1).decode() if m else '?'
    if 'ASSEM_MFG' in kind:
        continue
    if b'@comp_ids' not in d:
        continue

    nm = os.path.basename(a)
    print('=' * 66)
    print('%s   [%s]' % (nm[:44], kind))
    # все @model_name со значениями
    names = []
    cur = None
    for line in d.split(b'\n'):
        t = line.strip()
        if t.startswith(b'@model_name'):
            cur = '@model_name'
            continue
        if t.startswith(b'@'):
            cur = None
            continue
        if cur and t:
            parts = t.split(b' ', 2)
            if len(parts) >= 3:
                names.append(parts[2].decode('latin-1').strip())
                cur = None
    # все .prt/.asm в шапке
    refs = sorted(set(x.decode('latin-1').strip() for x in
                      re.findall(rb'[A-Za-z0-9_\-\.]{2,40}\.(?:[Pp][Rr][Tt]|[Aa][Ss][Mm])', d)))
    print('  @model_name значений: %d  -> %s' % (len(names), names[:6]))
    print('  ссылок .prt/.asm в шапке: %d -> %s' % (len(refs), refs[:6]))