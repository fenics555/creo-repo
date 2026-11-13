---
name: creo-read-relations-family
system: Creo
description: ИЗВЛЕЧЕНИЕ Relations, Family Table и внешних ссылок (MdlRefInfo) напрямую из бинарного файла.
when: relations, equations, family table, FamilyInf, MdlRefInfo, external references, links, base_part
priority: critical
date: 13.11.2026
---
# ИЗВЛЕЧЕНИЕ ОТНОШЕНИЙ, СЕМЕЙСТВ И ССЫЛОК — ЧТЕНИЕ ИЗ ФАЙЛА

## 1. ОБЩАЯ ЛОГИКА
Чтение выполняется через анализ секций, определенных в `#UGC_TOC`. Для извлечения текстовых данных (Relations, Family Table, Names) используется поиск маркеров внутри секций `LargeText` и `FamilyInf`.

## 2. СЕКЦИИ И МАРКЕРЫ

### 2.1. Relations (Уравнения)
* **Секция:** `LargeText`
* **Формат:** Текст уравнений, часто начинающийся с конструкций `/*if`, `/*else`, `/*endif`.
* **Кодировка:** UTF-8 или CP1251.
* **Особенность:** Необходимо искать внутри `LargeText` паттерны уравнений, игнорируя служебный мусор.

### 2.2. Family Table (Семейства)
* **Секция:** `FamilyInf`
* **Маркеры:** `Sld_FamilyInfo`, `instances_data`, `values_xar`.
* **Структура:**
    * `instances_data` → дерево имен исполнений.
    * `values_xar` → таблица значений параметров.
* **Примечание:** Использовать логику из `SKILL_creo_read_family.md`.

### 2.3. Внешние ссылки (Links / BOM)
* **Секция:** `MdlRefInfo`
* **Маркеры:** `component`, `filename` (или пути к файлам).
* **Цель:** Извлечение списка компонентов, входящих в сборку, и их имен.

## 3. ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ
* **Кодировки:** Всегда пробовать `utf-8` -> `cp1251`.
* **Инструментарий:** `creo_read.py` (primitives: `parse_toc`, `read`).
* **Запреты:** Не использовать CREOSON/J-Link для этого этапа (только прямое чтение).

## 4. СТАТУС
* [ ] Разработан парсер.
* [ ] Протестирован на `00080-00.asm`.
* [ ] Протестирован на `23-1017gri-01.prt.1`.
