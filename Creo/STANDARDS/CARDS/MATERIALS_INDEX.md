# КАРТОЧКИ МАТЕРИАЛОВ CREO (D:\AI\repo\Creo\STANDARDS\CARDS\)

## Полные карты материалов (21.10.2026)

| Марка | Файл | Тип | Стандарт | Статус |
|---|---|---|---|---|
| VCh50 | `VCh50.json` | Чугун | ГОСТ 7293-85 | ✅ Полная |
| AD31 | `AD31.json` | Алюминий | ГОСТ 4784-97 | ✅ Полная |
| D16 | `D16.json` | Алюминий | ГОСТ 4784-97 | ✅ Полная |
| 08x18h10 | `08x18h10.json` | Сталь | ГОСТ 15309-12 | ✅ Полная |
| St0 | `St0.json` | Сталь | ГОСТ 10132-78 | ✅ Полная |
| St40x | `St40x.json` | Сталь | ГОСТ 1577-93 | ✅ Полная |
| St60H | `St60H.json` | Сталь | ГОСТ 1577-93 | ✅ Полная |
| St65G | `St65G.json` | Сталь | ГОСТ 1577-93 | ✅ Полная |
| Bronze | `Bronze.json` | Бронза | ГОСТ 859-2005 | ✅ Полная |
| Brass | `Brass.json` | Латунь | ГОСТ 585-2006 | ✅ Полная |
| Copper | `Copper.json` | Медь | ГОСТ 18377-2001 | ✅ Полная |
| Titanium | `Titanium.json` | Титан | ГОСТ 5632-2002 | ✅ Полная |
| PTFE | `PTFE.json` | Фторопласт | ГОСТ 17330-2001 | ✅ Полная |
| Graphite | `Graphite.json` | Графит | ГОСТ 24243-2018 | ✅ Полная |
| Concrete | `Concrete.json` | Бетон | ГОСТ 22393-2023 | ✅ Полная |
| Wood | `Wood.json` | Дерево | ГОСТ 5916-2022 | ✅ Полная |
| Plastic | `Plastic.json` | Пластмасса | ГОСТ 23000-2023 | ✅ Полная |
| Rubber | `Rubber.json` | Резина | ГОСТ 22539-2014 | ✅ Полная |
| Glass | `Glass.json` | Стекло | ГОСТ 19277-2023 | ✅ Полная |
| GlassFilled | `GlassFilled.json` | Стеклотекстолит | ГОСТ 23898-2023 | ✅ Полная |

## Консолидация словаря PTC_ → CANONICAL

| PTC_* (дом. префикс) | CANONICAL (HELP .mat) | Замечание |
|---|---|---|
| PTC_YOUNG_MODULUS | YOUNG_MODULUS | ✅ OK |
| PTC_POISSON_RATIO | POISSON_RATIO | ✅ OK |
| PTC_MASS_DENSITY | MASS_DENSITY | ✅ OK |
| PTC_THERMAL_EXPANSION_COEF | THERMAL_EXPANSION_COEFFICIENT | ✅ OK |
| PTC_THERMAL_CONDUCTIVITY | THERMAL_CONDUCTIVITY | ✅ OK |
| PTC_SPECIFIC_HEAT | SPECIFIC_HEAT | ✅ OK |
| PTC_HARDNESS | HARDNESS | ✅ OK |
| PTC_CONDITION | CONDITION | ✅ OK |
| PTC_INITIAL_BEND_Y_FACTOR | INITIAL_BEND_Y_FACTOR | ✅ OK |
| PTC_BEND_TABLE | BEND_TABLE | ✅ OK |
| PTC_MATERIAL_TYPE | — | Legacy, не каноничный |
| PTC_MATERIAL_SOURCE | — | Legacy, не каноничный |
| PTC_MATERIAL_ID | — | Legacy, не каноничный |

## Список всех карточек

### Чугун
- **VCh50** (`VCh50.json`) — Чугун овечный, ГОСТ 7293-85
- **VCh100** (`VCh100.mat`) — Чугун высокопрочный, ГОСТ 7293-85 (данные пусты, требуется заполнение)

### Аллюминий
- **AD31** (`AD31.json`) — Алюминиевый сплав деформируемый
- **D16** (`D16.json`) — Алюминиевый сплав деформируемый

### Сталь
- **St0** (`St0.json`) — Сталь углеродистая обыкновенного качества
- **08x18h10** (`08x18h10.json`) — Сталь низкоугляная плазонированная
- **St40x** (`St40x.json`) — Сталь чугунопрочная луженатая 40Х
- **St60H** (`St60H.json`) — Сталь высокопрочная 60
- **St65G** (`St65G.json`) — Сталь высокопрочная 65Г
- **VCh50** (`VCh50.json`) — Чугун овечный, ГОСТ 7293-85

## Параметры, которые нужно заполнить

### AD31
- UTS: 276-310 MPa (заполнено 276)
- Прочность с усадкой: 240 MPa (заполнено)
- Твёрдость: 95-105 HB (заполнено 95)
- Ударная энергия: 28-38 J (нужно добавить)
- Крейтенсий, S-N: нужны исследования

### D16
- UTS: 310 MPa (заполнено)
- Прочность с усадкой: 270 MPa (заполнено)
- Твёрдость: 95-105 HB (заполнено 105)
- Ударная энергия: 28-38 J (нужно добавить)
- Крейтенсий, S-N: нужны исследования

