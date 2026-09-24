# -*- coding: utf-8 -*-
"""ФАЗА 2 — ЧИСТКА агента. Удаляются ТОЛЬКО файлы из явного списка ниже.
Каждое удаление логируется; занятые файлы пропускаются; итог — сколько освободилось."""
import os
from pathlib import Path

AG = Path(r"D:\AI\tools\agent")
DRY = False          # поставь True для сухого прогона

# --- корень: одноразовые скрипты и хвосты (проверено: ссылок в коде нет) ---
ROOT_DEL = [
    "fix_skills.py", "fix_gui.py", "fix_build_system.py", "fix_build_system_v2.py", "fix_build_system_v3.py",
    "fix_loop_v2.py", "fix_crashskill.py", "fix_parse_model.py", "fix_think_tags.py", "fix_all_think_tags.py",
    "fix_all_think_tags_v2.py", "fix_newlines.py", "patch_http_handlers.py",
    "debug_violations.py", "debug_skill.py", "debug_skill_v2.py", "debug_groups.py",
    "harvest_part1.py", "harvest_part2.py", "probe_wiz.py", "login_probe.py",
    "final_write.py", "cleanup_agent.py",
    "check_out.txt", "tmp_read.txt", "tmp_repr.txt", "test_file.txt", "payload.json",
    "agent_start_debug.log", "ctl_up.log", "ctl_up_err.log", "agent_err.log", "agent_out.log", "agent.sqlite",
]
# --- папки целиком (одноразовые тест-артефакты) ---
DIR_DEL = ["test_purge_dir", "test_purge_dir_new"]
# --- файлы внутри tmp\ ---
TMP_DEL = ["fix_app_js.py", "fix_app_js_v2.py", "fix_app_js_v3.py"]
# --- посторонние дампы БД вне маски ротации ---
DATA_DEL = ["backup_20260907_0828.sqlite", "backup_pre_orphan_20260904.sqlite"]

freed = 0
done, skipped = [], []


def kill(p: Path):
    global freed
    try:
        sz = p.stat().st_size if p.is_file() else sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
    except Exception:
        sz = 0
    if DRY:
        print("  [dry] %s  %.2f МБ" % (p, sz / 1048576)); return
    try:
        if p.is_dir():
            import shutil; shutil.rmtree(p)
        else:
            p.unlink()
        freed += sz
        done.append("%s (%.2f МБ)" % (p.name, sz / 1048576))
        print("  - %s  %.2f МБ" % (p, sz / 1048576))
    except Exception as e:
        skipped.append("%s — %s" % (p, e))
        print("  ! не удалилось: %s (%s)" % (p, e))


print("=== 1. корень агента ===")
for n in ROOT_DEL:
    p = AG / n
    if p.exists():
        kill(p)

print("=== 2. папки-артефакты ===")
for n in DIR_DEL:
    p = AG / n
    if p.exists():
        kill(p)

print("=== 3. tmp\\ ===")
for n in TMP_DEL:
    p = AG / "tmp" / n
    if p.exists():
        kill(p)

print("=== 4. посторонние дампы data\\ ===")
for n in DATA_DEL:
    p = AG / "data" / n
    if p.exists():
        kill(p)

print("=== 5. __pycache__ агента (пересоздастся) ===")
pc = AG / "__pycache__"
if pc.exists():
    for f in sorted(pc.glob("*.pyc")):
        kill(f)

print("=== 6. data\\tmp (кроме открытых файлов) ===")
dt = AG / "data" / "tmp"
if dt.exists():
    for f in sorted(dt.glob("*")):
        if f.is_file():
            kill(f)

print()
print("=" * 70)
print("УДАЛЕНО: %d объектов, освобождено %.2f МБ" % (len(done), freed / 1048576))
if skipped:
    print("ПРОПУЩЕНО (заняты/ошибка): %d" % len(skipped))
    for s in skipped[:15]:
        print("   ", s)