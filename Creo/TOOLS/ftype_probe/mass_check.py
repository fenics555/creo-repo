import struct, re, json, os, urllib.request

def call(c, f, s=None, d=None):
    b = {'command': c, 'function': f}
    if s:
        b['sessionId'] = s
    b['data'] = d or {}
    r = urllib.request.Request('http://127.0.0.1:8080/creoson',
        data=json.dumps(b).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'})
    return json.loads(urllib.request.urlopen(r, timeout=60).read().decode('utf-8'))


def read_props(path):
    """Читает PRO_MP_MASS / VOLUME / AREA по якорю '\\x2d' + be[1:8]."""
    b = open(path, 'rb').read()
    out = {}
    for prop in (b'PRO_MP_MASS', b'PRO_MP_VOLUME', b'PRO_MP_AREA'):
        vals = []
        for m in re.finditer(prop, b):
            win = b[m.start() + len(prop):m.start() + len(prop) + 40]
            # якорь: тег 0x2D, затем 7 байт хвоста double
            for i in range(len(win) - 8):
                if win[i] != 0x2D:
                    continue
                tail = win[i + 1:i + 8]
                if len(tail) != 7:
                    continue
                for lead in (0x40, 0x3F, 0x41):
                    try:
                        v = struct.unpack('>d', bytes([lead]) + tail)[0]
                    except Exception:
                        continue
                    if 1e-6 < abs(v) < 1e9:
                        vals.append((lead, v))
                        break
                if vals:
                    break
            if vals:
                break
        if vals:
            out[prop.decode()] = {'value': vals[0][1], 'lead': hex(vals[0][0])}
    return out


def candidates(path, prop=b'PRO_MP_MASS'):
    """Все значения по правилу '2D + be[1:8]', перебор ведущего байта."""
    b = open(path, 'rb').read()
    out = []
    for m in re.finditer(prop, b):
        win = b[m.start() + len(prop):m.start() + len(prop) + 40]
        for i in range(len(win) - 8):
            if win[i] != 0x2D:
                continue
            tail = win[i + 1:i + 8]
            if len(tail) != 7:
                continue
            got = []
            for lead in (0x3F, 0x40, 0x41):
                try:
                    v = struct.unpack('>d', bytes([lead]) + tail)[0]
                except Exception:
                    continue
                if 1e-4 < abs(v) < 1e6:
                    got.append((lead, v))
            if got:
                out.append(got)
            break
    return out


MODELS = [r'Z:\PTC\Work\137.011.0041\137_011_0041.prt',
          r'Z:\PTC\Work\00080\00080-03.prt',
          r'Z:\PTC\Work\00612\00612.prt']

for M in MODELS:
    if not os.path.exists(M + '.1'):
        continue
    s = call('connection', 'connect')['sessionId']
    if call('file', 'open', s, {'file': M})['status']['error']:
        continue
    want = None
    pl = (call('parameter', 'list', s, {'file': M}).get('data') or {}).get('paramlist') or []
    for p in pl:
        if p['name'] == 'MASS':
            want = float(p['value'])
    cs = candidates(M + '.1')
    print('%-20s вхождений=%-4d эталон=%s'
          % (os.path.basename(M), len(cs), ('%.15g' % want) if want else '—'))
    for i, g in enumerate(cs[:4]):
        txt = '  '.join('0x%02X->%.10g' % (l, v) for l, v in g)
        mark = ''
        for l, v in g:
            if want is not None and abs(v - want) < 1e-9:
                mark = '   <<< ЭТАЛОН (вед. 0x%02X)' % l
        print('   [%d] %s%s' % (i, txt, mark))
    print()


def read_mass(path):
    """Масса = PRO_MP_MASS ... <тег> <be[1:8]>."""
    b = open(path, 'rb').read()
    out = []
    for m in re.finditer(rb'PRO_MP_MASS', b):
        win = b[m.start() + 10:m.start() + 60]
        for off in range(len(win) - 8):
            tail = win[off + 1:off + 8]
            if len(tail) != 7:
                continue
            for lead in (0x40, 0x3F, 0x41, 0x3E, 0x42, 0x00):
                try:
                    v = struct.unpack('>d', bytes([lead]) + tail)[0]
                except Exception:
                    continue
                if 0.001 < abs(v) < 1e9:
                    out.append((hex(m.start()), hex(win[off]), lead,
                                tail.hex(' ').upper(), v))
                    break
            if out and out[-1][0] == hex(m.start()):
                break
    return out


import os
dirs = [l.strip().strip('"') for l in
        open(r'Z:\PTC\Work\search.pro', encoding='utf-8', errors='ignore')
        if l.strip()]
files = []
for dd in dirs:
    try:
        for f in os.listdir(dd):
            if f.lower().endswith(('.prt.1', '.asm.1')):
                files.append(os.path.join(dd, f))
    except Exception:
        pass
import random
random.seed(3)
random.shuffle(files)

print('ПРОВЕРКА МАССЫ НА %d МОДЕЛЯХ\n' % min(25, len(files)))
good = 0
for p in files[:25]:
    try:
        r = read_mass(p)
    except Exception:
        continue
    if not r:
        continue
    good += 1
    print('%-26s' % os.path.basename(p)[:26])
    for at, tagoff, lead, tail, v in r[:3]:
        print('    тег %s вед.байт 0x%02X  %s  = %.10g'
              % (tagoff, lead, tail, v))

V = 6.686151041318472
F = r'Z:\PTC\Work\137.011.0041\137_011_0041.prt.1'
b = open(F, 'rb').read()
print('эталон MASS = %.17g' % V)
print()

be = struct.pack('>d', V)
le = struct.pack('<d', V)
f4 = struct.pack('>f', V)
f4l = struct.pack('<f', V)
print('BE double : %s' % be.hex(' ').upper())
print('LE double : %s' % le.hex(' ').upper())
print('BE float  : %s' % f4.hex(' ').upper())
print()

for name, pat in (('BE double', be), ('LE double', le),
                  ('BE float', f4), ('LE float', f4l)):
    i = b.find(pat)
    cnt = 0
    k = 0
    while True:
        k = b.find(pat, k)
        if k < 0:
            break
        cnt += 1
        k += 1
    print('%-10s: вхождений %d %s' % (name, cnt,
          ('первое @0x%x' % i) if i >= 0 else '—'))

print()
print('=== байты ВОКРУГ каждого PRO_MP_MASS ===')
import re
seen = set()
for m in list(re.finditer(rb'PRO_MP_MASS', b))[:6]:
    p = m.start()
    win = b[p + 10:p + 34]
    key = win[:12].hex()
    if key in seen:
        continue
    seen.add(key)
    print('@%-9s %s' % (hex(p), win.hex(' ').upper()))
    # пробуем трактовать как 8 байт с разных смещений
    for off in range(0, min(20, len(win) - 8)):
        h = win[off:off + 8]
        try:
            vbe = struct.unpack('>d', h)[0]
            vle = struct.unpack('<d', h)[0]
        except Exception:
            continue
        if 1e-4 < abs(vbe) < 1e7:
            print('      BE@+%d = %.10g' % (off, vbe))
        if 1e-4 < abs(vle) < 1e7:
            print('      LE@+%d = %.10g' % (off, vle))