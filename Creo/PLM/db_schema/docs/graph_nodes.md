## Таблица: `graph_nodes`

**Описание:** Графовый слой: Узлы связей

| Колонка | Тип | Примечание |
|---------|-----|------------|
| `model` | — | |
| `kind` | — | |
| `folder` | — | |
| `path` | — | |
| `size` | — | |
| `volume` | — | |
| `material` | — | |
| `creo` | — | |
| `rev` | — | |
| `n_down` | — | |
| `n_up` | — | |
| `has_media` | — | |

### Связи (в эту таблицу):
- `snapshots.model` → `graph_nodes.model`
- `graph_edges.from` → `graph_nodes.model`
- `graph_edges.to` → `graph_nodes.model`
