# -*- coding: utf-8 -*-
"""ДИФФЕРЕНЦИАЛЬНАЯ МЕТКА — оружие против «неизвестного формата».

Идея: положить в модель через Creo ЗАВЕДОМОЕ значение (500), сохранить,
затем положить другое (1000), сохранить. Сравнить два файла побайтово:
все изменившиеся байты — и есть «место», где живёт значение.
Формат знать НЕ НУЖНО.

Режимы:
  1) Сравнить ДВА файла:               python difftag.py <файл1> <файл2>
  2) Найти маркер в одном файле:      python difftag.py --find <файл> <значение>
Запуск:
  python difftag.py --find "D:\AI\PROBA\m500.prt.1" 500
  python difftag.py "D:\AI\PROBA\m500.prt.1" "D:\AI\PROBA\m1000.prt.1"
"""
import re, sys, io, struct

def val3(b1, b2):
    """упакованное число по подтверждённой формуле"""
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

def enc3(v):
    """обратная упаковка: значение -> байты (маркер подбирается отдельно)"""
    for m in (0x2F, 0x48):
        for e in range(0, 16):
            f = (v / (2 ** (e + 1)) - 1.0) * 4096
            if abs(f - round(f)) < 1e-9 and 0 <= round(f) <= 4095:
                fi = int(round(f))
                yield bytes([m, (e << 4) | (fi >> 8), fi & 0xFF])

def find_marker(path, value):
    data = open(path, 'rb').read()
    o = io.open('difftag_out.txt', 'w', encoding='utf-8')
    o.write('ПОИСК МАРКЕРА %s в %s (%d байт)\n\n' % (value, path, len(data)))
    try:
        f = float(value)
    except ValueError:
        f = None

    # 1) как ASCII
    a = str(value).encode()
    pos = [m.start() for m in re.finditer(re.escape(a), data)]
    o.write('ASCII «%s»: %d вхождений %s\n'
            % (a.decode(), len(pos), ['@%d' % p for p in pos[:20]]))
    # 2) как UTF-8 (кириллица, если маркер в тексте)
    try:
        u = str(value).encode('utf-8')
        posu = [m.start() for m in re.finditer(re.escape(u), data)]
        o.write('UTF-8  «%s»: %d вхождений\n' % (value, len(posu)))
    except Exception:
        pass
    # 3) как упакованное (маркер 2F/48)
    if f is not None:
        for seq in enc3(f):
            p = [m.start() for m in re.finditer(re.escape(seq), data)]
            if p:
                o.write('упаков. %s = %g : %d вхождений %s\n'
                        % (' '.join('%02X' % c for c in seq), f, len(p),
                           ['@%d' % x for x in p[:20]]))
    # 4) как BE-double
    if f is not None:
        for tag, e in (('BE', '>d'), ('LE', '<d')):
            b = struct.pack(e, f)
            p = [m.start() for m in re.finditer(re.escape(b), data)]
            if p:
                o.write('double %s %s : %d вхождений %s\n'
                        % (tag, b.hex(' '), len(p), ['@%d' % x for x in p[:20]]))
    # 5) как целое 16/32 бита
    if f is not None and f == int(f):
        iv = int(f)
        for bits, e in ((2, '>h'), (2, '<h'), (4, '>i'), (4, '<i')):
            b = struct.pack(e, iv).to_bytes(bits, 'big') if bits == 2 else struct.pack(e, iv)
            p = [m.start() for m in re.finditer(re.escape(b), data)]
            if p:
                o.write('int%d %s %s : %d вхождений %s\n'
                        % (bits * 8, e, b.hex(' '), len(p), ['@%d' % x for x in p[:20]]))
    # 6) сколько всего полных упакованных чисел равно значению
    if f is not None:
        cnt = 0
        spots = []
        for i in range(len(data) - 2):
            if data[i] in (0x2F, 0x48) and abs(val3(data[i + 1], data[i + 2]) - f) < 1e-9:
                cnt += 1
                if len(spots) < 20:
                    spots.append(i)
        o.write('\nПОЛНЫЙ ПЕРЕБОР упакованных: значению %s равны %d значений %s\n'
                % (f, cnt, ['@%d' % s for s in spots]))
    o.close()
    print('difftag_out.txt')

def diff(f1, f2):
    a = open(f1, 'rb').read()
    b = open(f2, 'rb').read()
    o = io.open('difftag_out.txt', 'w', encoding='utf-8')
    o.write('ДИФФЕРЕНЦИАЛЬНАЯ МЕТКА\n%s (%d)\n%s (%d)\n\n'
            % (f1, len(a), f2, len(b)))
    n = min(len(a), len(b))
    runs = []
    i = 0
    while i < n:
        if a[i] != b[i]:
            j = i
            while j < n and a[j] != b[j]:
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    o.write('ИЗМЕНИВШИХСЯ БАЙТОВ: %d (из %d)\n' % (
        sum(j - i for i, j in runs), n))
    o.write('УЧАСТКОВ РАЗЛИЧИЙ: %d\n\n' % len(runs))
    for i, j in runs[:60]:
        lo = max(0, i - 12)
        o.write('@%-9d  A=%s\n' % (i, ' '.join('%02X' % c for c in a[lo:j + 12])))
        o.write('            B=%s\n' % ' '.join('%02X' % c for c in b[lo:j + 12]))
        # если участок похож на упакованное число — декодируем
        for k in range(i, max(i, j - 1)):
            if k + 2 < n and a[k] in (0x2F, 0x48) and b[k] in (0x2F, 0x48):
                o.write('            упаков. A=%g  B=%g\n'
                        % (val3(a[k + 1], a[k + 2]), val3(b[k + 1], b[k + 2])))
                break
    o.close()
    print('difftag_out.txt')

def main():
    if '--find' in sys.argv:
        i = sys.argv.index('--find')
        find_marker(sys.argv[i + 1], sys.argv[i + 2])
    elif len(sys.argv) >= 3:
        diff(sys.argv[1], sys.argv[2])
    else:
        print(__doc__)

if __name__ == '__main__':
    main()