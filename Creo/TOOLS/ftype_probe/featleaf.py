# -*- coding: utf-8 -*-
"""ПОСЛЕДНИЙ ОФЛАЙН-ШАГ: записи конкретных ФИЧ и поиск FEATTYPE рядом.
Фичи = листья дерева: «Вытягивание 1», «Отверстие 2», «Эскиз 1», «Скругление 3».
Критерий (владелец): если рядом с именем фичи есть число 1..279, различающееся
у РАЗНЫХ типов фич — это FEATTYPE. Сверяем на 2 моделях.
Запуск: python featleaf.py <файл> [файл2]
"""
import re, sys, io, os, collections

# кириллические названия операций
OP = re.compile(r'([А-ЯЁ][а-яё]+(?:\s+\d+)?)')
OPBY = re.compile(rb'([\xd0-\xd1][\x80-\xbf](?:[\xd0-\xd1][\x80-\xbf]|\s20|\x20)+?\x20?\d{1,3})')

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    out = io.open('featleaf_out.txt', 'w', encoding='utf-8')
    summary = {}
    for path in sys.argv[1:]:
        data = load(path)
        out.write('\n' + '#' * 76 + '\n# %s (%d байт)\n' % (os.path.basename(path), len(data)) + '#' * 76 + '\n')

        # находим UTF-8 кириллические имена вида «Слово N»
        found = []
        for m in re.finditer(rb'[\xd0-\xd1][\x80-\xbf](?:[\xd0-\xef][\x80-\xbf]|\x20|\xd0[\x80-\xbf]){1,30}', data):
            seg = m.group()
            try:
                s = seg.decode('utf-8')
            except Exception:
                continue
            # ГРАБЛЯ: фильтр «цифра или окончание -ая/-ое/-ие» отбрасывал
            # «Вытягивание» (окончание -ие есть, но без цифры). Нужен простой
            # критерий: кириллица длиной >= 4.
            if len(s) >= 4 and re.search(r'[А-Яа-яЁё]{4,}', s):
                found.append((m.start(), s, len(seg)))

        # группируем по «слово N»
        leaves = {}
        for pos, s, ln in found:
            mm = re.match(r'(.+?)\s*(\d*)$', s)
            base, num = mm.group(1), mm.group(2)
            if len(base) < 4:
                continue
            leaves.setdefault(base, []).append((pos, num))
        out.write('\nкириллических имён-кандидатов: %d записей, %d уникальных основ\n'
                  % (len(found), len(leaves)))
        for base in sorted(leaves, key=lambda b: -len(leaves[b]))[:25]:
            items = leaves[base]
            out.write('  %-22s x%-3d  позиции: %s\n'
                      % (base[:22], len(items), [p for p, _ in items[:6]]))
            summary.setdefault(os.path.basename(path), {}).setdefault(base, [p for p, _ in items])

        # для 4 самых частых оснований — байты вокруг первой позиции
        out.write('\n--- БАЙТЫ ВОКРУГ ИМЁН ФИЧ (по 4 самым частым) ---\n')
        for base in sorted(leaves, key=lambda b: -len(leaves[b]))[:4]:
            pos, num = leaves[base][0]
            lo = max(0, pos - 96)
            chunk = data[lo:pos + 96]
            out.write('\n  %s (N=%s) @%d:\n' % (base, num, pos))
            for off in range(0, len(chunk), 16):
                part = chunk[off:off + 16]
                asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in part)
                out.write('    %08X  %s  %s\n'
                          % (lo + off, ' '.join('%02X' % c for c in part), asc))
            # числа 1..279 в окне ±40
            nums = []
            for k in range(max(0, pos - 40), min(len(data) - 1, pos + 40)):
                if 1 <= data[k + 1] <= 279 and data[k] in (0xE0, 0xE1, 0xE2, 0xE3, 0xF1, 0xF2):
                    nums.append('%+d:%d' % (k - pos, data[k + 1]))
            out.write('    числа 1..279 в окне ±40: %s\n' % (', '.join(nums) or 'НЕТ'))
    out.close()
    print('featleaf_out.txt')

if __name__ == '__main__':
    main()