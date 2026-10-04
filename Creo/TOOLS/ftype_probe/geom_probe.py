import sys, re
sys.path.insert(0, r'D:\AI\repo\Creo\TOOLS\ftype_probe')
from creo_sections import read_toc

P = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
toc, _ = read_toc(P)
off, ln = toc['MdlStatus']
d = open(P, 'rb').read()
blob = d[off:off + ln]
txt = blob.decode('utf-8', 'replace')

i = txt.find('featssrf')
print('=== ПЕРВАЯ ЗАПИСЬ featssrf (контекст ±700 символов) ===')
print(repr(txt[max(0, i - 700):i + 700]))
print()

print('=== ВСЕ ИМЕНА ПОЛЕЙ рядом с featssrf ===')
seg = txt[max(0, i - 3000):i + 3000]
fields = sorted(set(m.group(1) for m in
                    re.finditer(r'([a-z][a-z0-9_]{2,30})\x00', seg)))
print(', '.join(fields[:60]))
print()

print('=== ЧТО ИДЁТ ПОСЛЕ featssrf (имена значений) ===')
tail = txt[i:i + 1500]
vals = re.findall(r'\x00([^\x00]{1,40})\x00', tail)
print(vals[:40])