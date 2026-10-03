# 15. КАТАЛОГ ПРОВЕРОК SMARTUPDATE: 52 проверки модели (что вендор считает нужным проверять)

_03.10.2026, Cline. Источник: `D:\AI\log\urn\bw\x\SmartUpdate\app\docu\su_adminguide_en\su_en_check_*.html`
(52 страницы), выжимка — `D:\AI\log\urn\bw\su_checks.txt` (скрипт `scan_checks.py`)._

## Почему это главный документ переноса
Плагины дают «как делать», а вендорский каталог проверок даёт **«что вообще имеет смысл
контролировать в модели»** — готовый перечень от индустрии, а не от нас. Ровно то, чего не хватает
движку правил агента.

## Что умеет каждая проверка (есть «Check» и часто «Update»)
По страницам видно общий принцип вендора: **почти каждая проверка не только ищет нарушение,
но и умеет исправить** (Update functions). То есть проверка = «найти и починить».
**Для дома это правильная модель:** не «красное сообщение», а «нашёл и предложил/сделал».

## Полный перечень 52 проверок (сгруппирован)
### Модель и параметры
`accuracy` (точность), `parameter` (параметры), `parameterquery`, `config_option`,
`failed_relations` (непрошедшие отношения), `relation` (отношения), `import_relation`,
`regeneration` (регенерация), `material`, `common_properties`,
`domain_and_category_properties`, `result_status`, `overwritten_dim_value`,
`skip_check_and_update`, `unit` (единицы), `insert_mode`, `cross_sections`.
### Имена и структура
`model_name_format` (формат имени!), `PTC_COMMON_NAME`, `model_setup`, `model_is_skeleton`,
`inseparable_assemblies`, `family_tables`, `feature`, `body`, `orientation`.
### Чертежи и графика
`drawing_actuality` (актуальность), `drawing_format`, `drawing_models`, `drawing_note`
(примечания!), `drawing_program`, `drawing_scale`, `drawing_size`, `drawing_view`,
`number_of_sheets` (число листов), `annotation`, `symbol`, `dimension`, `dim_missing_ref`,
`layer`, `layer_state`, `layer_view_dep`, `dimension` (размеры).
### Комбинации состояний и правила
`comb_state` (комбинированные состояния — «одна деталь, разные сборки»).
### Запуск внешних проверок
`run_mapkey` (прогнать mapkey), `run_modelcheck` (ModelCHECK), `run_SMARTColor`
(прогнать правила цвета) — **модуль умеет вызывать другие проверки как шаги**.
### Спецпроверки (с лицензией)
`SDA` (Smart Design Analyzer — сбор статистики по модели в базу!), `tolerance_standard`,
`tolerance_tables`, `simp_rep`.

## Что отсюда берём в агента (выборка с обоснованием)
| Проверка вендора | У нас есть? | Действие |
|---|---|---|
| `model_name_format` | частично (`cmnm_scan` — внутренние имена) | добавить проверку **имени файла** по `SKILL_naming_spec` |
| `failed_relations` | частично (`creo_get_relations`, `trail_*`) | `relations_check` — **приоритет 1 из плана** |
| `parameter` + `parameterquery` | `make_lst`, `creo_get_params`, `config_audit` | связать в один отчёт «параметры vs ограничения vs факт» |
| `drawing_note` | **нет** | аудит плашек/примечаний по чертежу (приоритет 3 плана) |
| `drawing_actuality` | **есть и лучше** — `pdf_status`/`creo_pdf_scan` дают вердикт по PDF | наша версия даже практичнее |
| `regeneration` | `creo_regenerate`, `trail_trend` | добавить «модель регенерируется с ошибкой» в трейл-анализ |
| `material` | `plm_reader` (читает материал из файла) | **наш метод лучше** — не нужен Creo |
| `model_is_skeleton`, `inseparable_assemblies` | **нет** | признаки модели уже читает `plm_reader` — добавить флаги |
| `layer` / `layer_state` | **нет** | логи слоёв читаются из файла модели |
| `number_of_sheets` | частично (PDF-страницы `pdf_pages`) | считать листы чертежа |
| `accuracy` | `creo_get_params` | быстрый отчёт по точности/единицам |
| `run_mapkey` | `creo_mapkey` (одна команда) | сценарии mapkey как набор шагов проверки |

## Вывод
Вендор разбил проверки на **предметные группы** (модель / имя / чертёж / правила / внешние) и
сделал каждую **исправляемой**. Наш движок правил должен уметь то же: проверка = условия +
действие («подсветить» / «исправить» / «записать в отчёт»).