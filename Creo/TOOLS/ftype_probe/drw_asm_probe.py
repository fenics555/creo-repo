# -*- coding: utf-8 -*-
"""ВЫЕМКА ИЗ ЧЕРТЕЖЕЙ И СБОРОК (только чтение):
  1) внешние ссылки на модели (.prt/.asm/.drw) — это «состав»
  2) rel_model_name и другие отношения — долг №3 «Обозначение»
  3) секции из #UGC_TOC + частотность полей
Запуск: python drw_asm_probe.py <файл> [<файл2> ...]
Вывод: drw_asm_out.txt
"""
import re, sys, io, os, collections

# ПРАВИЛЬНАЯ регулярка расширений (в исходной идее была ошибка:
# [14A-Za-z][14A-Za-z][Mm] матчила мусор вроде "44M")
EXT = re.compile(rb'([A-Za-z0-9_\-\.]{2,40}\.(?:prt|asm|drw|PRT|ASM|DRW))(?![A-Za-z0-9])')
FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')
REL = re.compile(rb'(rel_[a-z_]+|[a-z_]*model_name|param[a-z_]*\.[a-z_]+)')

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def sections(data):
    out = []
    for m in re.finditer(rb'\n#([A-Za-z_][A-Za-z0-9_]{2,30})[\r\n]', data):
        out.append((m.end(), m.group(1).decode()))
    out.sort()
    return out

def sec_of(secs, pos):
    cur = '(начало)'
    for s, n in secs:
        if s <= pos:
            cur = n
        else:
            break
    return cur

def main():
    out = io.open('drw_asm_out.txt', 'w', encoding='utf-8')
    for path in sys.argv[1:]:
        data = load(path)
        secs = sections(data)
        out.write('\n' + '#' * 78 + '\n# %s  (%d байт)\n' % (os.path.basename(path), len(data)) + '#' * 78 + '\n')

        out.write('СЕКЦИИ (%d): %s\n\n' % (len(secs), ', '.join(n for _, n in secs)))

        # 1) внешние ссылки
        refs = collections.Counter(m.group(1).decode('ascii', 'replace') for m in EXT.finditer(data))
        out.write('=== 1. ВНЕШНИЕ ССЫЛКИ НА МОДЕЛИ: %d уникальных ===\n' % len(refs))
        for r, c in refs.most_common(40):
            out.write('   %-44s x%d\n' % (r, c))

        # 2) отношения
        rels = collections.Counter(m.group(1).decode('ascii', 'replace') for m in REL.finditer(data))
        out.write('\n=== 2. ОТНОШЕНИЯ/ПАРАМЕТРЫ: %d уникальных ===\n' % len(rels))
        for r, c in rels.most_common(30):
            out.write('   %-40s x%d\n' % (r, c))

        # 3) rel_model_name + контекст
        out.write('\n=== 3. rel_model_name — ПОИСК ===\n')
        pat = b'rel_model_name'
        n = data.count(pat)
        out.write('   вхождений: %d\n' % n)
        s = 0
        for k in range(min(n, 4)):
            i = data.find(pat, s)
            if i < 0:
                break
            s = i + 1
            lo, hi = max(0, i - 48), min(len(data), i + 96)
            ch = data[lo:hi]
            out.write('   @%d секция=%s\n' % (i, sec_of(secs, i)))
            out.write('     hex  : %s\n' % ' '.join('%02X' % c for c in ch))
            asc = ''.join(chr(c) if 32 <= c < 127 else '.' for c in ch)
            out.write('     ascii: %s\n' % asc)

        # 4) поля-схема
        out.write('\n=== 4. ЧАСТЫЕ ПОЛЯ (топ-25) ===\n')
        cnt = collections.Counter(m.group(2).decode('ascii', 'replace') for m in FIELD.finditer(data))
        for k, c in cnt.most_common(25):
            out.write('   %-34s %d\n' % (k, c))
    out.close()
    print('drw_asm_out.txt')

if __name__ == '__main__':
    main()