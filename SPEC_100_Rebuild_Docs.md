# SPEC 100: Rebuild PASSPORT.md and README.md

## Goal
Rebuild `PASSPORT.md` and `README.md` using a "reconstruction" approach (writing complete files or large blocks) to bypass the limitations of the Anchor Method and `insert_line`.

## Strategy
- Use `write_file` for complete reconstruction or `editor` for large blocks.
- Constraints: All writes must remain $\le$ 8KB per operation.
- `PASSPORT.md` is currently broken (missing header and truncated).
- `README.md` contains a redundant large table.

## Files
- `D:\AI\repo\PASSPORT.md`
- `D:\AI\repo\README.md`
