---
name: crash-index
system: CRASH
description: Навигатор по всем крах-скиллам папки D:\AI\repo\crash по группам; вход и закон темы — SKILL_crash_constitution.md
when: крах, crash, список крахов, какой скилл, навигация по крахам, подпись краха
priority: high
date: 13.11.2026
executor: Cline
---

# СПИСОК КРАХ-СКИЛЛОВ (D:\AI\repo\crash)

**Закон и шаблоны темы:** `SKILL_crash_constitution.md` (порядок фиксации, шаблон экземпляра, шаблон передачи, правило именования).
**Порядок работы при сбое:** найди свою подпись в группах ниже → прочитай файл → если подпись совпала, увеличь `ПОВТОРЫ` и примени профилактику; если подпись новая — создай новый файл по шаблону из конституции.
**Актуальный состав папки (на 13.11.2026):** 70 файлов (`SKILL_crash_constitution.md` + `SKILL_crash_index.md` + 68 экземпляров). Точный пересчет — только счетчиком с диска.

---

## 1. Редактор файлов (`editor` / `write_file`) — 9 шт.
*   `SKILL_crash-editor-mismatch` — `editor` падает с `text not found` из-за расхождения `old_text` после частичной правки или смены контекста.
*   `SKILL_crash_editor-text-not-found` — `editor` не находит точный `old_text`, хотя при чтении текст совпадает.
*   `SKILL_crash_editor_context_mismatch` — `editor` падает из-за несовпадения текста или лимита размера при крупных правках.
*   `SKILL_crash_editor_too_large_and_non_unique_anchors` — `editor` падает из-за размера блока > 6 КБ или нескольких совпадений `old_text`.
*   `SKILL_editor_too_large` — `editor` отказывает с `Editor input too large` (блок `new_text` выше лимита ~6000 символов).
*   `SKILL_crash_editor-split-loses-indent` — файл собран вставками по 5–6 КБ и падает с `IndentationError` на шве между частями.
*   `SKILL_crash_editor-insert-line-splits-function` — вставка по номерам строк попадает внутрь функции и ломает отступы.
*   `SKILL_crash_editor-studycheck-halfedit-undefined-name` — правка оборвана до объявления имени (`NameError`) или вывод с эмодзи роняет консоль cp1251 (`UnicodeEncodeError`).
*   `SKILL_crash_editor-create-overwrote` — полная перезапись существующего файла уничтожила его тело (файл усох).

---

## 2. Консоль и процессы (`run_commands` / PowerShell / Python) — 9 шт.
*   `SKILL_crash_command-30s-timeout` — `run_commands` падает с `Command timed out after 30000ms`.
*   `crash_command_timeout_kills_process_tree` — `Start-Process cmd /c` и таймаут рвут всё дерево процессов вместе с результатом.
*   `SKILL_crash_ctl-inline-stderr-truncated` — рестарт или проба через инлайн `python -c` в PowerShell гибнет с обрезанным stderr.
*   `SKILL_crash_quoted-escape-parse-failure` — `ParseException` на кавычках `\"` внутри `run_commands`.
*   `crash_shell-mixed-cmd-and-powershell` — PowerShell-командлет (`Select-Object`) запущен внутри `cmd /c` и падает без исполнения команды.
*   `SKILL_crash_runcommands-copy-race-fake-parameter` — после `Copy-Item` мгновенный `Get-Content` в той же пачке падает с `PathNotFound` (гонка).
*   `SKILL_crash_runcommands_kill-by-name-house-services` — остановка процесса по имени (`Stop-Process -Name` / `taskkill /IM`) сносит чужие сервисы дома.
*   `crash_python_open-number-invalid-handle` — `open()` в Python получает число вместо пути (`OSError: Invalid argument` / `TypeError`).
*   `SKILL_crash_sys-stdout-closed-on-import` — проба падает с `ValueError: I/O operation on closed file` после переопределения `sys.stdout` при импорте.
*   `SKILL_crash_mass-replace-swapped-pairs` — инверсия пар при массовой замене скриптом без dry-run (п. 4.9).

