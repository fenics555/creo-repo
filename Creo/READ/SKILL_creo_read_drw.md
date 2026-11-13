# SKILL: Creo Drawing (.drw) Binary Parsing
## Description
Method for extracting model references, sheet information, and drawing attributes from .drw binary files.

## Findings (Stage 5)
- Section Dwg_Models: Contains model name references. Pattern: model_names<MODEL_NAME>.PRT
- Section Dwg_Objects: Contains drawing entities and links.
- Section Dwg_MasterRep: Contains format and master representation data.
- Attribute Records: Key-value pairs. Pattern: [Name]Value@<metadata>

## Integration
- Node: .drw node with role: DRAWING
- Edge: represents -> .prt/.asm node
- Edge: uses_format -> Format node
- Edge: has_sheet -> Sheet node
