# -*- coding: utf-8 -*-
"""Проверка пути инструмента: knowledge_tools.tool_search (как зовёт агент)."""
import os, sys, time
sys.path.insert(0, r"D:\AI\tools\agent")
os.chdir(r"D:\AI\tools\agent")
import knowledge_tools as K

for q in ("извещение об изменении", "спецификация ГОСТ 2.106"):
    t = time.time()
    r = K.tool_search(query=q)
    print("--- '%s': %.2f с, %d символов ---" % (q, time.time() - t, len(r)), flush=True)
    print(r[:400], flush=True)
print("\nчтение файла из репо:", K.tool_read(path=r"D:\AI\repo\README.md")[:80].replace("\n", " "), flush=True)
print("чтение лога из D:\\AI\\log:", K.tool_read(path=r"D:\AI\log\agent\agent_log_2026-09-23.txt")[:60].replace("\n", " "), flush=True)
