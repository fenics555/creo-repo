# -*- coding: utf-8 -*-
"""Живая проверка правки PLM: миграция таблиц в plm_* и сохранность ЧУЖОЙ таблицы bom."""
import os
import sys

AG = r"D:\AI\tools\agent"
sys.path.insert(0, AG)
os.chdir(AG)

import plm_tools  # noqa: E402

c = plm_tools._db()
c.commit()
names = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' "
                                 "AND name LIKE 'plm_%' ORDER BY name")]
print("наши таблицы: %s" % ", ".join(names) or "нет")
for t in ("bom", "usage", "items", "revisions", "changes", "models"):
    try:
        n = c.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
    except Exception:
        n = "ТАБЛИЦЫ НЕТ"
    print("   %-12s %s" % (t, n))
print(plm_tools.tool_param_audit())
print("plm_bom: %s" % plm_tools.tool_plm_bom(q="нет-такой"))
c.close()