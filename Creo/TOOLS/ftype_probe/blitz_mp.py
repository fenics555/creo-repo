import os, struct, re

path = r'Z:\PTC\Work\IS-10.001.001.003\is-10_001_001_003.prt.1'
d = open(path, 'rb').read()
TARGET = 0.625306586880975

def near(val, tag, label):
    """Ищем val в форме: тег + полные 8 байт BE"""
    be = struct.pack('>d', val)
    print('--- %s: ищем %s' % (label, be.hex(' ').upper()))
    hits = []
    for m in re.finditer(rb'\xe3([A-Za-z_][A-Za-z0-9_]{1,30})\x00', d):
        nm = m.group(1).decode('latin-1')
        win = d[m.end():m.end() + 60]
        j = win.find(be)
        if j >= 0:
            hits.append((nm, win[max(0, j - 12):j + 8].hex(' ').upper()))
    if hits:
        for nm, h in hits:
            print('   ПОЛНЫЙ 8-БАЙТОВЫЙ DOUBLE: %s  ctx=%s' % (nm, h))
    else:
        print('   полного 8-байтового double НЕТ нигде')
    return hits

print('=== PRO_MP_* : полная форма 0x6253 ===')
near(TARGET, b'\xed', 'MASS')

print()
print('=== Все PRO_MP_* записи и их хвосты ===')
for m in re.finditer(rb'\xe3(PRO_MP_[A-Za-z0-9_]{1,30})\x00', d):
    nm = m.group(1).decode('latin-1')
    win = d[m.end():m.end() + 30]
    print('   %-22s %s' % (nm, win.hex(' ').upper()))

print()
print('=== Ищем 3F E4 02 82 F5 94 11 CB где угодно в файле ===')
full = struct.pack('>d', TARGET)
idx = [hex(i) for i in range(len(d)) if d.startswith(full, i)]
print('   полное 8-байтовое вхождение MASS: %s' % (idx if idx else 'НЕТ НИГДЕ'))
part = full[2:]
idx2 = [hex(i) for i in range(len(d)) if d.startswith(part, i)]
print('   хвост be[2:8] встречается %d раз: %s' % (len(idx2), idx2[:8]))

print()
print('=== Контекст секции PRO_MP_MASS (первые 40 байт после имени) ===')
i = d.find(b'\xe3PRO_MP_MASS\x00')
print('смещение: %s' % hex(i) if i >= 0 else 'PRO_MP_MASS не найдено')
if i >= 0:
    print(d[i:i + 80].hex(' ').upper())