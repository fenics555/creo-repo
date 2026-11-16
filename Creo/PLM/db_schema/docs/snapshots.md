## Таблица: `snapshots`

**Описание:** Паспортный слой: Снапшоты состояний моделей (Core)

| Колонка | Тип | Примечание |
|---------|-----|------------|
| `path` | — | |
| `model` | — | |
| `folder` | — | |
| `size` | — | |
| `mtime` | — | |
| `volume` | — | |
| `material` | — | |
| `name` | — | |
| `designation` | — | |
| `rev` | — | |
| `author` | — | |
| `revdate` | — | |
| `role` | — | |
| `seen` | — | |
| `hist` | — | |
| `creo` | — | |
| `created` | — | |
| `pdata` | — | |

### Связи (из этой таблицы):
- `snapshots.model` → `params.model`
- `snapshots.path` → `params.path`
- `snapshots.model` → `bodies.model`
- `snapshots.path` → `bodies.path`
- `snapshots.model` → `materials.model`
- `snapshots.path` → `materials.path`
- `snapshots.model` → `master_mat.model`
- `snapshots.path` → `master_mat.path`
- `snapshots.model` → `matrices.model`
- `snapshots.path` → `matrices.path`
- `snapshots.model` → `components.model`
- `snapshots.path` → `components.path`
- `snapshots.model` → `drawing.model`
- `snapshots.path` → `drawing.path`
- `snapshots.model` → `features.model`
- `snapshots.path` → `features.path`
- `snapshots.model` → `dimensions.model`
- `snapshots.path` → `dimensions.path`
- `snapshots.model` → `dim_all.model`
- `snapshots.path` → `dim_all.path`
- `snapshots.model` → `equations.model`
- `snapshots.path` → `equations.path`
- `snapshots.model` → `health.model`
- `snapshots.path` → `health.path`
- `snapshots.model` → `history.model`
- `snapshots.path` → `history.path`
- `snapshots.model` → `changes.item`
- `snapshots.model` → `family.instance`
- `snapshots.model` → `graph_nodes.model`

### Связи (в эту таблицу):
- `links.parent` → `snapshots.model`
- `links.child` → `snapshots.model`
- `derived.base` → `snapshots.model`
- `derived.child` → `snapshots.model`
