name: crash_editor_too_large_and_non_unique_anchors
system: CRASH
description: Use when editor fails due to file size > 6KB or multiple matches found for old_text.
when: editor, too_large, multiple_matches, non_unique_anchor
date: 20.09.2026
executor: Cline
task: frontend_integration_pdfrefresh
ОШИБКА (дословно, для grep):
Editor input too large: new_text was ... characters, exceeding the recommended limit of 6000.
СИМПТОМ: Loop of failed editor calls or error about multiple matches.
ПРИЧИНА: Attempting full file rewrite via editor or using non-unique old_text in a file with duplicates.
ПРОФИЛАКТИКА:
1. For large files: Split the edit into multiple calls with small chunks of old_text/new_text.
2. For non-unique text: Find unique anchors (surrounding lines) or use run_commands to overwrite.
3. If file is highly corrupted (duplicates): Restore from last clean git commit and write using house channel (one write_file up to 8KB or part 1 + append strictly at the last line); PowerShell Set-Content for files with Cyrillic is forbidden - the console does not support it.
ПОВТОРЫ: 1
