# Конспект изучения: ДАВЫДОВКА (CreoJS-приложение «Спецификация») + сопоставление со скиллами CREO

**Статус:** живое чтение, 22.09.2026 (Cline).
**Источник кода:** `D:\AI\ИЗУЧИТЬ\ДАВЫДОВКА\creoJS\creo_bom_js\` (распакован из `creoJS.zip`, 23.5 МБ).
**Скиллы дома:** `D:\AI\repo\Creo\` (прочитаны все 30 файлов).
**Цель:** сверить, что уже описано в скиллах, что нового, и зафиксировать записи о сессиях Creo.

---

## 1. Что лежит в папке (инвентарь, размеры живые)

Давыдовка — веб-приложение, работающее во ВСТРОЕННОМ браузере Creo (Creo.JS) плюс
свой локальный python-сервер. Это НЕ creoson. Несколько страниц-приложений:

| Файл | Байт | Роль |
|---|---|---|
| `creojs.js` / `_creojs.js` | 46 714 / 46 714 | Браузерный мост CreoJS (дубликат): Promise-полифилл + `connector` (RPC через сокет к движку Creo.JS). Текст ошибки при обрыве: `Connection to Creo session lost`. |
| `index.creojs` | 50 270 | Серверный CreoJS-скрипт СПЕЦИФИКАЦИИ (объекты `pfc*`): обход компонентов, чтение параметров, основная надпись, правка параметров, экспорт изображений. |
| `index_rename.creojs` | 134 111 | Серверный CreoJS-скрипт ПЕРЕИМЕНОВАНИЯ: таблицы семейств, mfg-модели, порядок `model.Rename()` → `model.Save()`, backup, `ChangeDirectory`. |
| `index_report.creojs` | 53 181 | Серверный CreoJS-скрипт ОТЧЁТОВ/изображений: batch-съёмка окон, фон, конфиг-опции, восстановление состояния сессии. |
| `rename.js` | 312 813 | UI-логика страницы «Переименование» (граф ссылок). Зовёт сервер `http://127.0.0.1:8000` и CreoJS. |
| `index.html` / `index_rename.html` / `index_report.html` | 123 129 / 14 976 / 57 993 | Три страницы (плюс одноимённые `.css`). |
| `server.py` | 79 461 | Локальный HTTP-сервер на порту **8000**: раздаёт файлы + эндпоинты `/api/*`: `save/load-rename-graph-frame`, `rename-copies-frame`, `family-table-frame`, `assembly-copy-workspace-frame`, `import/open/create-excel-frame`, `create-report-excel-frame`, `pdf-info-frame`, `create-test-pdf-frame`, `/api/health`. |
| `excel_export.py` | 26 248 | Запись XLSX-спецификации БЕЗ внешних зависимостей (zip+xml): Формат/Зона/Позиция/Обозначение/Наименование/Количество/Примечание/Изображение. |
| `excel_import.py` | 5 398 | Чтение спецификации из XLSX (`read_specification_xlsx`). |
| `family_table_file.py` | 9 741 | Чтение дерева таблицы семейств ПРЯМО ИЗ ФАЙЛА модели (секция `FamilyInf`, теги имён `e3`/`1f`) — без сессии Creo и без загрузки исполнений. |
| `documentation_types.js` | 368 | Справочник типов документов: СБ, ГЧ, МЭ, МЧ, ТУ, ПМ. |
| `title_block_surnames.js` | 447 | Справочник фамилий основной надписи (разраб/пров/тконтр/нконтр/утв). |
| `python\` | — | Портативный CPython 3.13 (`python313.zip`, `python313._pth`, `*.pyd`). |
| `vendor\` | — | Pillow 12.3.0, pypdf 6.14.2, reportlab 5.0.0. |
| `pdf_templates\` | — | `bom_page_1/2/last.pdf`, `.tif`, `Фрагмент.frw`. |
| `assets\fonts\GostAproe.ttf` | — | ГОСТ-шрифт для PDF. |
| `start_server.bat` | 404 | Пуск сервера `127.0.0.1:8000` на портативном питоне. |

## 2. Архитектура (как это работает)

- **Порт 8000** — локальный python-сервер приложения (спецификация/переименование/отчёт).
  В доме этот же порт 8000 занят `copy-server` (см. `SKILL_creostart_fleet.md`).
- **CreoJS-канал**: страница в браузере Creo → `creojs.js` (мост) → движок Creo.JS → серверные
  скрипты `*.creojs`, которые зовут родное API `pfc*`. Родной API и CREOSON — два канала
  к **одной** сессии Creo (см. `SKILL_creojs_api.md`).
- **Серверные скрипты** (`*.creojs`) — то, что в доме заменяет CREOSON-вызовы:
  `pfcGetCurrentSession()`, `session.ChangeDirectory`, `assembly.ListItems`,
  `model.Rename()`, `model.Save()`, `drawing.ListViews`, `ExportCurrentRasterImage`.

## 3. Сопоставление со скиллами (что уже описано, что нового)

### Уже описано (сверено, расхождений нет)
- `SKILL_davydovka_creoson_map.md` — карта операций Давыдовки ↔ CREOSON. Верно:
  мануфактуринг (`creoRenameManufacturingInfo`, fixture) в CREOSON ОТСУТСТВУЕТ; подтверждено —
  в `index_rename.creojs` есть своя обработка mfg (`creoRenameIsManufacturingModel`, `item.mfg`).
- `SKILL_creojs_api.md` — таблица Давыдовка↔родное API↔CREOSON (Session, Directories, Model
  Operations, Family Tables, Export). Совпадает с реальным кодом `*.creojs`.
- `SKILL_creoson_rename_mechanism.md` — сессионный rename `onlysession:true` → `file:save`.
  В Давыдовке то же по смыслу: `model.Rename(name)` в памяти → `model.Save()` на диск,
  порядок сохранения снизу вверх (сортировка `renameRank`), старые версии — в backup.
- `SKILL_creoson_sessions_workdirs.md` — сессии/рабочие каталоги CREOSON (см. раздел 4).
- `SKILL_copy_rename.md` — методика копии/переименования, временная папка, спутники `_mfg`.

### Новое (в скиллах не было — внесено в скилл 22.09.2026)
1. **`family_table_file.py` — чтение таблицы семейств из файла модели без Creo-сессии**
   (секция `FamilyInf`, имена после байт `e3`/`1f`; проверено на Pro/E-, Creo 8, Creo 13).
   Дешёвый способ получить строки семейства, НЕ загружая исполнения в Creo.
2. **Паттерн гигиены сессии** в `index_report.creojs`: сохранить `originalDirectory`,
   `ChangeDirectory`, сменить фон/конфиг-опции, снять изображения, ВОССТАНОВИТЬ фон/конфиг,
   вернуть рабочую папку, активировать прежнее окно. Не оставлять сессию инженера в чужом
   состоянии (перекликается с правилом 16.5 `SKILL_creo_cards.md`).
3. **Давыдовка — ОДНОсессионная**: весь код идёт через `pfcGetCurrentSession()`; выбора
   инстанса Creo и работы с несколькими сессиями НЕТ. «Batch» в отчётах — пакетная съёмка
   окон в ТОЙ ЖЕ сессии, а не новый Creo.
4. Полный инвентарь кода с размерами и ролями (раздел 1) — перенесён в скилл.

## 4. Записи о сессиях Creo (несколько сессий, переключение, закрытие)

Не из Давыдовки, а из дома-скиллов (`SKILL_creoson_sessions_workdirs.md`), пробы 17–19.09.2026:

- **Сколько сессий видит CREOSON:** один JVM creoson держит JLINK к **одному** Creo. Второй
  запущенный Creo этому серверу НЕ доступен — нужен второй creoson на своём порту.
- **sessionId** — ручка СЕССИИ CREOSON, а не выбор инстанса Creo: два `connection:connect`
  дают разные sessionId, но видят один и тот же Creo (`creo:pwd` и `file:list` совпадают).
- **Переключение:** между ИНСТАНСАМИ Creo средствами одного CREOSON переключиться нельзя.
  Переключение рабочей папки — `creo:cd {dirname}`; оно НЕ перепривязывает уже загруженные
  модели (`file:open` по имени отдаёт модель ИЗ ПАМЯТИ). К какому Creo прицеплен сервер —
  сверять `creo:pwd` + `file:list` с ожиданием.
- **Запуск нескольких сессий:** `connection:start_creo` поднимает ВНЕШНИЙ `nitro_proe_remote.bat`
  (только это имя разрешено), но при живом Creo отказывает `Creo is already running`. Второй
  инстанс в пробе поднимали ПРЯМО обёрткой (`cd /d <папка>` + `start "" parametric.exe`).
  Скрытый старт: ключи `-g:no_graphics -i:rpc_input` (проверено по `CommandLine` xtop).
- **Закрытие:** `connection:stop_creo` закрывает ТОЛЬКО прицепленный Creo (в доме — лишь по
  слову пользователя). `connection:kill_creo` бьёт `xtop.exe`+`nmsd.exe` ПО ИМЕНИ = ВСЕ
  инстансы и рвёт JLINK (JVM падает `hs_err`), в доме запрещён. Адресно один инстанс —
  `Stop-Process -Id <pid>` (PID из `Get-Process xtop`), только по слову пользователя.
- **Второй инстанс на машине** = риск «снести» чужую сессию: пишущую операцию делать лишь
  после сверки `creo:pwd` с целевой папкой.

## 5. Выводы

- Давыдовка и дом-CREOSON решают одни и те же задачи двумя мостами: CreoJS (в браузере Creo)
  и CREOSON (JSON поверх JLINK). Механику переносить, UI не тащить (правило в
  `SKILL_davydovka_creoson_map.md`).
- Долг Д4 темы (каскад деталь+чертёж+владельцы на копиях, обходной путь mfg) — закрыт 17.09.
- Новое внесено в `SKILL_davydovka_creoson_map.md` 22.09.2026 (инвентарь, `family_table_file.py`,
  гигиена сессии, односессионность Давыдовки).