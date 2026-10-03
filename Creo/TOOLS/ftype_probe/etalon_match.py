# -*- coding: utf-8 -*-
"""ПРИЁМНИК ЭКСПОРТА ДЕРЕВА: сверяет список фич из Creo с байтами модели.
Запуск:
    python etalon_match.py <экспорт.txt> <модель.prt.1> [модель2 ...]
Что делает:
  1) парсит экспорт: имя фичи + feat_id (+ что ещё есть)
  2) ищет каждое имя в байтах и снимает окно ±48 байт
  3) извлекает значение ft_type рядом с именем, если поле есть
  4) сводит: ТИП ОПЕРАЦИИ -> значение ft_type (константа? разное?)
  5) проверяет feat_id из экспорта против 2-байтовых ID в файле
Вывод: etalon_out.txt
"""
import re, sys, io, os, collections

CYR = re.compile(r'[А-ЯЁ][а-яё]+')
LAT = re.compile(r'[A-Z][a-z]+')

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def parse_export(path):
    """[(имя_фичи, feat_id_если_есть, строка)] — максимально терпимо к формату."""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        txt = f.read()
    rows = []
    for line in txt.splitlines():
        s = line.strip()
        if not s:
            continue
        names = CYR.findall(s) or LAT.findall(s)
        # имя фичи = последнее слово с номером, напр. "Вытягивание 12"
        m = re.search(r'([A-Za-zА-Яа-яЁё]+)\s*(\d+)', s)
        nm = None
        if m:
            nm = '%s %s' % (m.group(1), m.group(2))
        fid = re.search(r'\b(?:id|ID|feat_id)\s*[=:]\s*(\d+)', s)
        rows.append((nm, int(fid.group(1)) if fid else None, s))
    return rows

def find_name_bytes(data, nm):
    pat = nm.encode('utf-8')
    out = []
    s = 0
    while True:
        i = data.find(pat, s)
        if i < 0:
            break
        out.append(i)
        s = i + 1
    return out

def extract_ft_type(data, pos, radius=48):
    """Ищем 'ft_type\\x00' рядом и берём значение после '\\x00'."""
    lo = max(0, pos - radius)
    hi = min(len(data), pos + radius)
    for m in re.finditer(rb'ft_type\x00(.)', data[lo:hi]):
        v = m.group(1)[0]
        return v, lo + m.start()
    return None, None

def main():
    if len(sys.argv) < 3:
        print('нужно: <экспорт.txt> <модель> [...]')
        return
    exp = sys.argv[1]
    models = sys.argv[2:]
    rows = parse_export(exp)
    out = io.open('etalon_out.txt', 'w', encoding='utf-8')
    out.write('ЭКСПОРТ: %s\nстрок разобрано: %d\n' % (exp, len(rows)))
    out.write('из них с распознанным именем фичи: %d\n\n'
              % sum(1 for r in rows if r[0]))

    out.write('--- ПРИМЕРЫ СТРОК ЭКСПОРТА ---\n')
    for nm, fid, s in rows[:25]:
        out.write('   имя=%-22s id=%-8s | %s\n' % (nm, fid, s[:90]))
    out.write('\n')

    for mp in models:
        data = load(mp)
        out.write('=' * 78 + '\nМОДЕЛЬ: %s (%d байт)\n' % (os.path.basename(mp), len(data)) + '=' * 78 + '\n')
        typemap = collections.defaultdict(collections.Counter)
        idcheck = collections.Counter()
        shown = 0
        for nm, fid, s in rows:
            if not nm:
                continue
            poss = find_name_bytes(data, nm)
            if not poss:
                continue
            base = re.match(r'([A-Za-zА-Яа-яЁё]+)', nm).group(1)
            for p in poss[:3]:
                v, vp = extract_ft_type(data, p)
                if v is not None:
                    typemap[base][v] += 1
                    if shown < 30:
                        out.write('  %-22s @%-9d ft_type=%-4d (позиция %d)\n' % (nm, p, v, vp))
                        shown += 1
            # проверка feat_id: BE и LE
            if fid is not None:
                for lbl, b in (('BE', fid.to_bytes(2, 'big')),
                               ('LE', fid.to_bytes(2, 'little'))):
                    if b in data:
                        idcheck[lbl] += 1

        out.write('\n--- СВОДКА: ТИП ОПЕРАЦИИ -> ft_type ---\n')
        if typemap:
            for t in sorted(typemap):
                vals = typemap[t]
                mark = ' ✅ КОНСТАНТА' if len(vals) == 1 else ' ⚠️ РАЗНЫЕ'
                out.write('  %-18s %s  %s\n'
                          % (t, dict(vals), mark))
            out.write('\n  >>> ЕСЛИ у каждого типа одно значение -> это и есть FEATTYPE.\n')
            out.write('  >>> Сверяем со словарём pfcFEATTYPE (см. feattype_dict.txt).\n')
        else:
            out.write('  ft_type НЕ НАЙДЕН рядом с именами (поле редкое).\n')

        out.write('\n--- ПРОВЕРКА feat_id ИЗ ЭКСПОРТА (2 байта) ---\n')
        out.write('  BE найдено: %d | LE найдено: %d  из %d фич с id\n'
                  % (idcheck['BE'], idcheck['LE'], sum(1 for r in rows if r[1])))
        out.write('  (если оба числа 0 -> feat_id из экспорта не пишется в файл как есть)\n')
    out.close()
    print('etalon_out.txt')

if __name__ == '__main__':
    main()