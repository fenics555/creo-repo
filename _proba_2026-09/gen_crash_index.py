# -*- coding: utf-8 -*-
"""Генератор списка крах-скиллов: D:\\AI\\repo\\crash\\SKILL_crash_index.md."""
import os, re

D = r"D:\AI\repo\crash"
OUT = os.path.join(D, "SKILL_crash_index.md")


def desc_of(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for ln in lines[:14]:
        s = ln.strip()
        m = re.match(r"^#?\s*description\s*:\s*(.+)$", s, re.I)
        if m:
            return m.group(1).strip()
    for ln in lines[:6]:
        s = ln.strip().lstrip("#").strip()
        if s and not s.lower().startswith(("name:", "system:", "when:", "date:", "executor:", "task:", "priority:")):
            return s
    return ""


items = []
for n in sorted(os.listdir(D)):
    if not n.endswith(".md") or n == "SKILL_crash_index.md":
        continue
    items.append((n, desc_of(os.path.join(D, n))))

head = [
    "---",
    "name: crash-index",
    "system: CRASH",
    "description: Список всех крах-скиллов папки crash (навигация); вход в тему — SKILL_crash_constitution.md",
    "when: крах, crash, список крахов, какой скилл, навигация по крахам",
    "priority: high",
    "date: 22.09.2026",
    "---",
    "# СПИСОК КРАХ-СКИЛЛОВ (D:\\AI\\repo\\crash)",
    "Вход/закон темы — `SKILL_crash_constitution.md` (правило, шаблон экземпляра, шаблон передачи, блок имён).",
    "Ниже — все экземпляры с кратким «когда применять». Счётчик повторов (`ПОВТОРЫ`) — внутри каждого скилла.",
    "",
]
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(head) + "\n")
    for n, d in items:
        f.write("- `%s` — %s\n" % (n[:-3], d if d else "(описание в файле)"))
    f.write("\nВсего крах-скиллов: %d (без учёта конституции и этого списка).\n" % len(items))
print("written", OUT, "items", len(items))