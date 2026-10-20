# SKILL_creo_reverse_engineering_knowledge.md

## Status: IN_PROGRESS (Links & Audit Modules)

### 1. Graph Architecture: Typed Relationship Graph
Instead of a simple tree, we use a **Typed Relationship Graph**.
Edges are categorized by type and direction (Upstream/Downstream).

#### 1.1. Taxonomy of Edges (Full Map)
| Category | Edge Type | Description | Source/Target Direction |
|---|---|---|---|
| **BOM (Inclusion)** | `contains` | Basic assembly hierarchy | Assembly $\to$ Component (Down) |
| | `contains_via_instance` | Assembly $\to$ Component with instance name | Assembly $\to$ Component (Down) |
| | `contains_simp_rep` | Component in a specific simplification | Assembly $\to$ Component (Down) |
| **Inheritance** | `inherit` | Derive/Inheritance (via `top_to_part_models`) | Part $\to$ Parent (Up) |
| | `mirror_of` | Mirror/Stock relationship (`MERGE_BASE_PART`) | Part $\to$ Base Part (Up) |
| | `copied_geom` | Copy Geometry | Part $\to$ Source (Up) |
| **Family Table** | `instance_of` | Family Instance $\to$ Generic Parent | Instance $\to$ Generic (Up) |
| | `used_via_instance` | Assembly $\to$ Generic (via instance) | Assembly $\to$ Generic (Down) |
| **Manufacturing** | `mfg_refers_to` | Mfg Assembly $\to$ Part | Bi-directional |
| | `mfg_stock_for` | Stock/Mirror part $\to$ Final part | Stock $\to$ Part (Up) |
| | `mfg_tool_for` | Tool $\to$ Operation | Tool $\to$ Op (Up) |
| **Audit/History** | `saved_as` | Part $\to$ Previous version (via `MdlStatus`) | Part $\to$ Old Part (Up) |
| | `rename_of` | Part $\to$ Renamed object | Part $\to$ Old Name (Up) |

### 2. Confirmed Patterns & Byte Structures

#### 2.1. MdlStatus (History & Audit)
Located in **`MdlStatus`** section. It is a structured section (not gzip).
Contains `mtrack_record_ptr` $\to$ `rec_arr`.
Each record has `action_type` and `typed_data` (8 subtypes):
- `MdlStored`: Simple save (version, comments).
- `TypedRedefineData`: Feature redefinition (feat_id, item_name).
- `TypedReorderData`: Feature reordering.
- `MTTyped_ModifyData`: **Dimension changes** (`dim_id`, `old_val`, `new_val`).
- `MpTypedData`: **Mass/Volume/Area changes** (stores `old_state` and `new_state` side-by-side).
- `RenameData`: Object renaming.
- `MTTyped_CreateData`: Feature creation.
- `MTTyped_FeatOperData`: Feature operations (patterns, groupings).

#### 2.2. Family Table
- Located in `FamilyInf` section. 
- Pattern: `\x00NAME\x00`.
- **Crucial**: To link instances to generic, must find `Sld_DrvTable`.

#### 2.3. Inheritance (Mirror/Derived)
- **Mirror**: `MERGE_BASE_PART\x00<name>\x00`.
- **Derived**: `top_to_part_models\x00<name>\x00`.

### 3. Implementation Details
- **Class**: `CreoLinksExtractor` in `creo_links.py`.
- **Dependencies**: `plm_reader.creo_read`, `creo_protocol_decoder.CreoProtocolDecoder`.
- **Encoding Note**: Use `latin-1` for decoding raw bytes before applying Unicode-aware regex patterns.

### 4. Known Issues / Pitfalls (CRITICAL)
1. **The Regex Trap**: NEVER use non-ASCII characters (like Cyrillic) directly inside a bytes regex (`rb"..."`). Decode to `latin-1` first.
2. **Endianness**: Always detect endianness via `MACH SUN_SunOS` marker. Windows is typically Little-Endian (`<d`), SunOS is Big-Endian (`>d`).
3. **Material Key**: Use `PTC_MATERIAL_NAME` instead of `PTC_MASTER_MATERIAL`.
4. **Parameter Encoding**: Fallback to `cp1251` for Russian parameters (`НАИМЕНОВАНИЕ`, etc.).
5. **TOC Normalization**: Remove `ND:0:` prefixes from TOC keys to ensure `toc.get("Model_Name")` works.
6. **BOM Definition**: BOM is not just a list of parts; it's `(assembly, simp_rep) -> [(component, instance, qty, ...)]`.

﻿# SKILL_creo_reverse_engineering_knowledge.md

## Status: IN_PROGRESS (Links Module)

### 1. Graph Architecture: Typed Relationships
Instead of a simple tree, we use a **Typed Relationship Graph**.
Edges are categorized by type:
- `contains`: Basic assembly hierarchy.
- `contains_via_instance`: Assembly -> Component (with instance name).
- `mirror_of`: Part -> Stock/Mirror part (via `MERGE_BASE_PART`).
- `inherit`: Part -> Parent (via `top_to_part_models` / `MdlRefInfo`).
- `instance_of`: Family Table instances -> Generic parent.

### 2. Confirmed Patterns & Findings
- **Family Table**: Located in `FamilyInf` section. Pattern: `\x00NAME\x00`.
  * *Crucial*: When parsing `FamilyInf` with regex, decode the segment to `latin-1` first to avoid `SyntaxError` with non-ASCII characters in bytes-regex.
- **Inheritance (Mirror)**: Look for the byte pattern `MERGE_BASE_PART\x00<name>\x00`.
- **Inheritance (Derived)**: Look for `top_to_part_models\x00<name>\x00`.
- **BOM**: Component data is often in `FeatDefsCmp` or `Comp_Data` sections.

### 3. Implementation Details
- **Class**: `CreoLinksExtractor` in `creo_links.py`.
- **Dependencies**: `plm_reader.creo_read`, `creo_protocol_decoder.CreoProtocolDecoder`.
- **Encoding Note**: Use `latin-1` for decoding raw bytes before applying Unicode-aware regex patterns.

### 4. Known Issues / Limitations
- `Mfg_info` extraction is currently a stub.
- Family Table generic parent identification is currently a placeholder (`GENERIC_PARENT`).
- BOM parsing is currently limited to top-level component identification.
