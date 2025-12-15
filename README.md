# Vibe and Thrive

**Pre-commit hooks that help you write better code with AI coding agents.**

When you're vibe coding with Claude, Cursor, Copilot, or other AI assistants, these hooks catch common patterns that lead to technical debt—before they hit your codebase.

## Why This Exists

AI coding agents are incredibly productive, but they can introduce subtle issues:

- **Duplicate code** - Agents often generate similar code blocks instead of extracting shared logic
- **Magic numbers** - Raw numbers scattered throughout instead of named constants
- **Hardcoded URLs** - `localhost:3000` instead of environment variables
- **Architecture mismatches** - Building ARM images when your server runs x86

These hooks act as guardrails, catching these patterns at commit time so you can fix them while the context is fresh.

## Quick Start

### 1. Install pre-commit

```bash
# macOS
brew install pre-commit

# pip
pip install pre-commit
```

### 2. Add to your project

Create or update `.pre-commit-config.yaml` in your project root:

```yaml
repos:
  - repo: https://github.com/allthriveai/vibe-and-thrive
    rev: v0.1.0  # Use the latest release
    hooks:
      - id: check-dry-violations-python
      - id: check-dry-violations-js
      - id: check-magic-numbers
      - id: check-hardcoded-urls
      - id: check-docker-platform
```

### 3. Install the hooks

```bash
pre-commit install
```

That's it! The hooks will run automatically on every commit.

## Available Hooks

### `check-dry-violations-python`

Detects code duplication in Python files using AST analysis:

- Duplicate code blocks (6+ consecutive similar lines)
- Repeated string literals (5+ occurrences of strings 40+ chars)
- Functions with identical bodies

```bash
# Warning output
DRY: 3 potential issue(s) in 2 file(s). Run with --verbose for details.
```

### `check-dry-violations-js`

Same analysis for JavaScript/TypeScript files:

- Duplicate code blocks
- Repeated string literals
- Repeated className patterns (React/Tailwind)

### `check-magic-numbers`

Flags hardcoded numbers that should be constants:

```python
# Bad
if retries > 5:
    timeout = 30000

# Good
MAX_RETRIES = 5
DEFAULT_TIMEOUT_MS = 30000
```

Allows common numbers: 0, 1, 2, -1, 100, 1000

### `check-hardcoded-urls`

Catches localhost/127.0.0.1 URLs that should use configuration:

```python
# Bad
API_URL = "http://localhost:8000/api"

# Good
API_URL = os.getenv("API_URL", "http://localhost:8000/api")
```

### `check-docker-platform`

Prevents ARM/x86 architecture mismatches when building Docker images on Apple Silicon for x86 servers:

- Checks `Dockerfile.prod` for `--platform` specification
- Validates docker-compose files
- Scans shell scripts for `docker build` commands

## Configuration

### Excluding Files

Each hook respects standard pre-commit exclude patterns:

```yaml
- id: check-dry-violations-python
  exclude: |
    (?x)^(
      .*/tests/.*|
      .*/migrations/.*
    )$
```

### Verbose Output

Run manually with verbose output:

```bash
pre-commit run check-dry-violations-python --all-files --verbose
```

## Philosophy

These hooks are designed to be **warnings, not blockers** (mostly). They alert you to potential issues but generally allow commits to proceed. The goal is awareness, not gatekeeping.

Hooks that block commits:
- `check-hardcoded-urls` - These are almost always bugs in production

Hooks that warn only:
- `check-dry-violations-*` - Duplication is sometimes intentional
- `check-magic-numbers` - Context matters
- `check-docker-platform` - May be handled in CI/CD

## Contributing

Found a pattern that AI agents commonly introduce? Open an issue or PR!

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with love by [AllThrive AI](https://allthrive.ai) for the vibe coding community.
