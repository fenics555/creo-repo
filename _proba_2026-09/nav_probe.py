# -*- coding: utf-8 -*-
"""Проба источников для «навигатора»: поиск сборок, деталировка, PDF рядом."""
import os
import sqlite3

AG = r"D:\AI\tools\agent\data\agent.sqlite"
HV = r"D:\AI\tools\agent\data\harvest.db"


def cols(conn, table):
    return [r[1] for r in conn.execute("PRAGMA table_info(\"%s\")" % table)]


print("=== agent.sqlite ===")
a = sqlite3.connect("file:%s?mode=ro" % AG, uri=True)
for t in ("models", "bom", "usage"):
    try:
        print("--- %s: %s | строк %d" % (t, ", ".join(cols(a, t)), a.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]))
    except Exception as e:
        print("--- %s: НЕТ (%s)" % (t, e))

print("\n=== поиск «турн» в models (движок поиска проверим на нём) ===")
try:
    rows = a.execute("SELECT name, ext, path FROM models WHERE LOWER(name) LIKE '%турн%' LIMIT 12").fetchall()
    for r in rows:
        print("   %-40s %-5s %s" % (r[0], r[1], os.path.dirname(r[2])))
    print("   найдено (первые 12): %d" % len(rows))
except Exception as e:
    print("   ошибка: %s" % e)

print("\n=== есть ли деталировка в bom (чужая таблица, только чтение) ===")
try:
    top = a.execute("SELECT parent, COUNT(*) c FROM bom GROUP BY parent ORDER BY c DESC LIMIT 5").fetchall()
    for p, c in top:
        print("   %s -> детей %d" % (p, c))
    kids = a.execute("SELECT child, qty FROM bom WHERE parent=? LIMIT 8", (top[0][0],)).fetchall() if top else []
    print("   пример состава «%s»: %s" % (top[0][0] if top else "-", ", ".join(k[0] for k in kids)))
except Exception as e:
    print("   ошибка: %s" % e)

print("\n=== harvest.db ===")
try:
    h = sqlite3.connect("file:%s?mode=ro" % HV, uri=True)
    tabs = [r[0] for r in h.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    print("   таблицы: %s" % ", ".join(tabs[:12]))
    for t in ("models_raw", "pairs"):
        if t in tabs:
            print("   --- %s: %s | строк %d" % (t, ", ".join(cols(h, t)), h.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]))
    if "pairs" in tabs:
        print("   пример пар (чертёж -> pdf):")
        for row in h.execute("SELECT * FROM pairs LIMIT 3"):
            print("      %s" % (row,))
except Exception as e:
    print("   ошибка: %s" % e)