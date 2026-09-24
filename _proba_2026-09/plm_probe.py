# -*- coding: utf-8 -*-
"""Инвентарь ПЛМ-данных агента: таблицы, схемы, индексы, наполнение (ТОЛЬКО ЧТЕНИЕ)."""
import sqlite3

DB = r"D:\AI\tools\agent\data\agent.sqlite"
c = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
for t in ("items", "bom", "usage", "revisions", "changes", "models", "facts", "trail_scans"):
    try:
        sql = c.execute("SELECT sql FROM sqlite_master WHERE name=?", (t,)).fetchone()
        n = c.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        idx = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name=?", (t,))]
        print("=== %s === строк: %d | индексы: %s" % (t, n, ", ".join(idx) or "нет"))
        print("   " + (sql[0].replace("\n", " ") if sql else "нет таблицы"))
        if n and t in ("items", "bom", "usage"):
            cols = [d[1] for d in c.execute("PRAGMA table_info(%s)" % t)]
            print("   пример:", c.execute('SELECT * FROM "%s" LIMIT 2' % t).fetchall())
            print("   колонки:", cols)
    except Exception as e:
        print("=== %s === ошибка: %s" % (t, e))
c.close()