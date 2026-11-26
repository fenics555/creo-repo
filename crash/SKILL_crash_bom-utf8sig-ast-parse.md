---
name: crash_bom-utf8sig-ast-parse
system: CRASH
description: Use when: ast.parse или compile падает на файле с BOM (SyntaxError invalid non-printable character U+FEFF), хотя файл «нормальный»
when: bom, utf-8-sig, U+FEFF, ast, parse, SyntaxError, non-printable, check-script
date: 26.11.2026
executor: Cline
task: нога A сторожа (регресс-тест kind<->SKILL_MAP)
---

ОШИБКА (дословно, для grep):
  SyntaxError: invalid non-printable character U+FEFF
  (строка 1, при ast.parse исходника, у которого в начале BOM)

СИМПТОМ: проверочный скрипт читает исходник и вызывает `ast.parse(src)` — падает на пустом месте: «invalid non-printable character U+FEFF» в строке 1. При этом сам файл компилируется нормально (`py_compile OK`), редактор и `read` его видят. Ошибка только в скриптах, которые парсят исходник через `ast`.

ПРИЧИНА: `open(path, encoding="utf-8")` **сохраняет BOM** (символ U+FEFF) в начале строки. `ast.parse`/`compile` не допускают BOM в строке-источнике (в отличие от самого `py_compile`, который читает файл с учётом кодировки). Аналогичная ловушка — любой парсер текста (regex по началу строки, JSON без `utf-8-sig`).

ПРОФИЛАКТИКА:
1. Читать исходники для `ast.parse` через `open(path, encoding="utf-8-sig")` — BOM снимается автоматически.
2. Если файл может быть и с BOM, и без — `utf-8-sig` безопасен в обоих случаях.
3. То же для `json.load` файлов, созданных `editor` (он может писать BOM при кириллице).

ПОВТОРЫ: 1
