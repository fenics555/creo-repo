---
name: spring-tension-master
system: Creo
description: ЭТАЛОН: Пружина растяжения (Tension Spring). ГОСТ 13766.
when: пружина растяжения, крючки, начальное натяжение, tension
priority: critical
---

# ЭТАЛОН: ПРУЖИНА РАСТЯЖЕНИЯ (TENSION SPRING)

## 0. КОНСТАНТЫ (CONST_)
/* G и τ — из канон-таблицы Инженерные/SKILL_materials_reference */
IF INPUT_MATERIAL == "AISI_302"
CONST_G_MODULUS = 68000
CONST_TAU_ALLOW = 650
ELSE
CONST_G_MODULUS = 78500   /* Сталь 70, 65Г, 60С2А по справочнику */
CONST_TAU_ALLOW = 800
ENDIF
CONST_SAFETY_STAT = 1.25      /* Коэф. запаса статический */
CONST_SAFETY_DYN = 1.50       /* Коэф. запаса динамический */
CONST_HOOK_TYPE = "A"         /* Тип крючков по ГОСТ 13766 (A - стандартные) */
CONST_PI = 3.14159265

/* Пределы индекса навивки C */
CONST_C_MIN = 4.0
CONST_C_MAX = 12.0

/* Коэффициент начального натяжения (для пружин с натягом) */
CONST_F0_FACTOR = 0.25        /* F0 = (0.2...0.3) * F2 */

## 1. ВХОДНЫЕ ПАРАМЕТРЫ (INPUT_)
/* Задаются пользователем или из эскиза */
INPUT_D_OUT = 20.0            /* Наружный диаметр пружины, мм */
INPUT_D_WIRE = 2.0            /* Диаметр проволоки, мм */
INPUT_L_FREE = 100.0          /* Длина свободная (между крючками), мм */
INPUT_L_WORK = 150.0          /* Длина рабочая (максимальная), мм */
INPUT_L_PRELOAD = 110.0       /* Длина предварительного натяга, мм */

/* Материал (справочно) */
INPUT_MATERIAL = "STEEL_9389" 

## 2. ГЕОМЕТРИЯ (GEOMETRY_)
/* Расчет средних диаметров */
GEOMETRY_D_MEAN = INPUT_D_OUT - INPUT_D_WIRE
GEOMETRY_D_IN = GEOMETRY_D_MEAN - INPUT_D_WIRE

/* Индекс навивки */
GEOMETRY_INDEX_C = GEOMETRY_D_MEAN / INPUT_D_WIRE

/* Проверка индекса */
GEOMETRY_ERR_C = (GEOMETRY_INDEX_C < CONST_C_MIN) | (GEOMETRY_INDEX_C > CONST_C_MAX)

/* Рабочий ход */
GEOMETRY_H_WORK = INPUT_L_WORK - INPUT_L_PRELOAD

/* Длина крючков (упрощенно для типа А: ~2 * D_mean) */
GEOMETRY_L_HOOKS = 2 * GEOMETRY_D_MEAN

/* Число рабочих витков (из геометрии) */
/* L_free = n * d + L_hooks => n = (L_free - L_hooks) / d */
GEOMETRY_N_WORK = (INPUT_L_FREE - GEOMETRY_L_HOOKS) / INPUT_D_WIRE
GEOMETRY_N_TOTAL = GEOMETRY_N_WORK + 2  /* +2 на крючки условно */

## 3. РАСЧЕТ СИЛ И НАПРЯЖЕНИЙ (LOAD_)
/* Жесткость пружины */
/* G * d^4 / (8 * D^3 * n) */
LOAD_STIFFNESS = (CONST_G_MODULUS * INPUT_D_WIRE^4) / (8 * GEOMETRY_D_MEAN^3 * GEOMETRY_N_WORK)

/* Силы */
LOAD_F_WORK = LOAD_STIFFNESS * GEOMETRY_H_WORK
LOAD_F_PRELOAD = LOAD_STIFFNESS * (INPUT_L_PRELOAD - INPUT_L_FREE) /* Может быть отрицательной, если нет натяга */

