#!/usr/bin/env python3
"""Pre-commit hook to detect TODO/FIXME comments before committing.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

AI agents often write TODO comments as placeholders and move on.
This hook reminds you to address them before committing.

Warns about:
- TODO
- FIXME
- XXX
- HACK
- BUG
"""

import re
import sys
from pathlib import Path

TODO_PATTERNS = [
    (r'\bTODO\b', 'TODO'),
    (r'\bFIXME\b', 'FIXME'),
    (r'\bXXX\b', 'XXX'),
    (r'\bHACK\b', 'HACK'),
    (r'\bBUG\b', 'BUG'),
]

# File patterns to skip
SKIP_PATTERNS = [
    r'\.md$',           # Markdown files often have legitimate TODOs
    r'CHANGELOG',       # Changelog files
    r'TODO\.txt$',      # Dedicated TODO files
    r'TODO\.md$',
]


def should_skip_file(filepath: Path) -> bool:
    """Check if file should be skipped."""
    filepath_str = str(filepath)
    return any(re.search(pattern, filepath_str, re.IGNORECASE) for pattern in SKIP_PATTERNS)


def check_file(filepath: Path) -> list[tuple[int, str, str]]:
    """Check a file for TODO/FIXME comments.

    Returns:
        List of (line_number, keyword, line_content) tuples
    """
    if should_skip_file(filepath):
        return []

    findings = []

    try:
        with open(filepath, encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                for pattern, keyword in TODO_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append((line_num, keyword, line.strip()))
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

        print(f'\nTODO/FIXME comments found: {total} in {file_count} file(s)\n')

        for filepath, findings in all_findings.items():
            print(f'  {filepath}:')
            for line_num, keyword, line in findings[:3]:
                preview = line[:60] + '...' if len(line) > 60 else line
                print(f'    Line {line_num} [{keyword}]: {preview}')
            if len(findings) > 3:
                print(f'    ... and {len(findings) - 3} more')

        print('\nConsider addressing these before committing.')
        print('This is a warning only - commit will proceed.\n')

    return 0  # Warning only


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
