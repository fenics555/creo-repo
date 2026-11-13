# SKILL: Creo Manufacturing (.mfg) Binary Parsing
## Description
Method for extracting operations, tool references, and workpiece links from .mfg binary files.

## Expected Structure
- Workpiece Link: Connection to the base .prt or .asm.
- Operation Nodes: Identification of individual manufacturing operations.
- Tool References: Extraction of tool IDs (e.g., T0xxx) used in operations.
- Workpiece/Blank: Identification of the stock/blank material/geometry.

## Integration
- Node: .mfg node with role: MFG
- Edge: manufactures -> Workpiece node
- Edge: has_operation -> Operation node
- Edge: uses_tool -> Tool node
