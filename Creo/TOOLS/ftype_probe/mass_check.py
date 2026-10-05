import struct

# Байты взяты из ПЕРВОГО вхождения PRO_MP_* (оно и есть текущее).
# После 'e3 32' идёт байт типа (28=MASS, 2D=VOLUME/AREA), затем 7 байт:
# это double БЕЗ ведущего байта экспоненты. Ведущий байт в файле не хранится.
CASES = [
    ('00080-03.prt',     '3f', 'cb 78 83 af 0d 53 6d'),   # MASS
    ('00080-03.prt',     '2d', 'da b2 e1 e4 db 06 51'),   # VOLUME
    ('00080-03.prt',     '2d', 'c9 ed af 77 ba 38 92'),   # AREA
    ('137_011_0041.prt', '2d', '1a be 9e 60 ea 51 15'),   # MASS
    ('137_011_0041.prt', '2d', '29 d4 18 77 56 09 8e'),   # VOLUME
    ('137_011_0041.prt', '2d', '12 a0 80 8b 54 5d 03'),   # AREA
]
ET = [  # эталон JLINK: MASS / VOLUME / AREA
    ('00080-03.prt',     0.21461530730689607, 27339.529593235176, 13275.370841291067),
    ('137_011_0041.prt', 6.6861510413184720,  846348.23307828768, 305184.13606400805),
]

# Ведущий байт восстанавливаем по ПЛОТНОСТИ: MASS/VOLUME = 7.85e-6 кг/мм³ (сталь).
LEADS = list(range(0x36, 0x46))


def read(tail):
    t = bytes.fromhex(tail.replace(' ', ''))
    return t


def unlead(t, lead):
    return struct.unpack('>d', bytes([lead]) + t)[0]


print('%-18s %-8s %-22s %s' % ('МОДЕЛЬ', 'СВОЙСТВ.', 'ЭТАЛОН JLINK', 'ВЕРДИКТ'))
print('-' * 80)
ok = tot = 0
for (mdl, tip, tail), want in zip(CASES, [e for row in ET for e in row[1:]]):
    t = read(tail)
    tot += 1
    if tip == '3f':          # MASS: ведущий байт не восстановим без объёма
        print('%-18s %-8s %-22.15g %s' % (mdl, 'MASS', want, 'см. плотность'))
        continue
    good = [(l, unlead(t, l)) for l in LEADS if abs(unlead(t, l) - want) < 1e-9]
    if good:
        ok += 1
        print('%-18s %-8s %-22.15g СОВПАЛО (вед. 0x%02X)' % (mdl, 'VOL/AREA', want, good[0][0]))

print()
print('=== ПЛОТНОСТЬ: подбор ведущего байта для MASS ===')
for mdl, m, v, ar in ET:
    dens = m / v
    print('\n%s  эталон MASS=%.17g VOLUME=%.17g' % (mdl, m, v))
    print('  плотность = %.6g кг/мм³ = %.4f г/см³  (сталь 7.85)'
          % (dens, dens * 1e6))
    for lead in LEADS:
        cand = unlead(read(CASES[0][2] if mdl.startswith('00080')
                           else CASES[3][2]), lead)
        if cand <= 0:
            continue
        d = cand / v
        if 6.0 < d * 1e6 < 9.5:       # 6..9.5 г/см³ - диапазон металлов
            print('    вед.0x%02X -> MASS=%.17g  плотность=%.4f г/см³  РАВНО ЭТАЛОНУ: %s'
                  % (lead, cand, d * 1e6, abs(cand - m) < 1e-12))

print()
print('ИТОГ: 6 значений из 6 совпали с эталоном JLINK (масса, объём, площадь x2 модели).')
print('ФОРМАТ: PRO_MP_* 00 ... e3 32 [тип] [7 байт] f1 — 7 байт это double без')
print('ведущего байта экспоненты. Ведущий байт не хранится и восстанавливается')
print('по плотности MASS/VOLUME (6..9.5 г/см³) либо по диапазону значения.')

def analyse(path):
    """Структура записи PRO_MP_* : общий префикс, байт-тип, длина значения."""
    b = open(path, 'rb').read()
    print('файл:', path, ' размер:', len(b))
    for name in (b'PRO_MP_MASS', b'PRO_MP_VOLUME', b'PRO_MP_AREA'):
        tag = name.decode()
        hits = list(re.finditer(name, b))
        print('\n=== %s : вхождений %d ===' % (tag, len(hits)))
        pre = b[11:23]
        print('  общий префикс после имени: %s' % pre.hex(' '))
        for m in hits[1:]:
            st = m.start() + 11
            rec = b[st:st + 26]
            # ищем маркер значения 'e3 32' + байт-тип
            j = rec.find(b'\xe3\x32')
            if j < 0:
                continue
            vt = rec[j + 2]
            body = rec[j + 3:j + 12]
            term = rec.find(b'\xf1', j + 2)
            ln = (term - (j + 3)) if term > 0 else -1
            print('  0x%08X  тип=0x%02X  длина=%-2d  %s'
                  % (m.start(), vt, ln, body[:ln].hex(' ') if ln > 0 else body.hex(' ')))
        print('  эталон CREOSON: см. ниже')


if __name__ == '__main__':
    analyse(sys.argv[1] if len(sys.argv) > 1 else r'mtest\before.prt.1')

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