# SKILL: Creo Parameter Graph Navigation

## The "Chain of Command" Pattern
Manufacturing data in Creo is not a flat list; it is a **linked list of parameter blocks**. A parameter often acts as a pointer to the next logical piece of metadata.

## The Navigation Chain
Based on deep inspection of `setup_data`, the hierarchy follows this sequence:
1.  **`setup_type`**: Identifies the block type.
2.  **`setup_id`**: Acts as a pointer/key to the attribute block.
3.  **`attr`**: Indicates the existence of an attribute set.
4.  **`appl_id`**: The Application ID (e.g., `05`), defining the context (Manufacturing/Setup).
5.  **`id_map_info_ptr`**: **CRITICAL**. This is a memory-style pointer/offset to a mapping table that connects the setup to a specific Tool, Fixture, or Process ID.
6.  **`setup_data(...)`**: The payload containing the actual geometry or process offsets.

## Extraction Logic for "The Jump"
To link a Part to a Fixture:
1.  **Locate** `setup_data` block.
2.  **Extract** `id_map_info_ptr` and `appl_id`.
3.  **Follow the Pointer**: Navigate to the offset indicated by `id_map_info_ptr` (or use it as a key in a search).
4.  **Identify the Entity**: The mapping table will contain the **Unique Identifier** (String or Integer) of the Fixture/Tool.
5.  **Global Search**: Use the extracted Unique Identifier to perform a recursive search across the entire PLM directory structure (`Z:\PTC\Work\...`).

## Troubleshooting
- If `setup_id` returns `'attr'`, do not stop. This is a sign that you must follow the chain to the `appl_id` and `id_map_info_ptr`.
- Always treat `id_map` as a **navigator**, not a value.
