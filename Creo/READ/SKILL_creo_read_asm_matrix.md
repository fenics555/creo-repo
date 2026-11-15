# SKILL: Извлечение матриц из бинарных файлов Creo (ASM)
# DESCRIPTION:
# Этот скилл описывает, как находить и извлекать 64-битные матрицы трансформации 
# из файлов сборки Creo (.asm).

# KEY FINDINGS (Обновлено 13.11.2026):
# 1. Имена компонентов (например, 'PLASTIC_RD.ASM') служат якорями, но могут храниться в неочевидных структурах.
# 2. Структуры метаданных (TOC) часто содержат поля 'ptr', которые являются RUNTIME-адресами, а не смещениями в файле.
# 3. РЕЗУЛЬТАТ АУДИТА: Сканирование на наличие сырых ортонормированных блоков (9/12/16 float64/float32) 
#    в .asm файлах (например, 00080-00.asm) не дало результатов. Это подтверждает, что матрицы трансформации 
#    часто НЕ кэшируются в самом .asm файле.
# 4. Если матрицы отсутствуют, следует искать:
#    - Положение компонента через ограничения/сопряжения (constraints/mates) в секциях 'NeuAsmSld' или 'MdlRefInfo'.
#    - Косвенные ссылки в 'MdlRefInfo' (хотя в некоторых версиях она может содержать только данные сессии/пайпов).
# 5. Эвристика для матрицы: блок из 9 чисел double, где часть 3x3 является ортонормированной 
#    (сумма квадратов строк ≈ 1.0).

# WORKFLOW:
# - Используйте 'find_comp_offset.py' для поиска имени компонента.
# - Используйте 'analyze_comp_block.py' для анализа окружающих метаданных.
# - Если значение 'matrix_ptr' < размер_файла, рассматривайте его как смещение в файле.
# - Если значение 'matrix_ptr' > размер_файла, это runtime-адрес (данные могут отсутствовать на диске).
# - Если сырой скан не дал результатов, проверьте 'NeuAsmSld' на наличие данных о положении на основе свойств.


## Proven: #FeatDefsCmp (Assembly Constraints)

This section contains the assembly constraints (mates) between components.

### 1. Structure
The section follows the `#UGC_TOC` index. It contains several key sub-structures:
- `trf_arr`: The transformation matrix for the component.
  - **Format:** `\xe2\x32\xed` + 8 bytes (IEEE-754 double) for each element of the matrix.
- `place_instruction_ptrs`: Pointers to placement instructions.
- `geometry1_id` & `geometry2_id`: The IDs of the geometric entities (faces, axes, etc.) involved in the mate.
- `memb_num1` & `memb_num2`: Count of members in the mate.
- `memb_id_tab2`: A table of member IDs.

### 2. Extraction Logic
1. Locate `#FeatDefsCmp` in `#UGC_TOC`.
2. Search for `trf_arr` to extract the component's position/orientation.
3. Match `geometry_id`s to elements in the feature tree.