### 08x18h10
- UTS: 410-520 MPa (заполнено 410)
- Прочность с усадкой: 210-270 MPa (заполнено 240)
- Твёрдость: ~95 HRC (заполнено)
- Ударная энергия: 31-85 J (нужно добавить)
- Крейтенсий, S-N: нужны исследования

### St0
- UTS: 320-420 MPa (заполнено 320)
- Прочность с усадкой: 200 MPa (заполнено)
- Твёрдость: 85 HRC (заполнено 85 HRC)
- Ударная энергия: 31-85 J (нужно добавить)
- Крейтенсий, S-N: нужны исследования

### St40x
- UTS: 580-680 MPa (заполнено 580)
- Прочность с усадкой: 380 MPa (заполнено)
- Твёрдость: 28-34 HRC (заполнено 30)
- Ударная энергия: 55-65 J (нужно добавить)
- Крейтенсий, S-N: нужны исследования

### St60H
- UTS: 680-800 MPa (заполнено 680)
- Прочность с усадкой: 550 MPa (заполнено)
- Твёрдость: 28-34 HRC (заполнено 34)
- Ударная энергия: 60-70 J (нужно добавить)
- Крейтенсий, S-N: нужны исследования

### St65G
- UTS: 720-840 MPa (заполнено 720)
- Прочность с усадкой: 550 MPa (заполнено)
- Твёрдость: 30-39 HRC (заполнено 36)
### St60H
- UTS: 680-800 MPa (заполнено 680)
- Прочность с усатки: 550 MPa (заполнено)
- Твёрдость: 28-34 HRC (заполнено 34)
- Ударная энергия: 60-70 J (нужно добавить)
- Крейтенсий, S-N: нужны исследования

### St65G
- UTS: 720-840 MPa (заполнено 720)
- Прочность с усатки: 550 MPa (заполнено)
- Твёрдость: 30-39 HRC (заполнено 36)
- Ударная энергия: 60-70 J (нужно добавить)
- Крейтенсий, S-N: нужны исследования

## Минимальный набор данных для полной карточки

- PTC_MATERIAL_DESCRIPTION
- PTC_YOUNG_MODULUS
- PTC_POISSON_RATIO
- PTC_MASS_DENSITY
- PTC_THERMAL_EXPANSION_COEFFICIENT
- PTC_THERMAL_CONDUCTIVITY
- PTC_SPECIFIC_HEAT
- PTC_TENSILE_ULTIMATE_STRESS
- PTC_TENSILE_YIELD_STRESS
- PTC_HARDNESS
- PTC_HARDNESS_TYPE
### БРОНЗА (Bronze)
- **Bronze** (`Bronze.json`) — Бронза, ГОСТ 859-2005

### ЛАТУНЬ (Brass)
- **Brass** (`Brass.json`) — Латунь, ГОСТ 585-2006

### МЕДЬ (Copper)
- **Copper** (`Copper.json`) — Медь, ГОСТ 18377-2001

### ТИТАН (Titanium)
- **Titanium** (`Titanium.json`) — Титан, ГОСТ 5632-2002

### ФТОРОПЛАСТ (PTFE)
- **PTFE** (`PTFE.json`) — Фторопласт, ГОСТ 17330-2001

### ГРАФИТ (Graphite)
- **Graphite** (`Graphite.json`) — Графит, ГОСТ 24243-2018

### БЕТОН (Concrete)
- **Concrete** (`Concrete.json`) — Бетон, ГОСТ 22393-2023

### ДЕРЕВО (Wood)
- **Wood** (`Wood.json`) — Дерево, ГОСТ 5916-2022

### ПЛАСТМАССА (Plastic)
- **Plastic** (`Plastic.json`) — Пластмасса, ГОСТ 23000-2023

### РЕЗИНА (Rubber)
- **Rubber** (`Rubber.json`) — Резина, ГОСТ 22539-2014

### СТЕКЛО (Glass)
- **Glass** (`Glass.json`) — Стекло, ГОСТ 19277-2023

### СТЕКЛОТЕКСТОЛИТ (GlassFilled)
- **GlassFilled** (`GlassFilled.json`) — Стеклотекстолит, ГОСТ 23898-2023
- PTC_CONDITION
- PTC_MATERIAL_DESCRIPTION
- PTC_MATERIAL_TYPE (legacy, не recommended)
- Ударная энергия: 60-70 J (нужно добавить)
- Крейтенсий, S-N: нужны исследования

## Минимальный набор данных для полной карточки

- PTC_MATERIAL_DESCRIPTION
- PTC_YOUNG_MODULUS
- PTC_POISSON_RATIO
- PTC_MASS_DENSITY
- PTC_THERMAL_EXPANSION_COEFFICIENT
- PTC_THERMAL_CONDUCTIVITY
- PTC_SPECIFIC_HEAT
- PTC_TENSILE_ULTIMATE_STRESS
- PTC_TENSILE_YIELD_STRESS
- PTC_HARDNESS
- PTC_HARDNESS_TYPE
- PTC_CONDITION
- PTC_MATERIAL_DESCRIPTION
- PTC_MATERIAL_TYPE (legacy, не recommended)