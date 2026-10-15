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

## 3А. ТОЧНЫЙ ШАБЛОН ПРОМПТА CLINE (раскопано 15.10.2026, extension.js 4.1.24)

Механизм (живая цитата кода):
```javascript
function fL(t){ ... let p = r==="yolo" ? whi.YOLO : whi.ACT, h=[rules, ...]; 
  return p.replace("{{PLATFORM_NAME}}",i)... .replace("{{CLINE_RULES}}",h).trim() }
whi = { ACT: rNu, YOLO: nNu }
```

### Дословный шаблон ACT (`rNu`) — что Cline пишет при старте
```
You are Cline, an AI coding agent. Your primary goal is to assist users with various
coding tasks by leveraging your knowledge and the tools at your disposal. Given the
user's prompt, you should use the tools available to you to answer user's question.

Always gather all the necessary context before starting to work on a task. ...

Environment you are running in:
<env>
1. Platform: {{PLATFORM_NAME}}
2. Date: {{CURRENT_DATE}}
3. IDE: {{IDE_NAME}}
4. Working Directory: {{CWD}}
</env>

Remember:
- Always adhere to existing code conventions and patterns.
- Always show your planning process before executing any task.
- Always use absolute paths when referring to files.
- You can call multiple tools in a single response. ...
- Always verify the files you have edited or created at the end of the task ...

Begin by analyzing the user's input and gathering any necessary additional context.
Then, present your plan at the start of your response along with tool calls ...

REMEMBER, be helpful and proactive! ... 
IMPORTANT: Always includes tool calls in your response until the task is complete

{{CLINE_RULES}}
{{CLINE_METADATA}}
```

### ЧТО ЭТО ЗНАЧИТ ДЛЯ НАС (выводы)
1. **Самоопределение — ПЕРВОЙ строкой:** «You are Cline, an AI coding agent». У нас в стенде
   самоопределение брали из §0 ЗАКОНА — но правила идут ПОСЛЕ роли; роль — отдельно.
2. **«Always gather all the necessary context before starting»** — прямое требование собрать
   контекст ДО работы. Это то, чего недоставало нашему стенду (обряд не запускался).
3. **«Begin by analyzing the user's input and gathering context. Then present your plan at the start»** —
   обряд старта задан В ШАБЛОНЕ, а не в правилах.
4. **«Always includes tool calls in your response until the task is complete»** — требование
   работать инструментами до конца.
5. 🔴 **ПРАВИЛА `{{CLINE_RULES}}` — В САМОМ КОНЦЕ ПРОМПТА** (после роли, окружения, Remember).
   Стенд ставил правила в НАЧАЛО — расхождение!
6. **`{{CLINE_METADATA}}`** — служебный блок с рабочей папкой (у нас это `РАБОЧАЯ ПАПКА:`).

### ПОДТВЕРЖДЕНО СТЕНДОМ (15.10.2026, gemma4)
| промпт стенда | вердикт |
|---|---|
| папка + правила (без роли) | `CITE_FAKE` — обряд не идёт |
| **+ служебная роль** («Ты — ИИ-агент… ПЕРВОЕ действие — изучить ПРАВИЛА ДОМА и выполнить обряд») | **`LAW_CITED`** ✅ |

**Вывод:** служебная роль (аналог `rNu`) — **обязательна**; без неё модель правила видит, но не применяет.

## 3Б. МЕХАНИЗМ АГЕНТА (`tools\agent\loop.py:build_system`) — УЖЕ ЕСТЬ (15.10.2026)

**Живой код** `D:\AI\tools\agent\loop.py:210–273`, функция `build_system(mode, question)`. Собирает системный промпт:

