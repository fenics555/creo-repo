# Конспект изучения: B&W Plugins Suite (SMART-модули для Creo)

**Статус:** чтение архива, без установки. Начат 03.10.2026 (Cline).
**Источник:** `D:\Интернет\B&W.Plugins.Suite.for.PTC.Creo.4.0-13.4.Win64-SSQ`
**Цель:** понять, что это за допы к Creo, как они встают в Creo, что из этого может быть
полезно дому (дом работает на CREO13 13.4.1.0).
**Карта скиллов дома:** `D:\AI\repo\SKILL_index.md`, вход темы Creo —
`D:\AI\repo\Creo\SKILL_creo_index.md`.

**Где живёт конспект:** `D:\AI\repo\B&W\` (отдельная папка-направление по слову хозяина).

---

<!-- ПРОГРЕСС -->
**Ход изучения:** прочитан весь архив по верхам (15 модулей × версии), все 74 `readme.txt`
одного шаблона, все 66 `license.ini`, Changelog-файлы модулей, проверено окружение дома
(установка Creo, `config.pro`, VERICUT-регистрация, таблицы отверстий, службы Flex).
Установка НЕ выполнялась. Дальше по желанию хозяина: (1) распаковка `SmartAssembly`/`SmartPDX`
ISO и чтение AdminGuide/UserGuide.chm; (2) прототип установки одного модуля в урне;
(3) аудит `config.pro` под добавление `protkdat` · _обновлено 03.10.2026 (Cline)_
<!-- /ПРОГРЕСС -->

## 1. Что это (дословно из файлов)
_03.10.2026, Cline_

Набор **B&W Plugins Suite** от **B&W Software GmbH** — 15 продуктов семейства SMART\*.
Лежит НЕ как набор файлов Creo, а как **инсталляторы под каждую версию Creo**
(папка `<продукт>\<версия> for Creo X.Y>`), плюс один **общий лицензионный сервер**
`BUW_Flex_Server_11.19.8_x64.7z` (4.08 МБ) и `z_checksums.sfv` (QuickSFV, 10.06.2026).
Вендор прямо упоминается в Changelog SMARTOptics: «Add Additional Tools information offered
by B&W Software GmbH» (7.0.4.0).

Топ-файлы архива: `readme_SSQ.txt` (452 б), `z_checksums.sfv` (49 КБ), `BUW_Flex_Server…7z`.

**Нужен ли скилл?** да — тело `SKILL_BW_PLUGINS.md` в этой папке, в `SKILL_CHARGE` пока не внесён.

## 2. Механика установки — одна на все 15 модулей
_03.10.2026, Cline_

Дословно из `_SolidSQUAD_\readme.txt` (одинаково во всех папках, отличается только именем продукта):
1) распаковать `BUW_Flex_Server_11.19.8_x64` в короткий путь и **от админа** запустить
   `server_install.bat` → ставится служба **«BUW License Server»**;
2) поставить SMART-модуль нужной версии, **лицензию на этапе setup НЕ настраивать**;
3) скопировать `_SolidSQUAD_\license.ini` в `<продукт>\bin`;
4) **регистрация в Creo — через `protk.dat`**: если
   `<Creo install>\Common Files\text\protk.dat` НЕТ — скопировать туда `protk.dat` из
   `<продукт>\bin`; если ЕСТЬ — дописать его содержимое в конец существующего.

`license.ini` у всех один и тот же вид (2 строки):
```
LICENSE_FILE 6501@localhost
LICENSETYPE <ПРОДУКТ>_STD_LL
```
где тип = `SMARTHOLECHART_STD_LL`, `SMARTXHATCH_STD_LL`, `SMARTOPTICS_STD_LL`,
`SMARTANNOTATE_STD_LL`, `SMARTMENU_STD_LL`, `SMART3DEXPORT_ADV_FL`, `SMARTCOLOR_DEMO`,
`SMARTMBDTOOLS_ADV_LL`, `SMARTASSEMBLY_STD_LL`, `SMARTDESIGNSERVER_STD_LL`,
`SMARTLIBRARY_STD_LL`, `SMARTUPDATE_STD_LL`, `PROGRESSIVE_DIES_STD_LL` (SMARTPDX!).

**Ключевое для дома:** канал подключения — **Pro/TOOLKIT (`protkdat`)**, тот же самый механизм,
которым в доме подключён VERICUT: в боевом `config.pro` есть строка
`protkdat D:\CGTech\VERICUT 9.0.1\windows64\proev\Creo60\protk.dat`. Значит B&W встанет
ровно тем же способом и в тот же механизм — а `agent\config_audit` уже умеет это проверять.

## 3. Совместимость с домом (дом на CREO13 13.4.1.0)
_03.10.2026, Cline_

Под **13.4** в архиве есть только **три** модуля:
`SmartOptics 13.0.0.0 for Creo 13.4`, `SMARTHolechart 19.4.1.0 for Creo 13.4`,
`SmartMBDTools 13.0.5.0 for Creo 13.4`.
Остальные двенадцать заканчиваются на **12.4** (или 11.0). Шестеро (Smart3DExport, SmartAnnotate,
SmartColor, SmartLibrary, SmartUpdate, SmartMenu) вообще не имеют сборки новее 11.0.

В `D:\PTC\CREO13\Creo 13.4.1.0\Common Files\text\` файла `protk.dat` **нет** (найдены только
в `otk_java_free\*` и `protoolkit\protk.dat`) — то есть при установке B&W он там появится
первым, и «дописывать в существующий» не придётся. Но: `config_audit` проверяет этот путь —
после установки путь должен перестать быть «битым» (это автопроверка установки).

**Нужен ли скилл?** да, `SKILL_BW_PLUGINS.md` § «совместимость» — с таблицей.

## 4. ЖИВАЯ НАХОДКА: SMARTHolechart — прямо в тему «Таблицы отверстий»
_03.10.2026, Cline_

Дом уже изучал `Z:\PTC\CREO-START\НАСТРОЙКИ\ТАБЛИЦА_ОТВЕРСТИЙ\*.hol` и нашёл 4 битые шапки
(GOST_MFZN_ALL без шапки THREAD_DATA; GOST_DK/GK/MK с разорванным `TAPER_ANGLE`) —
конспект `D:\AI\repo\ИЗУЧЕНО\Таблица отверстий\STUDY_NOTES.md`. Ошибка в трейлах:
`!Error while reading hole chart.` + `Cannot get THREAD_DAT`.

SMARTHolechart — это как раз плагин B&W, который этим занимается. Из его Changelog
(версии от 12.x до 19.4.1.0) видно:
- **19.3.0.0**: опция `SHC_LOG_TIME` (время в `holechart.log`) и новый placeholder `SURFACEID` [RM-22881, RM-22875];
- **19.3.0.1**: правило валидации при обновлении таблицы — «число колонок должно совпадать»
  и «заголовки колонок должны иметь те же значения» [RM-23710] — **это ровно те два дефекта,
  которые дом нашёл вручную**; значит у B&W есть эталонная проверка, а у дома — своя;
- **19.3.0.1**: UDF внутри merge-фичи больше не игнорируется, а распознаётся [RM-20581];
- **12.0.1.0/12.0.3.0/12.0.4.2**: `PARAMETER_MUST_EXIST`, `MARK_COS`, падение при «только неизвестные отверстия», лимит 255 символов в опциях (было 32);
- Changelog 12.4→13.4 идёт по одной строке «Supported releases: Creo Parametric X».

**Вывод:** это самый «домашний» модуль из 15. И он единственный из трёх 13.4-модулей,
который напрямую касается проблемы, зафиксированной в доме.

## 5. ЖИВАЯ НАХОДКА: SMARTMBDTools 13.0.5.0 — пересечение с домовыми инструментами
_03.10.2026, Cline_

Единственный модуль под 13.4 с большим Changelog (11 КБ, версии 13.0.0.0…13.0.5.0).
Из 13.0.5.0:
- **«Implement functionalities to rename model elements like features» [RM-24179]** — это
  ровно то, что дом уже делает сам (механизм rename: `SKILL_creoson_rename_mechanism`,
  `creo_comb`/`creo_ops` — переименование с сохранением ссылок, `creoRenameComponentKind`
  у Давыдовки). Конкурент/образец для проверки нашей методики;
- «Add Most Recently Used settings to the Combined state items» [RM-24168];
- «Fixed issue with allowed value list criterion in a parameter definition» [RM-24111] —
  контекст `make_lst`/`SKILL_parameters_guide`;
- «Implement the relation checking and updating functionality» [RM-14929] (13.0.1.0) —
  **проверка и обновление relations**, то есть то, что дом делает скриптами (`RELATIONS\`
  в репо, конституция relations). Реальный образец для сверки наших правил;
- экспорт в PDF с обрезкой геометрии/вставкой объектов, `ModelFromTemplate`, SA-MetaData.

## 6. ЖИВАЯ НАХОДКА: SMARTOptics — единственный модуль, где есть «физика», а не только CAD
_03.10.2026, Cline_

Changelog 7.0.0.0…7.0.4.0: трассировка лучей по поверхностям Creo, проверка точки пересечения
на принадлежность поверхности, базы оптических материалов **SCHOTT, HOYA, OHARA**,
проект хранится в **XML** (с защитой от перезаписи), категории лучей (`diffused` → `split`),
прогресс-диалог, «Additional Tools» от B&W Software GmbH.
13.0.0.0 для 13.4 — правка имён кнопок: `ok_pb` → `ok_pushbutton`, `cancel_pb` →
`cancel_pushbutton`, **mapkey могут потребовать правки** (важно для дома: Давыдовка/свои
программы сидят на mapkey!).

**Вывод:** дом — пресс-формы/литьё/механика, оптика не его профиль. Ценность — как образец
«модуль с реальной физикой и внешними базами данных» и как источник mapkey-расхождений.

## 7. Прочие модули — что видно по Changelog (кратко, для карты)
_03.10.2026, Cline_
- **SmartXhatch** — штриховка на чертежах (pattern hatching, distribute hatching, правила с
  NOT/AND/OR, конфликты с Windchill [RM-21740], «Pattern hatching applied with correct
  values» [RM-22053]). Для дома: сечения деталей пресс-форм на чертежах.
- **SmartUpdate** — пакетное обновление параметров/свойств/relations, batch-диалог,
  работа с семейными таблицами, «Add current model units to a set of parameters», поиск по
  конфигурациям. Для дома: массовое проставление ГОСТ-атрибутов.
- **SmartAnnotate** — стандартные примечания/надписи (ГОСТ/ESKD-плашки), «stack notes»,
  notification center, экспорт/импорт настроек в XML, SQL-интерфейс для stack notes,
  GD&T-боксы. Для дома — **самое близкое к `SKILL_drawings_eskd`**.
- **Smart3DExport** — экспорт 3D/PDF (Advanced, лицензия `ADV_FL`).
- **SmartColor** — цветовая кодировка; лицензия `SMARTCOLOR_DEMO` — **демо**, не STD.
- **SmartElectrode** — электроды пресс-форм: классификация accessory-параметров, ссылочные
  детали, материалы, PDMLink, обработка чертежа по `my_drawing_format.cfg`. Для дома
  (пресс-формы) — **прямо в профиль**, но максимум 12.4/18.4.2.0.
- **SmartMenu** — свой лента-меню вместо стандартной (ribbon), в т.ч. на Creo 4.0–11.
  Для дома: свой интерфейс без правки стандартных mapkey.
- **SmartLibrary** — библиотеки; сборок всего две (7.0/8.0) — модуль почти снят вендором.
- **SmartAssembly / SmartDesignServer** — поставляются **ISO-образами**
  (`B&W.SmartAssembly.12.0.2.0.Win64.iso` 210 МБ, `Smart.PDX.18.0.0.0.Win64.iso` 286 МБ),
  а не exe; по ним в архиве лежат **AdminGuide.chm (1.5 МБ) и UserGuide.chm (700 КБ)** —
  единственная нормальная документация во всём наборе.
- **SmartPDX** — прогрессивные штампы (license type `PROGRESSIVE_DIES_STD_LL`).

## 8. Документация в архиве — что есть
_03.10.2026, Cline_
Всего: 74 `.txt` (74 readme.txt), 72 `.html` (Changelog), 70 `.exe`, 66 `.ini` (license),
7 `.pdf` (whatsnew, только Smart3DExport 7.0 и SmartAnnotate 4.6/5.4/6.2, SmartColor 4.3/5.3/6.3),
2 `.iso`, 2 `.chm`, 1 `.7z`, 1 `.sfv`.
**Русскоязычной документации нет ни одной.** Все 74 readme — один и тот же 4-пунктовый шаблон
установки. Содержательных документов всего два: `AdminGuide.chm` и `UserGuide.chm` (SmartAssembly).

## ЧТО НЕ ПОЛУЧИЛОСЬ (пишется СРАЗУ)
_03.10.2026, Cline · инструмент: PowerShell / python (скрипты в урне)_

1. **Массовый вывод всех Changelog одним проходом обрезался на CSS.** Первая попытка брала
   первые 400 символов после удаления тегов — попала в блок `<style>` и дала бессмыслицу
   («Smart3DExport >> 10.0.0.2 >> body { padding: 30px; }…»). Вторая попытка вырезала блок `<body>`
   и упала на `Substring` с длиной больше строки (Changelog SMARTUpdate 10.3.0.0 — короткий).
   **Вывод:** вырезать не `[<>]`, а конкретный контейнер (`<h1>`/`<body>`) и ограничивать длину
   через `Substring(0, [Math]::Min(n, len))`.
2. **Содержимое инсталляторов не смотрел.** `exe`/`iso` не распаковывал: это шаг с правами и
   распаковкой — только по слову хозяина. Поэтому всё про внутренности (что именно делает
   `protk.dat`, какие DLL, где базы) — пока **гипотеза**, а не факт.
3. **Проверить, что Flex-сервер ставится, не смог** — службы `BUW` в системе нет, а
   `server_install.bat` требует админа и записи в реестр служб.
