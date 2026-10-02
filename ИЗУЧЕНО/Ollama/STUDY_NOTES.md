# КОНСПЕКТ ИЗУЧЕНИЯ: Ollama (локальный раннер моделей)

- ИЗУЧЕНО: 02.10.2026, Cline
- ИСТОЧНИК: `ollama help`, `ollama serve --help`, `ollama run --help`, `ollama create --help`,
  `ollama show --help`, `ollama stop --help`, `ollama pull --help`, `ollama ps --help`
- ПОВОД: дом работал с Ollama с сентября 2026 и не знал части её возможностей; правки по хелпу
  нашлись случайно, уже после нескольких часов работы
- МЕТОД: `PROMPT\SKILL_learning_new_direction.md` (начать с хелпа)

---

## 1. Версия и главное

`ollama --version` → **ollama version is 0.34.1**.

## 2. Команды (`ollama help`, полный список)

| команда | что делает |
|---|---|
| `serve` (алиас `start`) | запустить сервер |
| `create` | создать модель из Modelfile |
| `show` | информация о модели |
| `run` | запуск модели в диалоге |
| `stop` | остановить загруженную модель |
| `pull` / `push` | скачать / залить в реестр |
| `signin` / `signout` | аккаунт ollama.com |
| `list` | список моделей |
| `ps` | список **загруженных** моделей |
| `cp` / `rm` | копировать / удалить |
| `launch` | меню Ollama или интеграция (новая команда, в доме не используется) |

Глобальные флаги: `-h/--help`, `--nowordwrap`, `--verbose`, `-v/--version`.

## 3. КЛЮЧЕВОЕ ДЛЯ ДОМА: `think` — это УРОВЕНЬ, а не булев

```
--think string[="true"]   Enable thinking mode: true/false or high/medium/low for supported models
--hidethinking            Hide thinking output (if provided)
```

**ФАКТ (дословно из справки).** Дом передаёт в `/api/chat` поле `think` как Python-bool
(`loop_revive_test.py:235`). Значит дом умеет просить только «думать / не думать», тогда как
Ollama умеет просить **«думать короче»** (`low`).

**ЧТО ЭТО МЕНЯЕТ.** Рассылка промпта жгла `num_predict` у reasoning-моделей (у gpt-oss при
260 токенах `content` пуст, `done_reason=length`). Возможное дешёвое решение — просить `think: "low"`,
а не поднимать лимит до 2000 (экономия 40-55 минут прогона).

**ПРОВЕРОЧНЫЙ СТАТУС: НЕ ПРОВЕРЕНО** (живая проба не проводилась — момент её проведения указан
в `SKILL_num_predict_for_reasoning_models.md` §8).

`--hidethinking` — только прячет вывод размышления, не уменьшает его и не влияет на расход лимита.

## 4. Переменные окружения сервера (`ollama serve --help`) — полный список

| переменная | что делает | значение по умолчанию | отношение к дому |
|---|---|---|---|
| `OLLAMA_CONTEXT_LENGTH` | длина контекста, если не указано иначе | **4k/32k/256k в зависимости от VRAM** | отвечает на вопрос скилла `ctx_limit_vs_section_limit`: дефолт окна задаётся здесь, а не строкой в `/api/show` |
| `OLLAMA_LOAD_TIMEOUT` | сколько ждать загрузку модели до отказа | **5m** | **кандидат на причину молчаливых обрывов** на моделях 10-15 ГБ |
| `OLLAMA_KEEP_ALIVE` | сколько модель живёт в памяти | 5m | совпадает со значением `UNTIL` в `ollama ps` — подтверждено |
| `OLLAMA_MAX_LOADED_MODELS` | сколько моделей на GPU | — | в доме = 1, поэтому проверки вытесняют рабочую модель |
| `OLLAMA_NUM_PARALLEL` | параллельных запросов | — | дом не использует, модели гоняются последовательно |
| `OLLAMA_MAX_QUEUE` | длина очереди | — | не используется |
| `OLLAMA_MAX_TRANSFER_STREAMS` | потоков при скачивании | 4 | не используется |
| `OLLAMA_DEBUG` | подробный отладочный вывод | — | **включать при разборе обрывов загрузки** |
| `OLLAMA_MODELS` | путь к каталогу моделей | — | не используется |
| `OLLAMA_HOST` | адрес сервера | 127.0.0.1:11434 | стенд ходит сюда |
| `OLLAMA_NUM_PARALLEL`, `OLLAMA_SCHED_SPREAD`, `OLLAMA_FLASH_ATTENTION`, `OLLAMA_KV_CACHE_TYPE`, `OLLAMA_LLM_LIBRARY`, `OLLAMA_GPU_OVERHEAD`, `OLLAMA_IGPU_ENABLE`, `LLAMA_ARG_FIT`, `LLAMA_ARG_FIT_TARGET`, `OLLAMA_NOPRUNE`, `OLLAMA_ORIGINS`, `OLLAMA_NO_CLOUD` | прочее | — | в доме не используются, записано для полноты |

**Строки взяты дословно из справки 0.34.1; дом этими переменными раньше не пользовался.**

## 5. `ollama create`

```
-f, --file string             Name of the Modelfile (default "Modelfile")
-q, --quantize string         Quantize safetensors model to this level (e.g. nvfp4)
    --draft-quantize string   Quantize safetensors draft model to this level
    --force                   Continue local creation when MLX validation fails
```

Значение для дома: при пересборке моделей `Apply-AgentParams.ps1` эти флаги не используются —
модель пересоздаётся из исходного `FROM`, параметры меняются построчно.

## 6. `ollama show`

`-v/--verbose`, `--license`, `--modelfile`, `--parameters`, `--system`, `--template`.
Дом пользуется `--modelfile` и `--parameters` — это подтверждает, что **`num_ctx` в
`parameters` не показывается** (дефолт окна живёт в `OLLAMA_CONTEXT_LENGTH`, см. §4).

## 7. Чего в справке НЕТ (и это нормально)

- Справка CLI **не описывает HTTP-API** (`/api/chat`, `prompt_eval_count`, поля `thinking`).
  Дом пользуется API напрямую — значит по API нужна отдельная документация (ollama.com/docs).
- В справке нет ни слова про `prompt_eval_count`, который в доме врёт на переполнении окна
  (скилл `SKILL_ctx_limit_vs_section_limit.md` §4) — это свойство API, не CLI.

## 8. Выводы и что с этим делать

1. **Правило «начать с хелпа» подтверждено фактом на своей цене:** 2 минуты хелпа дали
   `--think low`, `OLLAMA_LOAD_TIMEOUT` и `OLLAMA_CONTEXT_LENGTH` — то есть объяснение двух
   молчаливых обрывов и, возможно, способ отменить подъём лимита.
2. **Следующий шаг — проба `think: "low"`** одним запросом к gpt-oss при `num_predict=260`.
3. **При следующем обрыве загрузки** — `OLLAMA_DEBUG=1` и `OLLAMA_LOAD_TIMEOUT=10m`.
4. **Справка CLI не покрывает API** — при изучении HTTP-части нужен `ollama.com/docs`, а не `help`.

## 9. Проверка конспекта

Ответить: (а) какие четыре вещи дом не знал про Ollama и нашёл за 2 минуты в хелпе;
(б) почему справка не описала `prompt_eval_count`; (в) какой следующий шаг проверит `think: "low"`.