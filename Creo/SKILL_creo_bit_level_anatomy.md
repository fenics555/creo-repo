# SKILL: Creo Bit-Level Anatomy & Reverse Engineering

**Status:** ACTIVE / EVOLVING
**Target:** Complete reconstruction of Creo `.prt` files from raw bytes to semantic models.

## 🧠 CORE PRINCIPLES (The "Golden Rules")
1. **NEVER TRUST THE TOC ALONE**: The Table of Contents (TOC) is a map, but the files contain the territory. Always validate TOC offsets against actual byte patterns (`feat_defs_`).
2. **KEYS OVER WINDOWS**: Do not search for data in "windows" (e.g., "find a double near an ID"). Search for **Keys** (e.g., `type\x00`, `ref_id\x00`) and extract values immediately following them.
3. **ANTI-HALLUCINATION (Binary Context)**: A sequence of bytes looks like a `double` only if it's NOT part of an ASCII string. Always use a "Printable ASCII Context Filter".
4. **POINTER-FIRST APPROACH**: Every major structure in Creo is linked. To master the file, you must master the `offset` and `pointer` logic.

## 🔍 DISCOVERED ANATOMY (The "Truth Table")

### 1. Feature Delimiters & Markers
| Pattern | Meaning | Reliability | Note |
| :--- | :--- | :--- | :--- |
| `feat_defs_NNN` | Feature Definition Marker | **HIGH** | The primary anchor for all feature-based parsing. |
| `FB E3 F7 80` | Internal Segmenter | **LOW** | **FALSE DELIMITER.** Do not use for tree construction. |
| `\x00` | Null Terminator | **HIGH** | Used to end strings and signify the end of key-value pairs. |

### 2. Key-Value Patterns (Surgical Extraction)
Found keys used to identify feature properties:
- `type\x00` / `ft_type\x00`: Identifies the feature type (e.g., EXTRUDE, REVOLVE).
- `AE_Type\x00`: High-priority attribute key for classification.
- `ref_id\x00` / `parent_id\x00`: Defines the hierarchy (Tree structure).
- `symbol_key\x00`: Identifies the internal logic/symbol used for the feature.

### 3. Data Types & Filtering
- **Doubles (64-bit)**: Found in geometry records. 
    - *Filter Rule*: If 8-16 bytes around the `double` are printable ASCII, it is a **STRING**, not a number.
- **Integers (32-bit)**: Often used for IDs and pointers.
    - *Format*: Check both Little-Endian (`<I`) and Big-Endian (`>I`) to be safe.

## 🗺️ ROADMAP TO "LAST BIT" MASTERY

### Phase 1: Semantic Mapping (CURRENT)
- [x] Identify feature types via Keys.
- [x] Extract geometry via context-aware filters.
- [x] Map raw numbers to engineering names (depth, radius, etc.).

### Phase 2: Pointer & Linkage Mastery (NEXT)
- [ ] **Pointer Analysis**: Determine if Creo uses absolute file offsets or relative offsets within segments.
- [ ] **TOC Deep Dive**: Reverse engineer how the TOC is built and how it links to the `FeatDefs` section.
- [ ] **Object Interdependency**: Map how a change in one feature (e.g., a Sketch) propagates through its children (e.g., an Extrude).

### Phase 3: Full Reconstruction
- [ ] **Binary Completeness**: Parse even the "unknown" or "unused" sections of the file.
- [ ] **Compression/Encoding**: Identify if any blocks use proprietary compression or non-UTF8 encodings.
