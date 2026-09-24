# Relations Card: liteika_hts_mm
Date: 2026-09-16 08:21
Source: CREOSON
Executor: Cline
Note: карточка ноги 1 выдумана, пересобрана из сырого близнеца спекой 50

--- RELATIONS ---
Обозначение=rel_model_name 

Объем_формовочной_смеси=0

/* ================================================================= */
/* РАСЧЕТ ЛИТЬЯ В ХТС                                                */
/* ================================================================= */

/* ================================================================= */
/* БЛОК 1. ВХОДНЫЕ ПАРАМЕТРЫ ТЕХНОЛОГА И ЦЕХА (ВВОДИТЬ СТРОГО ЗДЕСЬ!) */
/* ================================================================= */

/* --- 1.1. Выбор материала отливки -------------------------------- */
/* 1-ВЧ50, 2-СЧ25, 3-Алюминий, 4-Сталь40ХЛ, 5-БрАЖ9-4, 6-БрКМц3-1,   */
/* 7-БрА10Ж4Н4L                                                      */
ID_SPLAVA = 1

/* --- 1.2. Массовые и количественные параметры формовки ----------- */
MASSA_OTLIVKI    = 20.0   /* Чистая масса одной детали из чертежа, кг */
KOL_VO_OTLIVOK   = 1      /* Общее количество деталей во всей форме, шт */
KOL_VO_SHL       = 1      /* Количество независимых шлакоуловителей от стояка, шт */
KOL_VO_PITATELEY = 1      /* Количество впускных питателей на ОДНУ деталь, шт */

/* --- 1.3. Геометрия отливки и ХТС-формы (в ММ с экрана Creo!) --- */
DELTA_MM = 25.0   /* Преобладающая толщина стенки детали, мм */
H0_MM    = 120.0  /* Высота стояка от чаши до оси питателей, мм */
C_MM     = 224.0  /* Полная вертикальная высота отливки, мм */
P_MM     = 50.0   /* Расстояние от оси питателей до самого верха отливки, мм */

/* --- 1.4. Конструктивные скругления углов трапеций ЛПС ------------- */
R_SHL_MM = 5.0    /* Радиус upper углов шлакоуловителя, мм */
R_PIT_MM = 3.0    /* Радиус upper углов питателя, мм */

/* --- 1.5. Геометрия питаемых тепловых узлов для прибылей --------- */

/* ТУМБЛЕР КООРДИНАЦИИ И МАТРИЦЫ 4-Х СХЕМ РАБОТЫ ПРИБЫЛЕЙ КУСТА:    */
/* 1 - Автономная (верх и бок кормят свои узлы раздельно на 100%)    */
/* 2 - Совместная дополняющая (делят объем усадки пополам, 50/50)    */
/* 3 - Только боковые стаканы (верх убран, бок кормит 100% заготовки)*/
/* 4 - Только верхний купол  (бок убран, верх кормит 100% заготовки)*/
SXEMA_PITANIYA = 3

/* РАЗДЕЛ А: Параметры верхнего теплового узла заготовки ----------- */
PARAM_FORM_UP   = 2          /* Геометрия верха отливки: 1-стенка, 2-ступица/фланец */
H_UZLA_UP_MM    = 40.         /* Вертикальная высота ступицы по чертежу детали, мм   */
W_UZLA_UP_MM    = 120.      /* Наружный диаметр (ширина) верхнего узла детали, мм  */
KOL_PRIB_UP_TOT = 1            /* Назначаемое общее количество верхних прибылей, шт.  */

/* РАЗДЕЛ Б: Параметры боковых тепловых узлов заготовки ------------ */
PARAM_FORM_LAT  = 2          /* Геометрия бока отливки: 1-стенка, 2-круглый обод   */
H_UZLA_LAT_MM   = 40.      /* Вертикальная высота боковой стенки по чертежу, мм   */
W_UZLA_LAT_MM   = 120.   /* Ширина или диаметр бокового узла по чертежу, мм     */
KOL_PRIB_LAT_TOT = 1          /* Назначаемое общее количество боковых прибылей, шт.  */

/* --- 1.6. Параметры и константы внешних холодильников ХТС ----- */

/* ТУМБЛЕР МАТЕРИАЛА ХОЛОДИЛЬНИКА (Определяет теплоотвод и плотность): */
/* 1 - Консервативная сталь / чугун (Самый массовый цеховой вариант)   */
/* 2 - Медь (Король теплоотвода, экстремально быстрое охлаждение)     */
/* 3 - Литейный графит (Чистая поверхность, многократное применение)  */
MAT_CHILLER = 1

/* КОЭФФИЦИЕНТ ТОЛЩИНЫ ПЛИТЫ ХОЛОДИЛЬНИКА (От толщины стенки узла):  */
/* Задается в диапазоне 0.5 - 1.0. Меньше 0.5 - плита захлебнется.    */
/* Больше 1.0 - риск отбела чугуна ВЧ50 (появление хрупкого цементита) */
K_CHILL_THICK = 0.8

/* ТУМБЛЕР КAЛЬКУЛЯЦИИ И УЧЕТА ЗAТРАТ ОCHАСТКИ В СEБЕСТОИМОСТИ:     */
/* 0 - Оснастка многоразовая (Геометрия в Note считается НАПЕРЕД,    */
/*     но в Блок 13 себестоимости НЕ входит - цеховой стандарт)     */
/* 1 - Оснастка разовая/вваpная (Стоимость металла плиты полностью   */
/*     списывается на себестоимость одной текущей заготовки)        */
CHILLER_TO_ECO = 0

/* ТЕПЛОФИЗИЧЕСКИЕ КОНСТАНТЫ МАТЕРИАЛОВ (Плотность, кг/м3) ---------- */
DENSITY_STEEL   = 7850.0  /* Плотность углеродистой стали / чугуна   */
DENSITY_COPPER  = 8960.0  /* Плотность чистой меди                   */
DENSITY_GRAPHITE = 1750.0 /* Плотность прессованного графита         */

/* КОЭФФИЦИЕНТЫ ИНТЕНСИВНОСТИ ОТВОДА ТЕПЛА (Эффект падения модуля) - */
/* Показывают, какую долю от исходного модуля Чворинова сохраняет    */
/* узел отливки под воздействием плиты (чем меньше коэфф., тем лучше)*/
K_EFF_STEEL    = 0.75     /* Сталь снижает модуль узла на 25%        */
K_EFF_COPPER   = 0.60     /* Медь снижает модуль узла на 40%         */
K_EFF_GRAPHITE = 0.70     /* Графит снижает модуль узла на 30%       */


/* --- 1.7. Расценки плавильного участка и шихты ------------------- */
COST_METALL_RAW  = 45.0   /* Стоимость 1 кг исходной металлической шихты, руб/кг */
COST_MELTING_KWH = 7.5    /* Тариф на электроэнергию для индукционных печей, руб/кВт*ч */
POWER_FURNACE_KW = 800.0  /* Установленная мощность плавильной индукционной печи, кВт */
TONS_PER_HOUR    = 1.2    /* Фактическая производительность печи, тонн жидкого сплава в час */

/* --- 1.8. Расценки формовочного участка ХТС ---------------------- */
COST_SAND_TONS   = 3500.0 /* Стоимость 1 тонны свежего кварцевого песка, руб/т */
COST_RESIN_KG    = 280.0  /* Стоимость 1 кг связующей фурановой/фенольной смолы ХТС, руб/кг */
RESIN_PERCENT    = 1.2    /* Процентное содержание смолы в готовой песчаной смеси, % */

/* --- 1.9. Прямые трудозатраты и сдельщина рабочих ----------------- */
WAGE_M_WORKER    = 95000.0 /* Средняя базовая зарплата литейщика/термиста в месяц, руб */
WORK_HOURS_M     = 168.0   /* Количество рабочих часов в месяце, ч */
TIME_FORMING_MIN = 25.0    /* Норма времени на формовку и сборку одного куста, минут */
TIME_CLEAN_MIN   = 15.0    /* Норма времени на обрубку и зачистку одного куста, минут */

/* --- 1.10. Расценки и параметры термического участка ------------- */
COST_HEAT_KWH    = 7.5    /* Тариф на электроэнергию для термических печей отжига, руб/кВт*ч */
POWER_HEAT_KW    = 250.0  /* Мощность камерной электропечи ТО, кВт */
HEAT_BATCH_KG    = 3000.0 /* Масса полной разовой загрузки печи (садки), кг */

/* --- 1.11. Расценки и параметры дробеструйной очистки ----------- */
TIME_SHOT_BLAST_MIN = 12.0  /* Норма времени очистки одного куста в камере, минут */
COST_SHOT_KG        = 85.0  /* Стоимость 1 кг технической стальной/чугунной дроби, руб/кг */
POWER_SHOT_KW       = 45.0  /* Суммарная мощность электродвигателей дробеметной камеры, кВт */
SHOT_CONSUME_KG_H   = 4.5   /* Фактический износ (вынос) дроби на 1 час работы камеры, кг/ч */

/* ================================================================= */
/* БЛОК 2. АВТОМАТИЧЕСКИЙ ПАСПОРТ СПЛАВОВ И МЕТАЛЛУРГИЧЕСКИХ КОЭФФ.  */
/* ================================================================= */

/* --- 2.1. Страховка от ввода несуществующего ID сплава ----------- */
IF ID_SPLAVA != 1 & ID_SPLAVA != 2 & ID_SPLAVA != 3 & ID_SPLAVA != 4 & ID_SPLAVA != 5 & ID_SPLAVA != 6 & ID_SPLAVA != 7
    ID_SPLAVA = 1
ENDIF


/* --- 2.2. Назначение констант, усадки, ТО и ТВОИХ пропорций ЛПС -- */

