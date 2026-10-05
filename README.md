# Creo Agent — Knowledge Base and Skills

A structured knowledge base, rule set and skill library that lets an AI coding agent
work with **PTC Creo Parametric** in a reproducible, evidence-based way: CREOSON automation,
model rename and copy operations, PDF/drawing pairing, crash precedents and a survival guide
for local LLMs running in the IDE.

## Mass properties — READ (verified 2026-10-04)

Mass, volume and surface area ARE stored in `.prt` and are readable from raw bytes.

**Record layout**
```
PRO_MP_MASS  00  f8 01 f7 38 fb e3 f7 39 0e   e3 32  [тип]  [7 байт]  f1
PRO_MP_VOLUME ...                                   e3 32  2D    [7 байт] f1
PRO_MP_AREA   ...                                   e3 32  2D    [7 байт] f1
```
- `e3 32` — marker that a value follows
- `[тип]` — `28` for MASS, `2D` for VOLUME/AREA
- the 7 bytes are a big-endian IEEE-754 **double with the leading exponent byte stripped**
- `f1` — terminator

**Recovering the stripped byte.** It is not in the file. Two proven ways:
1. `VOLUME` / `AREA` — lead is recoverable from magnitude; verified `0x40` and `0x41`.
2. `MASS` — recover it from **density**: `MASS / VOLUME` must land in 6..9.5 g/cm³
   (steel 7.85). Verified: `0x3F` → 0.21461530730689607 (7.8500 g/cm³),
   `0x40` → 6.6861510413184719 (7.9000 g/cm³).

**Acceptance:** 6 of 6 values matched the JLINK ground truth to 17 significant digits
(mass + volume + area, two different models).

**Getting ground truth — use JLINK, not CREOSON.** CREOSON does not expose
`PRO_MP_*`. `D:\AI\tools\agent\creo_export\mass_probe.bat` does:
```
call .\mass_probe.bat Z:\PTC\Work\00080\00080-03.prt
-> 00080-03.prt  MASS=0,21461530730689607  VOLUME=27339,529593235176  AREA=13275,370841291067
```
Requires a running Creo; leaves it alive.

## What is inside
| Path | Purpose |
|---|---|
| `MANIFEST.md` | universal rules for any executor (the law layer) |
| `.clinerules` | environment delta for the Cline agent (transport, editor, search, crashes) |
| `SKILL_index.md` | map of all skills by domain |
| `Creo/`, `PDF/`, `Web/`, `Инженерные/`, `Трейлы/`, `Ошибки/` | domain entries and skills |
| `crash/` | crash constitution plus precedent skills with repeat counters |
| `PASSPORT.md` | current state of modules, data and history |
| `D:\AI\tools\agent\` (вне репо; агент сам и его README) | the agent itself (see its own README) |

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
