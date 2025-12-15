#!/usr/bin/env python3
"""Pre-commit hook to detect overly long functions.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

AI assistants often write monolithic functions that do too many things.
Functions over 50 lines are hard to test, understand, and maintain.

Warns but doesn't block commits.
"""

import ast
import re
import sys
from pathlib import Path

MAX_FUNCTION_LENGTH = 50  # lines


def check_python_file(filepath: Path) -> list[tuple[int, str, int]]:
    """Check a Python file for long functions.

    Returns:
        List of (line_number, function_name, length) tuples
    """
    findings = []

    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content, filename=str(filepath))

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Calculate function length
                start_line = node.lineno
                end_line = node.end_lineno or start_line

                # Account for decorators
                if node.decorator_list:
                    start_line = node.decorator_list[0].lineno

                length = end_line - start_line + 1

                if length > MAX_FUNCTION_LENGTH:
                    findings.append((start_line, node.name, length))

    except SyntaxError:
        # Skip files with syntax errors (might be templates, etc.)
        pass
    except Exception as e:
        print(f'Error checking {filepath}: {e}', file=sys.stderr)

    return findings


def check_js_file(filepath: Path) -> list[tuple[int, str, int]]:
    """Check a JavaScript/TypeScript file for long functions.

    Uses brace counting with string/comment awareness.

    Returns:
        List of (line_number, function_name, length) tuples
    """
    findings = []

    # Patterns for function definitions
    function_patterns = [
        re.compile(r'function\s+(\w+)\s*\('),              # function name(
        re.compile(r'(\w+)\s*=\s*function\s*\('),          # name = function(
        re.compile(r'(\w+)\s*=\s*\([^)]*\)\s*=>'),         # name = () =>
        re.compile(r'(\w+)\s*=\s*async\s*\([^)]*\)\s*=>'), # name = async () =>
        re.compile(r'async\s+function\s+(\w+)\s*\('),      # async function name(
        re.compile(r'(\w+)\s*\([^)]*\)\s*\{'),             # method name() {
    ]

    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()

        # Remove strings and comments to avoid false brace counts
        cleaned_content = _remove_strings_and_comments_js(content)
        lines = content.split('\n')
        cleaned_lines = cleaned_content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]
            cleaned_line = cleaned_lines[i]

            # Check if line starts a function
            func_name = None
            for pattern in function_patterns:
                match = pattern.search(cleaned_line)
                if match:
                    func_name = match.group(1)
                    break

            if func_name:
                # Count lines until function ends using cleaned content
                start_line = i + 1
                brace_count = 0
                in_function = False
                j = i

                while j < len(cleaned_lines):
                    # Count braces in cleaned line
                    for char in cleaned_lines[j]:
                        if char == '{':
                            brace_count += 1
                            in_function = True
                        elif char == '}':
                            brace_count -= 1
                            if in_function and brace_count == 0:
                                # Function ended
                                length = j - i + 1
                                if length > MAX_FUNCTION_LENGTH:
                                    findings.append((start_line, func_name, length))
                                i = j
                                break
                    else:
                        j += 1
                        continue
                    break

            i += 1

    except Exception as e:
        print(f'Error checking {filepath}: {e}', file=sys.stderr)

    return findings


def _remove_strings_and_comments_js(content: str) -> str:
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


def check_file(filepath: Path) -> list[tuple[int, str, int]]:
    """Check a file for long functions based on extension."""
    suffix = filepath.suffix.lower()

    if suffix == '.py':
        return check_python_file(filepath)
    elif suffix in ('.js', '.jsx', '.ts', '.tsx'):
        return check_js_file(filepath)

    return []


def main(filenames: list[str]) -> int:
    """Main entry point for pre-commit hook."""
    all_findings: dict[str, list[tuple[int, str, int]]] = {}

    for filename in filenames:
        filepath = Path(filename)
        findings = check_file(filepath)

        if findings:
            all_findings[filename] = findings

    if all_findings:
        total = sum(len(f) for f in all_findings.values())

        print(f'\n⚠️  Long functions detected: {total} function(s) over {MAX_FUNCTION_LENGTH} lines\n')

        for filepath, findings in all_findings.items():
            print(f'  {filepath}:')
            for line_num, func_name, length in findings:
                print(f'    Line {line_num}: {func_name}() is {length} lines')

        print('\n💡 Tip: Break long functions into smaller, focused functions.')
        print('   Each function should do one thing well.')
        print('   Ask AI: "This function is too long. Break it into smaller functions."\n')

        # Warn only, don't block
        return 0

    return 0


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
