# SKILL_creo_reverse_engineering_knowledge.md

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
