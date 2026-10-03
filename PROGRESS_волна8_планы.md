# PROGRESS SPEC 08 «ВОЛНА 8 — ПЛАНЫ ЗАДАЧ plan.json → plan_run»
НОГИ: нога 1 — Cline — 03.10.2026 (приёмка эстафеты волн 6–7, затем волна 8);
      нога 2 — Cline — 03.10.2026 (волна 11: генератор PROGRAM_REGISTRY.md)
SPEC: `D:\AI\ПРОЕКТ_ОБНОВЛЕНИЕ_АГЕНТА\спеки\05_СПЕКА_ВОЛНА8_ПЛАНЫ.md` (локальная папка, вне гита)
STATUS: ВОЛНА 8 ЗАКРЫТА (хвост — блокер JVM CREOSON, ждёт решения владельца); ВОЛНА 11 ЗАКРЫТА (реестр генерируется, расхождений 0)

## Ф1 ИНСТРУМЕНТ plan_run (волна 8, этап 6 плана) — ЗАКРЫТА
СДЕЛАНО (с цитатами):
- `agent\plan_run\plan_fmt.py` (182 стр.) — единый формат плана: `n · what · where ·
  args · risk · rollback · verdict`; `validate()` отвергает битый план (чужая версия,
  шаг без `where`/`rollback`, неизвестный риск); `from_batch_params()` — первый
  носитель формата (план batch_params).
- `agent\plan_run\runner.py` — исполнение по шагам: согласие RC 3, СТОП ПЕРВЫМ,
  журнал `D:\AI\log\plans\plan_run.log`, честный отказ RC 2 без CREOSON, щит RC 4,
  диспетчер `exec_step` по полю `what` (`set_param`, `rename_model`).
- `agent\plan_run\gui.py` + `plan_run_gui.bat`, `tool.json` (класс Ж), `README.md`
  (с блоком «С чего начать новой ноге» и контрактами), `run.bat`.
- `agent\plan_run_tools.py` — `plan_build`, `plan_run`, `plan_report`.
- `agent\dev\vol8_check.py`, `dev\vol8_live.py`, `dev\vol8_live_rename.py`.

ЖИВАЯ ЗАПИСЬ ДОКАЗАНА (`dev\vol8_live.py`, 15 критериев, 0 провалов):
`vol8_probe.prt.3` содержит `VOL8_PLAN = plan_run_2026_10_03`; откат вернул `.4`
к 102 параметрам без следов. Запись шла через САМ `runner.run_plan`.

ДЕФЕКТЫ, НАЙДЕННЫЕ ЖИВОЙ ПРОБОЙ (все закрыты):
1. `apply.py::ensure_active::norm_dir` съедал настоящий диск (`d:d:/x` → `:/x`);
2. `set_param` получал стем без расширения — `Error: Invalid File Name`;
3. `parameter:set` менял только сессию — без `file:save` на диске пусто;
4. ложный успех rename — отказ не содержит слов «ошибка»;
5. `rename_tools` принимал только имя и рабочую папку (правка `c1fcbae`).

ПРИЁМКИ: волны 1–8 RC 0 · `checks.py` 11/11, 351 объект, 100 % · `win_check` 0
провалов, окон 8 · `skills_check` violations=0.
КОММИТЫ: `tools` `63bae9b` (моя правка) и `c1fcbae` (autosave), запушены,
ahead=0 behind=0.

НЕ СДЕЛАНО:
- **живая запись `rename_model`** — внешний блокер: CREOSON падает на JVM.
  `setvars.bat` → `JAVA_HOME=D:\AI\Java` = Temurin 25.0.4 LTS, CREOSON 3.0.2
  (jars 2023) несовместим. Цитата из `hs_err_pid24868.log`:
  `#  EXCEPTION_ACCESS_VIOLATION (0xc0000005)` и
  `java/lang/NoSuchMethodError: DirectMethodHandle$Holder.invokeStaticInit`.
  Решение (JDK 8/11 или обновление CREOSON) — за владельцем.
- реестр-генерация `PROGRAM_REGISTRY.md` (волна 11), витрина — по запрету.

