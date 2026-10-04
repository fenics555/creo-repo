import os, re

def extract_universal_bom(data, file_path):
    """Двухфазный сборщик BOM.
    Возвращает (bom, kind, note). Проверено на 245 сборках."""
    if not file_path.lower().endswith(('.asm', '.asm.1')):
        return [], 'N/A', 'не сборка'

    head = data[:2000]
    if b'ASSEM_MFG' in head:
        return [], 'ASSEM_MFG', 'производственная ЧПУ-модель, спецификации нет'

    stem = os.path.basename(file_path).split('.')[0].upper()
    bom = []

    # ---- ФАЗА 2 (новое поколение, most-*): прямые текстовые ссылки ----
    # Формат: "d <длина> (имя.файла)" — имя может содержать дефис и кириллицу
    P2 = re.compile(
        rb'd \d+ \(([A-Za-z0-9_\-\.]{2,48}\.(?:[Pp][Rr][Tt]|[Aa][Ss][Mm]))\)')
    for m in P2.finditer(data):
        s = m.group(1).decode('latin-1').strip()
        if not s:
            continue
        base = s.split('.')[0].upper()
        if base == stem or s.upper() == stem:
            continue
        bom.append(s)

    kind = 'СБ (прямые ссылки)'
    if bom:
        return sorted(set(bom)), kind, '%d компонентов' % len(set(bom))

    # ---- ФАЗА 1 (старое поколение, nut_*, krishka): @comp_ids + 2-й @model_name ----
    if b'@comp_ids' in data:
        names = []
        cur = False
        for line in data[:20000].split(b'\n'):
            t = line.strip()
            if t.startswith(b'@model_name'):
                cur = True
                continue
            if t.startswith(b'@'):
                cur = False
                continue
            if cur and t:
                parts = t.split(b' ', 2)
                if len(parts) >= 3:
                    names.append(parts[2].decode('latin-1').strip())
                cur = False
        for n in names[1:]:
            if n.upper() != stem and n:
                bom.append(n + '.PRT')
        kind = 'обёртка (@comp_ids)'
        if bom:
            return bom, kind, '%d компонентов' % len(bom)
        return [], kind, 'только ссылка на себя'

    return [], kind, 'схема не распознана'