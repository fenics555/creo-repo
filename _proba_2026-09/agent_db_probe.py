# -*- coding: utf-8 -*-
"""Проба: схема и объёмы баз агента (ТОЛЬКО ЧТЕНИЕ, mode=ro)."""
import sqlite3, os, glob

for p in [r"D:\AI\tools\agent\data\agent.sqlite", r"D:\AI\tools\agent\data\harvest.db"]:
    print("=" * 72)
    print(p, ("%.1f МБ" % (os.path.getsize(p) / 1048576)) if os.path.exists(p) else "НЕТ ФАЙЛА")
    if not os.path.exists(p):
        continue
    try:
        c = sqlite3.connect("file:%s?mode=ro" % p.replace("\\", "/"), uri=True)
        ts = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        print("таблиц: %d" % len(ts))
        for t in ts:
            try:
                n = c.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
            except Exception:
                n = "?"
            print("   %-30s %s" % (t, n))
        c.close()
    except Exception as e:
        print("ошибка:", e)

print("=" * 72)
print("все базы внутри агента:")
seen = []
for p in glob.glob(r"D:\AI\tools\agent\**\*.db", recursive=True) + \
         glob.glob(r"D:\AI\tools\agent\**\*.sqlite", recursive=True):
    seen.append("  %-64s %.2f МБ" % (p, os.path.getsize(p) / 1048576))
print("\n".join(sorted(seen)) or "  нет")