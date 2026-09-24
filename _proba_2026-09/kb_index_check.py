# -*- coding: utf-8 -*-
"""Проверка нового индекса знаний: сборка FTS5 + поиск (без эмбеддингов)."""
import os, sys, time
sys.path.insert(0, r"D:\AI\tools\agent")
os.chdir(r"D:\AI\tools\agent")
import scanner

t = time.time()
print("index_all ->", scanner.index_all(), "за %.1f с" % (time.time() - t), flush=True)
print("состояние индекса:", scanner.kb_state(), flush=True)

for q in ("извещение об изменении ГОСТ 2.503", "спецификация ГОСТ 2.106", "PDF чертёж печать"):
    t = time.time()
    rows = scanner.kb_search(q, limit=3)
    print("\n--- поиск '%s': %d фрагментов за %.2f с ---" % (q, len(rows), time.time() - t), flush=True)
    for p, txt in rows:
        print("  %s | %s" % (p, txt.strip().replace("\n", " ")[:110]), flush=True)
