## Таблица: `health`

**Описание:** Аналитический слой: Состояние здоровья моделей

| Колонка | Тип | Примечание |
|---------|-----|------------|
| `path` | — | |
| `model` | — | |
| `regen` | — | |
| `reg_status` | — | |
| `inactive` | — | |
| `geom_rev` | — | |

### Связи (в эту таблицу):
- `snapshots.model` → `health.model`
- `snapshots.path` → `health.path`
