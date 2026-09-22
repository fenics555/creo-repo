# PROGRESS SPEC 112 «Причёска репо по аудиту напарника 22.09»
НОГИ: нога 1 — Cline (локальная модель) — 22.09.2026
SPEC: D:\AI\repo\SPEC_112_tidy_repo_audit.md (verbatim сообщения пользователя)
STATUS: ЖДЁТ СЛОВА

## Ф0 ЦИТАТЫ (нога 1, Cline, 22.09.2026 ~14:00)
СДЕЛАНО (цитаты с диска):
- Length: корень SKILL_local_agent_cline.md=20175 / Prog-копия=162; корень
  SKILL_agent_protocol.md=6435 / Prog-копия=162; crash\SKILL_editor_too_large.md=3462 /
  Prog-копия=167; Prog\SKILL_unit_testing.md=5462.
- Приборы (ASCII-скрипт D:\AI\log\urn\cline\spec112_probe.py, вывод
  spec112_probe_out.txt): корень выживания = «пять точек» ×1, указателей ×0,
  YAML_OPEN=False, строка 2 = заголовок «# ВЫЖИВАНИЕ ЛОКАЛЬНОГО ИИ В CLINE (VS Code),
  редакция 21.09.2026»; Prog-копия = 1 строка, указатель ×1; Prog\SKILL_agent_protocol.md
  идентичен Prog\SKILL_local_agent_cline.md по SHA256-голове 3D6C049A113132C0 и целит
  в SKILL_local_agent_cline.md (чужой адрес); crash\SKILL_editor_too_large.md
  указателей ×0; Prog\SKILL_unit_testing.md = 55 строк, 12 заголовков, паспорт текстом.
- Test-Path: D:\AI\repo\agents = True; Creo\SKILL_creo_index.md = True.
- Мёртвые имена (visibility-скан spec112_visibility.py): SKILL_index.md — 56 токенов,
  13 мёртвых; Creo index — SKILL_crash_creoson-write-rules; .clinerules и MANIFEST —
  SKILL_trails_index (папки Трейлы нет; при этом код дома пишет в repo\Трейлы\
  TRAIL_JOURNAL.md: trail_tools.py:23, db_tools.py:47, http_handlers.py:74).
- skills_check (прогон 22.09) — 13 нарушений, из них НОВЫЕ против отчёта 20.09:
  crash_loop_perception.md (нет executor, нет поля ОШИБКА); SKILL_agent-frozen.md
  (name mismatch agent_frozen/agent-frozen, нет ОШИБКА); SKILL_crash-destructive...
  (дефис вместо подчёркивания); SKILL_crash_execution-loop.md (name mismatch, нет ОШИБКА);
  SKILL_crash_handling.md (нет executor, нет ОШИБКА); SKILL_crash_reasoning-loop.md
  (name mismatch, нет ОШИБКА); SKILL_crash_regex_..._loop.md (name mismatch);
  SKILL_editor_too_large.md (нет executor, нет ОШИБКА); crash_appjs-... (нет executor).
- git log --no-pager -2: d1bc7fd «autosave repo 22.09.2026 13:44:09,77», bcedd2a.
  Рабочее дерево чистое (status --porcelain пуст) до правок документов этой ноги.
НЕ СДЕЛАНО: Ф1-Ф5 — ждут слова пользователя; Ф1 в дословной редакции не исполнима
(см. флаги), Ф3 пересекается с существующим файлом.
ЯКОРЬ: SPEC_112_tidy_repo_audit.md и PROGRESS_spec112.md в репо; скрипты и выводы в
D:\AI\log\urn\cline\ (spec112_probe*.py/txt, spec112_visibility*.py/txt, skills_check_112.txt);
baseline skills_check обновлён прогоном.
ПЛАН: правки — только по слову пользователя; предложения этапами (1-5) — в отчёте.

## ФЛАГИ РАСХОЖДЕНИЯ СПЕКИ С ДИСКОМ (анти-сикофанство, цитаты)
1. Ф1 опасна: «корневой = yaml-шапка из корня + тело из Prog-копии минус указатель».
   Факт: YAML_OPEN=False, в корне до первого заголовка только пустая строка (HEAD3 =
   ['', '# ВЫЖИВАНИЕ...', 'Закон трёх рук...']), а тело Prog-копии = 0 строк (162 Б —
   один указатель). Дословное исполнение = корень 20175 → ~0 Б (потеря закона дома).
2. Ф1: «Prog\SKILL_unit_testing.md = первая копия до второго заголовка» — копий внутри
   нет: H@1 «# SKILL_unit_testing», H@2 «# Направление: Программирование», H@3
   «# Priority: critical» (текстовый паспорт). Обрезка = потеря файла 5462 Б.
3. Ф2: переносить нечего — SKILL_object_creoson.md отсутствует и в корне, и в Creo
   (Test-Path False/False); живое имя в папке — Creo\SKILL_object_creoson_tests-01_asm.md.
