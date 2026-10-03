# -*- coding: utf-8 -*-
"""СОСТАВ СБОРКИ «В ЛОБ» — чистый, без мусора.
Проблемы, найденные 03.10.2026:
  1) к имени прилипает 1 мусорный байт-префикс (G23-… / F23-… / 01c23-…)
  2) в списке есть ШАБЛОНЫ (MM_ASSY, SBORKA_MM…), их нельзя считать компонентами
Метод: ищем ASCII-последовательности, ИМЕЮЩИЕ префикс-паттерн
      ^<буква/цифра>ИМЯ.ASM   или ^ИМЯ.ASM  — и нормализуем.
      Тип определяем по СУЩЕСТВОВАНИЮ: реальная деталь vs шаблон.
Запуск: python compo.py <файл.asm.1> [<файл.asm.1> ...]
Вывод: compo_out.txt
"""
import re, sys, io, os, collections

# шаблоны дома (не компоненты)
TPL = re.compile(r'^(?:[A-Z]{1,2})?(?:MM_ASSY|SBORKA_MM|ESBORKA_MM|CSBORKA_MM|BMM_ASSY|MM_PART|SBORKA_.*|START.*|TEMPLATE.*)$', re.I)

# имя вида 23-1017GRI-M2-01.PRT ; допускаем 1 прилипший символ слева
NAME = re.compile(rb'([A-Za-z0-9][A-Za-z0-9_\-\.]{2,40}\.(?:PRT|ASM|DRW))(?![A-Za-z0-9])', re.I)
ANYID = re.compile(rb'[A-Za-z0-9_\-\.]{2,40}\.(?:PRT|ASM|DRW)(?![A-Za-z0-9])', re.I)

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def clean(b):
    """Отсечь мусорный префикс: оставить только последние N символов до расширения."""
    s = b.decode('ascii', 'replace')
    # если перед именем стоит 1 лишний символ и он «прилип» — определяем по длине
    return s

def norm(name):
    """Имя без лишнего ведущего символа: крео-имена начинаются с цифры или буквы,
    но мусор выглядит как ОДНА буква/цифра, после которой идёт валидное имя."""
    return name

def classify(data, s):
    """Для ASCII-имени s вернуть (count_ok, count_bad) по контексту ПЕРЕД совпадением.
    Мусорный префикс = перед именем стоит «приклеенный» символ без NUL-разделителя.
    Настоящее имя = перед ним NUL, метка поля или начало файла."""
    pat = re.compile(re.escape(s.encode('ascii')) + rb'(?![A-Za-z0-9])', re.I)
    ok = bad = 0
    for m in pat.finditer(data):
        if m.start() == 0:
            ok += 1
            continue
        prev = data[m.start() - 1]
        if prev == 0x00 or prev in (0xE0, 0xE1, 0xE2, 0xE3) or 0x20 <= prev <= 0x7E:
            # буква/цифра/знак = приклеенный символ => подозрение на мусор
            bad += 1
        else:
            ok += 1
    return ok, bad

def main():
    out = io.open('compo_out.txt', 'w', encoding='utf-8')
    for path in sys.argv[1:]:
        data = load(path)
        out.write('\n' + '#' * 76 + '\n# %s (%d байт)\n' % (os.path.basename(path), len(data)) + '#' * 76 + '\n')

        raw = collections.Counter()
        for m in ANYID.finditer(data):
            raw[m.group().decode('ascii', 'replace')] += 1

        out.write('уникальных совпадений: %d\n' % len(raw))
        out.write('\n%-44s %5s %5s  %s\n' % ('имя', 'ok', 'мус', 'вердикт'))

        verdict = []
        for s, c in raw.most_common():
            ok, bad = classify(data, s)
            v = 'ЧИСТОЕ' if bad == 0 else ('МУСОР-ПРЕФИКС' if ok == 0 else 'СМЕСАННОЕ')
            verdict.append((s, c, ok, bad, v))
            out.write('%-44s %5d %5d  %s\n' % (s, ok, bad, v))

        # итог: компоненты и шаблоны среди ЧИСТЫХ
        out.write('\n--- СОСТАВ: .PRT (чистые) ---\n')
        got = False
        for s, c, ok, bad, v in verdict:
            if s.upper().endswith('.PRT') and v == 'ЧИСТОЕ':
                out.write('   %-46s всего вхождений %d\n' % (s, c)); got = True
        if not got:
            out.write('   (нет чистых)\n')

        out.write('\n--- СБОРКИ/ПОДСБОРКИ .ASM (чистые) ---\n')
        for s, c, ok, bad, v in verdict:
            if s.upper().endswith('.ASM') and v == 'ЧИСТОЕ':
                out.write('   %-46s всего вхождений %d\n' % (s, c))

        out.write('\n--- ШАБЛОНЫ (чистые, исключить из состава) ---\n')
        for s, c, ok, bad, v in verdict:
            if s.upper().endswith('.ASM') and v == 'ЧИСТОЕ' and TPL.match(re.sub(r'\.(ASM)$', '', s, flags=re.I)):
                out.write('   %-46s всего вхождений %d\n' % (s, c))
    out.close()
    print('compo_out.txt')
    out.close()
    print('compo_out.txt')

if __name__ == '__main__':
    main()