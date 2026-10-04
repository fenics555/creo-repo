#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""creo-read — ЕДИНЫЙ ПАРСЕР ФАЙЛОВ CREO «В ЛОБ».

ПРОВЕРЕННЫЕ механизмы (подтверждены замерами на боевой базе):
  --bom   состав сборки (comp_type + записи «id N (ИМЯ.PRT)»)
  --tree  дерево верхнего уровня (узлы + ID)
  --mass  объём и площадь (ED + BE-double)
  --dims  имена размеров
  --geom  геометрия: упакованные координаты
  --meta  инвентаризация полей
  --audit прогон всех механизмов по выборке

Режим ТОЛЬКО ЧТЕНИЕ.
python creo_read.py <файл> [--bom --mass --dims]
python creo_read.py <папка> --audit --limit 30
"""
import re, sys, os, io, glob, struct, collections

MARK3 = (0x2F, 0x48)
FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_\.\-\[\]]{1,60})\x00')
PRTN = re.compile(rb'([A-Za-z0-9][A-Za-z0-9_\-\.]{2,40}\.PRT)(?![A-Za-z0-9])', re.I)
JRN = re.compile(rb'\x20\x69\x64\x20[\x30-\x39]{1,5}\x20\x28'
                 rb'([A-Za-z0-9][A-Za-z0-9_\-\.]{1,40}\.PRT)\x29')

def sections(data):
    out = [(m.end(), m.group(1).decode())
           for m in re.finditer(rb'\n#([A-Za-z_][A-Za-z0-9_]{2,30})[\r\n]', data)]
    out.sort()
    return out

def sec_of(secs, pos):
    cur = '?'
    for s, n in secs:
        if s <= pos:
            cur = n
        else:
            break
    return cur

def val3(b1, b2):
    e = (b1 & 0xF0) >> 4
    f = ((b1 & 0x0F) << 8) | b2
    return 2 ** (e + 1) * (1 + f / 4096.0)

def payload_of(data, nm):
    """Все payload'ы поля nm (значение до следующего поля)."""
    hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
            for m in FIELD.finditer(data)]
    out = []
    for i, (pos, n, end) in enumerate(hits):
        if n != nm:
            continue
        nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 200)
        out.append((pos, data[end + 3:nxt]))   # маркер F9 XX 04 = 3 байта
    return out

def cmd_bom(data, o):
    hits = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
            for m in FIELD.finditer(data)]
    A, B = set(), set()
    for i, (pos, nm, end) in enumerate(hits):
        if nm != 'feat_name':
            continue
        if b'comp_type\x00\x02' in data[max(0, pos - 220):pos]:
            nxt = hits[i + 1][0] if i + 1 < len(hits) else min(len(data), end + 220)
            p = PRTN.search(data[end:nxt])
            if p:
                A.add(p.group(1).upper().decode())
    for m in JRN.finditer(data):
        B.add(m.group(1).upper().decode())
    parts = A | B
    o.write('СОСТАВ СБОРКИ: %d деталей (comp_type %d | «id N» %d)\n'
            % (len(parts), len(A), len(B)))
    for p in sorted(parts):
        o.write('   %s\n' % p)
    return bool(parts)

def cmd_tree(data, o):
    secs = sections(data)
    o.write('ДЕРЕВО: %d секций\n' % len(secs))
    pat = re.compile(rb'\xE3(.)(.)\x75\x00\x00\xE3([A-Za-z0-9_\-\.]{1,40})\x00')
    n = 0
    for m in pat.finditer(data):
        idv = (m.group(1)[0] << 8) | m.group(2)[0]
        o.write('  ID 0x%04X  %-18s [%s]\n'
                % (idv, m.group(3).decode('ascii', 'replace'), sec_of(secs, m.start())))
        n += 1
        if n > 40:
            o.write('  ...обрезано\n'); break
    return n > 0

def cmd_mass(data, o):
    o.write('МАССОВЫЕ СВОЙСТВА\n')
    got = False
    for name, key in (('volume', 'объём'), ('surfarea', 'площадь')):
        for m in re.finditer(name + rb'\x00\xed', data):
            v = struct.unpack('>d', data[m.end():m.end() + 8])[0]
            if 1e-9 < abs(v) < 1e12:
                o.write('  %-9s = %14.4f\n' % (key, v))
                got = True
                break
    return got

def cmd_dims(data, o):
    names = collections.Counter(m.group(1).decode()
                               for m in re.finditer(rb'([Dd]\d{1,4})(?![A-Za-z0-9])', data))
    o.write('РАЗМЕРЫ: имён dNNN = %d, записей nominal_value = %d\n'
            % (len(names), len(re.findall(rb'nominal_value', data))))
    for k, c in names.most_common(25):
        o.write('   %-10s ×%d\n' % (k, c))
    return bool(names)

