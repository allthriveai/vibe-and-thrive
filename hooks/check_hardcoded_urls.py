#!/usr/bin/env python3
"""Pre-commit hook to check for hardcoded URLs.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

Detects localhost and 127.0.0.1 URLs that should use environment variables
or configuration instead of hardcoded values.
"""

import re
import sys
from pathlib import Path

# Patterns to detect hardcoded URLs (pre-compiled for performance)
URL_PATTERNS = [
    re.compile(r'http://localhost:\d+'),
    re.compile(r'https://localhost:\d+'),
    re.compile(r'http://127\.0\.0\.1:\d+'),
    re.compile(r'https://127\.0\.0\.1:\d+'),
]

# Allowed patterns (exceptions, pre-compiled)
ALLOWED_PATTERNS = [
    re.compile(r'#.*http'),              # Comments
    re.compile(r'""".*http.*"""'),       # Docstrings
    re.compile(r"'''.*http.*'''"),       # Docstrings
    re.compile(r'//.*http'),             # JS/TS single-line comments
    re.compile(r'/\*.*http.*\*/'),       # JS/TS multi-line comments
    re.compile(r'import\.meta\.env\.\w+\s*\|\|\s*[\'"]http'),  # Vite env var fallback
    re.compile(r'process\.env\.\w+\s*\|\|\s*[\'"]http'),       # Node env var fallback
    re.compile(r'VITE_\w+.*http'),       # Vite config with env vars
    re.compile(r'os\.getenv\('),         # Python env var usage
    re.compile(r'os\.environ\.'),        # Python environ usage
    re.compile(r'\.env'),                # .env file references
    re.compile(r'getattr\(settings,'),   # Django settings with getattr (has env var lookup)
]


def check_file(filepath: Path) -> list[tuple[int, str]]:
    """Check a file for hardcoded URLs.

    Returns:
        List of (line_number, line_content) tuples for violations
    """
    violations = []

    try:
        with open(filepath, encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Skip if line matches allowed patterns
                if any(pattern.search(line) for pattern in ALLOWED_PATTERNS):
                    continue

                # Check for URL patterns
                for pattern in URL_PATTERNS:
                    if pattern.search(line):
                        violations.append((line_num, line.strip()))
                        break

    except Exception as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)

    return violations


def main(filenames: list[str]) -> int:
    """Main entry point for pre-commit hook.

    Returns:
        0 if no violations, 1 if violations found
    """
    has_violations = False

    for filename in filenames:
        filepath = Path(filename)
        violations = check_file(filepath)

        if violations:
            has_violations = True
            print(f'\nHardcoded URLs found in {filepath}:')
            for line_num, line in violations:
                print(f'  Line {line_num}: {line}')
            print('\n  Fix: Use environment variables or configuration instead')
            print('  Python: os.getenv("API_URL", "http://localhost:8000")')
            print('  JS/TS:  process.env.API_URL || "http://localhost:8000"')

    if has_violations:
        print('\n' + '=' * 60)
        print('FAIL: Hardcoded URLs detected')
        print('These will break in production!')
        print('=' * 60)
        return 1

    return 0


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
