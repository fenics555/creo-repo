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

## 6. ПРАВИЛА ДОМА (решение владельца, 15.10.2026) — НЕ ОБСУЖДАТЬ ЗАНОВО
1. **Папку `.clinerules\skills\` НЕ создавать.** Не нужно: при «открыть папку `D:\AI`» Cline
   подхватывает `D:\AI\.clinerules` автоматически, 100%. Плюс `.clinerules` — ЭТО ФАЙЛ
   (12 411 б), папку с тем же именем Windows создать не даст (`ENOTDIR`).
2. **Никаких дополнительных механизмов правки правил/скиллов.** Любой свой «сборщик промпта»,
   «загрузчик», «ужиматель» = ВТОРОЙ источник истины = ИСКАЖЕНИЕ. У Cline такого механизма нет:
   он только ЧИТАЕТ `.clinerules` и ПОДСТАВЛЯЕТ текст (`{{CLINE_RULES}}`), и отдаёт скилл по
   имени (`use_skill`). Больше ничего.
3. **Правки правил и скиллов — ТОЛЬКО через стенд** (`checks\agentic`), по одной правке,
   с записью в `SUITE.md`. Никаких автоматических правок закона и скиллов.
4. **`build_context.ps1` НЕ создавать.** Cline уже грузит правила сам; дублировать нечего.
5. **Папку `.clinerules` в папку не превращать** — сломается путь `D:\AI\.clinerules`,
   который тест 1 (`check_1_law`) проверяет как файл (держится 5/5).

## 7. ОШИБКИ, КОТОРЫЕ МЫ СДЕЛАЛИ (вывод)
1. Копировали закон в промпт руками -> «5/5», потом УБРАЛИ (решив, что модель должна читать сама).
   **Cline так НЕ делает: правила подставляет АВТО из файла.** Ручное копирование = кустарная эмуляция.
2. Искали скиллы в `repo\SKILL_*.md`, а Cline ищет в `.clinerules\skills\` -> **несовпадение путей**.
   НО: папку не делаем (п.6.1) — живые скиллы дом отдаёт через `read_file` по правилу 3.П.1 (триггеры).
3. «Тест 0» (заставить читать закон промптом) проверял НЕ ту гипотезу: Cline **не заставляет читать**, он **подставляет**.
4. Предлагали построить `build_context.ps1` + свой `use_skill` -> **ОТМЕНЕНО владельцем** (п.6.2, 6.4):
   дополнительный механизм искажает; у Cline его нет.

## 8. РАБОЧАЯ СХЕМА ДОМА (финал, 15.10.2026)
```
D:\AI\                                   <- РАБОЧАЯ ПАПКА Cline (открыть папку -> правила подхватятся)
├── .clinerules                          <- ПРАВИЛА (ФАЙЛ, 12 411 б; Cline подставляет АВТО)
├── repo\SKILL_index.md                  <- КАРТА скиллов (упомянута в законе, строка 49)
├── repo\**\SKILL_*.md                   <- СКИЛЛЫ дома (196 шт; читаются read_file по триггерам)
└── tools\agent\skills_index\            <- ИНДЕКС ПО СМЫСЛУ (3 руки: CLI/окно/визард)
    └── skills_index.py search "<задача>"   <- когда имя скилла неизвестно
```

## 9. ЧТО ИЗМЕНИТЬ В СКИЛЛАХ ПО ЭТОМУ РЕШЕНИЮ
- Заменить все ссылки `D:\AI\repo\INDEX\find_skill.ps1` -> `tools\agent\skills_index\skills_index.py`.
- Удалить `D:\AI\repo\INDEX\` целиком (PowerShell-референс; в `repo` не должно быть исполняющих).
- СДЕЛАНО 15.10.2026: ссылки в `checks\README.md`, `README.md`, `SKILL_stand_single_and_seed.md`,
  `PROMPT\SKILL_rules_edit_loop_ai.md`, `SKILL_cline_context_mechanism.md` -> заменены.
- ОСТАЛОСЬ: `check_3_skills.ps1:90`, `SUITE.md:50,304,312`, `config\paths.ps1:13`,
  `laws\law_04.md:36` (закон — правка только через стенд), `tmp\scripts\_gen_variants.ps1:16`.


