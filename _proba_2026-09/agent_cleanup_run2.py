# -*- coding: utf-8 -*-
"""ФАЗА 2б — вторая волна чистки: осиротевшие части и старые .bak (ссылок в коде нет)."""
from pathlib import Path

AG = Path(r"D:\AI\tools\agent")
DEL = ["purge_versions_part1.py", "purge_versions_part2.py",
       "test_imports.py", "test_purge_gui.py", "test_file.txt.prev", "rescan.json",
       "pre71_p2_agent.py.bak", "pre71_p2_sched.py.bak", "pre_spec77_pdftools.bak"]

freed = 0
for n in DEL:
    p = AG / n
    if not p.exists():
        continue
    sz = p.stat().st_size
    try:
        p.unlink(); freed += sz
        print("  - %s  %d б" % (n, sz))
    except Exception as e:
        print("  ! %s — %s" % (n, e))
print("освобождено: %.1f КБ" % (freed / 1024))
print("осталось файлов в корне: %d" % len([f for f in AG.iterdir() if f.is_file()]))