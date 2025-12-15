#!/usr/bin/env python3
"""Pre-commit hook to detect DRY violations and code duplication in Python files.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

Checks for:
1. Duplicate code blocks (similar consecutive lines)
2. Repeated string literals
3. Similar function implementations
"""

import ast
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Configuration
MIN_DUPLICATE_LINES = 6  # Minimum consecutive lines to flag as duplicate
MIN_STRING_LENGTH = 40  # Minimum string length to track for duplication
MIN_STRING_OCCURRENCES = 5  # How many times a string must appear to be flagged

# Files/directories to skip entirely
SKIP_PATTERNS = [
    r'.*/tests/.*',
    r'.*_test\.py$',
    r'.*test_.*\.py$',
    r'.*/migrations/.*',
    r'.*/conftest\.py$',
    r'.*/fixtures/.*',
    r'.*/scripts/.*',
    r'.*/docs/.*',
]

# Function name patterns to skip for "identical body" checks
SKIP_FUNCTION_PATTERNS = [
    r'^test_',
    r'^setUp$',
    r'^tearDown$',
    r'^__\w+__$',  # Dunder methods
]

# Body patterns to skip (these are acceptable to be identical)
SKIP_BODY_PATTERNS = [
    r'^pass$',
    r'^return None$',
    r'^return \[\]$',
    r'^return \{\}$',
    r'^return False$',
    r'^return True$',
    r'^raise NotImplementedError',
    r'^\.\.\.$',
]