IF ID_SPLAVA == 1
    /* ВЫСОКОПРОЧНЫЙ ЧУГУН ВЧ50. Канон Дитерта. Узкое горло - СТОЯК (1.0) */
    NAME_SPLAVA      = "ВЧ50 (Высокопрочный чугун)"
    PM               = 6900.0     /* Плотность жидкой фазы, кг/м3    */
    K_USADKI         = 0.010      /* Линейная технологическая усадка*/
    V_USADKI_LIQ     = 0.050      /* Дефицит объемной усадки (5.0%)  */
    K_LPS            = 0.35       /* Предварительная масса ЛПС (35%) */
    COEF_A           = 2.0        /* Коэффициент ТАУ по Дубицкому   */
    MR               = 0.42       /* Коэффициент расхода в песке ХТС */
    K_VOL_PRIB       = 2.0      /* Коэффициент избытка объема приб. */
    
    /* ИСПРАВЛЕНИЕ АУДИТА: Возврат секундного коэффициента Чворинова (с/мм2) */
    K_CHVORINOV      = 0.640      
    
    /* ИСПРАВЛЕНИЕ АУДИТА: Границы скоростей подъема и диаметр шлака по Стоксу */
    V_LIFT_MIN       = 12.0
    V_LIFT_MAX       = 35.0
    D_SH_MM          = 2.0

    /* ТВОЯ КАНOНИЧЕСКАЯ ПРОПОРЦИЯ: Стояк заперт, каналы расширяются */
    K_ST             = 1.00       /* Стояк - самое узкое место!      */
    K_SHL            = 1.25       
    K_PIT            = 1.50       
    K_THERM_PIT      = 6.0        /* Коэфф. тепловой протяженности ножа */
    K_CENTRIF_P      = 1.8        /* Оптимальный вихрь под магниевый шлак*/

    /* РЕЖИМ ТО ПО НАУЧНЫМ ДАННЫМ АЛТГТУ ДЛЯ ВЧ В ХТС-ФОРМАХ */
    NAME_TO          = "Высокий графитизирующий отжиг для устранения цементита (700C)"
    K_HEAT           = 0.25       
    K_HOLD           = 1.2        
    K_COOL           = 7.0        
ENDIF

IF ID_SPLAVA == 2
    /* СЕРЫЙ ЧУГУН СЧ25. Канон учебника Титова. Узкое горло - ПИТАТЕЛИ (1.0) */
    NAME_SPLAVA      = "СЧ25 (Серый чугун)"
    PM               = 6800.0     
    K_USADKI         = 0.008      
    V_USADKI_LIQ     = 0.020      
    K_LPS            = 0.25       
    COEF_A           = 2.0        
    MR               = 0.48       
    K_VOL_PRIB       = 1.20       
    K_CHVORINOV      = 0.600      
    
    V_LIFT_MIN       = 10.0
    V_LIFT_MAX       = 30.0
    D_SH_MM          = 2.0

    /* ТВОЯ КАНОНИЧЕСКАЯ ПРОПОРЦИЯ: Питатели зажаты, расширение вверх */
    K_ST             = 1.20       
    K_SHL            = 1.15       
    K_PIT            = 1.00       /* Питатели - самое узкое место!   */
    K_THERM_PIT      = 8.0        /* Серый чугун течет дальше всех   */
    K_CENTRIF_P      = 1.6        

    /* РЕЖИМ ТО ДЛЯ СЕРЫХ ЧУГУНОВ КЛАССА СЧ25 */
    NAME_TO          = "Низкотемпературный отжиг для снятия литейных напряжений (550C)"
    K_HEAT           = 0.30       
    K_HOLD           = 1.0        
    K_COOL           = 5.5        
ENDIF

IF ID_SPLAVA == 3
    /* АЛЮМИНИЕВЫЙ СПЛАВ АК7ч. Сверхрасширенная ЛПС. СТОЯК заперт (1.0) */
    NAME_SPLAVA      = "АК7ч (Алюминиевый сплав Silumin)"
    PM               = 2400.0     
    K_USADKI         = 0.0125     
    V_USADKI_LIQ     = 0.065      
    K_LPS            = 0.30       
    COEF_A           = 1.8        
    MR               = 0.32       
    K_VOL_PRIB       = 1.80       
    K_CHVORINOV      = 0.350      
    
    V_LIFT_MIN       = 15.0
    V_LIFT_MAX       = 45.0
    D_SH_MM          = 1.5

    /* ТВОЯ КАНОНИЧЕСКАЯ ПРОПОРЦИЯ под легкий сплав */
    K_ST             = 1.00       
    K_SHL            = 2.00       
    K_PIT            = 4.00       
    K_THERM_PIT      = 5.0        
    K_CENTRIF_P      = 2.2        

    /* КЛАССИЧЕСКИЙ РЕЖИМ ТО Т6 ДЛЯ АЛЮМИНИЕВЫХ СПЛАВОВ АК7ч */
    NAME_TO          = "Закалка (535C, вода) + Искусственное старение Т6 (175C)"
    K_HEAT           = 0.40       
    K_HOLD           = 2.0        
    K_COOL           = 3.0        
ENDIF

IF ID_SPLAVA == 4
    /* ЛИТЕЙНАЯ СТАЛЬ 40ХЛ. Сбалансированный транзитного стыка 1:1:1     */
    NAME_SPLAVA      = "Сталь 40ХЛ (Легированная сталь)"
    PM               = 7200.0     
    K_USADKI         = 0.020      
    V_USADKI_LIQ     = 0.070      
    K_LPS            = 0.40       
    COEF_A           = 1.5        
     MR               = 0.38  
    K_VOL_PRIB       = 2.00       
    K_CHVORINOV      = 0.880      
    
    V_LIFT_MIN       = 15.0
    V_LIFT_MAX       = 40.0
    D_SH_MM          = 2.5

    /* ТВОЯ КАНОНИЧЕСКАЯ ПРОПОРЦИЯ под сталь */
    K_ST             = 1.00       
    K_SHL            = 1.00       
    K_PIT            = 1.00       
    K_THERM_PIT      = 4.0        
    K_CENTRIF_P      = 1.4        

    /* ЦЕХОВОЙ РЕЖИМ ТЕРМООБРАБОТКИ ДЛЯ ЛИТЕЙНОЙ СТАЛИ 40ХЛ */
    NAME_TO          = "Полная нормализация для измельчения зерна (860C) + Отпуск"
    K_HEAT           = 0.20       
    K_HOLD           = 1.5        
    K_COOL           = 8.0        
ENDIF

IF ID_SPLAVA == 5
    /* МЕДНЫЕ СПЛАВЫ И БРОНЗЫ (Специфика под БрА10Ж4Н4Л)                 */
    NAME_SPLAVA      = "БрА10Ж4Н4Л (Алюминиевая бронза)"
    PM               = 7500.0     
    K_USADKI         = 0.015      
    V_USADKI_LIQ     = 0.055      
    K_LPS            = 0.35       
    COEF_A           = 2.5        
    MR               = 0.35       
    K_VOL_PRIB       = 1.60       
    K_CHVORINOV      = 0.760      
    
    V_LIFT_MIN       = 12.0
    V_LIFT_MAX       = 35.0
    D_SH_MM          = 2.0

    /* ТВОЯ КАНOНИЧЕСКАЯ ПРОПОРЦИЯ ГИДРАВЛИКИ */
    K_ST             = 1.00       
    K_SHL            = 1.20       
    K_PIT            = 1.30       
    K_THERM_PIT      = 6.0        
    K_CENTRIF_P      = 1.8        

    /* НАУЧНО ОБОСНОВАННЫЕ ПАРАМЕТРЫ ПРОГРАММЫ ТО ДЛЯ БрА10Ж4Н4Л */
    NAME_TO          = "Термическое улучшение (Закалка 980C + Высокий отпуск 650C)"
    K_HEAT           = 0.30       
    K_HOLD           = 1.5        
    K_COOL           = 6.0        
ENDIF

IF ID_SPLAVA == 6
    /* ЖAРОПРОЧНЫЕ СТAЛИ И НИКEЛЕВЫЕ СПЛAВЫ (Например, 12Х18Н9ТЛ)       */
    NAME_SPLAVA      = "12Х18Н9ТЛ (Аустенитная нержавеющая сталь)"
    PM               = 7000.0     
    K_USADKI         = 0.022      
    V_USADKI_LIQ     = 0.075      
    K_LPS            = 0.45       
    COEF_A           = 1.4        
    MR               = 0.33       
    K_VOL_PRIB       = 2.20       
    K_CHVORINOV      = 0.920      
    
    V_LIFT_MIN       = 15.0
    V_LIFT_MAX       = 40.0
    D_SH_MM          = 2.5

    /* ТВОЯ КАНОНИЧЕСКАЯ ПРОПОРЦИЯ: Дроссельная запертая под нержавейку */
    K_ST             = 1.00       
    K_SHL            = 1.30       
    K_PIT            = 1.60       
    K_THERM_PIT      = 4.5        
    K_CENTRIF_P      = 1.5        

    /* ВЫСОКОТЕМПЕРАТУРНАЯ АУСТЕНИТИЗАЦИЯ НЕРЖАВЕЙКИ */
    NAME_TO          = "Аустенитизация (Закалка 1050C в воду для растворения карбидов)"
    K_HEAT           = 0.15       
    K_HOLD           = 1.8        
    K_COOL           = 2.5        
ENDIF

IF ID_SPLAVA >= 7
    /* СПEЦИAЛЬНЫЕ СПЛAВЫ И МОДИФИЦИРОВAННЫЕ СПЛAВЫ (Например, ЧХ16)     */
    NAME_SPLAVA      = "ЧХ16 (Износостойкий хромистый чугун)"
    PM               = 7100.0     
    K_USADKI         = 0.018      
    V_USADKI_LIQ     = 0.060      
    K_LPS            = 0.38       
    COEF_A           = 2.2        
    MR               = 0.40       
    K_VOL_PRIB       = 1.70       
    K_CHVORINOV      = 0.720      
    
    V_LIFT_MIN       = 12.0
    V_LIFT_MAX       = 35.0
    D_SH_MM          = 2.0

    /* ТВОЯ КАНОНИЧЕСКАЯ ПРОПОРЦИЯ: Запертая по Гиршовичу под спецчугун */
    K_ST             = 1.00       
    K_SHL            = 1.25       
    K_PIT            = 1.40       
    K_THERM_PIT      = 5.5        
    K_CENTRIF_P      = 1.9        

    /* СЛОЖНЫЙ ЦИКЛ ТО ДЛЯ ВЫСОКОХРОМИСТЫХ ИЗНОСОСТОЙКИХ ЧУГУНОВ */
    NAME_TO          = "Дестабилизация аустенита (950C) + Воздушное охлаждение"
    K_HEAT           = 0.20       
    K_HOLD           = 1.5        
    K_COOL           = 9.0        
ENDIF


/* ================================================================= */
/* БЛОК 3. ПЕРЕВОД В СИ И ИНИЦИАЛИЗАЦИЯ ЗОМБИ-ПАРАМЕТРОВ             */
/* ================================================================= */

/* --- 3.1. Физическая константа гравитации ------------------------ */
Q_GRAV = 9.81

