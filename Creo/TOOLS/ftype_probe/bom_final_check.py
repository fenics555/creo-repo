import os, re

ASM = r'Z:\PTC\Work\00080\00080-03.asm.1'
d = open(ASM, 'rb').read()
print('СБОРКА: %s (%d байт)' % (os.path.basename(ASM), len(d)))
print()

# Гибридный метод comp_type + текстовый id
PAT = re.compile(rb'id \d+ \(([A-Za-z0-9_\-\. ]+\.(?:[Pp][Rr][Tt]|[14A-Za-z][14A-Za-z][Mm]))\)')
hits = [m.group(1).decode('latin-1') for m in PAT.finditer(d)]
uniq = sorted(set(hits))
print('BOM по гибридному методу: %d вхождений, %d уникальных' % (len(hits), len(uniq)))
for c in uniq[:20]:
    print('   ->', c)
print()

# Любые .prt/.asm упоминания как fallback
ALL = re.compile(rb'([A-Za-z0-9_\-\. ]{2,40}\.(?:prt|PRT|asm|ASM))')
allh = sorted(set(m.group(1).decode('latin-1') for m in ALL.finditer(d)))
print('ЛЮБЫЕ упоминания .prt/.asm в файле: %d уникальных' % len(allh))
for c in allh[:25]:
    print('   ?', c)