class DuplicationChecker(ast.NodeVisitor):
    """AST visitor that detects various forms of code duplication."""

    def __init__(self, filename: str):
        self.filename = filename
        self.string_literals: list[tuple[int, str]] = []
        self.function_bodies: dict[str, tuple[int, str, str]] = {}
        self.findings: list[str] = []

    def visit_Constant(self, node: ast.Constant) -> None:
        """Track string literals."""
        if isinstance(node.value, str) and len(node.value) >= MIN_STRING_LENGTH:
            if not self._is_docstring_context(node) and not self._is_common_pattern(node.value):
                self.string_literals.append((node.lineno, node.value))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Track function bodies for similarity detection."""
        if any(re.match(pattern, node.name) for pattern in SKIP_FUNCTION_PATTERNS):
            self.generic_visit(node)
            return

        body_repr = self._normalize_function_body(node)

        if self._is_trivial_body(body_repr):
            self.generic_visit(node)
            return

        body_hash = hashlib.md5(body_repr.encode()).hexdigest()[:16]  # noqa: S324
        self.function_bodies[node.name] = (node.lineno, body_hash, body_repr)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Track async function bodies."""
        if any(re.match(pattern, node.name) for pattern in SKIP_FUNCTION_PATTERNS):
            self.generic_visit(node)
            return

        body_repr = self._normalize_function_body(node)

        if self._is_trivial_body(body_repr):
            self.generic_visit(node)
            return

        body_hash = hashlib.md5(body_repr.encode()).hexdigest()[:16]  # noqa: S324
        self.function_bodies[node.name] = (node.lineno, body_hash, body_repr)
        self.generic_visit(node)

    def _is_trivial_body(self, body_repr: str) -> bool:
        """Check if function body is too trivial to flag."""
        if not body_repr or len(body_repr) < 20:
            return True

        body_simple = body_repr.strip()
        for pattern in SKIP_BODY_PATTERNS:
            if re.match(pattern, body_simple, re.IGNORECASE):
                return True

        if body_repr.count('\n') == 0:
            if 'Return' in body_repr or 'Raise' in body_repr or 'Pass' in body_repr:
                return True

        return False

    def _is_docstring_context(self, node: ast.Constant) -> bool:
        """Check if this constant might be a docstring."""
        value = str(node.value)
        return value.startswith('"""') or value.startswith("'''") or (len(value) > 50 and '\n' in value)

    def _is_common_pattern(self, value: str) -> bool:
        """Check if string is a common pattern we should ignore."""
        common_patterns = [
            r'^https?://',  # URLs
            r'^/api/v\d+/',  # API paths
            r'^\w+@\w+\.\w+',  # Email patterns
            r'^[A-Z_]+$',  # Constant-like patterns
            r'^\d{4}-\d{2}-\d{2}',  # Date patterns
            r'^application/\w+',  # MIME types
            r'^Bearer ',  # Auth headers
            r'.*\.py$',  # File paths
        ]
        return any(re.match(pattern, value) for pattern in common_patterns)

    def _normalize_function_body(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Create normalized representation of function body for comparison."""
        body = node.body
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
            body = body[1:]

        if not body:
            return ''

        lines = []
        for stmt in body:
            stmt_repr = ast.dump(stmt)
            stmt_repr = re.sub(r"id='\w+'", "id='VAR'", stmt_repr)
            stmt_repr = re.sub(r"arg='\w+'", "arg='ARG'", stmt_repr)
            lines.append(stmt_repr)

        return '\n'.join(lines)

    def check_duplications(self) -> list[str]:
        """Run all duplication checks and return findings."""
        self._check_string_duplicates()
        self._check_similar_functions()
        return self.findings

    def _check_string_duplicates(self) -> None:
        """Check for repeated string literals."""
        string_counts = Counter(s for _, s in self.string_literals)

        for string, count in string_counts.items():
            if count >= MIN_STRING_OCCURRENCES:
                lines = [line for line, s in self.string_literals if s == string]
                preview = string[:50] + '...' if len(string) > 50 else string
                self.findings.append(
                    f'String literal repeated {count} times (lines {", ".join(map(str, lines))}): "{preview}"'
                )

    def _check_similar_functions(self) -> None:
        """Check for functions with identical or very similar bodies."""
        hash_groups: dict[str, list[tuple[str, int]]] = defaultdict(list)
        for name, (line, body_hash, _) in self.function_bodies.items():
            hash_groups[body_hash].append((name, line))

        for body_hash, funcs in hash_groups.items():
            if len(funcs) > 1 and body_hash:
                func_list = ', '.join(f'{name} (line {line})' for name, line in funcs)
                self.findings.append(f'Functions with identical bodies: {func_list}')


def check_consecutive_duplicates(lines: list[str]) -> list[tuple[int, int, list[str]]]:
    """Check for consecutive duplicate code blocks."""
    findings = []

    normalized = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            stripped = ''
        normalized.append(stripped)

    i = 0
    while i < len(normalized) - MIN_DUPLICATE_LINES:
        if not normalized[i]:
            i += 1
            continue

        if 'noqa: DRY' in lines[i] or 'noqa:DRY' in lines[i]:
            i += 1
            continue

        block = normalized[i : i + MIN_DUPLICATE_LINES]

        if _is_trivial_block(block):
            i += 1
            continue

        found_duplicate = False
        for j in range(i + MIN_DUPLICATE_LINES, len(normalized) - MIN_DUPLICATE_LINES + 1):
            if normalized[j : j + MIN_DUPLICATE_LINES] == block:
                if all(len(line) > 10 for line in block if line):
                    findings.append(
                        (
                            i + 1,
                            i + MIN_DUPLICATE_LINES,
                            [lines[i + k] for k in range(MIN_DUPLICATE_LINES)],
                        )
                    )
                    found_duplicate = True
                    break

        # Skip past this block if we found a duplicate to avoid multiple reports
        if found_duplicate:
            i += MIN_DUPLICATE_LINES
        else:
            i += 1

    return findings


def _is_trivial_block(block: list[str]) -> bool:
    """Check if a code block is too trivial to flag."""
    trivial_patterns = [
        r'^\s*$',
        r'^\s*#',
        r'^\s*pass\s*$',
        r'^\s*return\s*$',
        r'^\s*\.\.\.\s*$',
        r'^\s*\}\s*$',
        r'^\s*\]\s*$',
        r'^\s*\)\s*$',
        r"^\s*'\w+'\s*:\s*",
        r'^\s*"\w+"\s*:\s*',
        r'^\s*self\.\w+\s*=\s*\w+\s*$',
    ]

    trivial_count = 0
    for line in block:
        if any(re.match(pattern, line) for pattern in trivial_patterns):
            trivial_count += 1

    return trivial_count > len(block) / 2


def should_skip_file(filepath: Path) -> bool:
    """Check if file should be skipped based on path patterns."""
    filepath_str = str(filepath)
    return any(re.search(pattern, filepath_str) for pattern in SKIP_PATTERNS)


def check_file(filepath: Path) -> list[str]:
    """Check a file for DRY violations."""
    if should_skip_file(filepath):
        return []

    findings = []

    try:
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        try:
            tree = ast.parse(content)
            checker = DuplicationChecker(str(filepath))
            checker.visit(tree)
            findings.extend(checker.check_duplications())
        except SyntaxError:
            pass

        duplicates = check_consecutive_duplicates(lines)
        for start, end, dup_lines in duplicates:
            preview = dup_lines[0].strip()[:40] + '...'
            findings.append(f'Duplicate code block at lines {start}-{end}: {preview}')

    except Exception as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)

    return findings


def main(filenames: list[str]) -> int:
    """Main entry point for pre-commit hook."""
    all_findings: dict[str, list[str]] = {}

    for filename in filenames:
        filepath = Path(filename)
        findings = check_file(filepath)

        if findings:
            all_findings[filename] = findings

    if all_findings:
        total_issues = sum(len(f) for f in all_findings.values())
        file_count = len(all_findings)
        print(f'DRY: {total_issues} potential issue(s) in {file_count} file(s). Run with --verbose for details.')
        return 0  # Warning only

    return 0


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
