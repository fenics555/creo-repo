---
name: creoson-inbox-deepseek
system: CREOSON-QUEUE
description: Use when: старт разборщика темы CREOSON/ДАВЫДОВКА — здесь остались только ДОЛГИ темы
when: inbox, deepseek, creoson, davydovka, долги, очередь
date: 17.09.2026
executor: DeepSeek4 (разборщик), создан ногой спеки 59
ВЕДЁТ: только исполнитель темы CREOSON (Cline). Файл удаляется, когда долги закрыты.
ПРОТОКОЛ: 1) пункты по порядку, по каждому — доказательство и вердикт с датой; 2) правки по
контракту (editor ≤3 КБ, old_text из свежего чтения, verbatim-русский через редактор);
3) закрытый пункт переносится в скилл темы и уходит из этого файла; 4) новые краховые подписи —
в crash\, не сюда.

## ДОЛГИ (открыты на 17.09.2026)
Д1. SKILL_creoson_complete.md: двойная кодировка (U+00E2=59, U+00C2=2, U+FFFD=0) и мёртвая
    строка 45 про rename_dependencies. Ждёт двухпроходной перекодировки самопроверяющим
    ASCII-скриптом (10.8/10.9): проход 1 — список подозреваемых, проход 2 — правка с бекапом;
    строку 45 заменить по SKILL_creoson_rename_mechanism.md.
Д2. Сырой близнец отношений liteika_hts_mm отсутствует на диске. Корень (диагноз напарника
    17.09): relations_get вернул data СПИСКОМ строк, а нормализация в creo_tools.tool_get_relations
    умеет только str и dict — падает AttributeError. Якорь: ветка
    `if isinstance(d, list): text = "\n".join(str(x) for x in d)` в creo_tools.tool_get_relations
    + та же нормализация в пробном скрипте; затем read-only relations_get →
    cards\liteika_hts_mm_relations_raw.json (размер+crc32+первые 80) и обновление
    SKILL_creo_cards.md (имя близнеца и хэш).
Д3. SKILL_crash_ctl-inline-stderr-truncated.md: строка про pid-файл
    (core.BASE\agent\agent.pid, НЕ data\agent.pid) и приёмка рестарта по смене PID +
    StartTime против mtime правленого файла. [ЗАКРЫТО ЭТИМ ЗАХОДОМ — см. скилл]
Д4. ДАВЫДОВКА: каскад «деталь + чертёж + сборки-владельцы» через rename_model на КОПИЯХ
    в полигоне D:\AI\PROBA\23-1017GRI (только копии, изменения сверять); мануфактуринг
    (-m2, -01-dor): в CREOSON mfg отсутствует — задокументировать обходной путь
    (спутники <имя>_mfg.asm, <имя>_mfg.drw, <имя>_wp.prt — файловый уровень).

## ЗАКРЫТО (перенесено в скиллы темы)
- п.2 pow/rtos → Creo/SKILL_creo_relations.md: «pow подтверждён живыми отношениями 17.09.2026
  (liteika_hts_mm, близнец crc32 454521701)»; строка «функции pow() НЕТ» удалена. СДЕЛАНО 17.09.
- п.4 правило 16.5 → Creo/SKILL_creo_cards.md: «ЧТЕНИЕ на модели в сессии инженера РАЗРЕШЕНО
  (file:list, parameter:list, file:massprops, file:relations_get, bom:get_paths); ЗАПРЕЩЕНЫ
  изменяющие (parameter:set, relations_set, regenerate, erase, save, rename, backup)». СДЕЛАНО 17.09.
- п.5 крах входа → crash\SKILL_crash_login-stale-memory.md: причина Б + профилактики 4-6 +
  «СЧЁТЧИК ПОВТОРОВ: 2» (закрыто другим исполнителем, проверено). СДЕЛАНО 17.09.
- п.7 ERR_creoson.md: разделы 1.7 (file:save с несуществующим именем сохраняет активную модель)
  и 1.8 (erase_not_displayed сессию не чистит) на месте. СДЕЛАНО 17.09.
- п.9 executor в скилах searchcodebase: у обоих `executor: Cline (solar-pro4)`; маршрут
  приложений зафиксирован в crash\SKILL_crash_constitution.md («профилактики среды — совет»). СДЕЛАНО 17.09.
- п.10 факты дома → Creo/SKILL_creoson_probe_method.md: порт 9056 рекомендован / дом живёт на
  8080 («менять только после пробы на всём флоте»), JRE Java 25 (RELEASE_NOTES 3.0.2),
  эндпоинты /creoson и /server. СДЕЛАНО 17.09.
