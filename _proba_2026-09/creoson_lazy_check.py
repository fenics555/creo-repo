# -*- coding: utf-8 -*-
"""Проверка ленивого CREOSON: creo_call должен сам поднять сервер при первом обращении."""
import os, sys, time
sys.path.insert(0, r"D:\AI\tools\agent")
os.chdir(r"D:\AI\tools\agent")
import creo_tools as CT

t = time.time()
j = CT.creo_call("connection", "is_creo_running")
err = (j.get("status") or {}).get("error")
print("creo_call(connection/is_creo_running) за %.0f с, ошибка=%s" % (time.time() - t, err), flush=True)
print(str(j)[:400], flush=True)