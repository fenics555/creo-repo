---
name: creoson-workflow
system: Creo
description: Use when: практическая работа в CREOSON от начала до конца — подключение, рабочие папки и ПЕРЕКЛЮЧЕНИЕ, открытие/закрытие, чтение/запись, ограничения среды
when: creoson, workflow, connect, sessionId, creo:pwd, creo:cd, file:open, file:erase, переключение, рабочая папка, вывод команд
priority: critical
date: 22.09.2026
---
# CREOSON: ПОЛНЫЙ РАБОЧИЙ ЦИКЛ (как работать и переключаться)
Спутники: `SKILL_creoson_complete.md` (карта API), `SKILL_creoson_sessions_workdirs.md`
(сессии и папки, живые пробы), `SKILL_creo_commands.md` (быстрый выбор команды),
`SKILL_creoson_write_rules.md` (пишущие), `SKILL_creoson_rename_mechanism.md`,
`SKILL_copy_assembly_project.md` (копия проекта).

## 1. Канал и ручка сессии
- Эндпоинты: `POST http://127.0.0.1:8080/creoson` (JSON) и `/server`; порт дома 8080
  (creoson 3.0.2, JRE Java 25 — штатный).
- ПЕРВЫЙ вызов — `connection:connect {}` → `sessionId` (верхний уровень ответа, НЕ в `data`).
  Далее `sessionId` кладётся в КАЖДЫЙ запрос на верхний уровень.
- Ответ: `{"status":{"error":false},"data":{...}}` либо `{"status":{"error":true,"message":"..."}}`.
- Ошибка со словом session → новый `connection:connect` и повтор.

## 2. Рабочие папки и ПЕРЕКЛЮЧЕНИЕ
- `creo:pwd` → `{"dirname":"..."}` (в старых сборках data бывает строкой И словарём — обрабатывать оба).
- `creo:cd {dirname}` → меняет рабочую папку. НЕ перепривязывает уже загруженные модели.
- `creo:list_files {filename:"*маска*"}` → файлы рабочей папки. Параметр называется
  `filename` (НЕ `file`!); без параметра/с `"*"` — все; с `"*.asm"` — только сборки.
- `creo:list_dirs {dirname}` → подпапки рабочей папки.
- `server:pwd` — только на эндпоинте `/server`; рабочая папка самого creoson (от сессии не зависит).
- К КАКОМУ Creo прицеплен сервер — сверять `creo:pwd` + `file:list` с ожиданием.

## 3. Модели: открыть / показать / выгрузить
- `file:list` → модели, открытые в сессии (источник истины по сессии).
- `file:open {file, dirname?, display}` → загрузить; `display:true` — показать окно.
- `file:get_fileinfo {file}` → `dirname` + `revision` (путь приходит с УДВОЕННЫМ диском `D:D:\...`).
- `file:display` / `file:close_window` / `file:erase`.
- `file:erase {file}` — выгрузить. `file:erase_not_displayed` сессию ПОЛНОСТЬЮ не чистит —
  нужен цикл `file:erase` по `file:list`.
- `file:save {file}` → пишет НОВУЮ версию `name.ext.N` (не перезапись).
- ⚠ `file:open` по имени, уже загруженному в сессию, отдаёт модель ИЗ ПАМЯТИ (одноимённая
  копия в другой папке это НЕ перебивает).

## 4. Чтение (безопасно на сессии инженера)
`parameter:list`, `file:massprops`, `file:relations_get`, `bom:get_paths`, `drawing:list_models`,
`file:has_instances`, `file:list_instances`, `familytable:list_tree`, `creo:get_config`.

## 5. Запись (осторожно; в доме — в полигоне или по слову)
`file:rename {file,new_name,onlysession:true}`, `file:save`, `file:backup {file,target_dir}`
(требует ОТКРЫТУЮ модель: `File '<name>' was not open.`), `parameter:set`, `file:relations_set`,
`interface:export_pdf`, `interface:export_image` (filename БЕЗ пути с `:`; модель показать).

## 6. Переименование и копия (кратко)
- Rename — только `onlysession:true` → `file:save` (дисковый `file:rename` = General Error).
  См. `SKILL_creoson_rename_mechanism.md`.
- Копия проекта (сборка+детали+чертежи+спутники+семейства) — `SKILL_copy_assembly_project.md`.

## 7. Ограничения среды (живые факты 22.09.2026)
- Один creoson = ОДИН Creo. При 2+ запущенных Creo свежий creoson на `connect` возвращает
  `Unable to connect to Creo; more than one instance of Creo is running` и роняет JVM (`hs_err`).
  Уже привязанный creoson продолжает работать. Полигонные пробы — только при ровно одном Creo.
