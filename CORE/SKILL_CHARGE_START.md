---
name: CHARGE_START
system: ЗНАНИЯ
description: Use when: стартовый набор знаний Creo/CREOSON — полные тексты главных скиллов (уже в промпте агента)
when: стартовый набор, Creo, CREOSON, с чего начать задачу, индекс Creo
date: 12.10.2026 11:44
---

# СТАРТОВЫЙ НАБОР ЗНАНИЙ (читать сразу, это в промпте агента)

**Собрано:** 12.10.2026 11:44
Порядок чтения: индекс Creo → индекс CREOSON → рутина CREOSON → природа модели → общая карта скиллов.



===== Creo\SKILL_creo_index.md =====
---
name: creo-index
system: INDEX
description: Use when: задача с темой Creo
when: creo, creoson, parametric, assembly, part, drawing
date: 22.09.2026
---

ЧТО ЗДЕСЬ: см. раздел «СТРУКТУРА И КАРТА СКИЛЛОВ» ниже — 8 подразделов (API, DOCS, CREOSON, COPY, STANDARDS, RELATIONS, DAVYDOVKA, INFRA).
КОГДА ОТКРЫВАТЬ: теги [CREO], [PARAMETRIC]
КОГДА ПИСАТЬ: CRASH триггеры: SKILL_creoson_probe_method, Ошибки\ERR_creoson_write_ops.md
универсальный закон — MANIFEST.md, специфика среды — в адаптерах

## ⚠️ ЗОНЫ РАБОТЫ С ФАЙЛАМИ (слово владельца, 03.10.2026) — ПЕРВОЕ, ЧТО ЧИТАТЬ
* **`D:\AI\PROBA` — можно ВСЁ** (создавать, переименовывать, удалять, пробовать, запускать Creo).
* **`Z:\PTC` — ТОЛЬКО ЧТЕНИЕ** (читать, сканировать, измерять, отчёты). Запись, ПУРГЕ, экспорт в папку
  склада, правка `config.pro`, запуск Creo с cwd на `Z:` — запрещены.
* Все пробы/опыты с Creo — **только в `PROBA`**, копия модели — под **уникальным именем**.
* Подробности: `SKILL_creo_file_reading.md` §0.

