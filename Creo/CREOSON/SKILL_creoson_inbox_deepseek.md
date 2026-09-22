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

## ДОЛГ (открыт на 17.09.2026)
Д4. ДАВЫДОВКА: каскад «деталь + чертёж + сборки-владельцы» через rename_model на КОПИЯХ
    в полигоне D:\AI\PROBA\23-1017GRI (только копии, изменения сверять); мануфактуринг
    (-m2, -01-dor): в CREOSON mfg отсутствует — задокументировать обходной путь
    (спутники <имя>_mfg.asm, <имя>_mfg.drw, <имя>_wp.prt — файловый уровень).

## ЗАКРЫТО (перенесено в скиллы темы)
- п.2 pow/rtos → Creo/RELATIONS/SKILL_creo_relations.md: «pow подтверждён живыми отношениями 17.09.2026
  (liteika_hts_mm, близнец crc32 454521701)»; строка «функции pow() НЕТ» удалена. СДЕЛАНО 17.09.
- п.4 правило 16.5 → Creo/STANDARDS/SKILL_creo_cards.md: «ЧТЕНИЕ на модели в сессии инженера РАЗРЕШЕНО
  (file:list, parameter:list, file:massprops, file:relations_get, bom:get_paths); ЗАПРЕЩЕНЫ
  изменяющие (parameter:set, relations_set, regenerate, erase, save, rename, backup)». СДЕЛАНО 17.09.
- п.5 крах входа → crash\SKILL_crash_login-stale-memory.md: причина Б + профилактики 4-6 +
  «СЧЁТЧИК ПОВТОРОВ: 2» (закрыто другим исполнителем, проверено). СДЕЛАНО 17.09.
- п.7 ERR_creoson.md: разделы 1.7 (file:save с несуществующим именем сохраняет активную модель)
  и 1.8 (erase_not_displayed сессию не чистит) на месте. СДЕЛАНО 17.09.
- п.9 executor в скилах searchcodebase: у обоих `executor: Cline (solar-pro4)`; маршрут
  приложений зафиксирован в crash\SKILL_crash_constitution.md («профилактики среды — совет»). СДЕЛАНО 17.09.
- Д1 (перекодировка SKILL_creoson_complete.md) → СДЕЛАНО 17.09.2026: двухпроходный
  самопроверяющий скрипт, проход 1 нашёл 61 подозреваемого (тире `â\x80\x94`,
  кавычки `Â«Â»`), проход 2 применил правку: было (e2=59, C2=2, fffd=0) crc32 7920e955,
  стало (0, 0, 0), 14086 → 13905 б; бекап data\backup\pre_recode_SKILL_creoson_complete.md.bak.
  Мёртвая строка 45 про rename_dependencies заменена по SKILL_creoson_rename_mechanism.md.
- Д2 (сырой близнец отношений) → СДЕЛАНО 17.09.2026: исправлена нормализация в
  creo_tools.tool_get_relations (dict+list), живая проба `type returned: str | len: 50677`,
  близнец cards\liteika_hts_mm_relations_raw.json (73872 б, data 68640 б, crc32 74a49c2f),
  SKILL_creo_cards.md обновлён (имя, размер, хэш, описание дыры в коде).
- Д3 (pid-файл и приёмка рестарта) → СДЕЛАНО 17.09.2026: пункт 5 в
  crash\SKILL_crash_ctl-inline-stderr-truncated.md (core.BASE\agent\agent.pid,
  смена PID + StartTime против mtime правленого файла, попутно sched.py/loop.py).
- п.10 факты дома → Creo/CREOSON/SKILL_creoson_probe_method.md: порт 9056 рекомендован / дом живёт на
  8080 («менять только после пробы на всём флоте»), JRE Java 25 (RELEASE_NOTES 3.0.2),
  эндпоинты /creoson и /server. СДЕЛАНО 17.09.
