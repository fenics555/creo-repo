# PASSPORT.md

## Описание
Паспорт дома — это актуальное состояние модулей, инструментов и истории развития репозитория D:\AI\repo. 
Является "источником истины" для всей системы.

## МОДУЛИ ДОМА

| Модуль | Описание |
|---|---|
| agent.py | ЯДРО: тонкий вход, поднимает голову, тело и ночь |
| loop.py | ЯДРО: голова и разговор: /ask, guide, диспетчер инструментов |
| http_handlers.py | ЯДРО: тело HTTP: маршруты, токены, щит согласования, раздача витрины |
| agent_sched.py | ЯДРО: ночной цикл и сторож |
| core.py | ЯДРО: лог/трейс, boot_report, двухступенчатая проверка здоровья CREOSON |
| pdf_tools.py | НАПРАВЛЕНИЯ: pdf-глаз: миниатюры fitz, вердикты реестра по mtime |
| harvest_reader.py | НАПРАВЛЕНИЯ: провод глаза к harvest.db, только чтение (mode=ro) |
| rename_tools.py | НАПРАВЛЕНИЯ: план переименования (Creo) |
| creo_ops_tools.py | НАПРАВЛЕНИЯ: делегат (Creo) |
| scanner.py | НАПРАВЛЕНИЯ: библиотека parse_model_header, донор харвеста |
| harvest.py | РУКИ БЕЗ ИИ: сканер: память harvest.db, CLI --roots/--text/--bench |
| harvest_gui.py | РУКИ БЕЗ ИИ: окно сканера (tkinter), работает без агента |
| purge_versions.py | РУКИ БЕЗ ИИ: чистильщик версий: превью, перенос в backup, PurgeLock |
| purge_gui.py | РУКИ БЕЗ ИИ: окно чистильщика (tkinter) |
| ctl.py | СЛУЖЕБНЫЕ: подъём и снятие агента и creoson (только недостающее) |
| log_clean.py | СЛУЖЕБНЫЕ: автоуборка D:\AI\log по retention.json |
| house_state.py | СЛУЖЕБНЫЕ: состояние дома на старте задачи, только чтение |
| STOP_ALL.ps1 | СЛУЖЕБНЫЕ: снятие процессов по маске и night_enable=0 одной кнопкой |
| GIT_SYNC.bat | СЛУЖЕБНЫЕ: синхронизация двух корней под гит |
| GIT_SYNC_REPO.bat | СЛУЖЕБНЫЕ: синхронизация двух корней под гит |
| web\app.js | ВИТРИНА: интерфейс инженера на порту 8765 |
| index.html | ВИТРИНА: интерфейс инженера на порту 8765 |
| pdf_refresh_batch.py | в работе |
| agent.sqlite | БАЗЫ И СОСТОЯНИЕ (data\): agent.sqlite, harvest.db, harvest.lock, agent.pid, kb_roots.txt, users.json, secrets.json, purge_gui_settings.json, harvest_gui_settings.json |
| harvest.db | БАЗЫ И СОСТОЯНИЕ (data\): agent.sqlite, harvest.db, harvest.lock, agent.pid, kb_roots.txt, users.json, secrets.json, purge_gui_settings.json, harvest_gui_settings.json |
| agent.pid | БАЗЫ И СОСТОЯНИЕ (data\): agent.sqlite, harvest.db, harvest.lock, agent.pid, kb_roots.txt, users.json, secrets.json, purge_gui_settings.json, harvest_gui_settings.json |
| kb_roots.txt | БАЗЫ И СОСТОЯНИЕ (data\): agent.sqlite, harvest.db, harvest.lock, agent.pid, kb_roots.txt, users.json, secrets.json, purge_gui_settings.json, harvest_gui_settings.json |
| users.json | БАЗЫ И СОСТОЯНИЕ (data\): agent.sqlite, harvest.db, harvest.lock, agent.pid, kb_roots.txt, users.json, secrets.json, purge_gui_settings.json, harvest_gui_settings.json |
| secrets.json | БАЗЫ И СОСТОЯНИЕ (data\): agent.sqlite, harvest.db, harvest.lock, agent.pid, kb_roots.txt, users.json, secrets.json, purge_gui_settings.json, harvest_gui_settings.json |
| purge_gui_settings.json | БАЗЫ И СОСТОЯНИЕ (data\): agent.sqlite, harvest.db, harvest.lock, agent.pid, kb_roots.txt, users.json, secrets.json, purge_gui_settings.json, harvest_gui_settings.json |
| harvest_gui_settings.json | БАЗЫ И СОСТОЯНИЕ (data\): agent.sqlite, harvest.db, harvest.lock, agent.pid, kb_roots.txt, users.json, secrets.json, purge_gui_settings.json, harvest_gui_settings.json |
| agent | ЛОГИ: D:\AI\log\agent |
| harvest | ЛОГИ: D:\AI\log\harvest |
| purge | ЛОГИ: D:\AI\log\purge |
| pdfrefresh | ЛОГИ: D:\AI\log\pdfrefresh |
| reports | ЛОГИ: D:\AI\log\reports |
| urn | ЛОГИ: D:\AI\log\urn\<имя> |
| cleaner | ЛОГИ: D:\AI\log\cleaner |
| MANIFEST.md | ПАМЯТЬ ДОМА (D:\AI\repo): MANIFEST.md, SKILL_index.md, SKILL_local_agent_cline.md, crash\, Creo\, DESIGN_davydovka_tokens.md, PROGRESS/SPEC/AUDIT — под гитом, не чистится. |
| SKILL_index.md | ПАМЯТЬ ДОМА (D:\AI\repo): MANIFEST.md, SKILL_index.md, SKILL_local_agent_cline.md, crash\, Creo\, DESIGN_davydovka_tokens.md, PROGRESS/SPEC/AUDIT — под гитом, не чистится. |
| SKILL_local_agent_cline.md | ПАМЯТЬ ДОМА (D:\AI\repo): MANIFEST.md, SKILL_index.md, SKILL_local_agent_cline.md, crash\, Creo\, DESIGN_davydovka_tokens.md, PROGRESS/SPEC/AUDIT — под гитом, не чистится. |
| crash\ | ПАМЯТЬ ДОМА (D:\AI\repo): MANIFEST.md, SKILL_index.md, SKILL_local_agent_cline.md, crash\, Creo\, DESIGN_davydovka_tokens.md, PROGRESS/SPEC/AUDIT — под гитом, не чистится. |
| Creo\ | ПАМЯТЬ ДОМА (D:\AI\repo): MANIFEST.md, SKILL_index.md, SKILL_local_agent_cline.md, crash\, Creo\, DESIGN_davydovka_tokens.md, PROGRESS/SPEC/AUDIT — под гитом, не чистится. |
| DESIGN_davydovka_tokens.md | ПАМЯТЬ ДОМА (D:\AI\repo): MANIFEST.md, SKILL_index.md, SKILL_local_agent_cline.md, crash\, Creo\, DESIGN_davydovka_tokens.md, PROGRESS/SPEC/AUDIT — под гитом, не чистится. |
| PROGRESS/SPEC/AUDIT | ПАМЯТЬ ДОМА (D:\AI\repo): MANIFEST.md, SKILL_index.md, SKILL_local_agent_cline.md, crash\, Creo\, DESIGN_davydovka_tokens.md, PROGRESS/SPEC/AUDIT — под гитом, не чистится. |

## ИСТОРИЯ И ПРАВКИ

| Дата | Спека | Описание |
|---|---|---|
| 14.09.2026 | 34 | Ремонт эпохи роста: паспорт и ридми обновлены с датами, модули актуализированы. |
| 17.09.2026 | 66б-66е | Аудит правил дома, crash-скиллы, МАНИФЕСТ в system-промпт. |
| 20.09.2026 | 100 | Реконструкция PASSPORT.md (восстановление заголовков и структуры). |

---
*Обновлено: 20.09.2026 (Спека 100)*
