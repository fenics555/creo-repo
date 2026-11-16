## Таблица: `master_mat`

**Описание:** Справочник материалов: Эталонные значения

| Колонка | Тип | Примечание |
|---------|-----|------------|
| `path` | — | |
| `model` | — | |
| `current_material` | — | |
| `master_name` | — | |
| `reported_name` | — | |
| `has_master` | — | |

### Связи (в эту таблицу):
- `snapshots.model` → `master_mat.model`
- `snapshots.path` → `master_mat.path`
