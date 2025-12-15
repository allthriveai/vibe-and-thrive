#!/usr/bin/env python3
"""Pre-commit hook to detect debug statements that may have been left in code.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

Warns about:
- console.log/debug/info (JS/TS)
- print() statements (Python)
- debugger statements (JS/TS)
- breakpoint() (Python)
- pdb/ipdb imports (Python)

Allows (doesn't flag):
- console.error, console.warn (legitimate logging)
- logger.* calls (proper logging)
- Lines with # noqa: debug or // noqa: debug comments
"""

import re
import sys
from pathlib import Path

# Patterns to detect debug statements
PYTHON_DEBUG_PATTERNS = [
    (r'^\s*print\s*\(', 'print()'),
    (r'^\s*breakpoint\s*\(', 'breakpoint()'),
    (r'^\s*import\s+pdb', 'pdb import'),
    (r'^\s*import\s+ipdb', 'ipdb import'),
    (r'^\s*from\s+pdb\s+import', 'pdb import'),
    (r'^\s*from\s+ipdb\s+import', 'ipdb import'),
    (r'pdb\.set_trace\s*\(', 'pdb.set_trace()'),
    (r'ipdb\.set_trace\s*\(', 'ipdb.set_trace()'),
]

JS_DEBUG_PATTERNS = [
    (r'console\.log\s*\(', 'console.log()'),
    (r'console\.debug\s*\(', 'console.debug()'),
    (r'console\.info\s*\(', 'console.info()'),
    (r'console\.table\s*\(', 'console.table()'),
    (r'console\.dir\s*\(', 'console.dir()'),
    (r'console\.trace\s*\(', 'console.trace()'),
    (r'^\s*debugger\s*;?\s*$', 'debugger'),
    (r'^\s*debugger\s*;?\s*//', 'debugger'),
]

# Patterns that indicate intentional/allowed usage
IGNORE_PATTERNS = [
    r'#\s*noqa:\s*debug',
    r'//\s*noqa:\s*debug',
    r'#\s*keep',
    r'//\s*keep',
    r'#\s*intentional',
    r'//\s*intentional',
    r'eslint-disable',
    r'logger\.',
    r'logging\.',
    r'log\.',
]


def check_file(filepath: Path) -> list[tuple[int, str, str]]:
    """Check a file for debug statements.

    Returns:
        List of (line_number, statement_type, line_content) tuples
    """
    findings = []
    suffix = filepath.suffix.lower()

    # Select patterns based on file type
    if suffix == '.py':
        patterns = PYTHON_DEBUG_PATTERNS
    elif suffix in ('.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'):
        patterns = JS_DEBUG_PATTERNS
    else:
        return []

    try:
        with open(filepath, encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Skip if line has ignore pattern
                if any(re.search(pattern, line, re.IGNORECASE) for pattern in IGNORE_PATTERNS):
                    continue

                # Skip if it's a comment line
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('//'):
                    continue

                # Check for debug patterns
                for pattern, name in patterns:
                    if re.search(pattern, line):
                        findings.append((line_num, name, line.strip()))
                        break

    except Exception as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)

    return findings


def main(filenames: list[str]) -> int:
    """Main entry point for pre-commit hook."""
    all_findings: dict[str, list[tuple[int, str, str]]] = {}

    for filename in filenames:
        filepath = Path(filename)
        findings = check_file(filepath)

        if findings:
            all_findings[filename] = findings

    if all_findings:
        total = sum(len(f) for f in all_findings.values())
        file_count = len(all_findings)

        print(f'\nDebug statements found: {total} in {file_count} file(s)\n')

        for filepath, findings in all_findings.items():
            print(f'  {filepath}:')
            for line_num, stmt_type, line in findings[:3]:  # Show first 3
                preview = line[:50] + '...' if len(line) > 50 else line
                print(f'    Line {line_num}: {stmt_type} - {preview}')
            if len(findings) > 3:
                print(f'    ... and {len(findings) - 3} more')

        print('\nTo suppress: add "# noqa: debug" or "// noqa: debug" comment')
        print('This is a warning only - commit will proceed.\n')

    return 0  # Warning only


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
