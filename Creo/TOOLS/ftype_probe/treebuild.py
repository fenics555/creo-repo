# -*- coding: utf-8 -*-
"""ДЕРЕВО ПОСТРОЕНИЯ «В ЛОБ» — восстановление по записям MdlStatus.
Запись фичи в файле (подтверждено байтами):
   <ID:2> | E0 01 "comp_type" 00 NN | E0 01 "prev_feat_id" 00 MM
         | E0 0A "feat_name" 00 "ИМЯ" 00 | E0 01 "pat_group_header_id" 00 …
Связь «родитель → ребёнок» = prev_feat_id.
Запуск: python treebuild.py <файл.prt.1>
Вывод: treebuild_out.txt
"""
import re, sys, io, os, collections

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def cyr(b):
    try:
        return b.decode('utf-8')
    except Exception:
        return b.decode('cp1251', 'replace')

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('treebuild_out.txt', 'w', encoding='utf-8')

    # 1) собрать все поля с позициями
    fields = [(m.start(), m.group(1)[0], m.group(2).decode('ascii', 'replace'), m.end())
              for m in FIELD.finditer(data)]
    out.write('ФАЙЛ %s (%d байт), полей %d\n\n' % (os.path.basename(path), len(data), len(fields)))

    # 2) ИМЕНА ФИЧ: маркер перед именем ВАРЬИРУЕТСЯ (E2, E3, F7 29 E2, F1…),
    #    поэтому ищем САМУ строку «Слово N» в UTF-8 — без требования к маркеру.
    # 1-й символ кириллицы = 2 байта (D0/D1 + 80-BF), далее буквы по 2 байта,
# затем пробел и номер. Маркер перед именем НЕ требуем (варьируется: E2/E3/F7 29 E2).
# 2) ИМЕНА ФИЧ. 1-й символ кириллицы = 2 байта (D0/D1 + 80-BF), далее буквы
    #    по 2 байта, затем пробел и номер. Маркер перед именем НЕ требуем:
    #    он варьируется (E2, E3, F7 29 E2, F1).
    namepat = re.compile(
        rb'([\xd0-\xd1][\x80-\xbf]'
        rb'(?:[\xd0-\xef][\x80-\xbf]){1,10}'
        rb'\x20'
        rb'[\x30-\x39]{1,3})'
        rb'\x00')
    feats = []
    for m in namepat.finditer(data):
        name = cyr(m.group(1))
        if not re.match(r'^[А-ЯЁ]', name):
            continue
        pos = m.start()
        fid = None
        win = data[pos:pos + 72]
        for k in range(1, min(len(win) - 2, 48)):
            if win[k] in (0x83, 0x84, 0x85, 0x86, 0x87) and win[k + 1] > 0x20:
                cand = (win[k] << 8) | win[k + 1]
                if 0x8000 <= cand <= 0x8FFF:
                    fid = cand
                    break
        feats.append((fid, None, name, None, pos))

    # 3) добавляем связи из записей с prev_feat_id (если есть)
    prevmap = {}
    for m in re.finditer(rb'prev_feat_id\x00(.)(.)', data):
        v0, v1 = m.group(1)[0], m.group(2)[0]
        if v0 == 0x00 and v1 > 0x20:
            prevmap[m.start()] = (v1 << 8) | data[m.end() + 1][0]

    out.write('НАЙДЕНО имён фич: %d\n\n' % len(feats))
    out.write('%-8s %-30s\n' % ('ID', 'имя'))
    for fid, prev, name, ctype, pos in feats:
        out.write('%-8s %-30s\n' % (('0x%04X' % fid) if fid else '-', name[:30]))

    out.write('\n=== РАСПРЕДЕЛЕНИЕ ПО ТИПАМ ОПЕРАЦИЙ ===\n')
    kinds = collections.Counter()
    for fid, prev, name, ctype, pos in feats:
        kinds[name.split()[0] if name.split() else name] += 1
    for k, c in kinds.most_common():
        out.write('   %-22s %d\n' % (k[:22], c))

    out.write('\n=== ЗАПИСИ С prev_feat_id ===\n')
    for p, v in sorted(prevmap.items()):
        out.write('   @%d prev=0x%04X\n' % (p, v))
    out.close()
    print('treebuild_out.txt feats=%d' % len(feats))

if __name__ == '__main__':
    main()