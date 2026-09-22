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
=== END ===