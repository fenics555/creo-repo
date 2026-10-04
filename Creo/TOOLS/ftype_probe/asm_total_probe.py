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
BC = re.compile(rb'@bom_count\s+\d+\s+\d+\s+(\d+)')

kinds = {}
withbom = []
for a in asms:
    try:
        head = open(a, 'rb').read(1200)
    except Exception:
        continue
    m = HEAD.search(head)
    kind = m.group(1).decode() if m else '?'
    kinds[kind] = kinds.get(kind, 0) + 1
    b = BC.search(head)
    if b:
        withbom.append((os.path.basename(a), kind, int(b.group(1))))

print('ВСЕГО .asm.1: %d' % len(asms))
print()
print('=== ТИПЫ СБОРОК (поле #UGC:2) ===')
for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
    print('   %-28s %d' % (k, v))
print()
print('=== СБОРКИ С @bom_count: %d ===' % len(withbom))
for nm, k, c in sorted(withbom, key=lambda x: -x[2])[:20]:
    print('   %-34s %-22s bom_count=%d' % (nm[:34], k, c))

ASM = r'Z:\PTC\Work\00080\00080-03.asm.1'
d = open(ASM, 'rb').read()
print('СБОРКА: %s (%d байт)' % (os.path.basename(ASM), len(d)))
print()

# ---------- 1. ТЕКСТОВЫЙ ЗАГОЛОВОК: @bom_count ----------
print('=== 1. ТЕКСТОВЫЙ ЗАГОЛОВОК (первые 900 байт) ===')
print(d[:900].decode('ascii', 'replace'))
print()

print('=== 2. ВСЕ @-теги ===')
for m in re.finditer(rb'@[A-Za-z_]+[^\n]*', d[:4000]):
    print('   %s' % m.group(0).decode('ascii', 'replace').strip())

print()
print('=== 3. ВСЕ .prt/.asm упоминания с префиксами ===')
PAT = re.compile(rb'([A-Za-z0-9_\-\. ]{2,44}\.(?:[Pp][Rr][Tt]|[Aa][Ss][Mm]))')
seen = {}
for m in PAT.finditer(d):
    s = m.group(1).decode('latin-1').strip()
    if s not in seen:
        seen[s] = (hex(m.start()), d[max(0, m.start()-8):m.start()].hex(' ').upper())
print('уникальных: %d' % len(seen))
for s, (a, p) in sorted(seen.items()):
    print('   %-30s @%-9s префикс: %s' % (s[:30], a, p))