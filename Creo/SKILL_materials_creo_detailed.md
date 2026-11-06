# CREO MATERIALS SKILLS - DETAILED CURRICULUM
# Repository: D:\AI\repo\Creo
# Version: 1.0 (based on updated .mtl files for Creo 12.4.2.0)
# ⚠️ 05.11.2026: проверено замером — этот конспект описывает РАБОЧИЙ формат `.mtl` (PTC_* — верно),
#    но НЕ описывает `.mat` (словарь без PTC_ — ДРУГОЙ формат). Полная картина, числа заполнения
#    и грабли: Creo\STANDARDS\SKILL_material_parameters.md

# ==============================================================
# LEVEL 1: BASIC MATERIAL IDENTIFICATION
# ==============================================================

## 1.1 Key Parameters for Material Identification

### PTC_MATERIAL_ID
- **Type**: String
- **Purpose**: Short material grade designation
- **Examples**: 'St0', 'St1kp', 'AD31', 'D16', 'VCh50', '08x18h10'
- **Location**: Within PARAMETERS section of .mtl file
- **Access**: Typically Full for modifiable materials

### PTC_MATERIAL_SOURCE
- **Type**: String
- **Purpose**: Standard or material category reference
- **Examples**: 'ГОСТ 380-94', 'ГОСТ 4784-97', 'ГОСТ 859-2014', 'ASTM A36'
- **Location**: Within PARAMETERS section of .mtl file
- **Access**: Typically Full

### PTC_MATERIAL_DESCRIPTION
- **Type**: String
- **Purpose**: Full material description in Russian
- **Examples**: 
  - 'Сталь углеродистая обыкновенного качества Ст0 ГОСТ 380-94'
  - 'Чугун ВЧ50 ГОСТ 7293-85'
  - 'Алюминий АД31 ГОСТ 4784-97'
- **Location**: Within PARAMETERS section of .mtl file
- **Access**: Typically Full
# ==============================================================
# LEVEL 3: MODULE CONFIGURATION & ADVANCED SETTINGS
# ==============================================================

## 3.1 Creo Modules Structure

### MODULES Section Format
```
MODULES = {
  { Name = STATIC }
  { Name = PLASTICITY }
  { Name = FATIGUE }
  { Name = DESTRUCTION }
}
```

### Module Descriptions

#### STATIC Module
- **Purpose**: Static stress analysis
- **Key Parameters**: 
  - Equivalent stress calculation
  - Factor of Safety
  - Static failure criteria
- **When to Enable**: Standard structural analysis

#### PLASTICITY Module
- **Purpose**: Plastic deformation analysis
- **Key Parameters**:
  - Yield strength (σ_y)
  - Hardening coefficients (K, n)
  - Plastic strain calculation
- **When to Enable**: Plastic deformation expected, forming analysis

#### FATIGUE Module
- **Purpose**: Fatigue life prediction
- **Key Parameters**:
  - S-N curve selection
  - Fatigue strength (PTC_FATIGUE_STRENGTH)
  - Cyclic loading parameters
  - PTC_S_N_CURVE
- **When to Enable**: Cyclic loading, vibration, alternating stresses

#### DESTRUCTION Module
- **Purpose**: Failure and fracture analysis
- **Key Parameters**:
  - Failure criteria
  - Safety factors
  - Fracture toughness
- **When to Enable**: Brittle materials, impact loading, safety-critical parts
# ==============================================================
# LEVEL 2: PARAMETERS MASTERY
# ==============================================================

## 2.1 Mechanical Properties

### PTC_YOUNG_MODULUS (Modulus of Elasticity)
- **Type**: Real (floating point number)
- **Units**: MPa (megapascals)
- **Typical Values**: 
  - Steel: 200,000 MPa (200 GPa)
  - Aluminum: 70,000-71,000 MPa (70-71 GPa)
  - Cast Iron: 100,000-110,000 MPa
- **Location**: PARAMETERS section
- **Access**: Full (often Locked in library materials)

### PTC_POISSON_RATIO
- **Type**: Real
- **Units**: Dimensionless (ratio)
- **Typical Values**: 
  - Steel: 0.3
  - Aluminum: 0.33
  - Cast Iron: 0.22-0.25
