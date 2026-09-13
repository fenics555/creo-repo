# ПАСПОРТ CREO-AGENT (обновлён: 11.09.2026, день; индекс обновлений — в конце файла)

## Окружение
- Машина frezer-4 (192.168.88.159): Z890 AORUS PRO ICE, Core Ultra 9 285K (24 ядра),
  64 ГБ RAM, RTX 5060 Ti 16 ГБ, Win11.
- Порты: агент-веб :8765 | CREOSON :8080 | copy-server :8000 | Ollama :11434.
- Пути: код D:\AI\tools\agent | БД/config D:\AI\tools\agent\data\ |
  логи D:\AI\tools\agent_log_frezer4.txt | core.BASE = D:\AI\tools (РОДИТЕЛЬ!) |
  репо/скиллы D:\AI\repo | kb_roots.txt и kb_exclude.txt — в папке агента.
- GitHub: fenics555/creo-agent и creo-repo, ветка master, пуш GIT_SYNC.bat.
- VS Code + Continue: C:\Users\User\.continue\config.yaml.

## Модели (Ollama; живой конфиг 11.09)
- Боевой чат: gemma4:26b (llm_model, подтверждено /status и ollama ps).
- Аудит/правки: qwen2.5-coder:32b-instruct-q4_K_M (скачана, только ручная Панель → МОДЕЛЬ ИИ).
- Ещё: deepseek-r1:14b, qwen2.5-coder:7b (autocomplete), nomic-embed-text,
  minicpm-v:8b (визия).

## Диагностика
- `diag_run` и `dev\ui_check.py`.
- Правила — `.clinerules`, единственный источник, правится человеком.
- `doctor` удалён.


## РЕШЕНИЕ (СПЕКА 19+20 FINAL, 13.09.2026)
- Канон кода — **монолит `agent.py`**. `engine.py` удалён после необратимого повреждения кодировки — НЕ воскрешать.
- Кракозябры в agent.py вычищены байтовыми якорными заменами (DEFAULT_PROTO/режим 2/STUB_PAGE) + подстрочными
  самопроверяющими заменами (cp1251 round-trip, потерянный байт 0x98 = заглавная И восстановлен как control-пара).
- probe-критерий: 0 битых прогонов, 0 U+FFFD, py_compile зелёный.

- **РЕЖИМЫ**: Инженер / Собеседник (тумблер, префиксы chat/agent, chat_mode, qa с mode=1).
  Ночная вахта 02:00: scan, index, usage, backup (housekeeping + drift_check), drafts.
   Дефолт REGISTRY синхронизирован с config.json (спека 23): `scan,index,usage,backup,drafts`.

## РОТАЦИЯ ИСПОЛНИТЕЛЕЙ (постоянно)
- Задачи Cline с правками кода и verbatim-payload — **облачный флагман** (DeepSeek 300k), пока есть лимит.
- Локальная **gemma4:26b** — МИКРО-задачи, пробы, аудиты, ночная qa, резерв без лимитов.
- **Муза** — рецензия скриншотов и отчётов. Сгоревший лимит = пинок-резюме в новую задачу облака или временный переход на локаль.

## ИНСТРУМЕНТЫ РОСТА
- **vision_audit** (`vision_audit.py`, фаза 2 — спека 21, 13.09.2026): сверка PDF-экспорта с чек-листом ГОСТ.
   Пункты material/roughness/scale читает vision-модель `model_vision` (minicpm-v:8b, переключается одной настройкой) по изображению страницы 1; вердикт с цитатой увиденного в note.
   При недоступной модели пункты честно `not_determined`. Чек-листы: `data\checklists\*.json` (первый — gost_stamp.json, 7 пунктов); новые чек-листы кладутся туда же.
    **Архитектура**: vision_audit подключён динамически через `tools_registry`, в `agent.py` его импортов нет и быть не должно (канон монолита + реестр).
