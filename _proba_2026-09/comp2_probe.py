# -*- coding: utf-8 -*-
"""Состав баз агента, часть 2: что осмысленно, что мусор (ТОЛЬКО ЧТЕНИЕ)."""
import sqlite3

c = sqlite3.connect("file:D:/AI/tools/agent/data/agent.sqlite?mode=ro", uri=True)
q = lambda s: c.execute(s).fetchall()
def one(s):
    r = c.execute(s).fetchone()
    return (r[0] if r else 0) or 0

print("=== chunks: %d ===" % one("SELECT COUNT(*) FROM chunks"))
print("  пустых/коротких (<50 симв.): %d" % one("SELECT COUNT(*) FROM chunks WHERE LENGTH(COALESCE(text,''))<50"))
print("  осмысленных (>=50 симв.):    %d" % one("SELECT COUNT(*) FROM chunks WHERE LENGTH(COALESCE(text,''))>=50"))
print("  из репо D:\\AI\\repo:          %d (осмысленных: %d)" % (
    one("SELECT COUNT(*) FROM chunks WHERE path LIKE 'D:\\AI\\repo%'"),
    one("SELECT COUNT(*) FROM chunks WHERE path LIKE 'D:\\AI\\repo%' AND LENGTH(COALESCE(text,''))>=50")))
print("  из Z:\\PTC\\Work:              %d" % one("SELECT COUNT(*) FROM chunks WHERE path LIKE 'Z:\\PTC\\Work%'"))
print("  путей уникальных:            %d" % one("SELECT COUNT(DISTINCT path) FROM chunks"))
print("  путей .drw:                  %d" % one("SELECT COUNT(DISTINCT path) FROM chunks WHERE lower(path) LIKE '%.drw.%'"))
print("  эмбеддингов всего, ГБ:       %.2f" % (one("SELECT SUM(LENGTH(emb)) FROM chunks")/1073741824))
print("  из них у мусора (<50), ГБ:   %.2f" % (one("SELECT SUM(LENGTH(emb)) FROM chunks WHERE LENGTH(COALESCE(text,''))<50")/1073741824))
print("  текстов всего, МБ:           %.1f" % (one("SELECT SUM(LENGTH(text)) FROM chunks")/1048576))

print("\n=== models: %d (эмбеддингов %d) ===" % (one("SELECT COUNT(*) FROM models"), one("SELECT COUNT(*) FROM model_embs")))
for e, n in q("SELECT lower(COALESCE(ext,'?')) e, COUNT(*) n FROM models GROUP BY e ORDER BY n DESC LIMIT 8"):
    print("   %-8s %8d" % (e, n))
print("  корни:")
for p, n in q("SELECT substr(path,1,24) p, COUNT(*) n FROM models GROUP BY p ORDER BY n DESC LIMIT 8"):
    print("   %-26s %8d" % (p, n))
print("  эмбеддингов models, ГБ:      %.2f" % (one("SELECT SUM(LENGTH(emb)) FROM model_embs")/1073741824))

print("\n=== связи и инвентарь ===")
print("  usage: %d | files: %d | bom(легаси): %d" % (
    one("SELECT COUNT(*) FROM usage"), one("SELECT COUNT(*) FROM files"), one("SELECT COUNT(*) FROM bom")))
c.close()