- **Location**: PARAMETERS section
- **🔴 Правило PTC (reserved_matl_param.html)**: допустимый диапазон **−0.9999 … 0.4999**.
  Значение **0.5 НЕДОПУСТИМО** — карточка с ним не читается. Для жидкостей/газов ставить **0.499**.

### PTC_MASS_DENSITY
- **Type**: Real
- **Units**: `kg/mm^3` (живой эталон 06.11.2026; в `.mat` — `g / cm^3`)
- **Typical Values**:
  - Steel: 7.85e-06 kg/mm³ (7850 kg/m³)
  - Aluminum: 2.78e-06 kg/mm³ (2780 kg/m³)
  - Cast Iron: ~7.80e-06 kg/mm³
- **Location**: PARAMETERS section
- **Правило PTC**: только ПОЛОЖИТЕЛЬНЫЕ значения

## 2.2 Impact and Fatigue Properties

### PTC_IMPACT_ENERGY
- **Type**: Real
- **Units**: Joules (J) - Charpy impact test
- **Typical Values**:
  - Carbon steel St0: 60.0 J
  - Low-alloy steel: 40-80 J
  - Aluminum alloys: 30-60 J
  - Cast iron: 20-50 J
- **Location**: PARAMETERS section
- **Access**: Full

### PTC_FATIGUE_STRENGTH
- **Type**: Real
- **Units**: MPa at 10⁶ cycles
- **Typical Values**:
  - Carbon steel: 200.0 MPa
  - Aluminum alloys: 100-180 MPa
  - Cast iron: 100-150 MPa
- **Location**: PARAMETERS section
- **Access**: Full

### PTC_S_N_CURVE
- **Type**: String
- **Units**: Curve identifier
- **Typical Values**:
  - 'unknown:2331' - Default Creo S-N curve
  - Custom curves: 'steel:250:1e6' or 'aluminum:150:1e6'
- **Location**: PARAMETERS section
- **Access**: Full

## 2.3 Thermal Properties

### PTC_THERMAL_EXPANSION_COEF
- **Type**: Real
- **Units**: 1/K (per Kelvin) or 1/°C
- **Typical Values**:
  - Steel: 1.18e-05 1/°C
  - Aluminum: 2.34e-05 1/°C
  - Cast Iron: ~1.2e-05 1/°C
- **Location**: PARAMETERS section

### PTC_THERMAL_CONDUCTIVITY
- **Type**: Real
- **Units**: W/(m·K) or N/(sec·°C)
- **Typical Values**:
  - Steel: 88.0 W/(m·K)
  - Aluminum: 188.0 W/(m·K)
  - Cast Iron: ~50.0 W/(m·K)
- **Location**: PARAMETERS section

### PTC_SPECIFIC_HEAT
- **Type**: Real
- **Units**: J/(kg·K) or mm²/(sec²·°C)
- **Typical Values**:
  - Steel: 462 J/(kg·K)
  - Aluminum: 900 J/(kg·K)
- **Location**: PARAMETERS section
# ==============================================================
# QUICK REFERENCE CARD (PRINTABLE)
# ==============================================================

## Key Parameters at a Glance

| Parameter | Type | Default Example | Units |
|-----------|------|-----------------|-------|
| PTC_MATERIAL_ID | String | 'St0' | - |
| PTC_MATERIAL_SOURCE | String | 'ГОСТ 380-94' | - |
| PTC_YOUNG_MODULUS | Real | 200000 | MPa |
| PTC_POISSON_RATIO | Real | 0.3 | - |
| PTC_MASS_DENSITY | Real | 7.82e-09 | tonne/mm³ |
| PTC_IMPACT_ENERGY | Real | 60.0 | J |
| PTC_FATIGUE_STRENGTH | Real | 200.0 | MPa @10⁶ циклов |
| PTC_S_N_CURVE | String | 'unknown:2331' | - |

## Module Quick Guide

| Module | Enable For | Key Parameters |
|--------|-----------|----------------|
| STATIC | Standard analysis | Equivalent stress |
| PLASTICITY | Forming, plastic deformation | Yield strength, hardening |
| FATIGUE | Cyclic loading | S-N curve, fatigue strength |
| DESTRUCTION | Safety-critical, brittle | Failure criteria |

---

*Document generated: Based on Creo 12.4.2.0 .mtl file structure*
*Last updated: Following completion of 37 .mtl file updates*
*Repository: D:\AI\repo\Creo*