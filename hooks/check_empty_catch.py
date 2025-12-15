#!/usr/bin/env python3
"""Pre-commit hook to detect empty catch/except blocks.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

AI agents often generate empty catch blocks that silently swallow errors,
making debugging incredibly difficult.

Warns about:
- except: pass (Python)
- except Exception: pass (Python)
- catch (e) {} (JavaScript/TypeScript)
- .catch(() => {}) (JavaScript/TypeScript)
"""

import re
import sys
from pathlib import Path


def _get_indentation(line: str) -> int:
    """Get the indentation level (number of leading spaces/tabs)."""
    return len(line) - len(line.lstrip())


def check_python_file(filepath: Path) -> list[tuple[int, str]]:
    """Check Python file for empty except blocks."""
    findings = []

    try:
        with open(filepath, encoding='utf-8') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Check for except clause
            if re.match(r'^except\s*.*:\s*$', stripped):
                except_indent = _get_indentation(line)
                body_indent = except_indent + 4  # Expected indentation of except body

                # Look at next non-empty line
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1

                if j < len(lines):
                    next_line = lines[j]
                    next_stripped = next_line.strip()
                    next_indent = _get_indentation(next_line)

                    # Only flag if the pass is at the correct body indentation level
                    if next_indent >= body_indent:
                        # Check if it's just 'pass' or a comment + pass
                        if next_stripped == 'pass':
                            findings.append((i + 1, line.strip()))
                        elif next_stripped.startswith('#') and j + 1 < len(lines):
                            # Check line after comment
                            after_line = lines[j + 1]
                            after_stripped = after_line.strip()
                            after_indent = _get_indentation(after_line)
                            if after_stripped == 'pass' and after_indent >= body_indent:
                                findings.append((i + 1, line.strip()))

            i += 1

    except Exception as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)

    return findings


def check_js_file(filepath: Path) -> list[tuple[int, str]]:
    """Check JavaScript/TypeScript file for empty catch blocks."""
    findings = []

    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Pattern for empty catch blocks: catch (...) { }
        # Handles multi-line with only whitespace/comments inside
        empty_catch_pattern = r'catch\s*\([^)]*\)\s*\{\s*\}'

        for match in re.finditer(empty_catch_pattern, content):
            # Find line number
            line_num = content[:match.start()].count('\n') + 1
            findings.append((line_num, 'catch block with empty body'))

        # Also check for .catch(() => {}) or .catch(e => {})
        promise_catch_pattern = r'\.catch\s*\(\s*\(?[^)]*\)?\s*=>\s*\{\s*\}\s*\)'

        for match in re.finditer(promise_catch_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            findings.append((line_num, '.catch() with empty callback'))

        # Check for catch with only console.log (often debug code)
        # This is a warning, not as severe
        catch_console_pattern = r'catch\s*\([^)]*\)\s*\{\s*console\.log[^}]*\}'

        for match in re.finditer(catch_console_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            findings.append((line_num, 'catch block only logs error (consider re-throwing)'))

    except Exception as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)

    return findings


def check_file(filepath: Path) -> list[tuple[int, str]]:
    """Check a file for empty catch blocks."""
    suffix = filepath.suffix.lower()

    if suffix == '.py':
        return check_python_file(filepath)
    elif suffix in ('.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'):
        return check_js_file(filepath)

    return []


def main(filenames: list[str]) -> int:
    """Main entry point for pre-commit hook."""
    all_findings: dict[str, list[tuple[int, str]]] = {}

    for filename in filenames:
        filepath = Path(filename)
        findings = check_file(filepath)

        if findings:
            all_findings[filename] = findings

    if all_findings:
        total = sum(len(f) for f in all_findings.values())
        file_count = len(all_findings)

        print(f'\nEmpty/suspicious catch blocks found: {total} in {file_count} file(s)\n')

        for filepath, findings in all_findings.items():
            print(f'  {filepath}:')
            for line_num, description in findings:
                print(f'    Line {line_num}: {description}')

        print('\nEmpty catch blocks silently swallow errors, making debugging hard.')
        print('Consider: logging, re-throwing, or handling the error properly.')
        print('This is a warning only - commit will proceed.\n')

    return 0  # Warning only


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
