# Репозиторий знаний КБ — D:\AI\repo

Центральное хранилище знаний, стандартов и документации дома CREO-AGENT.
**Обновлено:** 17.09.2026 · **Источник истины:** `PASSPORT.md`

## Состав
- **PASSPORT.md** — состояние и история дома
- **MANIFEST.md** — универсальный закон дома (правила 1-17, читается первым)
- **SKILL_*.md** — скиллы-компетенции по доменам (карта: `SKILL_index.md`)
- **crash/** — прецеденты крахов по шаблону конституции (`SKILL_crash_constitution.md` — документ рамок)
- **AUDIT_rules_*.md** — отчёты аудита правил дома (находки, варианты, вердикты)
- **Creo/**, **Инженерные/**, **Web/**, **1C/**, **Vericut/**, **PDF/** — отраслевые справочники
- **GUIDE/** — руководства по модулям агента
- **Ошибки/ERR_*.md**, **Трейлы/** — журналы ошибок и трейлов

## Структура и права
- Скиллы вносятся только через `write_file` исполнителя или git (правило 10.7); буфер обмена — нет.
- Новые знания рождаются в `D:\AI\tools\agent\data\drafts` и проходят апрув через `drafts_approve`.
- Автогенерируемые файлы руками не правятся: `SKILL_company_config.md` (passport_tools), `Трейлы/TRAIL_JOURNAL.md` (trail_tools), `Ошибки/ERR_*.md`.

## Поиск по знаниям
- `search_kb` — семантический поиск по индексу (34 365 фрагментов на 14.09.2026)
- `find_similar` — поиск похожих моделей по эмбеддингам (40 973 модели)
- `read_file` — чтение файлов в белых корнях

## История правок
- **14.09.2026 — спека 34:** паспорт актуализирован (38 блоков / 133 инструмента, живые цифры матриц), ридми приведены с датами.

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

## ОПЕРАЦИОННЫЙ БЛОК (ПУСК, СТОП, ВЗГЛЯД)

| Действие | Команда / Место | Описание |
|---|---|---|
| **ПУСК** (START) | `python D:\AI\tools\agent\agent.py` | Подъём ядра, HTTP-сервера (8765) и ночного цикла. |
| **СТОП** (STOP) | `powershell D:\AI\STOP_ALL.ps1` | Мгновенная остановка всех процессов агента и Creoson. |
| **ВЗГЛЯД** (VIEW) | `http://localhost:8765` | Витрина: статус агента, логи, управление. |

---
*Обновлено: 19.09.2026 (Спека 100)*

- **17.09.2026 — спеки 66б–66e:** МАНИФЕСТ вошёл в system-промпт агента; аудит правил дома (`AUDIT_rules_20260917.md`) и исполнение его кластеров; crash-скиллы приведены к шаблону конституции; `skills_check.py` — дельта-снапшот, честные проверки, grep-поле ОШИБКА; вход дома: `ensure_admin` из `secrets.json` (дефолт admin/admin снят), TTL токена 24ч; `.clinerules` v5.10 (определение «миграции», протокол ожидания детач-процесса в SKILL_local_agent_cline); М2 уточнён (utf-8 голова близнеца, отчёт задачи — выжимка в чате, полный текст в файле после 2000 знаков).