## 📌 СОСТОЯНИЕ НА 03.10.2026 (живая проверка, не пересказ)
* Инструмент чтения «в лоб» — `D:\AI\tools\agent\plm_reader\`, версия **V37**, база — `db\plm_reader_<дата>.db`
  (читается свежайший), настройки — `settings\settings.json`. Creo не нужен.
* Разбор чтения **деталь / сборка / чертёж** и список открытых долгов: `SKILL_creo_file_reading.md` §8.85–8.86.
* Проба чтения (живая, `PROBA`): деталь — материал/объём/роль/история; сборка — объём/история
  (параметры сборок **не читаются**, 0 %); чертёж — история (объём/обозначение **0 %** — законно).


РАЗРЕШЕНИЕ ВЛАДЕЛЬЦА (02.10.2026): CREOSON **не поднимается автоматически** (CTL его выключил
из автозапуска 23.09.2026 — он нужен только блокам на `creo_call` и поднимается по требованию),
**но по слову владельца запускается свободно**: «если нужен креосон — запускайте».
Не считай его «мёртвым» и не поднимай без надобности: инструменты класса Р (`orphan_scan`,
`config_audit`, `copy`) работают без него, он нужен только живым блокам Creo.

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

## ПОДРАЗДЕЛЫ И КАРТА СКИЛЛОВ
| Подраздел | Что внутри |
|---|---|
| **`READ\`** | **чтение и правка файлов «в лоб» по частям** (03.10.2026): `SKILL_creo_read_core` (ядро формата), `_part`, `_asm`, `_drw`, `_mfg`, `_family` (семейства + библиотека `Libraries`), `_feat` (операции построения), `SKILL_creo_write_raw` (правка в лоб), `SKILL_creo_new_file` (создание файла — подготовка); карта — `READ\_INDEX.md`. Вход: `SKILL_creo_file_reading.md` (исторический конспект 1910 строк, номера §) |
| `API\` | `SKILL_creojs_api.md` (Creo.JS/`pfc*`), `SKILL_creo_api_ecosystem.md` (каналы: OTK/JLINK/VB/Web.Link/CREOSON) |
| `DOCS\` | `SKILL_creo_docs_map.md` (где хелпы/PDF/API-руководства в `D:\PTC\CREO12`) |
| `CREOSON\` | `SKILL_creoson_workflow.md` (цикл, переключение папок), `SKILL_creoson_complete.md` (карта API), `SKILL_creoson_sessions_workdirs.md` (сессии/папки), `SKILL_creo_commands.md` (подбор команды), `SKILL_creoson_write_rules.md` (пишущие), `SKILL_creoson_rename_mechanism.md` (rename), `SKILL_creoson_probe_method.md` (пробы), `SKILL_creoson_inbox_deepseek.md` (долги темы) |
| `COPY\` | `SKILL_copy_assembly_project.md` (умная копия проекта), `SKILL_copy_rename.md` (методика копии/переименования) |
| `STANDARDS\` | `SKILL_creo_company.md`, `SKILL_company_config.md`, `SKILL_naming_spec.md`, `SKILL_drawings_eskd.md`, `SKILL_creo_templates.md`, `SKILL_creo_model_nature.md` (природа модели: деталь/сборка/производство), `SKILL_parameters_guide.md`, `SKILL_reference_limits.md`, `SKILL_creo_cards.md` |
| `RELATIONS\` | `SKILL_creo_relations.md`, `SKILL_relations_constitution.md`, `SKILL_relations_basics.md`, `SKILL_relations_examples.md`, `SKILL_curves_from_equation.md`, `SKILL_curves_examples.md`, `SKILL_spring_compression_generator.md`, `SKILL_spring_tension_master.md` |
| `DAVYDOVKA\` | `SKILL_davydovka_creoson_map.md` (карта Давыдовка ↔ CREOSON) |
| `INFRA\` | `SKILL_creostart_fleet.md` (флот, старт машин), `SKILL_object_creoson_tests-01_asm.md` (объектные пробы) |
| корень | этот индекс + `cards\` (карты моделей, сырые близнецы) + `SKILL_creo_file_reading.md` (чтение файлов «в лоб»: история, упакованные числа, оглавление, параметры и отношения; §8.70–8.81 от 28–29.09.2026; инструмент `plm_reader` V24) + `CREO_MAP.md`, `SKILLS_MAP.md` |
| проверка хозяйства | **спека прогона — `D:\AI\СПЕКИ\СПЕКА_ПРОВЕРКИ_CREO.md`** (установка/настройки `CREO-START`, библиотеки `Libraries`, склад `Work`, тормоза, ошибки, предложения). Читается целиком до первого действия; живые файлы Creo не менять |
| **СТОРОННИЕ ПЛАГИНЫ** | **отдельная папка-направление `D:\AI\repo\B&W\`** (03.10.2026, Cline): набор B&W Plugins Suite — 15 модулей SMART\* от B&W Software GmbH, канал `protkdat` (как VERICUT), лицензия FlexNet:6501. Вход: `B&W\README.md`, конспект `B&W\STUDY_NOTES.md`, скилл-заготовка `B&W\SKILL_BW_PLUGINS.md`. **Ничего не установлено.** Под CREO13 есть только 3 модуля из 15: SMARTHolechart 19.4.1.0 (работает с `.hol` — прямо в тему конспекта «Таблица отверстий»), SmartMBDTools 13.0.5.0, SmartOptics 13.0.0.0 (⚠️ ломает mapkey). Ключевое: **52 проверки модели вендора** (SMARTUpdate) — готовый перечень «что контролировать» для нашего движка правил (`B&W\15_КАТАЛОГ_ПРОВЕРОК_SMARTUPDATE.md`); карта файлов распакованных тел — `B&W\14_КАРТА_ФАЙЛОВ_ПРАВИЛО.md`; что в агенте лучше — `B&W\16_ЧТО_В_АГЕНТЕ_ЛУЧШЕ.md`. Подробности про канал — `API\SKILL_creo_api_ecosystem.md` § «СТОРОННИЕ ПЛАГИНЫ» |

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
## SKILL_index.md — НЕТ ФАЙЛА