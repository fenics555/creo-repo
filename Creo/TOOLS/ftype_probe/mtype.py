# -*- coding: utf-8 -*-
"""КАНДИДАТ В FEATTYPE: поле model_type рядом с id в блоках feat_defs_*.
Строгая проверка:
  1) значение model_type в каждом блоке (должно быть 1..279)
  2) повторяемость на 2+ моделях
  3) СОГЛАСОВАННОСТЬ: если модель — болт с отверстиями, у отверстий должен
     быть один тип, у других фич — другой. Ищем блоки с РАЗНЫМИ значениями.
  4) имена фич рядом (если есть) — сверяем со словарём pfcFEATTYPE.
Запуск: python mtype.py <файл> [файл2 ...]
"""
import re, sys, io, os, collections

FT = {}
_N = """FIRST HOLE SHAFT ROUND CHAMFER SLOT CUT PROTRUSION NECK FLANGE RIB EAR DOME
DATUM_PLANE LOC_PUSH UDF DATUM_AXIS DRAFT SHELL DOME2 CORNER_CHAMFER DATUM_POINT IMPORT
COSMETIC ETCH MERGE MOLD SAW TURN MILL DRILL OFFSET DATUM_SURFACE REPLACE_SURFACE GROOVE
PIPE DATUM_QUILT ASSEMBLY_CUT UDFTHREAD CURVE SURFACE_MODEL WALL BEND UNBEND"""
for i, n in enumerate(_N.split()):
    FT[i] = n
FT.update({232: 'PATTERN', 233: 'PATTERN_HEAD', 181: 'GROUP_HEAD', 89: 'COMPONENT',
           200: 'REFERENCE', 23: 'COSMETIC', 56: 'SET', 91: 'FIXTURE_SETUP',
           96: 'OPERATION', 235: 'ANNOTATION', 267: 'DERIVED_MEMBER'})

def ftname(v):
    return FT.get(v, '?%d' % v)

FIELD = re.compile(rb'([\xe0-\xff][\x00-\x0f])([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')
HEAD = re.compile(rb'\xF8.\xF7.\xFB\xE3\xE0\x01id\x00')
FEATDEF = re.compile(rb'feat_defs_([0-9]+)\x00')

def load(p):
    with open(p, 'rb') as f:
        return f.read()

def main():
    out = io.open('mtype_out.txt', 'w', encoding='utf-8')
    out.write('КАНДИДАТ: model_type в блоках feat_defs_*\n')
    out.write('Словарь pfcFEATTYPE: 0=H? 1=HOLE 2=SHAFT 3=ROUND 7=PROTRUSION '
              '13=DATUM_PLANE 16=DATUM_AXIS 232=PATTERN\n\n')
    grand = collections.Counter()
    for path in sys.argv[1:]:
        data = load(path)
        out.write('=' * 76 + '\n%s\n' % os.path.basename(path) + '=' * 76 + '\n')
        # все блоки: от заголовка до следующего заголовка
        heads = [m.start() for m in HEAD.finditer(data)]
        fdefs = [(m.start(), int(m.group(1))) for m in FEATDEF.finditer(data)]
        out.write('заголовков блоков: %d ;  маркеров feat_defs_N: %d\n' % (len(heads), len(fdefs)))
        found = []
        for p, num in fdefs:
            # ищем ближайший заголовок БЛИЖЕ К НАЧАЛУ файла, чем маркер
            h = None
            for hh in heads:
                if hh <= p + 40:
                    h = hh
                else:
                    break
            lo = h if h is not None else p
            chunk = data[lo:lo + 700]
            fs = [(m.start(), m.group(2).decode('ascii', 'replace'), m.end())
                  for m in FIELD.finditer(chunk)]
            vals = {}
            for k, (off, nm, e) in enumerate(fs):
                if nm in ('model_type', 'type', 'sub_type'):
                    tail = chunk[e:e + 8]
                    vals[nm] = (' '.join('%02X' % c for c in tail[:4]), tail[1] if len(tail) > 1 else None)
            # имя рядом
            nm = None
            for mm in re.finditer(rb'(?:feat_name|object_name|long_name)\x00(.)([A-Za-z0-9_\-\.]{2,40})\x00', chunk):
                nm = mm.group(2).decode('ascii', 'replace')
            found.append((p, num, vals, nm))
            out.write('  feat_defs_%-5d @%-9d model_type=%-14s type=%-14s имя=%s\n'
                      % (num, p,
                         vals.get('model_type', ('-',))[0],
                         vals.get('type', ('-',))[0],
                         nm))
            if vals.get('model_type', ('', None))[1]:
                grand[vals['model_type'][1]] += 1

    out.write('\n=== СВОДКА model_type ПО ВСЕМ МОДЕЛЯМ ===\n')
    for v, c in grand.most_common():
        out.write('   model_type=%-4d (%-22s) встречается %d раз\n' % (v, ftname(v), c))
    out.write('\n⚠️ КРИТЕРИЙ: значение должно 1) повторяться, 2) быть осмысленным '
              '(FEATTYPE), 3) различаться у РАЗНЫХ фич.\n')
    out.close()
    print('mtype_out.txt')

if __name__ == '__main__':
    main()