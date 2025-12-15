#!/usr/bin/env python3
"""Pre-commit hook to detect console.log used for error handling.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

AI assistants often use console.log in catch blocks instead of proper
error handling. This leads to silent failures and debugging nightmares.

Warns but doesn't block commits.
"""

import re
import sys
from pathlib import Path

# Pattern to find catch blocks with console.log
# This is a simplified check - looks for console.log near catch/except
PATTERNS = {
    'js': [
        # catch blocks with only console.log
        (r'catch\s*\([^)]*\)\s*{\s*console\.log', 'console.log in catch block'),
        (r'\.catch\s*\(\s*\([^)]*\)\s*=>\s*{\s*console\.log', 'console.log in .catch()'),
        (r'\.catch\s*\(\s*\([^)]*\)\s*=>\s*console\.log', 'console.log in .catch()'),
    ],
    'py': [
        # except blocks with only print
        (r'except[^:]*:\s*\n\s*print\s*\(', 'print() in except block'),
    ]
}


def check_file(filepath: Path) -> list[tuple[int, str]]:
    """Check a file for console.log/print in error handling.

    Returns:
        List of (line_number, issue_type) tuples
    """
    findings = []
    suffix = filepath.suffix.lower()

    if suffix in ('.js', '.jsx', '.ts', '.tsx'):
        patterns = PATTERNS['js']
    elif suffix == '.py':
        patterns = PATTERNS['py']
    else:
        return []

    try:
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            content = f.read()

        lines = content.split('\n')

        # Check for patterns in content
        for pattern, issue_type in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                # Find line number
                line_num = content[:match.start()].count('\n') + 1
                findings.append((line_num, issue_type))

        # Also check for catch blocks followed by console.log on next lines
        for i, line in enumerate(lines):
            line_num = i + 1  # 1-indexed line number for reporting

            # JavaScript catch
            if re.search(r'catch\s*\([^)]*\)\s*{?\s*$', line):
                # Check next few lines (j is 0-indexed)
                for j in range(i + 1, min(i + 4, len(lines))):
                    if 'console.log' in lines[j] and 'error' in lines[j].lower():
                        findings.append((j + 1, 'console.log for error handling'))
                        break

            # Python except
            if re.search(r'except\s+\w+[^:]*:\s*$', line) or re.search(r'except:\s*$', line):
                # Check next few lines (j is 0-indexed)
                for j in range(i + 1, min(i + 4, len(lines))):
                    next_line = lines[j]
                    if 'print(' in next_line and not re.search(r'#\s*noqa', next_line):
                        findings.append((j + 1, 'print() for error handling'))
                        break

    except Exception as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)

    # Deduplicate
    return list(set(findings))


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

        print(f'\n⚠️  Poor error handling detected: {total} instance(s)\n')

        for filepath, findings in all_findings.items():
            print(f'  {filepath}:')
            for line_num, issue_type in sorted(findings):
                print(f'    Line {line_num}: {issue_type}')

        print('\n💡 Tip: Use proper logging and error handling in catch blocks.')
        print('   - Log with appropriate level (error, warn)')
        print('   - Include context (what failed, relevant data)')
        print('   - Re-throw or handle gracefully')
        print('   - Don\'t just print and continue\n')

        # Warn only, don't block
        return 0

    return 0


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
