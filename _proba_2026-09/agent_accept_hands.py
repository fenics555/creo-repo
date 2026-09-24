# -*- coding: utf-8 -*-
"""ПРИЁМКА «РУКАМИ»: тот же реестр инструментов, что у агента, но вызов из скрипта.
Доказывает: инструментами можно пользоваться без ИИ и без HTTP."""
import sys, traceback
sys.path.insert(0, r"D:\AI\tools\agent")

import tools_registry as TR

print("блоков: %d | инструментов: %d" % (len(TR.BLOCKS), len(TR.TOOLS)))
print("блоки:", ", ".join(sorted(TR.BLOCKS)))
print("-" * 74)

CHECK = ["creo_status", "creo_pwd", "creo_session", "creo_get_active",
         "models_stats", "usage_state", "backup_list", "help"]
for name in CHECK:
    t = TR.get(name)
    if not t:
        print("%-18s НЕТ в реестре" % name)
        continue
    try:
        r = str(t["fn"]())
        r = " ".join(r.split())
        print("%-18s → %s" % (name, r[:220]))
    except Exception as e:
        print("%-18s → ОШИБКА: %s" % (name, e))
        traceback.print_exc()

print("-" * 74)
print("пишущие (под щитом, approval=True): %d" % len([t for t in TR.TOOLS if t.get("approval")]))
print("только чтение: %d" % len([t for t in TR.TOOLS if not t.get("approval")]))