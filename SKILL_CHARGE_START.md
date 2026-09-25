---
name: CHARGE_START
system: ЗНАНИЯ
description: Use when: стартовый набор знаний Creo/CREOSON — полные тексты главных скиллов (уже в промпте агента)
when: стартовый набор, Creo, CREOSON, с чего начать задачу, индекс Creo
date: 25.09.2026 14:48
---

# СТАРТОВЫЙ НАБОР ЗНАНИЙ (читать сразу, это в промпте агента)

**Собрано:** 25.09.2026 14:48
Порядок чтения: индекс Creo → индекс CREOSON → рутина CREOSON → природа модели → общая карта скиллов.



===== Creo\SKILL_creo_index.md =====
name: creo-index
system: INDEX
description: Use when: задача с темой Creo
when: creo, creoson, parametric, assembly, part, drawing
date: 22.09.2026
ЧТО ЗДЕСЬ: см. раздел «СТРУКТУРА И КАРТА СКИЛЛОВ» ниже — 8 подразделов (API, DOCS, CREOSON, COPY, STANDARDS, RELATIONS, DAVYDOVKA, INFRA).
КОГДА ОТКРЫВАТЬ: теги [CREO], [PARAMETRIC]
КОГДА ПИСАТЬ: CRASH триггеры: SKILL_creoson_probe_method, Ошибки\ERR_creoson_write_ops.md
универсальный закон — MANIFEST.md, специфика среды — в адаптерах

## ГЛАВНОЕ ОТКРЫТИЕ (22.09.2026): один `pfc*` — много каналов; CREOSON = обёртка
Управлять Creo можно **НАПРЯМУЮ, без CREOSON**:
- **Creo.JS** — JS во встроенном браузере Creo (этим идёт Давыдовка);
- **JLINK / Object TOOLKIT Java** — своя Java-программа на `com.ptc.pfc.*` (классы в `pfcasync.jar`)
  сама стартует/подключается к Creo (синхронно/асинхронно);
- **Object TOOLKIT C++ / Pro/TOOLKIT** — нативная DLL внутри процесса Creo (`protk.dat`);
- **VB API**, **Web.Link** — родственные каналы.
**CREOSON = JSON-сервер ПОВЕРХ JLINK**: `creoson-core-3.0.1.jar` = 268 классов
`com.simplifiedlogic.nitro.jlink`, а `com/ptc/pfc` в нём **0**; сами `pfc*` — в `pfcasync.jar`
(1873 класса). Разбор и пробы — `SKILL_creo_api_ecosystem.md`.
**Давыдовка** идёт каналом **Creo.JS** (мост `creojs.js` + серверные `*.creojs`) + свой
Python-сервер на 8000 (не CREOSON и не JLINK) — `SKILL_davydovka_creoson_map.md`.

