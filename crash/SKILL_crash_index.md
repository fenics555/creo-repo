---
name: crash-index
system: CRASH
description: Список всех крах-скиллов папки crash (навигация); вход в тему — SKILL_crash_constitution.md
when: крах, crash, список крахов, какой скилл, навигация по крахам
priority: high
date: 22.09.2026
---
# СПИСОК КРАХ-СКИЛЛОВ (D:\AI\repo\crash)
Вход/закон темы — `SKILL_crash_constitution.md` (правило, шаблон экземпляра, шаблон передачи, блок имён).
Ниже — все экземпляры с кратким «когда применять». Счётчик повторов (`ПОВТОРЫ`) — внутри каждого скилла.

- `SKILL_agent-frozen` — Use when: Агент (HTTP-сервис) «застыл» — порт 8765 слушает (LISTENING), но curl/requests возвращают «Connection closed without response» или «Timeout»; процесс есть, но не реагирует на запросы.
- `SKILL_crash-editor-mismatch` — Use when: editor падает с «text not found» из-за расхождения old_text после частичной правки или смены контекста
- `SKILL_crash_agent-duplicate-restart-race` — Use when: после рестарта агента живы ДВА python agent.py и на порту два LISTENING — рестарт среагировал в гонке со сторожем ctl --watch
- `SKILL_crash_agent_corruption` — Use when: агент после рестарта молчит/отвечает старым кодом, `py_compile` правленого `agent.py` падает (SyntaxError)
- `SKILL_crash_agent_silence` — Use when: исполнитель «завис» — сообщение кончилось рассуждением без вызова инструмента, IDE видит простой, пользователь спрашивает «что случилось» или «ты стоял»
- `SKILL_crash_analysis_search_codebase` — Use when: search_codebase падает с ошибкой миграции контекста или повторяется
- `SKILL_crash_cline_longsession_context_death` — Use when: окно Cline умирает молча после длинной сессии на шаге генерации длинного ответа
- `SKILL_crash_command-30s-timeout` — Use when: run_commands падает с "Command timed out after 30000ms" — таймаут
- `SKILL_crash_constitution` — ЗАКОН темы (не экземпляр): правило, шаблон экземпляра, шаблон передачи, блок имён.
- `SKILL_crash_context-limit-interruption` — Use when: задача прерывается из-за лимитов инструментов (search_codebase, контекст) или таймаутов
- `SKILL_crash_ctl-inline-stderr-truncated` — Use when: рестарт или проба агента через инлайн python -c в PowerShell гибнет
- `SKILL_crash_destructive-probe-rerun` — Use when: разрушительная проба (kill_creo, delete, erase, перезапись) исполнена ПОВТОРНО из оставшегося в tmp скрипта
- `SKILL_crash_editor-text-not-found` — Use when: editor не находит точный old_text, хотя при чтении текст совпадает
- `SKILL_crash_editor_context_mismatch` — Use when: editor падает из-за несовпадения текста или лимита размера при крупных правках
- `SKILL_crash_editor_too_large_and_non_unique_anchors` — Use when: editor падает из-за размера файла > 6 КБ или нескольких совпадений old_text
- `SKILL_crash_execution-loop` — Use when: агент зацикливается в попытках исправить ошибку, повторяя одну и ту же неудачную команду или используя несоответствующий инструмент (например, слишком сложный python -c в PowerShell).
- `SKILL_crash_handling` — Use when: петля или зависание из-за лимитов инструментов (editor too large, длинные цепочки run_commands, editor без old_text)
- `SKILL_crash_login-stale-memory` — Use when: вход в агента не проходит при верном пароле — три источника правды
- `SKILL_crash_missing-temp-artifacts` — Use when: временные артефакты tmp потеряны к моменту, когда нужны следующему шагу
- `SKILL_crash_omission_of_revive_protocol` — Use when: пропуск обязательных шагов ритуала (чтение скилла и строка-доказательство) при REVIVE или крахе
- `SKILL_crash_pdf-roots-two-lists` — Поиск PDF пуст при живых парах в базе знаний (сравнение scan_roots и kb_roots)
- `SKILL_crash_plan-loop-replan-no-exec` — один и тот же план три и более раз в рассуждениях без исполнения
- `SKILL_crash_protocol_omission` — Use when: пропуск обязательной записи крах-скилла — ритуал краха выполнен частично
- `SKILL_crash_quoted-escape-parse-failure` — ParseException «Отсутствует имя типа после знака "["» на \" внутри массива run_commands
- `SKILL_crash_readfiles_outdated_loop` — Use when: `read_files` в цикле возвращает `[outdated - see the latest file content]`
- `SKILL_crash_reasoning-loop` — указатель: закон и профилактика в `SKILL_crash_plan-loop-replan-no-exec.md` (дублирование запрещено)
- `SKILL_crash_regex_extraction_triple_quote_loop` — Use when: бесконечный цикл при regex-извлечении блоков кода в тройных кавычках (agent.py)
- `SKILL_crash_runcommands-copy-race-fake-parameter` — Use when: после Copy-Item мгновенный Get-Content падает PathNotFound (гонка
- `SKILL_crash_runcommands_kill-by-name-house-services` — Use when: остановка процесса по ИМЕНИ (Stop-Process -Name / taskkill /IM) в доме — сносит ЧУЖИЕ сервисы дома
- `SKILL_crash_scheduler-fire-skip` — Use when: задача планировщика с триггером повторения не стартует в расчётный
- `SKILL_crash_searchcodebase-any-pattern-migration-marker` — Use when: search_codebase возвращает маркер миграции
- `SKILL_crash_searchcodebase-multipattern-migration-marker` — Use when: search_codebase с 3+ regex-паттернами возвращает маркер миграции
- `SKILL_crash_searchcodebase-timeout` — Use when: search_codebase зависает/таймаут или возвращает маркер миграции вместо результатов
- `SKILL_crash_session-interruption` — Use when: потеря сессии, обрыв связи, генерация оборвана на полуслове
- `SKILL_crash_sleep-poll-loop-after-timeout` — Use when: исполнитель после таймаута run_commands (30 с) ждёт детач-процесс повторными опросами «Start-Sleep 25 + проверка файла» — и зацикливается на 5+ одинаковых ходах вместо смены метода и отчёта. Закон дома — MANIFEST.md (М7, М10).
- `SKILL_editor_too_large` — Use when: editor отказывает «Editor input too large» — блок new_text выше лимита (~6000 символов)
- `crash_appjs-syntaxerror-no-uicheck` — Use when: правка app.js/index.html ушла без пробы консоли — синтаксическая ошибка живёт до первой проверки
- `crash_deleted-house-file-without-word` — Use when: домовой файл (напр. harvest_gui.py) удалён вне data	mp и dataackup без прямого слова пользователя
- `crash_loop_perception` — Use when: исполнитель принимает череду мелких нужных шагов (инвентаризация, Select-String, проверки путей) за цикл и встаёт в REVIVE без реального зависания
- `crash_reasoning-loop` — Use when: исполнитель зацикливается на повторяющихся неудачных вызовах/рассуждениях без продвижения
- `SKILL_crash_editor-create-overwrote` — Use when: create/полная перезапись существующего файла убила тело (файл усох, 4256 → 1100 байт)
- `SKILL_crash_git_commit-sweeps-foreign-staged` — Use when: git commit без pathspec подметает чужой staged параллельной ноги
- `SKILL_crash_git_parallel-leg-rebase-reverts-worktree` — Use when: параллельная нога сделала rebase — рабочее дерево откатилось, своя работа в stash
- `SKILL_crash_loop_economy_failure` — Use when: исполнитель зацикливается из-за попыток «оптимизировать» (экономить) токены вместо полноценного чтения скиллов или соблюдения лимитов инструментов (например, editor too large), что приводит к ложным выводам и краху сессии.
- `SKILL_crash_editor-studycheck-halfedit-undefined-name` — Use when: файл после правки ссылается на необъявленное имя (NameError) — правка оборвана до объявления имени и до прогона проверки; и сопутствующее: вывод проверки с эмодзи роняет консоль cp1251 (UnicodeEncodeError 'charmap').
- `SKILL_crash_update-version-mismatch` — Use when: после обновления шапка новая, а «есть обновление» не гаснет — версия живёт в двух местах (`engine.VERSION` рядом с `APP_VERSION`), и/или манифест тянется по кэшируемому raw вместо GitHub API.

- `crash_git-push-says-up-to-date-but-ahead` — Use when: `git push` пишет «Everything up-to-date», но `git rev-list --left-right --count origin/master...HEAD` показывает ahead — пуш НЕ состоялся; приёмка только по `ls-remote` + нулям.
- `crash_shell-mixed-cmd-and-powershell` — Use when: `cmd /c '... && git ... 2>&1 | Select-Object ...'` падает с «'Select-Object' is not recognized» — PowerShell-командлет внутри cmd.exe; пуш при этом НЕ выполнился, а exit 1 выглядит как провал git.
- `SKILL_crash_strict_test_stamp-missing` — Use when: проверка `strict_test.py` проходит все вопросы, но отчёт не пишется — `NameError: name 'STAMP' is not defined` в разделе отчёта.
- `crash_path-guessed-by-analogy` — Use when: путь к папке назван по аналогии с соседней (`tools\agent` рядом есть и тоже «про агента»), и `cd` падает `PathNotFound`, хотя папка живёт в другом месте — `Test-Path` до команды, адрес брать из `CULTURE_files.md` §1.
- `SKILL_crash_ollama-ansi-stderr-falseexit` — Use when: `ollama stop/rm/create/ps` даёт ложный `NativeCommandError`/exit1 из-за ANSI-спиннера в stderr и рвёт цепочку `;` — успех проверять по `ollama list`/HTTP, а не по exit-коду PowerShell.

- `crash_bat_no_dry_run_flag` — Use when: лаунчер `.bat` запускается без ключа пробы/`--dry` и сразу делает необратимое действие (в индексе отсутствовал, внесён 02.10.2026).

- `SKILL_crash_creoson-search-pro-visibility` — Use when: CREOSON отказывает в открытии модели (`Unknown Model Extension`) при верном существующем пути; причина — папки нет в списке `Z:\PTC\Work\search.pro` (4109 папок), а не «видимость START-STD» и не «2 уровня» (оба утверждения опровергнуты).
- `SKILL_crash_creoson-open-prt1-extension` — Use when: `file:open` отвечает `Unknown Model Extension` при верном пути — чаще всего передан `имя.prt.1` вместо `имя.prt`; для чтения байтов путь с `.1` нужен, для API — без.
- `SKILL_crash_creo-text-not-binary` — Use when: в `.prt`/`.asm` ищешь фичи или компоненты по бинарным сигнатурам — заголовок UGC на самом деле открытый текст (`#UGC:2`, `@тег N L`, `E0 <len> поле\0`); сначала напечатать 2 КБ как текст, потом искать по ИМЕНАМ полей (`to_name`, `comp_ids`), а не по маркерам.
- `crash_command_timeout_kills_process_tree` — Use when: `Start-Process cmd /c <лаунчер>` и таймаут рвёт всё дерево процессов вместе с результатом.
- `crash_python_open-number-invalid-handle` — Use when: `open()` в Python получает номер как дескриптор (`OSError: Invalid argument` / `TypeError`).
- `crash_update-test-self-overwrite` — Use when: проверка обновления пишет поверх сравниваемого файла и «проходит» сама у себя.

Всего крах-скиллов: 54 (без учёта конституции и этого списка; сверено пересчётом файлов 02.10.2026, в индексе до этого стояло 49 — пять скиллов были не посчитаны).