/* --- 3.2. Перевод входной геометрии в систему СИ (Пункт 7 аудита) -- */
DELTA_M = DELTA_MM / 1000.0
H0_M    = H0_MM / 1000.0
C_M     = C_MM / 1000.0
P_M     = P_MM / 1000.0
D_SH    = D_SH_MM / 1000.0

/* --- 3.3. Инициализация глобального HOT_FACTOR -------------------- */
HOT_FACTOR = 1.0 + K_USADKI

/* --- 3.4. ТОТАЛЬНАЯ ЗАЧИСТКА: Объявление стартовых нулей ---------- */
/* Жестко запираем в числовой тип все параметры, которые глючили,    */
/* чтобы у Creo не было ни единого шанса перевести их в ручной ввод  */
NOM_H_SHL             = 0.0
NOM_L1_SHL            = 0.0
NOM_L2_SHL            = 0.0
S_SHL_FACT            = 0.0
P_SHL_FACT            = 0.0

NOM_H_PIT_PRIB        = 0.0
NOM_L1_PIT_PRIB       = 0.0
NOM_L2_PIT_PRIB       = 0.0

NOM_H_PIT_DET         = 0.0
NOM_L1_PIT_DET        = 0.0
NOM_L2_PIT_DET        = 0.0

S_TRAP_PRIB           = 0.0
S_GEOM_PRIB_ODN       = 0.0
S_TRAP_DET            = 0.0
S_GEOM_DET_ODN        = 0.0

M_SHEIKA_REAL         = 0.0
M_SHEIKA_EFF          = 0.0
M_PRIB_MOD_REAL       = 0.0

TIME_HEAT_UP          = 0.0
TIME_HOLD             = 0.0
TIME_COOL_DOWN        = 0.0
TIME_HOLD_RAW         = 0.0
HEAT_TIME_HOURS       = 0.0

/* ================================================================= */
/* БЛОК 4. РАСЧЕТ БАЛАНСА МЕТАЛЛА И ВРЕМЕНИ ЗАЛИВКИ ТАУ ПО ДУБИЦКОМУ */
/* ================================================================= */

/* --- 4.1. Сквозной расчет масс с учетом многоместной формовки ----- */
M_TOTAL   = MASSA_OTLIVKI * KOL_VO_OTLIVOK  
G_ZH      = M_TOTAL * (1.0 + K_LPS)  

KOL_OTL_NA_SHL = ceil(KOL_VO_OTLIVOK / KOL_VO_SHL)

/* Масса жидкого металла в форме, приходящаяся на один шлакоуловитель (М_Ж) */
M_ZH_ODN_SHL = (MASSA_OTLIVKI * KOL_OTL_NA_SHL) * (1.0 + K_LPS)
M_DET_ODN = MASSA_OTLIVKI


/* --- 4.2. РАСЧЕТ ВРЕМЕНИ ТАУ ПО ДУБИЦКОМУ С ЗАЩИТОЙ СТЕПЕНИ ------- */
/* ИСПРАВЛЕНИЕ АУДИТА: Вместо дроби (1.0/3.0) вшито жесткое число 0.3333 */
/* Это страхует парсер Creo от целочисленного сброса кубического корня в ноль */

/* СХЕМА А: Заливка ЧЕРЕЗ ПРИБЫЛЬ (Расчет по полной массе М_Ж с литниками) */
IF M_ZH_ODN_SHL > 0.0
    TAU_PRIB_VAR3 = COEF_A * pow((DELTA_MM * M_ZH_ODN_SHL), 0.3333)
    TAU_PRIB      = ceil(TAU_PRIB_VAR3)
ELSE
    TAU_PRIB      = 10.0
ENDIF

/* СХЕМА Б: Заливка НАПРЯМУЮ В ДЕТАЛЬ (Расчет по чистому весу одной детали) */
IF M_DET_ODN > 0.0
    TAU_DET_VAR3  = COEF_A * pow((DELTA_MM * M_DET_ODN), 0.3333)
    TAU_DET       = ceil(TAU_DET_VAR3)
ELSE
    TAU_DET       = 10.0
ENDIF


/* ================================================================= */
/* БЛОК 5. ГИДРАВЛИЧЕСКИЙ РАСЧЕТ ПЛОЩАДЕЙ СЕЧЕНИЙ ПО ТВОЕМУ КАНOНУ   */
/* ================================================================= */

/* --- 5.1. Автоматический расчет статического напора HP (в метрах) - */
IF P_M == 0.0
    HP = H0_M
ELSE
    IF P_M == C_M
        HP = H0_M - (C_M / 2.0)
    ELSE
        HP = H0_M - ( (P_M * P_M) / (2.0 * C_M) )
    ENDIF
ENDIF

/* Цеховой гидростатический напор стояка в миллиметрах для Note */
CAD_HP_MM = ceil(HP * 1000.0)


/* --- 5.2. ЧИСТЫЙ РАСЧЕТ СКОРОСТНОГО ГОРЛА ПО БЕРНУЛЛИ ------------ */
/* Базовая формула Бернулли вычисляет абстрактное узкое место 1.0 (м^2) */
/* Расчет идет от чистой массы деталей M_TOTAL для стабилизации струи   */
S_UZK_SECH = M_TOTAL / (PM * TAU_PRIB * MR * sqrt(2.0 * Q_GRAV * HP))


/* --- 5.3. ПРЯМОЕ ПРИМЕНЕНИЕ ТВОИХ КОЭФФИЦИЕНТОВ К ЭЛЕМЕНТАМ ------- */
/* Одиночный стояк куста (умножаем на твой коэффициент K_ST) */
S_ST = (S_UZK_SECH * K_ST) / KOL_VO_SHL

/* Магистральный шлакоуловитель (умножаем на твой коэффициент K_SHL) */
S_SHL = S_UZK_SECH * K_SHL

/* Суммарная и одиночная площадь питателей в прибыль (коэффициент K_PIT) */
SUM_S_PIT_PRIB = S_UZK_SECH * K_PIT
S_PIT_ODN_PRIB = SUM_S_PIT_PRIB / KOL_VO_OTLIVOK / KOL_VO_PITATELEY


/* --- 5.4. ДУБЛИРУЮЩИЙ РАСЧЕТ ДЛЯ СХЕМЫ Б (ПОДВОД НАПРЯМУЮ В ДЕТАЛЬ) */
S_UZK_SECH_DET = M_TOTAL / (PM * TAU_DET * MR * sqrt(2.0 * Q_GRAV * HP))

S_ST_DET = (S_UZK_SECH_DET * K_ST) / KOL_VO_SHL
SUM_S_PIT_DET  = S_UZK_SECH_DET * K_PIT
S_PIT_ODN_DET  = SUM_S_PIT_DET / KOL_VO_OTLIVOK / KOL_VO_PITATELEY

/* ================================================================= */
/* БЛОК 6. ГЕОМЕТРИЧЕСКИЙ РАСЧЕТ И КОМПЕНСАЦИЯ СКРУГЛЕНИЙ КАНАЛОВ    */
/* ================================================================= */

/* --- 6.0. ИМЕНОВАННЫЕ КОНСТАНТЫ ГЕОМЕТРИИ ХТС-КАНАЛОВ ------------ */
COEF_RAD_AREA = 0.430    /* Эмпирический коэфф. вычета площади на радиус     */
COEF_RAD_PERI = 0.892    /* Эмпирический коэфф. утяжки периметра на радиус   */
SLOPE_ANG_RAD = 0.087    /* Тангенс формовочного уклона 5 градусов трапеции */

/* --- 6.1. Геометрия воронки стояка по ГОСТ/документации (мм) ----- */
/* Переводим базовую площадь узкого горла стояка из м^2 в мм^2 */
S_ST_MM2 = S_ST * 1.0e6
NOM_D_ST_NIZ_MM = sqrt(4.0 * S_ST_MM2 / PI)

/* --- 6.2. Геометрия магистрального шлакоуловителя (мм) ----------- */
/* Переводим площадь коллектора-шлакоуловителя из м^2 в мм^2 */
S_SHL_MM2 = S_SHL * 1.0e6
NOM_H_SHL = sqrt(S_SHL_MM2 / (1.0 - SLOPE_ANG_RAD))
NOM_L1_SHL = (S_SHL_MM2 / NOM_H_SHL) + (NOM_H_SHL * SLOPE_ANG_RAD)
NOM_L2_SHL = (S_SHL_MM2 / NOM_H_SHL) - (NOM_H_SHL * SLOPE_ANG_RAD)

IF NOM_L2_SHL < 4.0
    NOM_L2_SHL = 4.0
ENDIF

/* Фактическая площадь и периметр полости ХТС с вычетом скруглений углов */
S_SHL_FACT = S_SHL_MM2 - COEF_RAD_AREA * pow(R_SHL_MM, 2.0)
P_SHL_FACT = NOM_L1_SHL + NOM_L2_SHL + 2.0 * NOM_H_SHL - COEF_RAD_PERI * R_SHL_MM

/* --- 6.3. Геометрия впускных питателей (квадрат L/H=1, мм) ------- */
/* СХЕМА А: Геометрия ножей-питателей под боковую прибыль */
S_PIT_PRIB_MM2 = S_PIT_ODN_PRIB * 1.0e6
NOM_H_PIT_PRIB = sqrt(S_PIT_PRIB_MM2 / (1.0 - SLOPE_ANG_RAD))
NOM_L1_PIT_PRIB = NOM_H_PIT_PRIB + (NOM_H_PIT_PRIB * SLOPE_ANG_RAD)
NOM_L2_PIT_PRIB = NOM_H_PIT_PRIB - (NOM_H_PIT_PRIB * SLOPE_ANG_RAD)

IF NOM_L2_PIT_PRIB < 4.0
    NOM_L2_PIT_PRIB = 4.0
ENDIF

/* СХЕМА Б: Геометрия ножей-питателей напрямую во фланец детали */
S_PIT_DET_MM2 = S_PIT_ODN_DET * 1.0e6
NOM_H_PIT_DET = sqrt(S_PIT_DET_MM2 / (1.0 - SLOPE_ANG_RAD))
NOM_L1_PIT_DET = NOM_H_PIT_DET + (NOM_H_PIT_DET * SLOPE_ANG_RAD)
NOM_L2_PIT_DET = NOM_H_PIT_DET - (NOM_H_PIT_DET * SLOPE_ANG_RAD)

IF NOM_L2_PIT_DET < 4.0
    NOM_L2_PIT_DET = 4.0
ENDIF

/* --- 6.4. Усадка -> CAD-размеры (мм) ---------------------------- */
/* Исполнительный диаметр воронки стояка strictly под имя твоей Note */
CAD_D_ST_NIZ     = ceil(NOM_D_ST_NIZ_MM * HOT_FACTOR)

