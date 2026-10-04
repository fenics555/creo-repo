import os

dirs = [l.strip().strip('"') for l in
        open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
        if l.strip()]
asm = []
prt = 0
for dd in dirs:
    try:
        for f in os.listdir(dd):
            lf = f.lower()
            if lf.endswith('.asm.1'):
                asm.append(os.path.join(dd, f))
            elif lf.endswith('.prt.1'):
                prt += 1
    except Exception:
        pass

print('папок в search.pro: %d' % len(dirs))
print('.prt.1 найдено: %d' % prt)
print('.asm.1 найдено: %d' % len(asm))
print()
for a in asm[:20]:
    print('   %-60s %d КБ' % (a[-60:], os.path.getsize(a) // 1024))