---

## 3. Циклы, петли и зацикливание — 9 шт.
*   `SKILL_crash_agent_loops_17.10.2026` — разбор усталости ноги и серии петель (промахи якорей подряд, повтор запуска тем же методом, ложная тревога).
*   `SKILL_crash_execution-loop` — зацикливание на повторе одной и той же неудачной команды или неподходящего инструмента.
*   `SKILL_crash_loop_economy_failure` — петля из-за попыток «экономить» токены вместо чтения скиллов или соблюдения лимитов инструментов.
*   `SKILL_crash_plan-loop-replan-no-exec` — один и тот же план 3+ раза в рассуждениях без вызова инструментов.
*   `SKILL_crash_reasoning-loop` — указатель на `SKILL_crash_plan-loop-replan-no-exec.md` (дублирование запрещено).
*   `crash_reasoning-loop` — зацикливание на повторяющихся неудачных вызовах и рассуждениях без продвижения.
*   `crash_loop_perception` — исполнитель принимает череду нужных мелких проверок за цикл и встаёт в `REVIVE` без реального зависания.
*   `SKILL_crash_sleep-poll-loop-after-timeout` — после таймаута 30 с исполнитель зацикливается на опросах `Start-Sleep 25 + проверка файла` вместо отчёта.
*   `SKILL_crash_readfiles_outdated_loop` — `read_files` в цикле возвращает `[outdated - see the latest file content]`.

---

## 4. Поиск по кодовой базе (`search_codebase`) — 4 шт.
*   `SKILL_crash_analysis_search_codebase` — `search_codebase` падает с `[migration] Tool result missing` в длинной сессии.
*   `SKILL_crash_searchcodebase-any-pattern-migration-marker` — `search_codebase` при любом числе паттернов возвращает маркер миграции (индекс нестабилен).
*   `SKILL_crash_searchcodebase-multipattern-migration-marker` — `search_codebase` с 3+ regex-паттернами (или в большой пачке вызовов) обрезает ответ маркером миграции.
*   `SKILL_crash_searchcodebase-timeout` — `search_codebase` зависает по таймауту или возвращает пустоту.

---

## 5. Git и параллельная работа — 3 шт.
*   `SKILL_crash_git_commit-sweeps-foreign-staged` — `git commit` без pathspec подметает чужой staged параллельной ноги.
*   `SKILL_crash_git_parallel-leg-rebase-reverts-worktree` — параллельная нога сделала rebase, рабочее дерево откатилось, своя работа ушла в stash.
*   `crash_git-push-says-up-to-date-but-ahead` — `git push` пишет `Everything up-to-date`, но ветка всё ещё `ahead` от `origin/master`.

---

## 6. Creo, CREOSON и чтение моделей — 5 шт.
*   `SKILL_crash_creoson-open-keeps-other-model` — `file:open` по полному пути не переключает окно, запись уходит в открытую модель с тем же именем.
*   `SKILL_crash_creoson-search-pro-visibility` — `Unknown Model Extension` при верном пути: папки нет в списке `Z:\PTC\Work\search.pro`.
*   `SKILL_crash_creoson-open-prt1-extension` — `file:open` падает, если передано имя с версией `.prt.1` вместо `.prt`.
*   `SKILL_crash_creo-text-not-binary` — поиск фич и компонентов бинарными сигнатурами вместо чтения текстового заголовка `#UGC:2` и имён полей.
*   `SKILL_crash_pdf-roots-two-lists` — поиск PDF пуст при живых парах в базе знаний (расхождение `scan_roots` и `kb_roots`).

---