CAD_H_SHL        = ceil(NOM_H_SHL * HOT_FACTOR)
CAD_L1_SHL_NIZ   = ceil(NOM_L1_SHL * HOT_FACTOR)
CAD_L2_SHL_VERH  = floor(NOM_L2_SHL * HOT_FACTOR)
CAD_S_SHL        = ceil(S_SHL_FACT * pow(HOT_FACTOR, 2.0))

/* Единая увязка длины шлакоуловителя через сквозной коэффициент K_THERM_PIT */
CAD_L_SHL        = ceil((K_THERM_PIT * NOM_H_SHL) * HOT_FACTOR)

/* Финальные CAD-размеры впускных ножей всей формы */
CAD_H_PIT_PRIB       = ceil(NOM_H_PIT_PRIB * HOT_FACTOR)
CAD_L_PIT_NIZ_PRIB   = ceil(NOM_L1_PIT_PRIB * HOT_FACTOR)
CAD_L_PIT_VERH_PRIB  = floor(NOM_L2_PIT_PRIB * HOT_FACTOR)
CAD_S_PIT_SUM_PRIB   = ceil((SUM_S_PIT_PRIB * 1.0e6) * pow(HOT_FACTOR, 2.0))

CAD_H_PIT_DET        = ceil(NOM_H_PIT_DET * HOT_FACTOR)
CAD_L_PIT_NIZ_DET    = ceil(NOM_L1_PIT_DET * HOT_FACTOR)
CAD_L_PIT_VERH_DET   = floor(NOM_L2_PIT_DET * HOT_FACTOR)
CAD_S_PIT_SUM_DET    = ceil((SUM_S_PIT_DET * 1.0e6) * pow(HOT_FACTOR, 2.0))
CAD_S_PIT_ODN_DET    = ceil((S_PIT_ODN_DET * 1.0e6) * pow(HOT_FACTOR, 2.0))


/* ================================================================= */
/* БЛОК 7. ГИДРАВЛИЧЕСКИЙ КОНТРОЛЬ ПО ГЕОМЕТРИЧЕСКОМУ ФАКТУ          */
/* ================================================================= */

/* --- 7.1. Расчет площадей по РЕАЛЬНЫМ закругленным 3D-трапециям --- */
S_TRAP_PRIB = ((CAD_L_PIT_NIZ_PRIB + CAD_L_PIT_VERH_PRIB) / 2.0) * CAD_H_PIT_PRIB
S_GEOM_PRIB_ODN = S_TRAP_PRIB - (COEF_RAD_AREA * pow(R_PIT_MM, 2.0))

S_TRAP_DET  = ((CAD_L_PIT_NIZ_DET + CAD_L_PIT_VERH_DET) / 2.0) * CAD_H_PIT_DET
S_GEOM_DET_ODN  = S_TRAP_DET - (COEF_RAD_AREA * pow(R_PIT_MM, 2.0))

/* Перевод в кв. метры СТРОГО через умножение на 1е-6 во избежание сброса в ноль */
SUM_S_GEOM_PRIB_M = (S_GEOM_PRIB_ODN * KOL_VO_OTLIVOK * KOL_VO_PITATELEY) * 1.0e-6
SUM_S_GEOM_DET_M  = (S_GEOM_DET_ODN * KOL_VO_OTLIVOK * KOL_VO_PITATELEY) * 1.0e-6

/* Снайперский расчет НАСТОЯЩЕГО времени заливки по Бернулли */
INPUT_TAU_PRIB = ceil(G_ZH / (MR * PM * SUM_S_GEOM_PRIB_M * sqrt(2.0 * Q_GRAV * HP)))
INPUT_TAU_DET  = ceil(M_TOTAL / (MR * PM * SUM_S_GEOM_DET_M * sqrt(2.0 * Q_GRAV * HP)))

IF INPUT_TAU_PRIB < 1.0
    INPUT_TAU_PRIB = 1.0
ENDIF
IF INPUT_TAU_DET < 1.0
    INPUT_TAU_DET = 1.0
ENDIF

/* --- 7.2. Скорость подъема расплава в форме (мм/сек) ------------- */
V_LIFT_PRIB = C_MM / INPUT_TAU_PRIB  
V_LIFT_DET  = C_MM / INPUT_TAU_DET   

/* --- 7.3. Экспертиза чистого статуса скоростей -------------------- */
STATUS_PRIB = "NORMA"
IF V_LIFT_PRIB < V_LIFT_MIN
    STATUS_PRIB = "MEDLENNO"
ENDIF
IF V_LIFT_PRIB > V_LIFT_MAX
    STATUS_PRIB = "BYSTRO"
ENDIF

STATUS_DET = "NORMA"
IF V_LIFT_DET < V_LIFT_MIN
    STATUS_DET = "MEDLENNO"
ENDIF
IF V_LIFT_DET > V_LIFT_MAX
    STATUS_DET = "BYSTRO"
ENDIF

/* --- 7.4. КОНТРОЛЬ РАССОГЛАСОВАНИЯ ТЕОРИИ И 3D-ГИДРАВЛИКИ --------- */
/* Датчик Схемы А: разница факта и теории Дубицкого */
DELTA_TAU_PRIB = INPUT_TAU_PRIB - TAU_PRIB
DELTA_TAU_PRIB_ABS = DELTA_TAU_PRIB
IF DELTA_TAU_PRIB < 0.0
    DELTA_TAU_PRIB_ABS = -1.0 * DELTA_TAU_PRIB
ENDIF

IF DELTA_TAU_PRIB_ABS > 3.0
    FLAG_HYDRO_MISMATCH_PRIB = 1  /* Расхождение более 3 сек */
ELSE
    FLAG_HYDRO_MISMATCH_PRIB = 0
ENDIF

/* Датчик Схемы Б: разница факта и теории Дубицкого */
DELTA_TAU_DET = INPUT_TAU_DET - TAU_DET
DELTA_TAU_DET_ABS = DELTA_TAU_DET
IF DELTA_TAU_DET < 0.0
    DELTA_TAU_DET_ABS = -1.0 * DELTA_TAU_DET
ENDIF

IF DELTA_TAU_DET_ABS > 3.0
    FLAG_HYDRO_MISMATCH_DET = 1  /* Расхождение более 3 сек */
ELSE
    FLAG_HYDRO_MISMATCH_DET = 0
ENDIF

/* --- 7.5. Динамическая сборка рекомендаций с учетом К_PIT ---------- */
RECOMMEND_PRIB = "ГИДРАВЛИКА ОК: Теория Дубицкого совпадает с 3D-формой."
IF FLAG_HYDRO_MISMATCH_PRIB == 1
    RECOMMEND_PRIB = "ВНИМАНИЕ! Время заливки улетело! Скорректируйте K_PIT на панели Блока 2."
ELSE
    IF STATUS_PRIB == "MEDLENNO"
        RECOMMEND_PRIB = "РЕКОМЕНДАЦИЯ КД: Скорость мала! Увеличьте K_PIT на панели Блока 2."
    ENDIF
    IF STATUS_PRIB == "BYSTRO"
        RECOMMEND_PRIB = "РЕКОМЕНДАЦИЯ КД: Скорость высока! Зажмите K_PIT на панели Блока 2."
    ENDIF
ENDIF

RECOMMEND_DET = "ГИДРАВЛИКА ОК: Теория Дубицкого совпадает с 3D-формой."
IF FLAG_HYDRO_MISMATCH_DET == 1
    RECOMMEND_DET = "ВНИМАНИЕ! Время заливки улетело! Скорректируйте K_PIT на панели Блока 2."
ELSE
    IF STATUS_DET == "MEDLENNO"
        RECOMMEND_DET = "РЕКОМЕНДАЦИЯ КД: Скорость мала! Увеличьте K_PIT на панели Блока 2."
    ENDIF
    IF STATUS_DET == "BYSTRO"
        RECOMMEND_DET = "РЕКОМЕНДАЦИЯ КД: Скорость высока! Зажмите K_PIT на панели Блока 2."
    ENDIF
ENDIF

/* --- 7.6. Округление скоростей и перевод статусов в РУС-вывод ------ */
V_PRIB_ROUND = floor(V_LIFT_PRIB * 10.0 + 0.5) / 10.0
V_DET_ROUND  = floor(V_LIFT_DET * 10.0 + 0.5) / 10.0

RUS_PRIB = "НОРМА"
IF STATUS_PRIB == "MEDLENNO"
    RUS_PRIB = "МЕДЛЕННО"
ENDIF
IF STATUS_PRIB == "BYSTRO"
    RUS_PRIB = "КРИТИЧЕСКИ БЫСТРО"
ENDIF

RUS_DET = "НОРМА"
IF STATUS_DET == "MEDLENNO"
    RUS_DET = "МЕДЛЕННО"
ENDIF
IF STATUS_DET == "BYSTRO"
    RUS_DET = "КРИТИЧЕСКИ БЫСТРО"
ENDIF

INFO_V_PRIB = RUS_PRIB + " | V=" + rtos(V_PRIB_ROUND)
INFO_V_PRIB = INFO_V_PRIB + " (Допуск: " + rtos(V_LIFT_MIN) + "..." + rtos(V_LIFT_MAX) + " мм/с)"
INFO_V_PRIB = INFO_V_PRIB + " [Т_факт=" + rtos(INPUT_TAU_PRIB) + " сек]"

INFO_V_DET  = RUS_DET + " | V=" + rtos(V_DET_ROUND)
INFO_V_DET  = INFO_V_DET + " (Допуск: " + rtos(V_LIFT_MIN) + "..." + rtos(V_LIFT_MAX) + " мм/с)"
INFO_V_DET  = INFO_V_DET + " [Т_факт=" + rtos(INPUT_TAU_DET) + " сек]"

/* ================================================================= */
/* БЛОК 8. МЕТАЛЛУРГИЧЕСКИЙ РАСЧЕТ ВЕРХНИХ ЗАКРЫТЫХ ПРИБЫЛЕЙ          */
/* ================================================================= */

/* --- 8.1. Инициализация триггеров матрицы 4-х схем питания ------- */
K_VOL_UP   = 1.0
K_VOL_LAT  = 1.0
K_MASS_UP  = 1.0
K_MASS_LAT = 1.0

IF SXEMA_PITANIYA == 2
    /* Схема 2: Совместная (доли объемов занижены на 50%) */
    K_VOL_UP   = 0.5
    K_VOL_LAT  = 0.5
ENDIF

