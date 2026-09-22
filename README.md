# Creo Agent — Knowledge Base and Skills

A structured knowledge base, rule set and skill library that lets an AI coding agent
work with **PTC Creo Parametric** in a reproducible, evidence-based way: CREOSON automation,
model rename and copy operations, PDF/drawing pairing, crash precedents and a survival guide
for local LLMs running in the IDE.

## What is inside
| Path | Purpose |
|---|---|
| `MANIFEST.md` | universal rules for any executor (the law layer) |
| `.clinerules` | environment delta for the Cline agent (transport, editor, search, crashes) |
| `SKILL_index.md` | map of all skills by domain |
| `Creo/`, `PDF/`, `Web/`, `Инженерные/`, `Трейлы/`, `Ошибки/` | domain entries and skills |
| `crash/` | crash constitution plus precedent skills with repeat counters |
| `PASSPORT.md` | current state of modules, data and history |
| `tools/agent/` | the agent itself (see its own README) |

## Quick start
1. Clone the repository and keep `MANIFEST.md` at the root of your knowledge base.
2. Copy `.clinerules` to your agent root (default `D:\AI`) — it loads automatically on session start.
3. Start a task: the agent reads the manifest, the survival skill and the domain entry it needs.

## Conventions
- Verbatim Russian content enters files only through the editor; the console does not carry Cyrillic.
- Every irreversible edit is preceded by a backup; external dumps are stored as raw twins with size and hash.
- A crash is never silent: report in the task, then a skill in `crash/` with a repeat counter.

## License
MIT
