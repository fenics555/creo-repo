# -*- coding: utf-8 -*-
"""Проверка формата имён в инвентаре (для приёмки spec113)."""
import os
import re
import sqlite3

AG = "file:D:/AI/tools/agent/data/agent.sqlite?mode=ro"
HV = "file:D:/AI/tools/agent/data/harvest.db?mode=ro"
a = sqlite3.connect(AG, uri=True)
h = sqlite3.connect(HV, uri=True)

print("=== agent.sqlite: samples models.name ===")
for (n,) in a.execute("SELECT name FROM models LIMIT 8"):
    print("   ", n)
print("всего:", a.execute("SELECT COUNT(*) FROM models").fetchone()[0])
print("с расширением .prt/.asm/.drw:",
      a.execute("SELECT COUNT(*) FROM models WHERE lower(name) LIKE '%.prt%' OR lower(name) LIKE '%.asm%'").fetchone()[0])
print("точное 'приваи':", a.execute("SELECT COUNT(*) FROM models WHERE name='приваи'").fetchone()[0])
print("LIKE 'приваи%':", a.execute("SELECT COUNT(*) FROM models WHERE name LIKE 'приваи%'").fetchone()[0])

print("\n=== harvest.db: samples models_raw.name ===")
for (n,) in h.execute("SELECT name FROM models_raw LIMIT 6"):
    print("   ", n)
print("всего:", h.execute("SELECT COUNT(*) FROM models_raw").fetchone()[0])
print("точное 'приваи':", h.execute("SELECT COUNT(*) FROM models_raw WHERE name='приваи'").fetchone()[0])
print("LIKE 'приваи%':", h.execute("SELECT COUNT(*) FROM models_raw WHERE name LIKE 'приваи%'").fetchone()[0])

print("\n=== ищем случай «модель есть в другом месте» (чертёж без модели рядом) ===")
def base(fn):
    return re.sub(r"\.(prt|asm|drw|frm|sec|lay)(\.\d+)?$", "", fn.lower(), flags=re.I)

found = 0
for (p,) in a.execute("SELECT path FROM models WHERE lower(name) LIKE '%.drw%' AND path LIKE 'Z:\\PTC\\Work%' LIMIT 3000"):
    d = os.path.dirname(p)
    b = base(os.path.basename(p))
    near = any(os.path.exists(os.path.join(d, b + ext)) or os.path.exists(os.path.join(d, b + ext + ".1"))
               for ext in (".prt", ".asm"))
    if near:
        continue
    # есть ли модель с таким же базовым именем где-то ещё в базе
    others = a.execute("SELECT path FROM models WHERE (lower(name) LIKE ? OR lower(name) LIKE ?) AND path <> ?",
                       (b + ".prt%", b + ".asm%", p)).fetchall()
    if others:
        found += 1
        print("  РЯДОМ НЕТ, но есть в другом месте: %s" % os.path.basename(p))
        print("     чертёж: %s" % p)
        print("     модель: %s" % others[0][0])
        if found >= 5:
            break
print("таких случаев найдено (до 5):", found)
a.close(); h.close()