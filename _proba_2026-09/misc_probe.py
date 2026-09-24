# -*- coding: utf-8 -*-
"""Последние факты: инвентарь/models, шаблоны с учётом версий, объём мусора в БЗ."""
import glob, os, sqlite3

c = sqlite3.connect("file:D:/AI/tools/agent/data/agent.sqlite?mode=ro", uri=True)
q = lambda s: (c.execute(s).fetchone()[0] or 0)

print("=== models / usage ===")
print("  models под Z:\\PTC\\Work:     %d" % q("SELECT COUNT(*) FROM models WHERE path LIKE 'Z:\\PTC\\Work%'"))
print("  models вне Work:            %d" % q("SELECT COUNT(*) FROM models WHERE path NOT LIKE 'Z:\\PTC\\Work%'"))
print("  моделей с неуникальным именем: %d" % q("SELECT COUNT(*) FROM (SELECT name FROM models GROUP BY name HAVING COUNT(*)>1)"))
print("  usage с известным путём:    %d из %d" % (q("SELECT COUNT(*) FROM usage WHERE COALESCE(parent_path,'')<>''"), q("SELECT COUNT(*) FROM usage")))

print("\n=== что останется после чистки БЗ ===")
print("  осмысленных чанков (>=50):  %d, эмбеддингов %.2f ГБ" % (
    q("SELECT COUNT(*) FROM chunks WHERE LENGTH(COALESCE(text,''))>=50"),
    q("SELECT SUM(LENGTH(emb)) FROM chunks WHERE LENGTH(COALESCE(text,''))>=50") / 1073741824))
for name, w in (("мусор <50 симв.", "LENGTH(COALESCE(text,''))<50"),
                ("чертежи .drw", "lower(path) LIKE '%.drw.%'"),
                ("установка Creo", "path LIKE 'D:\\PTC\\CREO12%'"),
                ("из репо (наши скиллы)", "path LIKE 'D:\\AI\\repo%'")):
    print("  %-24s %8d чанков, %6.2f ГБ эмбеддингов" % (
        name, q("SELECT COUNT(*) FROM chunks WHERE " + w),
        q("SELECT SUM(LENGTH(emb)) FROM chunks WHERE " + w) / 1073741824))
print("  матрица из осмысленных: %.2f ГБ (было 3.81)" % (
    q("SELECT COUNT(*) FROM chunks WHERE LENGTH(COALESCE(text,''))>=50") * 768 * 4 / 1073741824))

print("\n=== шаблоны: разрешение Creo-версий (base -> newest .N) ===")
for p in (r"Z:\PTC\CREO-START\НАСТРОЙКИ\ШАБЛОНЫ\mm_part.prt",
          r"Z:\PTC\CREO-START\НАСТРОЙКИ\ШАБЛОНЫ\sborka_mm.asm",
          r"Z:\PTC\CREO-START\НАСТРОЙКИ\ШАБЛОНЫ\mm_sheet.prt"):
    v = sorted(glob.glob(p + ".*"))
    print("  %-18s -> %s" % (os.path.basename(p), [os.path.basename(x) for x in v] or "НЕ найдено"))
print("  каталог $PRO_DIRECTORY\\ШАБЛОНЫ существует:", os.path.isdir(r"D:\PTC\CREO12\Creo 12.4.2.0\Common Files\ШАБЛОНЫ"))
print("  файлы .drw в ШАБЛОНЫ:", [os.path.basename(x) for x in glob.glob(r"Z:\PTC\CREO-START\НАСТРОЙКИ\ШАБЛОНЫ\*.drw*")])
c.close()