# -*- coding: utf-8 -*-
"""ПОКРЫТИЕ С УЧЁТОМ ОДНОБАЙТОВЫХ значений.
Таблица коротких значений уже есть в скилах:
   18=0.0  0F=1.0  0E=0.5  0D=0.25  07=0.001  ...
Плюс 3-байтовые: маркер 2F|48 + [E:F12].
Ищем, даёт ли учёт 1-байтовых рост покрытия с 13 %.
Запуск: python pntcover3.py [папка] [файлов]
Вывод: pntcover3_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
MARK3 = (0x2F, 0x48)

# короткие значения: байт -> значение (из словаря скилов)
SHORT = {0x18: 0.0, 0x0F: 1.0, 0x0E: 0.5, 0x0D: 0.25, 0x07: 0.001,
         0x10: 2.0, 0x11: 4.0, 0x12: 8.0, 0x13: 16.0, 0x14: 32.0,
         0x15: 64.0, 0x16: 128.0, 0x17: 256.0}

def val3(b0, b1, b2):
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    nf = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            if f.lower().endswith('.prt.1'):
                files.append(os.path.join(root, f))
        if len(files) > 30000:
            break
    random.seed(11)
    random.shuffle(files)

    out = io.open('pntcover3_out.txt', 'w', encoding='utf-8')
    out.write('ПОКРЫТИЕ С УЧЁТОМ 1-БАЙТОВЫХ ЗНАЧЕНИЙ · папка %s\n\n' % base)

    tb = t3 = t1 = 0
    n3 = n1 = 0
    good = 0
    recs = 0
    for fp in files[:nf]:
        try:
            data = open(fp, 'rb').read()
        except Exception:
            continue
        if b'crv_pnt_arr' not in data:
            continue
        hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
                for m in FIELD.finditer(data)]
        for i, (pos, nm, end) in enumerate(hits):
            if nm != 'crv_pnt_arr':
                continue
            nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
            payload = data[end:nxt]
            if not (8 <= len(payload) <= 120):
                continue
            body = payload[4:]
            recs += 1
            tb += len(body)
            used3 = used1 = 0
            vals = []
            k = 0
            while k < len(body):
                if body[k] in MARK3 and k + 2 < len(body):
                    vals.append(val3(body[k], body[k + 1], body[k + 2]))
                    used3 += 3
                    n3 += 1
                    k += 3
                elif body[k] in SHORT:
                    vals.append(SHORT[body[k]])
                    used1 += 1
                    n1 += 1
                    k += 1
                else:
                    k += 1
            good += sum(1 for v in vals if 0.001 <= abs(v) <= 1e5)
            t3 += used3
            t1 += used1

    out.write('записей:            %d\n' % recs)
    out.write('байт в массивах:    %d\n' % tb)
    out.write('покрыто 3-байт:     %d = %.1f %%\n' % (t3, 100.0 * t3 / max(1, tb)))
    out.write('покрыто 1-байт:     %d = %.1f %%\n' % (t1, 100.0 * t1 / max(1, tb)))
    out.write('ИТОГО покрытие:     %d = %.1f %%   (было 13.7 %%)\n'
              % (t3 + t1, 100.0 * (t3 + t1) / max(1, tb)))
    out.write('\nдекодировано чисел: 3-байт %d + 1-байт %d = %d\n' % (n3, n1, n3 + n1))
    out.write('правдоподобных:     %d = %.1f %%\n'
              % (good, 100.0 * good / max(1, n3 + n1)))
    out.close()
    print('pntcover3_out.txt cover=%.1f%% recs=%d' % (100.0 * (t3 + t1) / max(1, tb), recs))

if __name__ == '__main__':
    main()