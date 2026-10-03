# -*- coding: utf-8 -*-
"""FEATTYPE по имени: ищем feat_name и соседние числа.
Метод проверки: для признаков, где имя однозначно задаёт тип
(Отверстие=HOLE, Скругление=ROUND, Вытягивание/PROTRUSION, Вращение=REVOLVE),
должен повторяться ОДНО И ТО ЖЕ число. Так тип доказывается, а не угадывается.
Запуск: python ftbyName.py <файл>
Вывод: ftbyname_out.txt
"""
import re, sys, io, os, struct

def load(p):
    with open(p, 'rb') as f:
        return f.read()

NAME_FIELD = re.compile(rb'\xE0(.)(feat_name|feat_id|type|ftype|ft_type|feat_type|prev_feat_id|parent_feat_id|order|sort_key|name)\x00')

def nearby_numbers(chunk, span=48):
    """Положения и значения 1-4 байтовых целых рядом с полем."""
    out = []
    n = len(chunk)
    for i in range(n):
        for L in (1, 2, 4):
            if i + L > n:
                break
            v = int.from_bytes(chunk[i:i + L], 'big')
            if 0 < v < 400:
                out.append((i, L, v))
    return out

def main():
    path = sys.argv[1]
    data = load(path)
    out = io.open('ftbyname_out.txt', 'w', encoding='utf-8')
    out.write('FILE %s size=%d\n\n' % (os.path.basename(path), len(data)))

    recs = []
    for m in NAME_FIELD.finditer(data):
        if m.group(2) != b'feat_name':
            continue
        pos = m.end()
        tag = data[pos] if pos < len(data) else 0
        # значение: 0x0A/0xF1/0xF2 -> строка
        if tag in (0x0A, 0xF1, 0xF2):
            rest = data[pos + 1:pos + 1 + 80]
            z = rest.find(b'\x00')
            raw = rest[:z] if z >= 0 else rest
            try:
                nm = raw.decode('utf-8')
            except Exception:
                continue
            recs.append((m.start(), nm))

    out.write('feat_name найдено: %d\n' % len(recs))
    # группировка по ключевому слову
    KEYS = [('отверст', 'HOLE(1)'), ('HOLE', 'HOLE(1)'), ('скругл', 'ROUND(3)'),
            ('ROUND', 'ROUND(3)'), ('фаск', 'CHAMFER(4)'), ('CHAMFER', 'CHAMFER(4)'),
            ('вытягив', 'PROTRUSION(7)'), ('PROTRUSION', 'PROTRUSION(7)'),
            ('вращен', 'REVOLVE(?)'), ('массив', 'PATTERN(232)'), ('координ', 'COORD_SYS(68)')]
    stat = {}
    for pos, nm in recs:
        for k, label in KEYS:
            if k.lower() in nm.lower():
                lo = max(0, pos - 60)
                hi = min(len(data), pos + 160)
                nums = nearby_numbers(data[lo:hi])
                cnt = {}
                for i, L, v in nums:
                    if 0 < v < 290:
                        cnt.setdefault(v, 0)
                        cnt[v] += 1
                top = sorted(cnt.items(), key=lambda x: -x[1])[:6]
                stat.setdefault(label, []).append((nm, pos, top))
                break
    out.write('\n=== ЧАСТОТЫ ЧИСЕЛ РЯДОМ С ИМЕНЕМ (кандидаты на FEATTYPE) ===\n')
    for label, items in sorted(stat.items()):
        agg = {}
        for nm, pos, top in items:
            for v, c in top:
                agg.setdefault(v, 0)
                agg[v] += 1
        out.write('\n%s  (имён: %d)\n' % (label, len(items)))
        for v, c in sorted(agg.items(), key=lambda x: -x[1])[:10]:
            out.write('   число %-5d встречается у %d имён\n' % (v, c))
    out.write('\n=== ПРИМЕРЫ ===\n')
    for label, items in sorted(stat.items()):
        for nm, pos, top in items[:3]:
            out.write('%-22s %-28s абс.%d  числа: %s\n' % (label, nm[:28], pos, top))
    out.close()
    print('ftbyname_out.txt feat_names=%d' % len(recs))

if __name__ == '__main__':
    main()