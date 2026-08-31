---
name: creo-commands
system: Creo
description: Use when: быстрый подбор команды CREOSON под задачу
when: creoson, команда, что вызвать, rename, regenerate, pdf, параметры
priority: high
---

# БЫСТРЫЙ ВЫБОР КОМАНДЫ CREOSON

Полная карта со всеми параметрами — в SKILL_creoson_complete.md.
Здесь — «хочу сделать X -> какую команду вызвать».

## Узнать о Creo

- Creo жив? -> connection:is_creo_running
- sessionId (первым вызовом) -> connection:connect
- Запустить/остановить -> connection:start_creo / stop_creo / kill_creo

## Модели

- Открыть -> file:open {"file","dirname","display"}
- Сохранить -> file:save
- Переименовать -> file:rename {"file","new_name","rename_dependencies":true}
- Регенерировать -> file:regenerate
- Активная модель -> file:get_active
- Список в сессии -> file:list
- Есть ли файл -> file:exists
- Масса/объём -> file:massprops
- Ошибки открытия -> file:open_errors
- Relations читать/писать -> file:relations_get / relations_set
- Выгрузить из памяти -> file:erase

## Чертежи

- Создать -> drawing:create {"template","model"}
- Добавить модель -> drawing:add_model
- Регенерировать -> drawing:regenerate
- Модели в чертеже -> drawing:list_models
- Виды -> drawing:list_views / create_gen_view / scale_view

## Параметры и размеры

- Список параметров -> parameter:list
- Установить -> parameter:set {"name","value","type"}
- Размеры -> dimension:list / dimension:set

## Элементы, спецификация, таблицы

- Элементы -> feature:list / suppress / resume
- Дерево сборки -> bom:get_paths
- Семейные таблицы -> familytable:list / create_inst / exists

## Конфигурация и файлы

- Рабочая папка -> creo:pwd (data может прийти строкой ИЛИ словарём)
- Сменить папку -> creo:cd
- Список файлов -> creo:list_files (ключи: file_list / filelist / files)
- Config-опции -> creo:get_config / set_config
- Для Creo 7+ обязательно -> creo:set_creo_version

## Экспорт/импорт

- PDF -> interface:export_pdf {"use_drawing_settings":true}
- STEP/IGES -> interface:export_file
- Картинка -> interface:export_image
- Mapkey (тяжёлая артиллерия) -> interface:mapkey

## Типовые сценарии

Умное переименование (в агенте: creo_rename_model):
    file:open деталь+чертёж+сборки
    file:rename деталь (rename_dependencies:true)
    file:rename чертёж (rename_dependencies:true)
    drawing:regenerate чертёж
    file:regenerate + file:save по каждой сборке
    file:save деталь и чертёж

Чистка склада версий (в агенте: creo_purge_versions):
    creo:list_files -> группы имя.prt.N -> удалить все кроме последней

Аудит папки (в агенте: creo_audit_folder):
    creo:pwd -> creo:list_files -> для каждого .prt/.asm:
    file:open -> parameter:list -> file:relations_get -> file:erase

## Чего НЕ умеет CREOSON

- сложные сборки с нуля (только file:assemble)
- прямая правка 3D-геометрии (через параметры/relations/mapkey)
- Creo Simulate; запись в Windchill (только чтение)