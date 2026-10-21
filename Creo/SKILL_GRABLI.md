# SKILL_GRABLI: Lessons Learned

## Python Regex & Binary Data
- **Problem**: `re.PatternError: incomplete escape \x0 at position N`.
- **Cause**: Using literal `\x0` in a regex string in Python causes the parser to fail because it expects a two-digit hex code after `\x`.
- **Solution**: 
    - Use direct byte searching (`bytes.find()`) for locating keys.
    - If regex is absolutely necessary, use `re.escape()` or double-escape the sequence, or better yet, avoid raw byte escapes in the pattern string.
    - For binary data, work with `bytes` objects and avoid decoding until the value is isolated.

## Tooling Limitations
- **Editor**: When `editor` fails to replace text due to `old_text` mismatches or encoding issues, switch to creating a new file (e.g., `filename_vX.py`) to ensure a clean state.
- **Shell Encoding**: Be cautious with Cyrillic paths in shell commands. Use absolute paths and ensure encoding is handled correctly.
