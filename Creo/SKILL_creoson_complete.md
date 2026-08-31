---
name: creoson-complete
system: Creo
description: Use when: любая работа с Creo через CREOSON — имена команд, параметры, JSON-формат, сценарии
when: creoson, creo, автоматизация, JSON API, rename, regenerate, pdf, параметры, спецификация
priority: critical
---
## СТРУКТУРА ФАЙЛОВ CREO (обязательно к исполнению)
- Деталь — .prt, сборка — .asm, чертёж — .drw, формат — .frm, сечение — .sec,.layout — .lay.
- На диске к имени добавляется версия: korpus.prt.3; в командах CREOSON файл указывается БЕЗ версии: korpus.prt.
- Расширения .cre НЕ СУЩЕСТВУЕТ — не выдумывать. Команды «CREOSON RENAME» в bash НЕ СУЩЕСТВУЕТ.
- Переименование: команда file:rename, data {"file": "old.prt", "new_name": "new", "rename_dependencies": true}; чертёж отдельно: file:rename {"file": "old.drw", "new_name": "new"}.
- Истина по CREOSON — СЫРОЙ ответ живого сервера (TEST-first), а не справка. PTC-хелп (support.ptc.com/help/creo) — только в последнюю очередь.

# CREOSON — ПОЛНАЯ КАРТА API (сервер 3.0, JSON поверх JLINK)

== 1. АРХИТЕКТУРА ==

Твой код / ИИ-агент
  |  HTTP POST JSON
CREOSON Server  http://127.0.0.1:8080/creoson
  |  JLINK (PTC API)
Creo Parametric (3.0+, лучше всего 8–12)

Источники: github.com/SimplifiedLogic/creoson | creoson.com/functions.html
Python-обёртка: pip install creopyson (github.com/Zepmanbc/creopyson, docs: creopyson.readthedocs.io)

== 2. ЗАПРОС И ОТВЕТ ==

Запрос:
    {"sessionId": "...", "command": "file", "function": "open",
     "data": {"file": "my.prt", "display": true}}

- sessionId берётся ОДИН РАЗ через connection:connect и переиспользуется во всех запросах;
  при ошибке со словом "session" — реконнект и повтор.
- command = группа, function = функция группы, data = параметры.

Ответ:
    {"status": {"error": false}, "data": {...}}
    при ошибке: {"status": {"error": true, "message": "..."}}

== 3. ГРУППЫ КОМАНД ==

-- connection --
connect {} → sessionId (ПЕРВЫМ вызовом)
disconnect {}
is_creo_running {} → {"running": true}
start_creo {"bat_file": путь}
stop_creo {} | kill_creo {}

-- file (ГЛАВНАЯ) --
open {"file","dirname","display","activate"}
save {"file","filename"}
rename {"file","new_name","rename_dependencies":true}
regenerate {"file"}
list {} → файлы в сессии (data.file_list / filelist / files)
exists {"file"}
get_active {} → data строкой или {"file": ...}
get_fileinfo {"file"}
display | erase | erase_not_displayed | close_window {"file"}
assemble {"files":[...]}
backup {"file","dirname"}
massprops {"file"} → mass, volume, area/surface_area, density
open_errors {"file"}
relations_get | relations_set {"file","relations"}
postregen_relations_get | postregen_relations_set
get_accuracy | get_length_units | get_mass_units
set_length_units | set_mass_units {"units"}
get_transform | list_simp_reps | has_instances | list_instances
list_materials | get_cur_material | set_cur_material | load_material_file | delete_material
refresh | repaint

-- drawing --
create {"template","model","drawing","scale"}
add_model {"drawing","model"} | delete_models
regenerate {"drawing"} | regenerate_sheet {"sheet": 0 = все}
list_models | get_cur_model | set_cur_model
list_views | list_view_details | create_gen_view | create_proj_view
delete_view | rename_view | scale_view | get_view_loc | set_view_loc
get_view_scale | get_view_sheet | view_bound_box
add_sheet | delete_sheet | select_sheet | get_cur_sheet | get_num_sheets
get_sheet_format | set_sheet_format | get_sheet_size | scale_sheet
create_symbol | load_symbol_def | list_symbols | delete_symbol_inst | delete_symbol_def

-- creo --
pwd {} → рабочая папка (data = строка ИЛИ {"directory"})
cd {"dirname"}
list_files {"filename": маска} → data.file_list / files
list_dirs | mkdir | rmdir | delete_files
get_config {"name"} → data.values (список значений)
set_config {"name","value"}
get_std_color | set_std_color
set_creo_version {"version": 12}  ← ОБЯЗАТЕЛЬНО для Creo 7+ (иначе падают file:regenerate, file:assemble, feature:*, familytable:replace)

