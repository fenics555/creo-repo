# Документация схемы базы PLM Reader

Автогенерировано из `.tbls.yml`.


База данных: `D:/AI/tools/agent/plm_reader/db/plm_reader.db`


Всего таблиц: 31


## Список таблиц

- [`arch_dim_ch.md`](arch_dim_ch.md) 
- [`arch_dims.md`](arch_dims.md) 
- [`bodies.md`](bodies.md) — Геометрический слой: Массы и объемы тел
- [`changes.md`](changes.md) — Журнал изменений: Кто/Когда/Что
- [`components.md`](components.md) — Составной слой: Дерево сборки и компонентов
- [`derived.md`](derived.md) — Производные модели
- [`dim_all.md`](dim_all.md) — Агрегированный слой: Все размеры
- [`dimensions.md`](dimensions.md) — Размерный слой: Геометрические размеры
- [`drawing.md`](drawing.md) — Документационный слой: Связи с чертежами
- [`equations.md`](equations.md) — Математический слой: Уравнения и зависимости
- [`family.md`](family.md) — Семейный слой: Вариации модели
- [`features.md`](features.md) — Конструктивный слой: Дерево фичеров
- [`folders.md`](folders.md) 
- [`graph_edges.md`](graph_edges.md) — Графовый слой: Ребра связей
- [`graph_metrics.md`](graph_metrics.md) 
- [`graph_nodes.md`](graph_nodes.md) — Графовый слой: Узлы связей
- [`health.md`](health.md) — Аналитический слой: Состояние здоровья моделей
- [`history.md`](history.md) — Архивный слой: История версий
- [`item_ver.md`](item_ver.md) 
- [`items.md`](items.md) 
- [`links.md`](links.md) — Связи компонентов
- [`mass_props.md`](mass_props.md) 
- [`master_mat.md`](master_mat.md) — Справочник материалов: Эталонные значения
- [`materials.md`](materials.md) — Материальный слой: Свойства материалов
- [`matrices.md`](matrices.md) — Математический слой: Матрицы трансформации
- [`meta.md`](meta.md) 
- [`params.md`](params.md) — Параметрический слой: Значения параметров моделей
- [`props.md`](props.md) 
- [`snapshots.md`](snapshots.md) — Паспортный слой: Снапшоты состояний моделей (Core)
- [`tools.md`](tools.md) 
- [`unknown_fields.md`](unknown_fields.md) 

## ER-диаграммы (Mermaid)


Схема разделена на 4 точки обзора (viewpoints):

- **Паспорт и геометрия** — Основные данные моделей и их физика
  Таблицы: `snapshots`, `params`, `bodies`, `materials`, `master_mat`, `matrices`
  Диаграмма: [`er_Паспорт и геометрия.mmd`](er_Паспорт и геометрия.mmd)
- **Связи и состав** — Структура сборок и фичеров
  Таблицы: `snapshots`, `components`, `features`, `drawing`, `family`
  Диаграмма: [`er_Связи и состав.mmd`](er_Связи и состав.mmd)
- **История и архив** — Журналы и изменения
  Таблицы: `snapshots`, `history`, `changes`, `equations`
  Диаграмма: [`er_История и архив.mmd`](er_История и архив.mmd)
- **Граф и консоль** — Топология связей
  Таблицы: `snapshots`, `graph_nodes`, `graph_edges`, `health`, `dimensions`, `dim_all`
  Диаграмма: [`er_Граф и консоль.mmd`](er_Граф и консоль.mmd)