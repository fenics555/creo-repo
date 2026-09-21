# Creo-Repo (Agent Knowledge Base)

A structured knowledge base and skill set for an AI coding agent (Cline) to work with Creo Parametric and engineering tasks.

## Quick Start

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    ```

2.  **Setup environment**:
    - Copy `.clinerules` from this repository to your `D:\AI` directory (or your agent's root).
    - Ensure your agent has access to the workspace.

3.  **First Message**:
    Start your session by providing the agent with the `.clinerules` and the `MANIFEST.md`.

## Structure

- `D:\AI\repo\`: Main knowledge base, skills, and conventions.
- `D:\AI\tools\agent\`: Agent implementation and tools.
- `D:\AI\log\`: Logs and reports (not part of the repo).

## License

This project is licensed under the MIT License.

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

[см. PASSPORT.md для полного списка модулей дома]

## ОПЕРАЦИОННЫЙ БЛОК (ПУСК, СТОП, ВЗГЛЯД)

| Действие | Команда / Место | Описание |
|---|---|---|
| **ПУСК** (START) | `python D:\AI\tools\agent\agent.py` | Подъём ядра, HTTP-сервера (8765) и ночного цикла. |
| **СТОП** (STOP) | `powershell D:\AI\STOP_ALL.ps1` | Мгновенная остановка всех процессов агента и Creoson. |
| **ВЗГЛЯД** (VIEW) | `http://localhost:8765` | Витрина: статус агента, логи, управление. |

---
*Обновлено: 19.09.2026 (Спека 100)*

- **17.09.2026 — спеки 66б–66e:** МАНИФЕСТ вошёл в system-промпт агента; аудит правил дома (`AUDIT_rules_20260917.md`) и исполнение его кластеров; crash-скиллы приведены к шаблону конституции; `skills_check.py` — дельта-снапшот, честные проверки, grep-поле ОШИБКА; вход дома: `ensure_admin` из `secrets.json` (дефолт admin/admin снят), TTL токена 24ч; `.clinerules` v5.10 (определение «миграции», протокол ожидания детач-процесса в SKILL_local_agent_cline); М2 уточнён (utf-8 голова близнеца, отчёт задачи — выжимка в чате, полный текст в файле после 2000 знаков).
