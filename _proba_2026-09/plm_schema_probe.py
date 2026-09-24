# -*- coding: utf-8 -*-
"""Схема таблиц PLM в базе агента — ПЕРЕД правкой plm_tools (только чтение)."""
import sqlite3
import sys

db = sys.argv[1] if len(sys.argv) > 1 else r"D:\AI\tools\agent\data\agent.sqlite"
c = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
names = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("таблиц всего: %d" % len(names))
interesting = [n for n in names if n.lower() in ("items", "bom", "usage", "revisions", "changes")
               or n.lower().startswith("plm")]
for n in interesting:
    sql = c.execute("SELECT sql FROM sqlite_master WHERE name=?", (n,)).fetchone()[0]
    cnt = c.execute('SELECT COUNT(*) FROM "%s"' % n).fetchone()[0]
    print("\n--- %s (строк: %s)" % (n, cnt))
    print(sql)
print("\nвсе таблицы: %s" % ", ".join(names))