- `kill_creo` бьёт `xtop`+`nmsd` по имени (ВСЕ инстансы) и рвёт JLINK — ЗАПРЕЩЁН.
  `stop_creo` закрывает ТОЛЬКО прицепленный. Адресно — `Stop-Process -Id <pid>` (по `Get-Process xtop`).
- После `stop_creo` JVM creoson пересоздаётся сторожем и встаёт к новому единственному Creo.
- `familytable:list_tree` на БОЛЬШИХ семействах (сотни строк: `din912`, `pin_split`) — долго/висит;
  вложенность проверять через `file:has_instances` на промежуточном исполнении (составное имя
  `ИСПОЛНЕНИЕ<GENERIC>`; у промежуточного `has_instances=true`).
- ПРЕРЫВАНИЕ долгого вызова CREOSON (kill своего скрипта) подвешивает JVM/Creo (порт слушает,
  `connect` таймаутит) → сброс creoson+Creo ПО PID и подъём заново.

## 8. Кириллица (важно!)
Пути/имена с кириллицей через PowerShell `Invoke-RestMethod` ИСКАЖАЮТСЯ (`?` вместо букв:
`Directory does not exist: Z:/PTC/CREO-START/?????????/???????`). Кириллические пути гонять
ТОЛЬКО из Python (JSON + UTF-8), как в `D:\AI\PROBA\smartcopy.py`.

## 9. Живой цикл (эталон)
`connection:connect` → `creo:cd` «рабочая папка» → `creo:list_files` → `file:open {display:false}`
→ чтение/правка → `file:save` → `file:erase` → `creo:cd` обратно. Перед любой пишущей операцией
сверять `creo:pwd` с целевой папкой.

## 10. Конфиг полигона и общий `config.pro`
- Creo читает `config.pro` из START-IN папки (та, куда `cd /d` обёртки запуска).
- «Полный матч» без копирования: положить в start-in папку полигона БОЕВОЙ
  `Z:\PTC\CREO-START\START-STD\config.pro` — он ссылается на общие `Z:`-ассеты (шаблоны,
  `MY_ESKD.dtl`, шрифты), а TEMP/trails у него локальные. Тяжёлые ассеты (`НАСТРОЙКИ` 431 МБ,
  `Libraries` 14 ГБ) НЕ копировать — читать с `Z:`.
- Признак, что конфиг прочитан: новый трейл в `trail_dir` из конфига, а не в папке старта.

## 11. Тестовые модели mfg и семейств (Z:, только чтение; копировать можно, ЗАПИСЫВАТЬ нельзя)
Папка `Z:\PTC\Work\000_51 DF Держатели форм\000_1 DF-STP2 СТАНДАРТНЫЕ ИЗДЕЛИЯ ДФ\`:
- семейства-генерики: `df-stp2-gdf` (prt + asm), `df-stp2-sh-01/02`, `df-stp2-vdf`, `df-stp2-vz`, `df-stp2-vp`;
- ускорители исполнений (файлы экземпляров): `*.xpr` (`df-stp2-gdf-01.xpr`, `df-stp2-vp-19_05x18.xpr`, …),
  `*.tph` (`df-stp2-gdf.tph.1`, `df-stp2-gdf_tmp.tph.1`);
- сопутствующие типы: `.m_p` (процесс/мануфактуринг), `.mrd`, `.crc`, `.dsn`, `.stk`, `.tst`;
- рядом крупные проекты (напр. `23-1017GRI 2кап чистовой BDF 5 1_2''`), их копии — в `D:\AI\PROBA\…`.
- `Держатель форм`: сборка с компонентами вида `рычаг верхний` + `рычаг верхний.MFG` + `рычаг нижний.MFG`
  (обработки — одноимённые `.mfg`); в `Z:\PTC\Work\…` встречаются `*.mfg.1`, `ст-чпу-2-mfg.asm.1`, `.tph`.
- mfg-набор для проб (перенесён в `D:\AI\PROBA\mfg_test`):
  `Z:\PTC\Work\000_02 ST Стеклосфера\СТ-ЧПУ-02 Угловой стол многофункциональный\ст-чпу-2-mfg.asm`
  (обработка → ссылочная сборка `ст-чпу-2.asm` → 5 деталей).
- Живые прогоны умной копии (22.09.2026): семейство `df-stp2-gdf` (таблица сохранена, 3 исполнения
  `DF-STP2-GDF-01/02/03`) и mfg `ст-чпу-2-mfg.asm` (13 моделей, все `error:false`) —
  подробности в `SKILL_copy_assembly_project.md`.