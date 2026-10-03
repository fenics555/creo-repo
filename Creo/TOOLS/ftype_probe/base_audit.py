# -*- coding: utf-8 -*-
"""АВТО-АУДИТ вскрытых механизмов на боевой базе (СТРОГО ТОЛЬКО ЧТЕНИЕ).
Ничего не пишет на Z:. Ничего не запускает в Creo.
Цель: заменить «цифры из памяти прошлых сессий» на измеренные факты.
Запуск: python base_audit.py <папка> <ext> [N]
   напр. python base_audit.py Z:\PTC\Work prt 60
Вывод: base_audit_out.txt
"""
import os, re, sys, io, random, collections, struct

FIELD = re.compile(rb'\xE0(.)([A-Za-z][A-Za-z0-9_/\.\-]{1,60})\x00')
NAMEPAT = re.compile(rb'([\xd0-\xd1][\x80-\xbf](?:[\xd0-\xef][\x80-\xbf]){1,10}'
                     rb'\x20[\x30-\x39]{1,3})\x00')
EXTS = re.compile(rb'([A-Za-z0-9][A-Za-z0-9_\-\.]{2,40}\.(?:PRT|ASM|DRW))(?![A-Za-z0-9])')

def sample(base, ext, n):
    want = ('.' + ext + '.1')
    allf = []
    for root, dirs, files in os.walk(base):
        for f in files:
            lf = f.lower()
            if lf.endswith(want) or lf.endswith('.' + ext):
                allf.append(os.path.join(root, f))
        if len(allf) > 20000:
            break
    random.seed(42)                       # воспроизводимая выборка
    random.shuffle(allf)
    return allf[:n], len(allf)

def be(b):
    try:
        return struct.unpack('>d', b)[0]
    except Exception:
        return None

def audit(path, ext):
    r = {'name': os.path.basename(path), 'size': 0, 'ugc': False,
         'fields': 0, 'feat_names': 0, 'comp_type': 0,
         'volume': None, 'dwg_models': 0, 'intprt0': 0,
         'parent_dwg': 0, 'rel_model_name': 0, 'err': ''}
    try:
        data = open(path, 'rb').read()
        r['size'] = len(data)
        r['ugc'] = b'#UGC' in data[:200]
        r['fields'] = len(FIELD.findall(data))
        r['feat_names'] = len(NAMEPAT.findall(data))
        r['comp_type'] = len(re.findall(rb'comp_type\x00\x02', data))
        r['dwg_models'] = len(re.findall(rb'Dwg_Models', data))
        r['intprt0'] = len(re.findall(rb'IntPrt0', data))
        r['parent_dwg'] = len(re.findall(rb'parent_dwg_mdl_id', data))
        r['rel_model_name'] = len(re.findall(rb'rel_model_name', data))
        # объём: ED + BE-double сразу после nominal поля volume
        m = re.search(rb'volume\x00\xed', data)
        if m:
            v = be(data[m.end():m.end() + 8])
            if v is not None and 1e-9 < abs(v) < 1e12:
                r['volume'] = v
    except Exception as e:
        r['err'] = str(e)[:60]
    return r

def main():
    base, ext = sys.argv[1], sys.argv[2].lower()
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    files, total = sample(base, ext, n)
    out = io.open('base_audit_out.txt', 'w', encoding='utf-8')
    out.write('АВТО-АУДИТ · режим ТОЛЬКО ЧТЕНИЕ\n')
    out.write('папка: %s\nтип: .%s\nвсего файлов найдено: %d, в выборке: %d\n\n'
              % (base, ext, total, len(files)))

    if not files:
        out.write('ФАЙЛОВ НЕ НАЙДЕНО\n')
        out.close()
        print('нет файлов')
        return

    res = [audit(f, ext) for f in files]

    def pct(key):
        ok = sum(1 for r in res if r[key])
        return ok, len(res), 100.0 * ok / max(1, len(res))

    out.write('%-24s %-22s %s\n' % ('МЕТРИКА', 'ПРОБИТИЕ', 'ЗАМЕЧАНИЕ'))
    out.write('-' * 78 + '\n')
    metrics = [
        ('ugc', 'контейнер #UGC', ''),
        ('fields', 'закон поля E0..', 'шт. полей в файле'),
        ('feat_names', 'имена фич', 'шт. имён «Слово N»'),
        ('comp_type', 'состав (comp_type=02)', 'только для .asm'),
        ('volume', 'объём (ED+double)', 'массовые свойства'),
        ('dwg_models', 'секция Dwg_Models', 'только для .drw'),
        ('intprt0', 'встроенные детали IntPrt0', 'только для .drw'),
        ('parent_dwg', 'связь чертёж→модель', 'parent_dwg_mdl_id'),
        ('rel_model_name', 'механизм Обозначения', 'rel_model_name'),
    ]
    for key, name, note in metrics:
        ok, tot, p = pct(key)
        if key in ('fields', 'feat_names'):
            vals = [r[key] for r in res if r[key]]
            avg = sum(vals) / len(vals) if vals else 0
            out.write('%-24s %-22s среднее %d\n' % (name, '%d/%d' % (ok, tot), avg))
        else:
            out.write('%-24s %-22s %s\n' % (name, '%d/%d = %.0f%%' % (ok, tot, p), note))

    errs = [r for r in res if r['err']]
    out.write('\nОШИБОК ЧТЕНИЯ: %d из %d\n' % (len(errs), len(res)))
    for r in errs[:5]:
        out.write('   %s : %s\n' % (r['name'], r['err']))

    out.write('\n--- ПЕРВЫЕ 15 ФАЙЛОВ ---\n')
    out.write('%-42s %10s %8s %8s\n' % ('файл', 'байт', 'полей', 'имён'))
    for r in res[:15]:
        out.write('%-42s %10d %8d %8d\n' % (r['name'][:42], r['size'], r['fields'], r['feat_names']))
    out.close()
    print('base_audit_out.txt files=%d' % len(res))

if __name__ == '__main__':
    main()