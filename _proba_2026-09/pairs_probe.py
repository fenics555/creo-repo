# -*- coding: utf-8 -*-
"""Проба: домашние пары «чертёж + PDF» из harvest.db (ТОЛЬКО ЧТЕНИЕ) — учимся именам и папкам."""
import sqlite3

c = sqlite3.connect("file:D:/AI/tools/agent/data/harvest.db?mode=ro", uri=True)
print("=== схема таблицы pairs ===")
print(c.execute("SELECT sql FROM sqlite_master WHERE name='pairs'").fetchone()[0])
cols = [d[1] for d in c.execute("PRAGMA table_info(pairs)")]
print("колонки:", cols)

print()
print("=== свежесть ===")
try:
    for r in c.execute("SELECT freshness, COUNT(*) FROM pairs GROUP BY freshness"):
        print("   %-24s %d" % (r[0], r[1]))
except Exception as e:
    print("   нет колонки freshness:", e)

print()
print("=== 6 примеров пар ===")
for r in c.execute("SELECT * FROM pairs LIMIT 6"):
    print("   " + " | ".join(str(x)[:110] for x in r))

print()
print("=== имена PDF: расширения ===")
try:
    for r in c.execute("SELECT DISTINCT lower(substr(pdf_path, -4)) e, COUNT(*) FROM pairs GROUP BY e ORDER BY 2 DESC LIMIT 8"):
        print("   %-6s %d" % (r[0], r[1]))
except Exception as e:
    print("   ", e)