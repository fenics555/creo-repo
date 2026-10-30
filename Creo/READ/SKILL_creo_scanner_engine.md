# SKILL: ЕДИНЫЙ СКАНЕР ДОМА (`engine.py`) — ЧТО ЧИТАЕТ / СОБИРАЕТ / ПИШЕТ

> **Дата:** 30.10.2026 · **§172 в `SKILL_GRABLI.md`**
> **Файл:** `D:\AI\tools\agent\plm_reader\engine.py` (**227 108 Б** — главный движок)
> **Владелец:** «в доме читает ОДИН инструмент-сканер, он же пишет сразу в базу ЛИВ-живые данные
> из файлов Creo. Он собирает всё что нужно сразу в базу: параметры / материалы / что кто где
> поменял / связи / картинку превью… **И почему же он не пишет сразу всё что нужно, а что-то
> другое это доделывает?**»

## 🔴 ОТВЕТ НА ВОПРОС ВЛАДЕЛЬЦА
**Сканер УЖЕ пишет всё.** Движок `engine.py` собирает **11 таблиц** за один проход:
```
snapshots (паспорт+volume+material)  params (ВСЕ параметры)   history (кто/когда/ПК/Creo)
links (состав)      derived (наследование)   props (свойства)   family (семейства)
folders (дерево)    health (ЗДОРОВЬЕ)        changes (изменения) meta
+ ПРЕВЬЮ: save_media() → db\media\  (из ТЕХ ЖЕ байтов, файл не читается дважды)
```
**⇒ Мои `plm_import_mass.py` / `plm_feattype.py` — НЕ замена сканеру, а ОТЛАДКА нового канала.**
Правильно: **добавить функцию в `engine.py`**, а не плодить параллельные скрипты.

## ✅ ЧТО УЖЕ ЕСТЬ В ДВИЖКЕ (не надо изобретать!)
| Функция | Что даёт | Без Creo |
|---|---|---|
| `scan_item()` (стр.1018) | **ВСЁ за одно чтение файла** (§96.1.1 «один файл — одно чтение») | ✅ |
| `creo_params(raw)` (1398) | **все параметры модели** (имя+тип+значение) | ✅ |
| `family_of(raw)` (1426) | **таблица семейства** (генерик ↔ исполнения) | ✅ |
| `creo_history(raw)` (1034) | **кто/когда/ПК/версия Creo** | ✅ |
| **`creo_health(raw)`** | **ЗДОРОВЬЕ: `reg_status` · `inactive_geom` · `mdl_geom_rev`** | ✅ |
| `merge_base_parts(raw)` (351) | **ВСЕ родители наследования** (до 5 у оснастки) | ✅ |
| `ref_part_parents(raw)` (515) | родители производной детали | ✅ |
| `inherited_properties(raw)` (480) | **наследование СВОЙСТВА** (не геометрии) | ✅ |
| `copy_from_of(raw)` (556) | «модель скопирована от…» | ✅ |
| `asm_components(raw)` (1060) | **состав сборки** | ✅ |
| `save_media(raw)` (983) | **ПРЕВЬЮ** (картинка) | ✅ |
| `derived_of(raw)` (579) | заготовка/отливка (первый) | ✅ |

## 🏥 `health` — РАБОТАЕТ (замер 30.10.2026, живой файл)
```python
creo_health(raw) →
  {'regen': 'требует регенерации', 'reg_status': '102', 'inactive': 1, 'geom_rev': ''}
```
**Признаки (все в файле, Creo НЕ нужен):**
| Признак | Regex/поле | Смысл |
|---|---|---|
| `reg_status` | `reg_status\x00(.)` | **0 = регенерирована**, иное = **требует регенерации** |
| `MdlStatus` / `Sld_MdlStatus` | текст | статус модели есть |
| `inactive_geom` | счёт вхождений | **неактивная геометрия** |
| `mdl_geom_rev` | `mdl_geom_rev\x00(…)\x00` | ревизия геометрии |

**⚠️ ПОЧЕМУ В БАЗЕ 0 СТРОК:** таблица `health` создана в **V135** (в `SCHEMA`, не в `try` —
грабля 28.10.2026: `CREATE` внутри `try` глотал исключение → «no such table: health»).
**Скан после V135 по всему складу НЕ проходил** ⇒ таблица пуста. **Лечение: запустить скан.**
Проверка: `model_health(model)` — читает из базы (готова).

## 📤 КУДА ПИШЕТ (все INSERT — факт из кода)
```
snapshots : INSERT OR REPLACE  (path,model,folder,size,mtime,volume,material,name,
                                designation,rev,author,revdate,role,seen,hist,creo,created)
params    : INSERT             (path,model,name,type,value)
history   : INSERT (перед этим DELETE по path)  (path,model,ts,user,computer,creo,rev,action)
health    : INSERT OR REPLACE  (path,model,regen,reg_status,inactive,geom_rev)
links     : 4 вставки          (parent,child,qty,source,origin) — состав/семейство/наследование
derived   : INSERT             (child,base,kind,source,origin)
props     : INSERT             (child,prop,value,source)
family    : INSERT             (generic,instance,params,source)
folders   : INSERT             (path,parent,depth,models,files,seen)
changes   : 3 вставки          (item,rev,kind,descr,who,ts)
meta      : 4 вставки          (k,v)
```

## 🎯 ЧТО ОСТАЛОСЬ ДОБАВИТЬ В ДВИЖОК (задачи, а не «свои скрипты»)
| # | Что | Готовый канал |
|---|---|---|
| 1 | **МАССА** (`MASS`) | формат §167 `e3 32 [тип] [7 байт]` — добавить в `scan_item` |
| 2 | **ПЛОТНОСТЬ** (`PRO_MP_DENSITY`) | вывод из (масса, объём) |
| 3 | **ПЛОЩАДЬ** (`PRO_MP_AREA`) | тот же `e3 32` |
| 4 | **ТИП ЭЛЕМЕНТА** (`pfcFEATTYPE`) | `feat_defs_<N> − 910` + словарь `pfcFeature.h` (314) |
| 5 | **ДЕРЕВО ПОСТРОЕНИЯ** | `#AllFeatur → Sld_Features → first_feat_ptr` (открыто) |
| 6 | **КВАЛИТЕТ** (`tol_class`) | `dim_array` (§164) |
| 7 | **COG · инерция** | `PRO_MP_COG*` · `PRO_MP_IXX…` |

## 🔴 ПРАВИЛО ДОМА (закон владельца)
**Читает ОДИН инструмент — `engine.py`. Новый канал = НОВАЯ ФУНКЦИЯ В ДВИЖКЕ, а не отдельный скрипт.**
Отдельный скрипт — только для **отладки/замера** (в `PROBA`), затем переносится в `engine.py`.