## СТРУКТУРА (подразделы) И КАРТА СКИЛЛОВ
| Подраздел | Что внутри |
|---|---|
| `API\` | `SKILL_creojs_api.md` (Creo.JS/`pfc*`), `SKILL_creo_api_ecosystem.md` (каналы: OTK/JLINK/VB/Web.Link/CREOSON) |
| `DOCS\` | `SKILL_creo_docs_map.md` (где хелпы/PDF/API-руководства в `D:\PTC\CREO12`) |
| `CREOSON\` | `SKILL_creoson_workflow.md` (цикл, переключение папок), `SKILL_creoson_complete.md` (карта API), `SKILL_creoson_sessions_workdirs.md` (сессии/папки), `SKILL_creo_commands.md` (подбор команды), `SKILL_creoson_write_rules.md` (пишущие), `SKILL_creoson_rename_mechanism.md` (rename), `SKILL_creoson_probe_method.md` (пробы), `SKILL_creoson_inbox_deepseek.md` (долги темы) |
| `COPY\` | `SKILL_copy_assembly_project.md` (умная копия проекта), `SKILL_copy_rename.md` (методика копии/переименования) |
| `STANDARDS\` | `SKILL_creo_company.md`, `SKILL_company_config.md`, `SKILL_naming_spec.md`, `SKILL_drawings_eskd.md`, `SKILL_creo_templates.md`, `SKILL_creo_model_nature.md` (природа модели: деталь/сборка/производство), `SKILL_parameters_guide.md`, `SKILL_reference_limits.md`, `SKILL_creo_cards.md` |
| `RELATIONS\` | `SKILL_creo_relations.md`, `SKILL_relations_constitution.md`, `SKILL_relations_basics.md`, `SKILL_relations_examples.md`, `SKILL_curves_from_equation.md`, `SKILL_curves_examples.md`, `SKILL_spring_compression_generator.md`, `SKILL_spring_tension_master.md` |
| `DAVYDOVKA\` | `SKILL_davydovka_creoson_map.md` (карта Давыдовка ↔ CREOSON) |
| `INFRA\` | `SKILL_creostart_fleet.md` (флот, старт машин), `SKILL_object_creoson_tests-01_asm.md` (объектные пробы) |
| корень | этот индекс + `cards\` (карты моделей, сырые близнецы) + `SKILL_creo_file_reading.md` (чтение файлов «в лоб»: история, упакованные числа, оглавление; инструмент `plm_reader`) + `CREO_MAP.md`, `SKILLS_MAP.md` |

## КАК ИИ НАХОДИТ СКИЛЛ (правило поиска)
1. Вход — корневой `SKILL_index.md` (домен Creo) → **этот файл**.
2. Здесь — таблица подразделов; идти прямо в файл по пути `Creo\<подраздел>\SKILL_*.md`.
3. Ключевые слова для поиска — в поле `when` шапки каждого скилла.
4. В каждом подразделе есть свой `_INDEX.md` (если агент уже внутри папки).

## ИСТОЧНИКИ ДОКУМЕНТАЦИИ (только чтение)
Все хелпы/PDF/API-руководства — в установке `D:\PTC\CREO12` (полная карта и языки —
`SKILL_creo_docs_map.md`; разбор каналов — `SKILL_creo_api_ecosystem.md`).
Копии-дубли PTC в репо удалены словом пользователя 22.09 (в гит не возвращать); справка — в установке `D:\PTC\CREO12` (карта: `SKILL_creo_docs_map.md`).
Временная папка разбора `D:\AI\ИЗУЧИТЬ\CREO` разбирается и удаляется пользователем — на неё
в скиллах не опираться.


===== Creo\CREOSON\_INDEX.md =====
- `SKILL_creoson_routine.md` — CREOSON для рутины: полный практический разбор (18 групп, 199 функций, сценарии, грабли: кириллица, перезапуск, PID)
- `SKILL_creoson_workflow.md` — полный цикл работы в CREOSON (подключение, папки/переключение, чтение/запись)
- `SKILL_creoson_pfc_map.md` — CREOSON ↔ PTC `pfc*`: карта соответствия, проба прямого чтения через JLINK, карта JLINK-примеров


===== Creo\CREOSON\SKILL_creoson_workflow.md =====
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


===== Creo\STANDARDS\SKILL_creo_model_nature.md =====
---
name: creo-model-nature
system: Creo
description: Use when: определяешь природу модели (деталь / сборка / производство-мануфакчуринг) или правишь параметр ТИП, ПАРТИЯ; защита производственных моделей от массовых правок
when: ТИП, тип модели, производство, мануфакчуринг, ПАРТИЯ, чесалка, typcheck, оснастка, заготовка, приспособление
priority: high
---
# ПРИРОДА МОДЕЛИ: деталь / сборка / ПРОИЗВОДСТВО (23.09.2026)

## 1. Правило
Параметр `ТИП` (ограниченный) должен соответствовать природе модели:
| природа модели | `ТИП` | как выглядит |
|---|---|---|
| деталь (`.prt`) | `Деталь` | — |
| обычная сборка (`.asm`) | `Сборка` | — |
| **производственная модель** (мануфакчуринг, оснастка) | **`Производство`** | **выглядит как обычная сборка!** |

⚠️ Главная ловушка: производственная модель — это `.asm`, и по внешнему виду, составу и API она неотличима
от сборки. Если «лечить» её как сборку, ей поставят `Сборка` и испортят классификацию.

## 2. НЕОСПОРИМЫЕ ПРИЗНАКИ (проверено 23.09.2026, а не «по параметрам»)
Главное правило дома: природу модели доказывают **факты Creo**, а не параметры (их пишем мы же,
и там встречается наследие — например `ТИП = «3»` в старых файлах).

1. **Расширение файла `.mfg`** — самый быстрый и надёжный признак производственной модели
   (`model.GetFileName().endsWith(".mfg")`). В дереве дома таких файлов **414** (`.mold`/`.cast` — 0).
   Пример: `…\РЕЗЕЦ ТОКАРНЫЙ РЕЗЬБОВОЙ ВНУТРЕННИЙ\d25\d25.mfg.1`.
2. **C-API: `ProMdlSubtypeGet(model, &subtype)`** (`ProMdl.h:795`), перечислитель `ProMdlsubtype`
   (`ProMdl.h:63-92`) — полный законный список подтипов:
   `PROMDLSTYPE_ASM_DESIGN` (конструкторская сборка), `PROMDLSTYPE_MFG_NCASM` (manufacturing assembly),
   `PROMDLSTYPE_MFG_NCPART`, `PROMDLSTYPE_MFG_EXPMACH`, `PROMDLSTYPE_MFG_CMM`,
   `PROMDLSTYPE_MFG_SHEETMETAL`, `PROMDLSTYPE_MFG_CAST`, `PROMDLSTYPE_MFG_MOLD`, `PROMDLSTYPE_MFG_DIEFACE`,
   `PROMDLSTYPE_MFG_HARNESS`, `PROMDLSTYPE_MFG_PROCPLAN`, `PROMDLSTYPE_ASM_NCMODEL`,
   `PROMDLSTYPE_ASM_PROCPLAN`, `PROMDLSTYPE_PART_SHEETMETAL`, `PROMDLSTYPE_PART_SOLID` и др.
   Для наших задач достаточно отличить `ASM_DESIGN` от группы `MFG_*` (Mold/Cast в доме не встречаются).
3. **JLink: `Model::GetSubtype()` в нашем `pfcasync.jar` НЕТ**, а `instanceof pfcMFG.MFG`
   (`com.ptc.pfc.pfcMFG.MFG extends pfcModel.Model`) даёт **false даже для `.mfg`-модели** — проверено
   пробой (`mfgcheck`): `d25.mfg.1` → тип `1`, объект MFG = false. Значит в Java-движке опираемся на
   **расширение** и, при нужде, на C-API.
4. **`ModelType` (JLink)**: код 0 = сборка, 1 = деталь; производственная `.mfg`-модель отдаёт 1 —
   по типу модели производство и сборку не различить.
5. Маркеры дома `ТИП = Производство` и параметр `ПАРТИЯ` — **только подсказка**, не доказательство:
   у «производственных» `.asm` дома (напр. `p-515-300_008am-03.asm.1`) тип сборки (0) и никаких
   признаков MFG; это **оснастка**, которую дом так пометил.

## 2б. РОЛИ КОМПОНЕНТОВ — «кто есть кто» (API Creo, проверено 23.09.2026)
Тот самый «опрос», который есть у Давыдовки (`index_rename.creojs`):
- **`ComponentFeat.GetCompType()`** → `ComponentType`:
  `0 COMPONENT_WORKPIECE` (**заготовка**), `1 COMPONENT_REF_MODEL` (**ссылочная модель** = деталь проекта),
  `2 COMPONENT_FIXTURE` (**оснастка/приспособление**), `3 COMPONENT_MOLD_BASE`, `4 MOLD_COMP`,
  `5 MOLD_ASSEM`, `6 GEN_ASSEM`, `7 CAST_ASSEM`, `8 DIE_BLOCK`, `9 DIE_COMP`, `10 SAND_CORE` (**стержень**),
  `11 CAST_RESULT` (**результат литья**), `12 FROM_MOTION`, `13 NO_DEF_ASSUM`, `14 NONE` (нет роли).
- Оснастка ещё находится по признакам наладки: `FeatureType.FEATTYPE_FIXTURE_SETUP = 91`
  (`model.ListFeaturesByType(...)`, как в Давыдовке `creoRenameFixtureComponentIds`).
- **Вывод для дома**: производственную сборку можно доказать БЕЗ параметров — по ролям состава
  или по типу модели. Что подтвердилось на живых файлах:
  `d25.asm` → `D25.prt` = ссылочная модель, `D25Z.prt` = **ЗАГОТОВКА**;
  `p-b9210_10505.asm` → `P-B9210_10505.prt` = ссылочная модель, `P-B9210_10505_Z.prt` = **ЗАГОТОВКА**;
  `p-515-300_008am-03.asm` → ссылочная модель (заготовки нет);
  `sbsb.asm` → `D25.prt`, `PLATINA.prt` = **нет роли (14)** — то есть «приспособление» НЕ всегда помечено ролью.
- Тип модели: **`Model.GetType() == ModelType.MDL_MFG` работает** (`d25.mfg` → MDL_MFG); числовые значения:
  `MDL_ASSEMBLY=0`, `MDL_PART=1`, `MDL_DRAWING=2`, `MDL_MFG=6`. Проверять в try/catch — у нетиповых
  файлов тип может бросить `XUnusedValue` (замечание Давыдовки).
- Проба: у самой `.mfg`-модели `ListItems(ITEM_FEATURE)` бросает `XUnimplemented` — роли её компонентов
  читать иначе (через `pfcMFG.MFG.GetSolid()`/признаки наладки); это долг пробы.

## 2в. ДАВЫДОВКА — где это уже решено (кто и что)
Давыдовка (`D:\AI\ИЗУЧИТЬ\ДАВЫДОВКА\creoJS\creo_bom_js`, карта дома `Creo\DAVYDOVKA\SKILL_davydovka_creoson_map.md`,
конспект `STUDY_NOTES.md`) — единственный источник в доме, где производство разобрано по фактам:
| Что | Где |
|---|---|
| проверка «модель производственная» | `index_rename.creojs` → `creoRenameIsManufacturingModel` (каскад: `Model.Descr.Type === pfcModelType.MDL_MFG`, `isInstanceOf('pfcMFG')`, наличие `GetSolid`, `String(Type).indexOf('MFG')`) |
| роль компонента (заготовка/ссылочная/оснастка) | там же → `creoRenameComponentKind` (`feature.CompType` ↔ `pfcComponentType.COMPONENT_*`) |
| оснастка через признаки наладки | там же → `creoRenameFixtureComponentIds` (`FEATTYPE_FIXTURE_SETUP`, дети первого поколения) |
| **скан рабочей директории** | `rename.js` → `scanDirectory()` / `runFolderScan()` → `CreoJS.scanCreoRenameDirectory(...)`; на стороне Creo — `session.ListFiles(filter, latestOption, directory)` |
| правило копии | комментарий: «Обработкой может быть только сборка: деталь бывает заготовкой, но не MDL_MFG» |

## 2а. Как выглядит производственный набор (изучено на `d25`)
Папка `…\d25\` содержит: `d25.mfg.1` (производственная модель), `d25.asm.1` (сборка),
`d25.prt.1` (деталь), **`d25z.prt.1` (заготовка — суффикс `z`)**, **`platina.prt.1` (приспособление)**,
`sbsb.asm.1` (ещё сборка). Вывод: в производственной папке рядом живут заготовки и приспособления,
и «по имени/параметрам» их не отличить — нужны признаки из п.2 (расширение/подтип).

## 3. Что ещё живёт в производстве (слово хозяина: пока НЕ ЛЕЗЕМ, только изучаем)
- **заготовка** (workpiece / billet) — деталь, привязанная к производственной модели;
- **приспособления** (fixtures) — сборки оснастки;
- возможные свои значения `ТИП`/`ТИП2` (`Технология` уже есть в списке вариантов `ТИП2`).
Правило: в папках производства массовых правок не делать; при сомнении — спросить хозяина.

## 4. Правила безопасности для инструментов (чесалка `creo_comb`)
- Производственными считаются (и **не «лечатся»**): модели `.mfg`; модели с типом `MDL_MFG`;
  сборки, в составе которых есть компоненты с ролями **заготовка / ссылочная модель / оснастка**
  (`GetCompType()` 0/1/2). Маркеры дома (`ТИП=Производство`, `ПАРТИЯ`) — только подсказка.
- `typcheck` показывает их строкой `производственная (факты Creo) … — не трогаем`.
- `add` (правка) **не открывает `.mfg`** и **не меняет `ТИП`** у производственных; остальное лечит как обычно.
- Режим `roles <папка>` — читаемый отчёт «кто есть кто» (состав с ролями) для разбора производства.
- Прогон `add` по производственной папке — только по явному слову хозяина.

## 5. Грабли (из проб 23.09.2026)
- **Creo отдаёт модель из СЕССИИ по имени.** Если правишь копию в другой папке, а модель с таким именем
  уже открыта (или находится по `search.pro`), можно править/сохранить не тот файл. Проверка после
  `Save()`: новая версия обязана появиться **именно в целевой папке** (чесалка печатает
  `новая версия: <файл>` либо `ВНИМАНИЕ: новой версии в этой папке не видно…`).
  Для проб — давать копиям **уникальные имена** или перезапускать Creo.
- `ModelType` в API: код **0** = сборка, **1** = деталь (по нашим `dump`); тип мануфакчуринга в OTK —
  `MDL_MFG`, но дом различает производство по маркерам из п.2.
- Файлы хранятся версиями (`x.asm.1`), и JLink **не принимает** имя с версией
  (`XUnknownModelExtension`) — открывать через базовое имя (так делает `creo_comb.openAny`).

## 6. Связанное
`Creo\SKILL_creo_templates.md` (эталоны), `SKILL_parameters.md` (параметры дома),
`agent\dev\PROGRAM_REGISTRY.md` (`creo_comb` — чесалка, режимы `scan/add/typcheck/dump`).


===== SKILL_index.md =====
---
name: index
system: общее
description: Карта всех скиллов репо по доменам: что где лежит и куда смотреть
when: навигация, где что, карта скиллов, список скиллов, какой скилл, домены
priority: critical
---

# КАРТА СКИЛЛОВ РЕПО (D:\AI\repo)
Один скилл = одна зона знания. Домены не дублируют друг друга.

## НАПРАВЛЕНИЯ (первый указатель, состав по MANIFEST.md)
- Creo: Creo\SKILL_creo_index.md · PDF: PDF\SKILL_pdf_index.md · Web: Web\SKILL_web_index.md
- Инженерные: Инженерные\SKILL_engineering_index.md · Трейлы: Трейлы\SKILL_trails_index.md
- Ошибки: Ошибки\SKILL_errors.md · Крахи: crash\SKILL_crash_constitution.md (закон) + crash\SKILL_crash_index.md (список крах-скиллов)

### 1. Creo (Веб-агент, Инженер)
*Специализация на работе с CAD-системой через API и интерфейсы.*
**Вход темы — `Creo\SKILL_creo_index.md`** (главный индекс Creo: открытие + структура + карта).
ГЛАВНОЕ (22.09.2026): один `pfc*` — много каналов; управлять Creo можно напрямую (Creo.JS / OTK-JLINK /
Pro-TOOLKIT / VB / Web.Link), **CREOSON = JSON-сервер поверх JLINK**; Давыдовка — канал Creo.JS + свой сервер 8000.
Подразделы `Creo\` (в каждом свой `_INDEX.md`):
- `API\` — `SKILL_creojs_api` (Creo.JS/`pfc*`), `SKILL_creo_api_ecosystem` (каналы API) — **critical**
- `DOCS\` — `SKILL_creo_docs_map` (карта документации: хелпы/PDF/API) — **high**
- `CREOSON\` — `SKILL_creoson_workflow`, `SKILL_creoson_complete`, `SKILL_creoson_sessions_workdirs`,
  `SKILL_creo_commands`, `SKILL_creoson_write_rules`, `SKILL_creoson_rename_mechanism`,
  `SKILL_creoson_probe_method`, `SKILL_creoson_inbox_deepseek` — **critical**
- `COPY\` — `SKILL_copy_assembly_project` (умная копия проекта), `SKILL_copy_rename` — **critical**
- `STANDARDS\` — `SKILL_creo_company`, `SKILL_company_config`, `SKILL_naming_spec`, `SKILL_drawings_eskd`,
  `SKILL_creo_templates`, `SKILL_creo_model_nature` (деталь/сборка/производство — `ПАРТИЯ`, мануфакчуринг),
  `SKILL_parameters_guide`, `SKILL_reference_limits`, `SKILL_creo_cards`
- `RELATIONS\` — `SKILL_creo_relations`, `SKILL_relations_constitution`, `SKILL_relations_basics`,
  `SKILL_relations_examples`, `SKILL_curves_from_equation`, `SKILL_curves_examples`,
  `SKILL_spring_compression_generator`, `SKILL_spring_tension_master` — **critical**
- `DAVYDOVKA\` — `SKILL_davydovka_creoson_map` (карта Давыдовка ↔ CREOSON)
- `INFRA\` — `SKILL_creostart_fleet` (флот/старт), `SKILL_object_creoson_tests-01_asm` (объектные пробы)
- корень `Creo\` — `CREO_MAP` (строение Creo), `SKILLS_MAP` (карта скиллов ветки),
  `SKILL_creo_file_reading` (**чтение файлов Creo «в лоб»**: история изменений, упакованные числа, секции/параметры;
  там же инструмент дома `plm_reader`), `README_jlink_direct`
Карточки моделей — `Creo\cards\`.

### 2. Python / VS Code (Программист, папка Prog\)
*Стандарты кода, тестов и памяти агента; вход направления = эта секция,
собственный индекс-файл Prog\ = долг (см. секцию 7).*
- `Prog\SKILL_python_standard` (Стандарт расчётных скриптов: блоки, суффиксы, аудит) — **critical**
- `Prog\SKILL_test_first_rule` (Правило TEST-first) — **critical**
- `Prog\SKILL_tool_routing` (Маршрутизация запросов; единственная прописка здесь,
  из Core не дублировать) — **critical**
- `Prog\SKILL_agent_memory` (Память агента: что помнить, куда класть)
- `Prog\SKILL_automated_validation` (Автоматические пробы и гейты)
- `Prog\SKILL_code_parsing` (Разбор кода: ast, не regex)
- `Prog\SKILL_cursor_rules_format` (Форматы внешних правил cursor/cline)
- `Prog\SKILL_diff_and_apply` (Диффы и их применение)
- `Prog\SKILL_repo_mapping` (Карта репо и указатели)
- `Prog\SKILL_unit_testing` (Юнит-пробы на копиях)
- `STANDARD Engineering Calculation Script Architecture.md` (Архитектура расчётных
  скриптов; прописан под живым именем из корня, переименование = долг секции 7)
## ДОМЕН 3: Инженерные (оба агента)
| Скилл | Назначение |
|---|---|
| SKILL_materials_reference | справочник материалов (канон) |
| SKILL_engineering_mechanics | сопромат, динамика, усталость |
| SKILL_heat_hydraulics | тепло, гидравлика, пневматика |
| SKILL_casting_hts_master | литьё в ХТС |

## ДОМЕН 4: Производство (зеркало срезов 1С)
| Скилл | Назначение |
|---|---|
| SKILL_production_mirror | производственный контур: склад, входящие, запуск, отгрузки, якорь, время цикла |

### 5. Общее (Core)
*Фундаментальные правила работы агента.*
- **Управление**: 
    - `SKILL_log_management` (Логи и автоуборка) — **долг: файла нет** (аудит 22.09; механику держит tools\agent\log_clean.py)
    - `SKILL_agent_protocol` (Протокол инженера-напарника; живёт в корне репо) — **critical**
    - маршрутизация запросов — см. `Prog\SKILL_tool_routing` — **critical**
- **Контекст**: 
    - `company_conventions.md` (Паспорт КБ: станки, семантика; живое имя без префикса SKILL_)
    - `SKILL_web_vision_limits` (Возможности WEB/Vision)
    - `SKILL_local_agent_cline` (**Выживание в Cline/VS Code**; корень репо) — **critical**
    - `strategy.md` (Журнал развития; живое имя без префикса SKILL_)
    - `SKILL_skill_craft` — **долг: файла нет** (аудит 22.09); был задуман как мета-скилл (Ремесло промтов и скиллов; priority high,
      подгружается по надобности: задача о промтах, скиллах, правилах, шаблонах)
    - `SKILL_parameters` (Справочник параметров; «дикий», интегрирован 22.09)
    - `DESIGN_davydovka_tokens.md` (токены дизайна Давыдовки для окон и витрины;
      не скилл, а закон дизайна, цитируется .clinerules)
- **Аудит**: `AUDIT_rules_*.md` и `SKILL_audit_protocol.md`
- **Справочники и управленческие файлы** (не скиллы, в маршрутизацию не входят): `GUIDE\db.md`, `GUIDE\models.md`, `GUIDE\plm.md`, `Vericut\VERICUT_отложи_в_Vericut_260820.md`, `Ошибки\ERR_260902_web_fetch.md`, `BACKLOG_tools.md`

### 6. Agents (Автономные исполнители)
*Семь живых файлов, происхождение внешнее; priority normal; подгружаются по надобности; до первой пробы — внешний источник, не закон дома.*
- `agents\rag-architect\SKILL_rag_architect.md` + `agents\rag-architect\references\` (chunking_strategies_comparison.md, embedding_model_benchmark.md, rag_evaluation_framework.md)
- `agents\skill-security-auditor\SKILL_skill_security_auditor.md` + `agents\skill-security-auditor\references\threat-model.md`
- `agents\zero-hallucination-coder\SKILL_zero_hallucination_coder.md`
- `agents\SKILL-AUTHORING-STANDARD.md` (стандарт авторства скиллов)
- `AGENT_MAP.md` (**Карта строения агента** `D:\AI\tools\agent`: модули, порт 8765, инструменты,
  данные, ночи и сторож — high; вход по тегам «агент/agent.py/loop/tools_registry/8765»)
- `SKILL_parallel_local_leg.md` — **удалён по слову пользователя 23.09.2026** (спека 113 не оправдала
  формы: правила ноги = долг, если параллельные ноги вернутся). Уроки спеки 113 сироты не потеряны:
  живут в `PROGRESS_spec113.md`, раздел «ЧЕМУ УЧИТЬ НОГУ»; в `SPEC_113_orphan_drawings.md` (строки 43, 71)
  ссылки на удалённый скилл — висячие, сама спека по закону не правится.

## ДОМЕН 7: Автогенерируемые (руками не править)
| Файл | Кто пишет |
|---|---|
| Creo/STANDARDS/SKILL_company_config.md | passport_tools (живой паспорт из config.pro) |
| Трейлы/TRAIL_JOURNAL.md | trail_tools |
| Ошибки/ERR_*.md | каталог ошибок |
| Избранное/SKILL_favorites_<user>.md | избранное пользователя (папка gitignored, решение 22.09) |

## ПРАВИЛА МАРШРУТИЗАЦИИ
- Команда CREOSON → creo_commands, детали API → creoson_complete.
- «Как написать relations» → creo_relations (синтаксис) + relations_constitution (правила).
- «Единицы/шаблоны/шифры/параметры/чертежи» → creo_company.
- «Шаблон модели / новая модель / TPL_SOURCE» → creo_templates.
- Код проекта → python_standard + test_first_rule.
- Физика/материалы → Инженерные.
- «Где деталь / когда комплект / якорь / цикл» → production_mirror.
- «Почему вылетаю / как работать в Cline / где что лежит» → SKILL_local_agent_cline (в корне).
- «Запетлял / встал / повторяю одно и то же» mid-task → §9.3 SKILL_local_agent_cline:
  СТОП → вслух назвать подпись краха → смена метода ИЛИ стоп-отчёт пользователю (помощь снаружи).

## ИСТОЧНИКИ ПРАВДЫ
- DESIGN_davydovka_tokens.md: канон дизайна для новых инструментов. **Долг/проверить: файла в репо нет**
  (аудит 25.09: найден только в копии `D:\AI\log\urn\cline\repo_clone\`), окна дома сейчас строятся без токенов.
- SKILL_tool_template.md: шаблон создания трёхрукого инструмента — **долг: файла нет** (аудит 22.09).

### 7. ДОЛГИ И ИДЕИ КАРТЫ (честность: нет файла = нет скилла)
- **PDF**: домен пуст; скиллы перепечати, миниатюр и реестра родятся из практики
  pdf_tools.py и спеки 104 — долг оживления направления.
- **Web**: в папке один сырой файл `260826_1610.md`; довести до Золотого стандарта = долг.
- **Трейлы**: индекс создан 22.09 — `Трейлы\SKILL_trails_index.md` (в гите); журнал `Трейлы/TRAIL_JOURNAL.md` gitignored как операционный поток (пишет trail_tools).
- **Prog\SKILL_prog_index.md**: закрыт решением 22.09: вход = секция 2, индекс не создаётся.
- **Creo PDF удалены словом пользователя 22.09; источник восстановления = установка PTC и онлайн-справка, в дом не возвращать без задачи; в гит не входить.**
- **Библиотека `D:\AI\ИЗУЧИТЬ\CREO`**: на 22.09 вечером папки на диске нет (в `ИЗУЧИТЬ` остались ДАВЫДОВКА, Новые правила, Новые правила2); таблица в Creo-индексе отражает утренний замер 1 206 544 066 Б / 17 963 файла — судьбу папки решает пользователь, до его слова строку не переписывать.
- **.gitignore (решение 22.09)**: сведены два поколения; память дома (PROGRESS_*, SPEC_*, AUDIT_*, crash/, Трейлы/TRAIL_JOURNAL.md) под гитом не игнорируется; вне гита — secrets.json, users.json, data/, log/, *.db, backup_db/, *.log, *.bak, Избранное/.
- **Журнал Трейлов (решение 22.09)**: `Трейлы/TRAIL_JOURNAL.md` — память дома о том, кто и когда работал в железе; из игнора убран (в remote уже трекается, а ignore против трекнутого файла бессилен).
- **crash\SKILL_crash_reasoning-loop.md**: указатель вместо двойника (тело = plan-loop); удаление только по слову пользователя (22.09).
- **SKILL_architect_reviewer** (идея ниже): **долг: файла нет** (аудит 22.09).
- **Переименование**: `STANDARD Engineering Calculation Script Architecture.md` →
  `Prog\SKILL_calc_script_architecture.md` — по слову пользователя, со сверкой ссылок.

## ЗОЛОТОЙ СТАНДАРТ (Golden Standard Template)

Каждый новый скилл должен следовать структуре:
1. **Паспорт (Passport)**: Назначение, priority, когда применять.
2. **Домен (Domain)**: К какому направлению относится.
3. **Привычки (Habits/Rules)**: Конкретные правила работы с этим скиллом (напр. "всегда проверять X перед Y").
4. **Инструменты (Tools/Methods)**: Список методов/команд, которые использует скилл.
5. **Крах-протокол (Crash-Protocol)**: Специфические ошибки и как их фиксировать.
6. **Проба (Probe)**: Как проверить, что скилл работает (Unit tests/Manual checks).
7. **Указатель (Pointer)**: Указатель носит то же имя, что и закон, и живёт по старому пути; тело указателя = одна строка; одноимённость указателя и тела — норма, два одноимённых тела — нарушение (аудит 22.09).

## ИДЕЯ: SKILL_architect_reviewer
Предложение: создание специализированного скилла для аудита соответствия новых скиллов и планов "Золотому стандарту" и "Закону трёх линий".