-- parameter --
list {"file"} → data.param_list (name, type, value, designate, description)
set {"file","name","value","type": STRING|DOUBLE|INTEGER|BOOL|NOTE, "no_create"}
delete | copy | exists | set_designated

-- dimension --
list | list_detail {"file","name","dim_type": linear|radial|diameter|angular}
set {"name","value"} | set_text | copy | show | user_select

-- feature --
list | suppress | resume | delete | rename
list_params | set_param | delete_param | param_exists
list_group_features | list_pattern_features | user_select_csys

-- bom --
get_paths {"file","paths":false,"top_level":false,"exclude_inactive":false}
→ дерево: file, children[], seq_path (root.3.2); НЕ суй children списком в walk — корень это dict

-- interface --
export_pdf {"file","filename","dirname","use_drawing_settings":true,"sheet_range":"all"}
export_3dpdf | export_image {"width","height","dpi"} | export_file {"file_type": STEP|IGES}
export_program | import_file {"filename","new_model_type": asm|prt} | import_program
mapkey {"script"}  ← тяжёлая артиллерия для того, чего CREOSON не умеет
plot {"driver": POSTSCRIPT|JPEG|TIFF}

-- familytable --
list | list_tree | get_header | get_row | get_cell | set_cell
exists | add_inst | create_inst | delete_inst | delete | replace | get_parents

-- layer --
list | exists | show {"show":true|false} | delete   (статусы: BLANK, DISPLAY, HIDDEN, NORMAL)

-- note --
list | get | set {"value","location"} | delete | copy | exists

-- view --
list | list_exploded | activate | save

-- geometry --
bound_box | get_edges | get_surfaces

-- windchill --
authorize | list_workspaces | set_workspace | create_workspace | clear_workspace
delete_workspace | list_workspace_files | file_checked_out | server_exists | set_server

-- server --
pwd → папка сервера CREOSON

== 4. СЦЕНАРИИ (выверены) ==

Подключение (первым вызовом):
    POST /creoson  {"command":"connection","function":"connect","data":{}}
    → sessionId во все следующие запросы.

Открыть + масса:
    file:open {"file":"korpus.prt","display":true}
    file:massprops {"file":"korpus.prt"} → data.mass (кг)

Параметры:
    parameter:list {"file":"korpus.prt"} → data.param_list

Умное переименование (деталь + чертёж + сборки):
    1 file:open деталь, чертёж и все найденные сборки
    2 file:rename {"file":old.prt,"new_name":new,"rename_dependencies":true}
    3 file:rename {"file":old.drw,"new_name":new,"rename_dependencies":true}
    4 drawing:regenerate {"drawing":new}
    5 file:regenerate + file:save по каждой сборке
    6 file:save деталь и чертёж
    (в агенте — один инструмент creo_rename_model)

PDF:
    interface:export_pdf {"file":"chertezh.drw","dirname":"Z:/PDF_out","use_drawing_settings":true}

Чистка склада версий:
    creo:list_files → группы имя.prt.N → удалить все кроме последней
    (в агенте — creo_purge_versions)

Аудит папки:
    creo:pwd → creo:list_files → для каждого .prt/.asm:
    file:open → parameter:list (ОБОЗНАЧЕНИЕ/НАИМЕНОВАНИЕ/MASS) → file:relations_get
    → file:erase, если не была открыта до аудита
    (в агенте — creo_audit_folder)

== 5. ТИПИЧНЫЕ ОШИБКИ ==

| Симптом | Причина | Лечение |
|---|---|---|
| session expired / invalid session | sessionId протух | новый connection:connect и повтор |
| file not found | не та папка | creo:pwd, проверить рабочую папку |
| file already open | уже в сессии | file:erase перед повторным open |
| regenerate failed | битые relations | file:relations_get, чинить код |
| export_pdf пустой | нет активного чертежа | drawing:list_models, выбрать |
| data пришла строкой, а не dict | creo:pwd, file:get_active так отвечают | обрабатывать оба варианта |
| список файлов пуст при живом Creo | разные ключи ответа | проверять file_list / filelist / files |

== 6. ЧЕГО НЕ УМЕЕТ ==

- сложные сборки с нуля (только file:assemble)
- прямое правки 3D-геометрии (только параметры / relations / mapkey)
- Creo Simulate
- запись в Windchill (только чтение)
Для остального — interface:mapkey с готовым mapkey-скриптом.