- **graph** (`graph_tools.py`, спека 23→24, 13.09.2026): интерактивный граф связей модели (BOM-дерево, usage-родословная, links-перекрёстные ссылки); страница `/graph?name=X` на D3.js force-directed layout; клик по узлу переходит к графу этой модели; цвета: красный=центр, зелёный=BOM-дети, фиолетовый=BOM-родители, синий=usage, оранжевый=links.
- **map** (`map_tools.py`, спека 27, 13.09.2026): карта проекта — корневые каталоги и топ моделей по связям (BOM + usage + links); страница `/map?top=N` со списком корней (клик фильтрует топ) и топ-моделей (клик → `/graph?name=X`); клик по модели в топе открывает граф.
- **audit_batch** (`vision_audit.py`, спека 27, 13.09.2026): пакетный аудит устаревших PDF-экспортов; читает пары drw/pdf из реестра файлов, берёт только устаревшие с существующим PDF, сверяет по чек-листу gost_stamp глазами model_vision (minicpm-v:8b); возвращает таблицу вердиктов и список требующих переэкспорта; Creo и экспорт не трогает.

## ЖИВОЕ (база 09-04, дополнено боем 09-11)
- 09-13 (спека 23): минимальные токеновые гейты — `/fleet/info` и `trails` в `/status` закрыты без валидного токена (401); `data\tmp` полностью очищен (48→8 живых файлов); двойная кодировка `audit_params` в config.json подтверждена чистой (кракозябры только в консоли); дефолт `night_tasks` синхронизирован.
- 09-11: кодировка agent.py и qa_run.py — честный UTF-8 (была двойная cp1251→utf8,
  системный промт и QA-вопросы содержали кракозябры); дубль /status в do_GET удалён;
  read_file ограничен корнем read_roots (панель → Главное, дефолт D:\AI, лимит 2 МБ);
  QA-креды вынесены в data\secrets.json (в git не попадает, data/ в .gitignore);
  GIT_SYNC.bat пишет лог D:\AI\tools\git_sync.log; задача AI-WATCH исправлена
  (пугала пусками несуществующего D:\AI\agent.py, сторож жив как pythonw);
  PAGE (HTML/CSS/JS панели, 169 строк) вынесен из agent.py в panel_ui.py
  (якорный скрипт, PAGE-байты равны — сверка, панель 200/26 448 Б после рестарта);
  ctl.py: --browser открывает 127.0.0.1:8765 (был захардкод 192.168.88.159) и
  починен \t-escape в пути copy_err.txt (редирект писал в кривое имя);
  qa_run.py LOG_FILE считается по HOST (был захардкод agent_log_frezer4.txt).
- Веб-UI: вход, панель, стриминг, 🧙, ❓; 31 блок / 117 инструментов (реестр 11.09).
- База: models ~40902, files 27439, chunks 33720, usage ~346–353 тыс ссылок;
  usage_state после рестарта читает из БД.
- Creo-мост: матрица 18/18; creoson_full_test ПРОЙДЕН (чтения+пишущий цикл).
- Двухъярусный промт: 15 ядровых инструментов полностью + 98 компактно (имена);
  полные описания — tools_help block=<имя>.
- Парсер: fallback [TOOL] без двоеточия; echo_guard (отсечение копий подсказки);
  refusal guard (отказ «нет доступа» → ретрай с подсказкой _ACCESS_NUDGE);
  проза >150 символов после [РЕЗУЛЬТАТА] = ответ.
- trail_predict читает БД напрямую (не парсит чужой текст), все болезни в прогнозе.
- settings.set_val() сохраняет config.json для любого ключа (панель → настройки
  теперь реально пишутся).
- scanner.db() на WAL + timeout=60 (как core.db).
- usage_tools/plm_tools пишутся под approval=True.
- Мусор из БД вычищен: убраны history_ai/history_ad, files_idx/files_index,
  history_fts* (сироты). БД: 25→16 таблиц, 379→291 МБ.
- py_compile ядра и изменённых блоков — OK.

