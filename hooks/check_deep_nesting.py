#!/usr/bin/env python3
"""Pre-commit hook to detect deeply nested code.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

AI assistants often create "pyramid of doom" code with many levels of nesting.
Deep nesting makes code hard to read and maintain.

Warns but doesn't block commits.
"""

import ast
import re
import sys
from pathlib import Path

MAX_NESTING_DEPTH = 4


class NestingVisitor(ast.NodeVisitor):
    """AST visitor to track nesting depth in Python code."""

    def __init__(self):
        self.findings = []
        self.depth = 0
        self.max_depth = 0
        self.deepest_line = 0

    def _visit_nested(self, node):
        """Visit a node that increases nesting depth."""
        self.depth += 1
        if self.depth > self.max_depth:
            self.max_depth = self.depth
            self.deepest_line = node.lineno

        if self.depth > MAX_NESTING_DEPTH:
            self.findings.append((node.lineno, self.depth))

        self.generic_visit(node)
        self.depth -= 1

    def visit_If(self, node):
        self._visit_nested(node)

    def visit_For(self, node):
        self._visit_nested(node)

    def visit_While(self, node):
        self._visit_nested(node)

    def visit_With(self, node):
        self._visit_nested(node)

    def visit_Try(self, node):
        self._visit_nested(node)

    def visit_FunctionDef(self, node):
        # Reset depth for each function
        old_depth = self.depth
        self.depth = 0
        self.generic_visit(node)
        self.depth = old_depth

    def visit_AsyncFunctionDef(self, node):
        # Reset depth for each function
        old_depth = self.depth
        self.depth = 0
        self.generic_visit(node)
        self.depth = old_depth


def check_python_file(filepath: Path) -> list[tuple[int, int]]:
    """Check a Python file for deep nesting.

    Returns:
        List of (line_number, depth) tuples
    """
    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content, filename=str(filepath))
        visitor = NestingVisitor()
        visitor.visit(tree)

        return visitor.findings

    except SyntaxError:
        return []
    except Exception as e:
        print(f'Error checking {filepath}: {e}', file=sys.stderr)
        return []


def check_js_file(filepath: Path) -> list[tuple[int, int]]:
    """Check a JavaScript/TypeScript file for deep nesting.

    Uses brace counting with string/comment awareness.

    Returns:
        List of (line_number, depth) tuples
    """
    findings = []

    # Control flow keywords that increase nesting
    nesting_patterns = [
        re.compile(r'\bif\s*\('),
        re.compile(r'\belse\s*\{'),
        re.compile(r'\bfor\s*\('),
        re.compile(r'\bwhile\s*\('),
        re.compile(r'\bswitch\s*\('),
        re.compile(r'\btry\s*\{'),
        re.compile(r'\bcatch\s*\('),
    ]

    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Remove strings and comments to avoid false positives
        cleaned_content = _remove_strings_and_comments(content)
        cleaned_lines = cleaned_content.split('\n')

        depth = 0
        for i, (line, cleaned_line) in enumerate(zip(lines, cleaned_lines), 1):
            # Count braces in cleaned line (no strings/comments)
            open_braces = cleaned_line.count('{')
            close_braces = cleaned_line.count('}')

            # Decrease depth for closing braces first
            depth = max(0, depth - close_braces)

            # Check if this line has nesting keywords
            has_nesting_keyword = any(p.search(cleaned_line) for p in nesting_patterns)

            # Increase depth for opening braces
            if open_braces > 0:
                depth += open_braces
                # Report if we exceeded max depth with a nesting keyword
                if has_nesting_keyword and depth > MAX_NESTING_DEPTH:
                    findings.append((i, depth))

    except Exception as e:
        print(f'Error checking {filepath}: {e}', file=sys.stderr)

    return findings


def _remove_strings_and_comments(content: str) -> str:
    """Remove string literals and comments from JavaScript/TypeScript code."""
    result = []
    i = 0
    in_single_quote = False
    in_double_quote = False
    in_template = False
    in_single_comment = False
    in_multi_comment = False

    while i < len(content):
        char = content[i]
        next_char = content[i + 1] if i + 1 < len(content) else ''
        prev_char = content[i - 1] if i > 0 else ''

        # Handle escape sequences
        if prev_char == '\\' and not (in_single_comment or in_multi_comment):
            result.append(' ')
            i += 1
            continue

        # Single-line comment
        if char == '/' and next_char == '/' and not (in_single_quote or in_double_quote or in_template or in_multi_comment):
            in_single_comment = True
            result.append(' ')
            i += 1
            continue

        # Multi-line comment start
        if char == '/' and next_char == '*' and not (in_single_quote or in_double_quote or in_template or in_single_comment):
            in_multi_comment = True
            result.append(' ')
            i += 1
            continue

        # Multi-line comment end
        if char == '*' and next_char == '/' and in_multi_comment:
            in_multi_comment = False
            result.append(' ')
            i += 2
            continue

        # End of single-line comment
        if char == '\n' and in_single_comment:
            in_single_comment = False
            result.append(char)
            i += 1
            continue

        # String handling
        if not (in_single_comment or in_multi_comment):
            if char == "'" and not (in_double_quote or in_template):
                in_single_quote = not in_single_quote
                result.append(' ')
                i += 1
                continue
            if char == '"' and not (in_single_quote or in_template):
                in_double_quote = not in_double_quote
                result.append(' ')
                i += 1
                continue
            if char == '`' and not (in_single_quote or in_double_quote):
                in_template = not in_template
                result.append(' ')
                i += 1
                continue

        # Output character or space
        if in_single_quote or in_double_quote or in_template or in_single_comment or in_multi_comment:
            result.append(' ' if char != '\n' else '\n')
        else:
            result.append(char)

        i += 1

    return ''.join(result)


def check_file(filepath: Path) -> list[tuple[int, int]]:
    """Check a file for deep nesting based on extension."""
    suffix = filepath.suffix.lower()

    if suffix == '.py':
        return check_python_file(filepath)
    elif suffix in ('.js', '.jsx', '.ts', '.tsx'):
        return check_js_file(filepath)

    return []


def main(filenames: list[str]) -> int:
    """Main entry point for pre-commit hook."""
    all_findings: dict[str, list[tuple[int, int]]] = {}

    for filename in filenames:
        filepath = Path(filename)
        findings = check_file(filepath)

        if findings:
            # Deduplicate findings (only report deepest per area)
            unique_findings = {}
            for line, depth in findings:
                if line not in unique_findings or depth > unique_findings[line]:
                    unique_findings[line] = depth

            all_findings[filename] = list(unique_findings.items())

    if all_findings:
        total = sum(len(f) for f in all_findings.values())

        print(f'\n⚠️  Deep nesting detected: {total} location(s) exceed {MAX_NESTING_DEPTH} levels\n')

        for filepath, findings in all_findings.items():
            print(f'  {filepath}:')
            for line_num, depth in sorted(findings):
                print(f'    Line {line_num}: {depth} levels deep')

        print('\n💡 Tip: Reduce nesting with early returns, guard clauses, or extraction.')
        print('   Ask AI: "Refactor this to reduce nesting depth."\n')

        # Warn only, don't block
        return 0

    return 0


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