IF SXEMA_PITANIYA == 3
    /* Схема 3: Только бок (верх убран из экономики куста) */
    K_MASS_UP  = 0.0
ENDIF

IF SXEMA_PITANIYA == 4
    /* Схема 4: Только верх (бок убран из экономики куста) */
    K_MASS_LAT = 0.0
ENDIF

/* --- 8.2. Автоматический расчет литейного модуля верхнего узла ---- */
IF PARAM_FORM_UP == 1
    /* ВАРИАНТ 1: Узел прямоугольного сечения (плоская стенка) */
    M_OTL_UP = (H_UZLA_UP_MM * W_UZLA_UP_MM) / (2.0 * (H_UZLA_UP_MM + W_UZLA_UP_MM))
ELSE
    /* ВАРИАНТ 2: Узел круглого сечения (ступица, фланец, бобышка) */
    M_OTL_UP = (W_UZLA_UP_MM * H_UZLA_UP_MM) / (4.0 * H_UZLA_UP_MM + 2.0 * W_UZLA_UP_MM)
ENDIF

/* --- 8.3. Расчет базовой геометрии верхней купольной прибыли ----- */
/* Для надежного питания модуль прибыли: M_prib = 1.2 * M_otl */
NOM_D_PRIB_UP = 1.2 * 4.8 * M_OTL_UP
NOM_H_PRIB_UP = NOM_D_PRIB_UP * 1.2

/* --- 8.4. Контроль по дефициту объема от объемной усадки ---------- */
V_OTL_M3 = MASSA_OTLIVKI / PM
V_USADKI_MM3 = V_OTL_M3 * V_USADKI_LIQ * 1e9

/* Сколько усадочного объема обязана восполнить ОДНА верхняя прибыль */
V_NEED_ONE_PRIB_UP = (V_USADKI_MM3 * K_VOL_UP) / KOL_PRIB_UP_TOT

/* Фактический объем купольной прибыли (Цилиндр + Полусфера) */
R_PRIB_C_UP = NOM_D_PRIB_UP / 2.0
V_CYL_UP = PI * pow(R_PRIB_C_UP, 2.0) * (NOM_H_PRIB_UP - R_PRIB_C_UP)
V_SPH_UP = (2.0 / 3.0) * PI * pow(R_PRIB_C_UP, 3.0)
V_REAL_PRIB_UP = V_CYL_UP + V_SPH_UP

/* Страховочный фильтр по избытку объема из Паспорта сплавов */
IF V_REAL_PRIB_UP < (V_NEED_ONE_PRIB_UP * K_VOL_PRIB)
    /* ИСПРАВЛЕНИЕ АУДИТА: Замена дроби (1.0/3.0) на жесткое число 0.3333 */
    NOM_D_PRIB_UP = pow(((V_NEED_ONE_PRIB_UP * K_VOL_PRIB) / 0.94), 0.3333)
    NOM_H_PRIB_UP = NOM_D_PRIB_UP * 1.2
    
    /* Пересчитываем объем купола под новые координированные размеры */
    R_PRIB_C_UP = NOM_D_PRIB_UP / 2.0
    V_CYL_UP = PI * pow(R_PRIB_C_UP, 2.0) * (NOM_H_PRIB_UP - R_PRIB_C_UP)
    V_SPH_UP = (2.0 / 3.0) * PI * pow(R_PRIB_C_UP, 3.0)
    V_REAL_PRIB_UP = V_CYL_UP + V_SPH_UP
ENDIF

/* --- 8.5. Накатываем усадку HOT_FACTOR и выводим CAD-размеры ------ */
CAD_D_PRIB_UP = ceil(NOM_D_PRIB_UP * HOT_FACTOR)
CAD_H_PRIB_UP = ceil(NOM_H_PRIB_UP * HOT_FACTOR)

CAD_L_SHEIKA_PRIB_UP = 0.0
CAD_D_SHEIKA_PRIB_UP = CAD_D_PRIB_UP

CAD_M_OTL_UP = floor(M_OTL_UP * 10.0 + 0.5) / 10.0
CAD_V_PRIB_UP_CM3 = ceil(V_REAL_PRIB_UP / 1000.0)

/* Вычисляем массу ОДНОЙ чистой верхней прибыли для справочного Note */
M_ONE_PRIB_UP_KG = floor(((V_REAL_PRIB_UP * PM) / 1e9) * 10.0 + 0.5) / 10.0

/* ================================================================= */
/* БЛОК 9. ИНТЕЛЛЕКТУАЛЬНЫЙ РАСЧЕТ БОКОВЫХ ЗАКРЫТЫХ ПРИБЫЛЕЙ         */
/* ================================================================= */

/* --- 9.1. Константы конструкторского фильтра ХТС ----------------- */
K_KOTLETA      = 2.0    
K_FILTER_H     = 0.75   
K_THERMAL_BIAS_MIN = 1.10 
K_THERMAL_BIAS_MAX = 1.40 
L_ZAZOR_MIN    = 3.0    
L_ZAZOR_MAX    = 8.0    

/* --- 9.2. Литейный модуль и толщина стенки бокового узла --------- */
IF PARAM_FORM_LAT == 1
    M_OTL_LAT = (H_UZLA_LAT_MM * W_UZLA_LAT_MM) / (2.0 * (H_UZLA_LAT_MM + W_UZLA_LAT_MM))
    W_REAL_WALL_LAT = W_UZLA_LAT_MM
ELSE
    M_OTL_LAT = (W_UZLA_LAT_MM * H_UZLA_LAT_MM) / (4.0 * H_UZLA_LAT_MM + 2.0 * W_UZLA_LAT_MM)
    W_REAL_WALL_LAT = 2.0 * M_OTL_LAT
ENDIF

/* --- 9.3. Время затвердевания отливки по Чворинову (сек) -------- */
TIME_ZAT_DET_LAT = ceil(K_CHVORINOV * pow(M_OTL_LAT, 2.0))

/* --- 9.4. Объёмный дефицит на одну боковую прибыль (мм^3) -------- */
V_OTL_LAT_M3 = MASSA_OTLIVKI / PM
V_USADKI_LAT_MM3 = V_OTL_LAT_M3 * V_USADKI_LIQ * 1e9

V_NEED_ONE_PRIB_LAT = (V_USADKI_LAT_MM3 * K_VOL_LAT) / KOL_PRIB_LAT_TOT
V_PRIB_REQUIRED = V_NEED_ONE_PRIB_LAT * K_VOL_PRIB

/* --- 9.5. Базовый диаметр прибыли по теплофизике (мм) ------------ */
NOM_D_PRIB_LAT = 5.5 * M_OTL_LAT
NOM_H_PRIB_LAT = NOM_D_PRIB_LAT * 1.5

/* Проверка по избытку объёма металла по Василевскому */
R_PRIB_C_LAT = NOM_D_PRIB_LAT / 2.0
V_REAL_PRIB_LAT = PI * pow(R_PRIB_C_LAT, 2.0) * NOM_H_PRIB_LAT

IF V_REAL_PRIB_LAT < V_PRIB_REQUIRED
    /* ИСПРАВЛЕНИЕ АУДИТА: Замена дроби (1.0/3.0) на жесткое число 0.3333 */
    NOM_D_PRIB_LAT = pow((V_PRIB_REQUIRED / 1.178), 0.3333)
    NOM_H_PRIB_LAT = NOM_D_PRIB_LAT * 1.5
    V_REAL_PRIB_LAT = V_PRIB_REQUIRED
ENDIF

/* --- 9.6. ТЕОРЕТИЧЕСКИ НЕОБХОДИМАЯ ПЛОЩАДЬ ШЕЙКИ (мм^2) --------- */
H_NAP_SHEIKA_M = (NOM_H_PRIB_LAT / 1000.0) / 3.0
V_FLOW_SHEIKA = sqrt(2.0 * Q_GRAV * H_NAP_SHEIKA_M) * 0.25
DV_DT_LAT = (V_OTL_LAT_M3 * V_USADKI_LIQ / KOL_PRIB_LAT_TOT) / TIME_ZAT_DET_LAT
S_SHEIKA_MIN_MM2 = (DV_DT_LAT / V_FLOW_SHEIKA) * 1e6 * 1.5

/* --- 9.7. ПОШАГОВЫЙ МОДУЛЬ ПРОЕКТИРОВАНИЯ И ПОДГОНКИ ШЕЙКИ ------ */
H_SHEIKA_MAX = H_UZLA_LAT_MM * K_FILTER_H
IF H_SHEIKA_MAX > 42.0
    H_SHEIKA_MAX = 42.0
ENDIF

L_SHEIKA_MAX = H_SHEIKA_MAX * K_KOTLETA
W_FLANGE_LIMIT = W_UZLA_LAT_MM * 0.80
IF L_SHEIKA_MAX > W_FLANGE_LIMIT
    L_SHEIKA_MAX = W_FLANGE_LIMIT
ENDIF

NOM_H_SHEIKA_LAT = 2.2 * M_OTL_LAT
IF NOM_H_SHEIKA_LAT > H_SHEIKA_MAX
    NOM_H_SHEIKA_LAT = H_SHEIKA_MAX
ENDIF
IF NOM_H_SHEIKA_LAT < 8.0
    NOM_H_SHEIKA_LAT = 8.0
ENDIF

D_SHEIKA_MID = 0.8 * NOM_D_PRIB_LAT
IF D_SHEIKA_MID > L_SHEIKA_MAX
    D_SHEIKA_MID = L_SHEIKA_MAX
ENDIF

NOM_L1_SHEIKA = D_SHEIKA_MID + 3.0
NOM_L2_SHEIKA = D_SHEIKA_MID - 3.0
IF NOM_L2_SHEIKA < 4.0
    NOM_L2_SHEIKA = 4.0
ENDIF

S_SHEIKA_TRAP_NOM = ((NOM_L1_SHEIKA + NOM_L2_SHEIKA) / 2.0) * NOM_H_SHEIKA_LAT

FLAG_SHEIKA_DEFICIT = 0
IF S_SHEIKA_TRAP_NOM < S_SHEIKA_MIN_MM2
    FLAG_SHEIKA_DEFICIT = 1
ENDIF