/* Начальное натяжение F0 (если пружина с натягом) */
/* Для пружин с натягом F_preload должно быть > 0 */
LOAD_F0_CALC = LOAD_F_PRELOAD 

/* Коэффициент Wahl (для касательных напряжений) */
/* K = (4C - 1)/(4C - 4) + 0.615/C */
LOAD_K_WAHL = ((4 * GEOMETRY_INDEX_C) - 1) / ((4 * GEOMETRY_INDEX_C) - 4) + (0.615 / GEOMETRY_INDEX_C)

/* Напряжение при рабочей нагрузке */
/* Tau = K * 8 * F * D / (PI * d^3) */
LOAD_TAU_WORK = (LOAD_K_WAHL * 8 * LOAD_F_WORK * GEOMETRY_D_MEAN) / (CONST_PI * INPUT_D_WIRE^3)

/* Напряжение при предварительном натяге */
LOAD_TAU_PRELOAD = (LOAD_K_WAHL * 8 * LOAD_F_PRELOAD * GEOMETRY_D_MEAN) / (CONST_PI * INPUT_D_WIRE^3)

/* Допускаемое напряжение (условно для Сталь 9389, d < 3мм -> 800 МПа) */
/* TODO: Сделать таблицу материалов */
LOAD_TAU_ALLOW = CONST_TAU_ALLOW 

/* Проверка прочности */
LOAD_ERR_STRENGTH = LOAD_TAU_WORK > (LOAD_TAU_ALLOW / CONST_SAFETY_STAT)

## 4. КРЮЧКИ (HOOK_)
/* Напряжения в крючках (изгиб и кручение) */
/* Для крючков типа А радиус изгиба R1 = D_mean / 2 */
HOOK_R_BEND = GEOMETRY_D_MEAN / 2

/* Коэф. концентрации напряжений в крючке A1 = (4*C1^2 - C1 - 1) / (4*C1*(C1-1)) */
/* C1 = 2*R1 / d */
HOOK_C1 = (2 * HOOK_R_BEND) / INPUT_D_WIRE
HOOK_K_A1 = (4 * HOOK_C1^2 - HOOK_C1 - 1) / (4 * HOOK_C1 * (HOOK_C1 - 1))

/* Напряжение изгиба в крючке */
/* Sigma = K * 32 * F * R / (PI * d^3) */
HOOK_SIGMA_BEND = (HOOK_K_A1 * 32 * LOAD_F_WORK * HOOK_R_BEND) / (CONST_PI * INPUT_D_WIRE^3)

/* Допускаемое напряжение изгиба (обычно меньше, чем на кручение) */
HOOK_SIGMA_ALLOW = 600 

HOOK_ERR_BEND = HOOK_SIGMA_BEND > HOOK_SIGMA_ALLOW

## 5. ВЫХОДНЫЕ ПАРАМЕТРЫ (OUTPUT_ / d#)
/* Связь с геометрией Creo */
/* Предполагается, что d44 - шаг, d47 - диаметр проволоки и т.д. */
/* Эти имена должны соответствовать реальной модели! */

d47 = INPUT_D_WIRE
d42 = INPUT_D_OUT
d75 = INPUT_L_FREE

/* Расчетные параметры для анализа */
P_CALC_STIFFNESS = LOAD_STIFFNESS
P_CALC_F_WORK = LOAD_F_WORK
P_CALC_TAU = LOAD_TAU_WORK
P_CALC_N_WORK = GEOMETRY_N_WORK

/* Вердикты */
IF GEOMETRY_ERR_C == 1
  P_VERDICT_TEXT = "ОШИБКА: Индекс навивки вне диапазона 4..12"
ELSE
  IF LOAD_ERR_STRENGTH == 1
    P_VERDICT_TEXT = "ОШИБКА: Превышено напряжение среза"
  ELSE
    IF HOOK_ERR_BEND == 1
      P_VERDICT_TEXT = "ОШИБКА: Превышено напряжение в крючке"
    ELSE
      P_VERDICT_TEXT = "ОК: Пружина проходит проверку"
    ENDIF
  ENDIF
ENDIF

/* Отладочный вывод */
REL_MODEL_NAME = "SPRING_TENSION_CALC"