## 7. Автономный Python-агент (порт 8765) и Ollama — 7 шт.
*   `SKILL_agent-frozen` — HTTP-сервис на порту 8765 слушает (`LISTENING`), но не отвечает на запросы (`Timeout` / `Connection closed`).
*   `SKILL_crash_agent-duplicate-restart-race` — после рестарта запущены два процесса `python agent.py` в гонке со сторожем `ctl --watch`.
*   `SKILL_crash_agent_corruption` — после рестарта агент отвечает старым кодом или падает с `SyntaxError`.
*   `SKILL_crash_agent_silence` — исполнитель закончил ход рассуждением без вызова инструмента и встал в простой.
*   `SKILL_crash_agent_silent-death_noport-8765` — процесс агента молча завершился без записи ошибки в журнал, порт 8765 закрыт.
*   `SKILL_crash_login-stale-memory` — вход в агента не проходит при верном пароле из-за рассинхрона источников.
*   `SKILL_crash_ollama-ansi-stderr-falseexit` — `ollama stop/rm/create/ps` печатает ANSI-спиннер в stderr, вызывая ложный `NativeCommandError` в PowerShell.

---

## 8. Контекст Cline, сессии и протокол — 8 шт.
*   `SKILL_crash_cline_longsession_context_death` — окно Cline молча обрывается после длинной сессии при генерации большого ответа.
*   `SKILL_crash_context-limit-interruption` — задача прерывается из-за переполнения контекста или лимитов инструментов.
*   `SKILL_crash_session-interruption` — внезапный обрыв связи или генерации на полуслове.
*   `SKILL_crash_omission_of_revive_protocol` — пропуск обязательных шагов диагностики при получении сигнала `REVIVE` или крахе.
*   `SKILL_crash_protocol_omission` — пропуск обязательной записи или обновления счётчика в базе крахов.
*   `SKILL_crash_chatloop_reports-inventwork-not-pettles` — исполнитель выдумывает лишнюю работу вместо честного отчёта «задача завершена».
*   `crash_path-guessed-by-analogy` — путь к папке придуман по аналогии с соседней и падает с `PathNotFound`.
*   `crash_deleted-house-file-without-word` — домовой файл удалён вне `tmp` и `backup` без прямого слова пользователя.

---

## 9. Пробы, тесты, GUI и обновления — 13 шт.
*   `SKILL_crash_destructive-probe-rerun` — разрушительная проба (`kill_creo`, `delete`, перезапись) запущена повторно из старого скрипта в `tmp`.
*   `SKILL_crash_missing-temp-artifacts` — временные файлы в `tmp` потеряны к моменту следующего шага.
*   `SKILL_crash_probe-buffer-swallows-output` — фоновый прогон Python при таймауте оставляет пустой файл перенаправления из-за буферизации вывода.
*   `SKILL_crash_probe-dialog-hang-and-pollutes-settings` — автопрогон окна зависает на модальном `messagebox` или портит боевые настройки программы.
*   `SKILL_crash_gui-helper-returns-wrong-type` — окно `tkinter` зависает после подключения к общему каркасу `ui_common`.
*   `SKILL_crash_strict_test_stamp-missing` — проверка `strict_test.py` падает при записи отчёта с `NameError: name 'STAMP' is not defined`.
*   `SKILL_crash_regex_extraction_triple_quote_loop` — бесконечный цикл при извлечении блоков кода в тройных кавычках регулярным выражением.
*   `SKILL_crash_handling` — петля из-за превышения лимитов инструментов или длинных цепочек команд.
*   `SKILL_crash_scheduler-fire-skip` — задача планировщика с триггером повторения не стартует в расчётное время.
*   `SKILL_crash_update-version-mismatch` — версия обновления не гаснет из-за расхождения `engine.VERSION` и `APP_VERSION` или кэша GitHub.
*   `crash_appjs-syntaxerror-no-uicheck` — синтаксическая ошибка в `app.js`/`index.html` ушла без проверки в headless-браузере.
*   `crash_bat_no_dry_run_flag` — лаунчер `.bat` запущен без ключа пробы и сразу выполнил необратимое действие.
*   `crash_update-test-self-overwrite` — проверка обновления перезаписывает эталонный файл сама собой.

=== END ===
