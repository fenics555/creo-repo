# -*- coding: utf-8 -*-
"""Список таблиц agent.sqlite + учёт вызовов инструментов, если он есть (ТОЛЬКО ЧТЕНИЕ)."""
import sqlite3

c = sqlite3.connect("file:D:/AI/tools/agent/data/agent.sqlite?mode=ro", uri=True)
tabs = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("таблиц: %d" % len(tabs))
print(", ".join(tabs))
print("\n=== размеры (строки) ===")
for t in tabs:
    try:
        n = c.execute("SELECT COUNT(*) FROM [%s]" % t).fetchone()[0]
        print("   %-24s %10d" % (t, n))
    except Exception as e:
        print("   %-24s ? %s" % (t, e))
c.close()