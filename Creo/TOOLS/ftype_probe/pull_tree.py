import sys, re
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
from creo_sections import read_toc

P = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
toc, _ = read_toc(P)
off, ln = toc['MdlStatus']
d = open(P, 'rb').read()
blob = d[off:off + ln]
print('СЕКЦИЯ MdlStatus @0x%x  %d байт\n' % (off, ln))
txt = blob.decode('utf-8', 'replace')

# записи: feat_name <ИМЯ> ... icon_name <ТИП>, плюс связи "<ТИП> id <N>"
NAME = re.compile(r'feat_name[^А-ЯA-Za-z]{0,8}'
                  r'([А-ЯЁA-Z][А-ЯЁа-яёA-Za-z0-9_ ]{1,30}?)[^\wА-я]{1,6}'
                  r'(?:icon_name[^a-z]{0,8})?([a-z]{3,12})?')
CODE = re.compile(r'\x00([a-z]{4,12})\x00([А-ЯЁ][А-ЯЁа-яё ]{2,28}\d?)')

print('--- пары ИМЯ + код типа ---')
pairs = []
for m in CODE.finditer(txt):
    code, ru = m.group(1), m.group(2).strip()
    pairs.append((ru, code))
seen = set()
for ru, code in pairs:
    if ru in seen:
        continue
    seen.add(ru)
    print('   %-28s %s' % (ru, code))
print()
print('уникальных операций: %d' % len(seen))

print()
print('--- все уникальные коды типов в секции ---')
allcodes = {}
for m in re.finditer(r'\x00([a-z]{4,12})\x00', txt):
    c = m.group(1)
    allcodes[c] = allcodes.get(c, 0) + 1
for c, n in sorted(allcodes.items(), key=lambda x: -x[1])[:22]:
    print('   %-16s %d' % (c, n))

print()
print('--- имена фич с латиницей/номерами ---')
fn = sorted(set(re.findall(r'\x00(DTM\d+|LOCAL_GROUP\d*|ASM_[A-Z_]+|'
                          r'PRT_CSYS_DEF|WCS|COORD_SYS)\x00', txt)))
print('   %d шт: %s' % (len(fn), ', '.join(fn[:20])))