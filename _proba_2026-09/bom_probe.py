# -*- coding: utf-8 -*-
"""Кто и как наполняет таблицу bom (ТОЛЬКО ЧТЕНИЕ) + формы значений."""
import sqlite3

DB = r"D:\AI\tools\agent\data\agent.sqlite"
c = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
q = lambda s, *a: c.execute(s, a).fetchall()
print("всего строк bom:", q("SELECT COUNT(*) FROM bom")[0][0])
print("parent с путём (Z: или \\):", q("SELECT COUNT(*) FROM bom WHERE parent LIKE 'Z:%' OR parent LIKE '%\\\\%'")[0][0])
print("parent без пути:", q("SELECT COUNT(*) FROM bom WHERE parent NOT LIKE 'Z:%' AND parent NOT LIKE '%\\\\%'")[0][0])
print("child  с путём:", q("SELECT COUNT(*) FROM bom WHERE child LIKE 'Z:%' OR child LIKE '%\\\\%'")[0][0])
print("\nпримеры (parent | child | qty):")
for r in q("SELECT parent, child, qty FROM bom LIMIT 8"):
    print("   %s | %s | %s" % (str(r[0])[:60], str(r[1])[:60], r[2]))
print("\nуникальных parent:", q("SELECT COUNT(DISTINCT parent) FROM bom")[0][0],
      "| уникальных child:", q("SELECT COUNT(DISTINCT child) FROM bom")[0][0])
print("расширения child:", q("SELECT substr(child, -4) e, COUNT(*) FROM bom GROUP BY e ORDER BY 2 DESC LIMIT 6"))
print("\nфайлы(items) в базе:", q("SELECT COUNT(*) FROM items")[0][0])
c.close()