IF FLAG_SHEIKA_DEFICIT == 1
    L_NEED = (S_SHEIKA_MIN_MM2 / NOM_H_SHEIKA_LAT) * 1.05
    IF L_NEED <= L_SHEIKA_MAX
        D_SHEIKA_MID = L_NEED
    ELSE
        D_SHEIKA_MID = L_SHEIKA_MAX
        H_NEED = (S_SHEIKA_MIN_MM2 / D_SHEIKA_MID) * 1.05
        IF H_NEED <= H_SHEIKA_MAX
            NOM_H_SHEIKA_LAT = H_NEED
        ELSE
            NOM_H_SHEIKA_LAT = H_SHEIKA_MAX
        ENDIF
    ENDIF
    
    NOM_L1_SHEIKA = D_SHEIKA_MID + 3.0
    NOM_L2_SHEIKA = D_SHEIKA_MID - 3.0
    IF NOM_L2_SHEIKA < 4.0
        NOM_L2_SHEIKA = 4.0
    ENDIF
    S_SHEIKA_TRAP_NOM = ((NOM_L1_SHEIKA + NOM_L2_SHEIKA) / 2.0) * NOM_H_SHEIKA_LAT
ENDIF
S_SHEIKA_FINAL_MM2 = S_SHEIKA_TRAP_NOM

/* --- 9.8. АДАПТИВНЫЙ ЗАЗОР ПРИБЫЛЬ-ДЕТАЛЬ ------------------------ */
L_ZAZOR_MM = L_ZAZOR_MIN + (H_SHEIKA_MAX - NOM_H_SHEIKA_LAT) * 0.25
IF L_ZAZOR_MM > L_ZAZOR_MAX
    L_ZAZOR_MM = L_ZAZOR_MAX
ENDIF
IF L_ZAZOR_MM < L_ZAZOR_MIN
    L_ZAZOR_MM = L_ZAZOR_MIN
ENDIF

NOM_L_SHEIKA_PRIB_LAT = L_ZAZOR_MM + 2.0

/* --- 9.9. РАСЧЕТ МОДУЛЕЙ ДЛЯ ТЕПЛОФИЗИКИ (БЛОК 10) --------------- */
L_SLOPE_RAW = sqrt(pow(NOM_H_SHEIKA_LAT, 2.0) + pow(((NOM_L1_SHEIKA - NOM_L2_SHEIKA) / 2.0), 2.0))
P_SHEIKA_RAW = NOM_L1_SHEIKA + NOM_L2_SHEIKA + 2.0 * L_SLOPE_RAW
M_SHEIKA_REAL = S_SHEIKA_FINAL_MM2 / P_SHEIKA_RAW

K_BIAS_DYNAMIC = K_THERMAL_BIAS_MAX - (L_ZAZOR_MM - L_ZAZOR_MIN) / (L_ZAZOR_MAX - L_ZAZOR_MIN) * (K_THERMAL_BIAS_MAX - K_THERMAL_BIAS_MIN)
M_SHEIKA_EFF = M_SHEIKA_REAL * K_BIAS_DYNAMIC

/* Вариант 2 (Изомодульная коренастая боковая прибыль) */
NOM_H_PRIB_MOD = NOM_D_PRIB_LAT * 1.1
NOM_D_PRIB_MOD = 2.0 * sqrt(V_REAL_PRIB_LAT / (PI * NOM_H_PRIB_MOD))
M_PRIB_MOD_REAL = NOM_D_PRIB_MOD / 5.5

/* --- 9.10. Накатываем усадку HOT_FACTOR и выводим CAD-размеры ---- */
CAD_D_PRIB_LAT = ceil(NOM_D_PRIB_LAT * HOT_FACTOR)
CAD_H_PRIB_LAT = ceil(NOM_H_PRIB_LAT * HOT_FACTOR)

CAD_H_SHEIKA_LAT  = ceil(NOM_H_SHEIKA_LAT * HOT_FACTOR)
CAD_L1_SHEIKA_LAT = ceil(NOM_L1_SHEIKA * HOT_FACTOR)
CAD_L2_SHEIKA_LAT = floor(NOM_L2_SHEIKA * HOT_FACTOR)
IF CAD_L2_SHEIKA_LAT < 4
    CAD_L2_SHEIKA_LAT = 4
ENDIF
CAD_L_SHEIKA_LAT  = ceil(NOM_L_SHEIKA_PRIB_LAT * HOT_FACTOR)

CAD_D_SHEIKA_PRIB_LAT = ceil(0.75 * NOM_D_PRIB_LAT * HOT_FACTOR)

CAD_D_PRIB_MOD = ceil(NOM_D_PRIB_MOD * HOT_FACTOR)
CAD_H_PRIB_MOD = ceil(NOM_H_PRIB_MOD * HOT_FACTOR)
CAD_R_BOT_MOD  = ceil(CAD_D_PRIB_MOD * 0.3)
CAD_H_BOT_MOD  = CAD_R_BOT_MOD

CAD_R_BOT_STRAIGHT = ceil((0.18 * NOM_D_PRIB_LAT) * HOT_FACTOR)
CAD_H_KARMAN_STR   = ceil(((CAD_H_SHEIKA_LAT / 2.0) + CAD_R_BOT_STRAIGHT) * HOT_FACTOR)

CAD_L_FEED_ZONE = ceil((4.5 * W_REAL_WALL_LAT) * HOT_FACTOR)
CAD_M_OTL_LAT   = floor(M_OTL_LAT * 10.0 + 0.5) / 10.0

/* Вычисляем справочные массы одной чистой боковой прибыли двух вариантов */
M_ONE_PRIB_LAT_V1 = floor(((V_REAL_PRIB_LAT * PM) / 1e9) * 10.0 + 0.5) / 10.0
V_REAL_MOD_LAT = PI * pow((NOM_D_PRIB_MOD / 2.0), 2.0) * NOM_H_PRIB_MOD
M_ONE_PRIB_LAT_V2 = floor(((V_REAL_MOD_LAT * PM) / 1e9) * 10.0 + 0.5) / 10.0

/* ================================================================= */
/* БЛОК 10. ТЕПЛОФИЗИЧЕСКИЕ ЛИМИТЫ И ЭКСПЕРТИЗА ВЕРДИКТОВ (ФЛАГИ)    */
/* ================================================================= */

/* --- 10.1. Автономное проектирование предельных длин в 3D -------- */
/* Единая привязка к сквозному K_THERM_PIT без раздувания лишних параметров */
CAD_L_PIT_MAX = ceil(CAD_H_PIT_PRIB * K_THERM_PIT)
CAD_L_SHL_MAX = ceil(CAD_H_SHL * K_THERM_PIT)


/* --- 10.2. Независимые булевы флаги-датчики (По заветам аудита) -- */
FLAG_AREA_OK    = 0
FLAG_THERM_BAD  = 0
FLAG_THERM_OVER = 0

IF S_SHEIKA_FINAL_MM2 >= S_SHEIKA_MIN_MM2
    FLAG_AREA_OK = 1
ENDIF

IF M_SHEIKA_EFF <= M_OTL_LAT
    FLAG_THERM_BAD = 1
ENDIF

IF M_SHEIKA_EFF >= M_PRIB_MOD_REAL
    FLAG_THERM_OVER = 1
ENDIF


/* --- 10.3. Дополнительный расчет времени остывания элементов ----- */
TIME_ZAT_SHEIKA_RAW = ceil(K_CHVORINOV * pow(M_SHEIKA_REAL, 2.0))
TIME_ZAT_SHEIKA_EFF = ceil(K_CHVORINOV * pow(M_SHEIKA_EFF, 2.0))
TIME_ZAT_PRIB_1     = ceil(K_CHVORINOV * pow(M_PRIB_MOD_REAL, 2.0))


/* --- 10.4. Плоской пошаговый светофор вердиктов на 5 случаев ----- */
VERDICT_TEXT = "ОК: Условия направленной кристаллизации и площади полностью ВЫПОЛНЕНЫ."

/* СЛУЧАЙ 3 (ИДЕАЛ): Флаги в норме, площадь достаточна */
IF FLAG_AREA_OK == 1
    IF FLAG_THERM_BAD == 0
        IF FLAG_THERM_OVER == 0
            VERDICT_TEXT = "ОК: Условия направленной кристаллизации и площади полностью ВЫПОЛНЕНЫ."
        ENDIF
    ENDIF
ENDIF

/* СЛУЧАЙ 2: По теплу проходит, но есть дефицит площади Бернулли */
IF FLAG_AREA_OK == 0
    IF FLAG_THERM_BAD == 0
        IF FLAG_THERM_OVER == 0
            VERDICT_TEXT = "ВНИМАНИЕ: По теплу проходит, но есть ДЕФИЦИТ ПЛОЩАДИ! Нож расширен до предела."
        ENDIF
    ENDIF
ENDIF

/* СЛУЧАЙ 4: Нож заужен по теплу (Замерзнет раньше фланца детали) */
IF FLAG_THERM_BAD == 1
    VERDICT_TEXT = "РИСК: Нож заужен! Он перемерзнет раньше фланца детали."
ENDIF

/* СЛУЧАЙ 5: Нож переутолщен по теплу (Усадочная раковина зайдет в деталь) */
IF FLAG_THERM_OVER == 1
    VERDICT_TEXT = "РИСК: Нож избыточен! Усадочная раковина может зайти во фланец."
ENDIF

/* СЛУЧАЙ 1: Тотальный тупик габаритов ХТС со всех сторон */
IF S_SHEIKA_FINAL_MM2 < S_SHEIKA_MIN_MM2
    IF NOM_H_SHEIKA_LAT == H_SHEIKA_MAX
        IF D_SHEIKA_MID == L_SHEIKA_MAX
            /* Строка разрезана для жесткого лимита парсера Creo на длину строки */
            VERDICT_TEXT = "КРАШ ГАБАРИТОВ! Нож зажат ХТС со всех сторон. "
            VERDICT_TEXT = VERDICT_TEXT + "Добавьте прибыли или смените подвод!"
        ENDIF
    ENDIF
ENDIF


/* ================================================================= */
/* БЛОК 11. ЦЕНТРОБЕЖНЫЙ ШЛАКОУЛОВИТЕЛЬ И СОПРЯЖЕНИЕ КАНАЛОВ ЛПС     */
/* ================================================================= */

/* --- 11.1. Базовые пропорции центробежного цилиндра (мм) --------- */
/* СТРОГО ПО ПАСПОРТУ СПЛАВОВ: K_CENTRIF_P динамически меняет физику вихря */
NOM_D_CENTRIF = K_CENTRIF_P * sqrt(S_SHL_MM2)
NOM_H_CENTRIF = NOM_D_CENTRIF * 1.5

/* --- 11.2. Входной канал подвода (мм) ---------------------------- */
S_IN_MM2 = S_SHL_MM2
H_IN_NOM = NOM_H_SHL

