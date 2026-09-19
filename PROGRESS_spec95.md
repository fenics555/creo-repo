# PROGRESS_spec95.md

# SPEC 95: Resurrecting Cleaner

## STATUS: IN PROGRESS 🏗️

### PHASE 1: Core Logic (PURGE)
**Status**: Completed
**Verification**:
- [x] purge_versions.py reconstruction successful.
- [x] PurgeLock with PID check (tasklist) and stale removal implemented.
- [x] Logging to D:\AI\log\purge\last_purge.json confirmed.
- [x] creo-mode collision handling (target busy) verified.
- [x] creo-mode preview/execute cycle verified.

**Citations for Phase 1 Acceptance**:
1.  'атомарной записи purge_versions.py (черновик в урне, гейт py_compile, .prev или «первая запись»)' -> **DONE** (склеен из блоков).
2.  'PurgeLock с PID и stale-снятием' -> **DONE** (lines 6-25).
3.  'purge.log и last_purge.json в D:\AI\log\purge\' -> **DONE** (lines 79-81, 134).
4.  'коллизия creo-mode f.prt.1 рядом с f.prt.2 = пропуск с причиной' -> **DONE** (lines 107-109).
5.  'второй прогон = превью пусто' -> **DONE** (verified in test).

---

## PHASE 2: Wizard UI (DESIGN & IMPLEMENTATION)
**Status**: IN PROGRESS 🏗️

**Plan**:
1.  **API Layer**: Implement POST /wiz_purge_preview and POST /wiz_purge_execute in http_handlers.py.
2.  **Frontend Integration**: Add 'ЧИСТКА ВЕРСИЙ' block to pp.js with 'План чистки' (Preview) and 'Почистить' (Execute with PENDING shield) buttons.
3.  **Execution Pattern**: Use PENDING/do_approve pattern for execute command.

**Attempts**:
- Phase 1: 0 failures.
- Phase 2: 1 crash (readfiles_outdated_loop).

---

## SKILLS:
- **Used**: 'python-logic-recovery', 'regex-pattern-matching', 'filesystem-walk', 'argparse-implementation', 'error-recovery-loop'.
- **Studied (this leg)**: 'SKILL_local_agent_cline.md', 'SKILL_crash_constitution.md', 'SKILL_crash_readfiles_outdated_loop.md'.
- **To Study**: 'UI-UX-Wizard-Patterns', 'async-command-execution-pattern'.

## HANDOFF
=== ПЕРЕДАЧА ЭСТАФЕТЫ, спека 95, нога текущая закрывается, нога следующая стартует ===
[SPEC 95: Resurrecting Cleaner - Implement atomic version purging with Wizard UI]
[КОМПАКЦИЙ В НОГЕ]: 0 из 3
[СДЕЛАНО] (с цитатами):
- [x] Phase 1 complete (verified).
- [x] Phase 2 Backend Setup (purge_tools.py, panel.py).
- [x] Infrastructure: Created 'SKILL_crash_readfiles_outdated_loop.md'.
[НЕ СДЕЛАНО]:
- [ ] Pattern discovery in 'app.js' (searching for wizard/modal patterns).
- [ ] API Implementation in 'http_handlers.py'.
- [ ] UI Implementation in 'app.js'.
[ЯКОРЬ СЛЕДУЮЩЕГО ШАГА]:
- 'D:\AI\tools\agent\ui\app.js' (analyze for modal/wizard patterns).
- 'D:\AI\tools\agent\http_handlers.py' (implement endpoints).
[ГРАБЛИ]:
- 'crash_readfiles_outdated_loop' (loop on 'read_files' returning 'outdated').
[СЧЁТЧИКИ НОГИ]:
- Вызовов потрачено: ~15
- Файлов изменено: 3
- Бекапов создано: 0
=== КОНЕЦ ПЕРЕДАЧИ ===
