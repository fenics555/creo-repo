# -*- coding: utf-8 -*-
"""ДОЛГ №3: реальные обозначения и наименования в LargeText.
Ищем rel_model_name, уравнения отношений и готовые текстовые значения штампа.
Запуск: python designation.py <папка> [N]
Вывод: designation_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
KW = [b'rel_model_name', b'rel_', b'_call)', b'LOCAL_RESTR', b'if(', b'assign']
CYR = re.compile(rb'[\xd0-\xd1][\x80-\xbf](?:[\xd0-\xef][\x80-\xbf]){2,}')

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    files = []
    for root, dirs, fs in os.walk(base):
        for f in fs:
            if f.lower().endswith('.prt.1') or f.lower().endswith('.asm.1'):
                files.append(os.path.join(root, f))
        if len(files) > 30000:
            break
    random.seed(11)
    random.shuffle(files)

    out = io.open('designation_out.txt', 'w', encoding='utf-8')
    out.write('ДОЛГ №3: ОБОЗНАЧЕНИЯ / ОТНОШЕНИЯ · папка %s\n\n' % base)
    stat = collections.Counter()
    used = 0
    for fp in files:
        if used >= N:
            break
        try:
            data = open(fp, 'rb').read()
        except Exception:
            continue
        if b'rel_model_name' not in data:
            continue
        used += 1
        nm = os.path.basename(fp)
        out.write('=== %s (%d байт) ===\n' % (nm, len(data)))
        for kw in KW:
            c = data.count(kw)
            if c:
                stat[kw.decode('ascii', 'replace')] += 1
                out.write('   %-14s ×%d\n' % (kw.decode('ascii', 'replace'), c))
        # контекст вокруг rel_model_name
        s = 0
        for k in range(2):
            i = data.find(b'rel_model_name', s)
            if i < 0:
                break
            s = i + 1
            lo = max(0, i - 40)
            seg = data[lo:i + 90]
            asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in seg)
            out.write('   @%-8d %s\n' % (i, asc))
            # кириллица в этом окне
            for m in CYR.finditer(seg):
                try:
                    t = m.group().decode('utf-8')
                except Exception:
                    continue
                if len(t) > 3:
                    out.write('        кириллица: «%s»\n' % t)
        out.write('\n')
    out.write('=== СВОДКА ПО %d ФАЙЛАМ ===\n' % used)
    for k, v in stat.most_common():
        out.write('   %-16s в %d файлах\n' % (k, v))
    out.close()
    print('designation_out.txt used=%d' % used)

if __name__ == '__main__':
    main()