L1_IN_NOM = (S_IN_MM2 / H_IN_NOM) + (H_IN_NOM * SLOPE_ANG_RAD)
L2_IN_NOM = (S_IN_MM2 / H_IN_NOM) - (H_IN_NOM * SLOPE_ANG_RAD)
IF L2_IN_NOM < 4.0
    L2_IN_NOM = 4.0
ENDIF

/* --- 11.3. Выходной канал отвода (мм) ---------------------------- */
/* Сужение потока на 15% для поддержания центробежного вращения */
S_OUT_MM2 = S_SHL_MM2 * 0.85
H_OUT_NOM = NOM_H_SHL * 0.90

L1_OUT_NOM = (S_OUT_MM2 / H_OUT_NOM) + (H_OUT_NOM * SLOPE_ANG_RAD)
L2_OUT_NOM = (S_OUT_MM2 / H_OUT_NOM) - (H_OUT_NOM * SLOPE_ANG_RAD)
IF L2_OUT_NOM < 4.0
    L2_OUT_NOM = 4.0
ENDIF

/* --- 11.4. Накатываем усадку HOT_FACTOR и выводим CAD-размеры ----- */
CAD_D_CENTRIF   = ceil(NOM_D_CENTRIF * HOT_FACTOR)
CAD_H_CENTRIF   = ceil(NOM_H_CENTRIF * HOT_FACTOR)

/* Габариты входной трапеции (Подвод) */
CAD_H_IN_TRAP   = ceil(H_IN_NOM * HOT_FACTOR)
CAD_L1_IN_TRAP  = ceil(L1_IN_NOM * HOT_FACTOR)
CAD_L2_IN_TRAP  = floor(L2_IN_NOM * HOT_FACTOR)
CAD_S_IN_MM2    = ceil(S_IN_MM2 * pow(HOT_FACTOR, 2.0))

/* Габариты выходной трапеции (Отвод) */
CAD_H_OUT_TRAP  = ceil(H_OUT_NOM * HOT_FACTOR)
CAD_L1_OUT_TRAP = ceil(L1_OUT_NOM * HOT_FACTOR)
CAD_L2_OUT_TRAP = floor(L2_OUT_NOM * HOT_FACTOR)
CAD_S_OUT_MM2   = ceil(S_OUT_MM2 * pow(HOT_FACTOR, 2.0))

/* Конструирование шламового кармана и купола чаши */
CAD_H_KARMAN_CENTRIF = ceil((CAD_H_IN_TRAP * 0.6) * HOT_FACTOR)
CAD_R_BOT_CENTRIF    = ceil((CAD_D_CENTRIF * 0.15) * HOT_FACTOR)


/* ================================================================= */
/* БЛОК 12. ПРОГРАММА ТЕРМООБРАБОТКИ (ТО) ПО СТАНДАРТУ АУДИТА        */
/* ================================================================= */

/* --- 12.1. Прямое вычисление параметров нагрева садки (в часах) --- */
TIME_HEAT_UP = (HEAT_BATCH_KG / 100.0) * K_HEAT

/* Ограничение снизу: нагрев не может быть быстрее 2 часов для массивных садок */
/* Исключение составляют только серый чугун и нержавеющая аустенитная сталь */
IF ID_SPLAVA != 2
    IF ID_SPLAVA != 6
        IF TIME_HEAT_UP < 2.0
            TIME_HEAT_UP = 2.0 
        ENDIF
    ENDIF
ENDIF


/* --- 12.2. Изотермическая выдержка на независимых флагах -------- */
FLAG_TO_T6   = 0
FLAG_TO_ZERO = 0

/* Флаг Т6 активен только для алюминиевого сплава АК7ч */
IF ID_SPLAVA == 3
    FLAG_TO_T6 = 1
ENDIF

/* Интеллектуальный флаг: если в Паспорте сплавов K_HOLD занулен, выдержка = 0 */
IF K_HOLD <= 0.0
    FLAG_TO_ZERO = 1
ENDIF

/* Исполнительная логика вычисления времени выдержки садки */
IF FLAG_TO_T6 == 1
    TIME_HOLD = 6.0
ENDIF

IF FLAG_TO_T6 == 0
    IF FLAG_TO_ZERO == 1
        TIME_HOLD = 0.0
    ELSE
        /* Расчет времени выдержки на толщину преобладающей стенки отливки */
        TIME_HOLD_RAW = (DELTA_MM * K_HOLD / 60.0) + 1.0
        VAL_FOR_FLOOR = TIME_HOLD_RAW * 10.0 + 0.5
        TIME_HOLD = floor(VAL_FOR_FLOOR) / 10.0
    ENDIF
ENDIF


/* --- 12.3. Фиксация времени контролируемого охлаждения ----------- */
TIME_COOL_DOWN = K_COOL


/* --- 12.4. Итог: сквозное время работы термической печи (в часах) - */
HEAT_TIME_HOURS = TIME_HEAT_UP + TIME_HOLD + TIME_COOL_DOWN


/* ================================================================= */
/* БЛОК 13. ТЕПЛОФИЗИЧЕСКИЙ И ГЕОМЕТРИЧЕСКИЙ РАСЧЕТ ХОЛОДИЛЬНИКА    */
/* ================================================================= */

/* --- 13.1. Автоматический подбор констант по тумблеру MAT_CHILLER   */
CHILL_DENSITY = DENSITY_STEEL
CHILL_K_EFF   = K_EFF_STEEL

IF MAT_CHILLER == 2
    /* Выбрана медь - экстремальный теплоотвод */
    CHILL_DENSITY = DENSITY_COPPER
    CHILL_K_EFF   = K_EFF_COPPER
ENDIF

IF MAT_CHILLER == 3
    /* Выбран литейный графит - чистая поверхность */
    CHILL_DENSITY = DENSITY_GRAPHITE
    CHILL_K_EFF   = K_EFF_GRAPHITE
ENDIF


/* --- 13.2. Расчет конструктивных CAD-размеров плиты оснастки ----- */
/* Исполнительная толщина плиты на основе коэффициента усадки металла */
NOM_H_CHILLER_RAW = W_REAL_WALL_LAT * K_CHILL_THICK
CAD_H_CHILLER = ceil(NOM_H_CHILLER_RAW * HOT_FACTOR)

/* Площадь контактного пятна плиты по габаритам бокового фланца ХТС */
CAD_S_CHILL_CONT = ceil((H_UZLA_LAT_MM * W_UZLA_LAT_MM) * HOT_FACTOR)

/* Длина дуги (сегмента) плиты по ширине фланца заготовки в мм */
CAD_L_CHILLER = ceil(W_UZLA_LAT_MM * HOT_FACTOR)

/* Высота плиты холодильника по вертикали фланца заготовки в мм */
CAD_W_CHILLER = ceil(H_UZLA_LAT_MM * HOT_FACTOR)


/* --- 13.3. Калькуляция физического веса плиты (в кг) -------------- */
/* Находим объем плиты холодильника в кубических миллиметрах */
V_CHILLER_MM3 = NOM_H_CHILLER_RAW * H_UZLA_LAT_MM * W_UZLA_LAT_MM
M_ONE_CHILLER_KG = floor(((V_CHILLER_MM3 * CHILL_DENSITY) / 1e9) * 10.0 + 0.5) / 10.0


/* --- 13.4. Интенсификация остывания корки чугуна ВЧ50 по Чворинову - */
/* Рассчитываем падение времени кристаллизации узла отливки с плитой  */
M_OTL_LAT_CHILLED = M_OTL_LAT * CHILL_K_EFF
TIME_ZAT_CHILLED = ceil(K_CHVORINOV * pow(M_OTL_LAT_CHILLED, 2.0))


/* ================================================================= */
/* БЛОК 14. АВТОМАТИЧЕСКИЙ РАСЧЕТ СЕБЕСТОИМОСТИ ЗАГОТОВКИ (ERP)      */
/* ================================================================= */

/* --- 14.1. ПРЯМОЙ РАСЧЕТ МАСС ЭЛЕМЕНТОВ ЛПС (В КИЛОГРАММАХ) ------ */

/* 14.1.1. Линейный диаметр основания воронки стояка из ТВОЕЙ площади S_ST */
NOM_D_ST_NIZ_MM = sqrt(4.0 * (S_ST * 1.0e6) / PI)

/* 14.1.2. Объем и физический вес круглого стояка в килограммах */
V_ST_3D = PI * pow((NOM_D_ST_NIZ_MM / 2.0), 2.0) * H0_MM
M_ST_3D = (V_ST_3D * PM) / 1e9

/* 14.1.3. Вес шлакоуловителя по тепловой длине через сквозной параметр K_THERM_PIT */
M_SHL_3D = (S_SHL_MM2 * (K_THERM_PIT * NOM_H_SHL) * PM * KOL_VO_SHL) / 1e9

/* 14.1.4. Масса вращения цилиндрического тела центробежной чаши ХТС */
M_CENTRIF_3D = (PI * pow((NOM_D_CENTRIF / 2.0), 2.0) * NOM_H_CENTRIF * PM) / 1e9

/* 14.1.5. Суммарный вес всех работающих ножей-питателей всей формы */
M_PIT_3D = (CAD_S_PIT_SUM_PRIB * 40.0 * PM) / 1e9

/* 14.1.6. ЭКОНОМИКА МАТРИЦЫ СХЕМ: масса прибылей по тумблеру SXEMA_PITANIYA */
M_PRIB_UP_3D = (M_ONE_PRIB_UP_KG * KOL_PRIB_UP_TOT) * K_MASS_UP
M_PRIB_LAT_3D = (M_ONE_PRIB_LAT_V2 * KOL_PRIB_LAT_TOT) * K_MASS_LAT

/* 14.1.7. УЧЕТ ОCHАСТКИ: Прямая увязка веса холодильника из Блока 13 с тумблером экономии */
M_CHILLER_TO_ECO = M_ONE_CHILLER_KG * CHILLER_TO_ECO

/* 14.1.8. ИТОГ: Фактическая чистая massа скрапа ЛПС на один куст формы */
M_LPS_FACT = M_ST_3D + M_SHL_3D + M_CENTRIF_3D + M_PIT_3D + M_PRIB_UP_3D + M_PRIB_LAT_3D + M_CHILLER_TO_ECO


/* --- 14.2. КАЛЬКУЛЯЦИЯ БАЛАНСА ВЕСОВ, ВЫХОДА ГОДНОГО И КИМ ------- */

/* 14.2.1. Полный заливаемый вес жидкого металла ковша на форму */
M_POUR_TOTAL = (MASSA_OTLIVKI * KOL_VO_OTLIVOK) + M_LPS_FACT

