# -*- coding: utf-8 -*-
"""СОСТАВ СБОРКИ — два источника, coverage-мерка на реальной базе (read-only).
  Источник A: записи компонентов  E0 01 "comp_type" 00 02 … E0 0A "feat_name" 00 "<ИМЯ>.PRT"
  Источник B: текстовые записи журнала  "Компонент id NN (<ИМЯ>.PRT)"
Цель: измерить, сколько сборок закрывается одним и двумя источниками.
Запуск: python compo2.py [папка] [N]
Вывод: compo2_out.txt
"""
import re, sys, io, os, random, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')
# A: имя .PRT рядом с comp_type=02 в окне 200 байт
PRT = re.compile(rb'([A-Za-z0-9][A-Za-z0-9_\-\.]{1,40}\.PRT)(?![A-Za-z0-9])', re.I)
# B: запись вида  "id 120 (ИМЯ.PRT)"  — слово перед "id" может быть ЛЮБЫМ
#     (проверено: в файлах, где comp_type молчит, это НЕ «Компонент»).
#     Надёжный признак: ".PRT)" сразу после имени, в скобках.
JRN = re.compile(rb'\x20\x69\x64\x20[\x30-\x39]{1,5}\x20\x28'
                 rb'([A-Za-z0-9][A-Za-z0-9_\-\.]{1,40}\.PRT)\x29')

def sample(base, n):
    allf = []
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.lower().endswith('.asm.1'):
                allf.append(os.path.join(root, f))
        if len(allf) > 40000:
            break
    random.seed(7)
    random.shuffle(allf)
    return allf[:n]

def parts_source_a(data):
    """comp_type=02 + ближайшее имя .PRT в пределах 220 байт после."""
    out = set()
    for m in re.finditer(rb'comp_type\x00\x02', data):
        win = data[m.end():m.end() + 220]
        p = PRT.search(win)
        if p:
            out.add(p.group(1).upper().decode('ascii', 'replace'))
    return out

def parts_source_b(data):
    return {m.group(1).upper().decode('ascii', 'replace') for m in JRN.finditer(data)}

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else r'Z:\PTC\Work'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    files = sample(base, n)
    out = io.open('compo2_out.txt', 'w', encoding='utf-8')
    out.write('СОСТАВ СБОРКИ · два источника · папка %s · файлов %d\n\n' % (base, len(files)))

    a_only = b_only = both = neither = 0
    tot_parts = 0
    rows = []
    for f in files:
        try:
            data = open(f, 'rb').read()
        except Exception:
            continue
        A = parts_source_a(data)
        B = parts_source_b(data)
        if A and not B:
            a_only += 1
        elif B and not A:
            b_only += 1
        elif A and B:
            both += 1
        else:
            neither += 1
        if A or B:
            tot_parts += len(A | B)
        rows.append((os.path.basename(f), len(A), len(B), len(A | B)))

    t = len(rows)
    out.write('--- РАЗБИВКА ПО ИСТОЧНИКАМ (из %d файлов) ---\n' % t)
    out.write('  только A (comp_type):   %d\n' % a_only)
    out.write('  только B (журнал):      %d\n' % b_only)
    out.write('  оба источника:          %d\n' % both)
    out.write('  НИ ОДНОГО (нет ссылок на детали): %d\n' % neither)
    out.write('\n  >>> Покрытие только A:  %.1f %% файлов\n' % (100.0 * (a_only + both) / max(1, t)))
    out.write('  >>> Покрытие A+B:      %.1f %% файлов\n'
              % (100.0 * (a_only + b_only + both) / max(1, t)))
    out.write('  >>> Покрытие среди тех, где есть хоть одна деталь: %.1f %%\n'
              % (100.0 * (a_only + b_only + both) / max(1, t - neither)))
    out.write('\n  всего уникальных деталей во всех сборках: %d\n' % tot_parts)

    out.write('\n--- ПРИМЕРЫ (файл | A | B | A∪B) ---\n')
    for nm, a, b, u in rows[:20]:
        out.write('  %-46s %4d %4d %4d\n' % (nm[:46], a, b, u))
    out.close()
    print('compo2_out.txt A=%d B=%d both=%d none=%d' % (a_only, b_only, both, neither))

if __name__ == '__main__':
    main()