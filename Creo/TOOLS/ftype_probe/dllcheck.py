import struct, os, sys

DLL = r'D:\PTC\CREO13\Creo 13.4.1.0\Common Files\x86e_win64\lib\jnicipjavamtz.dll'
LIBDIR = os.path.dirname(DLL)

def imports(path):
    d = open(path, 'rb').read()
    pe = struct.unpack_from('<I', d, 0x3C)[0]
    assert d[pe:pe+4] == b'PE\x00\x00'
    nsec = struct.unpack_from('<H', d, pe + 6)[0]
    optsize = struct.unpack_from('<H', d, pe + 20)[0]
    opt = pe + 24
    magic = struct.unpack_from('<H', d, opt)[0]
    dd = opt + (112 if magic == 0x20B else 96)
    imp_rva = struct.unpack_from('<I', d, dd + 8)[0]  # import directory
    imp_sz = struct.unpack_from('<I', d, dd + 12)[0]
    secs = []
    so = pe + 24 + optsize
    for i in range(nsec):
        b = so + i * 40
        va = struct.unpack_from('<I', d, b + 12)[0]
        vs = struct.unpack_from('<I', d, b + 8)[0]
        raw = struct.unpack_from('<I', d, b + 20)[0]
        secs.append((va, max(vs, raw or vs), raw))
    def r2o(rva):
        for va, sz, raw in secs:
            if va <= rva < va + sz:
                return raw + (rva - va)
        return None
    out = []
    off = r2o(imp_rva)
    while True:
        ent = d[off:off + 20]
        if len(ent) < 20 or ent == b'\x00' * 20:
            break
        name_rva = struct.unpack_from('<I', ent, 12)[0]
        if not name_rva:
            break
        no = r2o(name_rva)
        end = d.index(b'\x00', no)
        out.append(d[no:end].decode('latin-1'))
        off += 20
    return out

names = imports(DLL)
print('DLL: %s' % os.path.basename(DLL))
print('зависимостей: %d' % len(names))
print()
local = set(f.lower() for f in os.listdir(LIBDIR))
missing = []
for n in names:
    low = n.lower()
    found = low in local or any(low in f for f in local)
    if not found:
        missing.append(n)
    print('  %-32s %s' % (n, 'есть' if found else '*** НЕТ РЯДОМ ***'))
print()
print('НЕ НАЙДЕНО: %d' % len(missing))
for m in missing:
    print('   ', m)