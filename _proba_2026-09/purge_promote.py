# -*- coding: utf-8 -*-
"""Перенос чистки версий Creo в автономную программу agent\\purge_versions\\
  engine.py  — движок (из agent\\purge_versions.py, пути по закону дома)
  gui.py     — окно (из agent\\purge_gui.py, свои настройки и логи)
Печатает все замены, чтобы правка была видимой, а не магической.
"""
import os
import re
import shutil
from pathlib import Path

AG = Path(r"D:\AI\tools\agent")
PROG = AG / "purge_versions"
PROG.mkdir(exist_ok=True)

# ---------- движок ----------
eng = (AG / "purge_versions.py").read_text(encoding="utf-8")
diffs = []


def sub(text, old, new, why):
    if old not in text:
        diff = "НЕ НАЙДЕНО: %s" % why
        return text
    diffs.append("engine: %s" % why)
    return text.replace(old, new, 1)


eng = sub(eng,
          "EXTS = {'.prt', '.asm', '.drw', '.frm', '.lay', '.sec'}",
          "EXTS = {'.prt', '.asm', '.drw', '.frm', '.lay', '.sec'}\n\n"
          "# --- автономная программа: всё своё рядом, логи по закону дома ---\n"
          "PROG_DIR = Path(__file__).resolve().parent\n"
          "LOG_DIR = Path(r\"D:\\AI\\log\\purge_versions\")\n"
          "SETTINGS_FILE = PROG_DIR / \"gui_settings.json\"",
          "добавлены PROG_DIR / LOG_DIR / SETTINGS_FILE")
eng = sub(eng, 'ld = Path(r"D:\\AI\\log\\purge")', "ld = LOG_DIR", "log dir -> LOG_DIR")
eng = sub(eng, "ld.mkdir(parents=True, exist_ok=True)",
          "ld.mkdir(parents=True, exist_ok=True)", "лог-каталог создаётся как раньше")
(AG / "purge_versions_shim_old.py").write_text(eng, encoding="utf-8") if False else None
(PROG / "engine.py").write_text(eng, encoding="utf-8")

# ---------- окно ----------
gui = (AG / "purge_gui.py").read_text(encoding="utf-8")
gui = sub(gui,
          "# Add agent tools to path\nsys.path.append(r\"D:\\AI\\tools\\agent\")",
          "# движок лежит рядом с окном (программа автономна)\n"
          "sys.path.insert(0, str(Path(__file__).resolve().parent))",
          "путь к движку: своя папка")
gui = sub(gui, "SETTINGS_FILE = Path(r\"D:\\AI\\data\\purge_gui_settings.json\")",
          "SETTINGS_FILE = Path(__file__).resolve().parent / \"gui_settings.json\"",
          "настройки -> рядом с программой")
gui = sub(gui, "LOG_FILE = Path(r\"D:\\AI\\log\\purge\\purge.log\")",
          "LOG_FILE = Path(r\"D:\\AI\\log\\purge_versions\\purge.log\")", "лог прогонов -> log\\purge_versions")
gui = sub(gui, "LAST_PURGE_FILE = Path(r\"D:\\AI\\log\\purge\\last_purge.json\")",
          "LAST_PURGE_FILE = Path(r\"D:\\AI\\log\\purge_versions\\last_purge.json\")", "отчёт -> log\\purge_versions")
gui = sub(gui, "LOCK_FILE = Path(r\"D:\\AI\\log\\purge\\purge.lock\")",
          "LOCK_FILE = Path(r\"D:\\AI\\log\\purge_versions\\purge.lock\")", "замок -> log\\purge_versions")
(PROG / "gui.py").write_text(gui, encoding="utf-8")

print("создано в %s:" % PROG)
for f in ("engine.py", "gui.py"):
    print("   %-10s %d КБ" % (f, round((PROG / f).stat().st_size / 1024, 1)))
print("замены:")
for d in diffs:
    print("   " + d)
print("\nПРОВЕРКА: остались ли жёсткие пути агента в программе")
for f in ("engine.py", "gui.py"):
    txt = (PROG / f).read_text(encoding="utf-8")
    for m in re.finditer(r"D:\\\\AI\\\\[^\"]*", txt):
        pass
    bad = [ln.strip() for ln in txt.splitlines()
           if "D:\\AI\\tools\\agent" in ln or "D:\\AI\\data" in ln or "log\\purge\\" in ln]
    print("   %-10s подозрительных строк: %d %s" % (f, len(bad), bad[:3]))