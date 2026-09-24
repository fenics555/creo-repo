# -*- coding: utf-8 -*-
"""Функциональная проверка: search_kb работает после перевода матрицы на ленивую загрузку."""
import os, sys, time
sys.path.insert(0, r"D:\AI\tools\agent")
os.chdir(r"D:\AI\tools\agent")
import knowledge_tools as K

q = sys.argv[1] if len(sys.argv) > 1 else "ГОСТ 2.503 извещение об изменении"
print("до поиска: MAT=%s ROWS=%d (ленивая)" % (K.MAT, len(K.ROWS)), flush=True)
t = time.time()
r = K.tool_search(query=q)
d = time.time() - t
print("поиск '%s': %.1f c, ответ %d символов" % (q, d, len(r)), flush=True)
print("----- начало ответа -----", flush=True)
print(r[:700], flush=True)
print("----- конец -----", flush=True)
print("после поиска: MAT=%s ROWS=%d" % (None if K.MAT is None else K.MAT.shape, len(K.ROWS)), flush=True)