def cmd_geom(data, o):
    tot = clean = nums = nice = 0
    for pos, body in payload_of(data, 'crv_pnt_arr'):
        if not (8 <= len(body) <= 200):
            continue
        tot += 1
        if len(body) % 4 == 0 and all(body[k + 1] in MARK3
                                       for k in range(0, len(body), 4)):
            clean += 1
        for k in range(len(body) - 2):
            if body[k] in MARK3:
                v = val3(body[k + 1], body[k + 2])
                nums += 1
                if 0.001 <= abs(v) <= 1e5 and abs(v * 4 - round(v * 4)) < 1e-9:
                    nice += 1
    o.write('ГЕОМЕТРИЯ: записей %d, чистых %d, координат %d, красивых %d\n'
            % (tot, clean, nums, nice))
    return tot > 0

def cmd_meta(data, o):
    f = collections.Counter(m.group(2).decode('ascii', 'replace')
                            for m in FIELD.finditer(data))
    o.write('МЕТАДАННЫЕ: полей уникальных = %d\n' % len(f))
    for k, c in f.most_common(15):
        o.write('   %-28s %d\n' % (k, c))
    return bool(f)

CMDS = {'--bom': cmd_bom, '--tree': cmd_tree, '--mass': cmd_mass,
        '--dims': cmd_dims, '--geom': cmd_geom, '--meta': cmd_meta}

def collect(path):
    if os.path.isdir(path):
        fs = []
        for ext in ('*.prt.1', '*.asm.1', '*.drw.1'):
            fs += glob.glob(os.path.join(path, '**', ext), recursive=True)
        return sorted(fs)
    return [path]

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    audit = '--audit' in args
    limit = 30
    if '--limit' in args:
        limit = int(args[args.index('--limit') + 1])
    flags = [a for a in args if a in CMDS]
    paths = [a for a in args if not a.startswith('--') and os.path.exists(a)]
    if not paths:
        print('нет файлов для обработки')
        return
    o = io.open('creo_read_out.txt', 'w', encoding='utf-8')
    if audit:
        files = []
        for p in paths:
            files += collect(p)
        files = files[:limit]
        stats = collections.Counter()
        for f in files:
            try:
                data = open(f, 'rb').read()
            except Exception:
                continue
            ok = []
            for flag, fn in CMDS.items():
                buf = io.StringIO()
                try:
                    if fn(data, buf):
                        ok.append(flag)
                except Exception:
                    pass
            for fl in ok:
                stats[fl] += 1
            o.write('%-44s %s\n' % (os.path.basename(f)[:44], ', '.join(ok) or '—'))
        o.write('\n=== ПОКРЫТИЕ ПО %d ФАЙЛАМ ===\n' % len(files))
        for fl in sorted(CMDS):
            c = stats[fl]
            o.write('  %-7s %5d = %5.1f %%\n' % (fl, c, 100.0 * c / max(1, len(files))))
    else:
        if not flags:
            flags = list(CMDS)
        for p in paths:
            data = open(p, 'rb').read()
            o.write('#' * 60 + '\n# %s (%d байт)\n' % (os.path.basename(p), len(data)))
            for fl in flags:
                o.write('\n--- %s ---\n' % fl)
                try:
                    if not CMDS[fl](data, o):
                        o.write('   (не найдено)\n')
                except Exception as e:
                    o.write('   ошибка: %s\n' % e)
    o.close()
    print('creo_read_out.txt')

if __name__ == '__main__':
    main()
                v = val3(body[k + 1], body[k + 2])
                nums += 1
                if 0.001 <= abs(v) <= 1e5 and abs(v * 4 - round(v * 4)) < 1e-9:
                    nice += 1
    o.write('ГЕОМЕТРИЯ: записей %d, чистых %d, координат %d, красивых %d\n'
            % (tot, clean, nums, nice))
    return tot > 0

def cmd_meta(data, o):
    f = collections.Counter(m.group(2).decode('ascii', 'replace')
                            for m in FIELD.finditer(data))
    o.write('МЕТАДАННЫЕ: полей уникальных = %d\n' % len(f))
    for k, c in f.most_common(15):
        o.write('   %-28s %d\n' % (k, c))
    return bool(f)

CMDS = {'--bom': cmd_bom, '--tree': cmd_tree, '--mass': cmd_mass,
        '--dims': cmd_dims, '--geom': cmd_geom, '--meta': cmd_meta}