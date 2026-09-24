# -*- coding: utf-8 -*-
"""Разовая правка plm_tools.py: свои таблицы модуля — с префиксом plm_ (закон дома).
Чужие таблицы дома (bom, usage, models) модуль больше не пишет и не чистит.
Печатает каждую изменённую строку (до -> после). Бэкап файла делается здесь же.
"""
import datetime
import shutil

SRC = r"D:\AI\tools\agent\plm_tools.py"

PAIRS = [
    ("INSERT OR IGNORE INTO items(", "INSERT OR IGNORE INTO plm_items("),
    ("INSERT INTO items(", "INSERT INTO plm_items("),
    ("SELECT COUNT(*) FROM items", "SELECT COUNT(*) FROM plm_items"),
    ("SELECT * FROM items", "SELECT * FROM plm_items"),
    ("SELECT designation, rev, lifecycle FROM items", "SELECT designation, rev, lifecycle FROM plm_items"),
    ("UPDATE items SET", "UPDATE plm_items SET"),
    # чужая bom (36 811 строк!) — не чистим и не читаем; своя — plm_bom
    ('c.execute("DELETE FROM bom")',
     'c.execute("DELETE FROM plm_bom")  # ТОЛЬКО своя таблица; чужая bom (36811 строк) не трогается'),
    ("INSERT OR IGNORE INTO bom(", "INSERT OR IGNORE INTO plm_bom("),
    ("SELECT COUNT(*) FROM items\").fetchone()[0]; bb = c.execute(\"SELECT COUNT(*) FROM bom\")",
     None),  # этой строки хватит двух предыдущих замен; отдельного правила не нужно
    ("SELECT COUNT(*) FROM bom", "SELECT COUNT(*) FROM plm_bom"),
    ("SELECT child FROM bom", "SELECT child FROM plm_bom"),
    ("SELECT parent FROM bom", "SELECT parent FROM plm_bom"),
    ("INSERT INTO changes(", "INSERT INTO plm_changes("),
    ("INSERT INTO revisions(", "INSERT INTO plm_revisions("),
]

text = open(SRC, encoding="utf-8").read()
orig = text
changed = []
for old, new in PAIRS:
    if new is None:
        continue
    if old in text:
        changed.append((old, new, text.count(old)))
        text = text.replace(old, new)

if text == orig:
    print("нечего менять (уже поправлено)")
    raise SystemExit(0)

bak = SRC + "." + datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + ".bak"
shutil.copy2(SRC, bak)
open(SRC, "w", encoding="utf-8").write(text)
print("бэкап: %s" % bak)
print("замен сделано:")
for old, new, n in changed:
    print("   x%d  %s\n        -> %s" % (n, old, new))
print("\nПРОВЕРКА (не должно остаться обращений к чужим таблицам):")
bad = 0
for pat in ("FROM bom", "INTO bom(", "FROM items", "INTO items(", "UPDATE items ", "FROM changes", "FROM revisions"):
    for i, ln in enumerate(text.splitlines(), 1):
        if pat in ln and "#" not in ln.split(pat)[0].replace("c.execute(", "#"):
            print("   строка %d: %s" % (i, ln.strip()[:110]))
            bad += 1
print("подозрительных строк: %d" % bad)