ЯКОРЬ: код `D:\AI\tools\agent\plan_run\`; отчёт
`D:\AI\log\reports\REPORT_волна8_планы_2026-10-03.md`; эстафета
`D:\AI\ПРОЕКТ_ОБНОВЛЕНИЕ_АГЕНТА\эстафеты\ЭСТАФЕТА_волна8_2026-10-03.md`;
копия-доказательство `D:\AI\PROBA\vol8_copy` (не удалять без слова владельца);
стек погашен (`parametric` нет, 8080 — 0 LISTENING).

## Ф2 ВОЛНА 11 — ГЕНЕРАТОР `PROGRAM_REGISTRY.md` (Cline, 03.10.2026, 22:0x)
СДЕЛАНО:
- **Проверено и опровергнуто** утверждение эстафеты волны 8 («в витрине список программ
  пуст»): живая проба `probe_prog_list.py` дала `groups: 4, programs: 23`, список полный.
- Настоящий долг: таблица «Программы» в `dev\PROGRAM_REGISTRY.md` была рукописной и
  не знала программ волн 2–8.
- `agent\dev\gen_registry.py` (161 стр.) — генератор таблицы из контрактов `tool.json`
  и `data\programs.json`, закон «не выдумывать», расхождения источников отдельным разделом.
- Маркеры `REGISTRY:BEGIN/END` в реестре; ручная таблица сохранена как «Снимок 03.10.2026».
- `agent\dev\README.md` дописан (строки `gen_registry.py`, `PROGRAM_REGISTRY.md`).
- **ХВОСТ ВОЛНЫ 11 ЗАКРЫТ по слову владельца «доделывай всё»:** 15 расхождений → **0**.
  Добавлены 5 записей в `data\programs.json` (`batch_params`, `drawing_audit`, `hol_check`,
  `plan_run`, `rules` — всего 28 программ); создан контракт `excel\tool.json`
  (контрактов 19, проблемных 0); остальным 9 записям помечено поле
  `"contract": "не полагается (...)"` — движки агента и снятые с диска legacy; генератор
  это поле учитывает. ⚠️ `data\programs.json` **не в гите** (`agent\.gitignore: data/`),
  поэтому правка витрины остаётся на этой машине — в общий репозиторий идёт реестр.
- ПРИЁМКИ (полный регресс, все RC 0): vol1–vol8 · `tool_contract` 19/0 · `checks.py`
  (все проверки пройдены, `registry_contracts` замечаний 0) · `win_check` провалов 0 ·
  `skills_check` violations=0 · `gen_registry --write` ×2 («НЕТ СМЕНЫ») · живая проба
  `prog_list`: groups 4, programs 28.
- Коммиты: `tools` `6fd6e63` запушен (ahead 0 behind 0); `excel\tool.json` и правка
  `programs.json` попали в autosave `71bc7fd`.
НЕ СДЕЛАНО:
- `ui\app.js` не тронут — запрет волны 8 в силе; данные витрины теперь полны.
- живая запись `rename_model` — по-прежнему блокер JVM (решение владельца: JDK 8/11).
ЯКОРЬ: `D:\AI\tools\agent\dev\gen_registry.py`, `dev\PROGRAM_REGISTRY.md`,
`data\programs.json` (28 программ, `updated 03.10.2026`), отчёт
`D:\AI\log\reports\REPORT_волна11_реестр_программ_2026-10-03.md`.
КРАХ ПО ХОДУ (зарегистрирован, вылечен): `patch_contracts_note.py` вставил в JSON
значение с одиночным слэшем (`dev\`) → `JSONDecodeError: Invalid \escape`, причём записал
файл ДО проверки. Счётчик `crash_quoted-escape-parse-failure` 1 → 2 + две строки
профилактики (проверять JSON до записи; удваивать слэш в данных для JSON).
ГРАБЛИ: эстафеты переписывают симптомы — сначала проба, потом починка; `re.sub` ломается
на `<!--` в результате (нужен `lambda`); правку файла на 160+ строк собирать тремя вызовами.

## HANDOFF
Спека: `05_СПЕКА_ВОЛНА8_ПЛАНЫ.md`. Сделано: инструмент `plan_run` (формат,
исполнитель, окно, контракт, README, три инструмента агента, приёмка, живая
запись доказана). Не сделано: живая запись `rename_model` (блокер JVM, решение
владельца). Якорь и приёмки — в отчёте. Грабли: успех проверять по файлу на
диске; `parameter:set` без `save` — тишина; числа приёмок протухают каждый ход;
`editor` отвергает блок >6000 Б; `cd /d` не работает в PowerShell; `read_files`
не открывает пути с кириллицей; JVM-краш выглядит как «сервис погас» —
читать `hs_err_pid*.log`.

=== END ===
