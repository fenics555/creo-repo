# -*- coding: utf-8 -*-
"""Проверка формата домашних баз: как хранятся имена моделей (для поиска «где модель»)."""
import sqlite3

for db, table in ((r"D:\AI\tools\agent\data\agent.sqlite", "models"),
                  (r"D:\AI\tools\agent\data\harvest.db", "models_raw")):
    print("=" * 80)
    print(db, "->", table)
    try:
        c = sqlite3.connect("file:%s?mode=ro" % db.replace("\\", "/"), uri=True)
        cols = [d[1] for d in c.execute("PRAGMA table_info(%s)" % table)]
        print("колонки:", cols)
        for r in c.execute("SELECT * FROM %s LIMIT 4" % table):
            print("   ", [str(x)[:70] for x in r])
        for probe in ("vbmt1604-20x20x5-v1", "vbmt1604-20x20x5-v1.prt", "a887-94-1500-01"):
            q = "SELECT * FROM %s WHERE lower(%s) LIKE ? LIMIT 2" % (table, cols[0])
            rows = c.execute(q, ("%" + probe.lower() + "%",)).fetchall()
            print("   поиск %-28s -> %d строк %s" % (probe, len(rows), ([str(x)[:60] for x in rows[0]] if rows else "")))
        c.close()
    except Exception as e:
        print("ошибка:", e)