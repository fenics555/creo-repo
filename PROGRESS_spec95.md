# PROGRESS_spec95.md

# SPEC 95: Resurrecting Cleaner

## STATUS: PHASE 1 COMPLETE (GREEN) ✅

### PHASE 1: Core Logic (PURGE)
**Status**: Completed
**Verification**:
- [x] `purge_versions.py` reconstruction successful.
- [x] `PurgeLock` with PID check (tasklist) and stale removal implemented.
- [x] Logging to `D:\AI\log\purge\last_purge.json` confirmed.
- [x] `creo-mode` collision handling (target busy) verified.
- [x] `creo-mode` preview/execute cycle verified.

**Citations for Phase 1 Acceptance**:
1.  "атомарной записи purge_versions.py (черновик в урне, гейт py_compile, .prev или «первая запись»)" -> **DONE** (склеен из блоков).
2.  "PurgeLock с PID и stale-снятием" -> **DONE** (lines 6-25).
3.  "purge.log и last_purge.json в D:\AI\log\purge\" -> **DONE** (lines 79-81, 134).
4.  "коллизия creo-mode f.prt.1 рядом с f.prt.2 = пропуск с причиной" -> **DONE** (lines 107-109).
5.  "второй прогон = превью пусто" -> **DONE** (verified in test).

---

## PHASE 2: Wizard UI (DESIGN & IMPLEMENTATION)
**Status**: IN PROGRESS 🏗️

**Plan**:
1.  **API Layer**: Implement `POST /wiz_purge_preview` and `POST /wiz_purge_execute` in `http_handlers.py`.
2.  **Frontend Integration**: Add "ЧИСТКА ВЕРСИЙ" block to `app.js` with "План чистки" (Preview) and "Почистить" (Execute with PENDING shield) buttons.
3.  **Execution Pattern**: Use `PENDING/do_approve` pattern for `execute` command.

**Attempts**:
- Phase 1: 0 failures.

---

**SKILLS**:
- **Used**: `python-logic-recovery`, `regex-pattern-matching`, `filesystem-walk`, `argparse-implementation`, `error-recovery-loop`.
- **To Study**: `UI-UX-Wizard-Patterns` (internal house patterns), `async-command-execution-pattern` (for detach).
