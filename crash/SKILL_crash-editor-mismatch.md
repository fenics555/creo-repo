name: editor-mismatch
system: CRASH
description: Use when: editor tool fails with "text not found" due to old_text mismatch after a partial update or context change.
when: editor-mismatch, text not found, mismatch, old_text mismatch
date: 16.09.2026
executor: Cline (cloud/local)
task: PASSPORT.md update (SPEC 44v)
ОШИБКА (дословно): Editor operation failed: No replacement performed: text not found in [FILE]
СИМПТОМ: editor call returns error instead of modifying the file, even though the user-perceived state matches the old_text or should be a simple replacement.
ПРИЧИНА: old_text was copied from a previous state but the file was modified in between (e.g., by a previous editor or insert_line call), or subtle encoding/escaping issues.
ПРОФИЛАКТИКА:
1. Always read_file immediately before an editor call to ensure old_text is fresh.
2. For large files, use findstr to verify the presence of the anchor/text before attempting replacement.
3. If mismatch persists, use a temporary Python script with a marker-based replacement (Anchor Patch).