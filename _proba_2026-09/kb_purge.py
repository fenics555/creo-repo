# -*- coding: utf-8 -*-
"""Чистка базы знаний агента: бэкап → удаление всех чанков → VACUUM (ТОЛЬКО agent.sqlite)."""
import os, shutil, sqlite3, time

AG = r"D:\AI\tools\agent"
DB = os.path.join(AG, "data", "agent.sqlite")
BK = os.path.join(AG, "data", "backup", "pre_kbclean_20260923_agent.sqlite")

def gb(p):
    return os.path.getsize(p) / 1073741824 if os.path.exists(p) else 0

print("до: база %.2f ГБ" % gb(DB), flush=True)
c = sqlite3.connect(DB, timeout=180)
c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
n_before = c.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
n_emb = c.execute("SELECT COUNT(*) FROM model_embs").fetchone()[0]
c.close()
print("чанков к удалению: %d (model_embs оставляем: %d)" % (n_before, n_emb), flush=True)

if not os.path.exists(BK):
    t = time.time()
    shutil.copy2(DB, BK)
    print("бэкап: %s (%.2f ГБ, %.0f с)" % (BK, gb(BK), time.time() - t), flush=True)
else:
    print("бэкап уже есть: %s" % BK, flush=True)

c = sqlite3.connect(DB, timeout=180)
c.execute("PRAGMA journal_mode=WAL")
t = time.time()
c.execute("DELETE FROM chunks")
c.commit()
print("удаление: %.0f с" % (time.time() - t), flush=True)
t = time.time()
c.execute("VACUUM")
c.commit()
print("VACUUM: %.0f с" % (time.time() - t), flush=True)
print("chunks сейчас: %d" % c.execute("SELECT COUNT(*) FROM chunks").fetchone()[0], flush=True)
c.close()
print("после: база %.2f ГБ (бэкап %.2f ГБ)" % (gb(DB), gb(BK)), flush=True)