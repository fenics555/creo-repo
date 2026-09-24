# -*- coding: utf-8 -*-
"""Из чего состоят базы знаний агента: chunks / models / model_embs (ТОЛЬКО ЧТЕНИЕ)."""
import sqlite3

c = sqlite3.connect("file:D:/AI/tools/agent/data/agent.sqlite?mode=ro", uri=True)
q = lambda s, *a: c.execute(s, a).fetchall()

print("=== схема ===")
for t in ("chunks", "models", "model_embs", "files"):
    try:
        print(t, "->", c.execute("PRAGMA table_info(%s)" % t).fetchall())
    except Exception as e:
        print(t, "нет:", e)

print("\n=== chunks: 1 330 971 ===")
print("уникальных путей:", q("SELECT COUNT(DISTINCT path) FROM chunks")[0][0])
print("\nТОП-12 корней (по началу пути):")
for p, n in q("""SELECT substr(path,1,28) p, COUNT(*) n FROM chunks
                 GROUP BY p ORDER BY n DESC LIMIT 12"""):
    print("   %-30s %8d" % (p, n))

print("\nпо расширению файла:")
for e, n in q("""SELECT lower(substr(path, -4)) e, COUNT(*) n FROM chunks
                 GROUP BY e ORDER BY n DESC LIMIT 12"""):
    print("   %-6s %8d" % (e, n))

print("\nдубликаты текста (одинаковый text):")
d = q("SELECT COUNT(*), SUM(cnt) FROM (SELECT text, COUNT(*) cnt FROM chunks GROUP BY text HAVING cnt > 1)")
print("   групп-дублей: %d, строк в них: %d" % (d[0][0] or 0, d[0][1] or 0))
print("пустых/коротких (<50 симв.):", q("SELECT COUNT(*) FROM chunks WHERE LENGTH(COALESCE(text,''))<50")[0][0])
print("длина путей: средн. %d, макс. %d" % tuple(x[0] or 0 for x in q("SELECT AVG(LENGTH(path)), MAX(LENGTH(path)) FROM chunks")[0]))

print("\n=== models ===")
print("всего:", q("SELECT COUNT(*) FROM models")[0][0], "| эмбеддингов:", q("SELECT COUNT(*) FROM model_embs")[0][0])
print("по расширению:")
for e, n in q("""SELECT lower(substr(name, -4)) e, COUNT(*) n FROM models
                 GROUP BY e ORDER BY n DESC LIMIT 8"""):
    print("   %-6s %8d" % (e, n))
print("ТОП-8 корней:")
for p, n in q("""SELECT substr(path,1,26) p, COUNT(*) n FROM models
                 GROUP BY p ORDER BY n DESC LIMIT 8"""):
    print("   %-28s %8d" % (p, n))
print("\n=== files (инвентарь) ===")
try:
    print("всего файлов:", q("SELECT COUNT(*) FROM files")[0][0])
    print("с хешем:", q("SELECT COUNT(*) FROM files WHERE hash IS NOT NULL AND hash<>''")[0][0])
except Exception as e:
    print("нет таблицы files:", e)
c.close()