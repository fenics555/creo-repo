"""ЕДИНЫЙ ЧИТАТЕЛЬ ФИЧ .prt — то, что реально доказано (04.10.2026).

Читает: имена фич, feat_id (varint 1/2/3 байта), порядок построения.
Не читает (долг 7): числовой тип операции — см. _INDEX.md.

Использование:
    python creofeat.py <файл.prt.1>            кратко
    python creofeat.py <файл.prt.1> --audit    сколько фич найдено
"""
import sys, io
from collections import defaultdict


def dec(b, k):
    """varint: длина в двух старших битах первого байта."""
    b0 = b[k]
    tag = b0 & 0xC0
    if tag == 0xC0:
        return ((b0 & 0x3F) << 16) | (b[k+1] << 8) | b[k+2], 3
    if tag == 0x80:
        return ((b0 & 0x7F) << 8) | b[k+1], 2
    return b0, 1


def read_features(b):
    """Фичи в обеих формах записи.

    Форма A (ASCII-имена):  <имя>\\0 01 00 [18 E5] <varint id>
    Форма B (кириллица):    e3 <varint id> <байт> <имя>\\0
    """
    out = []
    i = 0
    n = len(b)

    # --- форма A ---
    while i < n - 8:
        if b[i + 1:i + 4] == b'\x00\x01\x00' and 32 <= b[i] < 127:
            j = i - 1
            k = j
            while k >= 0 and 32 <= b[k] < 127:
                k -= 1
            if k >= 0 and 1 <= (i - k) <= 60:
                name = b[k + 1:i + 1]
                p = i + 4
                if b[p:p + 2] == b'\x18\xe5':
                    p += 2
                try:
                    fid, w = dec(b, p)
                except IndexError:
                    i += 1
                    continue
                if 0 < fid < 2_000_000:
                    try:
                        nm = name.decode('utf-8')
                    except UnicodeDecodeError:
                        nm = name.decode('latin-1')
                    # тот же фильтр, что и в форме B: имя с буквы,
                    # иначе в вывод идёт мусор (`>=`, `ND_TABLE`, числа)
                    if nm and (nm[0].isalpha() or nm[0] == '_'):
                        out.append((fid, nm, i, 'A'))
        i += 1

    # --- форма B ---
    i = 0
    while i < n - 4:
        if b[i] == 0xE3:
            try:
                fid, w = dec(b, i + 1)
            except IndexError:
                i += 1
                continue
            p = i + 1 + w
            if 0 < fid < 2_000_000 and p < n:
                # после ID идёт байт, затем имя в UTF-8 до NUL
                st = p + 1
                nm = b''
                q = st
                while q < n and b[q] != 0 and q - st < 80:
                    nm += bytes([b[q]])
                    q += 1
                if 1 <= len(nm) <= 60 and q < n and b[q] == 0:
                    try:
                        s = nm.decode('utf-8')
                    except UnicodeDecodeError:
                        s = ''
                    # ⚠️ имя должно начинаться с БУКВЫ. Без этого в форму B
                    # попадает мусор: `>=`, `A_2`, числа — они не фичи.
                    # ⚠️ длину 1 НЕЛЬЗЯ отбрасывать: фичи «А», «Б», «В»
                    # (Поперечное сечение) иначе теряются полностью.
                    if s and s[0].isalpha() and all(
                            c.isalnum() or c in '._- АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'
                            for c in s):
                        out.append((fid, s, i, 'B'))
        i += 1
    return out


def read_order(b, ids_a=None):
    """Списки `f8 <N>` + N*varint(id) — кандидаты на порядок построения.

    ⚠️ Без отбора по эталону список выбрать нельзя: «самый длинный» и
    «возрастающие ID» дают ложные списки (проверено). Здесь отбор
    САМОПРОВЕРЯЮЩИЙСЯ: берём список, который содержит ≥3 ID, найденных
    формой A (она ложных срабатываний не даёт), и максимизируем пересечение.

    Возвращает (список_id, отфильтрованные_фичи).
    """
    cands = []
    i = 0
    n = len(b)
    while i < n - 2:
        if b[i] == 0xF8 and 2 <= b[i + 1] <= 200:
            cnt = b[i + 1]
            k = i + 2
            ids = []
            for _ in range(cnt):
                if k >= n - 3:
                    break
                try:
                    v, w = dec(b, k)
                except IndexError:
                    break
                if v == 0 or v > 2_000_000:
                    break
                ids.append(v)
                k += w
            if len(ids) == cnt and len(ids) >= 5:
                cands.append((i, ids))
        i += 1

    ids_a = ids_a or set()
    best = None
    for off, ids in cands:
        ov = len([x for x in ids if x in ids_a])
        if ov >= 3 and (best is None or ov > best[0]):
            best = (ov, off, ids)
    if best is None:
        return None, None
    return best[2], best[1]


def main():
    path = sys.argv[1]
    b = open(path, 'rb').read()
    feats = read_features(b)
    ids_a = set(f for f, _, _, form in feats if form == 'A')
    order, order_off = read_order(b, ids_a)

    print('файл: %s' % path)
    print('размер: %d б' % len(b))
    print('записей-кандидатов в фичи: %d (форма A: %d, форма B: %d)'
          % (len(feats), len(ids_a), len(feats) - len(ids_a)))

    # ⚠️ Фильтр по списку порядка НЕ включаем по умолчанию.
    # Проверено 04.10.2026: самопроверяющийся отбор (пересечение с формой A)
    # даёт верный список в 137 (73/73, мусор 0), но в 9112 и al-138
    # выбирает НЕВЕРНЫЙ список и роняет покрытие 99 % → 46 %.
    # Причина: в моделях с кириллическими именами форма A находит всего
    # 4–5 фич, и критерий пересечения становится шумным.
    # Надёжно — только сверка с эталоном CREOSON (feat_order.py).
    if '--clean' in sys.argv:
        if order:
            keep = set(order)
            before = len(feats)
            feats = [f for f in feats if f[0] in keep]
            print('фильтр по порядку @%07X: %d элементов, отброшено %d записей'
                  % (order_off, len(order), before - len(feats)))
        else:
            print('⚠️ список порядка не найден — фильтр НЕ применён')

    if '--audit' in sys.argv:
        return

    print('\n--- ФИЧИ (имя, ID) ---')
    seen = set()
    for fid, nm, off, _f in sorted(feats, key=lambda x: x[0]):
        if fid in seen:
            continue
        seen.add(fid)
        print('  id=%-8d %s' % (fid, nm))


if __name__ == '__main__':
    main()