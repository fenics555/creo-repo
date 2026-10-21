# SKILL: Creo Manufacturing Parameter Blocks

## Pattern Discovery
Manufacturing metadata in Creo files is not stored as simple key-value pairs, but in structured, linked blocks of parameters.

## Block Structure
The typical sequence found in a manufacturing context is:
1. **Type Indicator** (e.g., `setup_type`): Points to the existence of a setup block.
2. **ID Indicator** (e.g., `setup_id`): Points to the unique identifier or the start of the ID block.
3. **Attribute Pointer** (e.g., `attr`): Indicates that the next segment contains metadata attributes.
4. **Application ID** (e.g., `appl_id`): A numeric/hex identifier (e.g., `05`) that defines the context or the specific manufacturing application.
5. **Data Payload** (e.g., `setup_data`): The actual binary or string payload containing the specifics of the setup/fixture.

## Extraction Strategy
- **DO NOT** use complex regex patterns that include raw escape sequences like `\x0`.
- **USE** direct byte searching (`data.find(key_bytes)`).
- **USE** "Context Windows": Search for the key, then look for null-terminated strings (`\x00 ... \x00`) or printable ASCII within a defined byte window after the key.
- **HEX Analysis**: If no string is found, extract the subsequent 8-16 bytes in HEX to manually identify if it's a binary float, integer, or offset.
