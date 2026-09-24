# -*- coding: utf-8 -*-
"""Проверка: сколько памяти ест импорт инструментов агента и ленива ли матрица.
Запуск: python mem_probe.py            — только импорт (быстро)
        python mem_probe.py --load     — ещё и реальная загрузка матрицы знаний
"""
import ctypes, ctypes.wintypes as wt, os, sys, time

class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]

def ram():
    p = PMC(); p.cb = ctypes.sizeof(PMC)
    ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),
                                             ctypes.byref(p), p.cb)
    return p.WorkingSetSize / 1024.0 ** 3, p.PeakWorkingSetSize / 1024.0 ** 3

AG = r"D:\AI\tools\agent"
sys.path.insert(0, AG); os.chdir(AG)
cur, peak = ram()
print("старт процесса: RAM %.2f ГБ" % cur, flush=True)

t = time.time()
import core                                   # noqa
import knowledge_tools as K
import similar_tools as S
print("импорт core+knowledge+similar: %.1f c, RAM %.2f ГБ (пик %.2f)" % (time.time() - t, *ram()), flush=True)
print("  knowledge: MAT=%s, ROWS=%d  -> ленивая: %s" % (K.MAT, len(K.ROWS), K.MAT is None), flush=True)
print("  similar  : MAT=%s, ROWS=%d  -> ленивая: %s" % (S.MAT, len(S.ROWS), S.MAT is None), flush=True)

t = time.time()
try:
    import tools_registry                      # импорт ВСЕХ инструментов агента
    print("импорт tools_registry: %.1f c, RAM %.2f ГБ (пик %.2f)" % (time.time() - t, *ram()), flush=True)
except Exception as e:
    print("tools_registry не поднялся: %s" % e, flush=True)

print("ИТОГ до ленивой загрузки: RAM %.2f ГБ, пик %.2f ГБ" % ram(), flush=True)

if "--load" in sys.argv:
    t = time.time()
    K.ensure()
    d = time.time() - t
    print("ensure() матрицы знаний: %.1f c, MAT=%s" % (d, None if K.MAT is None else K.MAT.shape), flush=True)

if "--sleep" in sys.argv:
    time.sleep(int(sys.argv[sys.argv.index("--sleep") + 1]))
