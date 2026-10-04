import os, re

dirs = [l.strip().strip('"') for l in
        open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
        if l.strip()]
target = None
allasm = []
for dd in dirs:
    try:
        for f in os.listdir(dd):
            if f.lower().endswith('.asm.1'):
                p = os.path.join(dd, f)
                allasm.append(p)
                if f.lower() == 'most-75.asm.1':
                    target = p
    except Exception:
        pass

print('найдено most-75.asm.1: %s' % (target or 'НЕТ'))
if not target:
    print('доступные most-*:\n%s' % '\n'.join(
        '   ' + os.path.basename(x) for x in allasm if 'most' in x.lower()))
    raise SystemExit(1)

d = open(target, 'rb').read()
print('ФАЙЛ: %s (%d байт)' % (target, len(d)))
print()

print('=== 1. ВСЕ @-ТЕГИ ===')
tags = sorted(set(m.group(0).decode() for m in
                  re.finditer(rb'@[A-Za-z0-9_]{2,24}', d)))
print('уникальных: %d' % len(tags))
print('   %s' % ', '.join(tags[:70]))
print()

print('=== 2. ССЫЛКИ НА ФАЙЛЫ (сторонние) ===')
P = re.compile(rb'([A-Za-z0-9_\-\. ]{2,44}\.(?:[Pp][Rr][Tt]|[Aa][Ss][Mm]))')
seen = {}
for m in P.finditer(d):
    s = m.group(1).decode('latin-1').strip()
    if s not in seen:
        seen[s] = (hex(m.start()), d[max(0, m.start()-6):m.start()].hex(' ').upper())
print('уникальных: %d' % len(seen))
for s, (a, p) in sorted(seen.items()):
    mark = '  <<< СТОРОННИЙ' if 'most-75' not in s.lower() else ''
    print('   %-34s @%-9s префикс %s%s' % (s[:34], a, p, mark))