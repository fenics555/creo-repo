# 12. КАРТА ВОЗМОЖНОСТЕЙ SMARTHOLECHART (изнутри, по фактам)

_03.10.2026, Cline. Источник: распакованное тело `D:\AI\log\urn\bw\x\holechart\app`._

## Состав пакета (226 файлов)
```
app\
  configure_license.exe (4.3 МБ)   License.txt (8.4 КБ)   Changelog.html
  x86e_win64\  shc190.dll (7.07 МБ) + buw_license_check-11-{10,12,14,16,17,19}.dll
  configuration\  holechart_options.cfg / _tables.cfg / _types.cfg / _threadnames.cfg
                  holechart_formats\ (11 форматов)  holechart_pictures\  symbols_dtl\mm\ (.sym, .gph)
  text\  usascii, german, french, italian, japanese, chinese_cn, chinese_tw
         + text\ribbon\shc_ribbon.rbn (13 КБ) + text\resource\shc_images\
```
**Находки:** DLL одна (`shc190.dll`) на все версии Creo; рядом — **шесть** `buw_license_check`
по версиям (11.10…11.19) — то есть лицензионная проверка версионная. Папки `symbols_dtl\mm\`
— **символы чертежа `.sym` и `.gph`**, которые дом уже умеет читать как формат.

## Что умеет модуль — по трём источникам
### 1. Лента (`.rbn`) — 5 групп по режимам, 17 команд
| Группа (режим) | Смысл |
|---|---|
| `shc_group_standby_mode` | покой: options, info, лицензия |
| `shc_group_asm_prt_mode` | сборка/деталь: создать/обновить таблицу |
| `shc_group_drw_mode` | чертёж: примечания, пересечения |
| `shc_group_drw_managment` | управление: удалить, обновить все, переместить строки |
| `shc_group_excludegeom` | исключение геометрии: исключить выбранное/остальное, показать |
Команды: `create`, `delete`, `update`, `export`, `intersect`, `show_note`, `change_id`,
`notes_auto`, `notes_arrange`, `movetabs`, `movetabrows`, `excludesel`, `excluderessel`,
`excluderesall`, `excludeshow`, `options`, `info`, `licborrow`.

**Дизайн-паттерн (важен для наших окон):** лента разделена **по режимам работы**, а не по
функциям; каждая группа имеет свой набор команд. У нас окна сделаны наоборот (кнопки пачками),
но принцип «показывай только то, что относится к текущему режиму» стоит взять.

### 2. Опции (`shc_opt.txt`, 995 строк) — **170 уникальных настроек**, 24 шаблона-подстановки
Топ-группы опций:
- рисование примечаний: рамка, стрелки, «текст внутри окружности, если диаметр больше N»
  (`ADVANCED_NOTES`);
- цвета поверхностей отверстий: 0/1/2/3 — не красить / красить / непрозрачно / прозрачность 50%
  (`COLOR_HOLES_0…3`);
- выгрузка: создавать ли `.drw` файл, имя из `DRW_FILENAME` (`CREATE_DRW_FILE_0/1`);
- потоки: «различать THREAD (THRU) и THREAD_B (BLIND)» (`CHECK_THREADLENGTH`);
- поверхности как резьба (совместимость ProE16/17), обратное направление плоскости размещения;
- единицы: «конвертировать, если единицы сборки отличаются» (`CONVERT_UNITS`);
- исключения геометрии, координатные системы (новое имя CSYS), размещение строк таблицы.
Шаблоны подстановки (`Wildcards`): `<DEPTH> <DIAMAX> <DIAMIN> <ANGLE> <HALFANGLE>`,
`<MDLNAME> <CSYSNAME> <VIEWID> <VIEWNAME> <TABFORMAT> <TABCHAR> <HOLETYPE> <DIAMETER> <DIR> <DATE> <PARAM=x>`.

**Ценность для агента:** это **готовый список «что имеет смысл настраивать»** для отверстий
и готовый синтаксис шаблонов подстановки — такой же пригодится в наших отчётах по сверке.

### 3. Типы отверстий (`holechart_types.cfg`) — **язык описания отверстия**
Файл написан простым блочным форматом:
```
START_DEF / T_Cy / TYPE THRU / FIRST_ID 0 / CYLINDER
D / D_Tu / D_To / T / − / − / 255.255.128
NC_INFO:  T_Cy <D>
USERFORMAT: <D> | X<X>;Y<Y>
PARAMETER / END_DEF
```
Типы: `T_Cy`, `T_CyCy`, `T_CoCy`, `T_CyCoCy`, `B_CyCo`, `B_CyCyCo`, `T_CyTh`, `T_CoCyTh`,
`B_CyThCo`, `B_CoCyThCo`, `USER`. Обозначения: `T`=сквозное, `B`=глухое, `Cy`=цилиндр,
`Co`=конус, `Th`=резьба.
`holechart_tables.cfg` — описание колонок (`X`,`Y`,`D`,`T`,`D_CB`,`T_CB`,`G`,`X_ANG`,`X_ORIENT`…)
и `holechart_threadnames.cfg` — реальные значения (`G1/2 5.67`, `NG50 90.15` и т.п.).

**Это самая ценная находка для переноса:** тип отверстия — **тип данных с полями**, а не текст.
Значит и наш валидатор `.hol`, и любая будущая таблица должны работать с такой моделью
(тип → набор полей → формат вывода), а не с плоским списком колонок.

### 4. Механизм (из строк DLL)
- `SHC_STARTUP` — точка входа Pro/TOOLKIT; `ptc_exit` — выход;
- `ProMacroLoad_v` / `ProMacroExecute_v` — модуль **сам грузит и выполняет макросы**;
- `ProConfigoptGet_v/Set_v`, `ProConfigoptionGet_v` — у модуля **свои config-опции**;
- RTTI-имена с `ProErrors` — код C++ с обработкой ошибок PTC.