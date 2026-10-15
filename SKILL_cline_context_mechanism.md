---
name: cline-context-mechanism
system: repo
description: Как Cline грузит ПРАВИЛА и СКИЛЛЫ в контекст модели (раскопано в extension.js 4.1.24). Нужно для своего механизма.
when: механизм правил, подгрузка скиллов, как клин читает rules, use_skill, контекст модели, свой загрузчик
priority: critical
date: 15.10.2026
executor: Cline
---

# МЕХАНИЗМ CLINE: правила и скиллы (раскопано 15.10.2026)

Источник: `C:\Users\<User>\.vscode\extensions\saoudrizwan.claude-dev-4.1.24\dist\extension.js` (26 МБ).

## 1. ЧТО И ГДЕ ИЩЕТ
```javascript
// директории ПРАВИЛ (функция типа yP):
<workspacePath>\.clinerules          // ФАЙЛ правил (наш случай: D:\AI\.clinerules)
<workspacePath>\.cline
+ globalRules (глобальные правила)

// СКИЛЛЫ / WORKFLOWS / HOOKS (функция pEi):
<workspacePath>\.clinerules\skills        // <- СКИЛЛЫ ЗДЕСЬ
<workspacePath>\.clinerules\workflows
<workspacePath>\.clinerules\hooks
<workspacePath>\.cline\...
<workspacePath>\.claude\skills            // поддержка формата Claude
<workspacePath>\.agents\skills

// константы:
oxr=".clinerules"; $ht=".cline";
clineRules=".clinerules"; workflows=".clinerules/workflows"; hooksDir=".clinerules/hooks";
clineruleSkillsDir=".clinerules/skills"; clineSkillsDir=".cline/skills";
claudeSkillsDir=".claude/skills"; agentsSkillsDir=".agents/skills";
wue="AGENTS.md";
```

## 2. КАК ОБРАБАТЫВАЕТ
```javascript
// три ТИПА сущностей:
type:"rule"      -> directories:[...], includeFile:(i,a)=> i===".clinerules"||...,
                    parseFile:(i)=> parse(i.content, workspacePath), resolveId:(i)=>id(i.name)
type:"skill"     -> discoverFiles, parseFile -> {name, description, instructions, frontmatter}
type:"workflow"  -> ...
// загрузка: loadDefinition(): обход директорий -> readFile(utf8) -> parseFile -> resolveId -> РЕЕСТР
getRegisteredRules()  -> [...registry.rules]
getRegisteredTools()  -> [...registry.tools]
getRegisteredMcpServers()
// + ПЕРЕКЛЮЧАТЕЛИ: localClineRulesToggles (вкл/выкл отдельного правила),
//   globalClineRulesToggles, remoteRulesToggles
```

## 3. ЧТО ПОПАДАЕТ В СИСТЕМНЫЙ ПРОМПТ
```javascript
// в шаблоне промпта есть ПЛЕЙСХОЛДЕР:
.replace("{{CLINE_RULES}}", h)   // h = собранный текст ПРАВИЛ
// ВЫВОД: ПРАВИЛА подставляются в промпт ТЕКСТОМ, АВТОМАТИЧЕСКИ.
```

## 4. КАК МОДЕЛЬ ПОЛУЧАЕТ СКИЛЛЫ — ЧЕРЕЗ ИНСТРУМЕНТ
```javascript
use_skill  ->  tool:"useSkill"  ->  аргумент: skill_name | skill | name
```
**Скиллы НЕ грузятся в промпт целиком.** Модель **вызывает инструмент `use_skill(<имя>)`** и ПОЛУЧАЕТ скилл.
(Аналог: `read_file`, но по «имени скилла», а не по пути.)

## 5. АРХИТЕКТУРА (итог)
| сущность | куда идёт | как |
|---|---|---|
| **ПРАВИЛА** | **в системный промпт** (`{{CLINE_RULES}}`) | авто из `<папка>\.clinerules` |
| **СКИЛЛЫ** | **НЕ в промпт** | модель **запрашивает**: инструмент `use_skill(name)` |
| метаданные скиллов | список/описания в промпте (чтобы знать, что звать) | из frontmatter (name/description) |
| переключатели | UI-настройки | localClineRulesToggles и др. |

## 6. ЧТО ЭТО ЗНАЧИТ ДЛЯ НАШЕГО ДОМА
| Cline | нам надо |
|---|---|
| `<папка>\.clinerules` -> в промпт | `D:\AI\.clinerules` **в промпт** (наш тест это делал — ВЕРНО; убирать не надо) |
| `<папка>\.clinerules\skills\` | **у нас НЕТ этой папки** -> Cline НЕ находит наши скиллы (они в `repo\**\SKILL_*.md`) |
| инструмент `use_skill(name)` | **сделать свой инструмент дома**: `use_skill`/`find_skill` -> читает скилл по имени |
| `SKILL_index.md` | раздавать как **карту доступных скиллов** (ссылка в правилах) |

## 7. ОШИБКИ, КОТОРЫЕ МЫ СДЕЛАЛИ (вывод)
1. Копировали закон в промпт руками -> «5/5», потом УБРАЛИ (решив, что модель должна читать сама).
   **Cline так НЕ делает: правила ВСЕГДА в промпте.** Ручное копирование = кустарная эмуляция механизма.
2. Искали скиллы в `repo\SKILL_*.md`, а Cline ищет в `.clinerules\skills\` -> **несовпадение путей**.
3. «Тест 0» (заставить читать закон промптом) проверял НЕ ту гипотезу: Cline **не заставляет читать**, он **подставляет**.

## 8. ЦЕЛЕВОЙ МЕХАНИЗМ ДОМА (предложение)
```
D:\AI\
├── .clinerules                     <- ПРАВИЛА (в промпт целиком)
├── .clinerules\skills\             <- (Cline ищет ЗДЕСЬ) ссылки/копии -> на repo\**\SKILL_*.md
├── repo\SKILL_index.md             <- КАРТА скиллов (ссылка из правил)
└── tools\agent\build_context.ps1   <- ОБЩИЙ ИНСТРУМЕНТ: собрать промпт (правила + карта/список скиллов)
```
- **Правила** -> в промпт (авто).
- **Список скиллов** (из `SKILL_index.md` или frontmatter) -> в промпт (лёгкий).
- **Сам скилл** -> модель запрашивает инструментом (`use_skill` / `find_skill`) -> читается по требованию.
- **Один инструмент для стенда и агента**; в Cline — свой, но грузит те же правила/скиллы.
