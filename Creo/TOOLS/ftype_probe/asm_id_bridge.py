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


def grab(d, tag, limit=6):
    """Собирает значения тега: @tag N L -> 'obj N VALUE'."""
    out = []
    cur = False
    for line in d.split(b'\n'):
        t = line.strip()
        if t.startswith(b'@' + tag):
            cur = True
            continue
        if t.startswith(b'@'):
            cur = False
            continue
        if cur and t:
            parts = t.split(b' ', 2)
            if len(parts) >= 3:
                out.append(parts[2].decode('latin-1', 'replace').strip())
            elif len(parts) == 2:
                out.append(parts[1].decode('latin-1', 'replace').strip())
            cur = False
            if len(out) >= limit:
                break
    return out


rows = []
for a in sorted(asms):
    try:
        d = open(a, 'rb').read(20000)
    except Exception:
        continue
    m = HEAD.search(d)
    kind = m.group(1).decode() if m else '?'
    nm = os.path.basename(a)

    mn = grab(d, b'model_name')
    comp = grab(d, b'comp_ids')
    dt = grab(d, b'comp_dep_types')
    dep = grab(d, b'dep_type')
    rev = grab(d, b'revnum')
    au = grab(d, b'name')
    cm = grab(d, b'comment')
    bc = grab(d, b'bom_count')

    # компонент = второй @model_name (первый = сама сборка)
    real = mn[1] if len(mn) > 1 else ''
    differs = real and real.upper() != (mn[0].upper() if mn else '')
    rows.append((nm, kind, mn, real, differs, comp, dt, dep, rev, au, cm, bc))

print('ВСЕГО .asm.1: %d' % len(asms))
real_asm = [r for r in rows if 'ASSEM_MFG' not in r[1]]
print('без ASSEM_MFG: %d, из них с @comp_ids: %d'
      % (len(real_asm), len([r for r in real_asm if r[5]])))
print()
print('%-30s %-26s %-10s %-12s %-14s' % ('ФАЙЛ', 'СОСТАВ (2-й @model_name)', 'revnum', 'автор', 'компон. ID'))
print('-' * 100)
for r in rows:
    if 'ASSEM_MFG' in r[1]:
        continue
    comp_txt = ('%s %s' % (r[3], '<<< РАЗНЫЙ' if r[4] else '(дубль)')) if r[3] else '-'
    print('%-30s %-26s %-10s %-12s %s'
          % (r[0][:30], comp_txt[:26], ','.join(r[8][:2])[:10],
             ','.join(r[9][:1])[:12], ','.join(r[5][:4])))
print()
print('=== РАЗНЫЕ (настоящие сборки) ===')
for r in rows:
    if r[4]:
        print('   %-32s -> %s' % (r[0][:32], r[3]))
print()
print('=== пример @comment (кириллица) ===')
for r in rows[:6]:
    if r[10]:
        print('   %-30s %r' % (r[0][:30], r[10][:70]))

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