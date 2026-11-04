# Creo Skills Repository - Folder Structure

## 1. STANDARDS Directory - Canonical Parameters

### D:\AI\repo\Creo\STANDARDS\

**Purpose:** Contains the canonical (HELP .mat) material parameter dictionary.

**Key File:** `SKILL_material_parameters.md` (already exists)

**Content Organization:**
- **1. Два поколения параметров** - Dual generation of parameters
  - Canonical (no PTC_ prefix)
  - Home/custom (PTC_ prefix)
- **2. Каноничный словарь** - Canonical dictionary table
  - Parameter | Type | Units | Purpose
  - All standard Creo material properties
- **3. Три формы чисел в UGC файлах** - Number formats in UGC files
  - BE-double IEEE
  - Packed 3 bytes
  - Extended 8 bytes
- **4. Правило §8.76** - Service prefix `\xf7` to discard

**Canonical Parameters List:**
- YOUNG_MODULUS (Real, MPa) - модуль упругости
- POISSON_RATIO (Real, dimensionless) - отношение поперечной деформации
- SHEAR_MODULUS (Real, MPa) - модуль сдвига
- THERMAL_EXPANSION_REF_TEMPERATURE (K) - температура отсчета коэффициента теплового расширения
- STRUCTURAL_DAMPING_COEFFICIENT (dimensionless) - демпфинг
- STRESS_LIMIT_FOR_TENSION (MPa) - предел растяжения
- STRESS_LIMIT_FOR_COMPRESSION (MPa) - предел сжатия
- STRESS_LIMIT_FOR_SHEAR (MPa) - предел сдвига
- THERMAL_CONDUCTIVITY (W/mK) - теплопроводность
- EMISSIVITY (dimensionless) - коэффициент излучения
- SPECIFIC_HEAT (J/kgK) - теплоёмкость
- HARDNESS (HB/HRC) - твердость
- CONDITION (String) - состояние/размер
- INITIAL_BEND_Y_FACTOR - начальный коэффициент изгиба по оси Y
- BEND_TABLE (String) - таблица изгиба
- PRO_UNIT_MASS (String) - единица массы в Creo
- PRO_UNIT_LENGTH (String) - единица длины в Creo
- PRO_UNIT_SYS (String) - основная система единиц Creo

## 2. MATERIALS Directory - Material Organizations

### D:\AI\repo\Creo\MATERIALS\

**Purpose:** Organized material libraries and property definitions.

**Subdirectories:**

#### D:\AI\repo\Creo\MATERIALS\Canonical\
- **Description:** Canonical material parameters from HELP .mat
- Contains parameter definitions and references

#### D:\AI\repo\Creo\MATERIALS\Home\

**Description:** Custom/homegrown materials with PTC_ prefix

**Sub-subdirectories:**
- `D:\AI\repo\Creo\MATERIALS\Home\Steel\` - Steel materials
- `D:\AI\repo\Creo\MATERIALS\Home\Aluminum\` - Aluminum materials
- `D:\AI\repo\Creo\MATERIALS\Home\CastIron\` - Cast iron materials
- etc. for other material groups

**File naming convention:** `material_name.mtl` or `material_name_params.json`

#### D:\AI\repo\Creo\MATERIALS\PTC_Prefixed\
- **Description:** Materials using PTC_ prefix format
- Contains .mtl files and parameter definitions

## 3. Z:\PTC\CREO-START\ Integration

### Connection to Existing Structure:

The existing `Z:\PTC\CREO-START\НАСТРОЙКИ\Материалы общего вида` directory should be referenced/organized as:

```
Reference: Z:\PTC\CREO-START\НАСТРОЙКИ\Материалы общего вида\
  ├── Steel\Steel_углеродистая_обыкновенного_качества\stal_st1kp.mtl
  └── [Other material directories]
```

**Integration Plan:**
- The `update_mtl.ps1` script should be moved/referenced in: `D:\AI\repo\Creo\TOOLS\material_updater\`
- Material files in Z: drive should be mirrored/organized in D:\AI\repo\Creo\MATERIALS\
- PTC-specific properties (PTC_IMPACT_ENERGY, PTC_FATIGUE_STRENGTH, etc.) should be documented

## 4. PTC Installation Reference

### From CREO_MAP.md:
- **Creo 12.4.2.0** installed at: `D:\PTC\CREO12\Creo 12.4.2.0`
- Full help documentation at: `D:\PTC\CREO12\Creo 12.4.2.0\Common Files\creo_help_pma`
- Russian help: `D:\PTC\CREO12\Creo 12.4.2.0\Common Files\creo_help_pma\russian`

## 5. Rules and Conventions

### Parameter Naming Rules:
1. **Canonical parameters:** No `PTC_` prefix (e.g., `YOUNG_MODULUS`, `POISSON_RATIO`)
2. **Home/custom materials:** `PTC_` prefix required (e.g., `PTC_YOUNG_MODULUS`, `PTC_HARDNESS_TYPE`)
3. **Rule:** Never mix - either canonical OR PTC_prefixed, not both for same parameter

### File Organization:
- `.mtl` files in materials libraries
- Parameter definitions in JSON or markdown
- Scripts in TOOLS directory
- Documentation in DOCS or inline in markdown files

## 6. Recommended Actions

1. **Move** `update_mtl.ps1` to `D:\AI\repo\Creo\TOOLS\material_updater\`
2. **Create** material organization structure under `D:\AI\repo\Creo\MATERIALS\`
3. **Document** the canonical parameter dictionary from `SKILL_material_parameters.md`
4. **Mirror/Reference** the Z: drive materials in the new structure
5. **Update** the `SKILL_material_parameters.md` with any new findings
6. **Create** cross-references between Z: drive materials and D:\AI\repo structure

## 7. Structure Summary Diagram

```
D:\AI\repo\Creo\
├── STANDARDS/          # Canonical parameters (already has SKILL_material_parameters.md)
│   └── SKILL_material_parameters.md
│
├── MATERIALS/          # Organized material libraries
│   ├── Canonical/      # Standard Creo parameters
│   ├── Home/           # Custom materials with PTC_ prefix
│   │   ├── Steel/
│   │   ├── Aluminum/
│   │   └── ...
│   └── PTC_Prefixed/   # PTC-format materials
│
├── TOOLS/              # Including update_mtl.ps1
│   └── material_updater/
│       └── update_mtl.ps1
│
├── DOCS/               # Documentation
│   └── ...
│
└── STRUCTURE.md        # This file
```