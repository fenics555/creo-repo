# -*- coding: utf-8 -*-
"""Проверка регулярки источника B на конкретном файле (read-only).
Запуск: python jrn_test.py <файл.asm.1>
"""
import re, sys

data = open(sys.argv[1], 'rb').read()
print('размер файла:', len(data))

# ищем кириллическое слово «Компонент»
for word, tag in [('Компонент', 'Компонент'), ('Чертеж', 'Чертеж'), ('Деталь', 'Деталь')]:
    p = tag.encode('utf-8')
    print('%-12s вхождений: %d' % (tag, data.count(p)))

p = 'Компонент'.encode('utf-8')
i = data.find(p)
print('\nпервое «Компонент» @%s' % (i if i >= 0 else 'нет'))
if i >= 0:
    seg = data[i:i + 80]
    print('hex  :', ' '.join('%02X' % c for c in seg))
    print('ascii:', ''.join(chr(c) if 32 <= c < 127 else '.' for c in seg))
    try:
        print('utf-8:', seg.decode('utf-8', 'replace'))
    except Exception as e:
        print('ошибка декодирования:', e)

# сколько .PRT и как они выглядят в этом файле
PRT = re.compile(rb'([A-Za-z0-9][A-Za-z0-9_\-\.]{1,40}\.PRT)(?![A-Za-z0-9])', re.I)
hits = PRT.findall(data)
print('\n.PRT вхождений: %d, уникальных: %d' % (len(hits), len(set(hits))))
for h in list(set(hits))[:8]:
    print('   ', h.decode('ascii', 'replace'))