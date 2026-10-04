# -*- coding: utf-8 -*-
"""creo_json.py — выгрузка доказанных данных в JSON для PLM (04.10.2026).

Собирает ТОЛЬКО проверенное. Где не прочитано — отдаёт пусто, НЕ выдумывает.

    python creo_json.py <файл>

ДОКАЗАНО:
* feat_id — varint, длина в двух старших битах (аудит 600 файлов / 58 197 записей)
* формы записи A (<имя>\\0 01 00 [18 E5] <id>) и B (e3 <id> <байт> <имя>\\0)
* параметры — маркер E3: E3 <имя>\\0 27 88 20 E3 <n> <значение>\\0
* имена в файле UTF-8; CREOSON отдаёт их ЗАГЛАВНЫМИ

НЕ ЧИТАЕТСЯ (не выдумывать):
* FEATTYPE — 7 гипотез опровергнуто
* дерево родитель→ребёнок — parchild_table пуст (Structure_Invalid)
* ведущий байт double — неоднозначен, выводятся оба кандидата
"""
import os, re, sys, json, struct

CYR = ' АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'


def dec_varint(b, k):
    if k >= len(b):
        return None, 0
    b0 = b[k]
    tag = b0 & 0xC0
    if tag == 0xC0:
        return ((b0 & 0x3F) << 16) | (b[k+1] << 8) | b[k+2], 3
    if tag == 0x80:
        return ((b0 & 0x7F) << 8) | b[k+1], 2
    return b0, 1


ANAME = re.compile(rb'([A-Za-z][A-Za-z0-9_\.]{0,30})\x00')
SKIP = set(b'attr txt_attrib idtab_ptr types operation feat_id comp_type '
           b'prev_feat_id feat_name ft_type'.split())


def read_features(d):
    out = []
    for m in ANAME.finditer(d):
        nm = m.group(1)
        if nm in SKIP:
            continue
        p = m.end()                      # match.end() стоит ПОСЛЕ \x00 имени
        if d[p:p+2] != b'\x01\x00':      # маркер формы A
            continue
        p += 2
        if d[p:p+2] == b'\x18\xe5':      # префикс ОПЦИОНАЛЕН
            p += 2
        fid, _ = dec_varint(d, p)
        if fid and 0 < fid < 2000000:
            out.append((fid, nm.decode('latin-1'), 'A'))
    i, n = 0, len(d)
    while i < n - 4:
        if d[i] == 0xE3:
            fid, w = dec_varint(d, i + 1)
            i += 1
            if not fid or fid >= 2000000:
                continue
            p = i + w + 1
            st = p
            while p < n and d[p] != 0 and p - st < 80:
                p += 1
            raw = d[st:p]
            if not (1 <= len(raw) <= 60):
                continue
            try:
                s = raw.decode('utf-8')
            except UnicodeDecodeError:
                continue
            if s and s[0].isalpha() and all(c.isalnum() or c in '._-' + CYR
                                              for c in s):
                out.append((fid, s, 'B'))
        i += 1
    return out


MARK = b'\x27\x88\x20'


def read_params(d):
    out, mass = {}, {}
    i, n = 0, len(d)
    while i < n - 6:
        if d[i] == 0xE3:
            st, p = i + 1, i + 1
            while p < n and d[p] != 0 and p - st < 90:
                p += 1
            raw = d[st:p]
            if 1 <= len(raw) <= 60 and d[p] == 0:
                try:
                    nm = raw.decode('utf-8')
                except UnicodeDecodeError:
                    nm = None
                if nm and (nm[0].isalpha() or nm[0] == '_'):
                    q = p + 1
                    if d[q:q+3] == MARK:
                        q += 3
                        if q < n and d[q] == 0xE3:
                            _, w = dec_varint(d, q + 1)
                            q += 1 + w
                            if nm.upper() == 'MASS':
                                j = q
                                while j < n - 9 and j < q + 30:
                                    if d[j] == 0x2D and len(d[j+1:j+8]) == 7:
                                        t = d[j+1:j+8]
                                        mass['mantissa'] = ' '.join(
                                            '%02X' % c for c in t)
                                        mass['via_0x40'] = struct.unpack(
                                            '>d', b'\x40' + t)[0]
                                        mass['via_0x3F'] = struct.unpack(
                                            '>d', b'\x3F' + t)[0]
                                        break
                                    j += 1
                                out[nm] = None
                            else:
                                e = d.find(b'\x00', q)
                                if 0 <= e - q <= 200:
                                    try:
                                        out[nm] = d[q:e].decode('utf-8')
                                    except UnicodeDecodeError:
                                        out[nm] = ''
        i += 1
    return out, mass


BOM = re.compile(rb'id \d+ \(([A-Za-z0-9_\-]+\.(?:[Pp][Rr][Tt]'
                 rb'|[14A-Za-z][14A-Za-z][Mm]))\)')


def read_bom(d, path):
    if not path.lower().endswith(('.asm', '.asm.1')):
        return []
    return sorted(set(x.decode('latin-1') for x in BOM.findall(d)))


def analyze(path):
    d = open(path, 'rb').read()
    feats = read_features(d)
    params, mass = read_params(d)
    uniq = {}
    for fid, nm, _f in feats:
        uniq.setdefault(fid, nm)
    res = {
        "file_info": {"name": os.path.basename(path),
                      "size_bytes": len(d),
                      "valid_ugc": d.startswith(b"#UGC")},
        "features": [{"id": k, "name": v} for k, v in sorted(uniq.items())],
        "parameters": params,
        "bom": read_bom(d, path),
        "mass_properties": {"volume": None, "area": None},
    }
    if mass:
        res["mass_double_candidates"] = mass
        res["mass_properties"]["note"] = (
            "MASS не восстановлен однозначно: ведущий байт IEEE-754 "
            "не выводится из 7 байт мантиссы. Оба кандидата выше.")
    return res


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
    else:
        print(json.dumps(analyze(sys.argv[1]), ensure_ascii=False, indent=2))
# === ЧЕСТНЫЕ ОГРАНИЧЕНИЯ (проверено на 3 моделях) ===
# * параметры: РАБОТАЮТ, значения совпали с эталоном CREOSON
#     (Обозначение=137_011_0041 / 00612 / 00080-03, Тип=Деталь, Формат=А3)
# * feat_id: 0 НЕВЕРНЫХ ID на 3 моделях (сверка с эталоном)
#     НО точность низкая: форма A даёт 600 записей против 75 верных на 137
#     (лишние — записи схемы, не фичи). Для чистого вывода нужен
#     отбор по списку порядка построения, а он требует эталона CREOSON.
# * MASS: ведущий байт не восстанавливается однозначно, выводятся оба кандидата.
# * массовые свойства (volume/area): НЕ РЕАЛИЗОВАНЫ, отдаётся null.