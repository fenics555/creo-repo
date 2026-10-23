# SKILL: Creo Entity Role Identification (Internal Linkage Principle)

## ⚠️ ВАЖНО: ПРИНЦИП "ИМЯ — ЭТО ЛОЖЬ"
Никогда не классифицируйте файл Creo на основе его имени (`_Z`, `_O`, `_MSTR` и т.д.). Имена могут быть любыми и не отражают суть. 
**Единственный источник истины — внутренние бинарные связи внутри UGC-контейнера.**

## 🗺️ ИЕРАРХИЧЕСКИЕ УРОВНИ (PLM Chain Levels)
В тяжелом машиностроении (оснастка, литье) цепочка — это сквозной граф.

| Уровень | Тип сущности | Описание |
| :--- | :--- | :--- |
| **L1** | **Конструкторская Деталь (Base Part)** | Финальное изделие. Чистая геометрия. |
| **L2** | **Деталь-Заготовка (Preparation/Blank)** | Геометрия с припусками. Связь через `Merge`/`Inheritance`. |
| **L3** | **Деталь-Отливка (Casting)** | Увеличенная заготовка. Наличие коэффициента усадки. |
| **L4** | **Мастер-Модель (Master Model)** | Управляющая модель (линии разъема, уклоны). |
| **L5** | **Техпроцесс ЧПУ (CAM/Manufacturing)** | Сборка, содержащая траектории, инструменты и операции. |

## 🔍 МАТРИЦА ИДЕНТИФИКАЦИИ (Detection Matrix)

| Роль сущности | Бинарные маркеры / Признаки (Evidence) | Где искать |
| :--- | :--- | :--- |
| **Конструкторская деталь (Base Part)** | Отсутствие признаков заготовки/отливки; связь `NeuPrtSld -> Base_Part`. | `LargeText` / `FeatDefs` |
| **Деталь-заготовка (Blank/Z)** | Признаки `Merge` / `Inheritance`; суффикс `_z` (вспомогательно). | `FeatDefs` / `LargeText` |
| **Деталь-отливка (Casting/O)** | Параметр `PTC_SHRINKAGE_FACTOR` (8-byte double); токен `CHUGUN` в LargeText. | `BasFullData` / `LargeText` |
| **Мастер-модель (Master Model)** | Признаки `Parting Line`, `Draft` (уклоны), `Core Print` (стержни). | `AllFeatur` / `FeatDefs` |
| **Техпроцесс ЧПУ (CAM/ASM_MFG)** | Секции `ASSEM_MFG` или `FullMData`; наличие параметров `OP`, `TOOL`, `MACH`. | `TOC` / `FullMData` |

## 🛠️ РЕФЕРЕНСНЫЙ КОД (Python Template)

```python
def determine_plm_relation_type(ugc_header: dict, filename: str) -> str:
    """
    Автоматическое присвоение PLM-типа связи на основе UGC-заголовка и имени.
    """
    file_type = ugc_header.get("type", "").upper()
    cmnm = filename.lower()

    if file_type == "DRAWING":
        return "Сборочный чертеж (КД)"
        
    elif file_type == "ASSEMBLY/ASSEM_MFG":
        return "Технологический техпроцесс механообработки (CAM)"
        
    elif file_type == "ASSEMBLY":
        if "sb" in cmnm or "сб" in cmnm:
            return "Сборочная единица (Сборка приспособления)"
        return "Конструкторская подсборка"
        
    elif file_type == "PART":
        if cmnm.endswith("_z.prt") or "zag" in cmnm:
            return "Деталь-заготовка (Предыдущая обработка)"
        elif "otl" in cmnm or "lit" in cmnm or cmnm.endswith("_o.prt"):
            return "Деталь-отливка (Исходный металл)"
        return "Конструкторская деталь (КД)"
        
    return "Неизвестная сущность PLM"
```
*   ❌ Доверять структуре папок на диске.
