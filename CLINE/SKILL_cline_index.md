---
name: cline-index
system: CLINE
description: Вход направления Cline (VS Code / claude-dev) — как Cline грузит правила и скиллы, шаблон промпта, выживание ноги, аудит сессий. Схема, которой стенд имитирует Cline.
when: cline, клайн, механизм правил cline, шаблон промпта cline, {{CLINE_RULES}}, схема claude-dev, роли/обряд, extension.js, выживание в cline, аудит сессии
priority: critical
date: 27.11.2026
executor: Cline
---

# НАПРАВЛЕНИЕ CLINE — вход

**Что здесь.** Всё о работе с Cline (VS Code, расширение `saoudrizwan.claude-dev`):
как Cline **грузит правила и скиллы**, точный **шаблон промпта**, **выживание ноги** (лимиты,
деградация), **аудит** других сессий. **Стенд имитирует Cline — значит должен знать эту схему.**

## КАРТА СКИЛЛОВ НАПРАВЛЕНИЯ

| Файл | Что внутри | Когда читать |
|---|---|---|
| `..\SKILL_cline_context_mechanism.md` (**critical**) | **МЕХАНИЗМ Cline**: где ищет правила, как подставляет `{{CLINE_RULES}}`, **точный шаблон промпта (12 блоков, 4.1.28)**, 8 плейсхолдеров, `use_skill`, эталон для применения | любая работа со схемой Cline, правка `HOUSE_SYSTEM` стенда, механизм правил |
| `..\SKILL_local_agent_cline.md` (**critical**) | **ВЫЖИВАНИЕ в Cline**: транспорт, редактор, режимы (§2.1–2.3), лимиты, REVIVE, замер окна §8 | старт ноги, длинная сессия, сбой |
| `CLINE\SKILL_cline_session_audit.md` | **АУДИТ сессии другой ноги**: чтение `messages.json`, поиск сессии по модели, разбор шагов, ловля петель | аудит чужого хода, разбор петель |
| `..\crash\SKILL_crash_cline_longsession_context_death.md` | крах: окно Cline молча обрывается на длинной сессии | обрыв длинной сессии |
| `..\Prog\SKILL_prog_local_agent_cline.md` | указатель (1 строка) | — |
| `AGENT_SETTINGS\checks\agentic\SKILL_cline_scheme.md` | «работаем по схеме Cline»: где искать в `extension.js`, лимиты 48 000 | работа со стендом по схеме Cline |

## ГЛАВНЫЕ ФАКТЫ (схема Cline — эталон стенда)

**Где Cline ищет правила:** `<рабочая папка>\.clinerules` (наш случай `D:\AI\.clinerules`).
**Как подставляет:** `.replace("{{CLINE_RULES}}", h)` — **текстом, автоматически**, ПРАВИЛА **В КОНЦЕ** промпта.

**8 плейсхолдеров:** `{{PLATFORM_NAME}}` · `{{CURRENT_DATE}}` · `{{IDE_NAME}}` · `{{CWD}}` ·
`{{CLINE_METADATA}}` · `{{CLINE_RULES}}` · `{{SKILL_NAME}}` · `{{USER_CURRENT_INPUT}}`

**12 блоков ACT-шаблона** (что Cline пишет сам): РОЛЬ → КОНТЕКСТ → ЧЕСТНОСТЬ → ОКРУЖЕНИЕ →
REMEMBER (вкл. ПАРАЛЛЕЛИЗМ инструментов) → ОБРЯД → ПРОАКТИВНОСТЬ → ИНСТРУМЕНТЫ ДО КОНЦА →
ФИНАЛ → ИСКЛЮЧЕНИЕ (простой вопрос) → `{{CLINE_RULES}}` → `{{CLINE_METADATA}}`.

**ПОЛНЫЙ ТЕКСТ ЭТАЛОНА:** `D:\AI\AGENT_SETTINGS\config\cline_template_reference.md`
(извлечён из `extension.js` 4.1.28 скриптом `D:\AI\log\urn\cline\extract_cline_template.py`).

**Источник (extension.js):** `C:\Users\<User>\.vscode\extensions\saoudrizwan.claude-dev-<ver>\dist\extension.js`.

## СВЯЗЬ СО СТЕНДОМ
Стенд **имитирует Cline**: `HOUSE_SYSTEM` в `checks\loop_revive_test.py` приведён к этим 12 блокам
(27.11.2026). Закон — `D:\AI\.clinerules`. Операции стенда — `..\AGENT_SETTINGS\skills\SKILL_stand_ops.md` §6г.
