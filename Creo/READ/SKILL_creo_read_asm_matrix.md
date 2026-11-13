# SKILL: Creo Binary Matrix Extraction (ASM)
# DESCRIPTION:
# This skill describes how to locate and extract 64-bit transformation matrices 
# from Creo assembly (.asm) files.
#
# KEY FINDINGS:
# 1. Component names (e.g., 'PLASTIC_RD.ASM') are used as anchors.
# 2. Metadata structures follow the name, containing fields like 'matrix_ptr' or 'world_matrix_ptr'.
# 3. CRITICAL: These 'ptr' fields often contain runtime memory addresses (e.g., 0x6c72...) 
#    rather than file offsets. This means the matrix data might NOT be in the file 
#    if it's a purely runtime-generated assembly, OR the pointers are offsets 
#    but the parser is misinterpreting them.
# 4. If the matrix data IS in the file, it appears as a block of 9, 12, or 16 
#    float64 (double) values.
# 5. Heuristic for matrix: A block of 9 doubles where the 3x3 part has 
#    orthonormal rows (sum of squares ≈ 1.0).
#
# WORKFLOW:
# - Use 'find_comp_offset.py' to locate component name.
# - Use 'analyze_comp_block.py' to inspect surrounding metadata.
# - If 'matrix_ptr' value < file_size, treat as file offset.
# - If 'matrix_ptr' value > file_size, it's a runtime address (data may be missing from disk).
# - Use 'find_matrix_data.py' to scan for blocks of doubles that pass the 
#   orthonormal check.
