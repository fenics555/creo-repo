# -*- coding: utf-8 -*-
"""Извлечение записей фич из FeatDefs: feat_defs_<N> блоки с полями и значениями.
Цель: найти числовой тип операции (FEATTYPE) рядом с именем/идентификатором фичи.
Запуск: python featdefs.py <файл> [макс_записей]
Вывод: featdefs_out.txt
"""
import re, sys, io, os

# FEATTYPE из pfcFeature.h
FEATTYPE = {}
_NAMES = """FIRST HOLE SHAFT ROUND CHAMFER SLOT CUT PROTRUSION NECK FLANGE RIB EAR DOME
DATUM_PLANE LOC_PUSH UDF DATUM_AXIS DRAFT SHELL DOME2 CORNER_CHAMFER DATUM_POINT IMPORT
COSMETIC ETCH MERGE MOLD SAW TURN MILL DRILL OFFSET DATUM_SURFACE REPLACE_SURFACE GROOVE
PIPE DATUM_QUILT ASSEMBLY_CUT UDFTHREAD CURVE SURFACE_MODEL WALL BEND UNBEND
SHEETMETAL_CUT FORM THICKEN BEND_BACK UDFNOTCH UDFPUNCH INTERNAL_UDF SPLIT_SURFACE GRAPH
SMMFGPUNCH SMMFGCUT FLATTEN SET VDA SMMFGFORM SHEETMETAL_PUNCH_POINT LIP MANUAL_MILL
MFGGATHER MFGTRIM MFGUSE_VOLUME CABLE_LOCATION CABLE_SEGMENT CABLE COORD_SYS CHANNEL
AREA_NIBBLE PATCH PLY CORE EXTRACT MFGREFINE SILHOUETTE_TRIM SPLIT EXTEND SOLIDIFY INTERSECT
ATTACH CROSS_SECTION UDFZONE UDFCLAMP DRILL_GROUP ISEGMENT CABLE_COSMETIC SPOOL COMPONENT
MFGMERGE FIXTURE_SETUP FLAT_PAT CONT_MAP EXP_RATIO RIP OPERATION WORKCELL CUT_MOTION
CUSTOMIZE DRV_TOOL_SKETCH DRV_TOOL_EDGE DRV_TOOL_CURVE DRV_TOOL_SURF MATERIAL_REMOVAL TORUS
PIPE_SET_START PIPE_POINT_TO_POINT PIPE_EXTEND PIPE_TRIM PIPE_FOLLOW PIPE_JOIN AUXILIARY
PIPE_LINE LINE_STOCK SOLID_PIPE BULK_OBJECT SHRINKAGE PIPE_JOINT PIPE_BRANCH
DRV_TOOL_TWO_CNTR SUB_HARNESS SHEETMETAL_OPTIMIZE DECLARE SHEETMETAL_POPULATE
OPERATION_COMPONENT MEASURE DRAFT_LINE"""
for _i, _n in enumerate(_NAMES.split()):
    FEATTYPE[_i] = _n

FT_EXTRA = {232: 'PATTERN', 233: 'PATTERN_HEAD', 181: 'GROUP_HEAD', 89: 'COMPONENT',
            200: 'REFERENCE', 23: 'COSMETIC', 56: 'SET', 91: 'FIXTURE_SETUP',
            96: 'OPERATION', 235: 'ANNOTATION', 267: 'DERIVED_MEMBER', 244: 'DESIGNATED_AREA'}
FEATTYPE.update(FT_EXTRA)

def ftname(v):
    if v is None:
        return ''
    return FEATTYPE.get(v, '?%d' % v)

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def sec_range(data, name):
    """(начало содержимого, длина) секции по точному маркеру."""
    m = re.search(rb'\n#' + name.encode() + rb'[\r\n]', data)
    if not m:
        return None
    start = m.end()
    # длина из оглавления #UGC_TOC
    toc = re.search(rb'#' + name.encode() + rb'\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)', data[:0x4000])
    ln = None
    if toc:
        ln = int(toc.group(2), 16)
    return start, (ln if ln else len(data) - start)

FIELD = re.compile(rb'([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')

def parse_block(chunk):
    """Разбор блока: [(имя_поля, отступ_значения_от_конца_имени, байты_значения)]"""
    res = []
    for m in FIELD.finditer(chunk):
        name = m.group(1).decode('ascii', 'replace')
        res.append((name, m.end(), chunk[m.end():m.end() + 8]))
    return res

def main():
    path = sys.argv[1]
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    data = load(path)
    out = io.open('featdefs_out.txt', 'w', encoding='utf-8')
    out.write('FILE %s size=%d\n' % (os.path.basename(path), len(data)))

    rng = sec_range(data, 'FeatDefs')
    if not rng:
        out.write('секции FeatDefs нет\n')
        out.close()
        return
    start, ln = rng
    out.write('FeatDefs: абс.%d длина=%d\n\n' % (start, ln))

    base = data.find(b'Sld_FeatDefs')
    out.write('Sld_FeatDefs абс.%d\n\n' % base)
    n = 0
    s = 0
    while n < mx:
        i = data.find(b'feat_defs_', base + s)
        if i < 0 or i > start + ln + 4096:
            break
        s = i + 10
        # вверх до метки записи
        lo = max(0, i - 24)
        chunk = data[lo:i + 260]
        out.write('=== #%d абс.%d ===\n' % (n + 1, i))
        for off in range(0, len(chunk), 16):
            part = chunk[off:off + 16]
            out.write('%08X  %s\n' % (lo + off, ' '.join('%02X' % c for c in part)))
        fs = parse_block(chunk)
        out.write('поля: ' + ', '.join('%s:%s' % (f[0], ' '.join('%02X' % b for b in f[2])) for f in fs) + '\n')
        # число после id
        for k, (nm, e, val) in enumerate(fs):
            if nm == 'id' and k + 1 < len(fs):
                pass
        out.write('\n')
        n += 1
    out.write('записей показано %d\n' % n)
    out.close()
    print('featdefs_out.txt, records=%d' % n)

if __name__ == '__main__':
    main()