4. Ф3: Creo\SKILL_creo_index.md уже существует (1193 Б, 27 имён из 29 файлов папки) —
   «создать одним write_file» = перезапись; нужна правка 2 строк, не создание.
5. Ф5: подпись crash_pointer-with-body нарушает конституцию (подпись без имени
   инструмента запрещена для новых экземпляров) — предлагаю SKILL_crash_editor_pointer-over-body.md.

## HANDOFF
Указатель спеки: D:\AI\repo\SPEC_112_tidy_repo_audit.md; журнал: D:\AI\repo\PROGRESS_spec112.md.
СДЕЛАНО: Ф0 целиком (замеры, мёртвые ссылки, невидимые скиллы, прогон skills_check),
полный аудит-отчёт D:\AI\log\reports\REPORT_spec112_cline_20260922.md.
НЕ СДЕЛАНО: ни одной правки в репо (кроме этих двух документов) — по манифесту
удаления/переименования вне tmp = только по прямому слову пользователя.
ЯКОРЬ: см. выше; git HEAD d1bc7fd.
ГРАБЛИ: переадресация `>` в PowerShell пишет UTF-16 → чужой вывод читать
`-Encoding unicode` или писать файл питоном; skills_check проверяет ТОЛЬКО crash\.
## ПЛАН ЭТАПОВ (редакция напарника, принята ногой 1; STATUS: В РАБОТЕ)
НОРМА Э1 (слово пользователя, вариант D): удалений и переименований нет вовсе; одноимённый
указатель (162-167 Б) при живом теле = домовая норма; два одноимённых ТЕЛА = нарушение.
Э1 (2 правки): (1) Prog\SKILL_agent_protocol.md — ПОЛНАЯ перезапись одной строкой
«Закон живёт в D:\AI\repo\SKILL_agent_protocol.md; этот файл — указатель, дублирование закона
запрещено» (сейчас целит в чужой закон, SHA 3D6C049A…); (2) SKILL_index.md, секция «ЗОЛОТОЙ
СТАНДАРТ» — добавить строку нормы про указатель (verbatim из слова). Три указателя оставить.
Prog-индекс не создавать; строку долга в секции 7 заменить.
Э2 (≈8 правок SKILL_index.md): мёртвые 13 ссылок по карте ноги: живые имена —
company_conventions.md (было SKILL_company_conventions), strategy.md (было SKILL_strategy),
Creo\SKILL_object_creoson_tests-01_asm.md (было SKILL_object_creoson), Трейлы\SKILL_trails_index.md
(заживёт в Э3), SKILL_calc_script_architecture (долг переименования STANDARD…); долговые строки —
SKILL_log_management, SKILL_skill_craft, SKILL_tool_template, SKILL_architect_reviewer,
SKILL_favorites_ (родятся от memory_tools); SKILL_auto_engine/logic_flow/data_harvest —
заменить фактическим списком 7 живых файлов agents. Плюс строка регистрации
«справочники и управленческие файлы (GUIDE\db|models|plm, Vericut\, Ошибки\ERR_260902_web_fetch.md,
BACKLOG_tools.md), не скиллы, в маршрутизацию не входят».
Якоря (свежее чтение): секция 2 шапка («*Стандарты кода, тестов и памяти агента; вход
направления = эта секция,»), секция 5 строки 70-82, секция 6 строки 85-89, долги строки 113-121,
ЗОЛОТОЙ СТАНДАРТ строки 123-131, ИСТОЧНИКИ ПРАВДЫ 109-111.
Э3 (2-3 правки + команды): создать Трейлы\ и Трейлы\SKILL_trails_index.md (фронтматтер
name trails-index, system трейлы, priority critical, when: трейл, журнал, сессия, кто открывал;
три строки: живой журнал Трейлы\TRAIL_JOURNAL.md пишет trail_tools.py, руками не править;
разбор = trail_analyze/trail_diagnose; накопленные проблемы = trail_problems); папку Избранное\
создать; Creo-индекс строка 8 — мёртвый SKILL_crash_creoson-write-rules → SKILL_creoson_probe_method.
Э4 (≈10 правок): четвёрку loop НЕ сливать; добить поля по §6 конституции (ОШИБКА дословно,
executor) в SKILL_crash_reasoning-loop.md, crash_reasoning-loop.md, SKILL_crash_plan-loop-replan-no-exec.md,
crash_loop_perception.md + строку «РОДСТВО: семья loop, см. также …» перекрёстно; те же поля —
SKILL_crash_handling.md и crash\SKILL_editor_too_large.md; skills_check.py расширить на корень и
Prog с отчётом в UTF-8; после правки .py — py_compile.
Э5 (2-3 команды): git pull --rebase origin master, затем push; конфликт на файле закона
(MANIFEST, .clinerules, корневые SKILL_, crash\) = СТОП-отчёт с цитатой, авторазрешение запрещено;
конфликт вне закона — решать в пользу remote, своё поверх отдельным коммитом.
Ф-ДОП (1 правка): в корень SKILL_local_agent_cline.md вставить yaml-фронтматтер (verbatim слова:
name: local-agent-cline, system: общее, description «Use when: локальная модель ИИ работает в
VS Code / Cline…», when «Cline, локальная модель, gemma, выживание, вылет, контекст, транспорт,
редактор, run_commands, крах», priority: critical), тело не трогать ни символом; приёмка
YAML_OPEN=True и «пять точек» = 1 (anchor: заголовок строки 2, insert не по номеру).
Бумаги: этапные блоки перед «=== END ===»; STATUS В РАБОТЕ → ЗАВЕРШЕНА после Э5; отчёт
дополняется таблицей «этап → цитата»; коммит и пуш внутри Э5.

