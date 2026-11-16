# Creo PLM — Скиллы и схема базы данных

## Архитектура и паспорт базы данных PLM Reader (актуально с V185)

Полный автогенерируемый паспорт всех 31 таблиц, 22 логических связей и 4 тематических ER-диаграмм находится в папке [`db_schema/docs/`](db_schema/docs/README.md) (конфигурация связей — [`db_schema/.tbls.yml`](db_schema/.tbls.yml)).

### Четыре обязательных правила работы с PLM-базой
1. **Единый источник правды:** Все запросы аналитики, графа и отчётов выполняются строго по SQLite-базе `plm_reader.db`, без прямого сканирования сетевого диска `Z:` из скиллов.
2. **Защита накопленной истории (`Purge-safe`):** Таблицы `changes`, `history`, `arch_dims`, `arch_dim_ch` хранят историю по удалённым после Purge итерациям файлов Creo — их очистка и перезапись запрещены.
3. **Разделение связей (`origin='real'` vs `origin='built'`):** Прямые факты из файлов имеют `origin='real'`; выведенные обратные связи («снизу вверх» из `plm_build_links.py`) имеют `origin='built'`.
4. **Точные ключи связывания таблиц (проверено линтером):**
   - `snapshots.model` ↔ `params.model`, `bodies.model`, `materials.model`, `master_mat.model`, `matrices.model`, `components.model`, `drawing.model`, `features.model`, `dimensions.model`, `dim_all.model`, `equations.model`, `health.model`, `history.model`, `arch_dims.model`, `arch_dim_ch.model`, `graph_nodes.model`
   - `snapshots.model` ↔ `changes.item` (колонка называется `item`, а не `model`!)
   - `snapshots.model` ↔ `family.instance` (колонка называется `instance`!)
   - `snapshots.model` ↔ `links.parent` / `links.child`, `derived.base` / `derived.child`, `graph_edges.from` / `graph_edges.to`

### Встроенный аудит и обновление документации схемы (`plm_database.py`)
- `python plm_database.py check --full` — проверка целостности SQLite, расхождения колонок с эталоном `SCHEMA` и наличия индексов на связующих колонках.
- `python plm_database.py export-docs` — пересборка `schema_passport.md` и 4 Mermaid ER-диаграмм по `.tbls.yml`.