## ЗАКРЫТО (эта сессия 09-04)
- C1 settings.set_val() не писал config (кроме auto_mode) — фикс: write_text в конец, return True для всех ключей → закрыт C2 settings_set «ключ не найден».
- C3 scanner.db() без WAL/timeout — фикс: PRAGMA journal_mode=WAL.
- C5 parallel_tools дублировал основной TOOL — фильтр дублей по сигнатуре.
- W1 пишущие инструменты без approval — web_save_rule, plm_mine → True.
- W5/W6 trail_predict не использовал trail_problems — переписан на прямое чтение БД.
- Парсер сдавался на 2-м invalid — теперь до 3 пинков + фолбэк с результатом.
- Эхо-щит: модель повторяла подсказку («текст» / «не понял») → теперь детектится,
  пользователю отдаётся last_res, не мусор.
- SKILL_agent_protocol.md: восстановлен гибрид DEFAULT_PROTO + best-of-bak +
  правила «доступ ЕСТЬ», «не понял после РЕЗУЛЬТАТА = запрет».
- Сиротские импорты убраны (diagnostic_tools, copy_server, copy_tools, scanner, spec_tools).
- usage_tools корни: читает agent/kb_roots.txt (непустой), ссылок >0.

## ЗАКРЫТО (оздоровительный заход 11.09)
1. Двойная кодировка agent.py/qa_run.py (кракозябры в системном промте и QA) →
   перекодированы в UTF-8, findstr кракозябр чист, py_compile OK.
2. Дубль /status в do_GET (мёртвый второй elif ~строка 710) → удалён.
3. Четыре пуска «python: can't open file D:\AI\agent.py» → источник: задача AI-WATCH
   с несуществующим путём; задача исправлена, рестарт стека проверен.
4. Секреты: QA-креды из qa_run.py → data\secrets.json; дефолт admin_password очищен,
   в config.json пусто (старый слабый 1945 отсутствует — проверено маскированно).
5. read_file читал любой путь машины → корни read_roots (дефолт D:\AI) + лимит 2 МБ;
   живые пробы: C:\Windows\win.ini — отказ; 371940 КБ sqlite — отказ.
6. GIT_SYNC.bat глушил ошибки (2>nul) → лог D:\AI\tools\git_sync.log.
7. Мусор data\tmp (30+ файлов clean_*, create_patch_*, fix_ctl_*, test_tool) → удалён.
8. doctor.py удалён из репо чисто (коммит 11.09 9:30, без висячего D);
   .clinerules v5.1 — read-only (+R), правится только человеком.
9. PAGE вынесен из agent.py в panel_ui.py (169 строк статики, anchors-скрипт
   с сверкой PAGE-байтов, бекап pre_page_agent.py); agent.py ~60 → 37 КБ
   (38 118 Б); рестарт чист, панель жива, 31 блок / 117 инструментов (реестр 11.09).
10. ctl.py: --browser на 127.0.0.1:8765 (был захардкод 192.168.88.159) и
    \t-escape в пути copy_err.txt (бил кривое имя из трейса редиректа).
11. qa_run.py: LOG_FILE по HOST (был захардкод agent_log_frezer4.txt);
    OLLAMA-WD.bat в ОСТРЫХ правках нет (рекомендация из ОТКРЫТО #5 —
    CPU-нужда: set OLLAMA_NUM_THREADS=16 перед пуском, кто пускает Ollama).
12. Зеркало паспорта в git: копия PASSPORT.md в D:\AI\repo\PASSPORT.md
    (github-страховка теперь покрывает паспорт — пушится GIT_SYNC).
13. Живая проверка с panel_ui.py (11.09): login ok, panel_ui.py — «Первая строка
    файла: # -*- coding: utf-8 -*-», win.ini — честный отказ.