| # | блок | живая цитата / источник |
|---|---|---|
| 1 | режим 2 = «собеседник» | «Ты — собеседник и помощник по любым темам… нет доступа к Creo, файлам и базам» |
| 2 | **ПРАВИЛА в промпт** | `load_skill("MANIFEST.md") + SKILL_agent_protocol.md` |
| 3 | заряд знаний | `SKILL_CHARGE.md` (карта скиллов) + `SKILL_CHARGE_START.md` (Creo-старт) |
| 4 | **ИНСТРУМЕНТЫ в промпт** | `TR.TOOLS` → `--- ТВОИ ИНСТРУМЕНТЫ ---` + `--- ПРОЧИЕ ИНСТРУМЕНТЫ ---` |
| 5 | размышления | `think_mode` 0 (запрещены) / 1 (4 строки) / 2 (полно, до N строк) |
| 6 | **ЖЁСТКИЕ ПРАВИЛА** | «1) ЯЗЫК только рус … 4) НЕ ХВАТАЕТ ДАННЫХ: назови, чего не хватает … не выдумывай» |

### Сравнение трёх механизмов
| свойство | Cline | **Агент** | Стенд think_probe |
|---|---|---|---|
| правила в промпт | ✅ `{{CLINE_RULES}}` | ✅ MANIFEST + протокол | ✅ (подстановка) |
| служебная роль | ✅ «You are Cline…» | ✅ «Ты — собеседник…» (mode 2) | ✅ (добавлено 15.10) |
| обряд «собери контекст → дай план» | ✅ явно | ⚠️ частично (`think_rule` требует 4 пункта) | ✅ (добавлено) |
| карта скиллов в промпт | ❌ | ✅ `SKILL_CHARGE.md` | ❌ |
| инструменты в промпт | ✅ | ✅ `TR.TOOLS` | ✅ (tools API) |
| «не выдумывай» | ✅ | ✅ п.4 | ✅ |
| лимит размышлений | ❌ | ✅ `think_lines_max` | ⚠️ NumPredict 400 |

**ВЫВОД:** у Агента механизм **уже есть и богаче Cline**. Недостающая деталь — **явная строка обряда**
(«прежде чем отвечать — изучи правила и объяви план»), как в шаблоне Cline `rNu`.

## 3В. ЭТАЛОННЫЙ ШАБЛОН ДЛЯ ПРИМЕНЕНИЯ (собран 15.10.2026) — по образцу Cline

**Зачем:** локальная модель в основном работает в Cline. Значит наш промпт должен повторять
порядок Cline. Этот шаблон — эталон; применяется к Агенту (`loop.py:build_system`) и к стенду.

### ПОРЯДОК СБОРКИ (7 блоков, как в Cline `whi.ACT` / `rNu`)
```
[1] РОЛЬ         — кто ты (агент с инструментами)
[2] КОНТЕКСТ     — «прежде чем работать — собери контекст» (ОБРЯД)
[3] ОКРУЖЕНИЕ    — платформа / дата / IDE / рабочая папка
[4] REMEMBER     — соглашения, план перед делом, абсолютные пути, вызовы инструментов
[5] ОБРЯД СТАРТА — «начни с анализа и плана; вызывай инструменты до завершения»
[6] ПРАВИЛА      — {{CLINE_RULES}}  ← В КОНЦЕ (не в начале!)
[7] МЕТА         — служебные данные (рабочая папка, ветка и т.п.)
```

### ГОТОВЫЙ ТЕКСТ (адаптация под дом; применять как есть)
```
Ты — ИИ-агент дома Инженера, работающий инструментами (read_file / write_file / shell).
Твоя цель — помочь Инженеру, используя доступные инструменты. Отвечай на русском.

СОБЕРИ КОНТЕКСТ ПРЕЖДЕ, ЧЕМ РАБОТАТЬ: прежде чем отвечать на задание — изучи ПРАВИЛА ДОМА
(даны ниже) и выполни их ОБРЯД СТАРТА. Без этого отвечать по существу ЗАПРЕЩЕНО.

Окружение:
<env>
1. Платформа: {{PLATFORM}}
2. Дата: {{DATE}}
3. Рабочая папка: {{CWD}}
</env>

Помни:
- Сверяйся с ПРАВИЛАМИ ДОМА — это высший приоритет.
- Дай план перед действием; действуй одним шагом, не расплывайся.
- Используй АБСОЛЮТНЫЕ пути при обращении к файлам.
- НЕ выдумывай факты: нет данных — скажи «НЕТ ДАННЫХ: <чего не хватает>» и прочитай файл.
- Работай инструментами до завершения задачи; в конце проверь результат.

НАЧНИ с анализа задания и сбора контекста, объяви режим и план. Работай инструментами,
пока задача не выполнена. ЗАПРЕЩЕНО имитировать вызовы инструментов текстом.

=== ПРАВИЛА ДОМА (главные) ===
{{CLINE_RULES}}
=== КОНЕЦ ПРАВИЛ ===
```

