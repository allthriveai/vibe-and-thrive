#!/usr/bin/env python3
"""Pre-commit hook to detect large blocks of commented-out code.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

AI assistants often comment out code instead of deleting it.
Version control exists for a reason—delete unused code.

Warns but doesn't block commits.
"""

import re
import sys
from pathlib import Path

# Minimum consecutive commented lines to trigger warning
MIN_COMMENT_BLOCK_SIZE = 5

# Patterns that look like commented-out code (not documentation)
CODE_PATTERNS = [
    r'^\s*#\s*(if|for|while|def|class|return|import|from|try|except)\b',
    r'^\s*#\s*\w+\s*=\s*',                    # variable assignment
    r'^\s*#\s*\w+\.\w+\(',                    # method call
    r'^\s*#\s*\w+\(',                          # function call
    r'^\s*//\s*(if|for|while|function|const|let|var|return|import|export|try|catch)\b',
    r'^\s*//\s*\w+\s*=\s*',                   # variable assignment
    r'^\s*//\s*\w+\.\w+\(',                   # method call
    r'^\s*//\s*\w+\(',                         # function call
    r'^\s*//\s*<\w+',                          # JSX
    r'^\s*//\s*}\s*$',                         # closing brace
    r'^\s*#\s*}\s*$',                          # closing brace
]

# Patterns that are acceptable comments (documentation, notes)
DOC_PATTERNS = [
    r'^\s*#\s*(TODO|FIXME|XXX|NOTE|HACK|BUG|WARNING):',
    r'^\s*#\s*noqa',
    r'^\s*#\s*type:\s*ignore',
    r'^\s*#\s*pylint:',
    r'^\s*#\s*pragma:',
    r'^\s*//\s*(TODO|FIXME|XXX|NOTE|HACK|BUG|WARNING):',
    r'^\s*//\s*eslint-',
    r'^\s*//\s*@ts-',
    r'^\s*#\s*-{3,}',                         # separator
    r'^\s*//-{3,}',                            # separator
    r'^\s*"""',                                # docstring
    r"^\s*'''",                                # docstring
    r'^\s*/\*\*',                              # JSDoc
    r'^\s*\*',                                 # JSDoc continuation
]


def is_code_comment(line: str) -> bool:
    """Check if a line looks like commented-out code."""
    # Skip if it looks like documentation
    for pattern in DOC_PATTERNS:
        if re.match(pattern, line, re.IGNORECASE):
            return False

    # Check if it looks like code
    for pattern in CODE_PATTERNS:
        if re.match(pattern, line):
            return True

    return False


def check_file(filepath: Path) -> list[tuple[int, int]]:
    """Check a file for blocks of commented-out code.

    Returns:
        List of (start_line, end_line) tuples for comment blocks
    """
    findings = []

    try:
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        block_start = None
        consecutive_comments = 0

        for i, line in enumerate(lines, 1):
            if is_code_comment(line):
                if block_start is None:
                    block_start = i
                consecutive_comments += 1
            else:
                if consecutive_comments >= MIN_COMMENT_BLOCK_SIZE:
                    findings.append((block_start, i - 1))
                block_start = None
                consecutive_comments = 0

        # Check final block
        if consecutive_comments >= MIN_COMMENT_BLOCK_SIZE:
            findings.append((block_start, len(lines)))

    except Exception as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)

    return findings


def main(filenames: list[str]) -> int:
    """Main entry point for pre-commit hook."""
    all_findings: dict[str, list[tuple[int, int]]] = {}

    for filename in filenames:
        filepath = Path(filename)

        # Skip non-code files
        if filepath.suffix.lower() not in ('.py', '.js', '.jsx', '.ts', '.tsx'):
            continue

        findings = check_file(filepath)

        if findings:
            all_findings[filename] = findings

    if all_findings:
        total = sum(len(f) for f in all_findings.values())

        print(f'\n⚠️  Commented-out code detected: {total} block(s)\n')

        for filepath, findings in all_findings.items():
            print(f'  {filepath}:')
            for start, end in findings:
                lines = end - start + 1
                print(f'    Lines {start}-{end}: {lines} lines of commented code')

        print('\n💡 Tip: Delete commented-out code. Use git to recover old code.')
        print('   If you need to keep it, explain why in a comment.\n')

        # Warn only, don't block
        return 0

    return 0


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
