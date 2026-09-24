# -*- coding: utf-8 -*-
"""ФАЗА 1 — инвентарь агента и план чистки (ТОЛЬКО ЧТЕНИЕ).
Для каждого файла-кандидата ищет ссылки по стему во всех .py/.bat/.ps1 агента."""
import os, re, glob, fnmatch
from pathlib import Path

AG = Path(r"D:\AI\tools\agent")
ROOT = [p for p in AG.iterdir() if p.is_file()]
SUB = [p for p in AG.iterdir() if p.is_dir()]

# кандидаты: одноразовые скрипты и хвосты
PAT_FILES = ["fix_*.py", "debug_*.py", "patch_*.py", "harvest_part*.py", "probe_*.py", "login_probe.py",
             "final_write.py", "fix_newlines.py", "cleanup_agent.py", "check_out.txt", "test_file.txt",
             "tmp_read.txt", "tmp_repr.txt", "payload.json", "*.log", "*_out.txt", "*_err.txt",
             "agent.sqlite", "agent_start_debug.log", "ctl_up.log", "ctl_up_err.log", "one_c_tools.py"]
KEEP = {"agent.py", "core.py", "settings.py", "tools_registry.py", "loop.py", "http_handlers.py",
        "agent_sched.py", "users.py", "scanner.py", "harvest.py", "backup.py", "ctl.py", "panel.py",
        "clean_skill.py", "index_repo.py", "house_state.py", "log_clean.py", "purge_versions.py",
        "kb_roots.txt", "kb_exclude.txt", "README.md"}

srcs = []
for ext in ("*.py", "*.bat", "*.ps1", "*.json"):
    srcs += glob.glob(str(AG / ext)) + glob.glob(str(AG / "dev" / ext)) + glob.glob(str(AG / "qa" / ext)) \
            + glob.glob(str(AG / "excel" / ext)) + glob.glob(str(AG / "copy" / ext))
bodies = {}
for s in srcs:
    try:
        bodies[s] = open(s, encoding="utf-8", errors="ignore").read()
    except Exception:
        bodies[s] = ""

cands = []
for f in ROOT:
    if f.name in KEEP:
        continue
    if any(fnmatch.fnmatch(f.name, p) for p in PAT_FILES):
        cands.append(f)

print("=" * 78)
print("КАНДИДАТЫ В КОРНЕ (с проверкой ссылок)")
print("=" * 78)
total = 0
for f in sorted(cands, key=lambda x: -x.stat().st_size):
    stem = f.stem
    refs = []
    for s, b in bodies.items():
        if Path(s).name == f.name:
            continue
        if re.search(r"\b%s\b" % re.escape(stem), b) or f.name in b:
            refs.append(Path(s).name)
    total += f.stat().st_size
    mark = "ССЫЛКИ!" if refs else "чисто"
    print("%-34s %8d б  %-8s %s" % (f.name, f.stat().st_size, mark,
                                    (", ".join(sorted(set(refs))[:4]) if refs else "")))
print("-" * 78)
print("ИТОГО кандидатов: %d, вес: %.2f МБ" % (len(cands), total / 1048576))

print()
print("=" * 78)
print("ПОДПАПКИ (размер, файлов)")
print("=" * 78)
for d in sorted(SUB, key=lambda x: x.name):
    fs = list(d.rglob("*"))
    sz = sum(p.stat().st_size for p in fs if p.is_file())
    print("%-24s %6d файлов  %9.2f МБ" % (d.name, len([p for p in fs if p.is_file()]), sz / 1048576))

print()
print("=" * 78)
print("ПОДОЗРИТЕЛЬНОЕ")
print("=" * 78)
for p in [AG / "agent.sqlite", AG / "login.json", AG / "data" / "secrets.json",
          AG / "data" / "backup_20260907_0828.sqlite", AG / "data" / "backup_pre_orphan_20260904.sqlite"]:
    print("%-58s %s" % (str(p).replace(str(AG), "."), ("%.2f МБ" % (p.stat().st_size / 1048576)) if p.exists() else "нет"))
print()
print("backups (ротация retention=7):")
bk = sorted((AG / "data" / "backups").glob("*.sqlite"), key=lambda f: f.stat().st_mtime)
for i, f in enumerate(bk):
    print("   %2d %-34s %8.2f ГБ  %s" % (i + 1, f.name, f.stat().st_size / 1073741824,
                                         "СТАРЕЙШИЙ (кандидат)" if i == 0 and len(bk) > 7 else ""))