### ЧЕМ ОТЛИЧАЕТСЯ ОТ ТЕКУЩЕГО СТЕНДА
| | стенд (сейчас) | по шаблону |
|---|---|---|
| роль | есть (добавлена) | [1] есть |
| правила | **В НАЧАЛЕ** | **[6] В КОНЦЕ** |
| обряд | в роли | [2]+[5] двумя строками |
| окружение `<env>` | нет | [3] есть |
| «не выдумывай» | нет в роли | [4] есть |

**Проверено стендом (gemma4):** роль+правила → `LAW_CITED` (было `CITE_FAKE` без роли).
Следующий шаг — проверить порядок «правила в конце».

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
3. **Правки ЗАКОНА — ТОЛЬКО С РАЗРЕШЕНИЯ ВЛАДЕЛЬЦА** (метод §12 скилла стенда): правки сначала
   в КОПИЯХ `AGENT_SETTINGS\laws\law_<ключ>.md` → прогон копий → выводы → **рекомендации** → ЖДАТЬ.
   Живой `D:\AI\.clinerules` САМИ НЕ ПРАВИМ. Никаких автоматических правок закона.
4. **`build_context.ps1` НЕ создавать.** Cline уже грузит правила сам; дублировать нечего.
5. **Папку `.clinerules` в папку не превращать** — сломается путь `D:\AI\.clinerules`,
   который тест 1 (`check_1_law`) проверяет как файл (держится 5/5).
6. **ЗАКОН = ЖИВОЙ РАБОЧИЙ ФАЙЛ, НЕ СТЕНД.** В законе НЕТ и НЕ ДОЛЖНО быть никаких стендов.
   **ЛЮБАЯ ПРАВКА ЗАКОНА — ТОЛЬКО ЧЕРЕЗ ВЛАДЕЛЬЦА.** Порядок работы ноги:
   **ТЕСТЫ → ВЫВОД → РЕКОМЕНДАЦИИ → ЖДАТЬ.**
   ЗАПРЕЩЕНО самому вписывать/менять/удалять пункты в `D:\AI\.clinerules`.
   Стенд (`AGENT_SETTINGS\checks\...`) тестирует закон — но НЕ правит его.

## 6А. ПОДТВЕРЖДЕНО ПРОГОНОМ (15.10.2026, gemma4, живой закон)

| промпт стенда | вердикт |
|---|---|
| «Правила дома — в контексте; путь НЕ называется» (**текста правил НЕТ**) | `CITE_FAKE` — модель пошла искать файл наугад, закон НЕ нашла; Ш3 её слова: «классическая ошибка агента — **ошибка поиска в среде вместо поиска в себе**» |
| `=== ПРАВИЛА ДОМА ===` + **полный текст закона** + `=== КОНЕЦ ПРАВИЛ ===` | **`LAW_CITED`** ✅ + `ritual=True` — прочитала `D:\AI\.clinerules` ПЕРВЫМ действием (ШАГ-0) |

**ВЫВОД (не оспаривать):** правило должно быть **ПОДСТАВЛЕНО В ПРОМПТ ТЕКСТОМ**.
Слова «правила в контексте» без самого текста = механизма НЕТ, модель работает наугад.
Это ровно поведение Cline: `{{CLINE_RULES}}` заменяется текстом правил.

**Термины (не путать):** `use_skill` — инструмент CLINE (у Агента нет). У Агента — `skills_search`
/ `skills_status` (`tools\agent\skills_index_tools.py`). `SKILL_READ` / `MAP_ONLY` — МЕТРИКИ
теста 3 (`check_3_skills.ps1`), а не инструменты.

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
  `laws\law_04.md:36` (закон — правка ТОЛЬКО с разрешения владельца), `tmp\scripts\_gen_variants.ps1:16`.