### УТОЧНЕНИЯ НОГИ К ПЛАНУ (требуют слова или подтверждения)
1. name-mismatch остаются: Э4 добивает ОШИБКА/executor, но 5 файлов сохранят расхождение
   `name:` с именем файла (SKILL_agent-frozen.md: agent_frozen/agent-frozen;
   SKILL_crash_destructive-probe-rerun.md; SKILL_crash_execution-loop.md:
   execution-loop/crash_execution-loop; SKILL_crash_reasoning-loop.md; SKILL_crash_regex_…).
   Правка поля `name:` внутри файла — не переименование, но у reasoning-loop получится имя,
   совпадающее с name в соседнем crash_reasoning-loop.md. Нужно решение: править `name:`
   или признать долг строкой.
2. Пустая папка Избранное\ в git не хранится (git не трекает пустые каталоги) — после клона её
   не будет; memory_tools создаёт её по потребности. Предложение: не создавать вовсе либо
   положить файл-заглушку.
3. Отчёт расширенного skills_check: у инструмента нет понятия исполнителя — предлагаю
   D:\AI\log\skills_check\skills_check_report.txt (правило «каждая программа пишет лог в свою
   подпапку»), а не log\urn\<исполнитель>\.
4. Проверка корня и Prog в skills_check: правила конституции (executor, ОШИБКА) к ним не
   применимы — иначе 100% ложных срабатываний (например GUIDE\*.md без фронтматтера).
   Предложение: вне crash\ проверять только наличие шапки `name:` и равенство её имени файла
   без SKILL_/.md.
5. Creo-индекс: живая замена мёртвого триггера — есть и точнее SKILL_creoson_probe_method:
   Ошибки\ERR_creoson_write_ops.md (реальный разбор ошибок записи). Предлагаю указать оба.
6. Э5: rebase при конфликте оставляет репо в состоянии rebase — план Б: `git rebase --abort`
   и СТОП-отчёт. Пуш в сеть ≤25 с не гарантирован (первая попытка отклонена по
   non-fast-forward, не по авторизации).
7. ОБЪЁМ: ≈25-30 вызовов на все этапы (>20 = передача). Предложение: нога 1 = Ф-ДОП + Э1 + Э3
   (закон и пустоты), нога 2 = Э2 + Э4, нога 3 = Э5 (синк).

## Э1 + Э3 + Ф-ДОП ВЫПОЛНЕНО (нога 1, Cline, 22.09.2026)
СТРАХОВКА (слово пользователя: архив не нужен): бекапы в data\backup — pre_spec112_SKILL_local_agent_cline.md.bak (20175), pre_spec112_SKILL_index.md.bak (10194), pre_spec112_Prog_SKILL_agent_protocol.md.bak (162), pre_spec112_Creo_SKILL_creo_index.md.bak (1193) — все Test-Path True; git HEAD до правок 98c5707.
Ф-ДОП: писатель spec112_leg1_frontmatter.py + verbatim spec112_frontmatter.txt → «body_before=20175 frontmatter=438 body_after=20614 delta=439» (тело побайтно). Проверка: LEN=20614, YAML_OPEN=True, «пять точек»=1, строк 189 (182+7).
Э1: Prog\SKILL_agent_protocol.md → LEN=159, указатель ×1, целит «в D:\AI\repo\SKILL_agent_protocol.md» (было — в чужой закон); SKILL_index.md: норма @131 («одноимённость» ×1), долг Prog-индекса закрыт @118.
Э3: Трейлы\SKILL_trails_index.md создан (572 Б, YAML_OPEN=True, name trails-index, priority critical); Creo-индекс строка 8 = «CRASH триггеры: SKILL_creoson_probe_method, Ошибки\ERR_creoson_write_ops.md» (оба адреса живы, Test-Path True); Избранное\ НЕ создавали (git не трекает пустые каталоги, папка родится memory_tools — строка обоснования в отчёте).
ГРАБЛИ НОГИ 1: правка плана съела терминатор «=== END ===» (возвращён этим блоком) — при правках PROGRESS проверять терминатор цитатой; «>» в PowerShell даёт UTF-16 в части запусков, надёжнее читать оба кодирования или писать вывод питоном.
=== END ===