/* 14.2.2. Коэффициент Использования Металла (выход годного куста) */
KIM = (MASSA_OTLIVKI * KOL_VO_OTLIVOK) / M_POUR_TOTAL


/* --- 14.3. ПОФРАКЦИОННЫЙ РАСЧЕТ ЗАТРАТ ЦЕХА НА 1 ЗАГОТОВКУ -------- */

/* 14.3.1. Доля веса заливки и скрапа ЛПС на одну деталь */
M_RAW_ONE = M_POUR_TOTAL / KOL_VO_OTLIVOK
M_SCRAP_ONE = M_LPS_FACT / KOL_VO_OTLIVOK

/* 14.3.2. ПОЛНЫЙ БУХГАЛТЕРСКИЙ БАЛАНС ДВИЖЕНИЯ МЕТАЛЛА И ЛОМА */
C_METAL_RAW_TOTAL = M_RAW_ONE * COST_METALL_RAW
C_SCRAP_RETURN = M_SCRAP_ONE * COST_METALL_RAW * 0.8
C_METAL_ONE = C_METAL_RAW_TOTAL - C_SCRAP_RETURN

/* Округляем веса для аккуратного вывода в Note */
M_RAW_W   = floor(M_RAW_ONE * 10.0 + 0.5) / 10.0
M_SCRAP_W = floor(M_SCRAP_ONE * 10.0 + 0.5) / 10.0

/* 14.3.3. Расход кВт*ч энергии индуктора на расплавление куста */
KW_MELT_TOTAL = (M_POUR_TOTAL / 1000.0) * (POWER_FURNACE_KW / TONS_PER_HOUR)
KW_MELT_ONE = KW_MELT_TOTAL / KOL_VO_OTLIVOK

/* 14.3.4. СТАТЬЯ 2: Стоимость ЭЛЕКТРОЭНЕРГИИ ПЛАВЛЕНИЯ по коммерческому тарифу */
C_MELT_ONE = KW_MELT_ONE * COST_MELTING_KWH

/* 14.3.5. Масса песка ХТС формы исходя из пропорции металла куста 1:4 */
M_SAND_TOTAL = M_POUR_TOTAL * 4.0

/* 14.3.6. Перевод массы песка в физический объем формовочной смеси в куб. метрах */
V_MIXTURE_M3 = floor((M_SAND_TOTAL / 1500.0) * 100.0 + 0.5) / 100.0
V_MIX_ONE = floor((V_MIXTURE_M3 / KOL_VO_OTLIVOK) * 100.0 + 0.5) / 100.0

/* 14.3.7. СТАТЬЯ 3: Стоимость КВАРЦЕВОГО ПЕСКА на одну полезную заготовку */
M_SAND_ONE = M_SAND_TOTAL / KOL_VO_OTLIVOK
C_SAND_ONE = (M_SAND_ONE / 1000.0) * COST_SAND_TONS

/* 14.3.8. Масса дорогостоящей жидкой связующей смолы ХТС в замесе формы */
M_RESIN_TOTAL = M_SAND_TOTAL * (RESIN_PERCENT / 100.0)
M_RESIN_ONE = M_RESIN_TOTAL / KOL_VO_OTLIVOK
M_RESIN_W = floor(M_RESIN_ONE * 10.0 + 0.5) / 10.0

/* 14.3.9. СТАТЬЯ 4: Стоимость СВЯЗУЮЩЕЙ СМОЛЫ ХТС на одну заготовку */
C_RESIN_ONE = M_RESIN_ONE * COST_RESIN_KG

/* 14.3.10. СТАТЬЯ 5: ПРЯМАЯ ЗАРПЛАТА рабочих (Формовка, сборка и обрубка куста) */
C_LABOR_ONE = (TIME_FORMING_MIN + TIME_CLEAN_MIN) * (WAGE_M_WORKER / WORK_HOURS_M / 60.0)

/* 14.3.11. Доля энергии камерной печи ТО, потребленная весом нашей детали */
KW_HEAT_ONE = (POWER_HEAT_KW * HEAT_TIME_HOURS) / (HEAT_BATCH_KG / MASSA_OTLIVKI)

/* 14.3.12. СТАТЬЯ 6: Стоимость ЭЛЕКТРОЭНЕРГИИ ТЕРМООБРАБОТКИ за полный цикл печи ТО */
C_HEAT_ONE = KW_HEAT_ONE * COST_HEAT_KWH

/* 14.3.13. СТАТЬЯ 7: ПРЯМОЙ РАСЧЕТ ФИНИШНОЙ ДРОБЕСТРУЙНОЙ ОЧИСТКИ ОТ ПРИГАРА */
KW_SHOT_TOTAL = POWER_SHOT_KW * (TIME_SHOT_BLAST_MIN / 60.0)
C_SHOT_ENERGY_TOTAL = KW_SHOT_TOTAL * COST_MELTING_KWH
KG_SHOT_SPENT_TOTAL = SHOT_CONSUME_KG_H * (TIME_SHOT_BLAST_MIN / 60.0)
COST_SHOT_MAT_TOTAL = KG_SHOT_SPENT_TOTAL * COST_SHOT_KG
C_SHOT_ONE = (C_SHOT_ENERGY_TOTAL + COST_SHOT_MAT_TOTAL) / KOL_VO_OTLIVOK

/* 14.3.14. СУММАРНАЯ ЭНЕРГЕТИКА: Расход энергии (Плавка + ТО + Очистка) в кВт*ч и рублях */
TOTAL_KW_ONE = KW_MELT_ONE + KW_HEAT_ONE + (KW_SHOT_TOTAL / KOL_VO_OTLIVOK)
TOTAL_ENERGY_COST_ONE = C_MELT_ONE + C_HEAT_ONE + (C_SHOT_ENERGY_TOTAL / KOL_VO_OTLIVOK)


/* --- 14.4. ИНТЕГРАЛЬНЫЙ СИНТЕЗ СЕБЕСТОИМОСТИ И СТРУКТУРЫ ЗАТРАТ --- */

/* 14.4.1. ИТОГОВАЯ СЕБЕСТОИМОСТЬ 1 штуки готовой заготовки с округлением вверх до рубля */
COST_ONE_OTLIVKI_RUB = ceil(C_METAL_ONE + C_MELT_ONE + C_SAND_ONE + C_RESIN_ONE + C_LABOR_ONE + C_HEAT_ONE + C_SHOT_ONE)

/* 14.4.2. Удельная себестоимость одного килограмма годного литья */
COST_PER_KG_RUB = floor((COST_ONE_OTLIVKI_RUB / MASSA_OTLIVKI) * 10.0 + 0.5) / 10.0

/* 14.4.3. Вычисляем процентный вклад каждой статьи затрат в итоговую стоимость до целого */
P_METAL     = floor((C_METAL_ONE / COST_ONE_OTLIVKI_RUB) * 100.0)
P_METAL_RAW = floor((C_METAL_RAW_TOTAL / COST_ONE_OTLIVKI_RUB) * 100.0)
P_SCRAP_RET = floor((C_SCRAP_RETURN / COST_ONE_OTLIVKI_RUB) * 100.0)

P_MELT      = floor((C_MELT_ONE / COST_ONE_OTLIVKI_RUB) * 100.0)
P_SAND      = floor((C_SAND_ONE / COST_ONE_OTLIVKI_RUB) * 100.0)
P_RESIN     = floor((C_RESIN_ONE / COST_ONE_OTLIVKI_RUB) * 100.0)
P_LABOR     = floor((C_LABOR_ONE / COST_ONE_OTLIVKI_RUB) * 100.0)
P_HEAT      = floor((C_HEAT_ONE / COST_ONE_OTLIVKI_RUB) * 100.0)
P_SHOT      = floor((C_SHOT_ONE / COST_ONE_OTLIVKI_RUB) * 100.0)

/* Процентное отношение масс элементов ЛПС к общему весу ковша до целого */
P_KG_DET    = floor(((MASSA_OTLIVKI * KOL_VO_OTLIVOK) / M_POUR_TOTAL) * 100.0)
P_KG_SCRAP  = floor((M_LPS_FACT / M_POUR_TOTAL) * 100.0)

/* ИСПРАВЛЕНИЕ: Гарантированный расчет доли всей энергии в себестоимости заготовки */
P_KW_TOT = floor((TOTAL_ENERGY_COST_ONE / COST_ONE_OTLIVKI_RUB) * 100.0)
M_RAW_W   = floor(M_RAW_ONE * 10.0 + 0.5) / 10.0
KW_MELT_W = floor(KW_MELT_ONE * 10.0 + 0.5) / 10.0
KW_TOT_W  = floor(TOTAL_KW_ONE * 10.0 + 0.5) / 10.0


/* --- 14.5. ФИНАНСОВЫЙ АУДИТ КУСТА ФОРМЫ -------------------------- */
/* 14.5.1. Текстовый индикатор экономической эффективности */
VERDICT_ECONOMY = "ЭКОНОМИКА: КИМ куста в НОРМЕ. Себестоимость оптимальна."
IF KIM < 0.50
    VERDICT_ECONOMY = "ПЕРЕРАСХОД! ЛПС тяжелее детали. Сократите прибыли."
ENDIF

--- PARAMETERS ---
Источник: CreosON parameter:list, 380 параметров, карточка 2026-09-16

ОБОЗНАЧЕНИЕ (STRING) = LITEIKA_HTS_MM
ОБОЗНАЧЕНИЕ1 (STRING) = 
СТАРЫЙ_НОМЕР (STRING) = 
НАИМЕНОВАНИЕ (STRING) = 
НАИМЕНОВАНИЕ1 (STRING) = 
НАИМЕНОВАНИЕ2 (STRING) = 
ТИП (STRING) = Сборка
ТИП2 (STRING) =  
ФОРМАТ (STRING) = А3
РАЗРАБОТАЛ (STRING) = 
ПРОВЕРИЛ (STRING) = 
ТЕХ_КОНТРОЛЬ (STRING) = 
НАЧ_ОТДЕЛА (STRING) = 
НОРМО_КОНТРОЛЬ (STRING) = 
УТВЕРДИЛ (STRING) = 
ПЕРВ_ПРИМЕН (STRING) = 
СПРАВ_№ (STRING) = 
MASS (DOUBLE) = 
СТАНДАРТ (STRING) = 
ПРЕДПРИЯТИЕ (STRING) = ООО "ПТО"
... ещё 360 параметров (полный список в liteika_hts_mm_params_raw.json)

--- MASSPROPS ---
Mass: 0.0 kg
Volume: 0 mm3
Area: 0.0 mm2