## ОТКРЫТО
1. agent.py всё ещё монолит ~68 КБ: PAGE вынесен (ЗАКРЫТО #9), но HTML/шаблоны
   стрима и инлайн-CSS остались; разнести статику стрима — бэклог.
2. Рекомендация (не баг): OLLAMA_NUM_THREADS=16 перед пуском Ollama (CPU-нужда
   Creo и системе); постановка в пускач — на усмотрение пускающего.
3. Косметика (не трогать): settings.py dict B — дубли ключей (log_mode,
   night_hour/minute по 2-3 раза); scanner.py — переопределения def (работает
   последний); settings.py тройной блок auto_mode (работает последний).
4. Требует рантайм-проверки (вечером): qa_night.bat после всех правок дня.
5. panel_ui.py синхронизирован с agent.py вручную: при правке UI правится
   panel_ui.py, при правке протокола — agent.py; пересечение — сверять.

## Ключевые однострочники (PowerShell)
- RAW модели:
  python -c "import sys;sys.path.insert(0,r'D:\AI\tools\agent');import agent,core,settings;r=core.post('/api/chat',{'model':settings.model_for('chat'),'stream':False,'messages':[{'role':'system','content':agent.build_system()},{'role':'user','content':'какая модель открыта в Creo?'}]},t=180);print('RAW>>>'+(r.get('message') or {}).get('content','')[:500]+'<<<')"
- Вычистить историю:
  python -c "import sqlite3;c=sqlite3.connect(r'D:\AI\tools\agent\data\agent.sqlite');print(c.execute('DELETE FROM history').rowcount);c.commit()"
- Бэкап БД:
  python -c "import shutil;shutil.copy2(r'D:\AI\tools\agent\data\agent.sqlite',r'D:\AI\tools\agent\data\backup_'+__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M')+'.sqlite')"
- FAIL из probe:
  Select-String -Path D:\AI\tools\diag_full.log -Pattern "FAIL" | Select-Object -Last 5
- Все инструменты (имена):
  python -c "import sys;sys.path.insert(0,r'D:\AI\tools\agent');import tools_registry as TR;print(sorted(t['name'] for t in TR.TOOLS))"

## Промты-заготовки
- Мини-аудит файла (в Continue/внешний ИИ): «Ты аудитор. Файл: @<имя>.
  Формат: файл:строка — CRITICAL/WARN — суть — фикс. Проверь: синтаксис;
  рекурсия в себя; дубли def; except без лога; Path vs str; контракт TOOLS.
  Цитируй строки. Макс 10 пунктов.»

## ИЗМЕНЕНО (утро 09-07)
- Добавлен блок calc_tools (3 инструмента: calc, calc_units, calc_formulas) — инженерный калькулятор с единицами и формулами.
- Фактический счёт: 30 блоков / 113 инструментов (реестр tools_registry authoritative).
- Причина расхождения с прежними 29/109: паспорт считал 109 до того, как diagnostic_tools получил diag_usage и diag_web; плюс calc_tools не был учтён. Теперь реестр — источник правды (blocks=30, tools=113).
- Правки: README.md агента (29→30, 109→113, 94→98), паспорт (те же цифры).

## ИСТОРИЯ ОБНОВЛЕНИЙ (индекс)
- 11.09.2026 (вечер, заход 2) — вынос PAGE в panel_ui.py (agent ~60→37 КБ, сверка
  байтов, рестарт чист); ctl.py: --browser на 127.0.0.1 + \t-escape в copy_err;
  qa\qa_run.py LOG_FILE по HOST; зеркало PASSPORT.md → D:\AI\repo (github-страховка).
- 11.09.2026 (день) — оздоровительный заход (8 пунктов, см. ЗАКРЫТО 11.09): UTF-8 кодировка,
  дубль /status, AI-WATCH, секреты → secrets.json, read_roots для read_file,
  чистка tmp, GIT_SYNC с логом, doctor.py удалён; контракт .clinerules v5.1
  (read-only, правка только человеком). README: раздел doctor → новый workflow.
- 09-07.2026 — блок calc_tools, счёт 30/113, правки README+паспорта.
- 09-04.2026 — базовая редакция паспорта (C1-C3, C5, W1, W5/W6 и пр.).