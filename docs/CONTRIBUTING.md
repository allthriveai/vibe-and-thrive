# Contributing to Vibe and Thrive

Found a pattern that AI agents commonly introduce? We'd love to add it!

## Adding a New Hook

### 1. Fork the repo

```bash
git clone https://github.com/allthriveai/vibe-and-thrive.git
cd vibe-and-thrive
```

### 2. Create your hook

Create a new file in `hooks/`:

```python
#!/usr/bin/env python3
"""Pre-commit hook to check for [your pattern].

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

[Explain what this hook catches and why it matters]

Warns but doesn't block commits.
"""

import sys
from pathlib import Path


def check_file(filepath: Path) -> list[tuple[int, str]]:
    """Check a file for [your pattern].

    Returns:
        List of (line_number, description) tuples
    """
    findings = []

    try:
        with open(filepath, encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Your detection logic here
                if should_flag(line):
                    findings.append((line_num, 'Description of issue'))

    except Exception as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)

    return findings


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

        print(f'\n⚠️  [Your issue] detected: {total} instance(s)\n')

        for filepath, findings in all_findings.items():
            print(f'  {filepath}:')
            for line_num, description in findings:
                print(f'    Line {line_num}: {description}')

        print('\n💡 Tip: [How to fix this issue]\n')

        # Return 0 for warnings, 1 to block commits
        return 0

    return 0


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
```

### 3. Register it in `.pre-commit-hooks.yaml`

```yaml
- id: check-your-pattern
  name: Check Your Pattern
  description: What it does
  entry: hooks/check_your_pattern.py
  language: python
  types_or: [python, javascript, ts, tsx]
```

### 4. Add to `pyproject.toml`

Add a CLI entry point:

```toml
[project.scripts]
vibe-check-yourpattern = "hooks.check_your_pattern:cli"
```

### 5. Add tests

Create `tests/test_check_your_pattern.py`:

```python
"""Tests for check_your_pattern.py hook."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'hooks'))

from check_your_pattern import check_file


class TestYourPattern:
    def test_detects_issue(self, tmp_path):
        test_file = tmp_path / 'test.py'
        test_file.write_text('problematic code here')

        findings = check_file(test_file)

        assert len(findings) == 1

    def test_ignores_valid_code(self, tmp_path):
        test_file = tmp_path / 'test.py'
        test_file.write_text('valid code here')

        findings = check_file(test_file)

        assert len(findings) == 0
```

### 6. Update documentation

- Add to `docs/HOOKS.md`
- Update the hook count in `README.md`

### 7. Submit a PR

```bash
git checkout -b add-check-your-pattern
git add .
git commit -m "Add check-your-pattern hook"
git push origin add-check-your-pattern
```

## Hook Guidelines

- **Warn by default** - Return `0` to allow commits, `1` only for security issues
- **Be specific** - Catch real problems, not style preferences
- **Allow suppression** - Support `# noqa:` comments
- **Skip tests** - Don't flag test files unless relevant
- **Clear messages** - Tell users what's wrong and how to fix it
- **Include tip** - Show how to fix the issue

## Ideas for New Hooks

Have an idea? We'd love contributions:

- `check-unused-imports` - Imports that aren't used
- `check-async-await` - Missing `await` on async calls
- `check-react-keys` - Missing keys in React lists
- `check-sql-injection` - SQL string concatenation
- `check-circular-imports` - Circular import detection
- `check-type-ignore` - Excessive `# type: ignore` comments

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## Code Style

We use:
- **Ruff** for Python linting and formatting
- **ESLint** for JavaScript/TypeScript

Run before committing:

```bash
ruff check hooks/
ruff format hooks/
```
