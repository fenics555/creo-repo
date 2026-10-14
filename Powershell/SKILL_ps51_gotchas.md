---
name: ps51-gotchas
system: Команды
description: Use when: PowerShell-скрипт падает с ошибкой парсинга, не запускается или ломается на кириллице
when: powershell, ps1, кириллица, UTF-8, encoding, кодировка, ExecutionPolicy, Bypass, NoProfile, парсинг, ошибка скрипта, policy
date: 14.10.2026
priority: high
---

# ГРАБЛИ POWERSHELL 5.1 ДОМА

1. **Кириллица в UTF-8 ломает PowerShell 5.1.** Живой факт (14.10.2026, PLM Reader):
   скрипты `sync_to_share.ps1` / `sync_check.ps1` с русскими комментариями и сообщениями
   в UTF-8 падали в PS 5.1. ЛЕЧЕНИЕ: пересоздать скрипт **ASCII-only** (комментарии и вывод
   по-английски). Русский verbatim в консоль не несёт и так (MANIFEST, п.6) — русское в файлы
   кладётся через редактор, не через скрипт.
2. **Стандартный запуск из любого окна / планировщика / агента:**
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\script.ps1
   ```
   `-NoProfile` снимает чужие профили, `Bypass` — политику выполнения. В доме это норма, а не
   «обход защиты»: скрипты дома свои.
3. **Кодировка вывода:** если скрипт печатает наружу — `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`
   (см. `INDEX\find_skill.ps1`), иначе кириллица в выводе превращается в кракозябры.
4. **Что чинить, а что нет:** два отказа одного пути = смена метода (MANIFEST, п.7). Ковыряться
   третий раз в упавшем .ps1 запрещено — переписывай ASCII-only или переводи работу на python.
